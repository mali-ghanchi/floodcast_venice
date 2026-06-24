import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.title("📈 Historical Analysis")

st.markdown("""
This page analyses historical tide gauge measurements in Venice
and applies linear regression to estimate future sea level trends.
""")

# -----------------------------------
# LOAD DATA
# -----------------------------------
graph = pd.read_csv(
    "data/venice data - historical.txt",
    sep=";",
    header=None
)

graph.columns = [
    "year",
    "sea_level_mm",
    "flag",
    "quality"
]

# Remove missing values
graph = graph[graph["sea_level_mm"] != -99999].copy()

# Convert mm → cm
graph["sea_level_cm"] = graph["sea_level_mm"] / 10
graph["year"] = graph["year"].astype(int)
graph = graph.sort_values("year")

# -----------------------------------
# MACHINE LEARNING MODEL
# -----------------------------------
X = graph[["year"]].values
y = graph["sea_level_cm"].values

model = LinearRegression()
model.fit(X, y)

# Historical trend (fitted values)
hist_trend = model.predict(X)

# -----------------------------------
# MODEL METRICS (CHRONOLOGICAL TRAIN/TEST SPLIT)
# -----------------------------------
n_obs = len(graph)
n_test = max(5, int(0.2 * n_obs))

X_train = X[:-n_test]
X_test = X[-n_test:]
y_train = y[:-n_test]
y_test = y[-n_test:]

model_eval = LinearRegression()
model_eval.fit(X_train, y_train)
y_test_pred = model_eval.predict(X_test)

mae_simple = mean_absolute_error(y_test, y_test_pred)
rmse_simple = np.sqrt(mean_squared_error(y_test, y_test_pred))
r_simple = np.corrcoef(y_test, y_test_pred)[0, 1] if len(y_test) > 1 else np.nan

st.markdown(f"""
### Historical Fit

- Feature used: year
- Pearson R: **{r_simple:.4f}**
- MAE (Mean Absolute Error): **{mae_simple:.2f} cm**
- RMSE (Root Mean Squared Error): **{rmse_simple:.2f} cm**
""")

# -----------------------------------
# STATISTICAL UNCERTAINTY (PREDICTION INTERVAL)
# -----------------------------------
residuals = y - hist_trend
n = len(X)
x = X.flatten()

dof = max(n - 2, 1)
s = np.sqrt(np.sum(residuals**2) / dof)

x_mean = x.mean()
Sxx = np.sum((x - x_mean) ** 2)

def prediction_std(x0: float) -> float:
    return s * np.sqrt(1 + 1 / n + (x0 - x_mean) ** 2 / Sxx)

# -----------------------------------
# FUTURE PREDICTION
# -----------------------------------
future_years = np.arange(
    graph["year"].max(),
    2101
).reshape(-1, 1)

predicted_levels = model.predict(future_years)

z = 1.96
future_years_flat = future_years.flatten()

std_pred = np.array([prediction_std(year) for year in future_years_flat])

upper_bound = predicted_levels.flatten() + z * std_pred
lower_bound = predicted_levels.flatten() - z * std_pred

# -----------------------------------
# LOAD NASA DATA
# -----------------------------------
@st.cache_data
def load_nasa_data():
    file_path = "data/ipcc_ar6_sea_level_projection_psmsl_id_39.xlsx"

    nasa_raw = pd.read_excel(file_path, sheet_name="Total", header=None)
    nasa_raw.columns = nasa_raw.iloc[0]
    nasa = nasa_raw.iloc[1:].copy()
    nasa.columns = [str(col).strip() for col in nasa.columns]

    meta_cols = ["psmsl_id", "process", "confidence", "scenario", "quantile"]
    for col in meta_cols:
        if col in nasa.columns:
            nasa[col] = nasa[col].astype(str).str.strip()

    nasa["quantile"] = pd.to_numeric(nasa["quantile"], errors="coerce")
    return nasa

nasa = load_nasa_data()

available_scenarios = sorted(nasa["scenario"].dropna().unique())
scenario = st.selectbox("Choose NASA scenario", available_scenarios)

nasa_sel = nasa[
    (nasa["process"].str.lower() == "total") &
    (nasa["scenario"] == scenario) &
    (nasa["quantile"] == 50)
].copy()

year_cols = []
for col in nasa_sel.columns:
    col_str = str(col).replace(".0", "").strip()
    if col_str.isdigit():
        year_cols.append(col)

nasa_long = nasa_sel.melt(
    id_vars=[c for c in ["psmsl_id", "process", "confidence", "scenario", "quantile"] if c in nasa_sel.columns],
    value_vars=year_cols,
    var_name="year",
    value_name="nasa_projection_m"
)

nasa_long["year"] = (
    nasa_long["year"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .astype(int)
)
nasa_long["nasa_projection_m"] = pd.to_numeric(nasa_long["nasa_projection_m"], errors="coerce")
nasa_long = nasa_long.dropna(subset=["nasa_projection_m"])

# Anchor NASA projection to Venice at January 2020
if 2020 in graph["year"].values:
    venice_2020_cm = graph.loc[graph["year"] == 2020, "sea_level_cm"].iloc[0]
else:
    nearest_idx = (graph["year"] - 2020).abs().idxmin()
    venice_2020_cm = graph.loc[nearest_idx, "sea_level_cm"]

nasa_long["nasa_cm"] = venice_2020_cm + nasa_long["nasa_projection_m"] * 100
nasa_long = nasa_long[nasa_long["year"] <= 2100].copy()

# -----------------------------------
# SESSION STATE
# -----------------------------------
if "show_future" not in st.session_state:
    st.session_state.show_future = False

# -----------------------------------
# BUTTONS
# -----------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("📈 Explore Future Prediction"):
        st.session_state.show_future = True

with col2:
    if st.button("📉 Return to Historical"):
        st.session_state.show_future = False

show_future = st.session_state.show_future

# -----------------------------------
# CREATE PLOTLY FIGURE
# -----------------------------------
fig = go.Figure()

# Always show historical data
fig.add_trace(
    go.Scatter(
        x=graph["year"],
        y=graph["sea_level_cm"],
        mode="lines",
        name="Historical Data",
        line=dict(color="steelblue")
    )
)

# -----------------------------------
# SHOW FUTURE ELEMENTS ONLY AFTER BUTTON CLICK
# -----------------------------------
if show_future:
    fig.add_trace(
        go.Scatter(
            x=graph["year"],
            y=hist_trend,
            mode="lines",
            name="Historical Trend (Linear Fit)",
            line=dict(color="orange")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=future_years_flat,
            y=predicted_levels.flatten(),
            mode="lines",
            name="Regression Prediction",
            line=dict(color="orange", dash="dash")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=np.concatenate([future_years_flat, future_years_flat[::-1]]),
            y=np.concatenate([upper_bound, lower_bound[::-1]]),
            fill="toself",
            name="Prediction Interval (~95%)",
            hoverinfo="skip",
            line=dict(color="rgba(255, 165, 0, 0)"),
            fillcolor="rgba(255, 165, 0, 0.2)"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=nasa_long["year"],
            y=nasa_long["nasa_cm"],
            mode="lines+markers",
            name=f"NASA {scenario} median",
            line=dict(color="crimson", width=3)
        )
    )

# -----------------------------------
# LAYOUT SETTINGS
# -----------------------------------
fig.update_layout(
    title="Venice Sea Level Analysis (Historical + Linear Projection + NASA)",
    xaxis_title="Year",
    yaxis_title="Sea Level (cm)",
    hovermode="x unified"
)

# -----------------------------------
# DISPLAY GRAPH
# -----------------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# INTERPRETATION (HISTORICAL)
# -----------------------------------
st.markdown("""
### Historical Interpretation

The tide gauge record describes **relative sea level** in Venice – that is,
the height of the sea surface **relative to the land** at the gauge.

This relative signal combines:

- **Global sea-level rise** (thermal expansion of the oceans, melting glaciers and ice sheets),  
- **Local vertical land motion**, in particular **land subsidence**.

A positive long-term trend in the tide gauge therefore means that the **water level
is rising relative to the land**, either because the ocean is rising, the land is sinking,
or both.

Over the historical record, the data show a clear upward trend in relative
sea level in Venice. This long-term rise increases the background likelihood of
flooding, especially during high-tide events such as *Acqua Alta*.
""")

# -----------------------------------
# INTERPRETATION (FUTURE)
# -----------------------------------
if show_future:
    st.markdown(f"""
    ### Future Projection

    The linear regression model uses only **time (year)** to describe the observed
    rise in relative sea level. Extrapolating this straight-line trend to **January 2100**
    gives a simple baseline projection.

    The shaded band is an approximate **95% prediction interval** based on the regression residuals.

    The **NASA {scenario} median** curve is plotted for comparison. NASA's projection is
    scenario-based and physically informed, while the regression model is a purely statistical
    extrapolation of Venice's historical trend.
    """)

    # -----------------------------------
    # RESIDUAL PLOT
    # -----------------------------------
    st.markdown("### Residual analysis")

    fig_res = go.Figure()
    fig_res.add_trace(go.Scatter(
        x=graph["year"],
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

    # -----------------------------------
    # FUTURE TABLE + EXPORT
    # -----------------------------------
    st.markdown("### Future prediction data")

    nasa_interp = np.interp(
        future_years_flat,
        nasa_long["year"].values,
        nasa_long["nasa_cm"].values
    )

    future_full_df = pd.DataFrame({
        "year": future_years_flat,
        "predicted_sea_level_cm": predicted_levels.flatten(),
        "lower_95PI_cm": lower_bound,
        "upper_95PI_cm": upper_bound,
        f"nasa_{scenario}_cm": nasa_interp
    })

    min_year = int(future_years_flat.min())
    max_year = int(future_years_flat.max())

    start_year, end_year = st.slider(
        "Select year range for export",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )

    mask = (
        (future_full_df["year"] >= start_year) &
        (future_full_df["year"] <= end_year)
    )
    future_filtered_df = future_full_df.loc[mask].reset_index(drop=True)

    st.markdown(
        "You can edit the table below before downloading."
    )

    edited_df = st.data_editor(
        future_filtered_df,
        num_rows="dynamic",
        key="future_editor"
    )

    csv_data = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download edited future predictions as CSV",
        data=csv_data,
        file_name="venice_future_linear_predictions_with_nasa.csv",
        mime="text/csv"
    )