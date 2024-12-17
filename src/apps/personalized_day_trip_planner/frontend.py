import streamlit as st
import json
import src.apps.personalized_day_trip_planner.backend as backend

st.title("Personalized Day Trip Planner")

user_name = st.text_input("Enter your name")
if user_name:
    if st.button("Generate Trip Plan"):
        with st.spinner("Generating your personalized trip plan..."):
            trip_plan = backend.generate_trip_plan(user_name)
            st.header("Trip Plan")
            st.json(trip_plan)