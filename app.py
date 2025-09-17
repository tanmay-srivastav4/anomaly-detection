import streamlit as st
import joblib
from geopy.distance import geodesic

model = joblib.load('anomaly_detection_model.pkl')
scaler = joblib.load('feature_scaler.pkl')

def is_outside_safe_zone(lat, lon):
    return 1 if geodesic((lat, lon), (27.3389, 88.6065)).km > 20 else 0

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

st.title("SurakshaTrack - Realtime Anomaly Prediction")

latitude = st.number_input("Latitude", value=27.3389)
longitude = st.number_input("Longitude", value=88.6065)
speed = st.number_input("Speed (km/h)", value=10.0)
time_spent_in_zone = 300  # static for now
distance_to_zone_center = geodesic((latitude, longitude), (27.3389, 88.6065)).meters

near_dangerous_area = is_in_dangerous_area(latitude, longitude)
outside_safe_zone = is_outside_safe_zone(latitude, longitude)

features = [[speed, time_spent_in_zone, distance_to_zone_center, near_dangerous_area, outside_safe_zone]]
features_scaled = scaler.transform(features)
anomaly = model.predict(features_scaled)[0]
predicted_sos = 1 if anomaly == -1 or near_dangerous_area == 1 or outside_safe_zone == 1 else 0

st.write(f"Distance to Zone Center: {distance_to_zone_center:.2f} m")
st.write(f"Near Dangerous Area: {'Yes' if near_dangerous_area else 'No'}")
st.write(f"Outside Safe Zone: {'Yes' if outside_safe_zone else 'No'}")

if predicted_sos == 1:
    st.error("🚨 ALERT: Anomaly or breach detected!")
else:
    st.success("✅ Everything normal. Tourist is safe.")
