import geopandas as gpd
from pathlib import Path
import pydeck as pdk
import streamlit as st
import os
import requests


st.set_page_config(layout="wide")

TILES = "https://sepehr-farhoodi.github.io/watershed-tiles/tiles_out/{z}/{x}/{y}.pbf"

view = pdk.ViewState(latitude=56.00, longitude=-96.82, zoom=4, min_zoom=2, max_zoom=10, bearing=0, pitch=0)


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




