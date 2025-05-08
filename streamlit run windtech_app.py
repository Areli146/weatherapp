import streamlit as st
import requests

# 🔑 Get your OpenWeatherMap API key and paste here:
API_KEY = "your_openweathermap_api_key"

st.set_page_config(page_title="WindTech Weather Monitor", page_icon="🌪️")
st.title("🌪️ WindTech Weather Monitor")
st.write("Check real-time weather for wind turbine safety and planning.")

# 🌍 City input
city = st.text_input("Enter city or location:", "Plovdiv")

def get_weather_data(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&appid={API_KEY}&units=metric"
    )
    response = requests.get(url)
    return response.json()

if st.button("Get Weather"):
    data = get_weather_data(city)

    if data.get("cod") != 200:
        st.error(f"Error: {data.get('message', 'Could not fetch weather')}")
    else:
        st.subheader(f"Weather in {data['name']}, {data['sys']['country']}")

        temp = data["main"]["temp"]
        wind_speed = data["wind"]["speed"]
        wind_deg = data["wind"].get("deg", 0)
        weather_desc = data["weather"][0]["description"].capitalize()
        rain = data.get("rain", {}).get("1h", 0)

        st.metric("🌡️ Temperature", f"{temp} °C")
        st.metric("💨 Wind Speed", f"{wind_speed} m/s")
        st.write(f"🧭 Wind Direction: {wind_deg}°")
        st.write(f"🌦️ Conditions: {weather_desc}")
        st.write(f"🌧️ Rain (last hour): {rain} mm")

        # ⚠️ Safety alert
        if wind_speed > 15:
            st.warning("⚠️ Wind is too strong for safe turbine work!")
        elif wind_speed > 10:
            st.info("⚠️ Caution: Moderate wind speed.")
        else:
            st.success("✅ Wind conditions are safe for maintenance.")

