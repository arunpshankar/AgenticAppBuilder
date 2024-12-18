import streamlit as st
from typing import Dict, List
from src.apps.name_demographics_analyzer import backend
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
    st.title("Name Demographics Analyzer")
    st.markdown("Enter a name to explore its predicted gender and associated nationalities.")
    
    name = st.text_input("Enter a name:", "")
    
    if name:
        with st.spinner("Analyzing name..."):
            try:
                gender_data = backend.get_gender_by_name(name)
                nationality_data = backend.get_nationality_by_name(name)

                if gender_data:
                    gender_prompt = f"The predicted gender for the name '{name}' is '{gender_data['gender']}'. The probability of this prediction is '{gender_data['probability']}'. Display this information formatted in markdown."
                    formatted_gender = process_with_gemini(gender_prompt)
                    st.markdown(formatted_gender)
                else:
                    st.error("Could not determine predicted gender for the name.")
                
                if nationality_data and nationality_data['country']:
                    nationality_prompt = f"The predicted nationalities for the name '{name}' are: {', '.join([f'{c["country_id"]} (Probability: {c["probability"]})' for c in nationality_data['country']])}. Display this information formatted in markdown."
                    formatted_nationality = process_with_gemini(nationality_prompt)
                    st.markdown(formatted_nationality)
                else:
                    st.error("Could not determine predicted nationalities for the name.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()