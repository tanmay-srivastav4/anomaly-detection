import streamlit as st
import pandas as pd
import time
import numpy as np
from geopy.distance import geodesic
import joblib

# Load model and scaler
model = joblib.load('anomaly_detection_model.pkl')
scaler = joblib.load('feature_scaler.pkl')

# Sample demo data simulating tourist movement
data = [
    {'latitude': 27.3389, 'longitude': 88.6065, 'timestamp': '2025-09-17 10:00:00', 'speed': 5, 'zone_id': 1},
    {'latitude': 27.3400, 'longitude': 88.6100, 'timestamp': '2025-09-17 10:05:00', 'speed': 4, 'zone_id': 1},
    {'latitude': 27.3450, 'longitude': 88.6200, 'timestamp': '2025-09-17 10:10:00', 'speed': 3, 'zone_id': 1},
    {'latitude': 27.4120, 'longitude': 88.9570, 'timestamp': '2025-09-17 10:15:00', 'speed': 2, 'zone_id': 2},
]

df = pd.DataFrame(data)

def is_outside_safe_zone(lat, lon):
    center = (27.3389, 88.6065)
    return 1 if geodesic((lat, lon), center).km > 20 else 0

def is_in_dangerous_area(lat, lon):
    dangerous_areas = [
        {'latitude': 27.9475, 'longitude': 88.3315},
        {'latitude': 27.2200, 'longitude': 88.6020},
        {'latitude': 27.3450, 'longitude': 88.8790},
        {'latitude': 27.4205, 'longitude': 88.9314},
        {'latitude': 27.4120, 'longitude': 88.9570},
    ]
    current_loc = (lat, lon)
    for area in dangerous_areas:
        if geodesic(current_loc, (area['latitude'], area['longitude'])).km <= 0.5:
            return 1
    return 0

st.title("🌐 Real-Time Tourist Movement & SOS Alert Simulation")

for i in range(len(df)):
    row = df.iloc[i]
    
    # Time spent in zone simulation
    time_spent_in_zone = 300  # Static for demo purpose
    
    # Distance to zone center
    distance_to_zone_center = geodesic(
        (row['latitude'], row['longitude']),
        (27.3389, 88.6065)
    ).meters
    
    near_dangerous_area = is_in_dangerous_area(row['latitude'], row['longitude'])
    outside_safe_zone = is_outside_safe_zone(row['latitude'], row['longitude'])
    
    features = [[
        row['speed'],
        time_spent_in_zone,
        distance_to_zone_center,
        near_dangerous_area,
        outside_safe_zone
    ]]
    
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]  # -1 = anomaly, 1 = normal
    
    sos_triggered = (prediction == -1) or (near_dangerous_area == 1) or (outside_safe_zone == 1)
    
    st.subheader(f"Step {i+1}")
    st.write(f"📍 Latitude: {row['latitude']}, Longitude: {row['longitude']}")
    st.write(f"⏱️ Timestamp: {row['timestamp']}")
    st.write(f"⚡ Speed: {row['speed']} km/h")
    st.map(pd.DataFrame({'lat': [row['latitude']], 'lon': [row['longitude']]}))
    
    if sos_triggered:
        st.error("🚨 SOS ALERT! Tourist entered a dangerous zone!")
    else:
        st.success("✅ Safe zone - no anomaly detected.")
    
    time.sleep(3)  # Simulates real-time movement delay
    st.write("---")
