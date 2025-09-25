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

def send_to_discord(post_content: Dict[str, Any]) -> None:
    """
    Sends the generated social media post to a Discord channel using a webhook.

    Args:
        post_content (Dict[str, Any]):
            A dictionary expected to contain 'caption' and 'image_prompt' keys.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    # 1. Validate the Webhook URL
    if not webhook_url:
        print("ERROR: DISCORD_WEBHOOK_URL not found in .env file. Cannot send notification.")
        return

    # 2. Validate the input content
    if not post_content or not isinstance(post_content, dict) or "caption" not in post_content:
        print("ERROR: Post content is invalid or missing a 'caption'. Cannot send notification.")
        return

    # 3. Format the data for Discord's embed structure for a clean look
    # Hex color codes are used for the vertical bar on the side of the embed.
    data = {
        "content": "✨ **New Social Media Post Ready for Review** ✨",
        "embeds": [
            {
                "title": "Post Caption",
                "description": post_content.get("caption", "*No caption was generated.*"),
                "color": 5814783  # A pleasant blue color
            },
            {
                "title": "AI Image Prompt",
                "description": post_content.get("image_prompt", "*No image prompt was generated.*"),
                "color": 15258703  # A warm orange color
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
