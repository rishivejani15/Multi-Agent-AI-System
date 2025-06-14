from agents.news_agent import NewsAgent
from agents.planner_agent import PlannerAgent
from agents.spacex_agent import SpaceXAgent
from agents.weather_agent import WeatherAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.goal_checker_agent import GoalCheckerAgent

def run_pipeline(state: dict, max_iterations: int = 3) -> dict:
    """Run the agent pipeline with retries."""
    agents = {
        "PlannerAgent": PlannerAgent(),
        "SpaceXAgent": SpaceXAgent(),
        "WeatherAgent": WeatherAgent(),
        "NewsAgent": NewsAgent(),
        "AnalyzerAgent": AnalyzerAgent(),
        "GoalCheckerAgent": GoalCheckerAgent()
    }
    
    for iteration in range(max_iterations):
        state["iteration"] = iteration + 1

        state = agents["PlannerAgent"].process(state)
        if state.get("planner_status") != "success" or not state.get("plan"):
            state["error"] = "Planning failed"
            break

        for agent_name in state["plan"]:
            if agent_name in agents:
                state = agents[agent_name].process(state)
            else:
                state["error"] = f"Unknown agent: {agent_name}"
                break

        if state.get("goal_met", False):
            break
        else:
            print(f"\n🔁 Retrying (Iteration {iteration + 1})...")

    return state

def main():
    """Run the multi-agent system."""
    goal = "Find the next SpaceX launch, check weather at that location, then summarize if it may be delayed."
    state = {"goal": goal}

    state = run_pipeline(state)

    print("Planning:", state.get("plan", []))
    launch_data = state.get("launch_data", {})
    if launch_data:
        print("\n🚀 Launch Info:", launch_data.get("mission_name"), "-", launch_data.get("launch_date_utc"))
    weather_data = state.get("weather_data", {})
    if weather_data and "weather" in weather_data and "main" in weather_data:
        print("\n🌦️ Weather:", weather_data["weather"][0]["main"], "-", weather_data["main"]["temp"], "°C")
    news = state.get("news_headlines", [])
    if news:
        print("\n📰 News Headlines:")
        for headline in news:
            print("-", headline)

    analysis = state.get("analysis", "")
    if analysis:
        print("\n📊 Analysis:", analysis)
    if state.get("goal_met", False):
        print("\n✅ Goal Achieved!")
    else:
        print("\n❌ Goal Not Met:", state.get("error", "Unknown error"))

if __name__ == "__main__":
    main()