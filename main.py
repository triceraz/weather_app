import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
coordinate_url = "http://api.openweathermap.org/geo/1.0/direct"

weather_url = f"https://api.openweathermap.org/data/2.5/weather"


def get_weather_data(url, city):
    weather_params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=weather_params)
    if response.status_code == 200:
        weather_data = response.json()
        print(weather_data["main"]["temp"])
    else:
        print(f"Failed to retrieve weather data {response.status_code}")


def get_city(url, city):
    coordinate_params = {"q": city, "appid": API_KEY, "limit": 1}
    response = requests.get(url, params=coordinate_params)
    if response.status_code == 200:
        city_data = response.json()
        return city_data[0]["lat"], city_data[0]["lon"]
    else:
        print(f"Failed to retrieve city data {response.status_code}")


# get_weather_data(url)
city_data = get_city(coordinate_url, "London")
print(city_data)
