from google.adk.agents import Agent
import requests

class SpaceXAgent(Agent):
    def __init__(self):
        super().__init__(name="SpaceXAgent", description="Fetches the next SpaceX launch and its coordinates.")

    def get_next_launch_details(self) -> dict:
        try:
            url = "https://api.spacexdata.com/v3/launches/next"
            res = requests.get(url)
            data = res.json()
            return {
                "status": "success",
                "launch_data": {
                    "mission_name": data.get("mission_name"),
                    "launch_date_utc": data.get("launch_date_utc"),
                    "site": data["launch_site"].get("site_name_long"),
                    "rocket": data["rocket"].get("rocket_name"),
                    "details": data.get("details", "No details available."),
                    "upcoming": data.get("upcoming", True),
                    "site_name": data["launch_site"].get("site_name")
                }
            }
        except Exception as e:
            return {"status": "error", "error_message": str(e)}

    def resolve_site_to_latlon(self, site_name: str) -> tuple:
        try:
            url = "https://api.spacexdata.com/v4/launchpads"
            res = requests.get(url).json()
            for pad in res:
                if pad['name'].lower() == site_name.lower():
                    return pad['latitude'], pad['longitude']
            return None, None
        except Exception:
            return None, None

    def run(self, input_text: str, state: dict) -> dict:
        result = self.get_next_launch_details()
        state["spacex_status"] = result["status"]

        if result["status"] == "success":
            state["launch_data"] = result["launch_data"]
            site_name = result["launch_data"].get("site_name", "")
            lat, lon = self.resolve_site_to_latlon(site_name)
            state["latlon"] = (lat, lon) if lat is not None and lon is not None else None
        else:
            state["spacex_error"] = result.get("error_message", "Unknown error")

        return state
