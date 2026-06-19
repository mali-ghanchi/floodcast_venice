# Brainstorm

## Author
- Muhammad Ali Ghanchi

## Initial Idea Generation

When first approaching this project, several application ideas were considered:

- **Spare Parts Demand Forecaster** — predicting factory spare part needs to reduce downtime and inventory costs.
- **Supply Chain Delay Risk Analyzer** — flagging high-risk shipments *before* they are sent.
- **Stock Price Trend Predictor** — forecasting market trends using historical data.
- **Job Market Analyzer** — analysing engineering job market trends.
- **Venice Sea Level Rise Predictor** — analysing and predicting sea level rise in Venice using historical tide gauge and climate data.

## Why Venice Sea Level Rise?

After evaluating all options, the **Venice Sea Level Rise Predictor** was selected for the following reasons:

- **Real-world relevance**  
  Venice is one of the most documented and vulnerable cities globally when it comes to sea level rise, tidal flooding and land subsidence. Flooding is already an everyday problem, not a distant scenario.

- **Data availability**  
  High-quality, open historical and climate data are freely available:
  - Venice tide gauge records,
  - global temperature anomalies,
  - atmospheric CO₂,
  - global mean sea level,
  - and RCP-based sea-level scenarios.

- **Engineering context**  
  The topic is directly relevant for **civil engineering**, **urban planning**, **coastal protection**, and **infrastructure decision-making** (e.g. MOSE barriers, flood defences, drainage).

- **Clear business / decision-support case**  
  The application is framed as a **decision-support dashboard** for:
  - urban planners and engineers,
  - government authorities,
  - civil protection agencies,
  - and secondarily for tourism and public awareness.

- **Machine learning & modelling applicability**  
  Linear regression and simple climate-driven models are well suited to:
  - long-term trend analysis of time series,
  - combining local measurements with global climate indicators,
  - providing understandable results plus prediction intervals.

## Rejected Ideas and Reasons

- **Stock Price Predictor**  
  - Overly generic and heavily overused as a student project topic.  
  - Weak connection to engineering / mechatronics and physical systems.

- **Supply Chain Delay Risk Analyzer**  
  - Interesting from a business perspective, but realistic, open datasets are harder to find and clean for this course timeframe.  
  - Would quickly turn into a pure business analytics project.

- **Job Market Analyzer**  
  - Potentially useful, but not clearly tied to engineering domain knowledge or physical modelling.  
  - Data is fragmented and often scraped or noisy.

The Venice sea-level topic offered a better balance of **data quality**, **engineering relevance**, and **clarity of impact**.

## Data Sources Considered

- **Venice tide gauge data (PSMSL / related sources)** — selected for historical relative sea level data (including land subsidence effects).
- **Global temperature anomalies (NASA GISTEMP)** — selected to represent large-scale warming signal.
- **Atmospheric CO₂ (NOAA Mauna Loa)** — selected as a key driver for long-term climate change.
- **Global Mean Sea Level (NASA satellite altimetry)** — selected to compare global mean trends with local Venice behaviour.
- **Sea-level scenario / RCP data for Venice (Excel)** — selected to provide physically based projections (RCP 2.6, RCP 8.5, high-end scenario) for comparison with the statistical models.

Other sources that were briefly considered but not used:

- **Kaggle** — rejected due to limited Venice-specific and tide-gauge-quality data.
- **UN Comtrade / World Bank** — not directly relevant for a sea-level / flooding application.

## Technology Decisions

- **Python** — required by the course and well-suited for data science + web apps.
- **pandas + numpy** — for loading, cleaning and transforming time-series and tabular data.
- **scikit-learn** — to implement:
  - simple linear regression (historical trend),
  - a climate-driven multivariate regression (year + temperature + CO₂).
- **Plotly** — for interactive, web-ready time-series visualisations and uncertainty bands.
- **Streamlit** — chosen as the web application framework:
  - quick to develop,
  - good for dashboards,
  - easy to integrate with Python data science code.
- **.streamlit/config.toml** — to configure application-wide theme and improve visual consistency.

These choices keep the tech stack **simple and coherent**, while still allowing for meaningful modelling, visualisation, and an interactive user experience.