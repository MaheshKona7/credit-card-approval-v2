# Phase 6: Project Testing - Strategy & Matrix

This document defines the testing strategy, validation levels, test execution processes, and the detailed test matrix for the Credit Card Approval Prediction System.

---

## 1. Testing Strategy & Levels

We employ three validation tiers to verify system correctness, robustness, and compliance:

### 1.1 Unit Testing (Isolated Business Logic)
Focuses on evaluating `app.py:apply_policy_rules()` in isolation using mock attributes. This verifies that our four financial policy override rules trigger exactly as specified, protecting operations from statistical anomalies.

### 1.2 Integration Testing (Web Flow)
Uses Flask's built-in `test_client()` to simulate request payloads sent to `/predict`. We check that:
* HTTP status codes are `200 OK` for valid inputs.
* The system returns informative error descriptions for invalid datatypes or missing fields.
* The output HTML correctly contains the expected underwriting result banners (`APPROVED` or `REJECTED`) and probability strings.

### 1.3 Model Integration & Range Validation
Verifies that features are preprocessed correctly and that input scales match the training boundaries before calling the model classifier.

---

## 2. Test Scenarios Matrix

Below is the verification matrix containing edge-case candidate profiles:

| Test ID | Scenario Description | Inputs (Income, Age, Employment, Status) | Expected Decision | Verification Path |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Absolute income below floor | Income: `$10,000`<br>Age: `35`<br>Employment: `5.0 yrs`<br>Income Type: `Working` | **REJECTED** | **Layer 1 Policy Override** (Income Floor Rule) |
| **TC-02** | Unemployed student risk | Income: `$25,000`<br>Age: `20`<br>Employment: `0.0 yrs`<br>Income Type: `Student` | **REJECTED** | **Layer 1 Policy Override** (Unemployed Student Rule) |
| **TC-03** | Underage unemployed risk | Income: `$18,000`<br>Age: `18`<br>Employment: `0.0 yrs`<br>Income Type: `Working` | **REJECTED** | **Layer 1 Policy Override** (Underage Unemployed Rule) |
| **TC-04** | Low income student risk | Income: `$17,500`<br>Age: `22`<br>Employment: `2.0 yrs`<br>Income Type: `Student` | **REJECTED** | **Layer 1 Policy Override** (Low-Income Student Rule) |
| **TC-05** | High-income manager profile | Income: `$120,000`<br>Age: `42`<br>Employment: `12.0 yrs`<br>Income Type: `Commercial associate` | **APPROVED** | **Layer 2 Machine Learning Prediction** |
| **TC-06** | Stable pensioner profile | Income: `$45,000`<br>Age: `65`<br>Employment: `0.0 yrs`<br>Income Type: `Pensioner` | **APPROVED** | **Layer 2 Machine Learning Prediction** |
| **TC-07** | Borderline worker profile | Income: `$22,000`<br>Age: `24`<br>Employment: `1.5 yrs`<br>Income Type: `Working` | **APPROVED** | **Layer 2 Machine Learning Prediction** |

---

## 3. Automated Test Suite Execution

We provide an executable test suite in [test_app.py](file:///c:/Users/mahi9/Desktop/creditcard_approval_project/6.Project%20Testing/test_app.py).

### Running Tests
To run the automated tests, open your terminal, activate your virtual environment, and run the following python command:

```powershell
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Run the test suite
python -m unittest "6.Project Testing/test_app.py" -v
```

This will run all unit and integration test assertions, checking both policy triggers and route behavior.
