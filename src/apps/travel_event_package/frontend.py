import streamlit as st
from src.apps.travel_event_package import backend
from src.llm.gemini_text import generate_content
from src.config.setup import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """Processes the prompt with Gemini to get a formatted response."""
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return "Error formatting response."

def display_events(events: list):
    """Displays formatted event information."""
    if not events:
        st.write("No events found.")
        return

    st.subheader("Top 5 Events")
    for event in events[:5]:
        st.markdown(f"**{event.get('title', 'N/A')}**")
        st.write(f"When: {event.get('start_date', 'N/A')}")
        st.write(f"Where: {event.get('venue', {}).get('name', 'N/A')}, {event.get('venue', {}).get('address', 'N/A')}")
        if event.get('description'):
          formatted_desc = process_with_gemini(f"Summarize this event description in two short sentences: {event.get('description')}")
          st.write(f"Summary: {formatted_desc}")
        st.write("---")

def display_products(products: list):
    """Displays formatted product information."""
    if not products:
        st.write("No related products found.")
        return

    st.subheader("Top 5 Related Products")
    for product in products[:5]:
        st.markdown(f"**{product.get('title', 'N/A')}**")
        st.write(f"Price: {product.get('price', 'N/A')}")
        if product.get('description'):
            formatted_desc = process_with_gemini(f"Summarize this product description in one short sentence: {product.get('description')}")
            st.write(f"Summary: {formatted_desc}")
        st.write("---")


def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Travel Event and Shopping Suggestions")

    location_ip = backend.get_public_ip()
    if location_ip:
        st.write(f"Estimated Location IP: {location_ip}")

        events_data = backend.search_events_by_location(location_ip)
        if events_data and 'events' in events_data:
          display_events(events_data['events'])
          
          if events_data['events']:
            first_event = events_data['events'][0]
            if first_event:
              products_data = backend.search_products_for_event(first_event.get('title', ''))

              if products_data and 'shopping_results' in products_data:
                display_products(products_data['shopping_results'])
              else:
                st.write("Could not fetch related products.")
          else:
                st.write("No events found.")

        else:
          st.write("Could not fetch events for this location.")

    else:
        st.error("Could not determine your location. Please ensure you have a working internet connection.")


if __name__ == "__main__":
    main()