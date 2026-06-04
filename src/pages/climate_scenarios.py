import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.title("🌍 Climate-Driven Sea Level Prediction")

st.markdown("""
This page uses **global temperature and CO₂** together with time
to predict **relative sea level in Venice**, and extrapolates this
relationship into the future.
""")

# ===================================
# 1. LOAD DATA
# ===================================

# --- Venice tide gauge ---
sea = pd.read_csv('data/venice data - historical.txt', sep=';', header=None)
sea.columns = ['year', 'sea_level_mm', 'flag', 'quality']
sea = sea[sea['sea_level_mm'] != -99999]
sea['sea_level_cm'] = sea['sea_level_mm'] / 10
sea = sea[['year', 'sea_level_cm']]

# --- Global temperature: GLB.Ts+dSST.csv ---
# col 0 = Year, col 13 ≈ annual mean anomaly
temp_raw = pd.read_csv('data/GLB.Ts+dSST.csv', header=None, sep=',')

temp = temp_raw[[0, 13]].copy()
temp.columns = ['year', 'temp_anomaly']
temp['temp_anomaly'] = pd.to_numeric(temp['temp_anomaly'], errors='coerce')
temp = temp.dropna(subset=['temp_anomaly'])

# --- CO₂: co2_annmean_mlo.csv ---
# col 0 = year, col 1 = annual mean ppm
co2_raw = pd.read_csv('data/co2_annmean_mlo.csv', header=None, sep=',')

co2 = co2_raw[[0, 1]].copy()
co2.columns = ['year', 'co2_ppm']
co2['co2_ppm'] = pd.to_numeric(co2['co2_ppm'], errors='coerce')
co2 = co2.dropna(subset=['co2_ppm'])

# ===================================
# 2. MERGE DATASETS
# ===================================

df = sea.merge(temp, on='year', how='inner')
df = df.merge(co2, on='year', how='inner')

year_min = int(df['year'].min())
year_max = int(df['year'].max())
st.markdown(f"**Merged dataset years:** {year_min}–{year_max}")

# ===================================
# 3. TRAIN CLIMATE-DRIVEN MODEL
# ===================================

feature_cols = ['year', 'temp_anomaly', 'co2_ppm']
X = df[feature_cols]
y = df['sea_level_cm']

climate_model = LinearRegression()
climate_model.fit(X, y)

# Historical predictions
y_pred_hist = climate_model.predict(X)

mae = mean_absolute_error(y, y_pred_hist)

st.markdown(f"""
### Historical Fit (Climate-Driven Model)

- Features used: `year`, `temp_anomaly`, `co2_ppm`  
- MAE (Mean Absolute Error): **{mae:.2f} cm**
""")

# ===================================
# 4. EXTRAPOLATE TEMP & CO₂ → 2100
# ===================================

st.markdown("### Future Extrapolation up to 2100")

st.markdown("""
We linearly extrapolate global **temperature** and **CO₂** trends over time,
then feed these extrapolated values into the climate-driven model to obtain
a possible future sea level trajectory for Venice.
""")

# Fit simple linear trends temp(year) and co2(year)
temp_trend_model = LinearRegression()
temp_trend_model.fit(df[['year']], df['temp_anomaly'])

co2_trend_model = LinearRegression()
co2_trend_model.fit(df[['year']], df['co2_ppm'])

# Future years
future_years = np.arange(year_max + 1, 2101)
future_years_df = pd.DataFrame({'year': future_years})

# Extrapolate temp and co2
future_temp = temp_trend_model.predict(future_years_df[['year']])
future_co2 = co2_trend_model.predict(future_years_df[['year']])

future_features = pd.DataFrame({
    'year': future_years,
    'temp_anomaly': future_temp,
    'co2_ppm': future_co2
})

# Climate-driven sea level prediction for future
y_future_pred = climate_model.predict(future_features[feature_cols])

# ===================================
# 5. PLOT: HISTORICAL + FUTURE
# ===================================

fig = go.Figure()

# Historical observed
fig.add_trace(go.Scatter(
    x=df['year'],
    y=df['sea_level_cm'],
    name='Venice Sea Level (Observed)',
    mode='lines',
    line=dict(color='steelblue', width=1.5)
))

# Historical model fit
fig.add_trace(go.Scatter(
    x=df['year'],
    y=y_pred_hist,
    name='Model Fit (Climate-Driven, Historical)',
    mode='lines',
    line=dict(color='orange', dash='dash', width=2)
))

# Future extrapolated prediction
fig.add_trace(go.Scatter(
    x=future_years,
    y=y_future_pred,
    name='Climate-Driven Prediction (Extrapolated)',
    mode='lines',
    line=dict(color='purple', dash='dot', width=2)
))

fig.update_layout(
    title='Climate-Driven Regression: Past Fit and Future Extrapolation',
    xaxis_title='Year',
    yaxis_title='Sea Level (cm)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# ===================================
# 6. INTERPRETATION
# ===================================

st.markdown("""
### Interpretation

This page shows a **climate-driven regression model** that uses:

- `year` (capturing long-term local effects like subsidence),
- `temp_anomaly` (global temperature anomaly),
- `co2_ppm` (global atmospheric CO₂),

to predict **relative sea level in Venice**.

We:

1. Train the model on the historical overlap period.
2. Fit simple linear trends for global temperature and CO₂ as functions of time.
3. Extrapolate temperature and CO₂ up to the year 2100.
4. Use the climate-driven model to compute a **future sea level trajectory** for Venice.

The extrapolated curve is not a full physical climate model, but a
**data-driven scenario** that links global climate trends to local flood risk
in a way that can support discussions for urban planning and civil protection.
""")