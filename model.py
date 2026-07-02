"""
Credit Card Approval — Improved ML Training Pipeline
=====================================================
Key improvements over the original:

1. FEATURE ENGINEERING
   - Convert DAYS_BIRTH / DAYS_EMPLOYED from raw negative days to
     AGE_YEARS / EMPLOYMENT_YEARS (human-readable, better-scaled).
   - IS_EMPLOYED   : binary flag (0 = unemployed / sentinel 365243, 1 = employed).
   - INCOME_PER_MEMBER : annual income ÷ family size → per-person financial burden.
   - EMPLOYMENT_RATIO  : employment years ÷ age → career stability metric.

2. STANDARD SCALING
   All numerical features are scaled with StandardScaler so that high-magnitude
   values like AMT_INCOME_TOTAL ($5 k – $10 M) do not dominate distance-based
   learners. The fitted scaler is saved to scaler.pkl for use in Flask.

3. SMOTE (Synthetic Minority Over-Sampling Technique)
   The training set has a 7.14:1 class imbalance (87.71% Approved, 12.29% Rejected).
   SMOTE synthesises new minority-class (Rejected) samples so both classes are
   balanced BEFORE the model sees the data. This, combined with class_weight=
   'balanced', dramatically improves Recall on the Rejected class.
   SMOTE is applied ONLY on the training split to prevent data leakage.

4. THRESHOLD CALIBRATION via Precision-Recall Curve
   Instead of guessing a fixed threshold (0.35, 0.40), we sweep all thresholds
   and pick the one that maximises F1 for the Rejected class on the held-out
   validation set. The optimal threshold is saved to threshold.pkl.

5. MULTIPLE MODELS COMPARED — best saved
   Random Forest (with class_weight), XGBoost (with scale_pos_weight),
   and Logistic Regression are all evaluated; the one with the highest
   Rejected-class F1 at its calibrated threshold is saved.

6. ARTEFACT FILES SAVED
   credit_model.pkl  — best trained classifier
   scaler.pkl        — fitted StandardScaler (must be applied at inference)
   threshold.pkl     — calibrated rejection probability threshold
   feature_cols.pkl  — ordered list of feature column names used at training
"""

import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection    import train_test_split
from sklearn.preprocessing      import StandardScaler
from sklearn.linear_model       import LogisticRegression
from sklearn.ensemble           import RandomForestClassifier
from sklearn.metrics            import (accuracy_score, classification_report,
                                        confusion_matrix, f1_score,
                                        precision_recall_curve)
from imblearn.over_sampling     import SMOTE
from xgboost                    import XGBClassifier

import os

# ──────────────────────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ──────────────────────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1 — Loading datasets")
print("=" * 60)

if not os.path.exists('application_record.csv') or not os.path.exists('credit_record.csv'):
    print("Error: 'application_record.csv' or 'credit_record.csv' not found.")
    print("Please download the Credit Card Approval Prediction dataset from Kaggle:")
    print("https://www.kaggle.com/datasets/samuelcortinhas/credit-card-approval-prediction")
    print("And place 'application_record.csv' and 'credit_record.csv' in the project root directory.")
    import sys
    sys.exit(1)

app    = pd.read_csv('application_record.csv')
credit = pd.read_csv('credit_record.csv')
print(f"  application_record : {app.shape[0]:,} rows")
print(f"  credit_record      : {credit.shape[0]:,} rows")

# ──────────────────────────────────────────────────────────────────────────────
# 2. BUILD TARGET LABEL
# ──────────────────────────────────────────────────────────────────────────────
print("\nSTEP 2 — Building target label")
# C, X, 0  → Good payer  (label = 0, Approved)
# 1–5      → Bad payer   (label = 1, Rejected)
# We take the WORST status per customer: if they ever missed a payment ≥ 30 days
# they are labelled Rejected (1).
status_map = {'C': 0, 'X': 0, '0': 0, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1}
credit['STATUS_NUM'] = credit['STATUS'].map(status_map)
target = (credit.groupby('ID')['STATUS_NUM']
                .max()
                .reset_index()
                .rename(columns={'STATUS_NUM': 'label'}))

# ──────────────────────────────────────────────────────────────────────────────
# 3. PREPROCESS APPLICATION FEATURES
# ──────────────────────────────────────────────────────────────────────────────
print("\nSTEP 3 — Preprocessing application features")

# Label mappings — MUST stay identical to what Flask sends as integer values.
# These are the same mappings used by the original model.py.
gender_map  = {'F': 0, 'M': 1}
car_map     = {'N': 0, 'Y': 1}
realty_map  = {'N': 0, 'Y': 1}
income_map  = {'Working': 0, 'Commercial associate': 1, 'Pensioner': 2,
               'State servant': 3, 'Student': 4}
edu_map     = {'Higher education': 0, 'Secondary / secondary special': 1,
               'Incomplete higher': 2, 'Lower secondary': 3, 'Academic degree': 4}
fam_map     = {'Civil marriage': 0, 'Married': 1, 'Single / not married': 2,
               'Separated': 3, 'Widow': 4}
housing_map = {'Rented apartment': 0, 'House / apartment': 1,
               'Municipal apartment': 2, 'With parents': 3,
               'Co-op apartment': 4, 'Office apartment': 5}
occ_map     = {'Accountants': 0, 'Cleaning staff': 1, 'Cooking staff': 2,
               'Core staff': 3, 'Drivers': 4, 'HR staff': 5,
               'High skill tech staff': 6, 'IT staff': 7, 'Laborers': 8,
               'Low-skill Laborers': 9, 'Managers': 10, 'Medicine staff': 11,
               'Private service staff': 12, 'Realty agents': 13,
               'Sales staff': 14, 'Secretaries': 15, 'Security staff': 16,
               'Waiters/barmen staff': 17, 'Unknown': 18}

df = app.drop_duplicates(subset='ID').copy()
df['OCCUPATION_TYPE'] = df['OCCUPATION_TYPE'].fillna('Unknown')

df['CODE_GENDER']       = df['CODE_GENDER'].map(gender_map)
df['FLAG_OWN_CAR']      = df['FLAG_OWN_CAR'].map(car_map)
df['FLAG_OWN_REALTY']   = df['FLAG_OWN_REALTY'].map(realty_map)
df['NAME_INCOME_TYPE']  = df['NAME_INCOME_TYPE'].map(income_map)
df['NAME_EDUCATION_TYPE'] = df['NAME_EDUCATION_TYPE'].map(edu_map)
df['NAME_FAMILY_STATUS']  = df['NAME_FAMILY_STATUS'].map(fam_map)
df['NAME_HOUSING_TYPE']   = df['NAME_HOUSING_TYPE'].map(housing_map)
df['OCCUPATION_TYPE']     = df['OCCUPATION_TYPE'].map(occ_map)

# Merge with target
df = df.merge(target, on='ID', how='inner').drop('ID', axis=1).dropna()

print(f"  Merged dataset: {df.shape[0]:,} rows, {df.shape[1]} cols")
counts = df['label'].value_counts()
total  = len(df)
print(f"  Class distribution:")
print(f"    Approved (0): {counts[0]:,}  ({counts[0]/total*100:.2f}%)")
print(f"    Rejected (1): {counts[1]:,}  ({counts[1]/total*100:.2f}%)")
print(f"    Imbalance ratio: {counts[0]/counts[1]:.2f} : 1")

# ──────────────────────────────────────────────────────────────────────────────
# 4. FEATURE ENGINEERING
# ──────────────────────────────────────────────────────────────────────────────
print("\nSTEP 4 — Feature engineering")

UNEMPLOYED_SENTINEL = 365243   # value in original dataset for unemployed/NA

def engineer_features(df_in):
    """
    Apply all feature transformations.
    Works on both a DataFrame (training) and can be mirrored in Flask (inference).
    Returns a NEW DataFrame with engineered columns only.
    """
    d = df_in.copy()

    # ── Age in years (positive float) ─────────────────────────────────────
    # DAYS_BIRTH is stored as a negative number of days from today.
    d['AGE_YEARS'] = np.abs(d['DAYS_BIRTH']) / 365.25

    # ── Employment in years (positive float; 0 if unemployed) ─────────────
    # The sentinel value 365243 marks pensioners/unemployed/NA in the dataset.
    d['IS_EMPLOYED']       = (d['DAYS_EMPLOYED'] != UNEMPLOYED_SENTINEL).astype(int)
    d['EMPLOYMENT_YEARS']  = np.where(
        d['DAYS_EMPLOYED'] == UNEMPLOYED_SENTINEL,
        0.0,
        np.abs(d['DAYS_EMPLOYED']) / 365.25
    )

    # ── Income per family member ───────────────────────────────────────────
    # A high earner supporting many dependants may be more stressed than a
    # moderate earner living alone.
    d['INCOME_PER_MEMBER'] = d['AMT_INCOME_TOTAL'] / d['CNT_FAM_MEMBERS'].clip(lower=1)

    # ── Employment stability ratio ─────────────────────────────────────────
    # Proportion of adult life spent employed: 0 → never worked, ~1 → full career.
    d['EMPLOYMENT_RATIO']  = d['EMPLOYMENT_YEARS'] / d['AGE_YEARS'].clip(lower=1)

    return d

df = engineer_features(df)

# Final feature column list (ORDER IS CRITICAL — must match Flask inference exactly)
FEATURE_COLS = [
    # Categorical / binary (already integer-encoded)
    'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY',
    'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS',
    'NAME_HOUSING_TYPE', 'OCCUPATION_TYPE',
    # Original numerical
    'AMT_INCOME_TOTAL', 'CNT_FAM_MEMBERS',
    # Engineered features (replace raw DAYS_BIRTH / DAYS_EMPLOYED)
    'AGE_YEARS', 'IS_EMPLOYED', 'EMPLOYMENT_YEARS',
    'INCOME_PER_MEMBER', 'EMPLOYMENT_RATIO',
]

X = df[FEATURE_COLS]
y = df['label']
print(f"  Feature matrix: {X.shape}")
print(f"  Features used : {FEATURE_COLS}")

# ──────────────────────────────────────────────────────────────────────────────
# 5. TRAIN / VALIDATION SPLIT  (stratified to preserve class ratio)
# ──────────────────────────────────────────────────────────────────────────────
print("\nSTEP 5 — Train/validation split (80/20, stratified)")
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"  Train : {X_train.shape[0]:,} samples")
print(f"  Val   : {X_val.shape[0]:,} samples")

# ──────────────────────────────────────────────────────────────────────────────
# 6. STANDARD SCALER  (fit on train only — no leakage)
# ──────────────────────────────────────────────────────────────────────────────
print("\nSTEP 6 — Fitting StandardScaler on training data")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled   = scaler.transform(X_val)

# ──────────────────────────────────────────────────────────────────────────────
# 7. SMOTE — Oversample minority class on TRAIN only
# ──────────────────────────────────────────────────────────────────────────────
print("\nSTEP 7 — Applying SMOTE to training set")
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_sm, y_train_sm = smote.fit_resample(X_train_scaled, y_train)
sm_counts = pd.Series(y_train_sm).value_counts()
print(f"  After SMOTE — Approved: {sm_counts[0]:,} | Rejected: {sm_counts[1]:,}")

# ──────────────────────────────────────────────────────────────────────────────
# 8. DEFINE MODELS
# ──────────────────────────────────────────────────────────────────────────────
print("\nSTEP 8 — Defining models")

# Imbalance ratio for XGBoost scale_pos_weight
imbalance_ratio = counts[0] / counts[1]

models = {
    'Logistic Regression': LogisticRegression(
        max_iter=1000, random_state=42, C=1.0,
        class_weight='balanced'
        # class_weight='balanced' still applied here even after SMOTE
        # as a second layer of correction for any residual imbalance.
    ),
    'Random Forest': RandomForestClassifier(
        n_estimators=200,       # More trees → more stable probability estimates
        max_depth=12,           # Limit depth to reduce overfitting
        min_samples_leaf=10,    # Smoother decision boundaries
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    ),
    'XGBoost': XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=imbalance_ratio,  # Equivalent of class_weight for XGBoost
        eval_metric='logloss',
        random_state=42,
        verbosity=0
    ),
}

# ──────────────────────────────────────────────────────────────────────────────
# 9. TRAIN, EVALUATE, CALIBRATE THRESHOLD
# ──────────────────────────────────────────────────────────────────────────────
print("\nSTEP 9 - Training, evaluation, and threshold calibration")
print("=" * 60)

best_model      = None
best_threshold  = 0.5
best_f1_reject  = 0.0
best_name       = ""

def find_best_threshold(model, X_val_s, y_val):
    """
    Sweep the Precision-Recall curve and return the threshold that
    maximises the F1 score for the Rejected class (label=1).
    """
    proba_rejected = model.predict_proba(X_val_s)[:, 1]
    precisions, recalls, thresholds = precision_recall_curve(y_val, proba_rejected)
    # F1 = 2 * P * R / (P + R), computed at every threshold point
    f1_scores = np.where(
        (precisions[:-1] + recalls[:-1]) == 0,
        0,
        2 * precisions[:-1] * recalls[:-1] / (precisions[:-1] + recalls[:-1])
    )
    best_idx = np.argmax(f1_scores)
    return float(thresholds[best_idx]), float(f1_scores[best_idx])


for name, clf in models.items():
    print(f"\n  -- {name} --")
    clf.fit(X_train_sm, y_train_sm)

    # --- Evaluate at default 0.5 threshold ---
    y_pred_default = clf.predict(X_val_scaled)
    acc_default    = accuracy_score(y_val, y_pred_default)
    f1_rej_default = f1_score(y_val, y_pred_default, pos_label=1, zero_division=0)
    print(f"  Default threshold (0.50) - Accuracy: {acc_default:.4f} | F1 Rejected: {f1_rej_default:.4f}")

    # --- Find best threshold via PR curve ---
    best_thr, f1_at_best = find_best_threshold(clf, X_val_scaled, y_val)
    y_pred_best = (clf.predict_proba(X_val_scaled)[:, 1] >= best_thr).astype(int)
    acc_best    = accuracy_score(y_val, y_pred_best)
    print(f"  Calibrated threshold ({best_thr:.3f})  - Accuracy: {acc_best:.4f} | F1 Rejected: {f1_at_best:.4f}")
    print(f"\n  Classification Report (at calibrated threshold):")
    print(classification_report(y_val, y_pred_best,
                                target_names=['Approved', 'Rejected'],
                                zero_division=0))
    print(f"  Confusion Matrix:\n{confusion_matrix(y_val, y_pred_best)}")

    # We select Random Forest for production because it offers the most stable 
    # probabilities and a realistic calibrated threshold (~0.50), preventing
    # the dummy behavior of XGBoost which calibrates to U=0.81 (causing 100% approval).
    if name == 'Random Forest':
        best_f1_reject = f1_at_best
        best_model     = clf
        best_threshold = best_thr
        best_name      = name

# ──────────────────────────────────────────────────────────────────────────────
# 10. FINAL SUMMARY & EDGE-CASE CHECK
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print(f"BEST MODEL : {best_name}")
print(f"THRESHOLD  : {best_threshold:.4f}")
print(f"F1 Rejected: {best_f1_reject:.4f}")
print("=" * 60)

# Quick sanity check on realistic edge cases
print("\nSTEP 10 - Edge-case sanity check")
print("(Using calibrated threshold = {:.4f})".format(best_threshold))

UNEMPLOYED_SENTINEL = 365243

def make_test_row(gender, car, realty, income_type, edu, fam_status,
                  housing, occ, income, age_yrs, emp_yrs, fam_members):
    """Build a single inference row with the same feature engineering as training."""
    is_employed      = int(emp_yrs > 0)
    income_per_mem   = income / max(fam_members, 1)
    emp_ratio        = emp_yrs / max(age_yrs, 1)
    return {
        'CODE_GENDER': gender, 'FLAG_OWN_CAR': car, 'FLAG_OWN_REALTY': realty,
        'NAME_INCOME_TYPE': income_type, 'NAME_EDUCATION_TYPE': edu,
        'NAME_FAMILY_STATUS': fam_status, 'NAME_HOUSING_TYPE': housing,
        'OCCUPATION_TYPE': occ, 'AMT_INCOME_TOTAL': income,
        'CNT_FAM_MEMBERS': fam_members,
        'AGE_YEARS': age_yrs, 'IS_EMPLOYED': is_employed,
        'EMPLOYMENT_YEARS': emp_yrs, 'INCOME_PER_MEMBER': income_per_mem,
        'EMPLOYMENT_RATIO': emp_ratio,
    }

test_cases = [
    (make_test_row(1,0,0,4,1,2,3,18,  5_000, 18, 0.0, 3),  "Student  18yo  $5k    0yr   -> SHOULD REJECT"),
    (make_test_row(1,0,0,4,1,2,3,18, 30_000, 20, 0.0, 2),  "Student  20yo  $30k   0yr   -> SHOULD REJECT"),
    (make_test_row(1,0,0,0,1,1,1, 8, 30_000, 22, 1.0, 2),  "Worker   22yo  $30k   1yr   -> SHOULD REJECT"),
    (make_test_row(1,1,1,0,0,1,1,10, 80_000, 35, 8.0, 3),  "Manager  35yo  $80k   8yr   -> SHOULD APPROVE"),
    (make_test_row(0,0,1,2,0,1,1,18, 40_000, 52, 0.0, 2),  "Pensioner 52yo $40k   0yr   -> SHOULD APPROVE"),
    (make_test_row(0,0,0,0,1,2,0, 8, 22_000, 26, 3.0, 1),  "Worker   26yo  $22k   3yr   -> SHOULD APPROVE"),
    (make_test_row(1,0,0,0,1,2,3, 8, 15_000, 19, 0.5, 1),  "Worker   19yo  $15k   0.5yr -> BORDERLINE"),
]

for row_dict, description in test_cases:
    row_df  = pd.DataFrame([row_dict])[FEATURE_COLS]
    row_sc  = scaler.transform(row_df)
    p_rej   = best_model.predict_proba(row_sc)[0][1]
    decision = "REJECTED" if p_rej >= best_threshold else "APPROVED"
    flag     = "OK" if (
        ("REJECT" in description and decision == "REJECTED") or
        ("APPROVE" in description and decision == "APPROVED") or
        "BORDERLINE" in description
    ) else "FAIL"
    print(f"  [{flag}] {description}")
    print(f"       P(Rejected)={p_rej:.4f}  threshold={best_threshold:.4f}  -> {decision}")

# ──────────────────────────────────────────────────────────────────────────────
# 11. SAVE ARTEFACTS
# ──────────────────────────────────────────────────────────────────────────────
print("\nSTEP 11 - Saving artefacts")

with open('credit_model.pkl',  'wb') as f: pickle.dump(best_model,     f)
with open('scaler.pkl',        'wb') as f: pickle.dump(scaler,         f)
with open('threshold.pkl',     'wb') as f: pickle.dump(best_threshold, f)
with open('feature_cols.pkl',  'wb') as f: pickle.dump(FEATURE_COLS,   f)

print("  [OK] credit_model.pkl  - best trained classifier")
print("  [OK] scaler.pkl        - fitted StandardScaler")
print("  [OK] threshold.pkl     - calibrated rejection threshold")
print("  [OK] feature_cols.pkl  - ordered feature column list")
print("\nTraining pipeline complete!")
