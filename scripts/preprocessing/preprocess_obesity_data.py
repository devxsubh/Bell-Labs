"""
Preprocess WHO Obesity Dataset
Creates a clean country-year obesity dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set paths
BASE_DIR = Path(__file__).parent.parent.parent  # Go up to project root
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "cleaned"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("WHO OBESITY DATA PREPROCESSING")
print("=" * 60)

print("\n🔧 Step 1: Loading dataset...")
# Load the dataset
obesity_file = RAW_DATA_DIR / "data.csv"
df = pd.read_csv(obesity_file, low_memory=False)
print(f"   Loaded {len(df):,} rows")

print("\n🔧 Step 2: Cleaning column names...")
# Clean column names - strip leading/trailing spaces
df.columns = df.columns.str.strip()
print(f"   Column names: {list(df.columns)[:10]}...")

print("\n🔧 Step 3: Filtering for correct indicator...")
# Filter for obesity indicator - contains "obesity" AND "BMI"
initial_count = len(df)
obesity_mask = (
    df['Indicator'].str.contains('obesity', case=False, na=False) &
    df['Indicator'].str.contains('BMI', case=False, na=False)
)
df = df[obesity_mask]
print(f"   Filtered to {len(df):,} rows (removed {initial_count - len(df):,} rows)")
print(f"   Unique indicators: {df['Indicator'].unique()}")

print("\n🔧 Step 4: Filtering for Both sexes...")
# Filter for "Both sexes"
initial_count = len(df)
df = df[df['Dim1'] == 'Both sexes']
print(f"   Filtered to {len(df):,} rows (removed {initial_count - len(df):,} rows)")

print("\n🔧 Step 5: Filtering for adults (Age Group)...")
# Filter for adults - check if Dim2 contains age group info
if 'Dim2' in df.columns:
    initial_count = len(df)
    # Filter for "18+" or "Adults" in age group
    age_mask = (
        df['Dim2'].str.contains('18', case=False, na=False) |
        df['Dim2'].str.contains('adult', case=False, na=False)
    )
    df = df[age_mask]
    print(f"   Filtered to {len(df):,} rows (removed {initial_count - len(df):,} rows)")
    print(f"   Age groups: {df['Dim2'].unique()}")
else:
    print("   No Age Group column found, skipping age filter")

print("\n🔧 Step 6: Selecting and renaming columns...")
# Select and rename columns
# Location → country
# SpatialDimValueCode → iso3
# Period → year
# FactValueNumeric → obesity_pct (use numeric value, not Value which has confidence intervals)

# Use FactValueNumeric if available, otherwise try to extract from Value
if 'FactValueNumeric' in df.columns:
    obesity_values = df['FactValueNumeric']
else:
    # Fallback: extract numeric from Value column (e.g., "10.0 [7.7-12.8]" -> 10.0)
    obesity_values = df['Value'].astype(str).str.extract(r'([\d.]+)')[0]

cleaned_df = pd.DataFrame({
    'country': df['Location'],
    'iso3': df['SpatialDimValueCode'],
    'year': df['Period'],
    'obesity_pct': obesity_values
})

print(f"   Selected {len(cleaned_df):,} rows with required columns")

print("\n🔧 Step 7: Cleaning values...")
# Convert year to integer
cleaned_df['year'] = pd.to_numeric(cleaned_df['year'], errors='coerce')

# Convert obesity_pct to float
cleaned_df['obesity_pct'] = pd.to_numeric(cleaned_df['obesity_pct'], errors='coerce')

# Remove NA rows
initial_count = len(cleaned_df)
cleaned_df = cleaned_df.dropna(subset=['country', 'year', 'obesity_pct', 'iso3'])
print(f"   Removed {initial_count - len(cleaned_df):,} rows with missing values")
print(f"   Remaining rows: {len(cleaned_df):,}")

print("\n🔧 Step 8: Cleaning country names...")
# Strip whitespace from country names
cleaned_df['country'] = cleaned_df['country'].astype(str).str.strip()

# Standardize country names to match FAO naming conventions
# Load FAO country names for reference
try:
    fao_pop = pd.read_csv(BASE_DIR / "data" / "processed" / "cleaned" / "Cleaned_FAO_Population.csv", usecols=['country'])
    fao_countries = set(fao_pop['country'].str.strip().str.lower())
    print(f"   Loaded {len(fao_countries)} FAO country names for reference")
    
    # Create a mapping for common name variations
    country_mapping = {}
    for country in cleaned_df['country'].unique():
        country_lower = str(country).lower().strip()
        # Try to find matching FAO country name
        for fao_country in fao_countries:
            # Exact match
            if country_lower == fao_country:
                country_mapping[country] = fao_pop[fao_pop['country'].str.lower() == fao_country]['country'].iloc[0]
                break
            # Partial match (country name contains or is contained in FAO name)
            elif country_lower in fao_country or fao_country in country_lower:
                if len(country_lower) > 5 and len(fao_country) > 5:  # Avoid short matches
                    country_mapping[country] = fao_pop[fao_pop['country'].str.lower() == fao_country]['country'].iloc[0]
                    break
    
    # Apply mapping where available
    if country_mapping:
        cleaned_df['country'] = cleaned_df['country'].map(country_mapping).fillna(cleaned_df['country'])
        print(f"   Mapped {len(country_mapping)} country names to FAO conventions")
except Exception as e:
    print(f"   Could not load FAO country names: {e}")
    print("   Using original country names")

# Remove duplicates (keep first occurrence)
initial_count = len(cleaned_df)
cleaned_df = cleaned_df.drop_duplicates(subset=['country', 'year'], keep='first')
if len(cleaned_df) < initial_count:
    print(f"   Removed {initial_count - len(cleaned_df):,} duplicate rows")

print(f"   Final dataset: {len(cleaned_df):,} rows")

# Show summary
print("\n📊 Summary:")
print(f"   Countries: {cleaned_df['country'].nunique()}")
print(f"   Years: {cleaned_df['year'].min():.0f} - {cleaned_df['year'].max():.0f}")
print(f"   Obesity range: {cleaned_df['obesity_pct'].min():.2f}% - {cleaned_df['obesity_pct'].max():.2f}%")
print(f"   Mean obesity: {cleaned_df['obesity_pct'].mean():.2f}%")
print(f"\n   Sample countries: {sorted(cleaned_df['country'].unique())[:10]}")

print("\n💾 Saving cleaned dataset...")
output_file = OUTPUT_DIR / "Cleaned_Obesity.csv"
cleaned_df.to_csv(output_file, index=False)
print(f"   ✅ Saved to: {output_file}")
print(f"   File size: {output_file.stat().st_size / 1024:.2f} KB")

print("\n✅ Preprocessing complete!")
print("=" * 60)

