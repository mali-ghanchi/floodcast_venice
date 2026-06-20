import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.title("📈 Historical Analysis")

st.markdown("""
This page analyses historical tide gauge measurements in Venice
and applies linear regression to estimate future sea level trends.
""")

# -----------------------------------
# METRIC CARDS
# -----------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Dataset Range",
        value="1909–2000"
    )

with col2:
    st.metric(
        label="Prediction Horizon",
        value="2100"
    )

with col3:
    st.metric(
        label="Estimated Trend",
        value="+2.3 mm/year"
    )

with col4:
    st.metric(
        label="Flood Risk",
        value="High"
    )

# -----------------------------------
# LOAD DATA
# -----------------------------------
graph = pd.read_csv(
    'data/venice data - historical.txt',
    sep=';',
    header=None
)

graph.columns = [
    'year',
    'sea_level_mm',
    'flag',
    'quality'
]

# Remove missing values
graph = graph[
    graph['sea_level_mm'] != -99999
]

# Convert mm → cm
graph['sea_level_cm'] = (
    graph['sea_level_mm'] / 10
)

# -----------------------------------
# MACHINE LEARNING MODEL
# -----------------------------------
X = graph[['year']].values  # (n, 1)
y = graph['sea_level_cm'].values

model = LinearRegression()
model.fit(X, y)

# Historical trend (fitted values)
hist_trend = model.predict(X)

# -----------------------------------
# STATISTICAL UNCERTAINTY (PREDICTION INTERVAL)
# -----------------------------------
# Residuals
residuals = y - hist_trend
n = len(X)
x = X.flatten()

# For simple linear regression: 2 parameters (slope + intercept)
dof = max(n - 2, 1)

# Residual standard error (noise level)
s = np.sqrt(np.sum(residuals**2) / dof)

# Statistics of the predictor (year)
x_mean = x.mean()
Sxx = np.sum((x - x_mean) ** 2)

def prediction_std(x0):
    """
    Standard deviation of the prediction interval for a new observation
    at year x0 (simple linear regression).

    Formula:
    s * sqrt(1 + 1/n + (x0 - x̄)^2 / Sxx)
    """
    return s * np.sqrt(1 + 1/n + (x0 - x_mean) ** 2 / Sxx)

# -----------------------------------
# FUTURE PREDICTION
# -----------------------------------
future_years = np.arange(
    graph['year'].max(),
    2101
).reshape(-1, 1)

predicted_levels = model.predict(future_years)

# Compute a 95% prediction interval for future years
z = 1.96  # approx 95% interval
future_years_flat = future_years.flatten()

std_pred = np.array([prediction_std(year) for year in future_years_flat])

upper_bound = predicted_levels.flatten() + z * std_pred
lower_bound = predicted_levels.flatten() - z * std_pred

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

# Store current mode
show_future = st.session_state.show_future

# -----------------------------------
# CREATE PLOTLY FIGURE
# -----------------------------------

fig = go.Figure()

# -----------------------------------
# ALWAYS SHOW HISTORICAL DATA
# -----------------------------------

fig.add_trace(
    go.Scatter(
        x=graph['year'],
        y=graph['sea_level_cm'],
        mode='lines',
        name='Historical Data'
    )
)

# -----------------------------------
# SHOW FUTURE ELEMENTS ONLY
# AFTER BUTTON CLICK
# -----------------------------------

if show_future:

    # Historical trend line (fitted regression)
    fig.add_trace(
        go.Scatter(
            x=graph['year'],
            y=hist_trend,
            mode='lines',
            name='Historical Trend (Linear Fit)',
            line=dict(color='orange')
        )
    )

    # Future prediction
    fig.add_trace(
        go.Scatter(
            x=future_years_flat,
            y=predicted_levels.flatten(),
            mode='lines',
            name='Regression Prediction',
            line=dict(color='orange', dash='dash')
        )
    )

    # Statistically derived prediction interval
    fig.add_trace(
        go.Scatter(
            x=np.concatenate([
                future_years_flat,
                future_years_flat[::-1]
            ]),
            y=np.concatenate([
                upper_bound,
                lower_bound[::-1]
            ]),
            fill='toself',
            name='Prediction Interval (~95%)',
            hoverinfo='skip',
            line=dict(color='rgba(255, 165, 0, 0)'),  # no border
            fillcolor='rgba(255, 165, 0, 0.2)'        # light orange
        )
    )

# -----------------------------------
# LAYOUT SETTINGS
# -----------------------------------

fig.update_layout(
    title='Venice Sea Level Analysis (Historical + Linear Projection)',
    xaxis_title='Year',
    yaxis_title='Sea Level (cm)',
    hovermode='x unified'
)

# -----------------------------------
# DISPLAY GRAPH
# -----------------------------------

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------------
# INTERPRETATION
# -----------------------------------

st.markdown("""
### Historical Interpretation

The tide gauge record describes **relative sea level** in Venice – that is,
the height of the sea surface **relative to the land** at the gauge.

This relative signal combines:

- **Global sea-level rise** (thermal expansion of the oceans, melting glaciers and ice sheets), and  
- **Local vertical land motion**, in particular **land subsidence** (the city and lagoon slowly sinking).

A positive long-term trend in the tide gauge therefore means that the **water level
is rising relative to the land**, either because the ocean is rising, the land is sinking,
or (in reality) a combination of both.

Over the period 1909–2000, the historical data show a clear upward trend in relative
sea level in Venice. This long-term rise increases the background likelihood of
flooding, especially during high-tide events such as *Acqua Alta*.
""")

# -----------------------------------
# FUTURE INTERPRETATION
# -----------------------------------

if show_future:

    st.markdown("""
    ### Future Projection

    The linear regression model uses only **time (year)** to describe the observed
    rise in relative sea level. Extrapolating this straight-line trend to 2100 gives
    a **first-order projection** of how sea level could evolve if the historical
    behaviour simply continues.

    The shaded band around the projection is a **statistical prediction interval**
    derived from the regression residuals. It represents an approximate range within
    which individual future observations might fall, assuming that:

    - the linear relationship between year and sea level remains valid, and  
    - the size of the year-to-year noise is similar to the past.

    The interval widens with time because predictions far beyond the historical
    data range become increasingly uncertain. This illustrates that while a
    linear trend provides a useful baseline, long-term planning for Venice should
    also consider more complex physical scenarios (e.g. accelerated ice-sheet
    melt and changing subsidence rates).
    """)

    # -----------------------------------
# FUTURE TABLE + EXPORT (ONLY IF FUTURE IS SHOWN)
# -----------------------------------

if show_future:

    st.markdown("### Future prediction data")

    # Full future results table
    future_full_df = pd.DataFrame({
        "year": future_years_flat,
        "predicted_sea_level_cm": predicted_levels.flatten(),
        "lower_95PI_cm": lower_bound,
        "upper_95PI_cm": upper_bound
    })

    # Year range selector
    min_year = int(future_years_flat.min())
    max_year = int(future_years_flat.max())

    start_year, end_year = st.slider(
        "Select year range for export",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )

    # Filter by selected range
    mask = (future_full_df["year"] >= start_year) & (future_full_df["year"] <= end_year)
    future_filtered_df = future_full_df.loc[mask].reset_index(drop=True)

    st.markdown(
        "You can edit the table below (delete rows and change values) "
        "before downloading."
    )

    # Editable table
    edited_df = st.data_editor(
        future_filtered_df,
        num_rows="dynamic",   # allows adding/removing rows
        key="future_editor"
    )

    # Download as CSV
    csv_data = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download edited future predictions as CSV",
        data=csv_data,
        file_name="venice_future_linear_predictions.csv",
        mime="text/csv"
    )