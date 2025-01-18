import streamlit as st
from src.apps.local_business_investment_analyzer import backend
from src.llm.gemini_text import generate_content
from src.config.setup import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a given prompt using the Gemini model.

    Args:
        prompt (str): The prompt to send to Gemini.

    Returns:
        str: The text response from Gemini.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return "Error processing with Gemini"

def display_business_info(business_info: dict):
    """
    Displays business information in a user-friendly format.

    Args:
        business_info (dict): A dictionary containing business information.
    """
    if not business_info:
        st.write("No business information available.")
        return
    
    st.subheader(business_info.get("title", "Business Information"))
    
    if "local_results" in business_info and business_info["local_results"]:
      for result in business_info["local_results"]:
          st.markdown(f"**Name:** {result.get('title', 'N/A')}")
          st.markdown(f"**Address:** {result.get('address', 'N/A')}")
          st.markdown(f"**Phone:** {result.get('phone', 'N/A')}")
          st.markdown(f"**Rating:** {result.get('rating', 'N/A')}")
          st.markdown(f"**Reviews:** {result.get('reviews', 'N/A')}")
          st.markdown(f"**Website:** {result.get('website', 'N/A')}")
          st.markdown("---")
    else:
        st.write("No specific local results found.")
    
    if 'finance_data' in business_info and business_info['finance_data']:
        st.subheader("Financial Data:")
        financial_data = business_info['finance_data']
        if isinstance(financial_data, list):
             for data in financial_data:
                st.markdown(f"**Symbol:** {data.get('symbol', 'N/A')}")
                st.markdown(f"**Price:** {data.get('price', 'N/A')}")
                st.markdown(f"**Change:** {data.get('change', 'N/A')}")
                st.markdown(f"**Change Percent:** {data.get('changePercent', 'N/A')}")
                st.markdown("---")
        else:
            st.write("Financial data not in list format")
    else:
        st.write("No financial data available.")

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Local Business Investment Analyzer")

    business_type = st.text_input("Enter business type (e.g., restaurant, cafe):", "restaurant")
    location = st.text_input("Enter location (e.g., New York, NY):", "New York, NY")

    if st.button("Analyze"):
        if not business_type or not location:
            st.error("Please enter both business type and location.")
            return

        try:
            with st.spinner("Fetching data..."):
                business_info = backend.get_business_investment_data(business_type, location)

                if business_info:
                    prompt = f"Format this business information into a user-friendly summary, especially the JSON data. Format for optimal reading and comprehension: {business_info}"
                    formatted_info = process_with_gemini(prompt)
                    st.write(formatted_info)
                    display_business_info(business_info)

                else:
                    st.error("Could not retrieve business information.")

        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            st.error("An error occurred during the analysis.")


if __name__ == "__main__":
    main()