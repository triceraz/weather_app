# Weather App

# Small PyQt5 GUI that shows current weather for a city using OpenWeather. Also uses OpenWeather API to get latitude and longitude of the chosen city.

# - Run: `python main.py`
# - Add your API key to [.env](.env) as `OPENWEATHER_API_KEY` (used as [`API_KEY`](main.py))
# - Enter a city and press "Get Weather" (UI in [`WeatherApp`](main.py); logic in [`get_weather`](main.py) and [`get_city`](main.py))
# - Emoji mapping: see [`get_weather_emoji`](main.py)

# Dependencies:
# ```
# pip install -r requirements.txt
# ```

# Notes:
# - .gitignore excludes the .env and virtual env (see [.gitignore](.gitignore))
# - Keep the API key private
