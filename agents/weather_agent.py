from google.adk.agents import Agent
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAgent(Agent):
    def __init__(self):
        super().__init__(name="WeatherAgent", description="Fetches current weather at the launch site.")

    def get_weather(self, lat: float, lon: float) -> dict:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("OPENWEATHER_API_KEY not set in environment variables.")

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            response = requests.get(url)
            return {"status": "success", "weather_data": response.json()}
        except Exception as e:
            return {"status": "error", "error_message": str(e)}

    def run(self, input_text: str, state: dict) -> dict:
        latlon = state.get("latlon")
        if latlon and isinstance(latlon, tuple) and None not in latlon:
            lat, lon = latlon
            result = self.get_weather(lat, lon)
            state["weather_status"] = result["status"]

            if result["status"] == "success":
                state["weather_data"] = result["weather_data"]
            else:
                state["weather_error"] = result["error_message"]
        else:
            state["weather_status"] = "failed"
            state["weather_error"] = "Missing or invalid coordinates."

        return state
