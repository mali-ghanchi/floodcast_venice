# Brainstorm

## Author
- Muhammad Ali Ghanchi

## Initial Idea Generation
When first approaching this project, several application ideas were considered:

- **Spare Parts Demand Forecaster** — predicting factory spare part needs to reduce costs
- **Supply Chain Delay Risk Analyzer** — flagging high-risk shipments before they are sent
- **Stock Price Trend Predictor** — forecasting market trends using historical data
- **Job Market Analyzer** — analyzing engineering job market trends
- **Venice Sea Level Rise Predictor** — analyzing and predicting sea level rise in Venice using historical tide gauge data

## Why Venice Sea Level Rise?
After evaluating all options, the Venice Sea Level Rise Predictor was selected for the following reasons:

- **Real-world relevance** — Venice is one of the most documented cases of sea level rise and urban flooding globally
- **Data availability** — high quality, open-source historical tide gauge data is freely available via PSMSL and Zenodo
- **Engineering context** — directly applicable to civil engineering, urban planning, and infrastructure decision-making
- **Clear business case** — the application serves urban planners, government authorities, and civil protection agencies
- **Machine Learning applicability** — linear regression is well suited to long-term trend forecasting on time series data

## Rejected Ideas and Reasons
- **Stock Price Predictor** — overly generic, heavily done by other students, weak engineering relevance
- **Supply Chain Analyzer** — strong business case but real datasets are harder to find and clean
- **Job Market Analyzer** — interesting but lacks direct engineering/mechatronics relevance

## Data Sources Considered
- **PSMSL (Permanent Service for Mean Sea Level)** — selected for historical tide gauge data (1909–2000)
- **Zenodo (Record 5139890)** — selected for RCP-based future sea level projections (2007–2100)
- **Kaggle** — considered but rejected as Venice-specific data was limited
- **UN Comtrade / World Bank** — considered but not relevant to this specific application

## Technology Decisions
- **Python** — required by course
- **pandas + numpy** — data loading, cleaning, and processing
- **scikit-learn** — linear regression model for sea level prediction
- **Plotly** — interactive web-based visualizations
- **Streamlit** — web application framework, simple and beginner-friendly
