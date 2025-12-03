# Documentation

Organized documentation for the Nutrition & Obesity Trends Analysis project.

## 📁 Folder Structure

```
doc/
├── README.md              # This file
│
├── guides/                # How-to guides and methodology
│   └── methodology.md    # Detailed methodology and pipeline
│
├── reference/             # Reference documentation
│   ├── data_dictionary.md      # Variable descriptions
│   ├── data_analysis.md        # Dataset analysis report
│   └── dataset_analysis.md     # Alternative dataset analysis
│
└── notes/                 # Research notes and findings
    └── research_notes.md  # Research findings and literature review
```

## 📚 Documentation Files

### Guides

#### `guides/methodology.md`
- **Purpose**: Detailed methodology for the analysis
- **Contents**:
  - Data sources and collection
  - Data processing pipeline
  - Cleaning and transformation steps
  - Analysis approach
- **Use when**: Understanding how the project works

### Reference

#### `reference/data_dictionary.md`
- **Purpose**: Variable descriptions and data structure
- **Contents**:
  - Variable names and types
  - Units and descriptions
  - Data sources
  - Final dataset structure
- **Use when**: Working with the data, understanding variables

#### `reference/data_analysis.md`
- **Purpose**: Dataset analysis and integration report
- **Contents**:
  - Raw dataset descriptions
  - Data structure analysis
  - Integration process
  - Coverage statistics
- **Use when**: Understanding raw data structure

#### `reference/dataset_analysis.md`
- **Purpose**: Alternative dataset analysis
- **Contents**: Similar to data_analysis.md but with different focus
- **Use when**: Need additional dataset insights

#### `reference/final_eda_report.md` ⭐
- **Purpose**: Comprehensive EDA report with findings, figures, and tables
- **Contents**:
  - Executive summary and key findings
  - Global trends analysis
  - Country rankings
  - Correlation analysis
  - Food group patterns
  - Insights and recommendations
  - References to all figures and tables
- **Use when**: Understanding EDA results, preparing presentations, writing papers

### Notes

#### `notes/research_notes.md`
- **Purpose**: Research findings and literature review
- **Contents**:
  - Global obesity trends
  - Nutrition transition patterns
  - Research findings
  - Key insights
- **Use when**: Understanding research context and findings

## 🔄 Documentation Status

### ✅ Updated
- File paths updated to reflect new folder structure
- References to `master_panel_final.csv` instead of old `integrated_nutrition_data.csv`
- Pipeline references updated to `run_pipeline.py`

### ⚠️ May Need Updates
- Some methodology details may reference old script locations
- Check file paths in methodology.md match current structure

## 📝 Quick Reference

**Main Dataset**: `data/processed/final/master_panel_final.csv`

**Pipeline**: `run_pipeline.py`

**Scripts Location**:
- Preprocessing: `scripts/preprocessing/`
- Panels: `scripts/panels/`
- Analysis: `scripts/analysis/`

**Processed Data**:
- Cleaned: `data/processed/cleaned/`
- Mappings: `data/processed/mappings/`
- Panels: `data/processed/panels/`
- Final: `data/processed/final/`

## 🔍 Finding Information

- **How does the pipeline work?** → `guides/methodology.md`
- **What do the variables mean?** → `reference/data_dictionary.md`
- **What's in the raw data?** → `reference/data_analysis.md`
- **What are the research findings?** → `notes/research_notes.md`

---

**For project overview**: See main `README.md`  
**For quick start**: See `QUICK_START.md`  
**For data structure**: See `data/processed/README.md`

