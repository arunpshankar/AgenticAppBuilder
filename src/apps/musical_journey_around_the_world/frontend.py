import streamlit as st
import src.apps.musical_journey_around_the_world.backend as backend
import json

def main():
    st.title("Musical Journey Around the World")

    st.write("Let's explore music from your current location!")

    if st.button("Start the Journey"):
        with st.spinner("Fetching your location..."):
            location_data = backend.get_location_info()

        if location_data and "country" in location_data:
             country = location_data["country"]
             st.success(f"Your country: {country}")
             st.session_state.country = country
        else:
             st.error("Could not determine your location. Please try again.")
             return
        

        with st.spinner(f"Finding music from {st.session_state.country}..."):
            artist_data = backend.get_artists_from_country(st.session_state.country)

        if artist_data and artist_data['artists']:
            st.subheader("Popular Artists and Themes:")
            for artist in artist_data['artists']:
                st.write(f"- **{artist['name']}**")
                if "themes" in artist and artist["themes"]:
                    st.write(f"  - Themes: {', '.join(artist['themes'])}")
                else:
                     st.write(" No Themes Found.")
                if "lyrics" in artist and artist["lyrics"]:
                     st.write("  - Sample Lyrics:")
                     st.code(artist["lyrics"], language="python")
                else:
                     st.write(" No Lyrics Found.")


        else:
            st.error("Could not find artists from the given location.")

    
        with st.spinner(f"Finding playlist of {st.session_state.country}..."):
            playlist_data = backend.get_playlists()
            
        if playlist_data:
           st.subheader("Playlist Sample:")
           st.json(playlist_data)
        else:
            st.error("Could not fetch playlist data.")

        with st.expander("Currency Exchange (Optional)"):
            if st.checkbox("Show Currency Information"):
                with st.spinner("Fetching currency data..."):
                    currency_data = backend.get_currency_exchange(st.session_state.country)

                if currency_data:
                     st.subheader("Currency Exchange:")
                     st.json(currency_data)
                else:
                     st.error("Could not fetch currency exchange data.")
        

    if "country" in st.session_state:
         if st.button("Get More Info About the Country"):
             with st.spinner("Fetching Country Info"):
                country_info = backend.get_country_info(st.session_state.country)

             if country_info:
                 st.subheader("Country Info")
                 st.json(country_info)
             else:
                 st.error("Could not retrieve country Info.")
            

if __name__ == "__main__":
    main()