class AnalyzerAgent:
    def analyze(self, weather: dict) -> str:
        """Analyze weather to predict launch delays."""
        try:
            condition = weather['weather'][0]['main']
            wind_speed = weather['wind']['speed']
            if condition in ['Rain', 'Thunderstorm'] or wind_speed > 12:
                return "Launch may be delayed due to weather conditions."
            return "Weather is clear. Launch unlikely to be delayed."
        except Exception as e:
            return f"Analysis failed: {str(e)}"

    def process(self, state: dict) -> dict:
        """Analyze weather data and save result."""
        if state.get("weather_status") == "success" and state.get("weather_data"):
            state["analysis"] = self.analyze(state["weather_data"])
            state["analyzer_status"] = "success"
        else:
            state["analysis"] = "Analysis failed: No weather data available"
            state["analyzer_status"] = "failed"
        return state