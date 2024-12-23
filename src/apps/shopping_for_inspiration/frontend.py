import streamlit as st
from typing import Dict, List
from src.apps.shopping_for_inspiration import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Formats a given prompt using the Gemini model.

    Args:
        prompt (str): The prompt to be formatted.

    Returns:
        str: The formatted response from Gemini.
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
    st.title("Shopping for Inspiration")

    search_term = st.text_input("Enter a concept or trend to search for:", "")
    if search_term:
        try:
            st.subheader("Image Search Results:")
            image_results = backend.search_images(search_term)
            if image_results and "images_results" in image_results:
                for i, image_data in enumerate(image_results["images_results"][:5]):  # Display only the first 5 images
                    st.image(image_data["thumbnail"], caption=f"Image {i+1}", use_column_width=True)
                    
            else:
                st.error("No image results found or invalid image result structure.")

            st.subheader("Related Walmart Products:")
            walmart_results = backend.search_walmart(search_term)
            if walmart_results and "organic_results" in walmart_results:
                 formatted_results = process_with_gemini(f"Format the following JSON data for user readability:\n {str(walmart_results['organic_results'])}")
                 st.markdown(formatted_results)
            else:
               st.error("No product results found or invalid product result structure.")    

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()