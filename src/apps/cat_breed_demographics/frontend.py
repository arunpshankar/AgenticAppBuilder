import streamlit as st
from typing import Dict, List
from src.apps.cat_breed_demographics import backend
from src.llm.gemini import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Process content through Gemini and format as markdown.
    
    Args:
        prompt (str): Input prompt for Gemini
        
    Returns:
        str: Formatted markdown response
    """
    response = generate_content(gemini_client, MODEL_ID, prompt)
    return response.text


def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Cat Breed Demographics")
    
    st.header("Choose a cat breed:")
    breeds = backend.get_cat_breeds()
    if breeds:
       breed_names = [breed["breed"] for breed in breeds]
       selected_breed = st.selectbox("Select cat breed", breed_names)
       
       if selected_breed:
           st.subheader(f"Details for {selected_breed}")
           breed_details = next((breed for breed in breeds if breed["breed"] == selected_breed), None)
           if breed_details:
             st.write(f"**Country**: {breed_details.get('country', 'Unknown')}")
             st.write(f"**Origin**: {breed_details.get('origin', 'Unknown')}")
             st.write(f"**Coat**: {breed_details.get('coat', 'Unknown')}")
             st.write(f"**Pattern**: {breed_details.get('pattern', 'Unknown')}")

    
           st.header("Generate example adoption profile:")

           human_name = st.text_input("Enter a Human Name (e.g., 'Alice' or 'Bob')", "Alice")
           if human_name:
                gender_info = backend.get_gender_from_name(human_name)
                nationality_info = backend.get_nationality_from_name(human_name)

                if gender_info and gender_info.get("gender"):
                   st.write(f"**Predicted Gender for {human_name}**: {gender_info['gender']}")
                if nationality_info and nationality_info.get("country"):
                    st.write(f"**Predicted Nationality for {human_name}**: {', '.join([country['country_id'] for country in nationality_info['country']])}")
                

                if breed_details and gender_info and nationality_info:
                    prompt = f"""Given the cat breed: {selected_breed}, with details: {breed_details},
                      and a person with the name: {human_name}, likely gender: {gender_info.get('gender', 'Unknown')}, and likely nationalities: {', '.join([country['country_id'] for country in nationality_info['country']])}. 
                      Generate a brief adoption profile including this cat and human information"""
                    
                    formatted_profile = process_with_gemini(prompt)
                    st.markdown(formatted_profile)
                else:
                  st.write("Could not fully generate a profile with the provided data")
    else:
        st.error("Failed to load cat breeds from API")


if __name__ == "__main__":
    main()