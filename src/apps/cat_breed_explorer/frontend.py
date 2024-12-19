import streamlit as st
from typing import List, Dict
from src.apps.cat_breed_explorer import backend
from llm.gemini_text import generate_content
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
    st.title("Cat Breed Explorer")
    
    breeds_data = backend.fetch_cat_breeds()
    if breeds_data and "data" in breeds_data:
        breeds = [item["breed"] for item in breeds_data["data"]]
        selected_breed = st.selectbox("Select a Cat Breed", breeds)

        if selected_breed:
            fact_data = backend.fetch_cat_fact()
            if fact_data and "fact" in fact_data:
                fact = fact_data["fact"]
                prompt = f"Please format the following cat fact in a fun and interesting way:\n\n{fact}"
                formatted_fact = process_with_gemini(prompt)
                st.markdown(f"**Fun Fact about {selected_breed}s:**")
                st.markdown(formatted_fact)
            else:
                st.error("Could not fetch a cat fact.")
    else:
        st.error("Could not fetch cat breeds.")


if __name__ == "__main__":
    main()