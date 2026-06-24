# FloodCast Venice — Sea Level Rise Predictor

**Author:** Muhammad Ali Ghanchi

---

# Project Goal

Develop a Python-based, multi-page Streamlit web application that analyses historical tide gauge data from Venice, combines it with global climate indicators such as temperature anomalies and atmospheric CO₂, and applies statistical and machine learning models to estimate future relative sea level.

The application also compares these model-based projections with external scenario-based projections, including NASA/IPCC local sea-level projections for Venice, and provides decision-support outputs for planners, civil protection agencies, researchers, and the wider public.

---

# Development Phases

## Phase 1 — Setup & Data Acquisition

### Tasks
- Set up Python virtual environment.
- Initialize Git repository and connect to GitLab.
- Download historical tide gauge data for Venice.
- Download global temperature anomaly data.
- Download atmospheric CO₂ data.
- Download global mean sea level data.
- Download scenario comparison data for Venice.
- Download NASA/IPCC local sea-level projection data.
- Create project folder structure:
  - `src/`
  - `data/`
  - `assets/`
  - `.streamlit/`

---

## Phase 2 — Data Processing

### Historical Tide Gauge Data
- Remove missing values (`-99999`).
- Convert sea level values from millimetres to centimetres.

### Climate Data
- Load temperature anomaly data.
- Load atmospheric CO₂ data.
- Select relevant columns.
- Convert values to numeric.
- Remove invalid entries.

### Global Mean Sea Level
- Load and process global sea-level data.
- Prepare for comparison with Venice observations.

### Scenario Data
- Load and process scenario comparison datasets.

### NASA/IPCC Local Projections
- Load data from the `Total` sheet.
- Identify year columns.
- Reshape data from wide to long format.
- Convert values from metres to centimetres.
- Align projections to the Venice baseline around 2020.

### Dataset Construction
- Merge Venice sea level, temperature anomalies, and CO₂ by year.
- Create the final modelling dataset.

---

## Phase 3 — Model Development

### Historical Linear Regression

- Train a linear regression model:
  - `year → relative sea level (cm)`
- Perform chronological train/test split.
- Evaluate using:
  - Pearson R
  - MAE
  - RMSE
- Estimate a 95% prediction interval.
- Extrapolate predictions to January 2100.

---

### Climate-Driven Regression

Predictors:

- `year`
- `temp_anomaly`
- `co2_ppm`

Methods:

- Feature scaling
- Ridge regression
- GridSearchCV hyperparameter tuning

Evaluation:

- Train/test performance
- MAE
- RMSE
- R²

Forecasting:

- Extrapolate climate variables to 2100.
- Predict future sea level.
- Construct prediction intervals.

---

### SARIMAX Forecasting

- Train a SARIMAX model on annual sea-level observations.
- Use chronological train/test evaluation.
- Calculate:
  - Pearson R
  - MAE
  - RMSE
- Refit using the full dataset.
- Forecast to January 2100.
- Compare forecasts with NASA local projections.

---

### Scenario Comparison

- Compare:
  - Historical regression forecasts
  - Climate-driven forecasts
  - SARIMAX forecasts
  - NASA/IPCC scenario projections

Features:

- Interactive scenario comparisons.
- Future exceedance analysis.
- Scenario-based visualizations.

---

## Phase 4 — Visualization

Interactive visualizations created using Plotly:

- Historical Venice tide gauge data.
- Historical regression trend and projection.
- Climate-driven forecast with uncertainty.
- SARIMAX forecast with uncertainty.
- Forecast versus NASA scenario projections.
- Global versus local sea-level comparisons.

### Visualization Requirements

- Clear labels and units.
- Consistent colours and legends.
- Hover tooltips.
- Unified x-axis interactions.

---

## Phase 5 — Streamlit Application

### Pages

- Home / Overview
- Historical Analysis
- Climate-Driven Model
- Comparison Dashboard
- Global vs Local Sea Level
- Free Forecast
- Resources

### Features

- Navigation cards using `st.page_link`.
- Downloadable datasets.
- NASA/IPCC projection downloads.
- Global Streamlit theme configuration.

Run locally using:

```bash
streamlit run src/app.py
```

---

## Phase 6 — Documentation & Submission

### Documentation

Complete:

- `README.md`
- Setup instructions
- Usage instructions
- Data source descriptions

### Repository Requirements

- Clean and readable Python code.
- Source datasets.
- Streamlit configuration.
- Updated `requirements.txt`.

### Final Deliverables

- GitLab repository.
- Presentation slides covering:
  - Business case
  - System architecture
  - Implementation
  - Results
  - Evaluation
  - Application screenshots

---

# Expected Outcome

A fully functional Streamlit application that:

- Visualizes historical relative sea level in Venice.
- Provides a historical linear regression forecast to 2100.
- Provides a climate-driven regression forecast using temperature and CO₂.
- Provides a SARIMAX time-series forecast.
- Displays prediction intervals for future projections.
- Compares forecasts with NASA/IPCC scenario projections.
- Highlights differences between global and local sea-level change.
- Allows users to download datasets for transparency and further analysis.

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Statsmodels
- Plotly
- Streamlit
- Git / GitLab

---

# Target Users

- Government authorities
- Urban planners
- Civil protection agencies
- Researchers
- Students
- General public

---