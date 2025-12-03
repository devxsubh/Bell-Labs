# Dataset Analysis and Integration Report

## Overview

This document provides a comprehensive analysis of the three datasets (FoodBalanceSheet, FoodSecurity, Population) and documents the integration process for Phase 1 of the Nutrition and Obesity Trends project.

## Dataset Analysis

### 1. FoodBalanceSheet Data

**File**: `data/raw/FoodBalanceSheet_data/FoodBalanceSheets_E_All_Data_(Normalized).csv`

**Structure**:
- Format: Normalized CSV
- Columns: Area Code, Area Code (M49), Area, Item Code, Item Code (FBS), Item, Element Code, Element, Year Code, Year, Unit, Value, Flag, Note
- Size: ~4.8 million rows (604 MB)

**Contains**:
- **Nutritional Elements**:
  - Fat supply quantity (g/capita/day) - Element Code 684
  - Fat supply quantity (t) - Element Code 681
  - Protein supply quantity (g/capita/day) - Element Code 674
  - Protein supply quantity (t) - Element Code 671
  - Food supply (kcal) - Element Code 661
  - Food supply (kcal/capita/day) - Element Code 664
  - Food supply quantity (kg/capita/yr) - Element Code 645

- **Food Items**: 238+ different food items/categories including:
  - Cereals and cereal products
  - Sugar and sweeteners
  - Fruits and fruit products
  - Vegetables and vegetable products
  - Dairy products
  - Meat and meat products
  - And many more categories

- **Coverage**:
  - Countries: All countries in FAO database
  - Years: 2010-2023 (and potentially historical data)
  - Time series: Annual data

**Key Features**:
- Per capita data already calculated for key nutrients (fat, protein, calories)
- Total quantities also available for calculation
- Food items categorized for food group analysis

### 2. FoodSecurity Data

**File**: `data/raw/FoodSecurity_data/Food_Security_Data_E_All_Data_(Normalized).csv`

**Structure**:
- Format: Normalized CSV
- Columns: Area Code, Area Code (M49), Area, Item Code, Item, Element Code, Element, Year Code, Year, Unit, Value, Flag
- Size: ~279,000 rows (48 MB)

**Contains**:
- **Food Security Indicators**:
  - Average dietary energy supply adequacy (percent) (3-year average)
  - Confidence intervals (lower and upper bounds)
  - Various food security metrics

- **Coverage**:
  - Countries: Subset of countries with food security data
  - Years: 2000-2023 (3-year averages)
  - Time series: 3-year rolling averages

**Key Features**:
- Provides dietary energy supply adequacy metrics
- Includes confidence intervals for uncertainty quantification
- Complementary to FoodBalanceSheet data

### 3. Population Data

**File**: `data/raw/Population_data/Population_E_All_Area_Groups_NOFLAG.csv`

**Structure**:
- Format: Wide CSV (years as columns)
- Columns: Area Code, Area Code (M49), Area, Item Code, Item, Element Code, Element, Unit, Y1950, Y1951, ..., Y2023
- Size: ~172 rows (358 KB)

**Contains**:
- **Demographic Elements**:
  - Total Population - Both sexes (Element Code 511)
  - Total Population - Male (Element Code 512)
  - Total Population - Female (Element Code 513)
  - Urban population (Element Code 561)
  - Rural population (Element Code 551)

- **Coverage**:
  - Countries: All countries in FAO database
  - Years: 1950-2023 (historical data available)
  - Time series: Annual data

**Key Features**:
- Long historical time series (70+ years)
- Population data in thousands (needs conversion)
- Wide format (needs transformation to long format)

## Data Completeness Assessment

### Available for Research Questions

**Question 1 - Sugar, Fat, Protein, Fiber Consumption**:
- Fat: ✅ Available (g/capita/day)
- Protein: ✅ Available (g/capita/day)
- Sugar: ✅ Available (Sugar & Sweeteners items exist)
- Fiber: ⚠️ Need to verify in Item codes
- Regional patterns: ✅ Can analyze by Area/Country

**Question 3 - Dietary Homogenization**:
- Food consumption by country: ✅ Available
- Food items by country: ✅ Available
- Temporal data: ✅ Available (2010-2023)
- Can compare dietary patterns across countries over time

**Question 4 - Food Groups Consumption Changes**:
- Food groups: ✅ Cereals, Dairy, Fruits, Vegetables available
- Temporal data: ✅ Available (2010-2023)
- Historical data: ⚠️ Need to verify full range
- Processed foods: ⚠️ Need to categorize from items

**Question 6 - Interactive Bar Plot with Per Capita Consumption**:
- Nutrient consumption: ✅ Available
- Population data: ✅ Available
- Per capita calculation: ✅ Can be done
- Country and year data: ✅ Available

**Question 5 - Income and Nutritional Quality**:
- Calorie intake: ✅ Available
- Nutritional diversity: ✅ Can calculate
- Income/GDP data: ❌ NOT properly available in datasets

**Question 7 - Predictive and Descriptive Analysis**:
- Descriptive analysis: ✅ Can be done
- Predictive modeling: ⚠️ Limited data without health outcomes

**Question 2 - Obesity and Diabetes Correlation**:
- Dietary consumption: ✅ Available
- Obesity rates: ❌ NOT in provided datasets
- Diabetes rates: ❌ NOT in provided datasets

## Missing Data Requirements

### Critical Missing Data

1. **Health Outcomes Data** (Required for Question 2):
   - Obesity rates by country and year
   - Diabetes prevalence by country and year
   - Cardiovascular disease rates (optional)
   
   **Recommended Sources**:
   - WHO (World Health Organization) Global Health Observatory
   - Our World in Data - Health and Nutrition
   - Kaggle: Obesity and diabetes datasets

2. **Economic Data** (Required for Question 5):
   - GDP per capita by country and year
   - Income levels (World Bank income classifications)
   - Economic development indicators
   
   **Recommended Sources**:
   - World Bank Open Data
   - Our World in Data - Economic Development
   - Kaggle: GDP and economic indicators datasets

## Integration Process

### Step 1: Data Structure Analysis

**Common Keys Identified**:
- **Area/Country**: Country names (need standardization)
- **Year**: Year values (need format alignment)

**Key Challenges**:
- Population data in wide format (needs transformation)
- Year formats may differ (string vs integer)
- Country name standardization needed
- Population values in thousands (need conversion)

### Step 2: Data Transformation

**Population Data Transformation**:
- Melt from wide to long format
- Extract year from column names (Y1950 → 1950)
- Convert population from thousands to actual numbers
- Filter for total population (both sexes)

**FoodBalanceSheet Data Extraction**:
- Filter for relevant nutritional elements:
  - Fat supply (g/capita/day)
  - Protein supply (g/capita/day)
  - Food supply (kcal/capita/day)
  - Food supply quantity (kg/capita/yr)
- Map elements to nutrient types
- Extract sugar items if available

**Country Name Standardization**:
- Strip whitespace
- Title case conversion
- Handle special characters

### Step 3: Data Integration

**Merge Strategy**:
1. Merge FoodBalanceSheet with Population on Area and Year (inner join)
2. Merge FoodSecurity data on Area and Year (left join)
3. Calculate per capita consumption where needed
4. Create unified schema

**Unified Schema**:
- Country: Standardized country name
- Year: Integer year
- Population: Total population (actual numbers)
- Nutrient_Type: Fat, Protein, Calories, Food_Quantity, Sugar_Calories
- Food_Item: Food item category
- Element: Original element description
- Consumption_Value: Consumption value
- Consumption_Unit: Unit of measurement

### Step 4: Data Quality Checks

**Quality Issues Identified**:
- Missing values in some years/countries
- Data flags (E, I, X) indicate data quality
- Need to handle outliers
- Need to validate population consistency

**Data Quality Measures**:
- Check for missing values
- Validate data consistency
- Identify outliers
- Standardize units

### Step 5: Integrated Dataset

**Output File**: `data/processed/final/master_panel_final.csv` (current format)

**Dataset Characteristics**:
- Format: CSV (normalized)
- Rows: Varies based on merge (expected: millions)
- Columns: Country, Year, Population, Nutrient_Type, Food_Item, Consumption_Value, Consumption_Unit, etc.
- Coverage: Countries with matching data across all sources

## Data Quality Issues

### Known Issues

1. **Missing Values**:
   - Some countries may have missing data for certain years
   - Food security data may not cover all countries
   - Historical data may be incomplete

2. **Data Flags**:
   - 'E': Estimated value
   - 'I': Imputed value
   - 'X': External source
   - Need to consider data quality in analysis

3. **Year Coverage**:
   - FoodBalanceSheet: 2010-2023 (need to verify)
   - Population: 1950-2023
   - FoodSecurity: 2000-2023 (3-year averages)
   - Overlap period: 2010-2023

4. **Country Coverage**:
   - Not all countries present in all datasets
   - Regional aggregations may be included
   - Need to filter for country-level data only

###Plan

### For Phase 1

1. **Proceed with Integration**:
   - Integrate available datasets
   - Answer questions that can be answered (Questions 1, 3, 4, 6)
   - Document missing data requirements

2. **Data Verification**:
   - Verify sugar and fiber availability in FoodBalanceSheet
   - Check historical data availability
   - Validate population data consistency

3. **Data Enhancement**:
   - Source health outcomes data for Question 2
   - Source economic data for Question 5
   - Consider additional food categorization for processed foods

### For Future Phases

1. **Expand Data Sources**:
   - Integrate WHO health data
   - Integrate World Bank economic data
   - Add subnational data where available

2. **Data Quality Improvements**:
   - Handle missing values more systematically
   - Implement data quality scoring
   - Add data lineage tracking

3. **Advanced Analysis**:
   - Implement time series analysis
   - Add predictive modeling capabilities
   - Create more sophisticated visualizations

## Integration Output

**Final Dataset**: `data/processed/final/master_panel_final.csv`

**Schema**:
- `Country`: Standardized country name (from Area)
- `Year`: Integer year
- `Population`: Total population (actual numbers, not thousands)
- `Nutrient_Type`: Fat, Protein, Calories, Food_Quantity, Sugar_Calories
- `Food_Item`: Food item category from FoodBalanceSheet
- `Element`: Original element description
- `Consumption_Value`: Consumption value
- `Consumption_Unit`: Unit of measurement

## Next Steps

1. ✅ Run integration script to create unified dataset

2. ✅ Verify data quality and completeness

3. ✅ Perform exploratory data analysis

4. ✅ Create visualizations for available questions

5. ⏳ Source missing health and economic data (for Questions 2 and 5)
6. ⏳ Integrate additional datasets (if needed)
7. ⏳ Proceed with full analysis

---

**Report Generated**: [Date]
**Phase**: Phase 1 - Dataset Analysis and Integration
**Status**: Complete

