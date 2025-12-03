import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("EXTENDED EXPLORATORY DATA ANALYSIS")
print("=" * 70)



# ============================================================================
# STEP 1: Load & Prepare Data
# ============================================================================
print("\n📂 STEP 1: Loading and preparing data...")

DATA_DIR = Path("data/processed")
FINAL_DIR = DATA_DIR / "final"
OUTPUT_DIR = Path("data/outputs")
EXTENDED_TABLES_DIR = OUTPUT_DIR / "extended" / "tables"
EXTENDED_FIGURES_DIR = OUTPUT_DIR / "extended" / "figures"

# Create output directories
EXTENDED_TABLES_DIR.mkdir(parents=True, exist_ok=True)
EXTENDED_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
print(f"   Created output directories")

# Load data with fallback
input_file_primary = OUTPUT_DIR / "master_panel_with_shares.csv"
input_file_fallback = FINAL_DIR / "master_panel_final.csv"

if input_file_primary.exists():
    master = pd.read_csv(input_file_primary)
    print(f"   Loaded from: {input_file_primary}")
elif input_file_fallback.exists():
    master = pd.read_csv(input_file_fallback)
    print(f"   Loaded from: {input_file_fallback} (fallback)")
else:
    raise FileNotFoundError("Neither master_panel_with_shares.csv nor master_panel_final.csv found")

print(f"   Initial dataset: {len(master):,} rows, {len(master.columns)} columns")

# Convert numerical columns
numerical_cols = ['year', 'energy_kcal_day', 'protein_g_day', 'fat_g_day', 
                  'sugar_g_day', 'obesity_pct', 'population']
for col in numerical_cols:
    if col in master.columns:
        master[col] = pd.to_numeric(master[col], errors='coerce')

# Identify food-group share columns (columns ending with '_share')
share_cols = [c for c in master.columns if c.endswith('_share')]
for col in share_cols:
    master[col] = pd.to_numeric(master[col], errors='coerce')

# Compute fat_share if not present
if 'fat_share' not in master.columns and 'fat_g_day' in master.columns and 'energy_kcal_day' in master.columns:
    master['fat_share'] = (master['fat_g_day'] * 9 / master['energy_kcal_day'] * 100).round(2)
    master['fat_share'] = master['fat_share'].replace([np.inf, -np.inf], np.nan)
    print(f"   Computed fat_share column")

print(f"   Converted numerical columns")
print(f"   Found {len(share_cols)} food-group share columns")
print(f"   Year range: {int(master['year'].min())} - {int(master['year'].max())}")
print(f"   Countries: {master['country'].nunique()}")



# ============================================================================
# STEP 2: Region Detection & Handling
# ============================================================================
print("\n🌍 STEP 2: Region detection and handling...")

# Check for existing region column
region_cols = ['region', 'Region', 'continent', 'Continent', 'ParentLocation']
region_col = None
for col in region_cols:
    if col in master.columns:
        region_col = col
        master['region'] = master[col]
        print(f"   Found region column: {col}")
        break

# If no region column, try to load mapping file
if region_col is None:
    mapping_file = DATA_DIR / "country_region_mapping.csv"
    if mapping_file.exists():
        region_map = pd.read_csv(mapping_file)
        master = master.merge(region_map, on='country', how='left')
        if 'region' in master.columns:
            print(f"   Loaded region mapping from: {mapping_file}")
        else:
            print(f"   ⚠️  Warning: Region mapping file exists but 'region' column not found")
            master['region'] = 'Global'
    else:
        print(f"   ⚠️  Warning: No region column or mapping file found. Using 'Global' for all countries")
        master['region'] = 'Global'

# Fill any missing regions with 'Global'
master['region'] = master['region'].fillna('Global')
print(f"   Regions identified: {sorted(master['region'].unique())}")



# ============================================================================
# STEP 3: Regional Analysis
# ============================================================================
print("\n📊 STEP 3: Regional analysis...")

# Compute regional-year means
regional_summary = master.groupby(['region', 'year']).agg({
    'energy_kcal_day': 'mean',
    'obesity_pct': 'mean',
    'population': 'sum'
}).reset_index()
regional_summary.columns = ['region', 'year', 'energy_kcal_day_mean', 'obesity_pct_mean', 'population_sum']
regional_summary = regional_summary.round(2)
regional_summary.to_csv(EXTENDED_TABLES_DIR / "regional_summary_by_year.csv", index=False)
print(f"   ✅ Saved: regional_summary_by_year.csv ({len(regional_summary)} rows)")

# Plot regional obesity trends
plt.figure(figsize=(12, 7))
for region in sorted(regional_summary['region'].unique()):
    region_data = regional_summary[regional_summary['region'] == region]
    plt.plot(region_data['year'], region_data['obesity_pct_mean'], 
             marker='o', linewidth=2, markersize=6, label=region)
plt.title('Regional Obesity Trends Over Time', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Average Obesity Prevalence (%)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(EXTENDED_FIGURES_DIR / "regional_obesity_trends.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Saved: regional_obesity_trends.png")

# Food-group shares by region for latest year
latest_year = int(master['year'].max())
latest_data = master[master['year'] == latest_year].copy()

if len(share_cols) > 0:
    regional_fg_shares = latest_data.groupby('region')[share_cols].mean().reset_index()
    # Round to 2 decimal places
    for col in share_cols:
        regional_fg_shares[col] = regional_fg_shares[col].round(2)
    regional_fg_shares.to_csv(EXTENDED_TABLES_DIR / "regional_foodgroup_shares_latest_year.csv", index=False)
    print(f"   ✅ Saved: regional_foodgroup_shares_latest_year.csv")
    
    # Stacked bar for top 6 regions by population
    region_pop = latest_data.groupby('region')['population'].sum().sort_values(ascending=False)
    top_regions = region_pop.head(6).index.tolist()
    
    # Prepare data for stacked bar
    top_regions_data = regional_fg_shares[regional_fg_shares['region'].isin(top_regions)].copy()
    top_regions_data = top_regions_data.set_index('region')
    top_regions_data = top_regions_data.reindex(top_regions)  # Maintain order
    
    plt.figure(figsize=(14, 7))
    bottom = np.zeros(len(top_regions))
    for col in share_cols:
        plt.bar(range(len(top_regions)), top_regions_data[col].values, 
                bottom=bottom, label=col.replace('_share', ''), width=0.6)
        bottom += top_regions_data[col].values
    
    plt.xticks(range(len(top_regions)), top_regions, rotation=45, ha='right')
    plt.ylabel('Share of Total Energy (%)', fontsize=12)
    plt.title(f'Food Group Energy Shares by Region ({latest_year}) - Top 6 by Population', 
              fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(EXTENDED_FIGURES_DIR / "regional_foodgroup_shares_top_regions.png", 
                dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: regional_foodgroup_shares_top_regions.png")

# ============================================================================
# STEP 4: Clustering (Diet Typologies)
# ============================================================================
print("\n🔍 STEP 4: Clustering analysis (diet typologies)...")

# Check if scikit-learn is available
try:
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.preprocessing import StandardScaler
    sklearn_available = True
    print("   scikit-learn is available")
except ImportError:
    sklearn_available = False
    print("   ⚠️  scikit-learn not available. Skipping clustering analysis.")

if sklearn_available:
    # Build feature table for latest year
    feature_cols = ['energy_kcal_day', 'fat_share', 'protein_g_day']
    # Add first 6 food-group share columns if available
    feature_cols.extend(share_cols[:6])
    
    # Filter to available columns
    feature_cols = [c for c in feature_cols if c in latest_data.columns]
    
    # Create country-level feature table
    country_features = latest_data[['country'] + feature_cols].copy()
    country_features = country_features.dropna()
    
    if len(country_features) >= 10:
        print(f"   Using {len(country_features)} countries with complete data")
        print(f"   Features: {feature_cols}")
        
        # Extract feature matrix
        X = country_features[feature_cols].values
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Try k from 2 to 6
        k_range = range(2, 7)
        silhouette_scores = []
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_scaled)
            score = silhouette_score(X_scaled, labels)
            silhouette_scores.append(score)
            print(f"   k={k}: silhouette_score = {score:.3f}")
        
        # Choose best k
        best_k_idx = np.argmax(silhouette_scores)
        best_k = k_range[best_k_idx]
        print(f"   Best k: {best_k} (silhouette_score = {silhouette_scores[best_k_idx]:.3f})")
        
        # Fit final model with best k
        kmeans_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        country_features['cluster'] = kmeans_final.fit_predict(X_scaled)
        
        # Save silhouette scores
        silhouette_df = pd.DataFrame({
            'k': list(k_range),
            'silhouette_score': silhouette_scores
        })
        silhouette_df.to_csv(EXTENDED_TABLES_DIR / f"silhouette_scores_{latest_year}.csv", index=False)
        print(f"   ✅ Saved: silhouette_scores_{latest_year}.csv")
        
        # Save cluster assignments
        cluster_assignments = country_features[['country', 'cluster']].copy()
        cluster_assignments.to_csv(EXTENDED_TABLES_DIR / f"country_clusters_k{best_k}_{latest_year}.csv", index=False)
        print(f"   ✅ Saved: country_clusters_k{best_k}_{latest_year}.csv")
        
        # Plot cluster centroids
        centroids = kmeans_final.cluster_centers_
        plt.figure(figsize=(12, 7))
        for i in range(best_k):
            plt.plot(range(len(feature_cols)), centroids[i], 
                    marker='o', linewidth=2, markersize=8, label=f'Cluster {i}')
        plt.xticks(range(len(feature_cols)), feature_cols, rotation=45, ha='right')
        plt.ylabel('Standardized Feature Value', fontsize=12)
        plt.title(f'Cluster Centroids (k={best_k}, {latest_year})', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(EXTENDED_FIGURES_DIR / f"cluster_centroids_k{best_k}_{latest_year}.png", 
                    dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: cluster_centroids_k{best_k}_{latest_year}.png")
        
        # Merge cluster assignments back to master
        master = master.merge(cluster_assignments, on='country', how='left', suffixes=('', '_cluster'))
        if 'cluster_cluster' in master.columns:
            master['cluster'] = master['cluster_cluster']
            master = master.drop(columns=['cluster_cluster'])
        
        clustering_done = True
        clustering_k = best_k
    else:
        print(f"   ⚠️  Too few countries ({len(country_features)}) for clustering. Need at least 10.")
        clustering_done = False
        clustering_k = None
else:
    clustering_done = False
    clustering_k = None

# ============================================================================
# STEP 5: Dietary Diversity Index (Shannon)
# ============================================================================
print("\n🌐 STEP 5: Computing Dietary Diversity Index (Shannon)...")

if len(share_cols) > 0:
    # Compute Shannon diversity for each country-year
    def shannon_diversity(shares):
        """Compute Shannon diversity index from food group shares"""
        # Filter out zeros and NaN
        p = shares[shares > 0].values
        if len(p) == 0:
            return np.nan
        # Normalize to sum to 1
        p = p / p.sum()
        # Compute Shannon index
        return -np.sum(p * np.log(p))
    
    # Apply to each row
    master['diet_diversity_shannon'] = master[share_cols].apply(shannon_diversity, axis=1)
    
    # Save per-country-year DDI
    ddi_country_year = master[['country', 'year', 'diet_diversity_shannon']].copy()
    ddi_country_year = ddi_country_year.dropna()
    ddi_country_year.to_csv(EXTENDED_TABLES_DIR / "diet_diversity_shannon_country_year.csv", index=False)
    print(f"   ✅ Saved: diet_diversity_shannon_country_year.csv ({len(ddi_country_year)} rows)")
    
    # Regional average DDI for latest year (re-filter to get updated data)
    latest_data = master[master['year'] == latest_year].copy()
    ddi_regional = latest_data.groupby('region')['diet_diversity_shannon'].mean().reset_index()
    ddi_regional.columns = ['region', 'avg_ddi']
    ddi_regional = ddi_regional.sort_values('avg_ddi', ascending=False).round(3)
    ddi_regional.to_csv(EXTENDED_TABLES_DIR / "ddi_by_region_latest_year.csv", index=False)
    print(f"   ✅ Saved: ddi_by_region_latest_year.csv")
    
    # Plot DDI by region
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(ddi_regional)), ddi_regional['avg_ddi'].values, width=0.6)
    plt.xticks(range(len(ddi_regional)), ddi_regional['region'], rotation=45, ha='right')
    plt.ylabel('Average Dietary Diversity Index (Shannon)', fontsize=12)
    plt.title(f'Dietary Diversity by Region ({latest_year})', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(EXTENDED_FIGURES_DIR / "ddi_by_region_latest_year.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: ddi_by_region_latest_year.png")
else:
    print("   ⚠️  No food-group share columns found. Skipping DDI computation.")
    master['diet_diversity_shannon'] = np.nan

# ============================================================================
# STEP 6: Nutrition Transition (Change Over Time)
# ============================================================================
print("\n📈 STEP 6: Nutrition transition analysis...")

first_year = int(master['year'].min())
last_year = int(master['year'].max())

# Get countries with both first and last year
countries_first = set(master[master['year'] == first_year]['country'].unique())
countries_last = set(master[master['year'] == last_year]['country'].unique())
countries_both = countries_first & countries_last

print(f"   Countries with data in both {first_year} and {last_year}: {len(countries_both)}")

# Compute percent change for each country
transition_data = []
for country in countries_both:
    first_data = master[(master['country'] == country) & (master['year'] == first_year)].iloc[0]
    last_data = master[(master['country'] == country) & (master['year'] == last_year)].iloc[0]
    
    # Compute percent change
    def pct_change(old_val, new_val):
        if pd.isna(old_val) or pd.isna(new_val):
            return np.nan
        if old_val == 0 or abs(old_val) < 1e-10:
            return np.nan
        return ((new_val - old_val) / old_val) * 100
    
    # Get fat_share, compute if missing
    fat_share_first = first_data.get('fat_share', np.nan)
    fat_share_last = last_data.get('fat_share', np.nan)
    
    # If fat_share missing, compute from fat_g_day and energy
    if pd.isna(fat_share_first) and 'fat_g_day' in first_data and 'energy_kcal_day' in first_data:
        if first_data['fat_g_day'] > 0 and first_data['energy_kcal_day'] > 0:
            fat_share_first = (first_data['fat_g_day'] * 9 / first_data['energy_kcal_day'] * 100)
    if pd.isna(fat_share_last) and 'fat_g_day' in last_data and 'energy_kcal_day' in last_data:
        if last_data['fat_g_day'] > 0 and last_data['energy_kcal_day'] > 0:
            fat_share_last = (last_data['fat_g_day'] * 9 / last_data['energy_kcal_day'] * 100)
    
    fat_share_pct_change = pct_change(fat_share_first, fat_share_last)
    energy_pct_change = pct_change(first_data.get('energy_kcal_day', np.nan),
                                   last_data.get('energy_kcal_day', np.nan))
    obesity_pct_change = pct_change(first_data.get('obesity_pct', np.nan),
                                    last_data.get('obesity_pct', np.nan))
    
    # If percent change not possible, use absolute change for obesity
    if pd.isna(obesity_pct_change):
        obesity_abs_change = last_data.get('obesity_pct', np.nan) - first_data.get('obesity_pct', np.nan)
    else:
        obesity_abs_change = np.nan
    
    transition_data.append({
        'country': country,
        'fat_share_pct_change': fat_share_pct_change,
        'energy_kcal_day_pct_change': energy_pct_change,
        'obesity_pct_change': obesity_pct_change,
        'obesity_abs_change': obesity_abs_change
    })

transition_df = pd.DataFrame(transition_data)
transition_df.to_csv(EXTENDED_TABLES_DIR / "nutrition_transition_pct_change_first_last.csv", index=False)
print(f"   ✅ Saved: nutrition_transition_pct_change_first_last.csv")

# Top 20 countries with largest increase in fat_share
top20_fat = transition_df.nlargest(20, 'fat_share_pct_change')[['country', 'fat_share_pct_change']].copy()
top20_fat.to_csv(EXTENDED_TABLES_DIR / "top20_fat_share_increase.csv", index=False)
print(f"   ✅ Saved: top20_fat_share_increase.csv")

# Scatter plot: fat_share change vs obesity change
plot_data = transition_df[['fat_share_pct_change', 'obesity_pct_change', 'obesity_abs_change']].dropna(subset=['fat_share_pct_change'])

# Use percent change if available, otherwise absolute change
if plot_data['obesity_pct_change'].notna().sum() > 10:
    y_col = 'obesity_pct_change'
    y_label = 'Obesity Percent Change (%)'
    plot_data = plot_data[plot_data['obesity_pct_change'].notna()]
else:
    y_col = 'obesity_abs_change'
    y_label = 'Obesity Absolute Change (%)'
    plot_data = plot_data[plot_data['obesity_abs_change'].notna()]

if len(plot_data) > 0:
    plt.figure(figsize=(10, 6))
    plt.scatter(plot_data['fat_share_pct_change'], plot_data[y_col], alpha=0.6, s=30)
    plt.xlabel('Fat Share Percent Change (%)', fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title('Fat Share Change vs Obesity Change (First to Last Year)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(EXTENDED_FIGURES_DIR / "fat_change_vs_obesity_change.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: fat_change_vs_obesity_change.png")

# ============================================================================
# STEP 7: Outlier Detection (Latest Year)
# ============================================================================
print("\n🔍 STEP 7: Outlier detection (latest year)...")

# Compute z-scores (re-filter to get updated data)
latest_data = master[master['year'] == latest_year].copy()
latest_data['energy_z'] = (latest_data['energy_kcal_day'] - latest_data['energy_kcal_day'].mean()) / latest_data['energy_kcal_day'].std()
latest_data['obesity_z'] = (latest_data['obesity_pct'] - latest_data['obesity_pct'].mean()) / latest_data['obesity_pct'].std()

# High obesity but low energy
outliers_high_ob_low_energy = latest_data[
    (latest_data['obesity_z'] > 2) & (latest_data['energy_z'] < -1)
][['country', 'energy_kcal_day', 'obesity_pct', 'energy_z', 'obesity_z']].copy()
outliers_high_ob_low_energy.to_csv(EXTENDED_TABLES_DIR / "outliers_high_obesity_low_energy_latest_year.csv", index=False)
print(f"   ✅ Saved: outliers_high_obesity_low_energy_latest_year.csv ({len(outliers_high_ob_low_energy)} outliers)")

# High energy but low obesity
outliers_high_energy_low_ob = latest_data[
    (latest_data['energy_z'] > 2) & (latest_data['obesity_z'] < -1)
][['country', 'energy_kcal_day', 'obesity_pct', 'energy_z', 'obesity_z']].copy()
outliers_high_energy_low_ob.to_csv(EXTENDED_TABLES_DIR / "outliers_high_energy_low_obesity_latest_year.csv", index=False)
print(f"   ✅ Saved: outliers_high_energy_low_obesity_latest_year.csv ({len(outliers_high_energy_low_ob)} outliers)")

# ============================================================================
# STEP 8: Save Extended Master Dataset
# ============================================================================
print("\n💾 STEP 8: Saving extended master dataset...")

# Merge transition data back to master
if 'transition_df' in locals():
    master = master.merge(transition_df[['country', 'fat_share_pct_change', 'energy_kcal_day_pct_change', 
                                         'obesity_pct_change', 'obesity_abs_change']], 
                         on='country', how='left')

master.to_csv(EXTENDED_TABLES_DIR / "master_extended_features.csv", index=False)
print(f"   ✅ Saved: master_extended_features.csv ({len(master)} rows, {len(master.columns)} columns)")

# ============================================================================
# STEP 9: Diagnostics and Console Output
# ============================================================================
print("\n" + "=" * 70)
print("DIAGNOSTICS SUMMARY")
print("=" * 70)
print(f"\n📊 Dataset Information:")
print(f"   Countries processed: {master['country'].nunique()}")
print(f"   Years covered: {int(master['year'].min())} - {int(master['year'].max())}")
print(f"   Latest year: {latest_year}")
print(f"   Total observations: {len(master):,}")

print(f"\n🔍 Clustering:")
if clustering_done:
    print(f"   ✅ Clustering performed: k={clustering_k}")
else:
    print(f"   ⚠️  Clustering skipped (scikit-learn not available or insufficient data)")

print(f"\n📁 Main Output Files:")
print(f"   Tables directory: {EXTENDED_TABLES_DIR}")
print(f"   Figures directory: {EXTENDED_FIGURES_DIR}")
print(f"\n   Key tables:")
print(f"     - regional_summary_by_year.csv")
print(f"     - regional_foodgroup_shares_latest_year.csv")
if clustering_done:
    print(f"     - silhouette_scores_{latest_year}.csv")
    print(f"     - country_clusters_k{clustering_k}_{latest_year}.csv")
print(f"     - diet_diversity_shannon_country_year.csv")
print(f"     - nutrition_transition_pct_change_first_last.csv")
print(f"     - master_extended_features.csv")
print(f"\n   Key figures:")
print(f"     - regional_obesity_trends.png")
print(f"     - regional_foodgroup_shares_top_regions.png")
if clustering_done:
    print(f"     - cluster_centroids_k{clustering_k}_{latest_year}.png")
print(f"     - ddi_by_region_latest_year.png")
print(f"     - fat_change_vs_obesity_change.png")

print("\n" + "=" * 70)
print("✅ EXTENDED EDA COMPLETE")
print("=" * 70)

