import streamlit as st
from typing import Dict, List
from src.apps.local_business_financial_snapshot import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a text prompt using the Gemini model.

    Args:
        prompt (str): The text prompt to be processed.

    Returns:
        str: The generated text response from the Gemini model.
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
    st.title("Local Business Financial Snapshot")

    business_name = st.text_input("Enter Business Name", placeholder="e.g., 'Starbucks'")
    location = st.text_input("Enter Location (optional)", placeholder="e.g., 'New York, NY'")
    
    if st.button("Search"):
        if not business_name:
            st.warning("Please enter a business name.")
            return

        with st.spinner("Searching for business information..."):
            local_business_data, financial_data = backend.search_business(business_name, location)

        st.header("Local Business Information")
        if local_business_data and local_business_data.get("local_results"):
           
            for business in local_business_data["local_results"]:
                st.subheader(business.get("title", "Business Name"))
                st.write(f"**Rating:** {business.get('rating', 'N/A')}")
                st.write(f"**Address:** {business.get('address', 'N/A')}")
                st.write(f"**Phone:** {business.get('phone', 'N/A')}")
                
        else:
            st.write("No local business information found.")

        st.header("Financial Information")
        if financial_data and financial_data.get("summary"):
            
            prompt = f"Format the following JSON data into a readable paragraph: {financial_data}"
            formatted_financial_data = process_with_gemini(prompt)
            st.write(formatted_financial_data)

            if financial_data.get("news_results"):
                st.subheader("Recent News:")
                for news in financial_data["news_results"]:
                    st.write(f"- [{news.get('title', 'News')}]({news.get('link', '#')})")
        else:
            st.write("No financial information found for this business. It might not be publicly traded.")

if __name__ == "__main__":
    main()