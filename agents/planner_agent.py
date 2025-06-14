class PlannerAgent:
    def process(self, state: dict) -> dict:
        """Parses the user goal and generates an execution plan."""
        goal = state.get("goal", "").lower()
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
