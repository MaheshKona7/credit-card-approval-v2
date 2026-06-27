import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("Loading data...")
app = pd.read_csv('application_record.csv')
credit = pd.read_csv('credit_record.csv')

# Unique mappings (aligned with Flask forms)
gender_map = {'F': 0, 'M': 1}
car_map = {'N': 0, 'Y': 1}
realty_map = {'N': 0, 'Y': 1}
income_map = {'Working': 0, 'Commercial associate': 1, 'Pensioner': 2, 'State servant': 3, 'Student': 4}
edu_map = {'Higher education': 0, 'Secondary / secondary special': 1, 'Incomplete higher': 2, 'Lower secondary': 3, 'Academic degree': 4}
fam_map = {'Civil marriage': 0, 'Married': 1, 'Single / not married': 2, 'Separated': 3, 'Widow': 4}
housing_map = {'Rented apartment': 0, 'House / apartment': 1, 'Municipal apartment': 2, 'With parents': 3, 'Co-op apartment': 4, 'Office apartment': 5}
occ_map = {'Accountants': 0, 'Cleaning staff': 1, 'Cooking staff': 2, 'Core staff': 3, 'Drivers': 4, 'HR staff': 5, 
           'High skill tech staff': 6, 'IT staff': 7, 'Laborers': 8, 'Low-skill Laborers': 9, 'Managers': 10, 
           'Medicine staff': 11, 'Private service staff': 12, 'Realty agents': 13, 'Sales staff': 14, 
           'Secretaries': 15, 'Security staff': 16, 'Waiters/barmen staff': 17, 'Unknown': 18}

# Preprocessing features
print("Preprocessing features...")
app_processed = app.copy()
app_processed = app_processed.drop_duplicates(subset='ID')
app_processed['OCCUPATION_TYPE'] = app_processed['OCCUPATION_TYPE'].fillna('Unknown')

# Apply mapping
app_processed['CODE_GENDER'] = app_processed['CODE_GENDER'].map(gender_map)
app_processed['FLAG_OWN_CAR'] = app_processed['FLAG_OWN_CAR'].map(car_map)
app_processed['FLAG_OWN_REALTY'] = app_processed['FLAG_OWN_REALTY'].map(realty_map)
app_processed['NAME_INCOME_TYPE'] = app_processed['NAME_INCOME_TYPE'].map(income_map)
app_processed['NAME_EDUCATION_TYPE'] = app_processed['NAME_EDUCATION_TYPE'].map(edu_map)
app_processed['NAME_FAMILY_STATUS'] = app_processed['NAME_FAMILY_STATUS'].map(fam_map)
app_processed['NAME_HOUSING_TYPE'] = app_processed['NAME_HOUSING_TYPE'].map(housing_map)
app_processed['OCCUPATION_TYPE'] = app_processed['OCCUPATION_TYPE'].map(occ_map)

# Preprocessing target (Option B)
# C, X, 0 -> 0 (Good / Approved)
# 1-5 -> 1 (Bad / Rejected)
print("Preprocessing target labels...")
status_map = {'C': 0, 'X': 0, '0': 0, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1}
credit['STATUS_NUM'] = credit['STATUS'].map(status_map)
target = credit.groupby('ID')['STATUS_NUM'].max().reset_index()
target.rename(columns={'STATUS_NUM': 'label'}, inplace=True)

# Merge features and target
df = app_processed.merge(target, on='ID', how='inner')
df = df.drop('ID', axis=1)
df = df.dropna()

# Extract exactly the 12 features that the Flask app uses
features_cols = [
    'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'NAME_INCOME_TYPE',
    'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE',
    'OCCUPATION_TYPE', 'AMT_INCOME_TOTAL', 'DAYS_BIRTH', 'DAYS_EMPLOYED',
    'CNT_FAM_MEMBERS'
]
X = df[features_cols]
y = df['label']

print(f"Dataset shape: {X.shape}")
print(f"Class counts:\n{y.value_counts()}")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Models list
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42)
}

best_model = None
best_acc = 0.0
best_name = ""

# Train and evaluate models
for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    if acc > best_acc:
        best_acc = acc
        best_model = model
        best_name = name

print(f"\nBest Model: {best_name} (Accuracy: {best_acc:.4f})")

# Save the best performing model
print("Saving best model to credit_model.pkl...")
with open('credit_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

print("Best model trained and saved successfully!")
