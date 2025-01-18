import streamlit as st
from src.apps.product_review_analyzer import backend
from src.llm.gemini_text import generate_content
from src.config.setup import initialize_genai_client
from src.config.logging import logger
import json

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes the given prompt with Gemini and returns the formatted response.
    
    Args:
        prompt (str): The prompt to send to Gemini.
    
    Returns:
        str: The formatted response from Gemini.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return "Error generating formatted response."
    
def display_search_results(results: dict, search_type: str) -> None:
    """
    Displays search results in a user-friendly format, using Gemini for formatting JSON if needed.

    Args:
        results (dict): The search results to display.
        search_type (str): The type of search performed (e.g., 'Google Shopping', 'Walmart').
    """
    try:
        if not results:
            st.write("No results found.")
            return

        if search_type == "Google Shopping":
            st.subheader("Top Google Shopping Results:")
            if "shopping_results" in results and results["shopping_results"]:
              
              formatted_results = []
              for item in results["shopping_results"][:5]:
                formatted_results.append(f"Title: {item.get('title', 'N/A')}, Price: {item.get('price', 'N/A')}, Link: {item.get('link', 'N/A')}")

              prompt = f"Summarize the following product shopping results:\n {formatted_results}"
              formatted_text = process_with_gemini(prompt)
              st.write(formatted_text)

            else:
              st.write("No shopping results available")


        elif search_type == "Walmart Basic Search":
          st.subheader("Top Walmart Results:")
          if "organic_results" in results and results["organic_results"]:
            
            formatted_results = []
            for item in results["organic_results"][:5]:
              formatted_results.append(f"Title: {item.get('title', 'N/A')}, Price: {item.get('price', 'N/A')}, Link: {item.get('link', 'N/A')}")
            prompt = f"Summarize the following product results:\n {formatted_results}"
            formatted_text = process_with_gemini(prompt)
            st.write(formatted_text)

          else:
            st.write("No Walmart search results available")


        elif search_type == "Google Search Results":
            st.subheader("Top Google Search Results:")
            if "organic_results" in results and results["organic_results"]:
              formatted_results = []
              for item in results["organic_results"][:5]:
                formatted_results.append(f"Title: {item.get('title', 'N/A')}, Link: {item.get('link', 'N/A')}")

              prompt = f"Summarize the following Google search results:\n {formatted_results}"
              formatted_text = process_with_gemini(prompt)
              st.write(formatted_text)
            else:
              st.write("No Google search results available")


        elif search_type == "Google Local Basic Search":
          st.subheader("Top Google Local Results:")
          if "local_results" in results and results["local_results"]:

            formatted_results = []
            for item in results["local_results"][:5]:
                formatted_results.append(f"Title: {item.get('title', 'N/A')}, Rating: {item.get('rating', 'N/A')}, Address: {item.get('address', 'N/A')}")
            prompt = f"Summarize the following local search results:\n {formatted_results}"
            formatted_text = process_with_gemini(prompt)
            st.write(formatted_text)

          else:
            st.write("No local results available")


        else:
            st.write("Unsupported search type.")

    except Exception as e:
      logger.error(f"Error displaying search results: {e}")
      st.error("Error occurred while displaying results.")
    

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Product Review Analyzer")

    product_name = st.text_input("Enter product name:", "")

    if product_name:
        st.subheader("Searching for: " + product_name)

        # Google Shopping Search
        st.write("Fetching Google Shopping results...")
        try:
            shopping_results = backend.search_google_shopping(product_name)
            display_search_results(shopping_results, "Google Shopping")
        except Exception as e:
            logger.error(f"Error during Google Shopping search: {e}")
            st.error("Error fetching Google Shopping results.")


        # Walmart Search
        st.write("Fetching Walmart results...")
        try:
          walmart_results = backend.search_walmart(product_name)
          display_search_results(walmart_results, "Walmart Basic Search")
        except Exception as e:
          logger.error(f"Error during Walmart search: {e}")
          st.error("Error fetching Walmart results")


        # Google Search
        st.write("Fetching Google Search results...")
        try:
            google_search_results = backend.search_google(product_name)
            display_search_results(google_search_results, "Google Search Results")
        except Exception as e:
            logger.error(f"Error during Google search: {e}")
            st.error("Error fetching Google Search results.")


        # Google Local Search
        st.write("Fetching Google Local results...")
        try:
          google_local_results = backend.search_google_local(product_name)
          display_search_results(google_local_results, "Google Local Basic Search")
        except Exception as e:
          logger.error(f"Error during Google Local search: {e}")
          st.error("Error fetching Google Local results")


if __name__ == "__main__":
    main()