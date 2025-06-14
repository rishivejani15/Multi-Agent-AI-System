from google.adk.agents import Agent
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class NewsAgent(Agent):
    def __init__(self):
        super().__init__(name="NewsAgent", description="Fetches recent news related to the launch mission.")

    def run(self, input_text: str, state: dict) -> dict:
        api_key = os.getenv("NEWSAPI_KEY")
        if not api_key:
            state["news_status"] = "failed"
            state["news_error"] = "Missing NewsAPI key"
            return state

        mission = state.get("launch_data", {}).get("mission_name", "SpaceX")
        url = f"https://newsapi.org/v2/everything?q={mission}&sortBy=publishedAt&apiKey={api_key}"

        try:
            res = requests.get(url)
            articles = res.json().get("articles", [])[:5]
            headlines = [a.get("title", "No Title") for a in articles]
            state["news_headlines"] = headlines
            state["news_status"] = "success"
        except Exception as e:
            state["news_status"] = "failed"
            state["news_error"] = str(e)

        return state
