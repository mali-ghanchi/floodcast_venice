# Alignment

**Author:** Muhammad Ali Ghanchi

---

## Purpose

This document verifies that FloodCast Venice meets all requirements in the AP Examination Requirements by Prof. Dr.-Ing. Tobias Miunske.

---

## 1. Definition of the Application and Business Idea

**Application:** FloodCast Venice — a multi-page Streamlit web dashboard for analysing and forecasting relative sea level rise in Venice.

**Problem solved:** Urban planners and civil protection agencies lack a simple, accessible tool to visualise when Venice's flooding thresholds will be crossed under different climate scenarios. Existing tools are either too technical or too expensive for smaller municipalities.

**Business model:**
- Free tier (general public, tourists, researchers): historical data viewer, basic trend graph
- Premium tier (government authorities, urban planners, civil protection agencies): full scenario comparison, RCP overlays, threshold-crossing tool, data export, future projections
- Revenue via B2G (Business to Government) annual SaaS licensing
- Scalable beyond Venice — same architecture redeployable for any coastal city with PSMSL tide gauge data

**Technical functionality:** Users interact with an interactive dashboard, select flooding thresholds via sliders, compare multiple forecast models and climate scenarios, and download datasets for further analysis.

---

## 2. Data Foundation

All datasets are real, open-source, and from established scientific institutions. No synthetic data was used at any stage.

| Dataset | Source | Used for |
|---|---|---|
| Venice tide gauge (1909–2000) | PSMSL | Primary historical record; all model training |
| Global temperature anomalies | NASA GISTEMP | Climate-driven regression feature |
| Atmospheric CO2 | Mauna Loa Observatory | Climate-driven regression feature |
| Global Mean Sea Level | NASA satellite altimetry | Global vs Local comparison page |
| RCP scenario projections | Zenodo (peer-reviewed) | Comparison dashboard |
| NASA/IPCC local projections for Venice | IPCC AR6 | Historical analysis comparison |

All datasets were processed from raw form — no pre-cleaned or synthetic versions were used.

---

## 3. Data Processing and AI Implementation

### Data preprocessing steps implemented
- Removal of missing values (-99999 notation) from tide gauge data
- Unit conversion: sea level from millimetres to centimetres
- Numeric type conversion and invalid entry removal for climate datasets
- Inner-join merging of Venice, temperature, and CO2 datasets by year
- Reshaping of NASA/IPCC Excel projection data from wide to long format
- Conversion of NASA projections from metres to centimetres
- Alignment of NASA projections to Venice tide gauge baseline at year 2020

### Models implemented

**Historical linear regression (scikit-learn LinearRegression)**
- Feature: `year`
- Chronological 80/20 train/test split for evaluation
- Metrics: Pearson R, MAE, RMSE on held-out test period
- 95% prediction interval derived analytically: `s * sqrt(1 + 1/n + (x0 - x_mean)^2 / Sxx)`
- Extrapolated to 2100 and compared against NASA/IPCC local projections

**Climate-driven regression (scikit-learn Ridge + Pipeline + GridSearchCV)**
- Features: `year`, `temp_anomaly`, `co2_ppm`
- Feature scaling via StandardScaler
- Hyperparameter tuning: alpha tested across [0.01, 0.1, 1.0, 10.0, 100.0] using 5-fold cross-validation on the training set
- Chronological 80/20 split for evaluation
- Metrics: R², MAE, RMSE on held-out test period
- Approximate prediction interval from residual variance using matrix form
- Future temperature and CO2 extrapolated linearly, then fed into climate model to 2100

### AI methods correctly applied and understood
- Model selection justified: linear and Ridge regression appropriate for long-term trend forecasting on environmental time series data
- Limitations identified and documented: non-stationarity detected via chronological testing; widening uncertainty bands added as a direct response
- Hyperparameter tuning performed and confirmed empirically to have minimal impact on the simple model (single feature, no multicollinearity to regularize), but a genuine candidate for the climate model (three correlated features)
- Residual analysis performed for both models to check for systematic patterns

---

## 4. Digital Implementation and Deployment

**Framework:** Streamlit multi-page web application

**Visualization:** Plotly interactive charts with hover tooltips, unified x-axis, and legend toggles

**Application pages:**

| Page | Key features |
|---|---|
| Home | KPI cards, navigation cards, Venice images |
| Historical Analysis | Linear regression, NASA comparison, residual plot, CSV export |
| Climate-Driven Model | Ridge regression, tuning results, forecast, residuals, CSV export |
| Comparison Dashboard | RCP scenario overlay, threshold-crossing slider and table |
| Free Forecast | Linear forecast vs NASA projections, WorldTides live API |
| Global vs Local | Venice vs GMSL anomaly, local amplification signal |
| Resources | Download buttons for all six datasets |

**Live API integration:** WorldTides API used on the Free Forecast page to display short-term actual tide heights for Venice — demonstrating real-time data integration alongside long-term model projections.

**Deployment:** Runs locally via `streamlit run src/app.py`

**Executability:** Application is fully executable and demonstrable on request

---

## 5. GitLab and Presentation Slides

- Repository hosted in Prof. Miunske's GitLab organization from the start of development
- Regular commits throughout all development phases with descriptive commit messages
- Documentation files committed alongside code: README.md, brainstorm.md, plan.md, alignment.md
- Presentation: 5 required slides covering Business Case, Architecture and Methodology, Technical Implementation, Results and Evaluation, Goal Achievement

---

## Summary

All four mandatory project components are fully addressed. The project uses exclusively real data, applies correctly implemented and evaluated AI/ML methods, delivers a working multi-page Python web application with live API integration, and is fully version-controlled and documented on GitLab.
