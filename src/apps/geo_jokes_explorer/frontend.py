import streamlit as st
import json
import src.apps.geo_jokes_explorer.backend as backend

st.title("Geo-Jokes Explorer")

if st.button("Get a Joke Based on Location"):
    try:
        result = backend.get_location_based_joke()
        st.subheader("Joke Result:")
        st.json(result)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write("Please ensure the service is working and try again later.")