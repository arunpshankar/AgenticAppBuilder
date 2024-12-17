import streamlit as st
import json
import src.apps.the_quirky_explorer.backend as backend

st.title("The Quirky Explorer")

if 'ip_address' not in st.session_state:
    st.session_state['ip_address'] = None
if 'location_data' not in st.session_state:
     st.session_state['location_data'] = None
if 'joke' not in st.session_state:
     st.session_state['joke'] = None
if 'trivia' not in st.session_state:
    st.session_state['trivia'] = None
if 'cat_fact' not in st.session_state:
    st.session_state['cat_fact'] = None

def fetch_data():
    with st.spinner('Fetching IP Address...'):
      ip_address = backend.get_ip_address()
      st.session_state['ip_address'] = ip_address['ip']

    with st.spinner('Fetching location data...'):
        location_data = backend.get_location_from_ip(st.session_state['ip_address'])
        st.session_state['location_data'] = location_data

    with st.spinner('Fetching Joke...'):
        joke = backend.get_joke()
        st.session_state['joke'] = joke

    with st.spinner('Fetching Trivia...'):
        trivia = backend.get_trivia()
        st.session_state['trivia'] = trivia
    with st.spinner('Fetching Cat Fact...'):
        cat_fact = backend.get_cat_fact()
        st.session_state['cat_fact'] = cat_fact
    

if st.button("Start Exploration"):
    fetch_data()

if st.session_state['ip_address']:
    st.subheader("Your IP Address:")
    st.write(st.session_state['ip_address'])


if st.session_state['location_data']:
    st.subheader("Location Data:")
    st.json(st.session_state['location_data'])

if st.session_state['joke']:
    st.subheader("Joke:")
    st.write(f"**Setup:** {st.session_state['joke']['setup']}")
    st.write(f"**Punchline:** {st.session_state['joke']['punchline']}")

if st.session_state['trivia']:
   st.subheader("Art Trivia Question:")
   st.write(f"**Question:** {st.session_state['trivia']['question']}")
   st.write(f"**Correct Answer:** {st.session_state['trivia']['correct_answer']}")
   
if st.session_state['cat_fact']:
    st.subheader("Random Cat Fact:")
    st.write(st.session_state['cat_fact']['fact'])

```