# Weather App

A simple desktop weather application built with **PyQt5** and the **OpenWeatherMap API**.
Enter any city name to view the current temperature, description, and coordinates in a clean graphical interface.

---

## Requirements

All dependencies are listed in `requirements.txt`.
Packages include:

* `requests`
* `python-dotenv`
* `PyQt5`

Install them with:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Setup

1. **Clone the repository** (or copy the files to a directory):

   ```bash
   git clone https://github.com/triceraz/weather_app.git
   cd weather_app
   ```

2. **Create a `.env` file** in the project root and add your OpenWeatherMap API key:

   ```bash
   OPENWEATHER_API_KEY=your_api_key_here
   ```

   > You can get a free API key by signing up at [OpenWeatherMap](https://openweathermap.org/api).

3. **Run the app:**

   ```bash
   python3 weather_app.py
   ```

---

## Usage

1. Launch the app.
2. Type a city name (e.g., `London`, `Tokyo`, `New York`).
3. Click **“Get Weather”**.
4. View:

   * Temperature (°C)
   * Coordinates (latitude and longitude)
   * Weather description
