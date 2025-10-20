import requests
import sys
from dotenv import load_dotenv
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt


load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.coordinates_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.coordinates_label)

        self.setLayout(vbox)

        self.city_input.setFixedHeight(80)

        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.coordinates_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.coordinates_label.setObjectName("coordinates_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: "Helvetica Neue", Arial, Helvetica, sans-serif;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
                padding: 10px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
            QLabel#coordinates_label{
                font-size: 20px;
                color: #555;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = API_KEY
        if not api_key:
            self.display_error(
                "Missing API key:\nSet OPENWEATHER_API_KEY in .env and restart"
            )
            return

        city = self.city_input.text().strip()
        if not city:
            self.display_error("Please enter a city name")
            return

        coords = self.get_city(city)
        if coords is None:
            self.display_error(
                "City not found or network error:\nCheck the city name or your connection"
            )
            return

        lat, lon = coords
        self.coordinates_label.setText(f"Lat: {lat:.4f}, Lon: {lon:.4f}")

        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}

        try:
            response = requests.get(weather_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if int(data.get("cod", 0)) == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            status_code = None
            if getattr(http_error, "response", None) is not None:
                status_code = getattr(http_error.response, "status_code", None)
            match status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def get_city(self, city):
        coordinate_url = "http://api.openweathermap.org/geo/1.0/direct"
        """Return (lat, lon) for the given city using the geocoding API, or None."""
        coordinate_params = {"q": city, "appid": API_KEY, "limit": 1}
        try:
            response = requests.get(
                coordinate_url, params=coordinate_params, timeout=10
            )
            response.raise_for_status()
            city_data = response.json()
            if not city_data:
                return None
            return city_data[0]["lat"], city_data[0]["lon"]
        except requests.exceptions.RequestException:
            return None

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.coordinates_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_c = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
