# Data Dictionary: Nutrition and Obesity Trends

This document describes the variables and data structure used in the Nutrition and Obesity Trends analysis.

## Data Sources

### Raw Datasets (from Kaggle)

**Kaggle Dataset**: `vivekvv12/foodsecurity-data`

The project uses three main datasets loaded from Kaggle:

1. **FoodBalanceSheet Data**: `FoodBalanceSheet_data/FoodBalanceSheets_E_All_Data_(Normalized).csv`
2. **FoodSecurity Data**: `FoodSecurity_data/Food_Security_Data_E_All_Data_(Normalized).csv`
3. **Population Data**: `Population_data/Population_E_All_Area_Groups_NOFLAG.csv`

### Integrated Dataset

**File**: `data/processed/integrated_nutrition_data.csv`

This is the unified dataset created by `scripts/integrate_datasets.py` that merges all three datasets.

## Integrated Dataset Structure

### Core Variables

| Variable Name | Type | Description | Units | Notes |
|--------------|------|-------------|-------|-------|
| Country | String | Country name | - | Standardized country names (from Area) |
| Year | Integer | Year of observation | YYYY | Range: varies by country and dataset |
| Population | Float | Total population | persons | Actual numbers (converted from thousands) |
| Nutrient_Type | String | Type of nutrient | - | Values: Fat, Protein, Calories, Food_Quantity, Sugar_Calories |
| Food_Item | String | Food item category | - | 238+ food items (e.g., Cereals, Fruits, Vegetables, etc.) |
| Element | String | Original element description | - | From FoodBalanceSheet (e.g., "Fat supply quantity (g/capita/day)") |
| Consumption_Value | Float | Consumption value | varies | Depends on nutrient type and element |
| Consumption_Unit | String | Unit of measurement | - | g/capita/day, kcal/capita/day, kg/capita/yr, etc. |

### FoodBalanceSheet Data Variables

**Source**: FAO Food Balance Sheets

| Variable Name | Type | Description | Units | Notes |
|--------------|------|-------------|-------|-------|
| Area Code | Integer | FAO area code | - | Unique identifier for area |
| Area Code (M49) | String | M49 area code | - | UN M49 standard code |
| Area | String | Area/Country name | - | Country or region name |
| Item Code | String | Food item code | - | CPC or FBS item code |
| Item Code (FBS) | String | Food Balance Sheet item code | - | Specific FBS classification |
| Item | String | Food item name | - | Food item description |
| Element Code | Integer | Element code | - | Unique identifier for element type |
| Element | String | Element description | - | E.g., "Fat supply quantity (g/capita/day)" |
| Year | Integer | Year | YYYY | Observation year |
| Unit | String | Unit of measurement | - | g/capita/day, kcal/capita/day, t, etc. |
| Value | Float | Consumption value | varies | Actual consumption value |
| Flag | String | Data quality flag | - | E: Estimated, I: Imputed, X: External |
| Note | String | Additional notes | - | Optional notes |

**Key Nutritional Elements**:
- `Fat supply quantity (g/capita/day)` - Element Code 684
- `Protein supply quantity (g/capita/day)` - Element Code 674
- `Food supply (kcal/capita/day)` - Element Code 664
- `Food supply quantity (kg/capita/yr)` - Element Code 645

### Population Data Variables

**Source**: FAO Population Estimates and Projections

| Variable Name | Type | Description | Units | Notes |
|--------------|------|-------------|-------|-------|
| Area Code | Integer | FAO area code | - | Unique identifier for area |
| Area Code (M49) | String | M49 area code | - | UN M49 standard code |
| Area | String | Area/Country name | - | Country or region name |
| Item Code | String | Population item code | - | E.g., "3010" |
| Item | String | Population item description | - | E.g., "Population - Est. & Proj." |
| Element Code | Integer | Element code | - | Unique identifier for element type |
| Element | String | Element description | - | E.g., "Total Population - Both sexes" |
| Unit | String | Unit of measurement | - | "1000 No" (thousands) |
| Y1950, Y1951, ..., Y2023 | Float | Population for each year | 1000 No | Population in thousands (needs conversion) |

**Note**: Population data is in wide format (years as columns) and is transformed to long format during integration.

### FoodSecurity Data Variables

**Source**: FAO Food Security Indicators

| Variable Name | Type | Description | Units | Notes |
|--------------|------|-------------|-------|-------|
| Area Code | Integer | FAO area code | - | Unique identifier for area |
| Area Code (M49) | String | M49 area code | - | UN M49 standard code |
| Area | String | Area/Country name | - | Country or region name |
| Item Code | String | Food security item code | - | E.g., "21010" |
| Item | String | Food security indicator | - | E.g., "Average dietary energy supply adequacy" |
| Element Code | Integer | Element code | - | Unique identifier for element type |
| Element | String | Element description | - | E.g., "Value" |
| Year Code | String | Year code | - | E.g., "20002002" (3-year average) |
| Year | String | Year range | - | E.g., "2000-2002" |
| Unit | String | Unit of measurement | - | "%" |
| Value | Float | Food security value | % | Indicator value |
| Flag | String | Data quality flag | - | E: Estimated, I: Imputed, X: External |

## Derived Variables

### Per Capita Consumption

**Note**: Some elements in FoodBalanceSheet are already per capita (e.g., "Fat supply quantity (g/capita/day)"). For other elements, per capita is calculated during integration.

**Formula** (when needed): `Per_Capita = Total_Consumption / Population`

**Description**: Normalizes nutrient consumption by population size to enable cross-country comparisons.

**Unit**: Varies by nutrient type (g/capita/day, kcal/capita/day, kg/capita/yr)

### Nutritional Diversity Index

**Formula**: `Nutritional_Diversity = Number_of_Non_Zero_Nutrients / Total_Number_of_Nutrients`

**Description**: Measures the diversity of nutrients consumed (0 = no diversity, 1 = maximum diversity).

**Range**: 0 to 1

**Note**: This is calculated in analysis scripts, not in the integrated dataset.

### Growth Rate

**Formula**: `Growth_Rate = ((Value_Year_N - Value_Year_0) / Value_Year_0) * 100`

**Description**: Percentage change in consumption over a specified time period.

**Unit**: Percentage (%)

**Note**: This is calculated in analysis scripts, not in the integrated dataset.

## Data Quality Notes

### Missing Values
- Some countries may have missing data for certain years
- Missing values are handled appropriately during analysis
- Missing data patterns are documented in flags (E, I, X)

### Data Consistency
- Country names are standardized across datasets during integration
- Year values are validated for temporal consistency
- Units are consistent within each variable type
- Population data is converted from thousands to actual numbers

### Data Limitations
- Data quality varies by country
- Some countries may have incomplete time series
- Measurement methods may vary across countries
- FoodSecurity data uses 3-year averages (not annual)
- Population data in wide format requires transformation

### Data Flags

FoodBalanceSheet and FoodSecurity data include quality flags:
- **E**: Estimated value
- **I**: Imputed value (by receiving agency)
- **X**: External source (figure from external organization)

## Data Access

### Kaggle Dataset
- **Dataset Name**: `vivekvv12/foodsecurity-data`
- **Access Method**: `kagglehub` (recommended) or Kaggle API
- **See**: README.md for setup instructions

### Original Sources
- **FAO (Food and Agriculture Organization)**: Food Balance Sheets and Food Security data
- **USDA Economic Research Service**: Nutrition and health statistics (referenced, not directly in dataset)
- **World Bank**: Population and economic data (optional, not included in current dataset)
- **WHO (World Health Organization)**: Health outcomes data (optional, not included in current dataset)

### Integration Process
- Datasets are loaded from Kaggle using `kagglehub`
- Population data is transformed from wide to long format
- All datasets are merged on Area and Year
- Per capita consumption is calculated where needed
- Integrated dataset saved to: `data/processed/integrated_nutrition_data.csv`

## Notes

- **Population Units**: Population data is in thousands and is converted to actual numbers during integration
- **Year Formats**: Years are integer values (YYYY format)
- **Country Names**: Standardized during integration (title case, stripped whitespace)
- **Temporal Coverage**: 
  - FoodBalanceSheet: 2010-2023 (verify in your data)
  - Population: 1950-2023
  - FoodSecurity: 2000-2023 (3-year averages)
- **Units**: 
  - Fat: g/capita/day
  - Protein: g/capita/day
  - Calories: kcal/capita/day
  - Food Quantity: kg/capita/yr


