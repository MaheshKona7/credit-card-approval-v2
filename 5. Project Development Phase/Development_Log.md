# Phase 5: Project Development Phase

This development log documents the engineering design choices, model selection process, feature engineering formulas, and calibration strategies implemented during the core development of the credit card approval system.

---

## 1. Feature Engineering Implementation

Raw variables like `DAYS_BIRTH` and `DAYS_EMPLOYED` are counter-intuitive (negative counts) and poorly scaled. We implemented a series of domain-specific feature transformations inside `model.py:engineer_features()` and mirrored them in the Flask runtime:

1. **`AGE_YEARS`**: Converts negative birth days to absolute age.
   $$\text{AGE\_YEARS} = \frac{|\text{DAYS\_BIRTH}|}{365.25}$$
2. **`IS_EMPLOYED`**: Binary indicator (1 if employed, 0 if unemployed). Checks for the dataset's unemployment sentinel value `365243`.
   $$\text{IS\_EMPLOYED} = \begin{cases} 0, & \text{if } \text{DAYS\_EMPLOYED} = 365243 \\ 1, & \text{otherwise} \end{cases}$$
3. **`EMPLOYMENT_YEARS`**: Converts negative employment days to absolute years, mapping the sentinel `365243` to `0.0`.
   $$\text{EMPLOYMENT\_YEARS} = \begin{cases} 0.0, & \text{if } \text{DAYS\_EMPLOYED} = 365243 \\ \frac{|\text{DAYS\_EMPLOYED}|}{365.25}, & \text{otherwise} \end{cases}$$
4. **`INCOME_PER_MEMBER`**: Captures per-capita purchasing power and financial obligations.
   $$\text{INCOME\_PER\_MEMBER} = \frac{\text{AMT\_INCOME\_TOTAL}}{\max(\text{CNT\_FAM\_MEMBERS}, 1)}$$
5. **`EMPLOYMENT_RATIO`**: Measures career stability relative to age.
   $$\text{EMPLOYMENT\_RATIO} = \frac{\text{EMPLOYMENT\_YEARS}}{\max(\text{AGE\_YEARS}, 1)}$$

---

## 2. Managing Class Imbalance

The merged dataset contains:
* **Approved (Class 0)**: 87.71% (31,686 cases)
* **Rejected (Class 1)**: 12.29% (4,440 cases)
* **Imbalance Ratio**: 7.14 : 1

To prevent classifiers from maximizing accuracy by predicting Class 0 for every applicant, we implemented two concurrent strategies:
1. **SMOTE (Synthetic Minority Over-Sampling)**: Applied **only** to the training split (`X_train_scaled`, `y_train`) to synthesize new synthetic default cases, creating a balanced 1:1 training ratio.
2. **Balanced Weights**: Configured estimators with `class_weight='balanced'` to further penalize misclassification of default cases.

---

## 3. Model Comparison & Selection

Four classifiers were trained and validated on an 80/20 stratified split. Since local machine security controls blocked the execution of dynamic C-compiled DLLs (precluding the use of XGBoost), we benchmarked scikit-learn models:

| Classification Model | Accuracy | Precision (Rejected) | Recall (Rejected) | F1-Score (Rejected) | Selection Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 88.23% | 0.00% | 0.00% | 0.00% | Rejected (predicted all 0s) |
| **Decision Tree** | 88.30% | 50.46% | 32.17% | 39.29% | Rejected (high variance) |
| **Random Forest** | **88.95%** | **54.87%** | **34.15%** | **42.10%** | **Selected (Best Balance & Robustness)** |
| **Gradient Boosting** | 88.25% | 60.00% | 0.35% | 0.70% | Rejected (failed on default class) |

---

## 4. Rejection Threshold Calibration

Using a standard classification threshold of `0.5` causes model underperformance due to the extreme class imbalance. 

To resolve this, we swept the **Precision-Recall (PR) Curve** on the validation split:
1. Computed predicted probabilities for the validation dataset: `proba_rejected = model.predict_proba(X_val_scaled)[:, 1]`.
2. Evaluated Precision ($P$) and Recall ($R$) at each threshold step.
3. Found the probability boundary that maximizes the minority F1-score:
   $$F_1 = \frac{2 \times P \times R}{P + R}$$
4. **Calibrated Threshold**: The sweep selected **`0.2312`** as the optimal cutoff. Any application with a rejection probability $\ge$ `0.2312` is rejected. This increased default detection (Recall) from near 0 to **34.15%** while keeping overall accuracy high at **88.95%**.

---

## 5. Policy Override Layer Integration

Machine learning models are statistical and can make counter-intuitive predictions on extreme edge cases where training data is sparse. To safeguard banking operations, we implemented a **Layer 1 Policy Override Engine** inside `app.py:apply_policy_rules()`. 

The web server evaluates this engine before calling the ML model:

```text
Incoming Application
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ check: Income < $15k?                                  │── Yes ──► REJECTED (Reason: Income Floor)
└────────────────────────────────────────────────────────┘
       │ No
       ▼
┌────────────────────────────────────────────────────────┐
│ check: Student AND Employment = 0?                      │── Yes ──► REJECTED (Reason: Unemployed Student)
└────────────────────────────────────────────────────────┘
       │ No
       ▼
┌────────────────────────────────────────────────────────┐
│ check: Age <= 18 AND Employment = 0?                   │── Yes ──► REJECTED (Reason: Underage Unemployed)
└────────────────────────────────────────────────────────┘
       │ No
       ▼
┌────────────────────────────────────────────────────────┐
│ check: Student AND Income < $20k?                      │── Yes ──► REJECTED (Reason: Low-Income Student)
└────────────────────────────────────────────────────────┘
       │ No
       ▼
┌────────────────────────────────────────────────────────┐
│ Pass to Layer 2: Machine Learning Inference            │
└────────────────────────────────────────────────────────┘
```
This hard-coded fallback layer ensures the system maintains risk-mitigation rules regardless of statistical variations in the ML classifier.
