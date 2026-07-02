# Phase 1: Brainstorming & Ideation

## 1. Problem Identification & Definition

### 1.1 Problem Statement
In the modern financial ecosystem, credit cards represent a significant portion of consumer lending. However, commercial banks and financial institutions face a critical operational bottleneck in evaluating and decisioning credit card applications. Traditionally, credit underwriting has been a manual or semi-automated process governed by rigid, heuristics-based credit scoring engines. This approach suffers from several key deficiencies:
- **Operational Inefficiencies**: Manual verification of applicant profiles and risk factors leads to high decisioning latency, ranging from several days to weeks, resulting in high customer churn.
- **Cognitive Overhead & Human Error**: Human underwriters must evaluate multiple socio-economic indicators (e.g., employment history, asset ownership, family size, and income tiers) simultaneously, leading to subjective and inconsistent decisions.
- **Inability to Capture Non-Linear Relationships**: Standard linear scorecards fail to capture non-linear, multi-dimensional correlations between applicant features (e.g., the interaction of employment ratio and income per family member) and their ultimate repayment behavior.

**Objective**: To build an intelligent, machine-learning-driven underwriting system that automates the screening process. By training predictive classifiers on historical consumer demographic and financial profiles, the system evaluates applicant parameters to instantly flag low-risk (Approved) and high-risk (Rejected) applications.

---

### 1.2 Need for the System
The current competitive landscape of consumer banking demands instant or near-instant decisions. Credit Card issuers must balance the objective of growing their customer base with the constraint of minimizing credit defaults (Non-Performing Assets - NPAs). 
- **Automated Screening**: Instantly filtering obviously qualified and unqualified candidates.
- **Data-Driven Risk Mitigation**: Leveraging historical payment data (`credit_record.csv`) to formulate objective risk scores instead of relying purely on subjective credit officer criteria.
- **Financial Inclusion**: Assessing demographic and stability metrics (e.g., employment ratios, home ownership) to score "thin-file" applicants who lack a deep history.

---

### 1.3 Current Challenges
1. **Class Imbalance**: Credit card default datasets are inherently imbalanced, with approved payers greatly outnumbering default payers (typically an 88% vs 12% ratio). Models trained on such data naturally skew toward approving everyone, missing high-risk cases.
2. **Data Sparsity & Anomalies**: Demographic datasets often contain missing values (e.g., unknown occupation types) and sentinel values (e.g., `365243` days employed to denote retirement or unemployment) that require robust preprocessing.
3. **Signal Strength Mismatch**: Short-term demographic features contain a weak overall statistical correlation to long-term payment delinquency. This requires advanced feature engineering to uncover hidden signals.

---

### 1.4 Business Value
- **Reduced Decision Latency**: Cuts screening times from days to milliseconds.
- **Improved Risk Selectivity**: A calibrated threshold reduces the approval of bad clients, minimizing charge-off rates and delinquency losses.
- **Reduced Customer Acquisition Cost (CAC)**: Provides a smoother digital onboarding process, reducing application abandonment.
- **Optimized Resource Allocation**: Frees up senior underwriters to focus on complex, borderline corporate accounts while automating standard consumer screenings.

---

## 2. Idea Prioritization

To define the scope of the system, a set of key capabilities were brainstormed and evaluated using a prioritization framework based on **Impact vs. Feasibility**:

| Proposed Feature / Idea | Technical Feasibility (1-5) | Business Impact (1-5) | Priority | Description / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| **Layered Policy Rules Engine** | 5 | 5 | **High (P0)** | Hard rules (e.g. minimum income floors) act as immediate filters before the ML model, ensuring regulatory compliance. |
| **SMOTE Over-Sampling** | 4 | 5 | **High (P0)** | Addresses the 88:12 class imbalance at training time to improve minority-class (Rejection) recall. |
| **Standard Feature Scaling Pipeline** | 5 | 4 | **High (P0)** | Ensures distance-based and tree-based models interpret high-magnitude features (income) and binary flags equally. |
| **Probability Threshold Calibration** | 4 | 5 | **High (P0)** | Sweeps the Precision-Recall curve to find the optimal threshold for F1-score optimization on default risk. |
| **Real-time Flask Dashboard** | 4 | 4 | **Medium (P1)**| A user-friendly web interface allowing underwriters to input parameters and instantly get decisions. |
| **Explainable AI (SHAP/LIME)** | 3 | 4 | **Low (P2)** | Provides localized explanation maps showing which features drove approval or rejection (Future scope). |

---

## 3. Stakeholders & Benefits

### 3.1 Primary Stakeholders
- **Credit Risk Officers & Underwriters**: The primary end-users who interact with the decisioning panel to process applications.
- **Data Science & ML Engineering Teams**: Responsible for training, deploying, monitoring, and retraining the model.
- **Product Managers & Business Analysts**: Focused on tracking approval rates, conversion performance, and charge-off metrics.
- **Compliance & Legal Auditing Teams**: Ensure the system does not violate fair lending regulations (e.g., avoiding gender-based bias in automated decisioning).

### 3.2 Benefits Table
| Stakeholder | Key Benefit |
| :--- | :--- |
| **Financial Institution** | Minimizes Non-Performing Assets (NPAs) through predictive risk management. |
| **Underwriting Team** | Eliminates manual review bottlenecks, standardizing screening outcomes. |
| **Applicant** | Experiences instant decisioning and immediate onboarding feedback. |

---

## 4. Empathy Map

Understanding the key users (Credit Risk Officers and Applicants) is critical for effective system design:

```text
+---------------------------------------------------------------------------------------------------+
|                                       USER: CREDIT UNDERWRITER                                    |
+---------------------------------------------------------------------------------------------------+
|  SAYS:                                                |  THINKS:                                  |
|  - "I spend too much time keying in data manually."   |  - "Is this applicant hiding debts?"      |
|  - "It takes days to get credit checks returned."     |  - "Will automated models replace me?"    |
|  - "I need to justify every rejection to auditors."   |  - "I want a clear, interpretable score." |
|-------------------------------------------------------+-------------------------------------------|
|  DOES:                                                |  FEELS:                                   |
|  - Compares income files, assets, and credit histories|  - Anxious about approving a default case.|
|  - Cross-checks applicant flags against policy rules. |  - Overwhelmed by high application volumes.|
|  - Manually logs rejection reasons in the database.   |  - Frustrated by slow legacy platforms.   |
+---------------------------------------------------------------------------------------------------+
```

---

## 5. Future Scope & Objectives

### 5.1 Objectives
- Establish a pipeline that achieves an accuracy of **>80%** on credit approval decisioning.
- Implement an automated fallback policy layer to protect the bank from edge-case approvals that statistical models miss.
- Build a lightweight web interface that simulates production underwriting.

### 5.2 Future Scope
- **Alternative Data Integration**: Incorporate utility bill payment records, mobile data usage, and transaction patterns to evaluate thin-file applicants.
- **Dynamic retraining loops**: Set up a continuous pipeline that ingests new payment data quarterly and retrains models dynamically.
- **Model Explainability (XAI)**: Integrate SHAP explainability charts directly into the Flask result interface, displaying which demographic factors contributed most to the risk evaluation.
