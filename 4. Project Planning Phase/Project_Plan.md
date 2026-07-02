# Phase 4: Project Planning Phase

This document outlines the project management methodology, Work Breakdown Structure (WBS), execution milestones, and risk assessment for developing the Credit Card Approval Prediction System.

---

## 1. SDLC Methodology & Agile Framework

The project is executed using the **Agile/Scrum** framework, allowing for iterative feedback, model testing, and dashboard refinements.
* **Sprint Cycles**: 1-week sprints focusing on specific areas (data setup, model training, policy engineering, testing).
* **Daily Sync**: Standups to review data preprocessing blockers and feature engineering metrics.
* **Retrospectives**: Completed at the end of each iteration to calibrate classification thresholds.

---

## 2. Work Breakdown Structure (WBS)

The deliverables are structured into five main categories:

```text
Credit Card Approval System
├── 1. Data Ingestion & EDA
│   ├── WBS 1.1: Relational Join of application and credit CSV files
│   ├── WBS 1.2: Class imbalance checking
│   └── WBS 1.3: Matplotlib static distribution plot creation
├── 2. Model Development
│   ├── WBS 2.1: Preprocessing & numeric encoding mappings
│   ├── WBS 2.2: Feature Engineering (Age/Employment ratios)
│   ├── WBS 2.3: SMOTE Oversampling pipeline implementation
│   └── WBS 2.4: Model comparison & Pickle serialization
├── 3. Underwriting Rules Integration
│   ├── WBS 3.1: Minimum income filter construction
│   └── WBS 3.2: Edge-case student/youth policy restrictions
├── 4. Interface Development
│   ├── WBS 4.1: Flask route configurations
│   └── WBS 4.2: Dark-theme CSS fintech styling
└── 5. Verification & Testing
    ├── WBS 5.1: Automated unit testing of routes and policies
    └── WBS 5.2: Precision-Recall threshold calibration validation
```

---

## 3. Milestones & Timeline

| Milestone | Target Deliverables | Status |
| :--- | :--- | :--- |
| **Milestone 1: Data Alignment** | Complete join on `ID`, establish target definitions (`0` = Clean, `1` = Delinquent). | Completed |
| **Milestone 2: Model Training** | Build SMOTE balanced RandomForest, calibrate probability threshold to maximize F1-score. | Completed |
| **Milestone 3: Web Server** | Set up Flask app, serialize inputs, and configure policy layer overrides. | Completed |
| **Milestone 4: Testing Suite** | Implement automated unit test suites verifying rules and models. | In Progress |
| **Milestone 5: Documentation**| Complete detailed project phase files and user demonstration guides. | In Progress |

---

## 4. Risk Analysis & Mitigation Matrix

A proactive analysis was conducted to handle structural, system, and statistical risks:

| Risk Category | Identified Risk | Impact | Risk Level | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Deployment / Environment** | Local Computer Policy blocks execution of dynamic libraries like `xgboost.dll`. | High | **High** | Fallback to `scikit-learn`'s `RandomForestClassifier` which is fully compiled inside native python/scipy ecosystems, avoiding unverified DLL loads. |
| **Data Quality** | Target label is heavily imbalanced (only 12.29% defaults). | High | **High** | 1. Ingest `SMOTE` to synthesize minority class elements on the training partition.<br>2. Set `class_weight='balanced'` in estimators.<br>3. Calibrate threshold using Precision-Recall curve to optimize minority F1-score rather than using default 0.5. |
| **Data Integrity** | Anomaly in dataset where unemployed/retired people have employment days = `365243`. | Medium| **Medium** | Filter out value `365243` by creating a boolean flag `IS_EMPLOYED` and setting `EMPLOYMENT_YEARS = 0` for these entries. |
| **Model Drift** | Applicants' demographic profiles or economic states change over time, rendering static rules obsolete. | Medium| **Medium** | Document a retraining frequency plan and save scalers (`scaler.pkl`) alongside feature structures to maintain alignment. |
