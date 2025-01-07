import streamlit as st
from typing import Dict, List
from src.apps.investment_location_analyzer import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Formats the given prompt with Gemini.

    Args:
        prompt (str): The text prompt.

    Returns:
        str: The formatted text.
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
    st.title("Investment Location Analyzer")

    location = st.text_input("Enter a location (e.g., New York, NY):")
    industry = st.text_input("Enter an industry (e.g., coffee shops):")

    if location and industry:
        try:
            with st.spinner("Fetching data..."):
                local_results, finance_results = backend.fetch_data(location, industry)
            
            st.subheader("Local Business Results")
            if local_results:
                formatted_local_results = process_with_gemini(f"Format the following local business results into a readable format:\n{str(local_results)}")
                st.write(formatted_local_results)
            else:
                st.write("No local business results found.")

            st.subheader("Financial Comparison Results")
            if finance_results:
               formatted_finance_results = process_with_gemini(f"Format the following financial results into a readable format:\n{str(finance_results)}")
               st.write(formatted_finance_results)
            else:
                 st.write("No financial comparison results found.")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()