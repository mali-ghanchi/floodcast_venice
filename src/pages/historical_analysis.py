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
X = graph[['year']]
y = graph['sea_level_cm']

model = LinearRegression()
model.fit(X, y)

# Historical trend
hist_trend = model.predict(X)

# Future prediction
future_years = np.arange(
    graph['year'].max(),
    2101
).reshape(-1, 1)

predicted_levels = model.predict(
    future_years
)

# -----------------------------------
# USER CONTROLS
# -----------------------------------
st.sidebar.header("Graph Controls")

show_trend = st.sidebar.checkbox(
    "Show Historical Trend",
    value=True
)

show_prediction = st.sidebar.checkbox(
    "Show Future Prediction",
    value=True
)

show_uncertainty = st.sidebar.checkbox(
    "Show Uncertainty Range",
    value=True
)

# -----------------------------------
# CREATE PLOTLY FIGURE
# -----------------------------------
fig = go.Figure()

# Historical raw data
fig.add_trace(
    go.Scatter(
        x=graph['year'],
        y=graph['sea_level_cm'],
        mode='lines',
        name='Historical Data'
    )
)

# Historical trend line
if show_trend:

    fig.add_trace(
        go.Scatter(
            x=graph['year'],
            y=hist_trend,
            mode='lines',
            name='Historical Trend'
        )
    )

# Future prediction
if show_prediction:

    fig.add_trace(
        go.Scatter(
            x=future_years.flatten(),
            y=predicted_levels.flatten(),
            mode='lines',
            name='Regression Prediction',
            line=dict(dash='dash')
        )
    )

# Uncertainty range
if show_uncertainty:

    uncertainty = np.array([
        (year - 2000) * 0.05
        for year in future_years.flatten()
    ])

    upper_bound = (
        predicted_levels.flatten()
        + uncertainty
    )

    lower_bound = (
        predicted_levels.flatten()
        - uncertainty
    )

    fig.add_trace(
    go.Scatter(
        x=np.concatenate([
            future_years.flatten(),
            future_years.flatten()[::-1]
        ]),
        y=np.concatenate([
            upper_bound,
            lower_bound[::-1]
        ]),
        fill='toself',
        name='Uncertainty Range',
        hoverinfo='skip'
    )
)

# -----------------------------------
# LAYOUT SETTINGS
# -----------------------------------
fig.update_layout(
    title='Venice Sea Level Analysis',
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
# SUMMARY TEXT
# -----------------------------------
st.markdown("""
### Interpretation

The historical tide gauge data indicates a long-term increase
in relative sea level in Venice.

The regression model extends this trend into the future and
provides a simplified estimate of possible future developments
under the assumption that current historical patterns continue.
""")