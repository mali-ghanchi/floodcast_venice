# Brainstorm

**Author:** Muhammad Ali Ghanchi

---

# Initial Idea Generation

When first approaching this project, several application ideas were considered:

- Spare Parts Demand Forecaster
- Supply Chain Delay Risk Analyzer
- Stock Price Trend Predictor
- Job Market Analyzer
- Venice Sea Level Rise Predictor

---

# Why Venice Sea Level Rise?

After evaluating all options, the **Venice Sea Level Rise Predictor** was selected for several reasons.

## Real-World Relevance

Venice is one of the world's most flood-prone cities due to:

- sea-level rise,
- tidal flooding (*acqua alta*),
- long-term land subsidence.

The city represents an important real-world case study for understanding climate impacts on coastal communities.

---

## Data Availability

A wide range of open datasets were available and could be combined within a single application:

- Venice tide gauge observations,
- global temperature anomalies,
- atmospheric CO₂ concentrations,
- global mean sea-level records,
- scenario-based sea-level projections,
- NASA/IPCC local sea-level projections.

The availability of multiple independent datasets made it possible to investigate relationships between local sea level and broader climate drivers.

---

## Engineering Relevance

The topic is strongly connected to several engineering disciplines, including:

- Civil engineering,
- Coastal engineering,
- Urban planning,
- Flood risk management,
- Infrastructure resilience.

The project therefore provides practical relevance beyond purely academic forecasting.

---

## Decision-Support Potential

The application can provide useful information for several groups:

- Urban planners,
- Civil protection agencies,
- Government authorities,
- Researchers,
- Students,
- Interested members of the public.

Interactive visualisations and future projections can support awareness and planning decisions.

---

## Suitability for Modelling

The problem supports several complementary modelling approaches:

- Historical linear regression,
- Climate-driven multivariate regression,
- SARIMAX time-series forecasting,
- Comparison against externally published scenario projections.

This allows different modelling techniques to be evaluated and compared within the same application.

---

# Rejected Ideas and Reasons

## Stock Price Trend Predictor

- Very common project topic.
- Limited engineering relevance.
- Strong influence of unpredictable market behaviour.

---

## Supply Chain Delay Risk Analyzer

- Interesting real-world application.
- Difficult to obtain suitable open datasets.
- Greater complexity within the available project timeframe.

---

## Job Market Analyzer

- Less closely related to physical systems.
- Reduced opportunity for environmental or engineering modelling.

---

The Venice sea-level project offered the best balance between:

- real-world importance,
- open data availability,
- technical complexity,
- engineering relevance,
- visual impact.

---

# Data Sources Considered

| Data Source | Purpose |
|------------|----------|
| Venice tide gauge data | Historical relative sea level |
| Global temperature anomalies | Large-scale warming signal |
| Atmospheric CO₂ | Long-term climate forcing indicator |
| Global Mean Sea Level | Global comparison benchmark |
| Scenario-based Venice projections | Future comparison scenarios |
| NASA/IPCC local projections | Physically informed local projections |

---

# Technology Decisions

The following technologies were selected for the project.

## Python

Primary programming language used throughout the application.

## pandas and NumPy

Used for:

- data cleaning,
- transformation,
- merging,
- numerical analysis.

## scikit-learn

Used for:

- regression models,
- feature scaling,
- model evaluation,
- hyperparameter tuning.

## statsmodels

Used for:

- SARIMAX time-series forecasting.

## Plotly

Used to create:

- interactive visualisations,
- time-series plots,
- comparison dashboards.

## Streamlit

Used to develop the multi-page web application.

## openpyxl

Used to:

- read Excel-based scenario and projection datasets.

## `.streamlit/config.toml`

Used to provide:

- application-wide visual styling,
- consistent theme settings.

---

# Technology Selection Rationale

These tools were chosen to ensure that the project remained:

- technically coherent,
- practical to implement,
- suitable for machine learning and time-series analysis,
- capable of producing interactive visualisations,
- appropriate for a decision-support dashboard.

---

# Final Decision

The **FloodCast Venice** project was selected because it combines:

- environmental relevance,
- engineering applications,
- machine learning techniques,
- time-series forecasting,
- multiple real-world datasets,
- interactive visualisation.

The result is a technically challenging and socially relevant application capable of supporting understanding of future sea-level rise in Venice.

---