# Phase 7: User & API Manual

This document provides a comprehensive guide for setting up, running, configuring, and deploying the Credit Card Approval Prediction System.

---

## 1. Setup & Installation

### 1.1 Prerequisites
Ensure the following tools are installed on your system:
* **Python**: Version 3.8 or higher.
* **PIP**: Python Package Index.
* **Virtual Environment Creator**: Built-in `venv` library.

### 1.2 Installation Steps
Clone or navigate to the directory and run these commands:

1. **Navigate to the Project Root**:
   ```powershell
   cd c:\Users\mahi9\Desktop\creditcard_approval_project
   ```

2. **Establish and Activate the Virtual Environment**:
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Windows (CMD)
   .\venv\Scripts\activate.bat

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Core Dependencies**:
   ```bash
   pip install numpy pandas matplotlib seaborn scikit-learn Flask imbalanced-learn gunicorn
   ```

---

## 2. Operation & Script Execution

The workflow consists of three primary execution tasks:

### 2.1 Generating Explanatory Plots (EDA)
To run Exploratory Data Analysis and generate structural charts (e.g. Income Distributions, Target Label Proportions, etc.):
```bash
python eda.py
```
* **Output**: Exports high-resolution visual assets into the `static/images/` folder.

### 2.2 Model Training Pipeline
To run data merging, SMOTE balance operations, model fitting, threshold calibration, and artifact serialization:
```bash
python model.py
```
* **Outputs**:
  * `credit_model.pkl`: Best Random Forest model binary.
  * `scaler.pkl`: Fitted StandardScaler binary.
  * `threshold.pkl`: Calibrated float rejection threshold.
  * `feature_cols.pkl`: String list of ordered model inputs.

### 2.3 Launching the Web Server Locally
To start the Flask development server:
```bash
python app.py
```
* **Endpoint Access**: Open your web browser and navigate to **`http://127.0.0.1:5000/`**.

---

## 3. Web Service API Reference

The server exposes two routes:

### 3.1 Get Home View
* **Endpoint**: `/`
* **HTTP Method**: `GET`
* **Produces**: `text/html`
* **Response**: Returns the interactive underwriting input dashboard.

### 3.2 Post Prediction Request
* **Endpoint**: `/predict`
* **HTTP Method**: `POST`
* **Content-Type**: `application/x-www-form-urlencoded`
* **Parameters**:
  * `gender`: `0` (Female), `1` (Male)
  * `own_car`: `0` (No), `1` (Yes)
  * `own_realty`: `0` (No), `1` (Yes)
  * `income_type`: `0` (Working), `1` (Associate), `2` (Pensioner), `3` (State), `4` (Student)
  * `education`: `0` (Higher), `1` (Secondary), `2` (Incomplete), `3` (Lower), `4` (Academic)
  * `family_status`: `0` (Civil), `1` (Married), `2` (Single), `3` (Separated), `4` (Widow)
  * `housing_type`: `0` (Rented), `1` (House), `2` (Municipal), `3` (Parents), `4` (Co-op), `5` (Office)
  * `occupation`: Int mapping (0 to 18)
  * `annual_income`: Numerical annual salary value in USD
  * `age`: Age in years
  * `employment_days`: Employment history in years
  * `family_members`: Int size of household
* **Produces**: `text/html`
* **Response**: Renders `result.html` with decision status (Approved/Rejected), policy details (triggers and statements), and risk probabilities.

---

## 4. Deployment Instructions

### 4.1 Production WSGI Server Configuration
We use `gunicorn` as our production Web Server Gateway Interface (WSGI) runner. The project root contains a `Procfile` configured for easy deployment on platform-as-a-service providers (such as Heroku or Render):

```text
web: gunicorn app:app
```

### 4.2 Step-by-Step Render Deployment Guide
1. Push your project files (including directories 1 to 8) to a GitHub repository.
2. Log in to your Render dashboard and click **New Web Service**.
3. Link your GitHub repository.
4. Configure these runtime parameters:
   * **Runtime**: `Python`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app`
5. Click **Deploy Web Service**.
