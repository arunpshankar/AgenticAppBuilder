import streamlit as st
from typing import Dict, List
from src.apps.local_weather_and_space import backend

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Local Weather & ISS Tracker")

    st.markdown("Enter your location to get weather conditions and ISS location.")

    col1, col2 = st.columns(2, use_container_width=True)

    with col1:
        latitude = st.number_input("Latitude", value=34.0522, format="%.4f")
    with col2:
        longitude = st.number_input("Longitude", value=-118.2437, format="%.4f")

    if st.button("Get Data"):
         with st.spinner("Fetching data..."):
            try:
                weather_data, iss_data = backend.get_weather_and_iss_data(latitude, longitude)

                if weather_data:
                    st.subheader("Weather Forecast")
                    formatted_weather = backend.process_with_gemini(f"Format this weather data: {weather_data} for a human audience in markdown")
                    st.markdown(formatted_weather)
                else:
                    st.error("Could not retrieve weather data.")

                if iss_data:
                    st.subheader("ISS Location")
                    formatted_iss = backend.process_with_gemini(f"Format this ISS location data: {iss_data} for a human audience in markdown")
                    st.markdown(formatted_iss)
                else:
                    st.error("Could not retrieve ISS data.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()