import streamlit as st
from typing import Dict, List
from src.apps.pet_fact_generator import backend
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
    st.title("Pet Fact Generator")
    
    if "fact_type" not in st.session_state:
        st.session_state["fact_type"] = "cat"

    if st.button("Get New Fact/Image"):
        if st.session_state["fact_type"] == "cat":
            fact_data = backend.get_cat_fact()
            if fact_data:
                formatted_fact = process_with_gemini(f"Format this fact into a markdown blockquote: {fact_data['fact']}")
                st.markdown(formatted_fact, use_container_width=True)
                st.session_state["fact_type"] = "dog"
            else:
                st.error("Failed to retrieve cat fact.")
        elif st.session_state["fact_type"] == "dog":
             dog_image_data = backend.get_dog_image()
             if dog_image_data and dog_image_data.get("message"):
                 st.image(dog_image_data["message"], caption="Random Dog Image", use_column_width=True)
                 st.session_state["fact_type"] = "cat"
             else:
                 st.error("Failed to retrieve dog image.")
        
if __name__ == "__main__":
    main()