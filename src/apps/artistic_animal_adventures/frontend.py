import streamlit as st
import src.apps.artistic_animal_adventures.backend as backend
import json

st.title("Artistic Animal Adventures")

if st.button("Generate Adventure"):
    with st.spinner("Fetching data..."):
        adventure_data = backend.create_adventure()
    
    if adventure_data:
      st.subheader("The Artistic Animal Adventure:")
      st.write(f"**Animal Fact:** {adventure_data['animal_fact']}")
      st.image(adventure_data["fox_image"], caption="Random Fox Image", use_column_width=True)
      st.write(f"**Art Institute Artwork:**")
      st.json(adventure_data['art_institute_data'])
      st.write("\n")
      st.write(f"**Adventure Prompt:** *{adventure_data['adventure_prompt']}*")
    else:
        st.error("Failed to generate adventure. Please try again.")