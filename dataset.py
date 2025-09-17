# Example Center: Gangtok, Sikkim
center_lat = 27.33
center_long = 88.62

import random
from geopy.distance import distance
from geopy.point import Point

def generate_random_point(center_lat, center_long, max_radius_meters=20000):
    random_distance = random.uniform(0, max_radius_meters)
    random_bearing = random.uniform(0, 360)
    center_point = Point(center_lat, center_long)
    destination = distance(meters=random_distance).destination(point=center_point, bearing=random_bearing)
    return destination.latitude, destination.longitude

from geopy.distance import geodesic

def is_within_geofence(lat, lon, center_lat, center_long, max_radius_meters=20000):
    current_pos = (lat, lon)
    center_pos = (center_lat, center_long)
    distance_meters = geodesic(center_pos, current_pos).meters
    return distance_meters <= max_radius_meters  # True if inside geofence


import pandas as pd
from datetime import datetime, timedelta

num_points = 500  # Number of data points
base_time = datetime.now()
data = []

for i in range(num_points):
    lat, lon = generate_random_point(center_lat, center_long)
    timestamp = base_time + timedelta(minutes=5 * i)
    speed = round(random.uniform(0.1, 6.0), 2)
    zone_id = random.randint(1, 5)
    sos = 1 if random.random() < 0.02 else 0

    data.append([lat, lon, timestamp.strftime('%Y-%m-%d %H:%M:%S'), speed, zone_id, sos])

df = pd.DataFrame(data, columns=['latitude', 'longitude', 'timestamp', 'speed', 'zone_id', 'SOS'])
df.to_csv('synthetic_tourist_movements_sikkim.csv', index=False)
print("Synthetic dataset generated.")


# Example: Check if first data point is inside the geofence
lat = df.iloc[0]['latitude']
lon = df.iloc[0]['longitude']
inside = is_within_geofence(lat, lon, center_lat, center_long)

print(f"First point geofence status: {'Inside' if inside else 'Outside'}")


import folium

m = folium.Map(location=[center_lat, center_long], zoom_start=10)

# Geofence circle
folium.Circle(
    location=[center_lat, center_long],
    radius=20000,
    color='blue',
    fill=True,
    fill_opacity=0.2
).add_to(m)

# Plot sample points
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=2,
        color='green' if is_within_geofence(row['latitude'], row['longitude'], center_lat, center_long) else 'red'
    ).add_to(m)

m.save('sikkim_geofence_map.html')
print("Geofence map saved as sikkim_geofence_map.html")
