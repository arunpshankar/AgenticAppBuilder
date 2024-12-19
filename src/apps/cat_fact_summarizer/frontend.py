import streamlit as st
from typing import List
from src.apps.cat_fact_summarizer import backend

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Cat Fact Summarizer")
    st.markdown("Get a summary of cat facts and breed information.")
    
    num_facts = st.slider("Number of Facts to Retrieve", min_value=1, max_value=5, value=3)

    if st.button("Get Cat Facts and Breeds"):
      with st.spinner("Fetching cat data..."):
        try:
            facts = backend.get_cat_facts(num_facts)
            breeds = backend.get_cat_breeds()
            
            if facts:
                st.subheader("Cat Facts:")
                for fact in facts:
                    st.markdown(f"- {fact['fact']}")

            if breeds:
                st.subheader("Cat Breeds:")
                formatted_breeds = backend.process_with_gemini(f"Format this list of cat breeds as a bullet point list with each breed on a new line: {breeds}")
                st.markdown(formatted_breeds)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            
if __name__ == "__main__":
    main()