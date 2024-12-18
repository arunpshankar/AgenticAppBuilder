import streamlit as st
from typing import Dict, List
from src.apps.dog_breed_explorer import backend
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
    st.title("Dog Breed Explorer")
    
    breed_name = st.text_input("Enter a dog breed:")
    
    if breed_name:
        try:
            with st.spinner(f"Fetching image for {breed_name}..."):
                 image_url_data = backend.fetch_dog_image(breed_name)

            if image_url_data and image_url_data.get('status') == 'success':
                image_url = image_url_data.get('message', '')
                if image_url:
                    st.image(image_url, caption=f"Image of {breed_name}", use_container_width=True)
                else:
                    st.error("No image URL found for this breed.")
            else:
                error_message = image_url_data.get('message', 'Failed to fetch image.') if image_url_data else "Failed to fetch image."
                st.error(f"Error fetching image: {error_message}")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            
if __name__ == "__main__":
    main()