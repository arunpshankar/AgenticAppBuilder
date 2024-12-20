import streamlit as st
from typing import Dict, List
from src.apps.product_image_verification import backend
from src.llm.gemini_text import generate_content
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
    st.title("Product Image Verification")
    
    search_query = st.text_input("Enter product search query:")
    if search_query:
        with st.spinner("Fetching product data..."):
            walmart_results, google_results = backend.verify_product_images(search_query)
            
        if walmart_results and google_results:
            st.subheader("Walmart Search Results")
            for item in walmart_results:
                st.write(f"**Title:** {item.get('title', 'N/A')}")
                st.write(f"**Price:** {item.get('price', 'N/A')}")
                st.write(f"**Link:** {item.get('link', 'N/A')}")
                if 'image' in item:
                  st.image(item.get('image'), caption="Product Image", use_container_width=True)
                st.markdown("---")
            
            st.subheader("Google Images Results")
            for item in google_results:
                st.write(f"**Position:** {item.get('position', 'N/A')}")
                if 'thumbnail' in item:
                   st.image(item.get('thumbnail'), caption="Image Thumbnail", use_container_width=True)
                st.markdown("---")
            
            
            prompt = f"""
            Analyze the following Walmart product listings and Google image results for the query "{search_query}". 
            Walmart Results: {walmart_results}.
            Google Image Results: {google_results}.
            Provide a summary of the comparison, identifying any potential inconsistencies or misleading representations in the product images.
            """
            
            formatted_analysis = process_with_gemini(prompt)
            st.subheader("Analysis Summary")
            st.markdown(formatted_analysis)
        
        else:
            st.error("Could not retrieve results. Please check the search query or try again later.")
            
if __name__ == "__main__":
    main()