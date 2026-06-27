import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend to run on server
import matplotlib.pyplot as plt
import seaborn as sns

print("Starting EDA generation...")

# Load datasets
app = pd.read_csv('application_record.csv')
credit = pd.read_csv('credit_record.csv')

# Preprocess target using Option B
# Good (0) = 'C', 'X', '0'
# Bad (1) = '1', '2', '3', '4', '5'
status_map = {'C': 0, 'X': 0, '0': 0, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1}
credit['STATUS_NUM'] = credit['STATUS'].map(status_map)

# Group by client and get maximum status (meaning if they ever had a 30+ day late payment, they are classified as Bad/1)
target = credit.groupby('ID')['STATUS_NUM'].max().reset_index()
target.rename(columns={'STATUS_NUM': 'label'}, inplace=True)

# Merge
df = app.merge(target, on='ID', how='inner')
df_clean = df.drop_duplicates(subset='ID').copy()
df_clean['OCCUPATION_TYPE'] = df_clean['OCCUPATION_TYPE'].fillna('Unknown')

# Set styling
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.family'] = 'sans-serif'

# 1. Count plot of Approval Status
plt.figure()
ax = sns.countplot(x='label', data=df_clean, hue='label', palette=['#10b981', '#ef4444'], legend=False)
plt.title('Distribution of Credit Card Approvals (Option B)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Application Status', fontsize=12)
plt.ylabel('Count', fontsize=12)
ax.set_xticklabels(['Approved (Good Risk)', 'Rejected (High Risk)'])
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{int(height):,}\n({height/len(df_clean)*100:.1f}%)',
                (p.get_x() + p.get_width() / 2., height / 2.0),
                ha='center', va='center', xytext=(0, 0), textcoords='offset points',
                color='white', fontweight='bold')
plt.tight_layout()
plt.savefig('static/images/approval_distribution.png', dpi=300)
plt.close()
print("Saved approval_distribution.png")

# 2. Distribution Plot of Annual Income by Approval Status (filtered to <= 500k to avoid extremely long tails)
plt.figure()
income_filtered = df_clean[df_clean['AMT_INCOME_TOTAL'] <= 500000]
ax = sns.kdeplot(data=income_filtered, x='AMT_INCOME_TOTAL', hue='label', fill=True, common_norm=False, palette=['#10b981', '#ef4444'], alpha=0.5, linewidth=2)
plt.title('Annual Income Distribution by Approval Status (Income <= $500,000)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Annual Income ($)', fontsize=12)
plt.ylabel('Density', fontsize=12)
# Custom legend
legend = ax.get_legend()
handles = legend.legend_handles
ax.legend(handles, ['Approved', 'Rejected'], title="Status")
plt.tight_layout()
plt.savefig('static/images/income_distribution.png', dpi=300)
plt.close()
print("Saved income_distribution.png")

# 3. Education level by Approval Status
plt.figure(figsize=(12, 7))
ax = sns.countplot(y='NAME_EDUCATION_TYPE', hue='label', data=df_clean, palette=['#10b981', '#ef4444'])
plt.title('Approval Status by Education Level', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Count', fontsize=12)
plt.ylabel('Education Level', fontsize=12)
# Custom legend
legend = ax.get_legend()
handles = legend.legend_handles
ax.legend(handles, ['Approved', 'Rejected'], title="Status")
plt.tight_layout()
plt.savefig('static/images/education_vs_approval.png', dpi=300)
plt.close()
print("Saved education_vs_approval.png")

# 4. Income Type by Approval Status
plt.figure(figsize=(12, 7))
ax = sns.countplot(y='NAME_INCOME_TYPE', hue='label', data=df_clean, palette=['#10b981', '#ef4444'])
plt.title('Approval Status by Income Type', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Count', fontsize=12)
plt.ylabel('Income Type', fontsize=12)
# Custom legend
legend = ax.get_legend()
handles = legend.legend_handles
ax.legend(handles, ['Approved', 'Rejected'], title="Status")
plt.tight_layout()
plt.savefig('static/images/income_type_vs_approval.png', dpi=300)
plt.close()
print("Saved income_type_vs_approval.png")

print("EDA generation complete successfully!")
