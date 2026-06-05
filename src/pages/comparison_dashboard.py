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

# Baseline: predicted sea level at year 2000
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

# Climate-driven sea level prediction for future
predicted_levels = climate_model.predict(future_features[feature_cols])

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

# Our climate-driven prediction
fig.add_trace(go.Scatter(
    x=future_years['year'], y=predicted_levels,
    name='Our Prediction (Climate-Driven)',
    line=dict(color='orange', dash='dash', width=2)
))

# RCP Best case
fig.add_trace(go.Scatter(
    x=rcp['year'], y=rcp['best_case_cm'],
    name='Best Case (RCP 2.6)',
    line=dict(color='green', dash='dot', width=2)
))

# RCP Medium
fig.add_trace(go.Scatter(
    x=rcp['year'], y=rcp['medium_cm'],
    name='Medium Case (RCP 8.5 median)',
    line=dict(color='goldenrod', dash='dot', width=2)
))

# RCP Worst case
fig.add_trace(go.Scatter(
    x=rcp['year'], y=rcp['worst_case_cm'],
    name='Worst Case (High End)',
    line=dict(color='red', dash='dot', width=2)
))

fig.update_layout(
    title='Venice Sea Level — Climate-Driven Prediction vs Climate Scenarios',
    xaxis_title='Year',
    yaxis_title='Sea Level (cm)',
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=-0.3)
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# EXPLANATION
# -----------------------------
st.markdown("""
### What are we comparing?

- 🟠 **Our Prediction (Climate-Driven)**  
  Multivariate regression trained on real Venice tide gauge data **plus**  
  global temperature anomaly and CO₂ (`year`, `temp_anomaly`, `co2_ppm`).

- 🟢 **Best Case (RCP 2.6)** — strong global mitigation.
- 🟡 **Medium Case (RCP 8.5 median)** — high emissions, median sea-level response.
- 🔴 **Worst Case (High End)** — high emissions and strong ice-sheet contribution.

The gap between our climate-driven prediction and the worst-case scenario
represents the **additional impact of accelerating global climate processes**
that a simple statistical model trained on past data alone cannot fully capture.
""")