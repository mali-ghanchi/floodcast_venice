# Brainstorm

**Author:** Muhammad Ali Ghanchi

---

## Initial Ideas Considered

When first approaching this project, several application ideas were shortlisted:

- Spare Parts Demand Forecaster
- Supply Chain Delay Risk Analyzer
- Stock Price Trend Predictor
- Job Market Analyzer
- Venice Sea Level Rise Predictor

---

## Why Venice Sea Level Rise?

Venice was selected because it hit every requirement cleanly:

- **Real data exists and is open** — PSMSL tide gauge data going back to 1909, NASA/IPCC projections, global temperature and CO2 records, all freely available
- **Engineering relevance** — directly applicable to civil engineering, coastal infrastructure planning, and flood risk management
- **Clear business case** — urban planners and civil protection agencies genuinely need this kind of decision-support tool
- **Multiple modelling approaches possible** — the data supports linear regression and multivariate regression, making it suitable for demonstrating a range of AI/ML techniques
- **Visual impact** — sea level trends and future projections make for compelling, readable charts

---

## Why the Other Ideas Were Rejected

- **Stock Price Predictor** — overdone, weak engineering relevance, heavily influenced by unpredictable market events
- **Supply Chain Analyzer** — good business case but real datasets are hard to find and clean
- **Job Market Analyzer** — interesting but lacks connection to physical or engineering systems

---

## Data Sources Evaluated

| Dataset | Source | Decision |
|---|---|---|
| Venice tide gauge (1909–2000) | PSMSL | Used — primary historical record |
| RCP scenario projections | Zenodo | Used — for comparison dashboard |
| Global temperature anomalies | NASA GISTEMP | Used — climate-driven model feature |
| Atmospheric CO2 | Mauna Loa Observatory | Used — climate-driven model feature |
| Global Mean Sea Level | NASA satellite altimetry | Used — Global vs Local page |
| NASA/IPCC local projections for Venice | IPCC AR6 | Used — historical analysis comparison |
| Synthetic datasets | — | Rejected — prohibited by brief |

---

## Technology Decisions

| Tool | Role | Why chosen |
|---|---|---|
| Python | Core language | Required by brief |
| pandas + NumPy | Data cleaning, merging, numerical operations | Standard, already familiar |
| scikit-learn | Linear regression, Ridge, GridSearchCV, metrics | Best-in-class for ML in Python |
| Plotly | Interactive charts | Hover tooltips, zoom, legend toggles — far better than matplotlib for a web app |
| Streamlit | Web application framework | Fastest path from Python script to working web app; no frontend knowledge required |
| openpyxl | Reading Excel files | Required for pandas to handle .xlsx datasets |
| requests | WorldTides API calls | Standard HTTP library for live API integration |
| Git / GitLab | Version control | Required by brief |

---

## Key Design Decisions Made During Development

- **Switched from matplotlib to Plotly** — matplotlib produces static images; Plotly gives proper interactivity in the browser
- **Chose Streamlit over NiceGUI** — NiceGUI requires more boilerplate; Streamlit is Python-native and much faster to iterate with
- **Kept RCP data for comparison only, not training** — RCP values are projections, not real measurements; using them as training data would mean learning from someone else's model, not real observations
- **Used full dataset for deployed forecasts, separate split model for evaluation** — maximises training data for the actual predictions users see, while still providing an honest held-out test result
- **Chronological split for evaluation** — more honest than random splitting for a forecasting task, since it truly simulates predicting the future from the past
- **Added uncertainty bands** — after testing revealed non-stationarity (the 1989-1991 dip), a single confident prediction line would have been misleading; the widening band honestly communicates growing uncertainty at longer horizons
- **Integrated WorldTides API for short-term forecast** — provides a live real-world tide reading for Venice, adding a real-time data dimension alongside the long-term model projections
