"""
Preprocess FAO Food Balance Sheet Data
Converts messy FAO data into usable nutrient and population datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set paths
BASE_DIR = Path(__file__).parent.parent.parent  # Go up to project root
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "FoodBalanceSheet_data"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "cleaned"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("FAO DATA PREPROCESSING")
print("=" * 60)

print("\n🔧 Step 1: Loading FAO main dataset...")
# Load the main dataset
main_file = RAW_DATA_DIR / "FoodBalanceSheets_E_All_Data_(Normalized).csv"
df = pd.read_csv(main_file, low_memory=False)
print(f"   Loaded {len(df):,} rows")

print("\n🔧 Step 2: Cleaning column names and values...")
# Clean column names - remove leading/trailing spaces
df.columns = df.columns.str.strip()

# Clean string columns - strip leading/trailing spaces
string_cols = ['Area', 'Item', 'Element', 'Unit', 'Flag']
for col in string_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

print(f"   Column names: {list(df.columns)}")

print("\n🔧 Step 3: EXTRACTING population rows (not deleting)...")
# Extract population rows BEFORE removing them
population_keywords = ["Total Population - Both sexes"]
population_mask = df['Element'].str.contains('|'.join(population_keywords), case=False, na=False)

# Extract population data
population_df = df[population_mask].copy()
print(f"   Extracted {len(population_df):,} population rows")

# Convert population values
# FAO population unit is usually "1000 No" (thousands)
population_df['Value'] = pd.to_numeric(population_df['Value'], errors='coerce')

# Check unit and convert
if 'Unit' in population_df.columns:
    # Convert from thousands to actual population
    # Most FAO population data is in "1000 No" format
    unit_mask = population_df['Unit'].str.contains('1000', case=False, na=False)
    if unit_mask.any():
        population_df.loc[unit_mask, 'population'] = population_df.loc[unit_mask, 'Value'] * 1000
        print(f"   Converted {unit_mask.sum():,} rows from thousands to actual population")
    else:
        # If not in thousands, assume already in actual numbers
        population_df['population'] = population_df['Value']
        print("   Population already in actual numbers")

# Load AreaCodes for country name standardization
print("   Loading AreaCodes for country standardization...")
area_codes = pd.read_csv(RAW_DATA_DIR / "FoodBalanceSheets_E_AreaCodes.csv")
area_codes.columns = area_codes.columns.str.strip()
if 'Area' in area_codes.columns:
    area_codes['Area'] = area_codes['Area'].str.strip().str.replace('"', '')
area_codes = area_codes.drop_duplicates(subset=['Area Code'], keep='first')

# Convert codes to numeric for joining
population_df['Area Code'] = pd.to_numeric(population_df['Area Code'], errors='coerce')
area_codes['Area Code'] = pd.to_numeric(area_codes['Area Code'], errors='coerce')

# Join Area names to standardize country names
population_df = population_df.merge(area_codes[['Area Code', 'Area']], on='Area Code', how='left', suffixes=('', '_standardized'))
if 'Area_standardized' in population_df.columns:
    population_df['country'] = population_df['Area_standardized'].fillna(population_df['Area'])
else:
    population_df['country'] = population_df['Area']

# Create cleaned population table
cleaned_population = pd.DataFrame({
    'country': population_df['country'],
    'year': pd.to_numeric(population_df['Year'], errors='coerce'),
    'population': population_df['population'].astype(int)
})

# Remove rows with missing data
cleaned_population = cleaned_population.dropna(subset=['country', 'year', 'population'])
cleaned_population = cleaned_population.drop_duplicates(subset=['country', 'year'], keep='first')

print(f"   Final population dataset: {len(cleaned_population):,} rows")
print(f"   Countries: {cleaned_population['country'].nunique()}")
print(f"   Years: {cleaned_population['year'].min():.0f} - {cleaned_population['year'].max():.0f}")

# Save population dataset
pop_output_file = OUTPUT_DIR / "Cleaned_FAO_Population.csv"
cleaned_population.to_csv(pop_output_file, index=False)
print(f"   ✅ Saved population to: {pop_output_file}")

print("\n🔧 Step 4: Removing population rows from nutrient processing...")
# Now remove population rows from the working dataframe
initial_count = len(df)
df = df[~population_mask]
print(f"   Removed {initial_count - len(df):,} population rows from nutrient processing")
print(f"   Remaining rows: {len(df):,}")

print("\n🔧 Step 5: Filtering necessary nutrient elements...")
# Filter for nutrient supply elements
# Keep both per-capita per-day AND total values (we'll convert totals using population)
nutrient_patterns = [
    r'Food supply.*kcal/capita/day',
    r'Food supply.*kcal',  # Total kcal (will convert)
    r'Protein supply.*g/capita/day',
    r'Protein supply.*\(t\)',  # Total tonnes (will convert)
    r'Fat supply.*g/capita/day',
    r'Fat supply.*\(t\)',  # Total tonnes (will convert)
    r'Sugar supply.*g/capita/day',
    r'Sugar supply.*\(t\)'  # Total tonnes (will convert)
]

nutrient_pattern = '|'.join(nutrient_patterns)
df = df[df['Element'].str.contains(nutrient_pattern, case=False, na=False, regex=True)]
print(f"   Filtered to {len(df):,} nutrient supply rows")

print("\n🔧 Step 6: Loading metadata files...")
# Load metadata files
print("   Loading ItemCodes...")
item_codes = pd.read_csv(RAW_DATA_DIR / "FoodBalanceSheets_E_ItemCodes.csv")
item_codes.columns = item_codes.columns.str.strip()
print(f"   Loaded {len(item_codes):,} item codes")

print("   Loading ElementCodes...")
element_codes = pd.read_csv(RAW_DATA_DIR / "FoodBalanceSheets_E_Elements.csv")
element_codes.columns = element_codes.columns.str.strip()
print(f"   Loaded {len(element_codes):,} element codes")

print("   Loading AreaCodes...")
area_codes = pd.read_csv(RAW_DATA_DIR / "FoodBalanceSheets_E_AreaCodes.csv")
area_codes.columns = area_codes.columns.str.strip()
if 'Area' in area_codes.columns:
    area_codes['Area'] = area_codes['Area'].str.strip().str.replace('"', '')
area_codes = area_codes.drop_duplicates(subset=['Area Code'], keep='first')
print(f"   Loaded {len(area_codes):,} unique area codes")

# Convert code columns to numeric for proper joining
df['Item Code'] = pd.to_numeric(df['Item Code'], errors='coerce')
df['Element Code'] = pd.to_numeric(df['Element Code'], errors='coerce')
df['Area Code'] = pd.to_numeric(df['Area Code'], errors='coerce')

item_codes['Item Code'] = pd.to_numeric(item_codes['Item Code'], errors='coerce')
element_codes['Element Code'] = pd.to_numeric(element_codes['Element Code'], errors='coerce')
area_codes['Area Code'] = pd.to_numeric(area_codes['Area Code'], errors='coerce')

# Join metadata
print("\n🔧 Step 7: Mapping metadata...")
# Join Item names
if 'Item' in df.columns and df['Item'].notna().any():
    print("   Item column already exists")
else:
    df = df.merge(item_codes[['Item Code', 'Item']], on='Item Code', how='left', suffixes=('', '_new'))
    if 'Item_new' in df.columns:
        df['Item'] = df['Item_new'].fillna(df['Item'])
        df = df.drop(columns=['Item_new'])

# Join Element descriptions
df = df.merge(element_codes[['Element Code', 'Element']], on='Element Code', how='left', suffixes=('', '_standardized'))
if 'Element_standardized' in df.columns:
    df['Element'] = df['Element_standardized'].fillna(df['Element'])
    df = df.drop(columns=['Element_standardized'])

# Join Area names (standardize country names)
df = df.merge(area_codes[['Area Code', 'Area']], on='Area Code', how='left', suffixes=('', '_standardized'))
if 'Area_standardized' in df.columns:
    df['country'] = df['Area_standardized'].fillna(df['Area'])
else:
    df['country'] = df['Area']

print(f"   Metadata mapping complete. Rows: {len(df):,}")

print("\n🔧 Step 8: Standardizing units...")
# Convert Value to numeric
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

# Store original unit
df['unit_original'] = df['Unit'].copy()

# Create standardized unit and value columns
df['unit_standard'] = df['Unit'].copy()
df['value_standard'] = df['Value'].copy()

# Load population data for conversions
print("   Loading population data for per-capita conversions...")
pop_lookup = cleaned_population.set_index(['country', 'year'])['population'].to_dict()

# Function to get population for a country-year
def get_population(country, year):
    return pop_lookup.get((country, year), None)

# Convert kg/capita/year to g/capita/day
kg_year_mask = df['Unit'].str.contains('kg.*cap.*year', case=False, na=False, regex=True)
if kg_year_mask.any():
    df.loc[kg_year_mask, 'value_standard'] = df.loc[kg_year_mask, 'Value'] * 1000 / 365
    df.loc[kg_year_mask, 'unit_standard'] = 'g/capita/day'
    print(f"   Converted {kg_year_mask.sum():,} rows from kg/capita/year to g/capita/day")

# Convert tonnes to g/capita/day using population
tonnes_mask = df['Unit'].str.contains(r'tonnes|\(t\)', case=False, na=False, regex=True)
if tonnes_mask.any():
    print(f"   Converting {tonnes_mask.sum():,} rows from tonnes to g/capita/day...")
    converted = 0
    for idx in df[tonnes_mask].index:
        country = df.loc[idx, 'country']
        year = pd.to_numeric(df.loc[idx, 'Year'], errors='coerce')
        pop = get_population(country, year)
        if pop and pop > 0:
            # Convert tonnes to grams: value * 1,000,000
            total_grams = df.loc[idx, 'Value'] * 1_000_000
            # Convert to per-capita per-day: (total_grams / population) / 365
            df.loc[idx, 'value_standard'] = (total_grams / pop) / 365
            df.loc[idx, 'unit_standard'] = 'g/capita/day'
            converted += 1
    print(f"   Successfully converted {converted:,} rows using population data")

# Convert total kcal to kcal/capita/day
# Only convert rows that are NOT already per-capita (exclude rows with 'cap' or 'capita' in unit)
kcal_total_mask = (
    df['Unit'].str.contains('kcal', case=False, na=False) & 
    ~df['Unit'].str.contains('cap', case=False, na=False) &
    ~df['unit_standard'].str.contains('kcal.*cap', case=False, na=False, regex=True)
)
if kcal_total_mask.any():
    print(f"   Converting {kcal_total_mask.sum():,} rows from total kcal to kcal/capita/day...")
    converted = 0
    for idx in df[kcal_total_mask].index:
        country = df.loc[idx, 'country']
        year = pd.to_numeric(df.loc[idx, 'Year'], errors='coerce')
        pop = get_population(country, year)
        unit = str(df.loc[idx, 'Unit']).lower()
        value = df.loc[idx, 'Value']
        
        if pop and pop > 0:
            # Handle "million Kcal" - convert to total kcal first
            if 'million' in unit:
                total_kcal = value * 1_000_000
            else:
                # Assume already in total kcal
                total_kcal = value
            
            # Convert total kcal to per-capita per-day: (total_kcal / population) / 365
            df.loc[idx, 'value_standard'] = (total_kcal / pop) / 365
            df.loc[idx, 'unit_standard'] = 'kcal/capita/day'
            converted += 1
    print(f"   Successfully converted {converted:,} rows using population data")

# Handle rows that are already in per-capita per-day format (don't convert them)
# These should keep their original values
already_per_capita = (
    df['Unit'].str.contains('kcal.*cap', case=False, na=False, regex=True) |
    df['Unit'].str.contains('g/cap', case=False, na=False, regex=True)
)
df.loc[already_per_capita, 'value_standard'] = df.loc[already_per_capita, 'Value']
df.loc[already_per_capita, 'unit_standard'] = df.loc[already_per_capita, 'Unit']

# Standardize unit names to consistent format
kcal_mask = df['unit_standard'].str.contains('kcal.*cap', case=False, na=False, regex=True)
g_mask = df['unit_standard'].str.contains('g.*cap', case=False, na=False, regex=True)

df.loc[kcal_mask, 'unit_standard'] = 'kcal/capita/day'
df.loc[g_mask, 'unit_standard'] = 'g/capita/day'

# Keep only standardized per-capita per-day units
df = df[df['unit_standard'].isin(['kcal/capita/day', 'g/capita/day'])]
print(f"   Final unit distribution:\n{df['unit_standard'].value_counts()}")

print("\n🔧 Step 9: Mapping elements to standardized names...")
# Map element names to standardized nutrient names
element_mapping = {
    'Food supply (kcal/capita/day)': 'energy_kcal_day',
    'Food supply (kcal)': 'energy_kcal_day',
    'Protein supply quantity (g/capita/day)': 'protein_g_day',
    'Protein supply (g/capita/day)': 'protein_g_day',
    'Protein supply quantity (t)': 'protein_g_day',
    'Fat supply quantity (g/capita/day)': 'fat_g_day',
    'Fat supply (g/capita/day)': 'fat_g_day',
    'Fat supply quantity (t)': 'fat_g_day',
    'Sugar supply quantity (g/capita/day)': 'sugar_g_day',
    'Sugar supply (g/capita/day)': 'sugar_g_day',
    'Sugar supply quantity (t)': 'sugar_g_day'
}

def map_element_name(element):
    element_str = str(element)
    for key, value in element_mapping.items():
        if key in element_str:
            return value
    return element_str

df['element'] = df['Element'].apply(map_element_name)

print("\n🔧 Step 10: Adding food group mapping (placeholder)...")
# TODO: Create proper food group mapping from diet composition file or item codes
# For now, add a placeholder column
df['food_group'] = None
print("   Food group mapping: TODO (to be implemented with diet composition mapping)")

print("\n🔧 Step 11: Creating final cleaned nutrient dataset...")
# Create the final cleaned dataset with all required columns
cleaned_nutrients = pd.DataFrame({
    'country': df['country'],
    'year': pd.to_numeric(df['Year'], errors='coerce'),
    'item': df['Item'],
    'item_code': df['Item Code'],
    'food_group': df['food_group'],
    'element': df['element'],
    'element_code': df['Element Code'],
    'unit_standard': df['unit_standard'],
    'value_standard': df['value_standard'],
    'unit_original': df['unit_original'],
    'flag': df['Flag'] if 'Flag' in df.columns else None
})

# Remove rows with missing critical data
cleaned_nutrients = cleaned_nutrients.dropna(subset=['country', 'year', 'element', 'value_standard'])

# Remove duplicates (keep first occurrence)
initial_count = len(cleaned_nutrients)
cleaned_nutrients = cleaned_nutrients.drop_duplicates(
    subset=['country', 'year', 'item', 'element'], 
    keep='first'
)
if len(cleaned_nutrients) < initial_count:
    print(f"   Removed {initial_count - len(cleaned_nutrients):,} duplicate rows")

print(f"   Final cleaned nutrient dataset: {len(cleaned_nutrients):,} rows")

# Show summary
print("\n📊 Summary:")
print(f"   Countries: {cleaned_nutrients['country'].nunique()}")
print(f"   Years: {cleaned_nutrients['year'].min():.0f} - {cleaned_nutrients['year'].max():.0f}")
print(f"   Elements: {sorted(cleaned_nutrients['element'].unique())}")
print(f"   Items: {cleaned_nutrients['item'].nunique()}")

print("\n💾 Saving cleaned datasets...")
nutrients_output_file = OUTPUT_DIR / "Cleaned_FAO_Nutrients.csv"
cleaned_nutrients.to_csv(nutrients_output_file, index=False)
print(f"   ✅ Saved nutrients to: {nutrients_output_file}")
print(f"   File size: {nutrients_output_file.stat().st_size / (1024*1024):.2f} MB")

print(f"   ✅ Population already saved to: {pop_output_file}")
print(f"   File size: {pop_output_file.stat().st_size / (1024*1024):.2f} MB")

print("\n✅ Preprocessing complete!")
print("=" * 60)
