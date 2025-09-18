import streamlit as st
import pandas as pd
import time
import numpy as np
from geopy.distance import geodesic
import pydeck as pdk

# -----------------------------
# Safe zone config
# -----------------------------
SAFE_CENTER = (27.3389, 88.6065)  # (lat, lon)
SAFE_RADIUS_M = 20000  # 20 km in meters

dangerous_areas = [
    {'latitude': 27.9475, 'longitude': 88.3315},
    {'latitude': 27.2200, 'longitude': 88.6020},
    {'latitude': 27.3450, 'longitude': 88.8790},
    {'latitude': 27.4205, 'longitude': 88.9314},
    {'latitude': 27.4120, 'longitude': 88.9570},
]

# -----------------------------
# Functions
# -----------------------------
def is_outside_safe_zone(lat, lon):
    return 1 if geodesic((lat, lon), SAFE_CENTER).m > SAFE_RADIUS_M else 0

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🌐 Real-Time Tourist Movement & Geofence SOS Alert")

trail = []
lat, lon = SAFE_CENTER  # Start from safe zone center

for step in range(25):  # Move for 25 steps
    # Tourist gradually moves northeast (0.01 deg per step)
    lat += 0.01
    lon += 0.01
    trail.append([lon, lat])  # pydeck needs (lon, lat)

    # Check safe zone status
    outside_safe_zone = is_outside_safe_zone(lat, lon)

    # Trail path
    path_layer = pdk.Layer(
        "PathLayer",
        data=[{"path": trail}],
        get_path="path",
        get_color=[0, 100, 255],
        width_scale=3,
        width_min_pixels=2,
    )

    # Current position marker
    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame({"lon": [lon], "lat": [lat]}),
        get_position='[lon, lat]',
        get_color='[255, 0, 0]',
        get_radius=300,
    )

    # Dangerous areas
    danger_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame(dangerous_areas),
        get_position='[longitude, latitude]',
        get_color='[255, 50, 50]',
        get_radius=500,
    )

    # Safe zone geofence (20 km circle)
    geofence_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame({"lon": [SAFE_CENTER[1]], "lat": [SAFE_CENTER[0]]}),
        get_position='[lon, lat]',
        get_color='[0, 255, 0, 40]' if not outside_safe_zone else '[255, 0, 0, 60]',  
        get_radius=SAFE_RADIUS_M,
    )

    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=9,
        pitch=0
    )

    st.pydeck_chart(pdk.Deck(
        layers=[path_layer, point_layer, danger_layer, geofence_layer],
        initial_view_state=view_state
    ))

    # Alerts
    if outside_safe_zone:
        st.error("🚨 SOS ALERT! Tourist stepped OUTSIDE the safe zone!")
        break  # Stop movement immediately once anomaly is triggered
    else:
        st.success("✅ Tourist is SAFE inside the zone.")

    time.sleep(2)  # Simulate real-time movement
    st.write("---")
