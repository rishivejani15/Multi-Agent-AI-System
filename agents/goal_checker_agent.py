class GoalCheckerAgent:
    def is_goal_met(self, result: str) -> bool:
        """Check if the goal is met based on analysis."""
        return "delayed" in result.lower() or "clear" in result.lower()

    def process(self, state: dict) -> dict:
        """Check if the goal is met and save result."""
        if state.get("analyzer_status") == "success" and state.get("analysis"):
            state["goal_met"] = self.is_goal_met(state["analysis"])
            state["goal_status"] = "success"
        else:
            state["goal_met"] = False
            state["goal_status"] = "failed"
        return state