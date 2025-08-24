import geopandas as gpd
from pathlib import Path
import pydeck as pdk
import streamlit as st
import os
import requests

SCRIP_DIR = Path(__file__).parent


gdf = gpd.read_file(SCRIP_DIR / "HYMAP_BlueBound" / "HYSETS_watershed_boundaries" / "HYSETS_watershed_boundaries_20200730.shp")

# If CRS is None, set it to NAD83 (common for HYSETS data)
if gdf.crs is None:
    gdf.set_crs("EPSG:4269", inplace=True)  # NAD83 geographic
    print("Set CRS to EPSG:4269 (NAD83)")

# Now transform to WGS84 (EPSG:4326)
gdf = gdf.to_crs("EPSG:4326")

# Calculate the center of the data
min_lon, min_lat, max_lon, max_lat = gdf.total_bounds
center_lat = (min_lat + max_lat) / 2
center_lon = (min_lon + max_lon) / 2


st.set_page_config(layout="wide")

TILES = "https://sepehr-farhoodi.github.io/watershed-tiles/tiles_out/{z}/{x}/{y}.pbf"

view = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=4, min_zoom=2, max_zoom=10, bearing=0, pitch=0)


layer = pdk.Layer(
    "MVTLayer",
    data=TILES,
    pickable=True,
    auto_highlight=True,
    get_fill_color=[52, 152, 219, 120],  # Blue with higher opacity
    get_line_color=[52, 152, 219, 255],  # Solid blue border
    line_width_min_pixels=1,
    min_zoom=2,
    max_zoom=10
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view,
    map_provider="carto",
    map_style="dark",
    tooltip={
        "html": "<b>Name:</b> {Name}<br/><b>Area:</b> {Area} km²<br/><b>Source:</b> {Source}",
        "style": {
            "backgroundColor": "white",
            "color": "black",
            "padding": "10px",
            "border-radius": "5px",
            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
        }
    }
)


st.pydeck_chart(deck, use_container_width=True)




