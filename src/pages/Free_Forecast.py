import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests


# -------------------------------------------------
# 4. SHORT-TERM FORECAST FROM WORLDTIDES API
# -------------------------------------------------
st.markdown("### Short-term tide forecast for Venice)")

@st.cache_data
def fetch_venice_tides_worldtides(days: int = 3) -> pd.DataFrame:
    """
    Call the WorldTides API and return a DataFrame with datetime and water_level_cm
    for Venice for the next 'days' days.
    """
    api_key = st.secrets["worldtides"]["api_key"]

    base_url = "https://www.worldtides.info/api/v3"
    params = {
        "key": api_key,
        "lat": 45.44,    # Venice approx
        "lon": 12.33,
        "heights": "",   # request tide heights
        "date": "today",
        "days": days
    }

    r = requests.get(base_url, params=params, timeout=30)  # more patient timeout
    r.raise_for_status()
    data = r.json()

    heights = data.get("heights", [])
    if not heights:
        raise ValueError("No 'heights' field in API response.")

    df_h = pd.DataFrame(heights)
    df_h["datetime"] = pd.to_datetime(df_h["dt"], unit="s")
    df_h["water_level_cm"] = df_h["height"] * 100.0  # metres → cm

    return df_h[["datetime", "water_level_cm"]]


days = st.slider("Days ahead for tide forecast", min_value=1, max_value=7, value=3)

try:
    venice_api_df = fetch_venice_tides_worldtides(days=days)


    st.dataframe(venice_api_df.head())

    fig_api = go.Figure()
    fig_api.add_trace(go.Scatter(
        x=venice_api_df["datetime"],
        y=venice_api_df["water_level_cm"],
        name="WorldTides forecast (cm)",
        mode="lines",
        line=dict(color="red")
    ))

    fig_api.update_layout(
        title="Short-term tide forecast for Venice",
        xaxis_title="Time",
        yaxis_title="Water level (cm)",
        hovermode="x unified"
    )

    st.plotly_chart(fig_api, use_container_width=True)

    st.markdown("""
The forecast shows **short-term, high-frequency tide levels**
for the next few days, while the SARIMA model above focuses on the
**long-term monthly trend up to around year 2100**.
""")

except Exception as e:
    st.error(f"Error while calling WorldTides: {e}")
    st.info("If this persists, check `.streamlit/secrets.toml`, your WorldTides API key, or your network connection.")