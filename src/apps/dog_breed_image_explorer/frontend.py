import streamlit as st
from typing import Dict, List
from src.apps.dog_breed_image_explorer import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes the given prompt using the Gemini model.
    
    Args:
        prompt (str): The input prompt to process.
    
    Returns:
        str: The text response from the Gemini model.
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
    st.title("Dog Breed Image Explorer")
    
    breed = st.text_input("Enter a dog breed (e.g., hound):")
    num_images = st.slider("Number of images:", min_value=1, max_value=10, value=3)

    if st.button("Get Images"):
        if breed:
            try:
                with st.spinner(f"Fetching images for {breed}..."):
                    images_data = backend.get_random_dog_images_by_breed(breed, num_images)
                    if images_data and isinstance(images_data, dict) and "images" in images_data:
                        if images_data["images"]:
                            st.header(f"Random Images of {breed.capitalize()}")
                            for image_url in images_data["images"]:
                                st.image(image_url, use_column_width=True)
                        else:
                            st.error(f"No images found for the breed: {breed}")
                    else:
                        st.error("Failed to retrieve images.")
                        if images_data:
                           
                            prompt = f"Please format this JSON for better readability: {str(images_data)}"
                            formatted_json = process_with_gemini(prompt)
                            st.write("Raw API Response:")
                            st.code(formatted_json, language="json")


            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a dog breed.")

if __name__ == "__main__":
    main()
```