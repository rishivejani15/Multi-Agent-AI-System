from google.adk.agents import Agent

class GoalCheckerAgent(Agent):
    def __init__(self):
        super().__init__(name="GoalCheckerAgent", description="Checks whether the overall goal has been achieved.")

    def is_goal_met(self, result: str) -> bool:
        return "delayed" in result.lower() or "clear" in result.lower()

    def run(self, input_text: str, state: dict) -> dict:
        if state.get("analyzer_status") == "success" and state.get("analysis"):
            state["goal_met"] = self.is_goal_met(state["analysis"])
            state["goal_status"] = "success"
        else:
            state["goal_met"] = False
            state["goal_status"] = "failed"
        return state
