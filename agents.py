# agents.py
"""
This file contains the Python functions that define the agent nodes in our LangGraph workflow.
Each function takes the current agent state and returns an updated state.
"""

import os
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
    1. Defines the search parameters (location, search query, RSS feeds).
    2. Calls the tools (get_weather, perform_internet_search, parse_rss_feeds) to gather raw data.
    3. Compiles the raw data into a single string.
    4. Creates a detailed prompt instructing the LLM to analyze the data.
    5. Invokes the LLM to generate a concise "scout brief".
    6. Updates the `scout_brief` in the agent state.

    Args:
        state (AgentState): The current state of the workflow.

    Returns:
        AgentState: The updated state with the new scout_brief.
    """
    print("--- AGENT: SCOUT ---")

    # 1. Define search parameters
    location = "Glasgow, UK"
    search_query = "conferences and events in Glasgow today"
    
    # Real RSS feeds for Glasgow news, events, and culture
    rss_feed_urls = [
        "http://feeds.bbci.co.uk/news/scotland/rss.xml", # BBC News Scotland
        "https://www.glasgowlive.co.uk/rss.xml",          # Glasgow Live
        "https://www.whatsonglasgow.co.uk/rss/news/",     # What's On Glasgow
    ]

    # 2. Call tools to gather data
    weather_data = get_weather(location)
    search_data = perform_internet_search(search_query)
    rss_data = parse_rss_feeds(rss_feed_urls)

    # 3. Compile the raw data into a single context string
    # This structured format helps the LLM differentiate between data sources.
    compiled_data = f"""
    --- RAW DATA START ---

    ### Current Weather in {location}
    {weather_data}

    ### Top Google Search Results for "{search_query}"
    {search_data}

    ### Latest News from Local RSS Feeds
    {rss_data}

    --- RAW DATA END ---
    """

    # 4. Create the detailed prompt for the LLM
    # This prompt is crucial. It sets the persona, goal, constraints, and output format.
    prompt = f"""
    You are an expert Local Opportunity Scout for a small, cozy cafe in Glasgow called "Kahawa Mzuri".

    Your mission is to analyze the raw data provided below and identify the top 2-3 most actionable marketing hooks for the day. A "hook" is a specific event, weather condition, or piece of news that the cafe can use to create a relevant social media post.

    **Instructions:**
    1.  **Analyze the Data:** Carefully read through the weather, event search results, and news headlines.
    2.  **Identify Key Hooks:** Look for specific, actionable opportunities. Examples include:
        -   Major weather conditions (e.g., "very sunny and warm," "heavy rain all day").
        -   Specific local events with names and locations (e.g., "Glasgow International Comedy Festival at King's Theatre," "Farmers Market at Queen's Park").
        -   Significant local news that creates a shared community feeling.
    3.  **Ignore the Noise:** Disregard generic news, old events, or uninteresting weather (e.g., "partly cloudy").
    4.  **Synthesize, Don't Suggest:** Your job is ONLY to summarize the opportunities. Do NOT suggest any marketing ideas, menu pairings, or social media text. Simply report the facts.

    **Output Format:**
    Your final output must be a concise, factual brief. Start with a single-sentence summary of the day's general vibe, then list the key hooks as clear, distinct bullet points.

    **Example Output:**
    "Today in Glasgow is shaping up to be cool and culturally active.
    - Weather: Heavy rain is expected throughout the afternoon.
    - Event: The Merchant City Festival starts today, with street performances on Argyle Street.
    - News: The local football team, Glasgow Rangers, won their match last night."

    Now, analyze the following data and generate the brief.

    {compiled_data}
    """

    # 5. Invoke the LLM to get the scout brief
    response = llm.invoke(prompt)
    scout_brief = response.content

    print(f"Scout Brief:\n{scout_brief}")

    # 6. Update the state
    state["scout_brief"] = str(scout_brief)
    return state

