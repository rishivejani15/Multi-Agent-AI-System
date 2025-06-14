import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NewsAgent:
    def process(self, state: dict) -> dict:
        api_key = os.getenv("NEWSAPI_KEY")
        if not api_key:
            state["error"] = "Missing NewsAPI key"
            return state

        mission = state.get("launch_data", {}).get("mission_name", "SpaceX")
        url = f"https://newsapi.org/v2/everything?q={mission}&sortBy=publishedAt&apiKey={api_key}"

        try:
            res = requests.get(url)
            articles = res.json().get("articles", [])[:5]
            headlines = [a["title"] for a in articles]
            state["news_headlines"] = headlines
        except Exception as e:
            state["error"] = str(e)

        return state
