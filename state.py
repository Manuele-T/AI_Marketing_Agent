"""
This file defines the shared state for the AI marketing agent system.
It acts as the central "memory" that is passed between the different agent nodes in the graph.
"""
from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    """
    The shared state for the AI marketing agent.

    Attributes:
        cafe_context: The content of the cafe_context.md file.
        scout_brief: A summary of local opportunities (weather, events).
        strategist_instruction: A specific instruction for the Content Creator.
        final_social_post: The final, ready-to-publish social media post.
        errors: A list to accumulate any errors that occur during the workflow.
    """
    cafe_context: str
    scout_brief: Optional[str]
    strategist_instruction: Optional[str]
    final_social_post: Optional[dict]
    errors: List[str]