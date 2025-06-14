from google.adk.agents import Agent

class PlannerAgent(Agent):
    def __init__(self):
        super().__init__(name="PlannerAgent", description="Plans which agents need to run based on the user's goal.")

    def run(self, input_text: str, state: dict) -> dict:
        goal = state.get("goal", input_text).lower()
        plan = []

        if "spacex" in goal:
            plan.append("SpaceXAgent")
        if "weather" in goal:
            plan.append("WeatherAgent")
        if "news" in goal or "update" in goal or "spacex" in goal:
            plan.append("NewsAgent")
        if "weather" in goal or "spacex" in goal:
            plan.append("AnalyzerAgent")
            plan.append("GoalCheckerAgent")

        state["plan"] = plan
        state["planner_status"] = "success" if plan else "failed"
        return state
