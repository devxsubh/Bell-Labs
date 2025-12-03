"""
Exploratory Data Analysis (EDA) on Master Panel Dataset
Generates summary statistics, visualizations, and analysis outputs
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 60)
print("EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 60)

# STEP 1 — Load & Prepare Data
print("\n📂 STEP 1: Loading and preparing data...")
DATA_DIR = Path("data/processed")
FINAL_DIR = DATA_DIR / "final"
OUTPUT_DIR = Path("data/outputs")
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"

# Create output folders
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)
print(f"   Created output directories")

# Load master panel
master = pd.read_csv(FINAL_DIR / "master_panel_final.csv")
print(f"   Loaded master panel: {len(master):,} rows, {len(master.columns)} columns")

# Convert numerical columns properly
numerical_cols = ['year', 'energy_kcal_day', 'protein_g_day', 'fat_g_day', 
                  'sugar_g_day', 'obesity_pct', 'population']
for col in numerical_cols:
    if col in master.columns:
        master[col] = pd.to_numeric(master[col], errors='coerce')

print(f"   Converted numerical columns")
print(f"   Year range: {int(master['year'].min())} - {int(master['year'].max())}")
print(f"   Countries: {master['country'].nunique()}")

# STEP 2 — Summary Statistics
print("\n📊 STEP 2: Generating summary statistics...")
variables = ['energy_kcal_day', 'protein_g_day', 'fat_g_day', 'sugar_g_day', 'obesity_pct']

summary_stats = pd.DataFrame()
for var in variables:
    if var in master.columns:
        data = master[var].dropna()
        if len(data) > 0:
            summary_stats.loc[var, 'count'] = len(data)
            summary_stats.loc[var, 'missing'] = master[var].isna().sum()
            summary_stats.loc[var, 'mean'] = data.mean()
            summary_stats.loc[var, 'std'] = data.std()
            summary_stats.loc[var, 'min'] = data.min()
            summary_stats.loc[var, '25%'] = data.quantile(0.25)
            summary_stats.loc[var, 'median'] = data.median()
            summary_stats.loc[var, '75%'] = data.quantile(0.75)
            summary_stats.loc[var, 'max'] = data.max()
            summary_stats.loc[var, 'IQR'] = data.quantile(0.75) - data.quantile(0.25)

summary_stats = summary_stats.round(2)
summary_stats.to_csv(TABLES_DIR / "summary_stats_nutrients_obesity.csv")
print(f"   ✅ Saved summary statistics to: {TABLES_DIR / 'summary_stats_nutrients_obesity.csv'}")
print(summary_stats)

# STEP 3 — Obesity Ranking (Latest Year)
print("\n🏆 STEP 3: Obesity ranking for latest year...")
latest_year = int(master['year'].max())
print(f"   Latest year: {latest_year}")

latest_data = master[master['year'] == latest_year].copy()
latest_data = latest_data.sort_values('obesity_pct', ascending=False)

# Top 10
top10 = latest_data[['country', 'obesity_pct', 'energy_kcal_day', 'protein_g_day', 'fat_g_day']].head(10)
top10.to_csv(TABLES_DIR / "top10_obesity_latest_year.csv", index=False)
print(f"   ✅ Saved top 10 obesity countries to: {TABLES_DIR / 'top10_obesity_latest_year.csv'}")

# Bottom 10
bottom10 = latest_data[['country', 'obesity_pct', 'energy_kcal_day', 'protein_g_day', 'fat_g_day']].tail(10)
bottom10.to_csv(TABLES_DIR / "bottom10_obesity_latest_year.csv", index=False)
print(f"   ✅ Saved bottom 10 obesity countries to: {TABLES_DIR / 'bottom10_obesity_latest_year.csv'}")

# STEP 4 — Global Trends (Line Plots)
print("\n📈 STEP 4: Creating global trend plots...")

# Global obesity trend
global_obesity = master.groupby('year')['obesity_pct'].mean().reset_index()
plt.figure(figsize=(10, 6))
plt.plot(global_obesity['year'], global_obesity['obesity_pct'], marker='o', linewidth=2, markersize=8)
plt.title('Global Obesity Trend (Average Across Countries)', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Obesity Prevalence (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "global_obesity_trend.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved: {FIGURES_DIR / 'global_obesity_trend.png'}")

# Global energy trend
global_energy = master.groupby('year')['energy_kcal_day'].mean().reset_index()
plt.figure(figsize=(10, 6))
plt.plot(global_energy['year'], global_energy['energy_kcal_day'], marker='o', linewidth=2, markersize=8)
plt.title('Global Energy Intake Trend (Average Across Countries)', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Energy Intake (kcal/capita/day)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "global_energy_trend.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved: {FIGURES_DIR / 'global_energy_trend.png'}")

# STEP 5 — Food Group Shares
print("\n🍎 STEP 5: Analyzing food group shares...")

# Identify food group energy columns (exclude share columns and other metadata)
fg_energy_cols = [c for c in master.columns if c not in [
    'country', 'year', 'energy_kcal_day', 'protein_g_day', 'fat_g_day', 
    'sugar_g_day', 'obesity_pct', 'population', 'fg_energy_sum', 
    'total_energy_check', 'fg_energy_diff', 'energy_check_flag'
] and not c.endswith('_share')]

print(f"   Found {len(fg_energy_cols)} food group columns")

# Compute shares if not already computed
for col in fg_energy_cols:
    share_col = f"{col}_share"
    if share_col not in master.columns:
        master[share_col] = (master[col] / master['energy_kcal_day'] * 100).round(2)
        master[share_col] = master[share_col].replace([np.inf, -np.inf], np.nan)

# Get share columns
fg_share_cols = [c for c in master.columns if c.endswith('_share') and c != 'fg_energy_sum_share']

# For latest year: mean share of each food group
latest_year_data = master[master['year'] == latest_year].copy()
global_shares = pd.DataFrame({
    'food_group': [c.replace('_share', '') for c in fg_share_cols],
    'mean_share_pct': [latest_year_data[c].mean() for c in fg_share_cols]
})
global_shares = global_shares.sort_values('mean_share_pct', ascending=False)
global_shares.to_csv(TABLES_DIR / "global_foodgroup_shares_latest_year.csv", index=False)
print(f"   ✅ Saved: {TABLES_DIR / 'global_foodgroup_shares_latest_year.csv'}")

# Stacked bar plot
plt.figure(figsize=(12, 6))
food_groups = global_shares['food_group'].values
shares = global_shares['mean_share_pct'].values

# Create stacked bar (single bar)
bottom = 0
for i, (fg, share) in enumerate(zip(food_groups, shares)):
    plt.bar(0, share, bottom=bottom, label=fg, width=0.5)
    bottom += share

plt.xlim(-0.5, 0.5)
plt.xticks([0], ['Global Average'])
plt.ylabel('Share of Total Energy (%)', fontsize=12)
plt.title(f'Global Food Group Energy Shares ({latest_year})', fontsize=14, fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(FIGURES_DIR / "global_foodgroup_shares_latest_year.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved: {FIGURES_DIR / 'global_foodgroup_shares_latest_year.png'}")

# STEP 6 — Correlation Matrix
print("\n🔗 STEP 6: Computing correlation matrix...")

# Select variables for correlation
corr_vars = ['energy_kcal_day', 'protein_g_day', 'fat_g_day', 'sugar_g_day', 'obesity_pct']
# Add first 6 food group share columns
corr_vars.extend(fg_share_cols[:6])

# Filter to available columns
corr_vars = [v for v in corr_vars if v in master.columns]

# Compute correlation
corr_matrix = master[corr_vars].corr()
corr_matrix.to_csv(TABLES_DIR / "correlation_matrix.csv")
print(f"   ✅ Saved: {TABLES_DIR / 'correlation_matrix.csv'}")

# Plot heatmap using plt.imshow()
plt.figure(figsize=(10, 8))
im = plt.imshow(corr_matrix.values, aspect='auto', cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar(im, label='Correlation Coefficient')
plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45, ha='right')
plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
plt.title('Correlation Matrix: Nutrients and Obesity', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(FIGURES_DIR / "correlation_matrix.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved: {FIGURES_DIR / 'correlation_matrix.png'}")

# STEP 7 — Scatter Plots with Linear Fit
print("\n📉 STEP 7: Creating scatter plots with linear regression...")

# 1. Fat share vs obesity
# Compute fat_share = (fat_g_day * 9) / energy_kcal_day * 100
master['fat_share'] = (master['fat_g_day'] * 9 / master['energy_kcal_day'] * 100)

# Remove NaN values for plotting
plot_data = master[['fat_share', 'obesity_pct']].dropna()

if len(plot_data) > 0:
    x = plot_data['fat_share'].values
    y = plot_data['obesity_pct'].values
    
    # Linear regression
    coeffs = np.polyfit(x, y, 1)
    poly = np.poly1d(coeffs)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = poly(x_line)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, alpha=0.5, s=20)
    plt.plot(x_line, y_line, 'r-', linewidth=2, label=f'Linear fit: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
    plt.xlabel('Fat Share (% of Total Energy)', fontsize=12)
    plt.ylabel('Obesity Prevalence (%)', fontsize=12)
    plt.title('Fat Share vs Obesity Prevalence', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fat_share_vs_obesity.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {FIGURES_DIR / 'fat_share_vs_obesity.png'}")

# 2. Energy vs obesity
plot_data = master[['energy_kcal_day', 'obesity_pct']].dropna()

if len(plot_data) > 0:
    x = plot_data['energy_kcal_day'].values
    y = plot_data['obesity_pct'].values
    
    # Linear regression
    coeffs = np.polyfit(x, y, 1)
    poly = np.poly1d(coeffs)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = poly(x_line)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, alpha=0.5, s=20)
    plt.plot(x_line, y_line, 'r-', linewidth=2, label=f'Linear fit: y = {coeffs[0]:.3f}x + {coeffs[1]:.2f}')
    plt.xlabel('Energy Intake (kcal/capita/day)', fontsize=12)
    plt.ylabel('Obesity Prevalence (%)', fontsize=12)
    plt.title('Energy Intake vs Obesity Prevalence', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "energy_vs_obesity.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {FIGURES_DIR / 'energy_vs_obesity.png'}")

# STEP 8 — Boxplot: Energy vs Obesity Quartiles
print("\n📦 STEP 8: Creating boxplot by obesity quartiles...")

# Create obesity quartiles
master['obesity_quartile'] = pd.qcut(master['obesity_pct'], q=4, labels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)'])

# Prepare data for boxplot
quartile_data = []
quartile_labels = []
for quartile in ['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)']:
    data = master[master['obesity_quartile'] == quartile]['energy_kcal_day'].dropna()
    if len(data) > 0:
        quartile_data.append(data.values)
        quartile_labels.append(quartile)

if len(quartile_data) > 0:
    plt.figure(figsize=(10, 6))
    bp = plt.boxplot(quartile_data, tick_labels=quartile_labels, patch_artist=True)
    plt.ylabel('Energy Intake (kcal/capita/day)', fontsize=12)
    plt.xlabel('Obesity Quartile', fontsize=12)
    plt.title('Energy Intake Distribution by Obesity Quartile', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "energy_by_obesity_quartile.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {FIGURES_DIR / 'energy_by_obesity_quartile.png'}")

# STEP 9 — Save Updated Dataset
print("\n💾 STEP 9: Saving updated dataset with share columns...")
master.to_csv(DATA_DIR / "master_panel_with_shares.csv", index=False)
print(f"   ✅ Saved: {DATA_DIR / 'master_panel_with_shares.csv'}")
print(f"   Dataset now has {len(master.columns)} columns (added fat_share and obesity_quartile)")

# Final Summary
print("\n" + "=" * 60)
print("✅ EDA COMPLETE")
print("=" * 60)
print(f"\n📁 Output Summary:")
print(f"   Figures saved to: {FIGURES_DIR}")
print(f"   Tables saved to: {TABLES_DIR}")
print(f"\n📊 Generated Files:")
print(f"   Figures ({len(list(FIGURES_DIR.glob('*.png')))}):")
for fig in sorted(FIGURES_DIR.glob('*.png')):
    print(f"     - {fig.name}")
print(f"\n   Tables ({len(list(TABLES_DIR.glob('*.csv')))}):")
for table in sorted(TABLES_DIR.glob('*.csv')):
    print(f"     - {table.name}")
print(f"\n✅ All EDA outputs generated successfully!")

