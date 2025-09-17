import folium
import webbrowser

# Center of map (Gangtok or central Sikkim)
center_lat = 27.3389
center_lon = 88.6065

m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Safe Geofence (20 km radius)
folium.Circle(
    location=[center_lat, center_lon],
    radius=20000,  # 20 km in meters
    color='green',
    fill=True,
    fill_opacity=0.2,
    popup='Safe Zone: 20 km Radius'
).add_to(m)

# List of dangerous areas (with additional entries)
dangerous_areas = [
    {'name': 'South Lhonak Lake', 'latitude': 27.9475, 'longitude': 88.3315},
    {'name': 'Yangthang, Upper Rimbi', 'latitude': 27.2200, 'longitude': 88.6020},
    {'name': 'Zuluk Pass', 'latitude': 27.3450, 'longitude': 88.8790},
    {'name': 'Nathula Pass', 'latitude': 27.4205, 'longitude': 88.9314},
    {'name': 'Kupup Lake', 'latitude': 27.4120, 'longitude': 88.9570},
    # Add more if needed
]

# Plot dangerous areas
for area in dangerous_areas:
    folium.Marker(
        location=[area['latitude'], area['longitude']],
        icon=folium.Icon(color='red', icon='exclamation-triangle', prefix='fa'),
        popup=f"Dangerous Area: {area['name']}"
    ).add_to(m)

# Save and open map automatically
m.save('geofence_with_danger_areas.html')
webbrowser.open('geofence_with_danger_areas.html')

print("Map saved as geofence_with_danger_areas.html and opened in browser.")

