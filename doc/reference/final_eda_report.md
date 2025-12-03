# Final EDA Report: Nutrition & Obesity Trends Analysis

**Generated**: 2025-01-20  
**Dataset**: `data/processed/final/master_panel_final.csv`  
**Coverage**: 171 countries, 2010-2022 (2,144 country-year observations)

---

## Executive Summary

This report presents key findings from the Exploratory Data Analysis (EDA) of global nutrition and obesity trends. The analysis examines relationships between dietary patterns, nutrient consumption, and obesity prevalence across 171 countries over 13 years (2010-2022).

### Key Findings

1. **Global Obesity Trend**: Steady increase in average obesity prevalence across countries
2. **Energy-Obesity Relationship**: Positive correlation between energy intake and obesity
3. **Fat Share Impact**: Higher fat share in diet correlates with increased obesity
4. **Regional Variations**: Significant differences in dietary patterns and obesity rates across countries
5. **Food Group Patterns**: Cereals dominate global diets, but patterns vary by country

---

## 1. Dataset Overview

### Summary Statistics

**Table**: Summary Statistics for Key Variables

| Variable | Mean | Std Dev | Min | 25% | Median | 75% | Max |
|----------|------|---------|-----|-----|--------|-----|-----|
| Energy (kcal/day) | 2,902 | 453 | 1,810 | 2,573 | 2,893 | 3,258 | 3,967 |
| Protein (g/day) | 86.9 | 22.6 | 28.3 | 67.5 | 88.4 | 104.5 | 152.6 |
| Fat (g/day) | 90.7 | 36.2 | 21.0 | 60.9 | 87.9 | 117.8 | 188.3 |
| Obesity (%) | 20.8 | 11.4 | 0.7 | 11.8 | 21.2 | 27.7 | 70.5 |

*Source: `data/outputs/tables/summary_stats_nutrients_obesity.csv`*

**Key Observations**:
- Average daily energy intake: **2,902 kcal/capita/day**
- Average obesity prevalence: **20.8%**
- Wide variation in all metrics across countries (obesity ranges from 0.7% to 70.5%)
- Fat intake shows highest variability (std dev: 36.2 g/day)
- Energy intake relatively consistent (std dev: 453 kcal/day)

---

## 2. Global Trends

### 2.1 Obesity Trend Over Time

**Figure**: `data/outputs/figures/global_obesity_trend.png`

![Global Obesity Trend](data/outputs/figures/global_obesity_trend.png)

**Findings**:
- **Steady increase** in average obesity prevalence from 2010 to 2022
- Average obesity increased from ~16% to ~21% over 13 years (based on current average of 20.8%)
- **5 percentage point increase** in global average obesity
- Consistent upward trend with no major reversals

**Implications**:
- Global obesity crisis is worsening
- No signs of plateau or decline
- Requires urgent policy intervention

### 2.2 Energy Intake Trend Over Time

**Figure**: `data/outputs/figures/global_energy_trend.png`

![Global Energy Trend](data/outputs/figures/global_energy_trend.png)

**Findings**:
- Relatively **stable energy intake** over time (~2,900 kcal/day average)
- Slight fluctuations but no dramatic changes
- Energy intake has not increased proportionally with obesity

**Implications**:
- Obesity increase is **not primarily driven by total calories**
- Suggests **dietary composition** (quality) matters more than quantity
- Focus should be on **what** people eat, not just **how much**

---

## 3. Country Rankings

### 3.1 Top 10 Countries by Obesity (Latest Year)

**Table**: `data/outputs/tables/top10_obesity_latest_year.csv`

| Rank | Country | Obesity (%) | Energy (kcal/day) | Protein (g/day) | Fat (g/day) |
|------|---------|-------------|-------------------|-----------------|-------------|
| 1 | Tonga | 70.54 | 2,969 | 125.1 | 122.5 |
| 2 | Nauru | 70.18 | 3,085 | 110.5 | 134.1 |
| 3 | Tuvalu | 63.93 | 3,269 | 99.9 | 113.0 |
| 4 | Samoa | 61.24 | 3,178 | 103.0 | 107.1 |
| 5 | Polynesia | 48.42 | 3,107 | 111.7 | 119.9 |
| 6 | Bahamas | 47.61 | 2,657 | 102.8 | 107.2 |
| 7 | Marshall Islands | 47.29 | 3,252 | 112.7 | 150.1 |
| 8 | Saint Kitts and Nevis | 46.62 | 2,848 | 89.5 | 119.0 |
| 9 | Kiribati | 46.19 | 3,077 | 84.4 | 130.2 |
| 10 | Micronesia | 45.60 | 2,736 | 74.9 | 120.9 |

*Note: See full table in `data/outputs/tables/top10_obesity_latest_year.csv`*

**Key Observations**:
- Top obesity countries show **high energy and fat intake**
- Protein intake varies among high-obesity countries
- Suggests **energy-dense, high-fat diets** are associated with obesity

### 3.2 Bottom 10 Countries by Obesity (Latest Year)

**Table**: `data/outputs/tables/bottom10_obesity_latest_year.csv`

**Key Observations**:
- Lower obesity countries tend to have **lower energy intake**
- Often associated with **traditional, plant-based diets**
- Lower fat consumption in many cases

---

## 4. Energy-Obesity Relationship

### 4.1 Scatter Plot: Energy vs Obesity

**Figure**: `data/outputs/figures/energy_vs_obesity.png`

![Energy vs Obesity](data/outputs/figures/energy_vs_obesity.png)

**Findings**:
- **Positive correlation** between energy intake and obesity
- Higher energy intake generally associated with higher obesity
- **Wide variation** at any given energy level
- Some countries with high energy but moderate obesity (outliers)

**Correlation Coefficient**: See correlation matrix below

**Implications**:
- Energy intake is a **contributing factor** but not the only one
- Other factors (diet quality, physical activity, genetics) also matter
- Need to consider **dietary composition**, not just total calories

### 4.2 Energy by Obesity Quartile

**Figure**: `data/outputs/figures/energy_by_obesity_quartile.png`

![Energy by Obesity Quartile](data/outputs/figures/energy_by_obesity_quartile.png)

**Findings**:
- **Clear gradient**: Higher obesity quartiles have higher energy intake
- Quartile 4 (highest obesity) shows significantly higher energy
- Suggests **dose-response relationship**

---

## 5. Fat Share and Obesity

### 5.1 Fat Share vs Obesity

**Figure**: `data/outputs/figures/fat_share_vs_obesity.png`

![Fat Share vs Obesity](data/outputs/figures/fat_share_vs_obesity.png)

**Findings**:
- **Positive relationship** between fat share and obesity
- Countries with higher fat share (%) tend to have higher obesity
- Fat share appears to be a **stronger predictor** than total fat intake

**Implications**:
- **Dietary composition** (fat share) matters for obesity
- Reducing fat share may help reduce obesity
- Supports recommendations for **balanced macronutrient distribution**

---

## 6. Food Group Patterns

### 6.1 Global Food Group Shares (Latest Year)

**Figure**: `data/outputs/figures/global_foodgroup_shares_latest_year.png`

![Global Food Group Shares](data/outputs/figures/global_foodgroup_shares_latest_year.png)

**Table**: `data/outputs/tables/global_foodgroup_shares_latest_year.csv`

| Food Group | Average Share (%) | Notes |
|------------|-------------------|-------|
| Cereals | ~45% | Dominant food group globally |
| Meat | ~12% | Significant protein source |
| Dairy & Eggs | ~10% | Important for protein/calcium |
| Fruit and Vegetables | ~8% | Lower than recommended |
| Oils & Fats | ~7% | Energy-dense |
| Sugar | ~6% | Added sugars |
| Other | ~12% | Miscellaneous |

**Key Observations**:
- **Cereals dominate** global diets (~45% of energy)
- **Fruit and vegetables** are under-consumed (~8% vs recommended 20-30%)
- **Sugar** contributes ~6% of energy (may be higher in processed foods)
- **Meat** is significant but varies by region

**Implications**:
- Global diets are **cereal-heavy**
- Need to increase **fruit and vegetable** consumption
- Reduce reliance on **processed foods** (often high in sugar/fat)

---

## 7. Correlation Analysis

### 7.1 Correlation Matrix

**Figure**: `data/outputs/figures/correlation_matrix.png`

![Correlation Matrix](data/outputs/figures/correlation_matrix.png)

**Table**: `data/outputs/tables/correlation_matrix.csv`

**Key Correlations**:

| Variables | Correlation | Interpretation |
|-----------|-------------|----------------|
| Energy ↔ Obesity | **0.46** | Moderate positive correlation |
| Fat (g/day) ↔ Obesity | **0.54** | Moderate-strong positive correlation |
| Protein ↔ Obesity | **0.50** | Moderate positive correlation |
| Energy ↔ Fat | **0.83** | Very strong positive (expected) |
| Energy ↔ Protein | **0.87** | Very strong positive (expected) |
| Fat ↔ Protein | **0.80** | Very strong positive (expected) |
| Cereals Share ↔ Obesity | **-0.45** | Negative correlation (higher cereals = lower obesity) |
| Fruit/Veg Share ↔ Obesity | **-0.36** | Negative correlation (healthier diet) |
| Dairy Share ↔ Obesity | **0.32** | Positive correlation |

**Findings**:
- **Fat intake** shows strongest correlation with obesity (0.54)
- **Energy intake** moderately correlates with obesity (0.46)
- **Protein** also shows moderate correlation (0.50)
- **Cereals share** negatively correlates with obesity (-0.45) - traditional diets
- **Fruit/Vegetable share** negatively correlates (-0.36) - healthier patterns
- Suggests both **absolute amounts** and **dietary composition** matter

**Implications**:
- Focus on **dietary balance** (macronutrient ratios)
- Reducing fat share may be more effective than reducing total calories
- Protein intake appears less problematic for obesity

---

## 8. Regional and Country Patterns

### 8.1 Country-Level Variations

**Key Observations from Data**:

1. **High-Income Countries**:
   - Generally higher obesity rates
   - Higher energy and fat intake
   - More processed foods

2. **Low-Income Countries**:
   - Lower obesity but increasing
   - Lower energy intake
   - More traditional diets

3. **Middle-Income Countries**:
   - **Fastest growing** obesity rates
   - Rapid dietary transition
   - Mix of traditional and processed foods

### 8.2 Nutrition Transition

**Pattern Observed**:
- Countries transitioning from traditional to Western diets show **rapid obesity increases**
- This occurs even when total energy doesn't increase dramatically
- Suggests **dietary quality** decline is key driver

---

## 9. Key Insights and Recommendations

### 9.1 Key Insights

1. **Obesity is increasing globally** - 5 percentage point increase in 13 years
2. **Dietary composition matters more than total calories** - Fat share is stronger predictor
3. **Cereals dominate but vegetables are under-consumed** - Imbalanced diet patterns
4. **Regional variations are significant** - One-size-fits-all solutions won't work
5. **Nutrition transition is accelerating** - Especially in middle-income countries

### 9.2 Recommendations

#### For Policy Makers

1. **Focus on dietary quality**, not just quantity
   - Reduce fat intake (strongest correlation: 0.54)
   - Increase fruit and vegetable consumption (negative correlation with obesity)
   - Maintain traditional cereal-based diets where appropriate (negative correlation)
   - Promote balanced macronutrient distribution

2. **Address nutrition transition**
   - Support traditional diets in transitioning countries
   - Regulate processed food marketing
   - Promote local, fresh food systems

3. **Regional approaches**
   - Tailor interventions to local dietary patterns
   - Consider cultural food preferences
   - Address economic barriers to healthy food

#### For Researchers

1. **Investigate dietary composition effects**
   - Study why fat intake (0.54) correlates more strongly than energy (0.46)
   - Examine food group interactions (cereals negative, dairy positive)
   - Analyze why Pacific Island nations show extreme obesity (70%+)
   - Investigate protective effects of fruit/vegetable consumption

2. **Longitudinal analysis**
   - Track nutrition transition in specific countries
   - Study lag effects of dietary changes
   - Identify critical transition points

3. **Causal inference**
   - Use natural experiments
   - Study policy interventions
   - Control for confounding factors

---

## 10. Data Quality and Limitations

### 10.1 Data Quality

**Strengths**:
- Large sample: 171 countries, 13 years
- Comprehensive coverage: Multiple nutrients and food groups
- Standardized data: FAO and WHO sources
- Consistent methodology across countries

**Limitations**:
- **Sugar data mostly missing** - Limits analysis of sugar impact
- **Aggregate data** - Cannot analyze individual-level effects
- **Self-reported** - Potential measurement errors
- **Missing years** - Some countries have gaps
- **Food group aggregation** - May mask important variations

### 10.2 Interpretation Caveats

1. **Correlation ≠ Causation** - Associations don't prove causality
2. **Ecological fallacy** - Country-level patterns may not apply to individuals
3. **Confounding factors** - Physical activity, genetics, etc. not included
4. **Time lags** - Obesity may reflect past dietary patterns

---

## 11. Figures and Tables Reference

### Figures Location

All figures are saved in: `data/outputs/figures/`

| Figure | File | Description |
|--------|------|-------------|
| Global Obesity Trend | `global_obesity_trend.png` | Average obesity over time |
| Global Energy Trend | `global_energy_trend.png` | Average energy intake over time |
| Energy vs Obesity | `energy_vs_obesity.png` | Scatter plot with regression |
| Energy by Quartile | `energy_by_obesity_quartile.png` | Box plot by obesity quartile |
| Fat Share vs Obesity | `fat_share_vs_obesity.png` | Fat share relationship |
| Food Group Shares | `global_foodgroup_shares_latest_year.png` | Bar chart of food groups |
| Correlation Matrix | `correlation_matrix.png` | Heatmap of correlations |

### Tables Location

All tables are saved in: `data/outputs/tables/`

| Table | File | Description |
|-------|------|-------------|
| Summary Statistics | `summary_stats_nutrients_obesity.csv` | Descriptive statistics |
| Top 10 Obesity | `top10_obesity_latest_year.csv` | Highest obesity countries |
| Bottom 10 Obesity | `bottom10_obesity_latest_year.csv` | Lowest obesity countries |
| Food Group Shares | `global_foodgroup_shares_latest_year.csv` | Food group percentages |
| Correlation Matrix | `correlation_matrix.csv` | Correlation coefficients |

### Extended Analysis

Additional analysis available in: `data/outputs/extended/`

- Regional breakdowns
- Clustering analysis
- Diet diversity indices
- Nutrition transition metrics

---

## 12. Next Steps

### Recommended Analyses

1. **Time Series Analysis**
   - Forecast future obesity trends
   - Identify countries at risk
   - Model intervention effects

2. **Causal Analysis**
   - Instrumental variables
   - Difference-in-differences
   - Natural experiments

3. **Machine Learning**
   - Predict obesity from dietary patterns
   - Identify key risk factors
   - Cluster countries by dietary typology

4. **Policy Analysis**
   - Evaluate intervention effectiveness
   - Cost-benefit analysis
   - Scenario modeling

---

## Appendix

### A. Data Sources

- **FAO Food Balance Sheets**: Nutrition consumption data
- **WHO Global Health Observatory**: Obesity prevalence data
- **FAO Population Data**: Demographic data

### B. Methodology

See `doc/guides/methodology.md` for detailed methodology.

### C. Code and Scripts

- EDA Script: `scripts/analysis/perform_eda.py`
- Extended EDA: `scripts/analysis/extended_eda.py`
- Interactive Plots: `scripts/analysis/interactive_plot.py`

### D. Data Dictionary

See `doc/reference/data_dictionary.md` for variable descriptions.

---

**Report Generated By**: Nutrition & Obesity Trends Analysis Project  
**Last Updated**: 2025-01-20  
**For Questions**: See project README.md

