import json
from langchain_openai import ChatOpenAI

# --- IMPORTS ---
# Importing AgentState from the core folder
from src.core.state import AgentState

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def strategist_node(state: AgentState) -> AgentState:
    """
    The second agent in the workflow. It creates a marketing strategy.
    
    This node performs the following steps:
    1. Reads the `weather_summary`, `events`, and `cafe_context` from the state.
    2. Creates a detailed prompt that instructs the LLM to act as a marketing strategist.
    3. The prompt asks the LLM to generate a food recommendation based on the weather and five message ideas based on the events.
    4. Invokes the LLM to generate a JSON object with the food recommendation and message ideas.
    5. Updates the `food_recommendation` and `message_ideas` in the agent state.
    """
    print("--- AGENT: STRATEGIST ---")

    # 1. Read the necessary data from the state
    weather_summary = state["weather_summary"]
    events = state["events"]
    cafe_context = state["cafe_context"]

    # This check is a safeguard. The weather_summary and events should always be present.
    if weather_summary is None or events is None:
        state["errors"].append("Weather summary or events are missing.")
        return state

    # 2. Create the detailed prompt for the LLM
    prompt = f"""
    You are the expert Marketing Strategist for a small cafe called "The Daily Grind".
    Your task is to analyze the weather and events and create a food recommendation and five message ideas.
    
    **Instructions:**
    1. **Analyze the Inputs:** Carefully review the weather summary, the list of events, and the cafe's marketing playbook.
    2. **Generate Food Recommendation:** Based on the weather, suggest a suitable food item from the menu.
    3. **Generate Message Ideas:** For each of the five events, create a short, engaging message to attract attendees to the cafe. Include a relevant hashtag.
    4. **Format Output:** Your final output must be a JSON object with two keys: 'food_recommendation' and 'message_ideas'.
    
    **Example Output:**
    ```json
    {{
        "food_recommendation": "With this bright and mild weather, our Pistachio Iced Latte is the perfect refreshing treat!",
        "message_ideas": [
            "Going to the conference at Hilton Glasgow today? Grab a coffee with us! #hiltonglasgow",
            "Message idea 2",
            "Message idea 3",
            "Message idea 4",
            "Message idea 5"
        ]
    }}
    ```
    
    ---
    ### Input 1: Weather Summary
    {weather_summary}
    
    ### Input 2: Top 5 Events
    {json.dumps(events, indent=2)}
    
    ### Input 3: Cafe's Marketing Playbook & Context
    {cafe_context}
    ---
    
    Now, based on all the information above, generate the JSON object.
    """

    # 4. Invoke the LLM
    response = llm.invoke(prompt)

    try:
        content = str(response.content)

        # Find the start and end of the JSON object
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')

        if json_start_index != -1 and json_end_index != -1:
            json_response_string = content[json_start_index:json_end_index+1]
            strategist_data = json.loads(json_response_string)

            print(f"Strategist Output:\n{strategist_data}")
            
            # 5. Update the state
            state["food_recommendation"] = strategist_data.get("food_recommendation")
            state["message_ideas"] = strategist_data.get("message_ideas")
            return state
        else:
            raise ValueError("No JSON object found in the LLM response.")

    except (ValueError, json.JSONDecodeError) as e:
        error_message = f"Error parsing JSON from strategist_node: {e}\nLLM Response:\n{response.content}"
        print(error_message)
        state["errors"].append(error_message)
        return state