python
import streamlit as st
import requests

# Backend URL (replace with your actual backend URL)
BACKEND_URL = "http://localhost:8000"  # Assuming local backend running on port 8000

def get_journal_entry(name):
    """Calls the backend to get a journal entry."""
    try:
        response = requests.get(f"{BACKEND_URL}/journal?name={name}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the backend: {e}")
        return None

def main():
    st.title("The Curious Wanderer")

    name = st.text_input("Enter a name for your traveler:", "Alice")

    if st.button("Generate Journal Entry"):
      if name:
        with st.spinner("Generating your journal entry..."):
            journal_data = get_journal_entry(name)

            if journal_data:
                st.subheader("Travel Journal Entry:")
                st.write(f"Dear Diary,")
                st.write(journal_data['intro'])
                st.write(f"The local, an {journal_data['location']['city']} , asked me for {journal_data['joke']}. It seemed so strange. ")
                st.image(journal_data['dog_image'], caption="A random dog I saw on my travels.", use_column_width=True)
                st.write(f"I was fascinated to learn that: {journal_data['cat_fact']}")
                st.write("Until next time,")
                st.write(f"{name}")

      else:
        st.warning("Please enter a name.")

if __name__ == "__main__":
    main()