# Phase 8: Project Demonstration Guide

This guide serves as a manual for demonstrating the Credit Card Approval Prediction System to stakeholders, highlighting its features and testing specific user scenarios.

---

## 1. Interface Navigation

The system consists of two primary screens:

### 1.1 Underwriting Input Board (Home View)
* **Left Panel**: Consists of the 12-field input form capturing applicant demographic and financial metrics.
* **Right Panel**: Houses interactive EDA visualization graphs generated from the production datasets, showing the distribution of income tiers, target label ratios, and education parameters to help underwriters contextualize applicant demographics.

### 1.2 Decision Outcomes Dashboard (Result View)
* **Status Banner**: Displays a prominent, stylized outcome header: green `APPROVED` or red `REJECTED`.
* **Risk Probability Panel**: Visual progress bars mapping out the exact statistical likelihood of approval vs. rejection.
* **Policy Engine Logs**: Displays whether a policy rule overrode the decision, or if the result was computed using the machine learning model.
* **Applicant Summary**: Echoes back all input values for record-keeping and audit validation.

---

## 2. Scripted Demo Scenarios

Run these scenarios sequentially to showcase how the layered policy engines and ML classification behave.

### Scenario A: Low-Income Hard Policy Rejection
* **Purpose**: Demonstrates the Layer 1 Policy engine catching obvious high-risk profiles without calling the ML model.
* **Form Inputs**:
  * **Age**: `30`
  * **Income Type**: `Working`
  * **Occupation**: `Laborers`
  * **Annual Income**: `12500` *(Below the $15,000 threshold)*
  * **Employment Duration**: `4`
  * **Family Members**: `2`
  * *Other fields default.*
* **Expected Result**: **REJECTED**
* **Expected Log Detail**: `Policy Hard Reject Triggered: Annual income of $12,500 is below the minimum required threshold of $15,000.`
* **Probabilities**: `Approved: 0%` | `Rejected: 100%`

### Scenario B: Unemployed Student Rejection
* **Purpose**: Demonstrates the edge-case protection rules.
* **Form Inputs**:
  * **Age**: `20`
  * **Income Type**: `Student`
  * **Annual Income**: `35000`
  * **Employment Duration**: `0` *(Unemployed)*
  * **Family Members**: `1`
* **Expected Result**: **REJECTED**
* **Expected Log Detail**: `Policy Hard Reject Triggered: Student applicants with no employment history represent an unacceptable credit risk due to absence of stable income.`
* **Probabilities**: `Approved: 0%` | `Rejected: 100%`

### Scenario C: High-Income Approved Profile
* **Purpose**: Showcases standard ML-based approval processing.
* **Form Inputs**:
  * **Age**: `40`
  * **Income Type**: `Commercial associate`
  * **Education Type**: `Higher education`
  * **Occupation**: `Managers`
  * **Annual Income**: `95000`
  * **Employment Duration**: `9`
  * **Family Members**: `3`
  * **Owns Car / Realty**: `Yes` / `Yes`
* **Expected Result**: **APPROVED**
* **Expected Log Detail**: `Evaluation determined by Machine Learning Underwriting Pipeline.`
* **Probabilities**: High Approval Probability (e.g., `>85% Approved`).

### Scenario D: Borderline Applicant Evaluation
* **Purpose**: Demonstrates ML evaluation on a mid-risk worker.
* **Form Inputs**:
  * **Age**: `24`
  * **Income Type**: `Working`
  * **Education Type**: `Secondary / secondary special`
  * **Occupation**: `Drivers`
  * **Annual Income**: `24000`
  * **Employment Duration**: `1.2`
  * **Family Members**: `1`
  * **Owns Car / Realty**: `No` / `No`
* **Expected Result**: **APPROVED** (ML prediction using the calibrated rejection threshold).
* **Expected Log Detail**: `Evaluation determined by Machine Learning Underwriting Pipeline.`
