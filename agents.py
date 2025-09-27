# agents.py
"""
This file contains the Python functions that define the agent nodes in our LangGraph workflow.
Each function takes the current agent state and returns an updated state.
"""

import os
import json
from langchain_openai import ChatOpenAI

# Import state and tools
from state import AgentState
from tools import get_weather, perform_internet_search, parse_rss_feeds


# Initialize the LLM
# Using a specific model and a temperature of 0 for predictable, factual outputs.
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def scout_node(state: AgentState) -> AgentState:
    """
    The first agent in the workflow. It scans for local opportunities.

    This node performs the following steps:
    1. Defines the search parameters (location, search queries, RSS feeds).
    2. Calls the tools (get_weather, perform_internet_search, parse_rss_feeds) to gather raw data.
    3. Compiles the raw data into a single string.
    4. Creates a detailed prompt instructing the LLM to analyze the data and extract key information.
    5. Invokes the LLM to generate a JSON object containing the weather summary and top 5 events.
    6. Updates the agent state with the extracted information.

    Args:
        state (AgentState): The current state of the workflow.

    Returns:
        AgentState: The updated state with the new weather_summary and events.
    """
    print("--- AGENT: SCOUT ---")

    # 1. Define search parameters
    location = "Glasgow, UK"
    search_queries = [
        "events in Glasgow today",
        "events in glasgow west end today",
        "conferences in Glasgow today"
    ]
    
    # Real RSS feeds for Glasgow news, events, and culture
    rss_feed_urls = [
        "http://feeds.bbci.co.uk/news/scotland/rss.xml", # BBC News Scotland
        "https://www.glasgowlive.co.uk/rss.xml",          # Glasgow Live
        "https://www.whatsonglasgow.co.uk/rss/news/",     # What's On Glasgow
    ]

    # 2. Call tools to gather data
    weather_data = get_weather(location)
    search_data = "\n".join([perform_internet_search(query) for query in search_queries])
    rss_data = parse_rss_feeds(rss_feed_urls)

    # 3. Compile the raw data into a single context string
    compiled_data = f"""
    --- RAW DATA START ---

    ### Current Weather in {location}
    {weather_data}

    ### Top Google Search Results for "{search_queries}"
    {search_data}

    ### Latest News from Local RSS Feeds
    {rss_data}

    --- RAW DATA END ---
    """

    # 4. Create the detailed prompt for the LLM
    prompt = f"""
    You are an expert Local Opportunity Scout for a small, cozy cafe in Glasgow called "Glasgow Cozy Bean".

    Your mission is to analyze the raw data provided below and extract the weather summary and the top 5 most important events of the day, including their postcodes.

    **Instructions:**
    1.  **Analyze the Data:** Carefully read through the weather, event search results, and news headlines.
    2.  **Extract Weather:** Summarize the weather in a single sentence.
    3.  **Extract Events:** Identify the top 5 most important events of the day. For each event, provide its title and postcode. If a postcode is not available, use "Not found".
    4.  **Format Output:** Your final output must be a JSON object with two keys: 'weather_summary' and 'events'. The 'events' key should contain a list of objects, each with a 'title' and 'postcode' key.

    **Example Output:**
    ```json
    {{
        "weather_summary": "Today in Glasgow is bright and mild with a lively social scene beginning.",
        "events": [
            {{"title": "Glasgow Cocktail Fortnight starts today, featuring masterclasses and activities at top city bars.", "postcode": "G1 1-G2 1"}},
            {{"title": "Glasgow Necropolis is set to receive a new east end entrance following recent funding approval.", "postcode": "G4 0F"}},
            {{"title": "Event 3", "postcode": "Not found"}},
            {{"title": "Event 4", "postcode": "G12 8"}},
            {{"title": "Event 5", "postcode": "G3 8YW"}}
        ]
    }}
    ```

    Now, analyze the following data and generate the JSON object.

    {compiled_data}
    """

    # 5. Invoke the LLM to get the scout brief
    response = llm.invoke(prompt)
    try:
        # The LLM's response content is a string that often includes ```json ... ```
        # We need to extract the JSON part cleanly.
        content = str(response.content)
        
        # Find the start and end of the JSON object
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        
        if json_start_index != -1 and json_end_index != -1:
            json_response_string = content[json_start_index:json_end_index+1]
            scout_data = json.loads(json_response_string)
            
            print(f"Scout Output:\n{scout_data}")

            # 6. Update the state
            state["weather_summary"] = scout_data.get("weather_summary")
            state["events"] = scout_data.get("events")
        else:
            raise ValueError("No JSON object found in the LLM response.")

    except (ValueError, json.JSONDecodeError) as e:
        error_message = f"Error parsing JSON from scout_node: {e}\nLLM Response:\n{response.content}"
        print(error_message)
        state["errors"].append(error_message)

    return state

def strategist_node(state: AgentState) -> AgentState:
    """
    The second agent in the workflow. It creates a marketing strategy.

    This node performs the following steps:
    1.  Reads the `weather_summary`, `events`, and `cafe_context` from the state.
    2.  Creates a detailed prompt that instructs the LLM to act as a marketing strategist.
    3.  The prompt asks the LLM to generate a food recommendation based on the weather and five message ideas based on the events.
    4.  Invokes the LLM to generate a JSON object with the food recommendation and message ideas.
    5.  Updates the `food_recommendation` and `message_ideas` in the agent state.

    Args:
        state (AgentState): The current state of the workflow.

    Returns:
        AgentState: The updated state with the new food_recommendation and message_ideas.
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
    1.  **Analyze the Inputs:** Carefully review the weather summary, the list of events, and the cafe's marketing playbook.
    2.  **Generate Food Recommendation:** Based on the weather, suggest a suitable food item from the menu.
    3.  **Generate Message Ideas:** For each of the five events, create a short, engaging message to attract attendees to the cafe. Include a relevant hashtag.
    4.  **Format Output:** Your final output must be a JSON object with two keys: 'food_recommendation' and 'message_ideas'.

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
        # The LLM's response content is a string that often includes ```json ... ```
        # We need to extract the JSON part cleanly.
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
        else:
            raise ValueError("No JSON object found in the LLM response.")

    except (ValueError, json.JSONDecodeError) as e:
        error_message = f"Error parsing JSON from strategist_node: {e}\nLLM Response:\n{response.content}"
        print(error_message)
        state["errors"].append(error_message)

    return state
