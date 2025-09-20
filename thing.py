import streamlit as st
import requests

# Mapping weather → color palettes
palettes = {
    "clear sky": ["#FFD700", "#87CEEB", "#FFA500"],
    "few clouds": ["#D3D3D3", "#87CEFA", "#778899"],
    "scattered clouds": ["#B0C4DE", "#708090", "#2F4F4F"],
    "overcast clouds": ["#A9A9A9", "#696969", "#2F4F4F"],
    "light rain": ["#5F9EA0", "#4682B4", "#2C3E50"],
    "moderate rain": ["#4169E1", "#27408B", "#000080"],
    "snow": ["#FFFFFF", "#E0FFFF", "#AFEEEE"],
    "thunderstorm": ["#2C3E50", "#34495E", "#000000"],
    "mist": ["#D3D3D3", "#A9A9A9", "#C0C0C0"],
}

st.set_page_config("Weather Colors", page_icon = "🌤️")
st.title("🌤️ Find Weather Colors!")

# Input city name
city = st.text_input("Enter city name", "Seoul")

# Load API key from Streamlit secrets (better than hardcoding)
openweathermap_api_key = st.secrets["openweathermap"]

if st.button("Get Weather"):
    if city:
        # API endpoint
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={openweathermap_api_key}&units=metric"

        # Send request
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Extract useful info
            first_forecast = data["list"][0]    
            temp = first_forecast["main"]["temp"]
            desc = first_forecast["weather"][0]["description"]
            humidity = first_forecast["main"]["humidity"]
            wind_speed = first_forecast["wind"]["speed"]

            st.write(f"Current weather in **{city}**: {desc}")

            # Pick palette (default to gray tones if unknown)
            palette = palettes.get(desc, ["#D3D3D3", "#A9A9A9", "#696969"])

            st.subheader("Weather Color Palette:")

            cols = st.columns(len(palette))
            for i, color in enumerate(palette):
                with cols[i]:
                    st.markdown(
                        f"<div style='background-color:{color}; height:100px; border-radius:10px'></div>",
                        unsafe_allow_html=True,
                    )
                    st.code(color)  # show hex code          
        else:

            st.error("City not found or API error!")

