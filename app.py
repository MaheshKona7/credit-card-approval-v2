from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the best-performing credit card approval model
with open('credit_model.pkl', 'rb') as f:
    model = pickle.load(f)

# ---------------------------------------------------------------------------
# Decision threshold for the ML model's rejection class.
# The dataset is heavily imbalanced (~88% Approved vs ~12% Rejected), so the
# model's raw output skews strongly toward approval. We lower this threshold
# below the default 0.5 to catch more true rejections.
# If P(Rejected) >= REJECTION_THRESHOLD → predict Rejected.
# ---------------------------------------------------------------------------
REJECTION_THRESHOLD = 0.40

# ---------------------------------------------------------------------------
# Income type encoding (must match the label-encoder used during training):
#   0 = Working  |  1 = Commercial associate  |  2 = Pensioner
#   3 = State servant  |  4 = Student
# ---------------------------------------------------------------------------
INCOME_TYPE_STUDENT = 4

# ---------------------------------------------------------------------------
# Minimum annual income required to qualify for a credit card.
# Applicants earning below this level are rejected via policy rule,
# regardless of what the ML model predicts.
# ---------------------------------------------------------------------------
MINIMUM_ANNUAL_INCOME = 15_000   # USD


def apply_policy_rules(annual_income, age, employment_years, income_type):
    """
    Hard business/policy rules that override the ML model for obviously
    high-risk profiles.  Real-world credit decisioning always layers policy
    filters on top of the statistical score to handle edge cases the model
    cannot reliably handle (especially when the training data is imbalanced).

    Returns:
        (reject: bool, reason: str | None)
        reject=True  → applicant is rejected; reason contains a human-readable note.
        reject=False → no hard rule triggered; fall through to ML model.
    """

    # Rule 1 – Absolute income floor
    # An annual income below $15 k is generally insufficient to service
    # revolving credit debt responsibly.
    if annual_income < MINIMUM_ANNUAL_INCOME:
        return True, (
            f"Annual income of ${annual_income:,.0f} is below the minimum "
            f"required threshold of ${MINIMUM_ANNUAL_INCOME:,.0f}."
        )

    # Rule 2 – Student with no employment history
    # A student who has never been employed (employment_years == 0) and has
    # no stable income source is a very high credit risk.
    if income_type == INCOME_TYPE_STUDENT and employment_years == 0:
        return True, (
            "Student applicants with no employment history represent an "
            "unacceptable credit risk due to absence of stable income."
        )

    # Rule 3 – Very young applicant (18) with zero employment
    # An 18-year-old with no work experience has no verifiable repayment
    # capacity and cannot demonstrate credit-worthiness.
    if age <= 18 and employment_years == 0:
        return True, (
            "Applicants aged 18 or younger with no employment history do not "
            "meet the minimum eligibility criteria."
        )

    # Rule 4 – Student + low income (even if slightly above the floor)
    # Students earning less than $20k annually still pose significant risk.
    if income_type == INCOME_TYPE_STUDENT and annual_income < 20_000:
        return True, (
            f"Student applicants with an annual income below $20,000 "
            f"(submitted: ${annual_income:,.0f}) do not qualify for credit."
        )

    return False, None   # No hard rule triggered – proceed to ML model


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # ── Extract inputs from the web form ─────────────────────────────────
        gender           = int(request.form['gender'])
        own_car          = int(request.form['own_car'])
        own_realty       = int(request.form['own_realty'])
        income_type      = int(request.form['income_type'])
        education        = int(request.form['education'])
        family_status    = int(request.form['family_status'])
        housing_type     = int(request.form['housing_type'])
        occupation       = int(request.form['occupation'])
        annual_income    = float(request.form['annual_income'])
        age              = int(request.form['age'])
        employment_years = float(request.form['employment_days'])
        family_members   = int(request.form['family_members'])

        # ── Layer 1: Policy / business rules ─────────────────────────────────
        # Check hard-reject conditions BEFORE running the ML model.
        # This prevents the imbalance-skewed model from approving profiles
        # that any reasonable underwriter would immediately decline.
        policy_reject, policy_reason = apply_policy_rules(
            annual_income, age, employment_years, income_type
        )

        if policy_reject:
            # Hard reject – bypass the ML model entirely.
            result = 'REJECTED'
            color  = 'red'
            # Set neutral proba values so the template can still display them.
            prob_approved = 0.0
            prob_rejected = 100.0
        else:
            # ── Layer 2: ML model scoring ─────────────────────────────────────
            # Convert Age (years) → DAYS_BIRTH (negative days, as in training data)
            days_birth = int(-age * 365.25)

            # Convert Employment (years) → DAYS_EMPLOYED
            # Unemployed / not-applicable applicants use sentinel value 365243
            # (this is the value present in the original Kaggle dataset).
            if employment_years == 0:
                days_employed = 365243
            else:
                days_employed = int(-employment_years * 365.25)

            # Feature order must exactly match the training pipeline:
            # CODE_GENDER, FLAG_OWN_CAR, FLAG_OWN_REALTY, NAME_INCOME_TYPE,
            # NAME_EDUCATION_TYPE, NAME_FAMILY_STATUS, NAME_HOUSING_TYPE,
            # OCCUPATION_TYPE, AMT_INCOME_TOTAL, DAYS_BIRTH, DAYS_EMPLOYED,
            # CNT_FAM_MEMBERS
            features = np.array([[
                gender, own_car, own_realty, income_type,
                education, family_status, housing_type,
                occupation, annual_income, days_birth,
                days_employed, family_members
            ]])

            # predict_proba gives soft probabilities; we apply our own threshold
            # instead of using model.predict()'s hard 0.5 cutoff, which over-
            # approves on this imbalanced dataset.
            # proba[0] = P(Approved/Good client), proba[1] = P(Rejected/Bad client)
            proba         = model.predict_proba(features)[0]
            prob_approved = proba[0]
            prob_rejected = proba[1]

            prediction = 1 if prob_rejected >= REJECTION_THRESHOLD else 0
            result     = 'APPROVED' if prediction == 0 else 'REJECTED'
            color      = 'green'    if prediction == 0 else 'red'

            prob_approved = round(prob_approved * 100, 1)
            prob_rejected = round(prob_rejected * 100, 1)

        # ── Build details dict for the result template ────────────────────────
        details = {
            'annual_income':   annual_income,
            'age':             age,
            'employment':      employment_years,
            'family_members':  family_members,
            'gender':          gender,
            'own_car':         own_car,
            'own_realty':      own_realty,
            'income_type':     income_type,
            'prob_approved':   prob_approved,
            'prob_rejected':   prob_rejected,
            'policy_reject':   policy_reject,
            'policy_reason':   policy_reason,
        }

        return render_template('result.html', result=result, color=color, details=details)

    except Exception as e:
        return (
            f'<div style="color:red; font-family:sans-serif; padding:2rem;">'
            f'<h3>Error Processing Request</h3><p>{str(e)}</p></div>'
        )


if __name__ == '__main__':
    app.run(debug=True)
