import streamlit as st
from typing import Dict, List
from src.apps.cat_fact_feed_builder import backend
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
    st.title("Cat Fact Feed Builder")
    
    st.markdown("This application allows you to retrieve cat facts. You can get a single random fact, or generate a feed with multiple facts.")
    
    st.header("Get a Single Random Fact")
    if st.button("Get Random Fact", key="random_fact_button"):
        with st.spinner("Fetching a random cat fact..."):
            fact_data = backend.get_random_cat_fact()
            if fact_data:
                formatted_fact = process_with_gemini(f"Format this cat fact into markdown: {fact_data}")
                st.markdown(formatted_fact, unsafe_allow_html=True)
            else:
                st.error("Failed to retrieve cat fact.")
    
    st.header("Generate a Cat Fact Feed")
    num_facts = st.number_input("Number of Facts", min_value=1, max_value=20, value=5, step=1)
    if st.button("Generate Feed", key="feed_button"):
         with st.spinner("Generating cat fact feed..."):
            fact_feed = backend.get_multiple_cat_facts(num_facts)
            if fact_feed:
                formatted_feed = process_with_gemini(f"Format this list of cat facts into markdown: {fact_feed}")
                st.markdown(formatted_feed, unsafe_allow_html=True)

            else:
                st.error("Failed to retrieve cat fact feed.")

if __name__ == "__main__":
    main()