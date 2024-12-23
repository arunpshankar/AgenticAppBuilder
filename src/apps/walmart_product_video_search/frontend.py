import streamlit as st
from typing import Dict, List
from src.apps.walmart_product_video_search import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a prompt using the Gemini model.
    Args:
        prompt (str): The prompt to send to the Gemini model.
    Returns:
        str: The text response from the Gemini model.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return f"Error: {e}"


def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Walmart Product Video Search")

    product_name = st.text_input("Enter Product Name", "")
    min_price = st.number_input("Enter Minimum Price", value=0.0, step=0.01)
    max_price = st.number_input("Enter Maximum Price", value=100.0, step=0.01)


    if st.button("Search"):
        if not product_name:
            st.error("Please enter a product name.")
            return

        try:
            with st.spinner("Searching..."):
                results = backend.search_products(product_name, min_price, max_price)

            if results and isinstance(results, dict) and 'products' in results:
                st.subheader("Walmart Product Search Results")
                
                if results['products']:
                  for product in results['products']:
                      st.write(f"**Product Name:** {product.get('name', 'N/A')}")
                      st.write(f"**Price:** ${product.get('price', 'N/A')}")
                      
                      video_search_term = f"{product.get('name', '')} review unboxing"

                      try:
                          video_results = backend.search_youtube_videos(video_search_term)
                          if video_results and isinstance(video_results, dict) and 'videos' in video_results:
                               st.write("Relevant Video Reviews:")
                               if video_results['videos']:
                                 for video in video_results['videos']:
                                    st.write(f"- [{video.get('title', 'N/A')}]({video.get('link', '#')})")
                               else:
                                  st.write("No video reviews found.")

                          else:
                            st.error("Error fetching video data.")

                      except Exception as e:
                          st.error(f"Error fetching video results: {e}")
                          logger.error(f"Error fetching video results: {e}")


                      st.divider()
                else:
                    st.write("No products found matching this criteria.")
            else:
                st.error("No results found or invalid response format.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
            logger.error(f"An error occurred during search: {e}")
            

if __name__ == "__main__":
    main()