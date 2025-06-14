import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAgent:
    def get_weather(self, lat: float, lon: float) -> dict:
        """Fetch weather from OpenWeatherMap API."""
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Check your .env file or environment variables.")
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            response = requests.get(url)
            return {"status": "success", "weather_data": response.json()}
        except Exception as e:
            return {"status": "error", "error_message": str(e)}

    def process(self, state: dict) -> dict:
        """Fetch weather data for the launch location."""
        if state.get("latlon") and state["latlon"] != (None, None):
            lat, lon = state["latlon"]
            weather_result = self.get_weather(lat, lon)
            state["weather_status"] = weather_result["status"]
            if weather_result["status"] == "success":
                state["weather_data"] = weather_result["weather_data"]
            else:
                state["weather_error"] = weather_result["error_message"]
        else:
            state["weather_status"] = "failed"
            state["weather_error"] = "Invalid or missing coordinates"
        return state