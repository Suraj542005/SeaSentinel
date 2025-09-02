import streamlit as st
import os
import folium
from streamlit_folium import st_folium
from opencage.geocoder import OpenCageGeocode

# -------------------------------
# Config
# -------------------------------
SAVE_DIR = "files"
os.makedirs(SAVE_DIR, exist_ok=True)

# Initialize OpenCage
OPENCAGE_KEY = "d22765be25474fb9a45d9f1a2b30853f"
geocoder = OpenCageGeocode(OPENCAGE_KEY)

st.set_page_config(page_title="SeaSentinel Dashboard", layout="wide")
st.title("🌊 SeaSentinel Dashboard")

# -------------------------------
# Sidebar - User Inputs
# -------------------------------
st.sidebar.header("Report a Disaster")

uploaded_file = st.sidebar.file_uploader(
    "Upload an image or video",
    type=["jpg", "jpeg", "png", "mp4", "mov", "avi"]
)

description = st.sidebar.text_area("Enter description")
location = st.sidebar.text_input("Enter location name")
disaster_type = st.sidebar.selectbox("Disaster Type", ["Flood", "Fire", "Earthquake"])

submit = st.sidebar.button("Save & Add to Map")

# -------------------------------
# State Management
# -------------------------------
if "data" not in st.session_state:
    st.session_state.data = []

if submit:
    if uploaded_file and description and location:
        # Geocode location
        results = geocoder.geocode(location)
        if results:
            lat = results[0]["geometry"]["lat"]
            lon = results[0]["geometry"]["lng"]

            # Save file
            file_path = os.path.join(SAVE_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            # Save metadata
            meta_path = os.path.join(SAVE_DIR, uploaded_file.name + ".txt")
            with open(meta_path, "w") as f:
                f.write(f"Description: {description}\n")
                f.write(f"Location: {location}\n")
                f.write(f"Disaster Type: {disaster_type}\n")
                f.write(f"Latitude: {lat}, Longitude: {lon}\n")

            # Add to session state for map
            st.session_state.data.append({
                "lat": lat,
                "lon": lon,
                "label": disaster_type
            })

            st.sidebar.success("✅ Report saved and added to map!")
        else:
            st.sidebar.error("❌ Could not find the location. Try being more specific.")
    else:
        st.sidebar.warning("Please upload a file, add description, and enter location.")

# -------------------------------
# Layout - Main Page
# -------------------------------
col1, col2 = st.columns([1, 2])

# Preview uploaded file
with col1:
    st.subheader("Preview")
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if "image" in file_type:
            st.image(uploaded_file, caption="Preview", width="stretch")
        elif "video" in file_type:
            st.video(uploaded_file)

# Map Visualization
with col2:
    st.subheader("Live Disaster Map")

    # Create folium map
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="OpenStreetMap")

    # Add pulsating effect CSS
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
    .pulse-orange { background: rgba(255, 165, 0, 0.5); }
    </style>
    """
    m.get_root().html.add_child(folium.Element(heatwave_css))

    # Add markers dynamically
    for d in st.session_state.data:
        if d["label"] == "Flood":
            color_class = "pulse-blue"
        elif d["label"] == "Fire":
            color_class = "pulse-red"
        else:
            color_class = "pulse-orange"

        folium.Marker(
            location=[d["lat"], d["lon"]],
            popup=f"Disaster: {d['label']}",
            icon=folium.DivIcon(
                html=f'<div class="pulse {color_class}"></div>'
            )
        ).add_to(m)

    # Show map
    st_folium(m, width=800, height=600)
