# notifier.py
"""
Contains the function for sending the final social media post to a Discord channel.

This module is a self-contained utility for delivering the output of the agent workflow.
It reads the Discord webhook URL from the environment variables and formats the post
content into a readable "embed" message.
"""

import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from the .env file in the project root
load_dotenv()

def send_to_discord(state: Dict[str, Any]) -> None:
    """
    Sends the generated social media post to a Discord channel using a webhook.

    Args:
        state (Dict[str, Any]):
            A dictionary expected to contain 'weather_summary', 'food_recommendation', 'events', and 'message_ideas' keys.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    # 1. Validate the Webhook URL
    if not webhook_url:
        print("ERROR: DISCORD_WEBHOOK_URL not found in .env file. Cannot send notification.")
        return

    # 2. Validate the input content
    if not state or not isinstance(state, dict):
        print("ERROR: State is invalid. Cannot send notification.")
        return

    weather_summary = state.get("weather_summary", "*No weather summary was generated.*")
    food_recommendation = state.get("food_recommendation", "*No food recommendation was generated.*")
    events = state.get("events", [])
    message_ideas = state.get("message_ideas", [])

    # 3. Format the data for Discord's embed structure for a clean look
    data = {
        "content": "✨ **New Social Media Post Ideas Ready for Review** ✨",
        "embeds": [
            {
                "title": "Weather Summary",
                "description": weather_summary,
                "color": 5814783  # A pleasant blue color
            },
            {
                "title": "Food Recommendation",
                "description": food_recommendation,
                "color": 15258703  # A warm orange color
            },
            {
                "title": "Top 5 Events",
                "description": "\n".join([f"- {event['title']} (Postcode: {event['postcode']})" if event['postcode'] != 'Not found' else f"- {event['title']}" for event in events]) if events else "*No events were found.*",
                "color": 3447003 # A vibrant green color
            },
            {
                "title": "Message Ideas",
                "description": "\n".join([f"- {idea}" for idea in message_ideas]) if message_ideas else "*No message ideas were generated.*",
                "color": 10181046 # A deep purple color
            }
        ]
    }

    # 4. Send the request to Discord
    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        # This will raise an exception for HTTP error codes (4xx or 5xx)
        response.raise_for_status()
        print("Successfully sent post to Discord for review.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending post to Discord: {e}")


# This block allows you to test the notifier directly
if __name__ == "__main__":
    print("Running notifier.py in standalone test mode...")

    # Create a dummy post to send
    test_post = {
        "caption": "This is a test caption from `notifier.py`! If you see this, the webhook is working correctly. 🚀",
        "image_prompt": "A test image prompt for a cute robot sending a message."
    }

    # You must have your DISCORD_WEBHOOK_URL in your .env file for this to work
    send_to_discord(test_post)
