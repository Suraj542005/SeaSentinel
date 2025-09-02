import folium
from streamlit_folium import st_folium
import streamlit as st

# Sample user data (lat, lon, classification)
data = [
    {"lat": 28.6139, "lon": 77.2090, "label": "Flood"},  # Delhi
    {"lat": 19.0760, "lon": 72.8777, "label": "Earthquake"},  # Mumbai
    {"lat": 13.0827, "lon": 80.2707, "label": "Fire"}  # Chennai
]

# Create a map centered at India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="OpenStreetMap")

# Define CSS/JS for pulsating effect
heatwave_css = """
<style>
.pulse {
  position: relative;
  width: 20px;
  height: 20px;
  background: rgba(0, 123, 255, 0.5);  /* default blue */
  border-radius: 50%;
}
.pulse::after {
  content: "";
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: inherit;
  animation: pulse-animation 2s infinite;
}
@keyframes pulse-animation {
  0% { transform: scale(1); opacity: 0.7; }
  70% { transform: scale(3); opacity: 0; }
  100% { transform: scale(1); opacity: 0; }
}
.pulse-red { background: rgba(255, 0, 0, 0.5); }
.pulse-blue { background: rgba(0, 123, 255, 0.5); }
</style>
"""

m.get_root().html.add_child(folium.Element(heatwave_css))

# Add animated markers
for d in data:
    color_class = "pulse-red" if d["label"] == "Fire" else "pulse-blue"

    folium.Marker(
        location=[d["lat"], d["lon"]],
        popup=f"Disaster: {d['label']}",
        icon=folium.DivIcon(
            html=f'<div class="pulse {color_class}"></div>'
        )
    ).add_to(m)

# Display in Streamlit
st_data = st_folium(m, width=700, height=500)
