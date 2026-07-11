"""
Data Analyzer - Load, clean, analyze, and visualize CSV datasets
Uses: Pandas for data manipulation, Matplotlib/Seaborn for visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pathlib import Path
from typing import Dict, List, Tuple, Any

warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


# ── ANSI Colors ───────────────────────────────────────────────────────────────

class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str) -> None:
    print(f"\n{Color.BOLD}{Color.CYAN}{'='*80}{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{text.center(80)}{Color.END}")
    print(f"{Color.BOLD}{Color.CYAN}{'='*80}{Color.END}\n")


def print_success(text: str) -> None:
    print(f"{Color.GREEN}✓ {text}{Color.END}")


def print_info(text: str) -> None:
    print(f"{Color.CYAN}ℹ {text}{Color.END}")


def print_section(text: str) -> None:
    print(f"\n{Color.BOLD}{Color.YELLOW}{'─'*80}{Color.END}")
    print(f"{Color.BOLD}{Color.YELLOW}  {text}{Color.END}")
    print(f"{Color.BOLD}{Color.YELLOW}{'─'*80}{Color.END}\n")


# ── Data Loading ──────────────────────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV data with error handling."""
    print_info(f"Loading data from: {filepath}")
    
    try:
        df = pd.read_csv(filepath)
        print_success(f"Data loaded successfully! Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"{Color.RED}✗ File not found: {filepath}{Color.END}")
        return None
    except pd.errors.EmptyDataError:
        print(f"{Color.RED}✗ File is empty{Color.END}")
        return None
    except Exception as e:
        print(f"{Color.RED}✗ Error loading data: {e}{Color.END}")
        return None


# ── Data Cleaning ─────────────────────────────────────────────────────────────

def analyze_missing_data(df: pd.DataFrame) -> None:
    """Analyze and display missing data."""
    print_section("MISSING DATA ANALYSIS")
    
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing Count': missing.values,
        'Percentage': missing_pct.values
    }).sort_values('Missing Count', ascending=False)
    
    missing_df = missing_df[missing_df['Missing Count'] > 0]
    
    if len(missing_df) == 0:
        print_success("No missing values found!")
    else:
        print(missing_df.to_string(index=False))
        print(f"\n{Color.YELLOW}Total missing values: {missing.sum()}{Color.END}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset by handling missing values and duplicates."""
    print_section("DATA CLEANING")
    
    original_shape = df.shape
    print_info(f"Original shape: {original_shape}")
    
    # Remove duplicates
    df = df.drop_duplicates()
    duplicates_removed = original_shape[0] - df.shape[0]
    print_success(f"Removed {duplicates_removed} duplicate rows")
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Fill numeric columns with median
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print_info(f"Filled {col} missing values with median: {median_val:.2f}")
    
    # Fill categorical columns with mode
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
            df[col].fillna(mode_val, inplace=True)
            print_info(f"Filled {col} missing values with mode: {mode_val}")
    
    print_success(f"Final shape: {df.shape}")
    return df


# ── Summary Statistics ────────────────────────────────────────────────────────

def display_basic_info(df: pd.DataFrame) -> None:
    """Display basic dataset information."""
    print_section("DATASET OVERVIEW")
    
    print(f"{Color.BOLD}Dataset Info:{Color.END}")
    print(f"  • Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"  • Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"  • Numeric columns: {len(df.select_dtypes(include=[np.number]).columns)}")
    print(f"  • Categorical columns: {len(df.select_dtypes(include=['object']).columns)}")
    
    print(f"\n{Color.BOLD}Column Names and Types:{Color.END}")
    for col in df.columns:
        dtype = df[col].dtype
        unique = df[col].nunique()
        print(f"  • {col:<25} {str(dtype):<15} ({unique} unique values)")


def display_summary_statistics(df: pd.DataFrame) -> None:
    """Display comprehensive summary statistics."""
    print_section("SUMMARY STATISTICS")
    
    numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.empty:
        print(f"{Color.YELLOW}No numeric columns found{Color.END}")
        return
    
    print(f"{Color.BOLD}Descriptive Statistics (Numeric Columns):{Color.END}\n")
    print(numeric_df.describe().to_string())
    
    print(f"\n{Color.BOLD}Correlation Analysis:{Color.END}\n")
    corr_matrix = numeric_df.corr()
    print(corr_matrix.to_string())


def display_categorical_analysis(df: pd.DataFrame) -> None:
    """Analyze categorical columns."""
    print_section("CATEGORICAL ANALYSIS")
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    if len(categorical_cols) == 0:
        print(f"{Color.YELLOW}No categorical columns found{Color.END}")
        return
    
    for col in categorical_cols:
        print(f"\n{Color.BOLD}{col.upper()}:{Color.END}")
        value_counts = df[col].value_counts().head(10)
        
        for val, count in value_counts.items():
            pct = (count / len(df)) * 100
            bar = '█' * int(pct)
            print(f"  {str(val):<30} {count:>6} ({pct:>5.1f}%) {bar}")


# ── Data Filtering & Grouping ─────────────────────────────────────────────────

def perform_grouping_analysis(df: pd.DataFrame) -> None:
    """Perform grouping and aggregation analysis."""
    print_section("GROUPING ANALYSIS")
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(categorical_cols) == 0 or len(numeric_cols) == 0:
        print(f"{Color.YELLOW}Insufficient columns for grouping analysis{Color.END}")
        return
    
    # Group by first categorical column and aggregate numeric columns
    group_col = categorical_cols[0]
    
    print(f"{Color.BOLD}Grouping by: {group_col}{Color.END}\n")
    
    grouped = df.groupby(group_col)[numeric_cols].agg(['mean', 'sum', 'count'])
    print(grouped.to_string())


# ── Visualization ─────────────────────────────────────────────────────────────

def create_visualizations(df: pd.DataFrame, output_dir: str = "output") -> None:
    """Generate and save visualizations."""
    print_section("GENERATING VISUALIZATIONS")
    
    Path(output_dir).mkdir(exist_ok=True)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # 1. Distribution plots for numeric columns
    if len(numeric_cols) > 0:
        print_info("Creating distribution plots...")
        
        fig, axes = plt.subplots(
            nrows=(len(numeric_cols) + 1) // 2,
            ncols=2,
            figsize=(14, 4 * ((len(numeric_cols) + 1) // 2))
        )
        axes = axes.flatten() if len(numeric_cols) > 1 else [axes]
        
        for idx, col in enumerate(numeric_cols):
            if idx < len(axes):
                axes[idx].hist(df[col].dropna(), bins=30, color='skyblue', edgecolor='black')
                axes[idx].set_title(f'Distribution of {col}', fontweight='bold')
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Frequency')
                axes[idx].grid(True, alpha=0.3)
        
        # Hide extra subplots
        for idx in range(len(numeric_cols), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/distributions.png", dpi=300, bbox_inches='tight')
        print_success(f"Saved: {output_dir}/distributions.png")
        plt.close()
    
    # 2. Correlation heatmap
    if len(numeric_cols) > 1:
        print_info("Creating correlation heatmap...")
        
        plt.figure(figsize=(10, 8))
        corr_matrix = df[numeric_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Correlation Heatmap', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/correlation_heatmap.png", dpi=300, bbox_inches='tight')
        print_success(f"Saved: {output_dir}/correlation_heatmap.png")
        plt.close()
    
    # 3. Categorical bar charts
    if len(categorical_cols) > 0:
        print_info("Creating categorical bar charts...")
        
        for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
            plt.figure(figsize=(12, 6))
            value_counts = df[col].value_counts().head(15)
            
            bars = plt.bar(range(len(value_counts)), value_counts.values, color='coral', edgecolor='black')
            plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
            plt.title(f'Distribution of {col}', fontsize=14, fontweight='bold')
            plt.xlabel(col)
            plt.ylabel('Count')
            plt.grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            filename = col.replace(' ', '_').replace('/', '_')
            plt.savefig(f"{output_dir}/{filename}_distribution.png", dpi=300, bbox_inches='tight')
            print_success(f"Saved: {output_dir}/{filename}_distribution.png")
            plt.close()
    
    # 4. Box plots for outlier detection
    if len(numeric_cols) > 0:
        print_info("Creating box plots for outlier detection...")
        
        fig, axes = plt.subplots(
            nrows=(len(numeric_cols) + 1) // 2,
            ncols=2,
            figsize=(14, 4 * ((len(numeric_cols) + 1) // 2))
        )
        axes = axes.flatten() if len(numeric_cols) > 1 else [axes]
        
        for idx, col in enumerate(numeric_cols):
            if idx < len(axes):
                axes[idx].boxplot(df[col].dropna(), vert=True, patch_artist=True,
                                 boxprops=dict(facecolor='lightgreen'))
                axes[idx].set_title(f'Box Plot: {col}', fontweight='bold')
                axes[idx].set_ylabel(col)
                axes[idx].grid(True, alpha=0.3)
        
        for idx in range(len(numeric_cols), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/boxplots.png", dpi=300, bbox_inches='tight')
        print_success(f"Saved: {output_dir}/boxplots.png")
        plt.close()


# ── Generate Insights ─────────────────────────────────────────────────────────

def generate_insights(df: pd.DataFrame) -> None:
    """Generate meaningful insights from the data."""
    print_section("KEY INSIGHTS")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    insights = []
    
    # Dataset size insight
    insights.append(f"📊 Dataset contains {df.shape[0]:,} records across {df.shape[1]} features")
    
    # Missing data insight
    missing_total = df.isnull().sum().sum()
    if missing_total == 0:
        insights.append("✅ No missing values detected - data quality is excellent")
    else:
        insights.append(f"⚠️  Found {missing_total} missing values across the dataset")
    
    # Numeric insights
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            mean_val = df[col].mean()
            std_val = df[col].std()
            cv = (std_val / mean_val * 100) if mean_val != 0 else 0
            
            insights.append(
                f"📈 {col}: Mean = {mean_val:.2f}, StdDev = {std_val:.2f}, "
                f"CV = {cv:.1f}% ({'high' if cv > 50 else 'moderate' if cv > 25 else 'low'} variability)"
            )
    
    # Categorical insights
    if len(categorical_cols) > 0:
        for col in categorical_cols[:2]:
            unique_count = df[col].nunique()
            most_common = df[col].mode()[0] if not df[col].mode().empty else 'N/A'
            most_common_pct = (df[col].value_counts().iloc[0] / len(df) * 100) if len(df) > 0 else 0
            
            insights.append(
                f"🏷️  {col}: {unique_count} unique values, "
                f"most common = '{most_common}' ({most_common_pct:.1f}%)"
            )
    
    # Correlation insight
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        max_corr_idx = np.unravel_index(
            np.ma.masked_equal(corr_matrix.values, 1.0).argmax(),
            corr_matrix.shape
        )
        col1, col2 = corr_matrix.index[max_corr_idx[0]], corr_matrix.columns[max_corr_idx[1]]
        max_corr = corr_matrix.iloc[max_corr_idx]
        
        insights.append(
            f"🔗 Strongest correlation: {col1} ↔ {col2} (r = {max_corr:.3f})"
        )
    
    for insight in insights:
        print(f"  {insight}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    """Main execution function."""
    print_header("DATA ANALYZER - CSV Analysis & Visualization Tool")
    
    # Example: Use sample_sales.csv if it exists, otherwise prompt
    filepath = input(f"{Color.BOLD}Enter CSV file path (or press Enter for sample_sales.csv): {Color.END}").strip() or "sample_sales.csv"
    
    # Load data
    df = load_data(filepath)
    if df is None:
        return
    
    # Display basic info
    display_basic_info(df)
    
    # Analyze missing data
    analyze_missing_data(df)
    
    # Clean data
    df_cleaned = clean_data(df)
    
    # Summary statistics
    display_summary_statistics(df_cleaned)
    
    # Categorical analysis
    display_categorical_analysis(df_cleaned)
    
    # Grouping analysis
    perform_grouping_analysis(df_cleaned)
    
    # Generate insights
    generate_insights(df_cleaned)
    
    # Create visualizations
    create_viz = input(f"\n{Color.BOLD}Generate visualizations? (y/n): {Color.END}").strip().lower()
    if create_viz == 'y':
        create_visualizations(df_cleaned)
    
    print_header("ANALYSIS COMPLETE")
    print_success("All operations completed successfully!")


if __name__ == "__main__":
    main()
