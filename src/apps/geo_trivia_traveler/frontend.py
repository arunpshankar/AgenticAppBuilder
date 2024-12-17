import streamlit as st
import src.apps.geo_trivia_traveler.backend as backend
import json

st.title("Geo-Trivia Traveler")

# --- Trivia Section ---
st.header("Trivia Question")
num_questions = st.slider("Number of Trivia Questions", 1, 5, 1)
trivia_data = backend.fetch_trivia_questions(num_questions)
if trivia_data:
    for i, question_data in enumerate(trivia_data["results"]):
        st.subheader(f"Question {i+1}")
        st.write(f"**Category:** {question_data['category']}")
        st.write(f"**Question:** {question_data['question']}")
        
        with st.expander("Show Answer and Geolocation"):
            country_name = st.text_input("Enter the country name", key=f"country_{i}")
            if country_name:
                location_data = backend.fetch_location_by_country(country_name)
                if location_data and location_data[0]:
                    st.write(f"**Correct Answer:** {question_data['correct_answer']}")
                    st.write("Location Info")
                    st.json(location_data[0])
                else:
                   st.write("Could not find country location. Please verify your spelling and try again.")
                
else:
    st.error("Failed to fetch trivia questions.")

# --- IP Geolocation Section ---
st.header("Your IP Geolocation")
if st.button("Get My IP Location"):
    ip_data = backend.fetch_ip_location()
    if ip_data:
        st.write("Your IP Information:")
        st.json(ip_data)
    else:
        st.error("Could not fetch IP location.")

# --- Geocoding Section ---
st.header("Geocoding")
location_query = st.text_input("Enter location (e.g., City, Landmark):")
if st.button("Get Geocoding Data") and location_query:
    geo_data = backend.fetch_geocoding_data(location_query)
    if geo_data:
        st.write("Geocoding Results:")
        st.json(geo_data)
    else:
        st.error("Could not geocode the given location.")