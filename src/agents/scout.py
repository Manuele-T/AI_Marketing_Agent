import json
from langchain_openai import ChatOpenAI

# --- IMPORTS ---
# Importing AgentState from the core folder
from src.core.state import AgentState
# Importing tools from the tools folder (file name is tools.py)
from src.tools.tools import get_weather, perform_internet_search, parse_rss_feeds

# Initialize the LLM
# Using a specific model and a temperature of 0 for predictable, factual outputs.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

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
    """
    print("--- AGENT: SCOUT ---")

    # 1. Define search parameters
    location = "Glasgow, UK"
    search_queries = [
        "events in Glasgow today",
        "events in glasgow west end today",
        "conferences in Glasgow today"
    ]

    # RSS feeds for Glasgow news, events, and culture
    rss_feed_urls = [
        "http://feeds.bbci.co.uk/news/scotland/rss.xml",  # BBC News Scotland
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
    You are an expert Local Opportunity Scout for a small, cozy cafe in Glasgow.
    Your mission is to analyze the raw data provided below and extract the weather summary and the top 5 most important events of the day, including their postcodes.
    
    **Instructions:**
    1. **Analyze the Data:** Carefully read through the weather, event search results, and news headlines.
    2. **Extract Weather:** Summarize the weather in a single sentence.
    3. **Extract Events:** Identify the top 5 most important events of the day. For each event, provide its title and postcode. If a postcode is not available, use "Not found".
    4. **Format Output:** Your final output must be a JSON object with two keys: 'weather_summary' and 'events'. The 'events' key should contain a list of objects, each with a 'title' and 'postcode' key.
    
    **Example Output:**
    ```json
    {{
        "weather_summary": "Today in Glasgow is bright and mild with a lively social scene beginning.",
        "events": [
            {{"title": "Glasgow Cocktail Fortnight starts today...", "postcode": "G1 1-G2 1"}},
            {{"title": "Glasgow Necropolis new entrance...", "postcode": "G4 0F"}},
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
            return state
        else:
            raise ValueError("No JSON object found in the LLM response.")

    except (ValueError, json.JSONDecodeError) as e:
        error_message = f"Error parsing JSON from scout_node: {e}\nLLM Response:\n{response.content}"
        print(error_message)
        state["errors"].append(error_message)
        return state