import streamlit as st
import src.apps.global_trivia_location_game.backend as backend
from src.llm.gemini import generate_content
from src.config.client import initialize_genai_client
import json

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def main():
    st.title("Global Trivia Location Game")
    
    if st.button("Get Trivia and Location"):
        with st.spinner("Fetching trivia and location..."):
          try:
              trivia_data, location_data = backend.fetch_trivia_and_location()
              st.subheader("Trivia Question")
              if trivia_data and "results" in trivia_data and trivia_data["results"]:
                  question_data = trivia_data["results"][0]
                  question = question_data.get("question", "No question found")
                  correct_answer = question_data.get("correct_answer", "No answer found")

                  # Format the question for better display
                  formatted_question = f"<p style='font-size: 1.2em; font-weight: bold;'>{question}</p>"
                  st.markdown(formatted_question, unsafe_allow_html=True)
                  st.markdown(f"**Correct Answer:** {correct_answer}")
              else:
                st.error("Could not fetch trivia question.")


              st.subheader("Your Approximate Location")
              if location_data and location_data.get("display_name"):
                st.markdown(f"**Location:** {location_data['display_name']}")
                latitude = location_data.get("lat", "N/A")
                longitude = location_data.get("lon", "N/A")
                if latitude != "N/A" and longitude != "N/A":
                    st.markdown(f"**Coordinates:** Latitude: {latitude}, Longitude: {longitude}")


                    # Generate content
                    prompt = f"Given this trivia question: {question}. and location name {location_data['display_name']},  generate a fun location-based trivia hint (one sentence maximum). Make it very short"
                    response = generate_content(gemini_client, MODEL_ID, prompt)
                    text_response = response.text
                    st.markdown(f"**Hint:** {text_response}")


              else:
                  st.error("Could not fetch location data.")
          except Exception as e:
               st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()