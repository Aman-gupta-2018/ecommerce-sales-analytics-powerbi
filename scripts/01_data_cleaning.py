"""
Data Cleaning & Preparation Script
====================================
Cleans and transforms the raw Superstore dataset for analysis.
Exports cleaned data ready for Power BI import.

Dataset Source: Kaggle - Superstore Dataset
https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "Sample - Superstore.csv")
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned")
os.makedirs(CLEAN_DIR, exist_ok=True)

print("=" * 60)
print("  SUPERSTORE DATA CLEANING & PREPARATION")
print("=" * 60)

# ---------------------------------------------------------------------------
# 1. Load Raw Data
# ---------------------------------------------------------------------------
print("\n[1/7] Loading raw data...")
df = pd.read_csv(RAW_PATH, encoding='latin1')
print(f"  Raw dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")

# ---------------------------------------------------------------------------
# 2. Data Quality Checks
# ---------------------------------------------------------------------------
print("\n[2/7] Running data quality checks...")

# Check for duplicates
dupes = df.duplicated().sum()
print(f"  Duplicate rows: {dupes}")
if dupes > 0:
    df = df.drop_duplicates()
    print(f"  -> Removed {dupes} duplicates. New shape: {df.shape}")

# Check for nulls
nulls = df.isnull().sum()
null_cols = nulls[nulls > 0]
if len(null_cols) > 0:
    print(f"  Columns with nulls: {dict(null_cols)}")
else:
    print("  No null values found.")

# Check for negative sales (data anomalies)
neg_sales = (df['Sales'] < 0).sum()
print(f"  Negative sales entries: {neg_sales}")

# ---------------------------------------------------------------------------
# 3. Data Type Conversions
# ---------------------------------------------------------------------------
print("\n[3/7] Converting data types...")

# Parse dates
df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', dayfirst=False)
print("  Converted Order Date and Ship Date to datetime.")

# Postal Code as string (leading zeros)
df['Postal Code'] = df['Postal Code'].astype(str).str.zfill(5)
print("  Converted Postal Code to string (preserved leading zeros).")

# ---------------------------------------------------------------------------
# 4. Feature Engineering
# ---------------------------------------------------------------------------
print("\n[4/7] Engineering new features...")

# Date-based features
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Month Name'] = df['Order Date'].dt.strftime('%B')
df['Order Quarter'] = df['Order Date'].dt.quarter
df['Order Day of Week'] = df['Order Date'].dt.day_name()
df['Year-Quarter'] = df['Order Date'].dt.to_period('Q').astype(str)
df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
print("  Added: Order Year, Month, Month Name, Quarter, Day of Week, Year-Quarter, Year-Month")

# Shipping duration
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
print("  Added: Shipping Days")

# Profit margin
df['Profit Margin (%)'] = np.where(
    df['Sales'] != 0,
    round((df['Profit'] / df['Sales']) * 100, 2),
    0
)
print("  Added: Profit Margin (%)")

# Revenue per unit
df['Revenue Per Unit'] = round(df['Sales'] / df['Quantity'], 2)
print("  Added: Revenue Per Unit")

# Discount flag
df['Has Discount'] = (df['Discount'] > 0).astype(int)
print("  Added: Has Discount (binary flag)")

# Profit flag
df['Is Profitable'] = (df['Profit'] > 0).astype(int)
print("  Added: Is Profitable (binary flag)")

# Cost (estimated)
df['Estimated Cost'] = round(df['Sales'] - df['Profit'], 2)
print("  Added: Estimated Cost")

# Discount Amount
df['Discount Amount'] = round(df['Sales'] * df['Discount'] / (1 - df['Discount']), 2)
print("  Added: Discount Amount")

# ---------------------------------------------------------------------------
# 5. Create Dimension Tables (Star Schema for Power BI)
# ---------------------------------------------------------------------------
print("\n[5/7] Creating dimension tables (star schema)...")

# Dim Customers
dim_customers = df[['Customer ID', 'Customer Name', 'Segment']].drop_duplicates(subset=['Customer ID'], keep='first')
dim_customers = dim_customers.sort_values('Customer ID').reset_index(drop=True)
print(f"  dim_customers: {len(dim_customers)} unique customers")

# Dim Products
# NOTE: The raw dataset can have the same Product ID with slightly different
# Product Name (e.g. vendor description variants). Deduplicate on Product ID
# only (keep the first occurrence) so Product ID can act as a primary key.
dim_products = df[['Product ID', 'Product Name', 'Category', 'Sub-Category']].drop_duplicates(subset=['Product ID'], keep='first')
dim_products = dim_products.sort_values('Product ID').reset_index(drop=True)
print(f"  dim_products: {len(dim_products)} unique products")

# Dim Geography
dim_geography = df[['City', 'State', 'Postal Code', 'Region', 'Country']].drop_duplicates()
dim_geography = dim_geography.sort_values(['Region', 'State', 'City']).reset_index(drop=True)
dim_geography.insert(0, 'Geo ID', range(1, len(dim_geography) + 1))
print(f"  dim_geography: {len(dim_geography)} unique locations")

# Map Geo ID back to fact table
geo_map = dim_geography.set_index(['City', 'State', 'Postal Code', 'Region', 'Country'])['Geo ID']
df['Geo ID'] = df.set_index(['City', 'State', 'Postal Code', 'Region', 'Country']).index.map(geo_map)

# Dim Date
date_range = pd.date_range(start=df['Order Date'].min(), end=df['Order Date'].max(), freq='D')
dim_date = pd.DataFrame({
    'Date': date_range,
    'Year': date_range.year,
    'Quarter': date_range.quarter,
    'Month': date_range.month,
    'Month Name': date_range.strftime('%B'),
    'Week': date_range.isocalendar().week.values,
    'Day': date_range.day,
    'Day of Week': date_range.day_name(),
    'Is Weekend': date_range.weekday.isin([5, 6]).astype(int),
})
print(f"  dim_date: {len(dim_date)} dates")

# Dim Ship Mode
dim_shipmode = pd.DataFrame({
    'Ship Mode': df['Ship Mode'].unique()
}).sort_values('Ship Mode').reset_index(drop=True)
dim_shipmode.insert(0, 'Ship Mode ID', range(1, len(dim_shipmode) + 1))
print(f"  dim_shipmode: {len(dim_shipmode)} ship modes")

# Fact Orders (the main fact table with foreign keys)
fact_columns = [
    'Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
    'Customer ID', 'Product ID', 'Geo ID',
    'Sales', 'Quantity', 'Discount', 'Profit',
    'Order Year', 'Order Month', 'Order Month Name', 'Order Quarter',
    'Order Day of Week', 'Year-Quarter', 'Year-Month',
    'Shipping Days', 'Profit Margin (%)', 'Revenue Per Unit',
    'Has Discount', 'Is Profitable', 'Estimated Cost', 'Discount Amount'
]
fact_orders = df[fact_columns].copy()
print(f"  fact_orders: {len(fact_orders)} rows")

# ---------------------------------------------------------------------------
# 6. Customer-Level Aggregations (for RFM & Segmentation)
# ---------------------------------------------------------------------------
print("\n[6/7] Building customer analytics table...")

max_date = df['Order Date'].max()
customer_agg = df.groupby('Customer ID').agg(
    Total_Orders=('Order ID', 'nunique'),
    Total_Revenue=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Total_Quantity=('Quantity', 'sum'),
    Avg_Order_Value=('Sales', 'mean'),
    Avg_Discount=('Discount', 'mean'),
    First_Order=('Order Date', 'min'),
    Last_Order=('Order Date', 'max'),
    Unique_Products=('Product ID', 'nunique'),
    Unique_Categories=('Category', 'nunique'),
    Avg_Profit_Margin=('Profit Margin (%)', 'mean'),
).reset_index()

# RFM Metrics
customer_agg['Recency (Days)'] = (max_date - customer_agg['Last_Order']).dt.days
customer_agg['Frequency'] = customer_agg['Total_Orders']
customer_agg['Monetary'] = round(customer_agg['Total_Revenue'], 2)

# RFM Scores (1-5 quintiles)
customer_agg['R_Score'] = pd.qcut(customer_agg['Recency (Days)'], q=5, labels=[5,4,3,2,1]).astype(int)
customer_agg['F_Score'] = pd.qcut(customer_agg['Frequency'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
customer_agg['M_Score'] = pd.qcut(customer_agg['Monetary'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
customer_agg['RFM_Score'] = customer_agg['R_Score'] + customer_agg['F_Score'] + customer_agg['M_Score']

# Customer Segments based on RFM
def rfm_segment(row):
    if row['RFM_Score'] >= 13:
        return 'Champions'
    elif row['RFM_Score'] >= 10:
        return 'Loyal Customers'
    elif row['R_Score'] >= 4 and row['F_Score'] <= 2:
        return 'New Customers'
    elif row['R_Score'] >= 3 and row['F_Score'] >= 3:
        return 'Potential Loyalists'
    elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
        return 'At Risk'
    elif row['R_Score'] <= 2 and row['M_Score'] >= 3:
        return 'Cant Lose Them'
    elif row['R_Score'] <= 2:
        return 'Lost/Hibernating'
    else:
        return 'Need Attention'

customer_agg['Customer Segment'] = customer_agg.apply(rfm_segment, axis=1)

# Round numeric columns
for col in ['Total_Revenue', 'Total_Profit', 'Avg_Order_Value', 'Avg_Discount', 'Avg_Profit_Margin']:
    customer_agg[col] = round(customer_agg[col], 2)

# Merge customer name and segment
customer_agg = customer_agg.merge(
    dim_customers[['Customer ID', 'Customer Name', 'Segment']],
    on='Customer ID', how='left'
)

print(f"  Customer analytics: {len(customer_agg)} customers")
print(f"  RFM Segments: {dict(customer_agg['Customer Segment'].value_counts())}")

# ---------------------------------------------------------------------------
# 7. Export Cleaned Data
# ---------------------------------------------------------------------------
print("\n[7/7] Exporting cleaned datasets...")

# Main cleaned dataset (flat - for general analysis)
df.to_csv(os.path.join(CLEAN_DIR, "superstore_cleaned.csv"), index=False)
print(f"  superstore_cleaned.csv ({len(df):,} rows)")

# Star schema tables for Power BI
fact_orders.to_csv(os.path.join(CLEAN_DIR, "fact_orders.csv"), index=False)
dim_customers.to_csv(os.path.join(CLEAN_DIR, "dim_customers.csv"), index=False)
dim_products.to_csv(os.path.join(CLEAN_DIR, "dim_products.csv"), index=False)
dim_geography.to_csv(os.path.join(CLEAN_DIR, "dim_geography.csv"), index=False)
dim_date.to_csv(os.path.join(CLEAN_DIR, "dim_date.csv"), index=False)
dim_shipmode.to_csv(os.path.join(CLEAN_DIR, "dim_shipmode.csv"), index=False)
print(f"  Star schema tables exported (fact_orders, dim_customers, dim_products, dim_geography, dim_date, dim_shipmode)")

# Customer analytics for RFM dashboard
customer_agg.to_csv(os.path.join(CLEAN_DIR, "customer_rfm_analysis.csv"), index=False)
print(f"  customer_rfm_analysis.csv ({len(customer_agg)} customers)")

print("\n" + "=" * 60)
print("  DATA CLEANING COMPLETE")
print("=" * 60)
print(f"\n  Output directory: {CLEAN_DIR}")
print(f"  Files created: 7")
print(f"  Ready for Power BI import!")
