import streamlit as st
import json
from src.apps.pet_fact_&_fun_finder import backend

def main():
    st.title("Pet Fact & Fun Finder")

    animal_type = st.radio("Choose an animal:", ("Cat", "Dog"))

    if animal_type == "Cat":
        
        if st.button("Get Cat Fact"):
            fact_data = backend.get_cat_fact()
            if fact_data:
                st.subheader("Cat Fact:")
                st.json(fact_data)
            else:
                st.error("Failed to fetch cat fact.")

    elif animal_type == "Dog":
        if st.button("Get Dog Image"):
           dog_data = backend.get_dog_image()
           if dog_data:
                st.subheader("Dog Image:")
                st.image(dog_data["message"], use_column_width=True)
           else:
                st.error("Failed to fetch dog image.")

    if st.checkbox("Get Location Based Data"):
       
        location_data = backend.get_location_and_charge_data()
        if location_data and "ip_address" in location_data and "charge_data" in location_data:
            st.subheader("Your IP address")
            st.json(location_data["ip_address"])
            if location_data["charge_data"]:
              st.subheader("Nearby Charging Stations:")
              st.json(location_data["charge_data"])
            else:
                st.warning("No charging station data found for this location.")

        else:
            st.error("Failed to fetch location or charge station data.")


    if st.button("Get Random Fox Image"):
        fox_data = backend.get_fox_image()
        if fox_data:
            st.subheader("Random Fox Image:")
            st.image(fox_data["image"], use_column_width=True)
        else:
            st.error("Failed to fetch fox image.")


if __name__ == "__main__":
    main()