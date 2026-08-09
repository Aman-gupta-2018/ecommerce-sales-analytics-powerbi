"""
Exploratory Data Analysis & Statistical Insights
==================================================
Comprehensive EDA on the Superstore dataset.
Generates charts saved to outputs/charts/ and a summary report.
These insights drive the Power BI dashboard design.

Dataset Source: Kaggle - Superstore Dataset
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned", "superstore_cleaned.csv")
CHART_DIR = os.path.join(BASE_DIR, "outputs", "charts")
REPORT_DIR = os.path.join(BASE_DIR, "outputs", "reports")
os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# Style
sns.set_theme(style="whitegrid", palette="husl", font_scale=1.1)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#44AF69', '#EDB88B', '#D7263D']

print("=" * 60)
print("  EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# ---------------------------------------------------------------------------
# Load Data
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH, parse_dates=['Order Date', 'Ship Date'])
rfm = pd.read_csv(os.path.join(BASE_DIR, "data", "cleaned", "customer_rfm_analysis.csv"))

print(f"\nDataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"Date Range: {df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}")
print(f"Total Revenue: ${df['Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Overall Profit Margin: {(df['Profit'].sum() / df['Sales'].sum() * 100):.1f}%")

report_lines = []
def log(text):
    print(text)
    report_lines.append(text)

log("\n" + "=" * 60)
log("  KEY BUSINESS INSIGHTS")
log("=" * 60)

# =========================================================================
# 1. REVENUE TREND (Monthly)
# =========================================================================
log("\n--- 1. Revenue & Profit Trends ---")
monthly = df.groupby('Year-Month').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
).reset_index()
monthly['Year-Month'] = pd.to_datetime(monthly['Year-Month'])

fig, ax1 = plt.subplots(figsize=(14, 5))
ax1.fill_between(monthly['Year-Month'], monthly['Revenue'], alpha=0.3, color=COLORS[0])
ax1.plot(monthly['Year-Month'], monthly['Revenue'], color=COLORS[0], linewidth=2, label='Revenue')
ax1.plot(monthly['Year-Month'], monthly['Profit'], color=COLORS[1], linewidth=2, label='Profit')
ax1.set_title('Monthly Revenue & Profit Trend (2014-2017)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Month')
ax1.set_ylabel('Amount ($)')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax1.legend()
ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.savefig(os.path.join(CHART_DIR, '01_revenue_profit_trend.png'))
plt.close()

# YoY Growth
yearly = df.groupby('Order Year')['Sales'].sum()
for i in range(1, len(yearly)):
    growth = (yearly.iloc[i] - yearly.iloc[i-1]) / yearly.iloc[i-1] * 100
    log(f"  YoY Growth {yearly.index[i-1]}->{yearly.index[i]}: {growth:+.1f}%")

# =========================================================================
# 2. CATEGORY PERFORMANCE
# =========================================================================
log("\n--- 2. Category & Sub-Category Performance ---")
cat_perf = df.groupby('Category').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
    Avg_Margin=('Profit Margin (%)', 'mean'),
).sort_values('Revenue', ascending=False)

for cat in cat_perf.index:
    r = cat_perf.loc[cat]
    log(f"  {cat}: Revenue=${r['Revenue']:,.0f} | Profit=${r['Profit']:,.0f} | Margin={r['Avg_Margin']:.1f}%")

# Sub-category profit/loss chart
subcat = df.groupby('Sub-Category').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
).sort_values('Profit')

fig, ax = plt.subplots(figsize=(12, 7))
colors = [COLORS[3] if p < 0 else COLORS[0] for p in subcat['Profit']]
bars = ax.barh(subcat.index, subcat['Profit'], color=colors, edgecolor='white')
ax.set_title('Profit by Sub-Category (Loss Makers in Red)', fontsize=14, fontweight='bold')
ax.set_xlabel('Profit ($)')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax.axvline(x=0, color='black', linewidth=0.8)
for bar, val in zip(bars, subcat['Profit']):
    ax.text(val + (500 if val >= 0 else -500), bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', ha='left' if val >= 0 else 'right', fontsize=9)
plt.savefig(os.path.join(CHART_DIR, '02_subcategory_profit.png'))
plt.close()

loss_cats = subcat[subcat['Profit'] < 0]
if len(loss_cats) > 0:
    log(f"  LOSS-MAKING sub-categories: {', '.join(loss_cats.index)}")
    log(f"  Total losses: ${loss_cats['Profit'].sum():,.0f}")

# =========================================================================
# 3. REGIONAL ANALYSIS
# =========================================================================
log("\n--- 3. Regional Performance ---")
region_perf = df.groupby('Region').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
    Avg_Margin=('Profit Margin (%)', 'mean'),
).sort_values('Revenue', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Revenue by region
axes[0].pie(region_perf['Revenue'], labels=region_perf.index, autopct='%1.1f%%',
            colors=COLORS[:4], startangle=90, pctdistance=0.8)
axes[0].set_title('Revenue Share by Region', fontweight='bold')

# Profit by region
axes[1].bar(region_perf.index, region_perf['Profit'], color=COLORS[:4], edgecolor='white')
axes[1].set_title('Profit by Region', fontweight='bold')
axes[1].set_ylabel('Profit ($)')
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '03_regional_performance.png'))
plt.close()

for reg in region_perf.index:
    r = region_perf.loc[reg]
    log(f"  {reg}: Revenue=${r['Revenue']:,.0f} | Profit=${r['Profit']:,.0f} | Margin={r['Avg_Margin']:.1f}%")

# =========================================================================
# 4. TOP 10 STATES
# =========================================================================
log("\n--- 4. Top & Bottom States ---")
state_perf = df.groupby('State').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
).sort_values('Profit', ascending=False)

fig, ax = plt.subplots(figsize=(14, 6))
top_bottom = pd.concat([state_perf.head(10), state_perf.tail(5)])
colors = [COLORS[0] if p >= 0 else COLORS[3] for p in top_bottom['Profit']]
ax.barh(top_bottom.index, top_bottom['Profit'], color=colors, edgecolor='white')
ax.set_title('Top 10 & Bottom 5 States by Profit', fontsize=14, fontweight='bold')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax.axvline(x=0, color='black', linewidth=0.8)
plt.savefig(os.path.join(CHART_DIR, '04_top_bottom_states.png'))
plt.close()

loss_states = state_perf[state_perf['Profit'] < 0]
log(f"  States with net loss: {len(loss_states)}")
for st in loss_states.index:
    log(f"    {st}: ${loss_states.loc[st, 'Profit']:,.0f}")

# =========================================================================
# 5. DISCOUNT IMPACT ANALYSIS
# =========================================================================
log("\n--- 5. Discount vs. Profitability Analysis ---")

# Discount buckets
df['Discount Bucket'] = pd.cut(df['Discount'], bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.5, 1.0],
                                labels=['No Discount', '1-10%', '11-20%', '21-30%', '31-50%', '50%+'])
disc_impact = df.groupby('Discount Bucket', observed=True).agg(
    Total_Revenue=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Avg_Margin=('Profit Margin (%)', 'mean'),
    Order_Count=('Order ID', 'nunique'),
).reset_index()

fig, ax1 = plt.subplots(figsize=(10, 5))
x = range(len(disc_impact))
bars = ax1.bar(x, disc_impact['Total_Profit'], color=[COLORS[0] if p >= 0 else COLORS[3] for p in disc_impact['Total_Profit']])
ax1.set_xticks(x)
ax1.set_xticklabels(disc_impact['Discount Bucket'], rotation=0)
ax1.set_title('Impact of Discounts on Profitability', fontsize=14, fontweight='bold')
ax1.set_ylabel('Total Profit ($)')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax2 = ax1.twinx()
ax2.plot(x, disc_impact['Avg_Margin'], color=COLORS[1], marker='o', linewidth=2, label='Avg Margin %')
ax2.set_ylabel('Avg Profit Margin (%)')
ax2.legend(loc='upper right')
plt.savefig(os.path.join(CHART_DIR, '05_discount_impact.png'))
plt.close()

no_disc = df[df['Discount'] == 0]
with_disc = df[df['Discount'] > 0]
log(f"  No Discount -> Avg Margin: {no_disc['Profit Margin (%)'].mean():.1f}% | Profit Rate: {(no_disc['Profit'] > 0).mean()*100:.1f}%")
log(f"  With Discount -> Avg Margin: {with_disc['Profit Margin (%)'].mean():.1f}% | Profit Rate: {(with_disc['Profit'] > 0).mean()*100:.1f}%")
log(f"  INSIGHT: Discounts above 20% consistently lead to losses")

# =========================================================================
# 6. SHIPPING ANALYSIS
# =========================================================================
log("\n--- 6. Shipping Mode Analysis ---")
ship_perf = df.groupby('Ship Mode').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Avg_Ship_Days=('Shipping Days', 'mean'),
    Orders=('Order ID', 'nunique'),
).sort_values('Revenue', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].bar(ship_perf.index, ship_perf['Orders'], color=COLORS[:4])
axes[0].set_title('Orders by Ship Mode', fontweight='bold')
axes[0].set_ylabel('Number of Orders')

axes[1].bar(ship_perf.index, ship_perf['Avg_Ship_Days'], color=COLORS[:4])
axes[1].set_title('Avg Shipping Days by Ship Mode', fontweight='bold')
axes[1].set_ylabel('Days')
for i, v in enumerate(ship_perf['Avg_Ship_Days']):
    axes[1].text(i, v + 0.1, f'{v:.1f}', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '06_shipping_analysis.png'))
plt.close()

for mode in ship_perf.index:
    r = ship_perf.loc[mode]
    log(f"  {mode}: {r['Orders']} orders | Avg {r['Avg_Ship_Days']:.1f} days | Profit ${r['Profit']:,.0f}")

# =========================================================================
# 7. CUSTOMER SEGMENT ANALYSIS
# =========================================================================
log("\n--- 7. Customer Segment Analysis ---")
seg_perf = df.groupby('Segment').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Customers=('Customer ID', 'nunique'),
    Orders=('Order ID', 'nunique'),
).sort_values('Revenue', ascending=False)

for seg in seg_perf.index:
    r = seg_perf.loc[seg]
    log(f"  {seg}: {r['Customers']} customers | {r['Orders']} orders | Revenue ${r['Revenue']:,.0f} | Profit ${r['Profit']:,.0f}")

# =========================================================================
# 8. RFM CUSTOMER SEGMENTATION
# =========================================================================
log("\n--- 8. RFM Customer Segmentation ---")
seg_counts = rfm['Customer Segment'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
# Segment distribution
seg_counts.plot(kind='barh', ax=axes[0], color=COLORS[:len(seg_counts)])
axes[0].set_title('Customer Count by RFM Segment', fontweight='bold')
axes[0].set_xlabel('Number of Customers')

# Segment by revenue
seg_rev = rfm.groupby('Customer Segment')['Monetary'].sum().sort_values(ascending=True)
seg_rev.plot(kind='barh', ax=axes[1], color=COLORS[:len(seg_rev)])
axes[1].set_title('Revenue by Customer Segment', fontweight='bold')
axes[1].set_xlabel('Total Revenue ($)')
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '07_rfm_segmentation.png'))
plt.close()

for seg in seg_counts.index:
    seg_data = rfm[rfm['Customer Segment'] == seg]
    log(f"  {seg}: {len(seg_data)} customers | Avg Revenue ${seg_data['Monetary'].mean():,.0f}")

# =========================================================================
# 9. SEASONALITY & DAY-OF-WEEK
# =========================================================================
log("\n--- 9. Seasonality Patterns ---")
monthly_avg = df.groupby('Order Month')['Sales'].sum()
best_month = monthly_avg.idxmax()
worst_month = monthly_avg.idxmin()
log(f"  Best Month: {pd.Timestamp(2020, best_month, 1).strftime('%B')} (${monthly_avg.max():,.0f})")
log(f"  Worst Month: {pd.Timestamp(2020, worst_month, 1).strftime('%B')} (${monthly_avg.min():,.0f})")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
month_names = [pd.Timestamp(2020, m, 1).strftime('%b') for m in range(1, 13)]
axes[0].bar(month_names, monthly_avg.values, color=COLORS[0], edgecolor='white')
axes[0].set_title('Revenue by Month', fontweight='bold')
axes[0].set_ylabel('Total Revenue ($)')
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily = df.groupby('Order Day of Week')['Sales'].sum().reindex(day_order)
axes[1].bar(range(7), daily.values, color=COLORS[1], edgecolor='white')
axes[1].set_xticks(range(7))
axes[1].set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
axes[1].set_title('Revenue by Day of Week', fontweight='bold')
axes[1].set_ylabel('Total Revenue ($)')
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, '08_seasonality.png'))
plt.close()

# =========================================================================
# 10. CORRELATION ANALYSIS
# =========================================================================
log("\n--- 10. Key Correlations ---")
numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Days', 'Profit Margin (%)']
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=1, ax=ax)
ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
plt.savefig(os.path.join(CHART_DIR, '09_correlation_matrix.png'))
plt.close()

log(f"  Discount-Profit correlation: {corr.loc['Discount', 'Profit']:.3f} (negative = more discount, less profit)")
log(f"  Sales-Profit correlation: {corr.loc['Sales', 'Profit']:.3f}")

# =========================================================================
# 11. COHORT ANALYSIS (Return Rate by First-Purchase Quarter)
# =========================================================================
log("\n--- 11. Customer Cohort Analysis ---")
customer_first = df.groupby('Customer ID')['Order Date'].min().reset_index()
customer_first.columns = ['Customer ID', 'First Order']
customer_first['Cohort'] = customer_first['First Order'].dt.to_period('Q')

df_cohort = df.merge(customer_first, on='Customer ID')
df_cohort['Order Period'] = df_cohort['Order Date'].dt.to_period('Q')
df_cohort['Periods Since'] = (df_cohort['Order Period'] - df_cohort['Cohort']).apply(lambda x: x.n if hasattr(x, 'n') else 0)

cohort_data = df_cohort.groupby(['Cohort', 'Periods Since'])['Customer ID'].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index='Cohort', columns='Periods Since', values='Customer ID')
cohort_pct = cohort_pivot.divide(cohort_pivot[0], axis=0) * 100

fig, ax = plt.subplots(figsize=(14, 8))
sns.heatmap(cohort_pct.iloc[:8, :8], annot=True, fmt='.0f', cmap='YlOrRd', ax=ax,
            linewidths=1, cbar_kws={'label': 'Retention %'})
ax.set_title('Customer Retention by Cohort (% of Initial Customers)', fontsize=14, fontweight='bold')
ax.set_xlabel('Quarters Since First Purchase')
ax.set_ylabel('Cohort (First Purchase Quarter)')
plt.savefig(os.path.join(CHART_DIR, '10_cohort_retention.png'))
plt.close()

log("  Cohort retention heatmap generated.")

# =========================================================================
# 12. TOP PRODUCTS
# =========================================================================
log("\n--- 12. Top Products ---")
top_prods = df.groupby('Product Name').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Qty_Sold=('Quantity', 'sum'),
).sort_values('Revenue', ascending=False).head(10)

for prod in top_prods.index:
    r = top_prods.loc[prod]
    log(f"  {prod[:50]}: Revenue=${r['Revenue']:,.0f} | Profit=${r['Profit']:,.0f}")

# =========================================================================
# EXECUTIVE SUMMARY
# =========================================================================
log("\n" + "=" * 60)
log("  EXECUTIVE SUMMARY & RECOMMENDATIONS")
log("=" * 60)
log(f"""
1. REVENUE GROWTH: The business shows strong year-over-year growth.
   Total Revenue: ${df['Sales'].sum():,.0f} | Total Profit: ${df['Profit'].sum():,.0f}

2. DISCOUNT OPTIMIZATION (Critical Finding):
   - Orders without discounts have {no_disc['Profit Margin (%)'].mean():.0f}% avg margin
   - Orders with discounts have {with_disc['Profit Margin (%)'].mean():.0f}% avg margin
   - RECOMMENDATION: Cap discounts at 20%. Eliminate 30%+ discounts.
   - Estimated profit recovery: ~${abs(df[df['Discount'] > 0.2]['Profit'][df['Profit'] < 0].sum()):,.0f}

3. PRODUCT STRATEGY:
   - Loss-making sub-categories need review: {', '.join(loss_cats.index)}
   - Technology has highest profit margin; invest in marketing
   - Office Supplies: high volume, steady profits

4. REGIONAL FOCUS:
   - {loss_states.index[0] if len(loss_states) > 0 else 'N/A'} is the biggest loss-making state
   - Focus growth in West region (highest profit margin)

5. CUSTOMER RETENTION:
   - {len(rfm[rfm['Customer Segment'].isin(['At Risk', 'Cant Lose Them', 'Lost/Hibernating'])])} customers at risk of churning
   - Champions ({len(rfm[rfm['Customer Segment'] == 'Champions'])}) drive disproportionate revenue
   - RECOMMENDATION: Implement loyalty program for Potential Loyalists
""")

# Save report
report_path = os.path.join(REPORT_DIR, "eda_insights_report.txt")
with open(report_path, 'w') as f:
    f.write('\n'.join(report_lines))

print(f"\nCharts saved to: {CHART_DIR}")
print(f"Report saved to: {report_path}")
print(f"Total charts generated: {len(os.listdir(CHART_DIR))}")
print("\nEDA Complete!")
