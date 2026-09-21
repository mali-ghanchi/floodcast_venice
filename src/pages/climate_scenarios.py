import streamlit as st
import pandas as pd
import numpy as np

from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV

import plotly.graph_objects as go

st.title("🌍 Climate-Driven Sea Level Prediction")

st.markdown("""
This page uses a **climate-driven regression model** to predict Venice sea level:

- **Chronological train/test split** (train on earlier years, test on later years)  
- **Scaling** of features using StandardScaler  
- **Ridge regression** with **hyperparameter tuning** (alpha) via GridSearchCV  
- Evaluation on a **held-out test period**  
- Then refit the **best model on all data** for:
  - historical fit,
  - future projection to 2100,
  - approximate prediction interval,
  - residual plot,
  - editable export table.
""")


# Venice tide gauge and cleaning data
sea = pd.read_csv("data/venice data - historical.txt", sep=";", header=None)
sea.columns = ["year", "sea_level_mm", "flag", "quality"]
sea = sea[sea["sea_level_mm"] != -99999] 
sea["sea_level_cm"] = sea["sea_level_mm"] / 10
sea = sea[["year", "sea_level_cm"]]

# Global temperature and cleaning data
temp_raw = pd.read_csv("data/GLB.Ts+dSST.csv", header=None, sep=",")
temp = temp_raw[[0, 13]].copy()
temp.columns = ["year", "temp_anomaly"] 
temp["temp_anomaly"] = pd.to_numeric(temp["temp_anomaly"], errors="coerce")
temp = temp.dropna(subset=["temp_anomaly"])

# CO2 and cleaning data
co2_raw = pd.read_csv("data/co2_annmean_mlo.csv", header=None, sep=",")
co2 = co2_raw[[0, 1]].copy()
co2.columns = ["year", "co2_ppm"]
co2["co2_ppm"] = pd.to_numeric(co2["co2_ppm"], errors="coerce")
co2 = co2.dropna(subset=["co2_ppm"])


df = sea.merge(temp, on="year", how="inner")
df = df.merge(co2, on="year", how="inner") #merging

year_min = int(df["year"].min())
year_max = int(df["year"].max())
st.markdown(f"**Merged dataset years:** {year_min}–{year_max}  ·  **Samples:** {len(df)}")



feature_cols = ["year", "temp_anomaly", "co2_ppm"]
X_full = df[feature_cols].values #data training here
y_full = df["sea_level_cm"].values


test_frac = 0.2
n = len(X_full) #split training 80-20
n_test = int(n * test_frac)
n_train = n - n_test

sort_idx = np.argsort(df["year"].values)
X_sorted = X_full[sort_idx]
y_sorted = y_full[sort_idx]
years_sorted = df["year"].values[sort_idx]

X_train, X_test = X_sorted[:n_train], X_sorted[n_train:]
y_train, y_test = y_sorted[:n_train], y_sorted[n_train:]
years_test = years_sorted[n_train:]

st.markdown(f"Train size: **{len(X_train)}**  ·  Test size: **{len(X_test)}**")
st.markdown(f"Test years: **{int(years_test.min())}–{int(years_test.max())}**")


pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", Ridge())
])

param_grid = {
    "model__alpha": [0.01, 0.1, 1.0, 10.0, 100.0]
}

grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
best_alpha = grid_search.best_params_["model__alpha"]
best_cv_score = grid_search.best_score_

st.markdown(f"""
### Hyperparameter tuning

- Tried alphas: `{param_grid["model__alpha"]}`
- Best alpha (from 5-fold CV on train): **{best_alpha}**
- Best cross-validated R² (train folds): **{best_cv_score:.4f}**
""")



y_test_pred = best_model.predict(X_test)

r_test = np.corrcoef(y_test, y_test_pred)[0, 1] if len(y_test) > 1 else np.nan
mae_test = mean_absolute_error(y_test, y_test_pred)
rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))

st.markdown(f"""
### Performance on held-out test period

- Test years: **{int(years_test.min())}–{int(years_test.max())}**
- Pearson R: **{r_test:.4f}** # checking validity of shown graph
- Test MAE: **{mae_test:.2f} cm**
- Test RMSE: **{rmse_test:.2f} cm**
""")


climate_model_full = Pipeline([
    ("scaler", StandardScaler()), 
    ("model", Ridge(alpha=best_alpha))
])

climate_model_full.fit(X_full, y_full)

y_pred_hist = climate_model_full.predict(X_full)

residuals_full = y_full - y_pred_hist
mae_full = mean_absolute_error(y_full, y_pred_hist)
rmse_full = np.sqrt(mean_squared_error(y_full, y_pred_hist))
r_full = np.corrcoef(y_full, y_pred_hist)[0, 1]


n_full = len(X_full)
x_year = df["year"].values

dof = max(n_full - 2, 1)
s = np.sqrt(np.sum(residuals_full**2) / dof)

x_mean = x_year.mean()
Sxx = np.sum((x_year - x_mean) ** 2)

def prediction_std(year_val: float) -> float:
    """
    Approximate prediction standard deviation for a new observation at given year.
    Formula: s * sqrt(1 + 1/n + (x0 - x_mean)^2 / Sxx)
    """
    return s * np.sqrt(1 + 1 / n_full + (year_val - x_mean) ** 2 / Sxx)


future_years = np.arange(year_max, 2101) #future prediction till 2100
future_years_df = pd.DataFrame({"year": future_years})

temp_trend_model = Ridge(alpha=best_alpha)
temp_trend_model.fit(df[["year"]], df["temp_anomaly"])

co2_trend_model = Ridge(alpha=best_alpha)
co2_trend_model.fit(df[["year"]], df["co2_ppm"])

future_temp = temp_trend_model.predict(future_years_df[["year"]])
future_co2 = co2_trend_model.predict(future_years_df[["year"]])

future_features = pd.DataFrame({
    "year": future_years,
    "temp_anomaly": future_temp,
    "co2_ppm": future_co2
})

X_future = future_features[feature_cols].values
y_future_pred = climate_model_full.predict(X_future)

z = 1.96
std_pred = np.array([prediction_std(y) for y in future_years])

upper_bound = y_future_pred + z * std_pred
lower_bound = y_future_pred - z * std_pred



if "show_future_climate_tuned_chrono" not in st.session_state:
    st.session_state.show_future_climate_tuned_chrono = False #using buttons to check future, looks cleaning that way

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("📈 Explore Future Prediction"):
        st.session_state.show_future_climate_tuned_chrono = True

with col_btn2:
    if st.button("📉 Return to Historical"):
        st.session_state.show_future_climate_tuned_chrono = False

show_future = st.session_state.show_future_climate_tuned_chrono

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=years_sorted, #ploting
    y=y_sorted,
    name="Venice Sea Level (Observed)",
    mode="lines",
    line=dict(color="steelblue", width=1.5)
))

hist_pred_sorted = y_pred_hist[sort_idx]

fig.add_trace(go.Scatter(
    x=years_sorted,
    y=hist_pred_sorted,
    name="Model Fit (Climate-Driven, Tuned Ridge)",
    mode="lines",
    line=dict(color="orange", dash="dash", width=2)
))

if show_future:
    fig.add_trace(go.Scatter(
        x=np.concatenate([future_years, future_years[::-1]]),
        y=np.concatenate([upper_bound, lower_bound[::-1]]),
        fill="toself",
        name="Prediction Interval (~95%)",
        hoverinfo="skip",
        line=dict(color="rgba(255, 0, 0, 0)"),
        fillcolor="rgba(255, 0, 0, 0.2)"
    ))

    fig.add_trace(go.Scatter(
        x=future_years,
        y=y_future_pred,
        name="Climate-Driven Prediction (Tuned Ridge)",
        mode="lines",
        line=dict(color="red", dash="dash", width=2)
    ))

fig.update_layout(
    title="Climate-Driven Regression: Historical Fit and Future Extrapolation",
    xaxis_title="Year",
    yaxis_title="Sea Level (cm)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)



st.markdown("""
### Interpretation

- The model uses **year**, **global temperature anomaly**, and **CO₂ concentration** as predictors.
- Feature scaling and Ridge regression with GridSearchCV hyperparameter tuning are applied.
- The model is evaluated on a **held-out later period** (chronological split), mimicking real forecasting.
- The best model is then refitted on **all years** to produce the final historical fit and future projections.
- The **orange dashed line** shows the tuned climate-driven fit to historical data.
- The **red line and shaded band** show the extrapolated future projection with an approximate 95% prediction interval.

**Why Pearson R instead of R²?**  
This model estimates the long-term trend direction in sea level, not precise year-by-year values.
Pearson R measures how well the model tracks the direction of change — which is more meaningful
here than R², which penalises heavily for absolute value misses on a small, noisy test set.
""") #explaining the graph here



if show_future: #carrying out residual analysis
    st.markdown("### Residual analysis (test set only)")

    test_residuals = y_test - y_test_pred

    fig_res = go.Figure()
    fig_res.add_trace(go.Scatter(
        x=years_test,
        y=test_residuals,
        mode="markers",
        name="Test Residuals (Observed - Predicted)",
        marker=dict(color="darkslategray", size=6)
    ))

    fig_res.add_hline(y=0, line=dict(color="red", dash="dot"))

    fig_res.update_layout(
        title="Test-set residuals over time",
        xaxis_title="Year",
        yaxis_title="Residual (cm)",
        hovermode="x"
    )

    st.plotly_chart(fig_res, use_container_width=True)

    st.markdown("""
    These residuals are computed only on the **held-out test period**, showing how far the
    model's predictions deviate from the observed sea level in years it was never trained on.
    Points scattered around zero with no strong pattern indicate the model captures the
    overall trend without a systematic bias.
    """) #more explanation



if show_future: #table for exporting data and what not

    st.markdown("### Future prediction data")

    future_full_df = pd.DataFrame({
        "year": future_years,
        "predicted_sea_level_cm": y_future_pred,
        "lower_95PI_cm": lower_bound,
        "upper_95PI_cm": upper_bound
    })

    min_year_fut = int(future_years.min())
    max_year_fut = int(future_years.max())

    start_year, end_year = st.slider(
        "Select year range for export",
        min_value=min_year_fut,
        max_value=max_year_fut,
        value=(min_year_fut, max_year_fut),
        step=1
    )

    mask = (
        (future_full_df["year"] >= start_year) &
        (future_full_df["year"] <= end_year)
    )
    future_filtered_df = future_full_df.loc[mask].reset_index(drop=True)

    st.markdown("You can edit the table below before downloading.")

    edited_df = st.data_editor(
        future_filtered_df,
        num_rows="dynamic",
        key="future_climate_tuned_chrono_editor"
    )

    csv_data = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download edited tuned climate-driven predictions as CSV",
        data=csv_data,
        file_name="venice_future_climate_tuned_predictions.csv",
        mime="text/csv"
    )