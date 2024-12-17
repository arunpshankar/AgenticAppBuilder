import streamlit as st
import src.apps.pet_pal_explorer.backend as backend
import json
from src.llm.gemini import generate_content
from src.config.client import initialize_genai_client


gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"


def main():
    st.title("Pet Pal Explorer")
    st.markdown("Enter your name to discover your ideal pet companion!")
    
    name = st.text_input("Your Name", "John Doe")
    if name:
        with st.spinner('Fetching your info...'):
            user_info = backend.get_user_info(name)
        
        if user_info and isinstance(user_info, dict):
            st.subheader("Your Profile")
            
            # Use Gemini to generate a more descriptive user profile
            prompt = f"""
            Given the following user information, create a short, descriptive profile in markdown format.

            User Information:
            Name: {user_info.get('name', 'N/A')}
            Age: {user_info.get('age', 'N/A')}
            Gender: {user_info.get('gender', 'N/A')}
            Nationality: {user_info.get('nationality', 'N/A')}
            
            Profile:
            """
            
            response = generate_content(gemini_client, MODEL_ID, prompt)
            if response and response.text:
              st.markdown(response.text)
            else:
              st.write(f"Name: {user_info.get('name', 'N/A')}")
              st.write(f"Age: {user_info.get('age', 'N/A')}")
              st.write(f"Gender: {user_info.get('gender', 'N/A')}")
              st.write(f"Nationality: {user_info.get('nationality', 'N/A')}")

            
            with st.spinner('Finding the purrfect pet...'):
               pet_suggestion = backend.suggest_pet(user_info)
            
            if pet_suggestion:
                st.subheader("Your Suggested Pet")
                st.markdown(f"Based on your profile, we suggest a **{pet_suggestion['breed']}**.")

                if pet_suggestion["animal_type"] == "cat":
                  with st.spinner('Fetching a fun fact...'):
                      pet_fact = backend.get_cat_fact()
                  if pet_fact:
                    
                    prompt = f"""
                        Given the following cat fact, convert the fact into a more readable sentence in markdown.

                        Cat Fact: {pet_fact}

                        Readable Fact:
                        """
                    response = generate_content(gemini_client, MODEL_ID, prompt)
                    if response and response.text:
                       st.markdown(f"**Fun Fact:** {response.text}")
                    else:
                      st.markdown(f"**Fun Fact:** {pet_fact}")



                elif pet_suggestion["animal_type"] == "dog":
                  with st.spinner('Fetching a cute image...'):
                     pet_image = backend.get_dog_image(pet_suggestion['breed'])
                  if pet_image:
                    st.image(pet_image, caption="Your new friend", use_column_width=True)
            else:
              st.error("Could not find a suitable pet suggestion")


        else:
            st.error("Could not fetch user information. Please check the name and try again.")
    

if __name__ == "__main__":
    main()
```