"""
This file defines the shared state for the AI marketing agent system.
It acts as the central "memory" that is passed between the different agent nodes in the graph.
"""
from typing import TypedDict, List, Optional, Dict

class AgentState(TypedDict):
    """
    The shared state for the AI marketing agent.

    Attributes:
        cafe_context: The content of the cafe_context.md file.
        weather_summary: A summary of the weather for the day.
        food_recommendation: A food recommendation based on the weather.
        events: A list of the top 5 events of the day, each with a title and postcode.
        message_ideas: A list of 5 message ideas, one for each event.
        final_social_post: The final, ready-to-publish social media post.
        errors: A list to accumulate any errors that occur during the workflow.
    """
    cafe_context: str
    weather_summary: Optional[str]
    food_recommendation: Optional[str]
    events: Optional[List[Dict[str, str]]]
    message_ideas: Optional[List[str]]
    final_social_post: Optional[dict]
    errors: List[str]