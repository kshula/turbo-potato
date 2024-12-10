import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from io import StringIO

# Page configuration
st.set_page_config(page_title="Property Valuation System", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ("View Map", "View Properties", "Upload Data", "Add Property"),
)

# Initialize property data storage
if "properties" not in st.session_state:
    st.session_state["properties"] = pd.DataFrame(
        columns=["Name", "Latitude", "Longitude", "Rate"]
    )

# View Map Page
if page == "View Map":
    st.title("Property Valuation System - Lusaka")
    map_center = [-15.4167, 28.2833]  # Lusaka city center
    m = folium.Map(location=map_center, zoom_start=12, tiles="OpenStreetMap")

    # Add markers from session state
    for _, row in st.session_state["properties"].iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row['Name']}: Rate {row['Rate']}",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

    # Display the map
    st_folium(m, width=900, height=500)

# View Properties Page
elif page == "View Properties":
    st.title("Property List")
    if st.session_state["properties"].empty:
        st.write("No properties to display. Add or upload properties to get started.")
    else:
        st.dataframe(st.session_state["properties"])

# Upload Data Page
elif page == "Upload Data":
    st.title("Upload Property Data")
    uploaded_file = st.file_uploader(
        "Upload a CSV file containing property details (Name, Latitude, Longitude, Rate):",
        type="csv",
    )
    if uploaded_file:
        # Read uploaded CSV file
        try:
            uploaded_data = pd.read_csv(uploaded_file)
            # Validate required columns
            if {"Name", "Latitude", "Longitude", "Rate"}.issubset(uploaded_data.columns):
                st.session_state["properties"] = pd.concat(
                    [st.session_state["properties"], uploaded_data], ignore_index=True
                ).drop_duplicates()
                st.success("Data uploaded successfully!")
            else:
                st.error("The file must contain columns: Name, Latitude, Longitude, and Rate.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Add Property Page
elif page == "Add Property":
    st.title("Add New Property")
    with st.form("add_property_form"):
        name = st.text_input("Property Name")
        latitude = st.number_input("Latitude", value=0.0, format="%.6f")
        longitude = st.number_input("Longitude", value=0.0, format="%.6f")
        rate = st.text_input("Rate")
        submitted = st.form_submit_button("Add Property")

        if submitted:
            if name and rate:
                new_property = {
                    "Name": name,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Rate": rate,
                }
                st.session_state["properties"] = st.session_state["properties"].append(
                    new_property, ignore_index=True
                )
                st.success(f"Property '{name}' added successfully!")
            else:
                st.error("Please fill in all fields.")
