import requests

class SpaceXAgent:
    def get_next_launch_details(self) -> dict:
        """Fetch next SpaceX launch from API."""
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
        """Resolve SpaceX launchpad to latitude and longitude."""
        try:
            url = "https://api.spacexdata.com/v4/launchpads"
            res = requests.get(url).json()
            for pad in res:
                if pad['name'].lower() == site_name.lower():
                    return pad['latitude'], pad['longitude']
            return None, None
        except Exception:
            return None, None

    def process(self, state: dict) -> dict:
        """Fetch launch details and coordinates, save to state."""
        launch_result = self.get_next_launch_details()
        state["spacex_status"] = launch_result["status"]
        if launch_result["status"] == "success":
            state["launch_data"] = launch_result["launch_data"]
            site_name = state["launch_data"]["site_name"]
            lat, lon = self.resolve_site_to_latlon(site_name)
            state["latlon"] = (lat, lon) if lat is not None and lon is not None else None
        else:
            state["spacex_error"] = launch_result["error_message"]
        return state