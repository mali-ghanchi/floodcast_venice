# Project Plan

## Author

Muhammad Ali Ghanchi  

## Project Title

FloodCast Venice — Sea Level Rise Predictor

## Project Goal

Develop a Python-based, multi-page Streamlit web application that analyses historical tide gauge data from Venice, combines it with global climate indicators (temperature anomalies, atmospheric CO₂, global mean sea level), and applies regression models to estimate future relative sea level. The app compares these statistical projections with established climate scenarios (RCP-based) and provides decision-support outputs such as threshold exceedance years for planners and civil protection agencies.

---

## Development Phases

### Phase 1 — Setup & Data Acquisition

- Set up Python virtual environment.
- Initialize Git repository and connect to GitLab.
- Download **historical tide gauge data** for Venice (PSMSL).
- Download **global temperature anomaly** data (NASA GISTEMP).
- Download **atmospheric CO₂** data (NOAA Mauna Loa).
- Download **global mean sea level** data (NASA satellite altimetry).
- Download **sea-level scenario / RCP data** for Venice (Excel).
- Create project folder structure:  
  `src/`, `data/`, `assets/`, `.streamlit/`.

### Phase 2 — Data Processing

- Load and clean historical tide gauge data:
  - remove `-99999` missing values,
  - convert sea level from millimetres to centimetres.
- Load and prepare global temperature anomaly and CO₂ data:
  - select relevant columns, convert to numeric, drop invalid entries.
- Aggregate high-frequency GMSL data into **annual means**.
- Load and process scenario / RCP data from Excel:
  - select relevant columns,
  - convert values from metres to centimetres,
  - align scenario levels with a **baseline around the year 2000**.
- Merge Venice sea level with temperature and CO₂ by calendar year to form the core modelling dataset.

### Phase 3 — Model Development

- **Historical linear regression:**
  - Train a simple linear regression model using `year → relative sea level (cm)`.
  - Compute residuals and derive a **95 % prediction interval** for future years based on regression theory.
- **Climate-driven regression:**
  - Train a multivariate linear regression using  
    `year`, `temp_anomaly`, `co2_ppm → relative sea level (cm)`.
  - Evaluate model fit using **MAE** and **RMSE**.
  - Analyse residuals over time to assess model performance.
  - Fit separate linear trends for temperature and CO₂ over time and **extrapolate** them to 2100.
  - Use the trained climate-driven model to predict future relative sea level from extrapolated climate variables.
  - Construct a statistically consistent **prediction interval** for these future predictions.
- **Scenario comparison:**
  - Express RCP-based sea-level scenarios in centimetres relative to the same baseline as the regression model.
  - Implement logic to compute **first year of threshold exceedance** for each scenario and the climate-driven prediction.

### Phase 4 — Visualization

- Use **Plotly** to create interactive time series plots for:
  - historical Venice tide gauge data,
  - historical regression trend and future projection with prediction interval,
  - climate-driven prediction with uncertainty,
  - comparison of climate-driven prediction with RCP scenarios,
  - global vs local sea level (Venice anomalies vs global mean sea level anomalies and their difference).
- Ensure all plots:
  - have clear labels and units (relative sea level in cm),
  - use consistent colours and legends,
  - support hover tooltips and unified x-axis interaction.

### Phase 5 — Web Application (Streamlit)

- Build a **multi-page** Streamlit application with:
  - **Home / Overview** page (title, description, KPI cards, navigation, images, optional fundraiser link),
  - **Historical Analysis** (purely time-based regression and prediction interval),
  - **Climate-Driven Model** (multivariate regression with temperature and CO₂, metrics, residual analysis),
  - **Comparison Dashboard** (climate-driven vs RCP scenarios + threshold slider and results table),
  - **Global vs Local Sea Level** (Venice vs global mean sea level, local amplification / subsidence),
  - **Resources** section for data download (CSV exports of the main datasets).
- Add navigation cards on the home page that link to all analysis pages using `st.page_link`.
- Configure a global Streamlit theme via `.streamlit/config.toml`.
- Ensure the app runs locally via `streamlit run src/app.py`.

### Phase 6 — Documentation & Submission

- Complete `README.md` with:
  - project description (problem, use case, expected outcome),
  - setup and usage instructions,
  - short description of data sources.
- Update `requirements.txt` with all dependencies:
  - `streamlit`, `pandas`, `numpy`, `scikit-learn`, `plotly`, `openpyxl` (or equivalent).
- Ensure the repository contains:
  - clean and readable Python code,
  - data folder with input files (or instructions to obtain them),
  - `.streamlit/config.toml` for theme configuration.
- Final GitLab push with clear commit history.
- Prepare the required 5-slide presentation covering:
  - business case & added value,
  - architecture & methodology,
  - technical implementation,
  - results & evaluation,
  - goal achievement & app screenshots.

---

## Expected Outcome

A fully functional, web-based Python application that:

- Visualizes Venice **relative sea level** trends from the early 20th century up to 2100.
- Provides both a **historical linear trend** and a **climate-driven regression** using global temperature and CO₂.
- Shows statistically derived **prediction intervals** to communicate uncertainty.
- Compares regression-based projections with **RCP-based sea-level scenarios**, including a threshold analysis that identifies when critical sea-level increases are reached in each scenario.
- Highlights the difference between **global mean sea level rise and local relative sea level in Venice**, underlining the role of land subsidence and local amplification.
- Offers simple **download options** for the underlying datasets, supporting transparency and further analysis by planners, researchers, or students.