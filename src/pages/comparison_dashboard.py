import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

# -----------------------------
# LOAD HISTORICAL SEA LEVEL
# -----------------------------
sea = pd.read_csv(
    'data/venice data - historical.txt',
    sep=';', header=None
)
sea.columns = ['year', 'sea_level_mm', 'flag', 'quality']
sea = sea[sea['sea_level_mm'] != -99999]
sea['sea_level_cm'] = sea['sea_level_mm'] / 10
sea = sea[['year', 'sea_level_cm']]

# -----------------------------
# LOAD CO2 DATA
# -----------------------------
co2 = pd.read_csv('data/co2_annmean_mlo.csv', comment='#', header=None)
co2.columns = ['year', 'co2_ppm', 'uncertainty']
co2 = co2[['year', 'co2_ppm']]

# -----------------------------
# LOAD TEMPERATURE DATA
# -----------------------------
temp = pd.read_csv('data/GLB.Ts+dSST.csv', skiprows=1)
temp = temp.rename(columns={temp.columns[0]: 'year', temp.columns[-3]: 'annual_temp'})
temp = temp[['year', 'annual_temp']]
temp['year'] = pd.to_numeric(temp['year'], errors='coerce')
temp['annual_temp'] = pd.to_numeric(temp['annual_temp'], errors='coerce')
temp = temp.dropna()

# -----------------------------
# MERGE ALL THREE DATASETS
# -----------------------------
df = sea.merge(co2, on='year').merge(temp, on='year')

st.markdown("### 🔬 Hybrid Model — Merged Dataset")
st.write(f"Training on {len(df)} years of overlapping data ({int(df['year'].min())}–{int(df['year'].max())})")

# -----------------------------
# TRAIN HYBRID MODEL
# -----------------------------
X = df[['year', 'co2_ppm', 'annual_temp']]
y = df['sea_level_cm']

model = LinearRegression()
model.fit(X, y)

st.write(f"**Model R² Score:** {model.score(X, y):.4f}")
st.write("*(R² closer to 1.0 = better fit)*")

# -----------------------------
# FUTURE PREDICTIONS
# -----------------------------
# For future years we need estimated CO2 and temp values
# We use simple linear extrapolation for those too
co2_model = LinearRegression()
co2_model.fit(df[['year']], df['co2_ppm'])

temp_model = LinearRegression()
temp_model.fit(df[['year']], df['annual_temp'])

future_years = np.arange(2001, 2101)
future_co2 = co2_model.predict(future_years.reshape(-1, 1))
future_temp = temp_model.predict(future_years.reshape(-1, 1))

future_X = pd.DataFrame({
    'year': future_years,
    'co2_ppm': future_co2,
    'annual_temp': future_temp
})

future_predictions = model.predict(future_X)

# -----------------------------
# PLOT
# -----------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['year'], y=df['sea_level_cm'],
    name='Historical Data',
    line=dict(color='steelblue')
))

fig.add_trace(go.Scatter(
    x=future_years, y=future_predictions,
    name='Hybrid Model Prediction',
    line=dict(color='red', dash='dash')
))

fig.update_layout(
    title='Venice Sea Level — Hybrid Model Prediction',
    xaxis_title='Year',
    yaxis_title='Sea Level (cm)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# EXPLANATION
# -----------------------------
st.markdown("""
### How the Hybrid Model Works
Unlike a simple linear regression that only uses time,
this model uses **three inputs** simultaneously:
- 📅 **Year** — captures the overall time trend
- 🌫️ **CO2 levels (ppm)** — captures the effect of greenhouse gas emissions
- 🌡️ **Global temperature anomaly** — captures the effect of warming oceans

This is called **multivariate linear regression** and gives a more
scientifically grounded prediction than time alone.
""")