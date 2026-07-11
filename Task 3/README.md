# Data Analyzer

Complete data analysis toolkit — load CSV files, clean data, generate statistics, perform grouping, and create visualizations with Pandas, Matplotlib, and Seaborn.

---

## Features

| Feature | Description |
|---------|-------------|
| **CSV Loading** | Load CSV files with automatic error handling |
| **Data Cleaning** | Remove duplicates, handle missing values (median/mode imputation) |
| **Summary Statistics** | Descriptive stats, correlation analysis, distributions |
| **Categorical Analysis** | Frequency distributions with visual bars |
| **Grouping & Aggregation** | Group-by operations with mean, sum, count |
| **Missing Data Analysis** | Identify and quantify missing values |
| **Visualizations** | Histograms, correlation heatmaps, bar charts, box plots |
| **Insights Generation** | Automated key insights from the data |

---

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Generate Sample Data (Optional)

```bash
python generate_sample_data.py
```

This creates `sample_sales.csv` with 500+ records including:
- Sales transactions across multiple products and regions
- Missing values (intentional)
- Duplicate rows (intentional)

### 2. Run Analysis

```bash
python data_analyzer.py
```

When prompted:
- Enter CSV file path (or press Enter to use `sample_sales.csv`)
- Choose whether to generate visualizations

---

## What the Script Does

### 1. **Dataset Overview**
- Displays shape, memory usage, column types
- Lists all columns with data types and unique value counts

### 2. **Missing Data Analysis**
- Identifies columns with missing values
- Shows count and percentage for each

### 3. **Data Cleaning**
- Removes duplicate rows
- Fills numeric missing values with **median**
- Fills categorical missing values with **mode**

### 4. **Summary Statistics**
- Descriptive statistics (mean, std, min, max, quartiles)
- Correlation matrix for numeric columns

### 5. **Categorical Analysis**
- Frequency distribution for categorical columns
- Visual bar representation in terminal

### 6. **Grouping Analysis**
- Groups data by first categorical column
- Aggregates numeric columns (mean, sum, count)

### 7. **Key Insights**
- Dataset size
- Missing data status
- Variability analysis (coefficient of variation)
- Most common categorical values
- Strongest correlations

### 8. **Visualizations** (saved to `output/` folder)
- **Distribution plots** — Histograms for all numeric columns
- **Correlation heatmap** — Shows relationships between numeric variables
- **Categorical bar charts** — Top 15 values for each category
- **Box plots** — Outlier detection for numeric columns

---

## Sample Output

```
================================================================================
                    DATA ANALYZER - CSV Analysis & Visualization Tool
================================================================================

ℹ Loading data from: sample_sales.csv
✓ Data loaded successfully! Shape: (505, 8)

────────────────────────────────────────────────────────────────────────────────
  DATASET OVERVIEW
────────────────────────────────────────────────────────────────────────────────

Dataset Info:
  • Shape: 505 rows × 8 columns
  • Memory usage: 0.03 MB
  • Numeric columns: 4
  • Categorical columns: 4

Column Names and Types:
  • Date                     datetime64[ns]  (365 unique values)
  • Product                  object          (6 unique values)
  • Category                 object          (3 unique values)
  • Region                   object          (4 unique values)
  • Sales_Amount             float64         (495 unique values)
  • Quantity                 int64           (19 unique values)
  • Discount                 float64         (477 unique values)
  • Customer_Satisfaction    float64         (5 unique values)

────────────────────────────────────────────────────────────────────────────────
  MISSING DATA ANALYSIS
────────────────────────────────────────────────────────────────────────────────

Column                   Missing Count  Percentage
Customer_Satisfaction               10        1.98
Category                            10        1.98
Discount                            10        1.98

Total missing values: 30

────────────────────────────────────────────────────────────────────────────────
  DATA CLEANING
────────────────────────────────────────────────────────────────────────────────

ℹ Original shape: (505, 8)
✓ Removed 5 duplicate rows
ℹ Filled Discount missing values with median: 15.23
ℹ Filled Customer_Satisfaction missing values with median: 3.00
ℹ Filled Category missing values with mode: Electronics
✓ Final shape: (500, 8)

────────────────────────────────────────────────────────────────────────────────
  SUMMARY STATISTICS
────────────────────────────────────────────────────────────────────────────────

Descriptive Statistics (Numeric Columns):

       Sales_Amount    Quantity     Discount  Customer_Satisfaction
count    500.000000  500.000000   500.000000             500.000000
mean    1048.234500   10.456000    14.987200               2.998000
std      547.923421    5.512345    8.654321               1.421234
min      102.450000    1.000000     0.120000               1.000000
25%      573.125000    5.000000     7.450000               2.000000
50%     1045.670000   10.000000    15.230000               3.000000
75%     1521.875000   15.000000    22.560000               4.000000
max     1998.760000   19.000000    29.980000               5.000000

────────────────────────────────────────────────────────────────────────────────
  KEY INSIGHTS
────────────────────────────────────────────────────────────────────────────────

  📊 Dataset contains 500 records across 8 features
  ✅ No missing values detected - data quality is excellent
  📈 Sales_Amount: Mean = 1048.23, StdDev = 547.92, CV = 52.3% (high variability)
  📈 Quantity: Mean = 10.46, StdDev = 5.51, CV = 52.7% (high variability)
  🏷️  Product: 6 unique values, most common = 'Phone' (18.2%)
  🏷️  Region: 4 unique values, most common = 'North' (26.4%)
  🔗 Strongest correlation: Sales_Amount ↔ Quantity (r = 0.234)

Generate visualizations? (y/n): y

────────────────────────────────────────────────────────────────────────────────
  GENERATING VISUALIZATIONS
────────────────────────────────────────────────────────────────────────────────

ℹ Creating distribution plots...
✓ Saved: output/distributions.png
ℹ Creating correlation heatmap...
✓ Saved: output/correlation_heatmap.png
ℹ Creating categorical bar charts...
✓ Saved: output/Product_distribution.png
✓ Saved: output/Category_distribution.png
✓ Saved: output/Region_distribution.png
ℹ Creating box plots for outlier detection...
✓ Saved: output/boxplots.png

================================================================================
                              ANALYSIS COMPLETE
================================================================================

✓ All operations completed successfully!
```

---

## Visualizations Generated

### 1. Distributions (`distributions.png`)
Histograms showing the distribution of all numeric columns

### 2. Correlation Heatmap (`correlation_heatmap.png`)
Color-coded matrix showing correlations between numeric variables

### 3. Categorical Bar Charts
- `Product_distribution.png`
- `Category_distribution.png`
- `Region_distribution.png`

### 4. Box Plots (`boxplots.png`)
Outlier detection across all numeric columns

---

## Data Cleaning Methods

| Issue | Solution |
|-------|----------|
| Duplicates | Remove with `drop_duplicates()` |
| Missing (Numeric) | Fill with median (robust to outliers) |
| Missing (Categorical) | Fill with mode (most frequent value) |

---

## Code Structure

```python
# Main Functions
load_data()                     # CSV loading with error handling
clean_data()                    # Duplicate removal + missing value imputation
display_basic_info()            # Dataset overview
analyze_missing_data()          # Missing value analysis
display_summary_statistics()    # Descriptive stats + correlation
display_categorical_analysis()  # Frequency distributions
perform_grouping_analysis()     # Group-by aggregations
generate_insights()             # Automated insights
create_visualizations()         # Chart generation
```

---

## Sample Data Schema

| Column | Type | Description |
|--------|------|-------------|
| Date | datetime | Transaction date |
| Product | object | Product name (Laptop, Phone, etc.) |
| Category | object | Product category |
| Region | object | Sales region (North, South, East, West) |
| Sales_Amount | float | Revenue in dollars |
| Quantity | int | Number of units sold |
| Discount | float | Discount percentage applied |
| Customer_Satisfaction | int | Rating from 1-5 |

---

## License

MIT — Free to use and modify.
