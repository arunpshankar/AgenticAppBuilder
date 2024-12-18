import streamlit as st
from typing import Dict, List
from src.apps.cat_breed_fact_finder import backend
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
    st.title("Cat Breed Fact Finder")
    
    try:
        breeds = backend.get_cat_breeds()
        if not breeds:
            st.error("Failed to retrieve cat breeds.")
            return
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return
    
    breed_names = [breed["name"] for breed in breeds]
    selected_breed = st.selectbox("Select a cat breed:", breed_names, use_container_width=True)
    
    if selected_breed:
        st.subheader(f"Fun Fact about Cats (Related to {selected_breed})")
        try:
            fact = backend.get_cat_fact()
            if fact:
                formatted_fact = process_with_gemini(f"Format the following cat fact as a markdown paragraph: {fact}")
                st.markdown(formatted_fact, unsafe_allow_html=True)
            else:
                st.warning("Could not retrieve a cat fact.")
        except Exception as e:
             st.error(f"An error occurred while fetching a cat fact: {e}")


if __name__ == "__main__":
    main()