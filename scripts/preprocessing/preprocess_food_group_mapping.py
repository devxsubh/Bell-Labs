"""
Preprocess Diet Composition Dataset - Create Item to Food Group Mapping
Creates a clean mapping: Item → Item Code → Food Group
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re

# Set paths
BASE_DIR = Path(__file__).parent.parent.parent  # Go up to project root
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
FOODBALANCE_DIR = RAW_DATA_DIR / "FoodBalanceSheet_data"
CLEANED_DIR = BASE_DIR / "data" / "processed" / "cleaned"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "mappings"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("FOOD GROUP MAPPING PREPROCESSING")
print("=" * 60)

print("\n🔧 Step 1: Loading datasets...")
# Load full item list from cleaned nutrients (most comprehensive)
try:
    nutrients = pd.read_csv(CLEANED_DIR / "Cleaned_FAO_Nutrients.csv", usecols=['item', 'item_code'])
    items_df = nutrients[['item', 'item_code']].drop_duplicates()
    print(f"   Loaded {len(items_df):,} items from cleaned nutrients dataset")
except:
    # Fallback: load from raw dataset
    main_file = FOODBALANCE_DIR / "FoodBalanceSheets_E_All_Data_(Normalized).csv"
    print("   Loading FAO main dataset (sample)...")
    df_sample = pd.read_csv(main_file, nrows=100000, low_memory=False)
    df_sample.columns = df_sample.columns.str.strip()
    items_df = df_sample[['Item Code', 'Item']].drop_duplicates()
    items_df = items_df.rename(columns={'Item': 'item', 'Item Code': 'item_code'})
    print(f"   Using {len(items_df):,} items from sample dataset")

# Load ItemCodes metadata
print("   Loading ItemCodes metadata...")
item_codes_file = FOODBALANCE_DIR / "FoodBalanceSheets_E_ItemCodes.csv"
item_codes = pd.read_csv(item_codes_file)
item_codes.columns = item_codes.columns.str.strip()
print(f"   Loaded {len(item_codes):,} item codes from metadata")

# Clean item names
def clean_item_name(item):
    """Clean and normalize item names"""
    if pd.isna(item):
        return None
    item = str(item).strip()
    # Remove trailing parentheses and text after commas if needed
    item = re.sub(r'\s*\([^)]*\)\s*$', '', item)  # Remove trailing (text)
    item = re.sub(r',\s*[^,]*$', '', item)  # Remove text after last comma
    # Replace multiple spaces with single space
    item = re.sub(r'\s+', ' ', item)
    return item.strip()

items_df['item'] = items_df['item'].apply(clean_item_name)
item_codes['Item'] = item_codes['Item'].apply(clean_item_name)

print("\n🔧 Step 2: Creating food group mapping rules...")
# Define food group mapping rules based on item names
food_group_rules = {
    'Cereals': [
        'cereal', 'wheat', 'rice', 'maize', 'corn', 'barley', 'oats', 'rye', 
        'millet', 'sorghum', 'quinoa', 'buckwheat', 'grain', 'flour'
    ],
    'Pulses': [
        'pulse', 'bean', 'lentil', 'pea', 'chickpea', 'legume', 'soybean', 
        'groundnut', 'peanut'
    ],
    'Starchy Roots': [
        'potato', 'cassava', 'yam', 'sweet potato', 'taro', 'root', 'tuber'
    ],
    'Sugar': [
        'sugar', 'sweetener', 'honey', 'syrup', 'molasses', 'sugarcane', 
        'sugar beet', 'fructose', 'glucose'
    ],
    'Oils & Fats': [
        'oil', 'fat', 'butter', 'ghee', 'margarine', 'lard', 'shortening', 
        'coconut oil', 'palm oil', 'sunflower oil', 'olive oil', 'soybean oil',
        'rapeseed oil', 'cottonseed oil', 'groundnut oil', 'sesame oil'
    ],
    'Meat': [
        'meat', 'beef', 'pork', 'chicken', 'poultry', 'lamb', 'mutton', 
        'goat', 'turkey', 'duck', 'bovine', 'sheep', 'goat', 'game'
    ],
    'Dairy & Eggs': [
        'milk', 'cheese', 'yogurt', 'yoghurt', 'cream', 'butter', 'egg', 
        'dairy', 'whey'
    ],
    'Fruit and Vegetables': [
        'fruit', 'vegetable', 'apple', 'banana', 'orange', 'citrus', 
        'tomato', 'onion', 'carrot', 'cabbage', 'lettuce', 'spinach', 
        'pepper', 'cucumber', 'melon', 'berry', 'grape', 'date', 'fig',
        'mango', 'pineapple', 'avocado', 'broccoli', 'cauliflower'
    ],
    'Alcoholic Beverages': [
        'beer', 'wine', 'alcohol', 'spirit', 'beverage alcoholic', 'whiskey',
        'vodka', 'rum', 'gin'
    ],
    'Aquatic Products': [
        'fish', 'seafood', 'aquatic', 'salmon', 'tuna', 'sardine', 'mackerel',
        'shrimp', 'crab', 'lobster', 'mollusc', 'cephalopod', 'crustacean'
    ],
    'Nuts & Seeds': [
        'nut', 'almond', 'walnut', 'cashew', 'pistachio', 'hazelnut',
        'seed', 'sunflower seed', 'sesame seed', 'pumpkin seed'
    ],
    'Spices & Herbs': [
        'spice', 'herb', 'pepper', 'cinnamon', 'clove', 'ginger', 'turmeric',
        'cumin', 'coriander', 'cardamom'
    ],
    'Beverages (Non-alcoholic)': [
        'coffee', 'tea', 'cocoa', 'chocolate', 'beverage', 'juice', 'soda'
    ],
    'Other': [
        'other', 'miscellaneous', 'residual'
    ]
}

def map_item_to_food_group(item):
    """Map item name to food group based on keywords"""
    if pd.isna(item):
        return 'Other'
    
    item_lower = str(item).lower()
    
    # Special cases first (more specific)
    if 'grand total' in item_lower or item_lower == 'total':
        return None  # Don't assign food group to totals
    
    # Check for specific patterns
    if 'butter' in item_lower or 'ghee' in item_lower:
        if 'oil' not in item_lower:
            return 'Dairy & Eggs'
        else:
            return 'Oils & Fats'
    
    if 'offal' in item_lower:
        return 'Meat'
    
    if 'fish' in item_lower and 'oil' in item_lower:
        return 'Oils & Fats'
    
    if 'milk' in item_lower and 'butter' not in item_lower:
        return 'Dairy & Eggs'
    
    if 'grape' in item_lower and 'wine' in item_lower:
        return 'Alcoholic Beverages'
    if 'grape' in item_lower and 'excl' in item_lower:
        return 'Fruit and Vegetables'
    
    if 'beverage' in item_lower:
        if 'alcohol' in item_lower or 'fermented' in item_lower:
            return 'Alcoholic Beverages'
        else:
            return 'Beverages'
    
    # Check each food group's keywords
    for food_group, keywords in food_group_rules.items():
        for keyword in keywords:
            if keyword in item_lower:
                # Additional checks for ambiguous cases
                if keyword == 'butter' and 'oil' in item_lower:
                    continue  # Skip, handled above
                if keyword == 'milk' and 'butter' in item_lower:
                    continue  # Skip, handled above
                return food_group
    
    # Generic fallbacks
    if 'animal product' in item_lower:
        if 'fat' in item_lower:
            return 'Oils & Fats'
        return 'Meat'
    if 'vegetal product' in item_lower:
        return 'Fruit and Vegetables'
    
    # Handle "Other" items - try to infer from context
    if ', other' in item_lower or 'other' in item_lower or 'others' in item_lower:
        # Try to infer from the main category
        if 'aquatic' in item_lower or 'fish' in item_lower or 'marine' in item_lower or 'seafood' in item_lower:
            return 'Aquatic Products'
        if 'citrus' in item_lower or 'fruit' in item_lower or 'fruits' in item_lower:
            return 'Fruit and Vegetables'
        if 'cereal' in item_lower:
            return 'Cereals'
        if 'meat' in item_lower:
            return 'Meat'
        if 'mollusc' in item_lower:
            return 'Aquatic Products'
        if 'oil' in item_lower or 'oilcrop' in item_lower:
            return 'Oils & Fats'
        if 'pulse' in item_lower:
            return 'Pulses'
        if 'root' in item_lower:
            return 'Starchy Roots'
        if 'spice' in item_lower:
            return 'Spices & Herbs'
        if 'vegetable' in item_lower:
            return 'Fruit and Vegetables'
        if 'sweetener' in item_lower:
            return 'Sugar'
    
    # Handle specific item name variations
    if 'butter, ghee' in item_lower or 'ghee' in item_lower:
        return 'Dairy & Eggs'
    if 'beverages, alcoholic' in item_lower or 'beverages, fermented' in item_lower:
        return 'Alcoholic Beverages'
    if 'grapes and products (excl wine)' in item_lower:
        return 'Fruit and Vegetables'
    if 'lemons, limes' in item_lower:
        return 'Fruit and Vegetables'
    if 'oranges, mandarines' in item_lower:
        return 'Fruit and Vegetables'
    if 'offals, edible' in item_lower or 'offal' in item_lower:
        return 'Meat'
    if 'olives (including preserved)' in item_lower or 'olive' in item_lower:
        if 'oil' in item_lower:
            return 'Oils & Fats'
        return 'Fruit and Vegetables'
    if 'tea (including mate)' in item_lower:
        return 'Beverages'
    if 'sugar (raw equivalent)' in item_lower:
        return 'Sugar'
    if 'fats, animals, raw' in item_lower:
        return 'Oils & Fats'
    if 'fish, body oil' in item_lower or 'fish, liver oil' in item_lower:
        return 'Oils & Fats'
    if 'fish, seafood' in item_lower:
        return 'Aquatic Products'
    
    return 'Other'

print("\n🔧 Step 3: Applying food group mapping...")
items_df['food_group'] = items_df['item'].apply(map_item_to_food_group)

# Remove items without food groups (like "Grand Total")
items_df = items_df[items_df['food_group'].notna()]

print(f"   Mapped {len(items_df):,} items to food groups")
print(f"   Food group distribution:")
print(items_df['food_group'].value_counts().sort_index())

print("\n🔧 Step 4: Merging with ItemCodes metadata...")
# Merge with ItemCodes to ensure we have correct item codes
# Convert item codes to numeric
items_df['item_code'] = pd.to_numeric(items_df['item_code'], errors='coerce')
item_codes['Item Code'] = pd.to_numeric(item_codes['Item Code'], errors='coerce')

# Try to merge on item code first
mapping_df = items_df.merge(
    item_codes[['Item Code', 'Item']],
    left_on='item_code',
    right_on='Item Code',
    how='left',
    suffixes=('', '_metadata')
)

# If item name from metadata is different, use it (it's more authoritative)
if 'Item_metadata' in mapping_df.columns:
    mapping_df['item'] = mapping_df['Item_metadata'].fillna(mapping_df['item'])
    mapping_df = mapping_df.drop(columns=['Item_metadata', 'Item Code'])

# Clean item names again after merge
mapping_df['item'] = mapping_df['item'].apply(clean_item_name)

print(f"   Final mapping has {len(mapping_df):,} rows")

print("\n🔧 Step 5: Standardizing food group names...")
# Standardize food group names to be simple and readable
food_group_standardization = {
    'Cereals': 'Cereals',
    'Pulses': 'Pulses',
    'Starchy Roots': 'Starchy Roots',
    'Sugar': 'Sugar',
    'Oils & Fats': 'Oils & Fats',
    'Meat': 'Meat',
    'Dairy & Eggs': 'Dairy & Eggs',
    'Fruit and Vegetables': 'Fruit and Vegetables',
    'Alcoholic Beverages': 'Alcoholic Beverages',
    'Aquatic Products': 'Aquatic Products',
    'Nuts & Seeds': 'Nuts & Seeds',
    'Spices & Herbs': 'Spices & Herbs',
    'Beverages (Non-alcoholic)': 'Beverages',
    'Other': 'Other'
}

mapping_df['food_group'] = mapping_df['food_group'].map(food_group_standardization).fillna('Other')

print("\n🔧 Step 6: Ensuring all items from nutrients are included...")
# Get all items from nutrients dataset
try:
    nutrients = pd.read_csv(CLEANED_DIR / "Cleaned_FAO_Nutrients.csv", usecols=['item', 'item_code'])
    all_nutrient_items = nutrients[['item', 'item_code']].drop_duplicates()
    
    # Find missing items (before cleaning to preserve original names)
    mapped_item_set = set(mapping_df['item'].unique())
    missing_items = all_nutrient_items[~all_nutrient_items['item'].isin(mapped_item_set)].copy()
    
    if len(missing_items) > 0:
        print(f"   Found {len(missing_items)} items not yet mapped, mapping them now...")
        
        # First, try to map based on similar items already in mapping
        def find_similar_food_group(item_name):
            """Find food group by matching with similar items"""
            item_lower = str(item_name).lower()
            
            # Check if it's a variation of an existing mapped item
            for mapped_item, food_group in zip(mapping_df['item'], mapping_df['food_group']):
                mapped_lower = str(mapped_item).lower()
                # Extract base words (ignore "other", "others", etc.)
                item_words = set([w for w in item_lower.split() if len(w) > 3 and w not in ['other', 'others', 'products', 'including']])
                mapped_words = set([w for w in mapped_lower.split() if len(w) > 3 and w not in ['other', 'others', 'products', 'including']])
                
                # If significant word overlap, use same food group
                if item_words and mapped_words and len(item_words & mapped_words) >= 1:
                    return food_group
            
            return None
        
        # Try to map missing items
        for idx, row in missing_items.iterrows():
            item_name = row['item']
            # Skip Grand Total
            if 'grand total' in str(item_name).lower() or str(item_name).lower() == 'total':
                continue
            
            # Try to find similar food group first
            similar_group = find_similar_food_group(item_name)
            if similar_group:
                missing_items.loc[idx, 'food_group'] = similar_group
            else:
                # Use the mapping function
                missing_items.loc[idx, 'food_group'] = map_item_to_food_group(item_name)
        
        # Clean item names for consistency
        missing_items['item'] = missing_items['item'].apply(clean_item_name)
        
        # Remove items without food groups
        missing_items = missing_items[missing_items['food_group'].notna()]
        
        if len(missing_items) > 0:
            # Merge with existing mapping
            mapping_df = pd.concat([mapping_df, missing_items], ignore_index=True)
            print(f"   Added {len(missing_items)} additional items")
except Exception as e:
    print(f"   Could not load nutrients dataset: {e}")

print("\n🔧 Step 7: Removing duplicates...")
# Remove duplicates based on (item, food_group)
# If same item maps to multiple food groups, keep the most specific one
initial_count = len(mapping_df)
mapping_df = mapping_df.drop_duplicates(subset=['item', 'food_group'], keep='first')

# If an item still appears multiple times with different food groups, 
# prioritize more specific groups over "Other"
mapping_df = mapping_df.sort_values('food_group', key=lambda x: x.map({
    'Other': 999,  # Lowest priority
    'Beverages': 8,
    'Spices & Herbs': 7,
    'Nuts & Seeds': 6,
    'Aquatic Products': 5,
    'Alcoholic Beverages': 4,
    'Fruit and Vegetables': 3,
    'Dairy & Eggs': 2,
    'Meat': 2,
    'Oils & Fats': 2,
    'Sugar': 2,
    'Starchy Roots': 2,
    'Pulses': 2,
    'Cereals': 1  # Highest priority for cereals
}))

mapping_df = mapping_df.drop_duplicates(subset=['item'], keep='first')

if len(mapping_df) < initial_count:
    print(f"   Removed {initial_count - len(mapping_df):,} duplicate mappings")

print(f"   Final unique items: {len(mapping_df):,}")

print("\n🔧 Step 8: Creating final mapping dataset...")
# Create final mapping with required columns
final_mapping = pd.DataFrame({
    'item': mapping_df['item'],
    'item_code': mapping_df['item_code'],
    'food_group': mapping_df['food_group']
})

# Sort by food group and item name
final_mapping = final_mapping.sort_values(['food_group', 'item']).reset_index(drop=True)

# Show summary
print("\n📊 Summary:")
print(f"   Total items mapped: {len(final_mapping):,}")
print(f"   Unique food groups: {final_mapping['food_group'].nunique()}")
print(f"\n   Food group distribution:")
for group, count in final_mapping['food_group'].value_counts().sort_index().items():
    print(f"      {group}: {count} items")

print(f"\n   Sample mappings:")
for group in sorted(final_mapping['food_group'].unique())[:5]:
    sample = final_mapping[final_mapping['food_group'] == group].head(3)
    print(f"\n   {group}:")
    for _, row in sample.iterrows():
        print(f"      {row['item']} (code: {row['item_code']})")

print("\n💾 Saving mapping file...")
output_file = OUTPUT_DIR / "Item_to_FoodGroup.csv"
final_mapping.to_csv(output_file, index=False)
print(f"   ✅ Saved to: {output_file}")
print(f"   File size: {output_file.stat().st_size / 1024:.2f} KB")

print("\n✅ Food group mapping complete!")
print("=" * 60)

