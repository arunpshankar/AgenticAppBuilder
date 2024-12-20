import streamlit as st
from typing import Dict, List
from src.apps.safe_search_kids_content import backend

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Kid-Friendly Content Explorer")

    search_term = st.text_input("Enter a search term for kid-friendly videos:", "cartoons")
    if st.button("Search"):
        with st.spinner("Searching for kid-friendly videos and apps..."):
            video_results, app_results = backend.fetch_kids_content(search_term)

            st.header("Video Results")
            if video_results:
              for video in video_results:
                st.markdown(f"**Title:** {video['title']}")
                st.markdown(f"**Description:** {video['description']}")
                st.markdown(f"[Watch Video]({video['url']})")
                st.markdown("---")
            else:
              st.write("No videos found for this search term.")

            st.header("App Recommendations")
            if app_results:
                for app in app_results:
                    st.markdown(f"**App Name:** {app['title']}")
                    st.markdown(f"**Category:** {app['category']}")
                    st.markdown(f"[View on Play Store]({app['url']})")
                    st.markdown("---")
            else:
                st.write("No apps recommendations found.")

if __name__ == "__main__":
    main()