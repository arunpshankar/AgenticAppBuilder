import streamlit as st
from src.apps.local_event_shopping_assistant import backend
from src.llm.gemini_text import generate_content
from src.config.setup import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """Processes a text prompt with Gemini and returns the response."""
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return "Error processing text."

def display_events_and_products(events_data, shopping_data):
    """Displays events and related products in a user-friendly way."""
    if not events_data or not shopping_data:
       st.warning("No events or shopping data available.")
       return

    st.header("Local Events and Related Products")
    
    if events_data and events_data.get('events'):
        st.subheader("Upcoming Events")
        for event in events_data['events'][:5]: #Display top 5 events
            if isinstance(event, dict):
                event_name = event.get('title', 'N/A')
                event_time = event.get('start_time', 'N/A')
                event_location = event.get('venue', {}).get('name', 'N/A')
                st.markdown(f"**Event:** {event_name}")
                st.markdown(f"**Time:** {event_time}")
                st.markdown(f"**Location:** {event_location}")
                st.markdown("---")
    else:
        st.warning("No events found.")
    
    if shopping_data and shopping_data.get('shopping_results'):
            st.subheader("Related Products")
            for product in shopping_data['shopping_results'][:5]: # Display top 5 products
                if isinstance(product, dict):
                    product_name = product.get('title', 'N/A')
                    product_price = product.get('price', 'N/A')
                    product_link = product.get('link', 'N/A')
                    st.markdown(f"**Product:** {product_name}")
                    st.markdown(f"**Price:** {product_price}")
                    st.markdown(f"**Link:** {product_link}")
                    st.markdown("---")
    else:
         st.warning("No products found.")

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Local Event Shopping Assistant")

    location = st.text_input("Enter your location (e.g., city, zip code):")

    if st.button("Find Events and Products"):
        if not location:
            st.error("Please enter a location.")
            return
        
        try:
            with st.spinner("Fetching events and products..."):
                events_data, shopping_data = backend.fetch_events_and_products(location)
                if events_data and shopping_data:
                    display_events_and_products(events_data, shopping_data)
                else:
                    st.warning("Could not retrieve all data. Please verify the location.")

        except Exception as e:
            logger.error(f"Error in main application: {e}")
            st.error("An error occurred while fetching data. Please try again later.")

if __name__ == "__main__":
    main()