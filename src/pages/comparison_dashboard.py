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
# TRAIN LINEAR REGRESSION
# -----------------------------
X = sea[['year']]
y = sea['sea_level_cm']
model = LinearRegression()
model.fit(X, y)

# Get the baseline (sea level at year 2000)
baseline = float(model.predict(pd.DataFrame({'year': [2000]})))

# Predict 2000-2100
future_years = pd.DataFrame({'year': np.arange(2000, 2101)})
predicted_levels = model.predict(future_years)

# -----------------------------
# LOAD RCP DATA
# -----------------------------
rcp = pd.read_excel('data/venice_sea_level_comparison.xlsx')
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
st.markdown("Compare our linear regression prediction against RCP climate scenarios.")

# -----------------------------
# PLOT
# -----------------------------
fig = go.Figure()

# Historical data
fig.add_trace(go.Scatter(
    x=sea['year'], y=sea['sea_level_cm'],
    name='Historical Data',
    line=dict(color='steelblue', width=1.5),
    opacity=0.6
))

# Our prediction
fig.add_trace(go.Scatter(
    x=future_years['year'], y=predicted_levels,
    name='Our Prediction',
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
    title='Venice Sea Level — Our Prediction vs Climate Scenarios',
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
- 🟠 **Our Prediction** — linear regression trained on real Venice tide gauge data (1909–2000)
- 🟢 **Best Case (RCP 2.6)** — humanity drastically cuts emissions
- 🟡 **Medium Case (RCP 8.5 median)** — some action taken, moderate emissions
- 🔴 **Worst Case (High End)** — business as usual, no action taken

The gap between our prediction and the worst case scenario represents the 
**additional impact of accelerating climate change** that a simple linear trend cannot capture.
""")