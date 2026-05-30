import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title("🌍 Climate Scenarios")

st.markdown("""
This section explores possible future sea level developments
under different climate emission pathways.

The projections shown below are based on published climate
scenario data and illustrate how different greenhouse gas
emission trajectories may influence future sea level rise.
""")

# -----------------------------------
# LOAD DATA
# -----------------------------------

df = pd.read_excel(
    "data/venice_sea_level comparison.xlsx"
)

years = df["Unnamed: 1"]

# Convert metres -> centimetres
rcp26 = df["rcp2.6_95"] * 100

rcp85 = df["rcp8.5_50"] * 100

high_end = df["high-end"] * 100

# -----------------------------------
# METRIC CARDS
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Best Case",
        value="RCP 2.6"
    )

with col2:
    st.metric(
        label="Median Projection",
        value="RCP 8.5"
    )

with col3:
    st.metric(
        label="Extreme Scenario",
        value="High-End"
    )

# -----------------------------------
# SIDEBAR CONTROLS
# -----------------------------------

st.sidebar.header("Scenario Controls")

show_rcp26 = st.sidebar.checkbox(
    "Show RCP 2.6",
    value=True
)

show_rcp85 = st.sidebar.checkbox(
    "Show RCP 8.5",
    value=True
)


show_high_end = st.sidebar.checkbox(
    "Show High-End Scenario",
    value=True
)

# -----------------------------------
# CREATE GRAPH
# -----------------------------------

fig = go.Figure()

# RCP 2.6
if show_rcp26:
    fig.add_trace(
        go.Scatter(
            x=years,
            y=rcp26,
            mode="lines",
            name="RCP 2.6"
        )
    )

# RCP 8.5 Median
if show_rcp85:
    fig.add_trace(
        go.Scatter(
            x=years,
            y=rcp85,
            mode="lines",
            name="RCP 8.5"
        )
    )

# High-End Scenario
if show_high_end:
    fig.add_trace(
        go.Scatter(
            x=years,
            y=high_end,
            mode="lines",
            name="High-End Scenario"
        )
    )

# -----------------------------------
# GRAPH LAYOUT
# -----------------------------------

fig.update_layout(
    title="Projected Sea Level Rise Scenarios for Venice",
    xaxis_title="Year",
    yaxis_title="Relative Sea Level Rise (cm)",
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
# INTERPRETATION
# -----------------------------------

st.markdown("""
### Interpretation

The graph illustrates possible future sea level developments
under different climate pathways.

- **RCP 2.6** represents strong climate mitigation and lower emissions.
- **RCP 8.5** represents a higher-emissions future.
- **High-End Scenario** represents an extreme projection used for long-term risk assessment.

For Venice, higher sea levels increase the frequency and severity
of flooding events, potentially affecting infrastructure, tourism,
heritage sites, and residential areas.
""")