import streamlit as st
from typing import Dict, List
from src.apps.neighborhood_financial_health_mapping import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client
from src.config.logging import logger


gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Formats text using Gemini.

    Args:
        prompt (str): The prompt to send to Gemini.

    Returns:
        str: The formatted response from Gemini.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return "Error formatting response with Gemini."

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Neighborhood Financial Health Mapping")

    location = st.text_input("Enter a location (e.g., New York, NY):")
    query = st.text_input("Enter a business query (e.g., coffee shops):")

    if location and query:
        with st.spinner("Fetching data..."):
            try:
                 local_business_data, finance_data = backend.fetch_neighborhood_data(query, location)
            except Exception as e:
                logger.error(f"Error fetching data: {e}")
                st.error("An error occurred while fetching data. Please try again.")
                return
            
            if local_business_data:
                st.subheader("Local Business Results:")
                formatted_local_business_data = process_with_gemini(f"Format this local business JSON for a user-friendly display: {local_business_data}")
                st.markdown(formatted_local_business_data)
            else:
                 st.write("No local business data found.")

            if finance_data:
                st.subheader("Financial Data:")
                formatted_finance_data = process_with_gemini(f"Format this finance data JSON for a user-friendly display: {finance_data}")
                st.markdown(formatted_finance_data)
            else:
                st.write("No financial data found for the area.")

if __name__ == "__main__":
    main()