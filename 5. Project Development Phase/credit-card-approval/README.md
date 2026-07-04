# Credit Card Approval Prediction System

An intelligent, machine-learning-based underwriting system that automates credit card approval decisions. By training predictive classifiers on historical demographic and financial profiles, the system evaluates applicant parameters to instantly flag low-risk (Approved) and high-risk (Rejected) applications, mimicking standard banking operations.

---

## 📂 Project Architecture

```text
creditcard_approval_project/
│
├── static/
│   ├── css/
│   │   └── style.css            # Premium dark-theme fintech stylesheet
│   └── images/
│       ├── approval_distribution.png  # EDA Chart: Target label proportions
│       ├── income_distribution.png    # EDA Chart: Income density vs status
│       ├── education_vs_approval.png  # EDA Chart: Education vs status
│       └── income_type_vs_approval.png# EDA Chart: Income type vs status
│
├── templates/
│   ├── home.html                # Underwriting dashboard & application form
│   └── result.html              # Dynamic eligibility outcome view
│
├── app.py                       # Flask web application & model inference
├── model.py                     # Machine learning training & evaluation pipeline
├── eda.py                       # Exploratory Data Analysis visualization script
├── credit_model.pkl             # Serialized production Random Forest model
├── application_record.csv       # Dataset: Demographic and financial profiles
├── credit_record.csv            # Dataset: Monthly payment status records
└── README.md                    # Project documentation (this file)
```

---

## 📊 Dataset & Feature Engineering

The system processes two core raw relational files:
1. **`application_record.csv`**: Contains applicant demographics, assets, and income details.
2. **`credit_record.csv`**: Tracks monthly payment status history (e.g., C = paid off, X = no loan, 0 = 1-29 days late, 1-5 = 30+ to 150+ days overdue).

### Target Label Formulation (Option B)
To ensure compliance and risk alignment:
- **Good / Approved (`0`)**: Applicants with clean histories, no loans, or minor 1-29 day delays (`C`, `X`, `0`).
- **Bad / Rejected (`1`)**: High-risk applicants with a record of payments overdue by 30 days or more (`1`, `2`, `3`, `4`, `5`).

### Underwriting Predictors (12 Features)
The models are trained strictly on the 12 features captured by the Flask app input form:
* `CODE_GENDER` (Male / Female)
* `FLAG_OWN_CAR` (Yes / No)
* `FLAG_OWN_REALTY` (Yes / No)
* `NAME_INCOME_TYPE` (Working, Associate, Pensioner, State, Student)
* `NAME_EDUCATION_TYPE` (Higher, Secondary, Incomplete, Lower, Academic)
* `NAME_FAMILY_STATUS` (Married, Single, Civil, Separated, Widow)
* `NAME_HOUSING_TYPE` (House, Rented, Municipal, Co-op, Office, Parents)
* `OCCUPATION_TYPE` (19 categories)
* `AMT_INCOME_TOTAL` (Annual Income)
* `DAYS_BIRTH` (Age in Years converted to negative days)
* `DAYS_EMPLOYED` (Employment duration converted to negative days; 365243 for unemployed)
* `CNT_FAM_MEMBERS` (Total family members count)

---

## ⚡ Machine Learning Model Evaluation

We trained and evaluated four classification algorithms on an 80/20 train-test stratified split. Due to local Application Control policies blocking dynamic DLLs like `xgboost.dll`, scikit-learn's `GradientBoostingClassifier` was utilized as our Gradient Boosting model.

| Classification Algorithm | Accuracy | Precision (Class 1) | Recall (Class 1) | F1-Score (Class 1) |
| :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 88.23% | 0.00% | 0.00% | 0.00% |
| **Decision Tree** | 88.30% | 50.46% | 32.17% | 39.29% |
| **Random Forest (Selected)** | **88.95%** | **54.87%** | **34.15%** | **42.10%** |
| **Gradient Boosting** | 88.25% | 60.00% | 0.35% | 0.70% |

*The **Random Forest Classifier** was chosen for deployment due to its superior accuracy, robustness, and balance in classifying high-risk profiles.*

---

## 🚀 Setup & Execution Guide

### Prerequisites
* Python 3.8 or above
* PIP package manager
* Virtual environment tool (`venv`)

### 1. Installation
Clone/navigate to your folder and install dependencies inside a virtual environment:
```powershell
# Open terminal and move to project directory
cd c:\Users\mahi9\Desktop\creditcard_approval_project

# Activate the existing virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat

# Update/Install dependencies (if needed)
pip install numpy pandas matplotlib seaborn scikit-learn Flask
```

### 2. Run Data Analysis (EDA)
Generate high-resolution distribution and correlation plots:
```bash
python eda.py
```
This saves visual charts inside `static/images/` to power the web dashboard.

### 3. Run Model Training
Train all classifiers, print diagnostic matrices, and save the best model:
```bash
python model.py
```
This outputs performance indicators and creates/saves `credit_model.pkl`.

### 4. Launch the Web Application
Execute the Flask server locally:
```bash
python app.py
```
Open your browser and navigate to **`http://127.0.0.1:5000`** to access the underwriting dashboard and run instant applicant evaluations!
