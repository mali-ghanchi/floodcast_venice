import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
st.title("🌊 FloodCast Venice - Water you thinking?")
st.subheader("Sea Level Prediction & Climate Scenario Dashboard")

# -----------------------------
# LOAD HISTORICAL DATA
# -----------------------------
graph = pd.read_csv(
    'data/venice data - historical.txt',
    sep=';',
    header=None
)

graph.columns = ['year', 'sea_level_mm', 'flag', 'quality']

graph = graph[graph['sea_level_mm'] != -99999]

graph['sea_level_cm'] = graph['sea_level_mm'] / 10

# -----------------------------
# MACHINE LEARNING MODEL
# -----------------------------
X = graph[['year']]
y = graph['sea_level_cm']

model = LinearRegression()
model.fit(X, y)

# Historical trend
hist_trend = model.predict(X)

# Future prediction
future_years = pd.DataFrame(
    np.arange(graph['year'].max() + 1, 2101),
    columns=['year']
)

predicted_levels = model.predict(future_years)

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
st.sidebar.header("Graph Controls")

show_historical = st.sidebar.checkbox(
    "Show Historical Data",
    value=True
)

show_regression = st.sidebar.checkbox(
    "Show Regression Prediction",
    value=True
)

show_uncertainty = st.sidebar.checkbox(
    "Show Uncertainty Range",
    value=True
)

# -----------------------------
# CREATE GRAPH
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 5))

# Historical Data
if show_historical:
    ax.plot(
        graph['year'],
        graph['sea_level_cm'],
        label='Historical Data'
    )

# Historical Trend
ax.plot(
    graph['year'],
    hist_trend,
    linewidth=2,
    label='Historical Trend'
)

# Future Prediction
if show_regression:
    ax.plot(
        future_years,
        predicted_levels,
        linestyle='--',
        linewidth=2,
        label='Regression Prediction'
    )

# Uncertainty Range
if show_uncertainty:

    uncertainty = np.array([
        (year - 2000) * 0.05
        for year in range(
            int(future_years.min()),
            2101
        )
    ])

    upper_bound = predicted_levels.flatten() + uncertainty
    lower_bound = predicted_levels.flatten() - uncertainty

    ax.fill_between(
        future_years.flatten(),
        lower_bound,
        upper_bound,
        alpha=0.2,
        label='Uncertainty Range'
    )

# Labels
ax.set_title('Venice Sea Level Prediction')
ax.set_xlabel('Year')
ax.set_ylabel('Sea Level (cm)')

ax.legend()

# -----------------------------
# DISPLAY GRAPH
# -----------------------------
st.pyplot(fig)