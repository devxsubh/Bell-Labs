# Methodology: Nutrition and Obesity Trends Analysis

## Overview

This document describes the detailed methodology for analyzing global nutrition and obesity trends. The analysis examines dietary patterns, health outcomes, and their relationships across different countries and regions over time.

## Data Sources

### Primary Data Sources

1. **Kaggle Dataset**
   - Platform: Kaggle
   - Dataset Name: `vivekvv12/foodsecurity-data`
   - Method: Fetched directly from Kaggle using `kagglehub`
   - Contains: 
     - FoodBalanceSheet data (nutrition consumption data)
     - Population data (demographic data)
     - FoodSecurity data (food security indicators)
   - Original Sources:
     - FAO (Food and Agriculture Organization)
     - USDA Economic Research Service (referenced)

2. **Additional Data Sources** (Optional - Not in current dataset)
   - World Bank: Economic indicators (GDP per capita, income levels)
   - World Health Organization (WHO): Global health statistics (obesity, diabetes)
   - Our World in Data: Health and nutrition visualizations

## Data Processing Pipeline

### 1. Data Collection

**Step 1.1: Load from Kaggle**
- Use `kagglehub` to load datasets directly from Kaggle
- Script: `scripts/integrate_datasets.py` (main integration)
- Alternative: `scripts/load_data_from_kaggle.py` (optional caching)
- Datasets loaded:
  - FoodBalanceSheet: `FoodBalanceSheet_data/FoodBalanceSheets_E_All_Data_(Normalized).csv`
  - Population: `Population_data/Population_E_All_Area_Groups_NOFLAG.csv`
  - FoodSecurity: `Food_Security_Data_E_All_Data_(Normalized).csv`

**Step 1.2: Data Loading**
- Load FoodBalanceSheet data (nutrition consumption data)
- Load Population data (demographic data)
- Load FoodSecurity data (food security indicators)


### 2. Data Cleaning

**Step 2.1: Handle Missing Values**
- Identify missing values
- Apply appropriate strategies:
  - Drop rows with all missing values
  - Fill missing values with median/mean where appropriate
  - Preserve missing values for analysis where needed

**Step 2.2: Standardize Country Names**
- Standardize country names across datasets
- Handle country name variations
- Map country codes to standard names

**Step 2.3: Data Validation**
- Check for duplicate records
- Validate data types
- Check for outliers and anomalies
- Verify temporal consistency

### 3. Feature Engineering

**Step 3.1: Calculate Per Capita Consumption**
- Formula: `Consumption per capita = Total Nutrient Consumption / Population`
- Calculate for each nutrient (protein, fat, sugar, fiber, calories, etc.)
- Calculate for each country and year

**Step 3.2: Create Derived Metrics**
- Nutritional diversity index
- Processed vs. fresh food ratio
- Macronutrient balance (protein:fat:carbohydrate ratio)
- Growth rates over time periods

**Step 3.3: Temporal Aggregation**
- Aggregate data by year and country
- Calculate rolling averages and trends
- Identify period-specific patterns

### 4. Data Integration

**Step 4.1: Transform Population Data**
- Transform Population data from wide to long format
- Extract year from column names (Y1950 → 1950)
- Convert population from thousands to actual numbers
- Filter for total population (both sexes)

**Step 4.2: Merge Datasets**
- Merge FoodBalanceSheet data with Population data on Area and Year
- Merge FoodSecurity data on Area and Year (optional, left join)
- Standardize country names across datasets
- Use common keys: Area (Country), Year

**Step 4.3: Data Alignment**
- Align temporal coverage (handle different year ranges)
- Handle mismatched countries
- Preserve all available data
- Calculate per capita consumption where needed
- Save integrated dataset: `data/processed/integrated_nutrition_data.csv`

## Analysis Methods

### 1. Descriptive Analysis

**1.1 Summary Statistics**
- Mean, median, standard deviation
- Min, max, quartiles
- Skewness and kurtosis

**1.2 Regional Analysis**
- Compare dietary patterns by region
- Identify regional differences
- Analyze regional trends

**1.3 Temporal Trend Analysis**
- Analyze changes over time
- Calculate growth rates
- Identify trend patterns

### 2. Correlation Analysis

**2.1 Nutrient-Health Correlations**
- Calculate correlation between nutrients and health outcomes
- Identify strong associations
- Analyze correlation patterns

**2.2 Cross-Nutrient Correlations**
- Analyze relationships between different nutrients
- Identify dietary patterns
- Method: Correlation matrices

### 3. Predictive Analysis

**3.1 Model Selection**
- Linear Regression
- Ridge Regression
- Lasso Regression
- Random Forest
- Gradient Boosting

**3.2 Model Training**
- Split data into training and testing sets
- Standardize features
- Train multiple models
- Evaluate model performance

**3.3 Model Evaluation**
- R² Score
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- Cross-validation

**3.4 Feature Importance**
- Analyze feature importance
- Identify key predictors

### 4. Visualization

**4.1 Interactive Visualizations**
- Interactive bar plot with country/nutrient selection
- Plotly-based visualizations

**4.2 Static Visualizations**
- Distribution plots
- Correlation heatmaps
- Trend line plots

## Analysis Philosophy

### Design Principles

1. **Evidence-Based Approach**
   - All conclusions grounded in statistical analysis
   - Validated against multiple data sources
   - Transparent methodology

2. **Transparency**
   - All data processing steps documented
   - Assumptions clearly stated
   - Limitations acknowledged

3. **Reproducibility**
   - Code structured for replication
   - Version control for data and code
   - Clear documentation

4. **Comprehensive Coverage**
   - Multiple dimensions (temporal, spatial, nutritional, economic)
   - Various analytical methods
   - Multiple perspectives

### Methodological Considerations

**Causality vs. Correlation**
- Acknowledge that correlation does not imply causation
- Dietary patterns may be confounded by other factors
- Interpret findings with caution

**Data Quality**
- Account for varying data quality across countries
- Handle missing data appropriately
- Validate data sources

**Bias**
- Recognize potential biases in data collection
- Account for measurement errors
- Consider underreporting issues

**Temporal Considerations**
- Consider time lags between diet and health outcomes
- Account for temporal trends
- Handle irregular time series

## Limitations

1. **Data Quality**
   - Varying data quality across countries
   - Missing data may affect some analyses
   - Measurement errors possible

2. **Causality**
   - Correlation does not imply causation
   - Confounding factors may exist
   - Reverse causality possible

3. **Temporal Coverage**
   - Limited time period for some countries
   - Gaps in time series
   - Missing historical data

4. **Scope**
   - Focus on country-level data
   - Limited subnational data
   - Simplified nutritional metrics

## Future Enhancements

1. **Expanded Data Sources**
   - Include more recent years
   - Add subnational data
   - Integrate additional health indicators

2. **Advanced Analytics**
   - Causal inference methods
   - Machine learning models
   - Time series forecasting

3. **Enhanced Visualizations**
   - Interactive world maps
   - Network analysis
   - Animated time-lapse visualizations

4. **Policy Analysis**
   - Impact assessment of nutrition policies
   - Scenario modeling
   - Cost-benefit analysis


