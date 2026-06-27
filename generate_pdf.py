import os
from fpdf import FPDF

class ProjectPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, "Credit Card Approval Prediction System - Documentation", border=0, align="R")
            self.ln(10)
            # Add a thin gray horizontal line
            self.set_draw_color(220, 220, 220)
            self.line(10, 17, 200, 17)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", border=0, align="C")

def build_pdf():
    pdf = ProjectPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # ------------------ TITLE PAGE ------------------
    pdf.add_page()
    pdf.set_fill_color(245, 247, 250)
    pdf.rect(0, 0, 210, 297, "F") # Light background color for cover
    
    # Top Margin spacer
    pdf.ln(40)
    
    # Large Title
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(17, 24, 39) # Dark Charcoal
    pdf.multi_cell(0, 12, "CREDIT CARD APPROVAL\nPREDICTION SYSTEM", align="C")
    
    pdf.ln(10)
    # Colored accent bar
    pdf.set_fill_color(99, 102, 241) # Indigo Blue
    pdf.rect(70, 75, 70, 3, "F")
    
    pdf.ln(15)
    
    # Subtitle
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 8, "Machine Learning-Based Underwriting Automation\nEDA Insights, Classifiers Evaluation, and Web Application Guide", align="C")
    
    pdf.ln(90)
    
    # Metadata block at bottom
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(0, 6, "Developer Documentation", ln=True, align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "Powered by Scikit-Learn, Pandas, NumPy, and Flask", ln=True, align="C")
    pdf.cell(0, 6, "June 2026", ln=True, align="C")
    
    # ------------------ MAIN CONTENT ------------------
    pdf.add_page()
    pdf.set_text_color(17, 24, 39) # Reset color
    
    # 1. Project Overview
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(99, 102, 241) # Indigo Section headers
    pdf.cell(0, 10, "1. Project Overview", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    overview_text = (
        "Banks and financial institutions process thousands of credit card applications daily. "
        "Manually auditing every profile is highly resource-intensive and prone to human error. "
        "This project implements an automated, machine-learning-driven underwriting system. "
        "By training predictive classification models on historical customer demographic and "
        "financial profiles, the system evaluates applicant parameters to instantly flag low-risk "
        "profiles for approval and identify high-risk accounts to mitigate potential defaults."
    )
    pdf.multi_cell(0, 6, overview_text)
    pdf.ln(5)
    
    # 2. File & Folder Structure
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "2. Workspace Architecture", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Courier", "", 9.5)
    structure_text = (
        "creditcard_approval_project/\n"
        "|-- static/\n"
        "|   |-- css/style.css                # Premium dark-theme stylesheet\n"
        "|   |-- images/\n"
        "|       |-- approval_distribution.png # Distribution count chart\n"
        "|       |-- income_distribution.png   # Income distribution plot\n"
        "|       |-- education_vs_approval.png # Education vs approval plot\n"
        "|       |-- income_type_vs_approval.png# Income source vs approval plot\n"
        "|-- templates/\n"
        "|   |-- home.html                   # HTML: Dashboard and User Form\n"
        "|   |-- result.html                 # HTML: Decision display view\n"
        "|-- app.py                          # Flask routing and model server\n"
        "|-- model.py                        # Model training and export script\n"
        "|-- eda.py                          # EDA generator script\n"
        "|-- credit_model.pkl                # Production Random Forest Model\n"
        "|-- application_record.csv          # Dataset: Applicant demographic details\n"
        "|-- credit_record.csv               # Dataset: Monthly payment history"
    )
    pdf.multi_cell(0, 5, structure_text)
    pdf.ln(5)
    
    # 3. Preprocessing and Features
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "3. Feature Engineering & Mappings", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    feature_text = (
        "The model is trained strictly on the 12 features present in the Flask application input form:\n"
        "  - Gender (CODE_GENDER): Encoded as Male (1) or Female (0).\n"
        "  - Own Car (FLAG_OWN_CAR) / Own Realty (FLAG_OWN_REALTY): Encoded as Yes (1) or No (0).\n"
        "  - Income Source (NAME_INCOME_TYPE): Working, Associate, Pensioner, State servant, Student.\n"
        "  - Education Level (NAME_EDUCATION_TYPE): Higher, Secondary, Incomplete, Lower, Academic.\n"
        "  - Marital Status (NAME_FAMILY_STATUS) / Housing Type (NAME_HOUSING_TYPE).\n"
        "  - Occupation Sector (OCCUPATION_TYPE): Mapped across 19 unique industrial segments.\n"
        "  - Annual Income (AMT_INCOME_TOTAL): Total annual earnings of the client.\n"
        "  - Age (DAYS_BIRTH): Computed from years to negative days relative to evaluation.\n"
        "  - Employment Duration (DAYS_EMPLOYED): Computed to negative days; 365243 for unemployed.\n"
        "  - Family Members (CNT_FAM_MEMBERS): Total count of members in the household."
    )
    pdf.multi_cell(0, 6, feature_text)
    pdf.ln(5)

    # 4. Model Training Results
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "4. Classification Algorithms Performance", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, "The classifiers were evaluated using a stratified 80/20 train-test split on 36,457 integrated accounts. Minor payment delays (under 30 days) are grouped as Approved, and overdue durations exceeding 30 days are classified as High-Risk (Rejected).")
    pdf.ln(3)
    
    # Draw Model Metrics Table
    # Column Widths
    col_w = [55, 30, 35, 30, 30]
    headers = ["Model", "Accuracy", "Precision (C1)", "Recall (C1)", "F1-Score (C1)"]
    
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(99, 102, 241)
    pdf.set_text_color(255, 255, 255)
    
    # Table Header
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 8, h, border=1, align="C", fill=True)
    pdf.ln()
    
    # Table Data
    pdf.set_text_color(17, 24, 39)
    pdf.set_font("Helvetica", "", 9.5)
    data = [
        ["Logistic Regression", "88.23%", "0.00%", "0.00%", "0.00%"],
        ["Decision Tree", "88.30%", "50.46%", "32.17%", "39.29%"],
        ["Random Forest (Production)", "88.95%", "54.87%", "34.15%", "42.10%"],
        ["Gradient Boosting (Fallback)", "88.25%", "60.00%", "0.35%", "0.70%"]
    ]
    
    pdf.set_fill_color(249, 250, 251) # Alternate row color
    for row_idx, row in enumerate(data):
        fill = row_idx % 2 == 1
        # Check if Random Forest to highlight
        is_rf = "Random Forest" in row[0]
        if is_rf:
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(16, 185, 129) # Emerald Green for selected model
        else:
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(17, 24, 39)
            
        for i, val in enumerate(row):
            pdf.cell(col_w[i], 8, val, border=1, align="C", fill=fill)
        pdf.ln()
    
    pdf.set_text_color(17, 24, 39) # Reset text color
    pdf.ln(5)
    
    # 5. Instructions to Run
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 10, "5. System Operation & Execution Guide", ln=True)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.write(6, "Follow these steps to operate or modify the system:\n\n")
    
    # Bullet points
    bullet = chr(149)
    
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.write(6, f" {bullet} STEP 1: Activate Virtual Environment\n")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.write(6, "   Open terminal inside the project folder and activate the environment:\n")
    pdf.set_font("Courier", "", 9)
    pdf.write(6, "   PowerShell:  .\\venv\\Scripts\\Activate.ps1\n")
    pdf.write(6, "   CMD:         .\\venv\\Scripts\\activate.bat\n\n")
    
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.write(6, f" {bullet} STEP 2: Re-generate Visual Insights (EDA)\n")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.write(6, "   Re-process customer files and update saved count and distribution charts:\n")
    pdf.set_font("Courier", "", 9)
    pdf.write(6, "   Command:     python eda.py\n\n")
    
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.write(6, f" {bullet} STEP 3: Retrain Classifiers\n")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.write(6, "   Re-train all four algorithms and export the updated best model:\n")
    pdf.set_font("Courier", "", 9)
    pdf.write(6, "   Command:     python model.py\n\n")
    
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.write(6, f" {bullet} STEP 4: Start Underwriting Server\n")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.write(6, "   Run the Flask server and open the web dashboard:\n")
    pdf.set_font("Courier", "", 9)
    pdf.write(6, "   Command:     python app.py\n")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.write(6, "   Open your web browser and navigate to http://127.0.0.1:5000/\n")

    # Output file
    pdf.output("Credit_Card_Approval_System_Documentation.pdf")
    print("PDF documentation successfully generated as Credit_Card_Approval_System_Documentation.pdf!")

if __name__ == "__main__":
    build_pdf()
