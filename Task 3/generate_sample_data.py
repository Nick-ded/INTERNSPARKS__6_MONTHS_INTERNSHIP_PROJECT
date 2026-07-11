"""Generate sample sales dataset for analysis"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Generate sample sales data
n_records = 500

data = {
    'Date': [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(n_records)],
    'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse'], n_records),
    'Category': np.random.choice(['Electronics', 'Accessories', 'Computers'], n_records),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
    'Sales_Amount': np.random.uniform(100, 2000, n_records).round(2),
    'Quantity': np.random.randint(1, 20, n_records),
    'Discount': np.random.uniform(0, 30, n_records).round(2),
    'Customer_Satisfaction': np.random.randint(1, 6, n_records)
}

df = pd.DataFrame(data)

# Add some missing values intentionally
missing_indices = np.random.choice(df.index, size=30, replace=False)
df.loc[missing_indices[:10], 'Discount'] = np.nan
df.loc[missing_indices[10:20], 'Customer_Satisfaction'] = np.nan
df.loc[missing_indices[20:], 'Category'] = np.nan

# Add some duplicates
df = pd.concat([df, df.iloc[:5]], ignore_index=True)

# Save to CSV
df.to_csv('sample_sales.csv', index=False)
print(f"✓ Generated sample_sales.csv with {len(df)} records")
print(f"  • {df.isnull().sum().sum()} missing values")
print(f"  • {df.duplicated().sum()} duplicate rows")
