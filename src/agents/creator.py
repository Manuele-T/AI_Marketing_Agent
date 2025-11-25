import json

# --- IMPORTS ---
# Importing AgentState from the core folder
from src.core.state import AgentState

def creator_node(state: AgentState) -> AgentState:
    """
    The final agent in the workflow. It assembles the complete marketing brief.
    
    This node performs the following steps:
    1. Reads all the generated content from the state (weather, food, events, messages).
    2. Constructs a final dictionary, the "brief".
    3. Updates the agent state with this final brief.
    """
    print("--- AGENT: CREATOR ---")

    # 1. Read all the necessary data from the state
    weather_summary = state.get("weather_summary")
    food_recommendation = state.get("food_recommendation")
    events = state.get("events")
    message_ideas = state.get("message_ideas")

    # Safeguard against missing data
    if not all([weather_summary, food_recommendation, events, message_ideas]):
        error_message = "Creator node is missing required data from previous nodes."
        print(error_message)
        state["errors"].append(error_message)
        return state

    # 2. Construct the final brief
    brief = {
        "weather_summary": weather_summary,
        "food_recommendation": food_recommendation,
        "events": events,
        "message_ideas": message_ideas,
    }

    print(f"Creator Output:\n{json.dumps(brief, indent=2)}")

    # 3. Update the state with the final brief
    state["brief"] = brief
    
    return state