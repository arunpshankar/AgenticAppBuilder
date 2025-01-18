import streamlit as st
from src.apps.targeted_event_product_finder import backend
from src.config.setup import initialize_genai_client
from src.config.logging import logger

# Initialize Gemini client
gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

# --- UI ---
st.set_page_config(page_title="Targeted Event Product Finder", page_icon="🔎")
st.title("Find Products for Your Events")

# Input fields
col1, col2 = st.columns(2)
with col1:
    location = st.text_input("Enter Location", "New York")
with col2:
    event_query = st.text_input("Enter Event Query", "Concert")

def display_event_results(event_results):
    """
    Displays formatted event results using Streamlit.
    """
    if not event_results or 'events' not in event_results:
        st.error("No events found or invalid event data.")
        return

    st.subheader("Top 5 Event Summary:")
    events = event_results['events'][:5]
    for event in events:
        # Event Name
        st.markdown(f"<span style='font-size:18px; font-weight:bold;'>{event.get('title', 'N/A')}</span>", unsafe_allow_html=True)

        # Description
        st.markdown(f"<span style='font-size:14px;'>{event.get('description', 'N/A')}</span>", unsafe_allow_html=True)

        # Date and Time
        st.markdown(f"<span style='font-size:14px;'>**Date:** {event.get('date', 'N/A')}</span>", unsafe_allow_html=True)

        # Location
        st.markdown(f"<span style='font-size:14px;'>**Location:** {', '.join(event.get('address', ['N/A']))}</span>", unsafe_allow_html=True)

        st.markdown("---")

def display_product_results(product_results):
    """
    Displays formatted product results with thumbnails.
    """
    if not product_results or 'shopping_results' not in product_results:
        st.error("No products found or invalid product data.")
        return

    shopping_results = product_results['shopping_results'][:5]
    if shopping_results:
        st.subheader("Top 5 Related Products:")
        for result in shopping_results:
            # Thumbnail
            thumbnail_url = result.get('thumbnail', '')
            if thumbnail_url:
                st.image(thumbnail_url, width=100, caption=result.get('title', 'N/A'))

            # Product details
            st.markdown(f"<span style='font-size:14px;'>**Price:** {result.get('price', 'N/A')}</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:14px;'><a href='{result.get('link', 'N/A')}'>Product Link</a></span>", unsafe_allow_html=True)  # Using 'product_link'

            st.markdown("---")

def main():
    """
    Main function to run the Streamlit app.
    """
    # Search button
    if st.button("Search"):
        try:
            with st.spinner("Searching for events..."):
                event_results = backend.search_events(location, event_query)

            if event_results:
                display_event_results(event_results)

                with st.spinner("Searching for products..."):
                    product_results = backend.search_products_for_event(event_results.get('events'), event_query)

                if product_results:
                    display_product_results(product_results)
                else:
                    st.warning("No products found for these events.")
            else:
                st.warning("No events found for this query.")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            st.error("An unexpected error occurred. Please check the logs.")

if __name__ == "__main__":
    main()