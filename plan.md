# Project Plan

**Author:** Muhammad Ali Ghanchi

---

## Project Title

FloodCast Venice — Sea Level Rise Predictor

---

## Project Goal

Develop a Python-based, multi-page Streamlit web application that analyses historical tide gauge data from Venice, combines it with global climate indicators, and applies statistical and machine learning models to estimate future relative sea level. The application compares model-based projections with NASA/IPCC published scenarios and RCP climate pathways, and provides decision-support outputs for planners, civil protection agencies, and the general public.

---

## Development Phases

### Phase 1 — Setup and Data Acquisition (Completed)

- Set up Python virtual environment
- Initialized Git repository and connected to GitLab (Prof. Miunske's organization)
- Downloaded all datasets:
  - Venice tide gauge data (PSMSL, 1909–2000)
  - Global temperature anomalies (NASA GISTEMP)
  - Atmospheric CO2 (Mauna Loa)
  - Global Mean Sea Level (NASA satellite altimetry)
  - RCP scenario projections (Zenodo)
  - NASA/IPCC local sea-level projections for Venice (IPCC AR6)
- Created project folder structure: `src/`, `data/`, `assets/`, `.streamlit/`
- Created documentation files: `README.md`, `brainstorm.md`, `plan.md`, `alignment.md`

---

### Phase 2 — Data Processing (Completed)

- Removed missing values (-99999) from tide gauge data
- Converted sea level from millimetres to centimetres
- Loaded and cleaned temperature anomaly and CO2 datasets
- Merged Venice sea level, temperature, and CO2 by year into a single modelling dataset
- Loaded and processed NASA/IPCC projection Excel file (Total sheet, wide-to-long reshape, metres to centimetres, alignment to Venice 2020 baseline)
- Loaded RCP scenario data and converted to centimetres above year 2000 baseline

---

### Phase 3 — Model Development (Completed)

#### Historical Linear Regression
- Feature: `year`
- Target: `sea_level_cm`
- Chronological 80/20 train/test split for evaluation
- Evaluated using Pearson R, MAE, RMSE on held-out test period
- 95% prediction interval derived analytically from residual standard error
- Extrapolated predictions to 2100
- Compared against NASA/IPCC local projections on the same graph

#### Climate-Driven Regression
- Features: `year`, `temp_anomaly`, `co2_ppm`
- Feature scaling via StandardScaler
- Ridge regression with GridSearchCV hyperparameter tuning (alphas: 0.01, 0.1, 1.0, 10.0, 100.0)
- 5-fold cross-validation on training set
- Chronological 80/20 split for evaluation
- Evaluated using R², MAE, RMSE on held-out test period
- Future temperature and CO2 extrapolated linearly then fed into climate model to 2100
- Approximate prediction interval from residual variance

---

### Phase 4 — Visualization (Completed)

All charts built with Plotly:
- Historical data with regression trend and prediction interval
- Climate-driven forecast with uncertainty band
- RCP scenario comparison dashboard with threshold-crossing table
- Global vs local sea-level anomaly comparison
- Local amplification signal (Venice minus global mean)
- WorldTides short-term live tide forecast

---

### Phase 5 — Streamlit Application (Completed)

Multi-page application running via `streamlit run src/app.py`:

| Page | Content |
|---|---|
| Home | KPI cards, navigation cards, Venice images |
| Historical Analysis | Linear regression, prediction interval, NASA comparison, residual plot, CSV export |
| Climate-Driven Model | Ridge regression, hyperparameter tuning results, forecast, residuals, CSV export |
| Comparison Dashboard | RCP scenario overlay, threshold-crossing slider and table |
| Free Forecast | Historical linear forecast vs NASA projections, WorldTides live tide API |
| Global vs Local | Venice vs GMSL anomaly, local amplification signal |
| Resources | Download buttons for all datasets |

---

### Phase 6 — Documentation and Submission (Completed)

- README.md completed with setup instructions, usage, and data source descriptions
- requirements.txt updated with all dependencies
- GitLab repository maintained with consistent commit history throughout development
- Presentation slides prepared covering all five required topics

---

## Timeline Summary

| Phase | Status |
|---|---|
| Phase 1 — Setup and Data Acquisition | Done |
| Phase 2 — Data Processing | Done |
| Phase 3 — Model Development | Done |
| Phase 4 — Visualization | Done |
| Phase 5 — Streamlit Application | Done |
| Phase 6 — Documentation and Submission | Done |

---

## Technologies Used

Python, pandas, NumPy, scikit-learn, Plotly, Streamlit, openpyxl, requests, Git/GitLab
