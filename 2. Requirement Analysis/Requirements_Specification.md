# Phase 2: Requirement Analysis & Specification

This document details the functional, non-functional, data, and system requirements for the Credit Card Approval Prediction System, along with user stories that define the operational acceptance criteria.

---

## 1. Functional Requirements (FR)

The functional requirements describe the system capabilities that the underwriting software must provide to its end-users (credit risk officers).

### FR-1: Underwriting Application Form (User Inputs)
The system must render a web-based form containing the following 12 key predictive parameters:
1. **Gender**: Binary selection (`Male` or `Female`).
2. **Car Ownership**: Binary selection (`Yes` or `No`).
3. **Real Estate Ownership**: Binary selection (`Yes` or `No`).
4. **Income Type**: Dropdown selecting from `Working`, `Commercial associate`, `Pensioner`, `State servant`, or `Student`.
5. **Education Type**: Dropdown selecting from `Higher education`, `Secondary / secondary special`, `Incomplete higher`, `Lower secondary`, or `Academic degree`.
6. **Family Status**: Dropdown selecting from `Civil marriage`, `Married`, `Single / not married`, `Separated`, or `Widow`.
7. **Housing Type**: Dropdown selecting from `Rented apartment`, `House / apartment`, `Municipal apartment`, `With parents`, `Co-op apartment`, or `Office apartment`.
8. **Occupation**: Dropdown selecting from 18 specific occupations (e.g., Laborers, Managers, Core staff) or `Unknown`.
9. **Annual Income**: Numerical input field (positive float) representing the applicant's total annual income.
10. **Age**: Numerical input field (positive integer) representing the applicant's age in years.
11. **Employment Duration**: Numerical input field (positive float) representing the applicant's employment history in years (0.0 for unemployed/retired).
12. **Family Members**: Numerical input field (positive integer) representing the total count of family members.

### FR-2: Business Rules / Policy Override Layer
Before sending applicant details to the machine learning model, the system must evaluate four hard-coded banking policy filters. If any rule triggers, the application must be immediately **REJECTED** without calling the ML model, reporting the specific rule breached:
* **Income Floor Rule**: Rejects any applicant earning less than **$15,000** annually.
* **Unemployed Student Rule**: Rejects any student who has **0** employment years.
* **Underage Unemployed Rule**: Rejects any applicant aged **18 or younger** who has **0** employment years.
* **Low-Income Student Rule**: Rejects any student with an annual income below **$20,000**.

### FR-3: Machine Learning Model Inference
* If all policy checks pass, the system must preprocess and feed the inputs to the trained Random Forest classifier.
* Features must undergo identical engineering to the training stage:
  * Compute `AGE_YEARS` (from user age).
  * Compute `IS_EMPLOYED` (1 if employment years > 0 else 0).
  * Compute `EMPLOYMENT_YEARS` (user employment years).
  * Compute `INCOME_PER_MEMBER` = `AMT_INCOME_TOTAL` / `CNT_FAM_MEMBERS` (capped at min 1 member).
  * Compute `EMPLOYMENT_RATIO` = `EMPLOYMENT_YEARS` / `AGE_YEARS`.
* Scale the engineered feature set using the pre-fitted `StandardScaler` (`scaler.pkl`).
* Predict the soft probability of rejection.
* If the probability of rejection is $\ge$ the calibrated rejection threshold (`threshold.pkl`, approximately `0.2312`), the system must classify the applicant as **REJECTED**. Otherwise, classify as **APPROVED**.

### FR-4: Interactive Underwriter Dashboard
The dashboard must display:
* A response screen indicating either a green **APPROVED** banner or a red **REJECTED** banner.
* Probability metrics showing the exact risk percentages (e.g., "Approved Probability: 78.4%", "Rejected Probability: 21.6%").
* A detailed policy log explaining whether a policy rule triggered or if the decision was determined via machine learning scoring.
* A summary table echoing the user-submitted parameters for underwriting record verification.
* Static Exploratory Data Analysis (EDA) charts demonstrating dataset trends (Income Density, Education Distributions, and Label Proportions).

---

## 2. Non-Functional Requirements (NFR)

The non-functional requirements define the operational qualities, performance bounds, and security constraints.

### NFR-1: Performance & Latency
* **Inference Speed**: The end-to-end classification pipeline (form submission, feature scaling, policy checking, model prediction, and template rendering) must complete in under **100 milliseconds** under local hosting conditions.
* **Model Size**: The serialized model artifacts (`credit_model.pkl`, `scaler.pkl`) must remain lightweight, fitting within standard memory constraints without requiring heavy GPU execution.

### NFR-2: Robustness & Validation
* **Input Sanitization**: The input form must validate numeric fields (e.g., preventing negative values for income, age, family members, or employment duration).
* **Missing Value Fallbacks**: The model pipeline must gracefully handle missing categories by mapping unrecognized parameters to safety categories like `Unknown` occupation.

### NFR-3: Security & Regulatory Compliance
* **Compliance with Computer Policy Constraints**: The system must run on local endpoints without attempting to load dynamic system-level libraries that trigger security blocks (e.g., utilizing scikit-learn's Random Forest instead of XGBoost when dynamic DLL execution of `xgboost.dll` is blocked by local App Control).
* **Data Anonymization**: The dashboard must not display or request Personally Identifiable Information (PII) such as Social Security Numbers, Names, or Addresses, maintaining alignment with consumer privacy guidelines (GDPR/CCPA frameworks).

### NFR-4: Reproducibility & Consistency
* The training pipeline must yield identical classifier outputs across executions by pinning the random seed (`random_state=42`).
* Feature scale parameters inside `scaler.pkl` must stay static between training runs and active runtime web sessions.

---

## 3. Data & System Requirements

### 3.1 Data Specification
The training pipeline requires two raw CSV files:
1. **`application_record.csv`**: Contains demographical data indexed by `ID`.
2. **`credit_record.csv`**: Contains billing and payment records spanning up to 60 historical months per client, indexed by `ID` and `MONTHS_BALANCE`.

### 3.2 Software Dependencies
* **Core Runtime**: Python 3.8+
* **Web Server**: Flask 2.0+ (Micro web framework)
* **Data Manipulation**: Pandas 1.3+, Numpy 1.20+
* **Machine Learning**: Scikit-Learn 1.0+ (Scalers, Ensembles, Metrics)
* **Sampling Libraries**: Imbalanced-Learn (for `SMOTE` oversampling)
* **Data Visualization**: Matplotlib 3.4+, Seaborn 0.11+
* **Serialization**: Pickle (Python built-in)

---

## 4. User Stories & Acceptance Criteria

### User Story 1: Automated Policy Filter Check
> **As a** Credit Risk Underwriter,  
> **I want** the system to immediately flag and filter out obviously high-risk applications (like students without jobs or incomes under $15k),  
> **So that** I don't waste time running machine learning inference or manual reviews on applications that violate our basic bank lending rules.
* **Acceptance Criteria**:
  * Inputting an income of $12,000 immediately returns a "REJECTED" screen.
  * The result page explicitly lists: `Policy Hard Reject Triggered: Annual income of $12,000 is below the minimum required threshold of $15,000.`
  * The ML probability calculations are bypassed, displaying a default `0.0% Approved` and `100.0% Rejected` panel.

### User Story 2: ML-Based Risk Decisioning
> **As a** Credit Committee Auditor,  
> **I want** the system to calculate a probability score based on the client's asset, family status, and employment data,  
> **So that** we can evaluate borderline files and make consistent decisions that optimize default rates.
* **Acceptance Criteria**:
  * Form details for an established Manager with $80,000 income are correctly scaled and evaluated by the Random Forest model.
  * The screen returns a green "APPROVED" classification.
  * The exact probability of approval is printed to the interface (e.g., `85.4% Approved`).
