import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import numpy as np

# Disable grid globally
plt.rcParams.update({
    'font.size': 14,
    'axes.grid': False,          # ← Hides grid lines
    'axes.spines.top': False,
    'axes.spines.right': False
})

# Load and clean data
df = pd.read_excel('data/sales.xlsx', sheet_name='Sales Report')
df.columns = df.columns.str.strip()

# Fix European decimal commas
for col in ['Product Price', 'Order Quantity', 'Order Total']:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=False)
df_active = df[df['Order Status'] != 'Cancelled']

# Create large figure
fig = plt.figure(figsize=(28, 20))
gs = GridSpec(4, 2, figure=fig, height_ratios=[0.8, 2, 2, 2], hspace=0.5, wspace=0.3)

# Main title
fig.suptitle('Bicycle Sales Analysis Dashboard', fontsize=32, fontweight='bold', y=0.96)

# === KPI Banner (Top Row) ===
kpi_data = [
    ("Total Sales", f"${df_active['Order Total'].sum():,.0f}"),
    ("Total Quantity", f"{df_active['Order Quantity'].sum():,.0f}"),
    ("Avg. Order Value", f"${df_active['Order Total'].mean():,.2f}"),
    ("Total Orders", f"{len(df_active):,}"),
    ("Unique Customers", f"{df_active['Customer ID'].nunique():,}")
]

top_ax = fig.add_subplot(gs[0, :])
top_ax.axis('off')
x_positions = [0.1, 0.28, 0.46, 0.64, 0.82]
for i, (label, value) in enumerate(kpi_data):
    top_ax.text(x_positions[i], 0.7, value, ha='center', va='center', fontsize=22, fontweight='bold')
    top_ax.text(x_positions[i], 0.3, label, ha='center', va='center', fontsize=14)

# === Chart 1: Sales by Product Category ===
ax1 = fig.add_subplot(gs[1, 0])
cat_sales = df_active.groupby('Product Category')['Order Total'].sum().sort_values(ascending=False)
sns.barplot(x=cat_sales.values, y=cat_sales.index, hue=cat_sales.index, palette="viridis", ax=ax1, legend=False)
ax1.set_title('Sales by Product Category', fontsize=18, fontweight='bold')
ax1.set_xlabel('Sales ($)', fontsize=15)
ax1.tick_params(axis='y', labelsize=13)

# === Chart 2: Sales by Region ===
ax2 = fig.add_subplot(gs[1, 1])
region_sales = df_active.groupby('Product Region')['Order Total'].sum().sort_values(ascending=False)
sns.barplot(x=region_sales.values, y=region_sales.index, hue=region_sales.index, palette="magma", ax=ax2, legend=False)
ax2.set_title('Sales by Region', fontsize=18, fontweight='bold')
ax2.set_xlabel('Sales ($)', fontsize=15)
ax2.tick_params(axis='y', labelsize=13)

# === Chart 3: Monthly Sales Trend ===
ax3 = fig.add_subplot(gs[2, 0])
df_active['Month'] = df_active['Order Date'].dt.to_period('M')
monthly = df_active.groupby('Month')['Order Total'].sum()
ax3.plot(monthly.index.astype(str), monthly.values, marker='o', linewidth=3, color='steelblue', markersize=10)
ax3.set_title('Monthly Sales Trend', fontsize=18, fontweight='bold')
ax3.set_ylabel('Sales ($)', fontsize=15)
ax3.tick_params(axis='x', rotation=45, labelsize=13)

# === Chart 4: Top 10 Best-Selling Products ===
ax4 = fig.add_subplot(gs[2, 1])
top_prod = df_active.groupby('Product Name')['Order Total'].sum().nlargest(10)
sns.barplot(x=top_prod.values, y=top_prod.index, hue=top_prod.index, palette="rocket_r", ax=ax4, legend=False)
ax4.set_title('Top 10 Best-Selling Products', fontsize=18, fontweight='bold')
ax4.set_xlabel('Sales ($)', fontsize=15)
ax4.tick_params(axis='y', labelsize=12)
ax4.invert_yaxis()

# === Chart 5: Customer Feedback ===
ax5 = fig.add_subplot(gs[3, 0])
feedback = df_active['Customer Feedback'].value_counts()
feedback = feedback.reindex(['Positive', 'Neutral', 'Negative'], fill_value=0)
colors = {'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'}
ax5.pie(feedback.values, labels=feedback.index, autopct='%1.1f%%',
        colors=[colors.get(x, 'gray') for x in feedback.index],
        startangle=90, textprops={'color': 'white', 'weight': 'bold', 'fontsize': 14})
ax5.set_title('Customer Feedback Distribution', fontsize=18, fontweight='bold')

# === Chart 6: Payment & Shipping Methods (Fixed) ===
ax6 = fig.add_subplot(gs[3, 1])

payment = df_active['Payment Method'].value_counts()
shipping = df_active['Shipping Method'].value_counts()
all_labels = sorted(set(payment.index) | set(shipping.index))
x = np.arange(len(all_labels))

payment_vals = [payment.get(label, 0) for label in all_labels]
shipping_vals = [shipping.get(label, 0) for label in all_labels]

width = 0.35
ax6.bar(x - width/2, payment_vals, width, label='Payment Method', color='skyblue', alpha=0.9)
ax6.bar(x + width/2, shipping_vals, width, label='Shipping Method', color='salmon', alpha=0.9)

ax6.set_xticks(x)
ax6.set_xticklabels(all_labels, rotation=30, ha='right', fontsize=12)
ax6.set_title('Payment & Shipping Method Usage', fontsize=18, fontweight='bold')
ax6.set_ylabel('Number of Orders', fontsize=15)
ax6.legend(fontsize=13)

# === Export ===
plt.savefig('bicycle_sales_dashboard.png', dpi=300, bbox_inches='tight')
plt.savefig('bicycle_sales_dashboard.pdf', bbox_inches='tight')
plt.show()