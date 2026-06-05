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
This page uses **global temperature and CO₂**, together with time,
to predict **relative sea level in Venice**.

We first fit a regression model on historical data.
Optionally, you can explore a **future extrapolation** up to 2100,
including a **statistical prediction interval** that widens with time.
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

# Residuals and residual std (noise level)
residuals = y - y_pred_hist
n_samples, n_features = X.shape
dof = max(n_samples - (n_features + 1), 1)  # +1 for intercept
s = np.sqrt(np.sum(residuals**2) / dof)

# Design matrix with intercept for prediction interval
X_design = np.column_stack([np.ones(len(X)), X.values])
XtX_inv = np.linalg.inv(X_design.T @ X_design)

# Metrics
mae = mean_absolute_error(y, y_pred_hist)
rmse = np.sqrt(np.mean(residuals**2))

st.markdown(f"""
### Historical Fit (Climate-Driven Model)

- Features used: `year`, `temp_anomaly`, `co2_ppm`  
- MAE (Mean Absolute Error): **{mae:.2f} cm**  
- RMSE (Root Mean Squared Error): **{rmse:.2f} cm**
""")

# ===================================
# 4. BUTTONS: HISTORICAL vs FUTURE
# ===================================

if "show_future_climate" not in st.session_state:
    st.session_state.show_future_climate = False

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("📈 Explore Future Prediction"):
        st.session_state.show_future_climate = True

with col_btn2:
    if st.button("📉 Return to Historical"):
        st.session_state.show_future_climate = False

show_future = st.session_state.show_future_climate

# ===================================
# 5. EXTRAPOLATION TO 2100 (ONLY IF ENABLED)
# ===================================

if show_future:
    # Fit simple linear trends temp(year) and co2(year)
    temp_trend_model = LinearRegression()
    temp_trend_model.fit(df[['year']], df['temp_anomaly'])

    co2_trend_model = LinearRegression()
    co2_trend_model.fit(df[['year']], df['co2_ppm'])

    # Future years: include the last historical year so curves connect
    future_years = np.arange(year_max, 2101)
    future_years_df = pd.DataFrame({'year': future_years})

    # Extrapolate temp and CO₂
    future_temp = temp_trend_model.predict(future_years_df[['year']])
    future_co2 = co2_trend_model.predict(future_years_df[['year']])

    future_features = pd.DataFrame({
        'year': future_years,
        'temp_anomaly': future_temp,
        'co2_ppm': future_co2
    })

    # Climate-driven sea level prediction for future
    X_future = future_features[feature_cols].values
    y_future_pred = climate_model.predict(future_features[feature_cols])

    # --- REAL prediction interval based on linear regression ---
    # Build design matrix for future (with intercept)
    X_future_design = np.column_stack([np.ones(len(X_future)), X_future])

    # For each future point, compute prediction std:
    # std_pred(x0) = s * sqrt(1 + x0^T (X^T X)^(-1) x0)
    pred_var = []
    for x0 in X_future_design:
        v = x0 @ XtX_inv @ x0.T
        pred_var.append(1.0 + v)

    pred_var = np.array(pred_var)
    std_pred = s * np.sqrt(pred_var)

    z = 1.96  # ~95% prediction interval
    upper_bound = y_future_pred + z * std_pred
    lower_bound = y_future_pred - z * std_pred

else:
    future_years = None
    y_future_pred = None
    upper_bound = None
    lower_bound = None

# ===================================
# 6. PLOT: HISTORICAL + OPTIONAL FUTURE + UNCERTAINTY
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

# Future extrapolated prediction + uncertainty
if show_future and future_years is not None:
    # Uncertainty band
    fig.add_trace(go.Scatter(
        x=np.concatenate([future_years, future_years[::-1]]),
        y=np.concatenate([upper_bound, lower_bound[::-1]]),
        fill='toself',
        name='Prediction Interval (~95%)',
        hoverinfo='skip',
        line=dict(color='rgba(255, 0, 0, 0)'),
        fillcolor='rgba(255, 0, 0, 0.2)'
    ))

    # Future prediction line
    fig.add_trace(go.Scatter(
        x=future_years,
        y=y_future_pred,
        name='Climate-Driven Prediction (Extrapolated)',
        mode='lines',
        line=dict(color='red', dash='dash', width=2)
    ))

fig.update_layout(
    title='Climate-Driven Regression: Past Fit and Future Extrapolation',
    xaxis_title='Year',
    yaxis_title='Sea Level (cm)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# ===================================
# 7. INTERPRETATION
# ===================================

st.markdown("""
### Interpretation

- The **orange dashed line** is the **regression fit** learned from historical data:
  it links `year`, `temp_anomaly`, and `co2_ppm` to **Venice sea level**.

- When you click **“Explore Future Prediction”**, the app:
  1. Fits simple linear trends for global temperature and CO₂ over time.
  2. Extrapolates these trends up to the year 2100.
  3. Applies the **same regression model** to these future values.

- The **red dotted line** is the **extrapolated climate-driven prediction**.
- The **red shaded area** is a **prediction interval** based on the
  regression's residual variance and the linear model structure.
  It widens with time because predictions far beyond the training range
  are statistically less certain.

This gives you a **data-driven scenario curve with quantified uncertainty**
that you can compare to other sea-level scenarios (e.g. RCP-based projections)
in your overall decision-support dashboard.
""")

# ===================================
# 6b. RESIDUAL PLOT (MODEL EVALUATION)
# ===================================

st.markdown("### Residual analysis")

fig_res = go.Figure()
fig_res.add_trace(go.Scatter(
    x=df['year'],
    y=residuals,
    mode="markers",
    name="Residuals (Observed - Predicted)",
    marker=dict(color="darkslategray", size=6)
))

fig_res.add_hline(y=0, line=dict(color="red", dash="dot"))

fig_res.update_layout(
    title="Residuals over time",
    xaxis_title="Year",
    yaxis_title="Residual (cm)",
    hovermode="x"
)

st.plotly_chart(fig_res, use_container_width=True)

st.markdown("""
The residuals show how far the model predictions deviate from the observed
sea level in each year. Values scattered around zero without a strong long-term
trend indicate that the model captures the **overall mean relationship**
reasonably well, while short-term variability and local processes remain
unresolved.
""")