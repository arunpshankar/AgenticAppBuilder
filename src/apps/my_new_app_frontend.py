python
import streamlit as st
import requests
import json

# Backend API endpoint (replace with your actual backend URL)
API_URL = "http://localhost:8000"

st.title("The Global Citizen's Daily Brief")

name = st.text_input("Enter your name:")

if name:
    if st.button("Get my briefing"):
        try:
            response = requests.post(f"{API_URL}/briefing", json={"name": name})
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()


            st.subheader("Personalized Profile")
            st.write(f"Predicted Age: {data.get('age', 'N/A')}")
            st.write(f"Predicted Gender: {data.get('gender', 'N/A')}")
            st.write(f"Predicted Nationality: {data.get('nationality', 'N/A')}")


            st.subheader("Location and Space")
            if data.get('location'):
                location_data = data.get('location')
                st.write(f"Location: {location_data['city']}, {location_data['country']}")
            else:
                st.write("Location Information: Not Available")

            if data.get('iss_position'):
                 iss_data = data.get('iss_position')
                 st.write("Current ISS Location Relative to You:")
                 st.write(f"    Latitude: {iss_data['latitude']}")
                 st.write(f"    Longitude: {iss_data['longitude']}")
                 st.write(f"    Altitude: {iss_data['altitude']}")

            else:
                 st.write("ISS Position: Not Available")


            st.subheader("Local Information")
            if data.get('transport_info'):
                transport_data = data.get('transport_info')
                st.write(f"Nearby Transport Information:")
                for line in transport_data:
                     st.write(f"    {line['lineName']} - {line['towards']} - ETA: {line['timeToStation']} minutes")
            else:
                st.write("London Transport Data: Not Available")


            if data.get('weather'):
                weather_data = data.get('weather')
                st.write("Local Weather Forecast:")
                st.write(f"   Temperature: {weather_data.get('temperature', 'N/A')}°C")
                st.write(f"   Conditions: {weather_data.get('condition', 'N/A')}")
            else:
                st.write("Weather Forecast: Not Available")

        except requests.exceptions.RequestException as e:
            st.error(f"Error: Failed to connect to the backend: {e}")
        except json.JSONDecodeError:
            st.error("Error: Invalid JSON response from backend")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")