import streamlit as st
from typing import Dict, List
from src.apps.find_visual_matches_at_walmart import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Formats a given prompt using the Gemini model.

    Args:
        prompt (str): The prompt to be processed.

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
    st.title("Find Visual Matches at Walmart")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        try:
            image_url = backend.get_image_url(uploaded_file.getvalue())
            if image_url:
                st.image(image_url, caption="Uploaded Image", use_column_width=True)
                st.write("Extracting keywords from image...")

                keywords = backend.get_keywords_from_image_url(image_url)
                if keywords:
                    st.write(f"Keywords extracted: {', '.join(keywords)}")
                    st.write("Searching for similar products on Walmart...")
                    walmart_results = backend.search_walmart_products(keywords)
                    if walmart_results:
                        st.write("Walmart Search Results:")
                        formatted_results_prompt = f"Format this JSON to be user readable: {walmart_results}"
                        formatted_results = process_with_gemini(formatted_results_prompt)
                        st.write(formatted_results)
                    else:
                         st.error("No products found matching your criteria on Walmart.")
                else:
                    st.error("Failed to extract keywords from the image.")
            else:
                st.error("Failed to get image URL.")
        except Exception as e:
             st.error(f"An error occurred: {e}")



if __name__ == "__main__":
    main()