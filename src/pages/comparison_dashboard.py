import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

# -----------------------------
# LOAD HISTORICAL SEA LEVEL
# -----------------------------
sea = pd.read_csv('data/venice data - historical.txt', sep=';', header=None)
sea.columns = ['year', 'sea_level_mm', 'flag', 'quality']
sea = sea[sea['sea_level_mm'] != -99999]
sea['sea_level_cm'] = sea['sea_level_mm'] / 10
sea = sea[['year', 'sea_level_cm']]

# -----------------------------
# LOAD GLOBAL TEMPERATURE
# -----------------------------
# GLB.Ts+dSST.csv: col 0 = Year, col 13 ≈ annual mean anomaly
temp_raw = pd.read_csv('data/GLB.Ts+dSST.csv', header=None, sep=',')

temp = temp_raw[[0, 13]].copy()
temp.columns = ['year', 'temp_anomaly']
temp['temp_anomaly'] = pd.to_numeric(temp['temp_anomaly'], errors='coerce')
temp = temp.dropna(subset=['temp_anomaly'])

# -----------------------------
# LOAD CO₂ DATA
# -----------------------------
# co2_annmean_mlo.csv: col 0 = year, col 1 = annual mean ppm
co2_raw = pd.read_csv('data/co2_annmean_mlo.csv', header=None, sep=',')

co2 = co2_raw[[0, 1]].copy()
co2.columns = ['year', 'co2_ppm']
co2['co2_ppm'] = pd.to_numeric(co2['co2_ppm'], errors='coerce')
co2 = co2.dropna(subset=['co2_ppm'])

# -----------------------------
# MERGE DATASETS (SEA + TEMP + CO₂)
# -----------------------------
df = sea.merge(temp, on='year', how='inner')
df = df.merge(co2, on='year', how='inner')

# -----------------------------
# TRAIN CLIMATE-DRIVEN REGRESSION
# -----------------------------
feature_cols = ['year', 'temp_anomaly', 'co2_ppm']
X = df[feature_cols]
y = df['sea_level_cm']

climate_model = LinearRegression()
climate_model.fit(X, y)

# Historical predictions (for residuals)
y_pred_hist = climate_model.predict(X)

# Residuals and residual std
residuals = y - y_pred_hist
n_samples, n_features = X.shape
dof = max(n_samples - (n_features + 1), 1)  # +1 for intercept
s = np.sqrt(np.sum(residuals**2) / dof)

# Design matrix with intercept for confidence band
X_design = np.column_stack([np.ones(len(X)), X.values])
XtX_inv = np.linalg.inv(X_design.T @ X_design)

# Baseline: predicted sea level at year 2000 using climate-driven model
row_2000 = df[df['year'] == 2000].iloc[0]
baseline = climate_model.predict(
    [[row_2000['year'], row_2000['temp_anomaly'], row_2000['co2_ppm']]]
)[0]

# -----------------------------
# FUTURE PREDICTION 2000–2100
# -----------------------------

# Fit linear trends for temp(year) and co2(year) on historical period
temp_trend_model = LinearRegression()
temp_trend_model.fit(df[['year']], df['temp_anomaly'])

co2_trend_model = LinearRegression()
co2_trend_model.fit(df[['year']], df['co2_ppm'])

# Future years
future_years_array = np.arange(2000, 2101)
future_years = pd.DataFrame({'year': future_years_array})

# Extrapolate future temp and CO₂
future_temp = temp_trend_model.predict(future_years[['year']])
future_co2 = co2_trend_model.predict(future_years[['year']])

future_features = pd.DataFrame({
    'year': future_years_array,
    'temp_anomaly': future_temp,
    'co2_ppm': future_co2
})

X_future = future_features[feature_cols].values
predicted_levels = climate_model.predict(future_features[feature_cols])

# --- Regression-based confidence band (for mean prediction) ---
X_future_design = np.column_stack([np.ones(len(X_future)), X_future])

pred_var = []
for x0 in X_future_design:
    v = x0 @ XtX_inv @ x0.T  # variance of mean prediction
    pred_var.append(v)

pred_var = np.array(pred_var)
std_pred = s * np.sqrt(pred_var)

z = 1.64  # ~90% confidence interval (tighter visually)
upper_bound = predicted_levels + z * std_pred
lower_bound = predicted_levels - z * std_pred

# -----------------------------
# LOAD RCP DATA
# -----------------------------
rcp = pd.read_excel('data/venice_sea_level comparison.xlsx')
rcp = rcp.rename(columns={'Unnamed: 1': 'year'})
rcp = rcp[['year', 'rcp2.6_95', 'rcp8.5_50', 'high-end']].dropna()

# Convert metres to cm and add to baseline
rcp['best_case_cm'] = baseline + (rcp['rcp2.6_95'] * 100)
rcp['medium_cm'] = baseline + (rcp['rcp8.5_50'] * 100)
rcp['worst_case_cm'] = baseline + (rcp['high-end'] * 100)

# -----------------------------
# PAGE TITLE
# -----------------------------
st.markdown("# ⚖️ Comparison Dashboard")
st.markdown("Compare our **climate-driven prediction** against RCP climate scenarios.")

# -----------------------------
# PLOT
# -----------------------------
fig = go.Figure()

# Historical data (sea level)
fig.add_trace(go.Scatter(
    x=sea['year'], y=sea['sea_level_cm'],
    name='Historical Data (Tide Gauge)',
    line=dict(color='steelblue', width=1.5),
    opacity=0.6
))

# Uncertainty band for our prediction
fig.add_trace(go.Scatter(
    x=np.concatenate([future_years_array, future_years_array[::-1]]),
    y=np.concatenate([upper_bound, lower_bound[::-1]]),
    fill='toself',
    name='Our Prediction Uncertainty (~90%)',
    hoverinfo='skip',
    line=dict(color='rgba(255, 165, 0, 0)'),  # transparent border
    fillcolor='rgba(255, 165, 0, 0.2)'        # light orange
))

# Our climate-driven prediction
fig.add_trace(go.Scatter(
    x=future_years['year'], y=predicted_levels,
    name='Our Prediction (Climate-Driven)',
    line=dict(color='orange', dash='dash', width=2)
))

# RCP Best case
fig.add_trace(go.Scatter(
    x=rcp['year'], y=rcp['best_case_cm'],
    name='RCP 2.6',
    line=dict(color='green', dash='dot', width=2)
))

# RCP Medium
fig.add_trace(go.Scatter(
    x=rcp['year'], y=rcp['medium_cm'],
    name='RCP 8.5 (median)',
    line=dict(color='goldenrod', dash='dot', width=2)
))

# RCP Worst case
fig.add_trace(go.Scatter(
    x=rcp['year'], y=rcp['worst_case_cm'],
    name='High-end scenario',
    line=dict(color='red', dash='dot', width=2)
))

fig.update_layout(
    title='Venice Sea Level — Climate-Driven Prediction vs Climate Scenarios',
    xaxis_title='Year',
    yaxis_title='Sea Level (cm)',
    hovermode='x unified',
    legend=dict(
        orientation='h',
        yanchor='top',
        y=1.02,        # legend above plot
        xanchor='center',
        x=0.5
    ),
    margin=dict(b=80)  # extra bottom space for x-axis labels
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# THRESHOLD ANALYSIS
# -----------------------------

st.markdown("### Threshold analysis")

st.write(
    "Select a critical threshold above the year 2000 sea level. "
    "The table shows when each scenario first exceeds this level."
)

# Slider: threshold above year 2000 level
threshold_cm = st.slider(
    "Critical threshold above year 2000 level (cm)",
    min_value=0,
    max_value=100,
    value=30,
    step=5
)

# Absolute threshold in cm (relative to same reference as the curves)
threshold_absolute = baseline + threshold_cm

def first_year_crossing(years_array, values_array, threshold_value):
    """Return first year where values >= threshold_value, or 'Not before 2100'."""
    years_array = np.array(years_array)
    values_array = np.array(values_array)
    mask = values_array >= threshold_value
    if not np.any(mask):
        return "Not before 2100"
    return int(years_array[mask][0])

# Compute first exceedance year for each scenario
year_our_pred = first_year_crossing(future_years_array, predicted_levels, threshold_absolute)
year_rcp_26 = first_year_crossing(rcp['year'].values, rcp['best_case_cm'].values, threshold_absolute)
year_rcp_85 = first_year_crossing(rcp['year'].values, rcp['medium_cm'].values, threshold_absolute)
year_high_end = first_year_crossing(rcp['year'].values, rcp['worst_case_cm'].values, threshold_absolute)

results_df = pd.DataFrame({
    "Scenario": [
        "Our Prediction (Climate-Driven)",
        "RCP 2.6",
        "RCP 8.5 (median)",
        "High-end scenario"
    ],
    f"First year ≥ baseline + {threshold_cm} cm": [
        year_our_pred,
        year_rcp_26,
        year_rcp_85,
        year_high_end
    ]
})

st.table(results_df)

# -----------------------------
# EXPLANATION
# -----------------------------
st.markdown("""
### What are we comparing?

- 🟠 **Our Prediction (Climate-Driven)**  
  Multivariate regression trained on real Venice tide gauge data **and**  
  global temperature anomaly and CO₂.

- 🟠 **Uncertainty Band**  
  The shaded orange area is a **statistical confidence band** for the
  mean prediction of our regression model.

- 🟢 **RCP 2.6** — strong global mitigation, limited sea-level rise.  
- 🟡 **RCP 8.5 (median)** — high emissions, median sea-level response.  
- 🔴 **High-end scenario** — high emissions combined with strong ice-sheet response.

### Interpretation for planners and authorities

The **tide gauge record** already includes the combined effect of **global sea-level rise**
and **local land subsidence** in Venice. Our climate-driven regression continues this
historical relationship into the future, assuming that subsidence and the response to
global warming remain similar to the past.

However, the **RCP-based scenarios** incorporate additional physical processes,
especially accelerated ice-sheet melt, that can push global sea level — and thus
relative sea level in Venice — **well above what a simple statistical model would predict**.

The threshold table above shows how **high-end scenarios can reach critical levels
decades earlier** than the pure climate-driven regression.

For urban planners, this means that relying only on historical trends (even with CO₂
and temperature included) is risky; adaptation strategies should be stress-tested
against the **medium and high-end RCP scenarios**.
""")