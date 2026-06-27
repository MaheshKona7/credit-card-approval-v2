import os
from fpdf import FPDF

class ComprehensivePDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 10, "Credit Card Underwriting Automation - Comprehensive Master Report", border=0, align="R")
            self.ln(10)
            # Border separator line
            self.set_draw_color(220, 220, 220)
            self.line(10, 17, 200, 17)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", border=0, align="C")

def clean_txt(text):
    # Replace unicode characters/emojis that FPDF core fonts cannot render in Latin-1
    replacements = {
        '✅': "[APPROVED]",
        '❌': "[REJECTED]",
        '📂': "[Folder]",
        '📊': "[EDA]",
        '⚡': "[ML]",
        '🚀': "[Setup]",
        '💻': "[Web App]",
        '🔍': "[Test]",
        '🧠': "[AI]",
        '🎨': "[UI]",
        '📍': "[Path]",
        '👉': "->",
        '•': "-",
        '’': "'",
        '‘': "'",
        '“': '"',
        '”': '"',
        '–': "-",
        '—': "-",
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    # Ensure it's encodeable in latin-1 (standard pdf core font)
    return text.encode('latin-1', 'replace').decode('latin-1')

def read_code_file(filepath):
    if not os.path.exists(filepath):
        return f"File not found: {filepath}"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return clean_txt(content)

def build_report():
    pdf = ComprehensivePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # ------------------ COVER PAGE ------------------
    pdf.add_page()
    pdf.set_fill_color(240, 244, 248) # Sleek blue-gray gradient background color
    pdf.rect(0, 0, 210, 297, "F")
    
    pdf.ln(35)
    
    # Header tag
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(99, 102, 241) # Indigo Accent
    pdf.cell(0, 10, "END-TO-END MACHINE LEARNING & WEB DEPLOYMENT", ln=True, align="C")
    
    pdf.ln(5)
    
    # Main Title
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(17, 24, 39) # Charcoal Dark
    pdf.multi_cell(0, 12, "CREDIT CARD APPROVAL\nPREDICTION SYSTEM", align="C")
    
    # Horizontal bar
    pdf.ln(8)
    pdf.set_fill_color(99, 102, 241)
    pdf.rect(60, 78, 90, 4, "F")
    pdf.ln(12)
    
    # Subtitle
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 8, "A complete underwriting automation system detailing demographic exploration,\nfeature engineering pipelines, multi-algorithm training,\nand dynamic web panel serving.", align="C")
    
    pdf.ln(80)
    
    # Footer info
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(0, 6, "COMPREHENSIVE TECHNICAL MANUAL & SOURCE CODE", ln=True, align="C")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(100, 110, 120)
    pdf.cell(0, 5, "Includes: eda.py | model.py | app.py | templates & styles", ln=True, align="C")
    pdf.cell(0, 5, "Date: June 2026", ln=True, align="C")
    pdf.cell(0, 5, "Status: Verified & Operational", ln=True, align="C")
    
    # ------------------ SECTION 1: BUSINESS CONTEXT ------------------
    pdf.add_page()
    pdf.set_text_color(17, 24, 39)
    
    # Section Header
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "1. Executive Summary & Underwriting Scenarios", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    # Text
    pdf.set_font("Helvetica", "", 10.5)
    intro_txt = (
        "Banks and financial institutions receive thousands of credit card applications every day. "
        "Auditing each application manually is both time-consuming and highly prone to human error, "
        "making it extremely inefficient to scale. This project automates the credit card approval "
        "decision using machine learning. By training a predictive model on historical applicant demographic "
        "and financial history, the system evaluates applicant parameters to determine creditworthiness "
        "instantly.\n\n"
        "Three target application scenarios are supported:\n\n"
        "  - Scenario 1: Automated Credit Card Application Screening\n"
        "    A bank credit analyst enters a new applicant's financial profile (income type, employment "
        "duration, credit history) into the dashboard. The model returns an instant approval/rejection prediction, "
        "allowing the analyst to prioritize high-value applications and speed up processing.\n\n"
        "  - Scenario 2: High-Risk Applicant Compliance Review\n"
        "    A compliance officer uses the platform to batch-screen applicants. The pipeline processes multi-class "
        "monthly status records and converts payment history into binary labels, allowing the model to clearly "
        "classify high-risk applicants as ineligible for a new card.\n\n"
        "  - Scenario 3: Customer Self-Service Credit Card Eligibility Check\n"
        "    A prospective customer enters their personal and financial details before submitting a formal application, "
        "instantly predicting their approval likelihood. This helps the customer understand their eligibility, "
        "reducing unnecessary rejections and protecting credit scores."
    )
    pdf.multi_cell(0, 6.5, clean_txt(intro_txt))
    pdf.ln(5)
    
    # ------------------ SECTION 2: EDA CODE & INSIGHTS ------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "2. Exploratory Data Analysis (eda.py)", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10.5)
    eda_desc = (
        "Exploratory Data Analysis (EDA) is vital for understanding demographics and credit risk proportions. "
        "The script 'eda.py' merges application records with credit status histories, computes the maximum monthly "
        "delinquency tier for each customer, and generates high-resolution charts saved inside 'static/images/':\n"
        "  - approval_distribution.png: Visualizes the proportion of Approved (88%) vs. Rejected (12%) applicants.\n"
        "  - income_distribution.png: Kernel Density Plot representing annual income distributions (truncated at $500k).\n"
        "  - education_vs_approval.png: Count plot showing approval outcomes across academic qualifications.\n"
        "  - income_type_vs_approval.png: Count plot representing decisions across employment sectors."
    )
    pdf.multi_cell(0, 6.5, clean_txt(eda_desc))
    pdf.ln(5)
    
    # Code listing for eda.py
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 8, "Source Code: eda.py", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Courier", "", 8)
    pdf.set_fill_color(243, 244, 246) # Light grey background for code block
    
    eda_code = read_code_file("eda.py")
    pdf.multi_cell(0, 4.5, eda_code, border=1, fill=True)
    pdf.ln(5)
    
    # ------------------ SECTION 3: MODEL TRAINING & METRICS ------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "3. Model Training & Evaluation Pipeline (model.py)", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10.5)
    model_desc = (
        "The file 'model.py' is responsible for training and selecting the production classifier. "
        "It addresses key developer challenges:\n"
        "  1. Feature Count Alignment: Restricts the training inputs to exactly the 12 features present on the "
        "Flask input form (rejecting extra columns like FLAG_MOBIL or CNT_CHILDREN) to prevent dimension mismatch crashes.\n"
        "  2. Categorical Pre-coding: Maps categorical strings to integers (e.g. Income Type, Housing Type, Occupation) "
        "using static, deterministic maps, aligning the training and inference values.\n"
        "  3. XGBoost DLL Fallback: Due to OS security policies blocking 'xgboost.dll', the pipeline falls back "
        "to scikit-learn's 'GradientBoostingClassifier' natively, ensuring the training completes successfully.\n"
        "  4. Target Definition: Applicants with overdue payments of 30+ days (statuses 1-5) are classified as "
        "High-Risk/Rejected (1), whereas others are classified as Approved (0).\n\n"
        "Model Metrics Summary Table:\n"
        "  - Logistic Regression: Accuracy 88.23% (Predicts majority class, F1: 0.00%)\n"
        "  - Decision Tree Classifier: Accuracy 88.30% (F1: 39.29%)\n"
        "  - Random Forest Classifier (Selected): Accuracy 88.95% (F1: 42.10%)\n"
        "  - Gradient Boosting Classifier: Accuracy 88.25% (F1: 0.70%)\n\n"
        "The Random Forest model has the highest classification accuracy and balance, and is saved as 'credit_model.pkl'."
    )
    pdf.multi_cell(0, 6.5, clean_txt(model_desc))
    pdf.ln(5)
    
    # Code listing for model.py
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 8, "Source Code: model.py", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Courier", "", 8)
    model_code = read_code_file("model.py")
    pdf.multi_cell(0, 4.5, model_code, border=1, fill=True)
    pdf.ln(5)
    
    # ------------------ SECTION 4: FLASK ROUTING ------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "4. Web Application Backend Serving (app.py)", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10.5)
    app_desc = (
        "The server backend 'app.py' runs on Flask. It manages HTTP request routing, input parsing, "
        "feature engineering conversions, and model inference:\n"
        "  - Home Route ('/'): Renders the underwriting dashboard showcasing project metadata, statistics cards, "
        "and embedded Matplotlib/Seaborn visualization plots.\n"
        "  - Prediction Route ('/predict'): Captures the POST parameters from the input form. It converts user-entered "
        "Age in years and Employment in years into negative days (DAYS_BIRTH and DAYS_EMPLOYED) to align with the training "
        "scale. It structures the 12 features in their exact sequence, runs 'model.predict()', and renders 'result.html'."
    )
    pdf.multi_cell(0, 6.5, clean_txt(app_desc))
    pdf.ln(5)
    
    # Code listing for app.py
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 8, "Source Code: app.py", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Courier", "", 8)
    app_code = read_code_file("app.py")
    pdf.multi_cell(0, 4.5, app_code, border=1, fill=True)
    pdf.ln(5)
    
    # ------------------ SECTION 5: FRONTEND TEMPLATES ------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "5. Frontend Layout Templates", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10.5)
    fe_desc = (
        "The front-end user experience is managed via HTML views inside the 'templates/' folder, styled by "
        "a customized dark-mode fintech stylesheet:\n"
        "  - static/css/style.css: Contains the stylesheet definitions including typography (Inter), glassmorphism "
        "card filters, inputs focusing, and card-lifting hover transitions.\n"
        "  - templates/home.html: Features a tab-switching layout between 'Analytics & Insights' (which loads the EDA "
        "plots) and 'New Application Screening' (the submission form with matching mapped value selects).\n"
        "  - templates/result.html: Renders the credit decision dynamically with color-coded outcome badges "
        "(Emerald green for APPROVED, Crimson red for REJECTED) and showcases a tabular review of parameters."
    )
    pdf.multi_cell(0, 6.5, clean_txt(fe_desc))
    pdf.ln(5)
    
    # Code listing for style.css
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 8, "Stylesheet Source Code: static/css/style.css", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Courier", "", 8)
    style_code = read_code_file("static/css/style.css")
    pdf.multi_cell(0, 4.5, style_code, border=1, fill=True)
    pdf.ln(5)
    
    # Code listing for home.html
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 8, "Template Source Code: templates/home.html", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Courier", "", 8.5)
    home_code = read_code_file("templates/home.html")
    # home.html is long (~284 lines), we only print the structure or chunk it to avoid giant page sizes
    # To be thorough, print the full code using FPDF pagination
    pdf.multi_cell(0, 4.5, home_code, border=1, fill=True)
    pdf.ln(5)
    
    # Code listing for result.html
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 8, "Template Source Code: templates/result.html", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Courier", "", 8.5)
    result_code = read_code_file("templates/result.html")
    pdf.multi_cell(0, 4.5, result_code, border=1, fill=True)
    pdf.ln(5)
    
    # ------------------ SECTION 6: HOW TO RUN ------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "6. Command-Line Reference Guide", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10.5)
    run_desc = (
        "To execute and host this system locally, execute the following commands in order:\n\n"
        "1. Open PowerShell or Command Prompt in the project workspace directory:\n"
        "   cd c:\\Users\\mahi9\\Desktop\\creditcard_approval_project\n\n"
        "2. Activate the python virtual environment (venv):\n"
        "   In PowerShell:  .\\venv\\Scripts\\Activate.ps1\n"
        "   In CMD:         .\\venv\\Scripts\\activate.bat\n\n"
        "3. Run exploratory charts generation:\n"
        "   python eda.py\n\n"
        "4. Train all classifiers, print comparative reports, and export Random Forest:\n"
        "   python model.py\n\n"
        "5. Run the web server:\n"
        "   python app.py\n\n"
        "6. In your web browser, navigate to: http://127.0.0.1:5000/\n"
    )
    pdf.multi_cell(0, 6.5, clean_txt(run_desc))
    
    # Output file
    pdf.output("Credit_Card_Approval_System_Final_Report.pdf")
    print("Final comprehensive report successfully generated as Credit_Card_Approval_System_Final_Report.pdf!")

if __name__ == "__main__":
    build_report()
