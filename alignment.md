# Alignment

## Author
- Muhammad Ali Ghanchi

## Purpose
This document verifies that the *FloodCast Venice – Water you thinking?* project meets the requirements outlined in the **Application Programming (AP)** examination conditions.

---

## Requirement Checklist

### 1. Definition of the Application & Business Idea ✅

- **Application:**  
  *FloodCast Venice* — an interactive web dashboard for analysing and predicting **relative sea level** in Venice and comparing it with climate scenarios.

- **Problem solved:**  
  Urban planners, civil protection agencies, and local authorities need an intuitive way to understand **how fast relative sea level is rising in Venice**, **how much subsidence amplifies global sea-level rise**, and **when critical flood thresholds may be reached** under different assumptions.

- **Business / decision-support value:**  
  - Supports **proactive infrastructure planning** (e.g. MOSE barrier operation, sea walls, drainage, street elevation).  
  - Helps **civil protection** assess **timelines** for increasing flood risk.  
  - Can inform **policy and investment decisions** by illustrating the difference between historical trends and high-end climate scenarios.  
  - Provides a clear, visual communication tool for stakeholders and public awareness.

- **Target users:**  
  - Government authorities & city planners  
  - Civil protection and emergency services  
  - Engineers and infrastructure planners  
  - Secondary: students, researchers, and interested citizens

---

### 2. Data Foundation ✅

The project uses **real, open-source datasets** from established scientific institutions:

- **Historical tide gauge data (Venice):**  
  - Long-term relative sea level measurements at Venice (tide gauge record).  
  - Includes both **global sea-level rise** and **local land subsidence**.

- **Global temperature anomalies (NASA GISTEMP):**  
  - Annual global mean surface temperature anomaly, used as a climate indicator.

- **Atmospheric CO₂ (NOAA Mauna Loa):**  
  - Annual mean CO₂ concentration (ppm), representing the main driver of long-term warming.

- **Global Mean Sea Level (NASA satellite altimetry):**  
  - Global mean sea level anomaly from satellite observations, used to compare **global** vs **local** changes.

- **Sea-level scenario / RCP data for Venice (Excel):**  
  - Scenario curves corresponding to **RCP 2.6**, **RCP 8.5 (median)** and a **high-end** scenario, given in metres.  
  - Converted to centimetres and aligned to the Venice baseline around year 2000.

- **No synthetic training data used:**  
  All model training is done on **real measurements**. Synthetic / extrapolated values are used **only for prediction** (future inputs), not for training.

- **Engineering relevance:**  
  These datasets are directly used in **coastal engineering**, **climate impact assessment**, and **flood risk** studies, making them well aligned with engineering practice.

---

### 3. Data Processing and AI Implementation ✅

- **Data processing & cleaning:**
  - Removal of missing values (e.g. `-99999` in the tide gauge dataset).
  - Unit conversion from **mm to cm** for sea level.
  - Selection and type conversion of relevant columns for temperature and CO₂.
  - Aggregation of high-frequency GMSL data into **annual means**.
  - Conversion of scenario values from **metres to centimetres**.
  - Baseline alignment of scenario data to the modelled Venice sea level around the year 2000.

- **Merged modelling dataset:**
  - A combined table with columns:  
    `year`, `sea_level_cm (Venice)`, `temp_anomaly`, `co2_ppm`.

- **AI / Machine Learning components (scikit-learn):**
  1. **Historical Linear Regression**
     - Input: `year`  
     - Target: `relative sea level in Venice (cm)`  
     - Output: historical trend and extrapolated linear projection to 2100.  
     - A statistically consistent **95 % prediction interval** is constructed using regression residuals.

  2. **Climate-Driven Multivariate Regression**
     - Inputs: `year`, `temp_anomaly`, `co2_ppm`  
     - Target: `relative sea level in Venice (cm)`  
     - Evaluation: **MAE** and **RMSE** computed on historical data; **residual plot** used to inspect model behaviour over time.  
     - Simple linear trends for temperature and CO₂ are fitted and extrapolated to 2100.  
     - The trained climate-driven model is applied to these extrapolated climate inputs to generate future predictions.  
     - A **prediction interval** for future relative sea level is derived using the linear regression covariance structure and residual variance.

- **Scenario comparison & threshold analysis:**
  - The climate-driven prediction is compared to RCP-based scenarios (RCP 2.6, RCP 8.5 median, high-end).  
  - A **slider** lets users choose a critical threshold (cm above year 2000 level).  
  - For each scenario and for the climate-driven prediction, the dashboard computes the **first year** when this threshold is exceeded.

This demonstrates a correct application of regression-based AI methods within a Python application, including **uncertainty quantification** and **model evaluation**.

---

### 4. Digital Implementation and Deployment ✅

- Implemented as a **multi-page Streamlit web application** in Python.
- Pages include:
  - Home / Overview (KPI cards, navigation, images, optional fundraiser link)
  - Historical Analysis
  - Climate-Driven Model
  - Comparison Dashboard
  - Global vs Local Sea Level
  - Resources (data download)
- Uses Plotly for interactive visualisations.
- Configured via `.streamlit/config.toml` for a consistent UI theme.
- Runs locally via:

  ```bash
  streamlit run src/app.py