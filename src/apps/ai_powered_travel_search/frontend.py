import streamlit as st
from typing import Dict, List
from src.apps.ai_powered_travel_search import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a prompt with Gemini and returns the formatted text.

    Args:
        prompt (str): The prompt to be processed.

    Returns:
        str: The formatted text response from Gemini, or an error message if processing fails.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return f"Error processing with Gemini: {e}"


def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("AI Powered Travel Search")

    search_term = st.text_input("Enter your travel search query:", value="Flights to London")
    include_airlines = st.text_input("Airlines to include (comma-separated):", value="")
    exclude_airlines = st.text_input("Airlines to exclude (comma-separated):", value="")

    if st.button("Search"):
        try:
            with st.spinner("Searching..."):
                search_results = backend.search_travel_options(search_term, include_airlines, exclude_airlines)

                if search_results and isinstance(search_results, dict) and 'ai_overview' in search_results and 'flights' in search_results:
                    ai_overview = search_results.get('ai_overview', {})
                    flights = search_results.get('flights', [])

                    if ai_overview and isinstance(ai_overview, dict) and 'text' in ai_overview:
                         st.subheader("AI Overview Summary")
                         formatted_ai_summary = process_with_gemini(f"Format the following travel overview for readability: {ai_overview['text']}")
                         st.markdown(formatted_ai_summary)
                    else:
                        st.error("No AI overview available.")

                    if flights:
                        st.subheader("Flights")
                        for flight in flights:
                            st.write(f"Airline: {flight.get('airline', 'N/A')}")
                            st.write(f"Departure Airport: {flight.get('departure_airport', 'N/A')}")
                            st.write(f"Arrival Airport: {flight.get('arrival_airport', 'N/A')}")
                            st.write(f"Price: {flight.get('price', 'N/A')}")
                            st.write("---")
                    else:
                        st.warning("No flights found matching the criteria.")
                else:
                     st.error("No valid search results received.")


        except Exception as e:
           logger.error(f"An error occurred during search: {e}")
           st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()