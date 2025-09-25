"""
This file contains the tools for the AI marketing agent, including functions
to get the weather, perform internet searches, and parse RSS feeds.
"""
import os
import requests
import feedparser
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_weather(location: str = "Glasgow, UK") -> str:
    """
    Gets the current weather for a given location using the OpenWeatherMap API.
    Returns a string summarizing the weather conditions.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Error: WEATHER_API_KEY not found in environment variables."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"  # Use Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']

        return f"Current weather in {location}: {weather_description}, Temperature: {temperature}°C."

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    except KeyError:
        return f"Error: Unexpected response format from weather API for location '{location}'."


def perform_internet_search(query: str) -> str:
    """
    Performs an internet search for a given query using the SerpApi.
    Returns a string summarizing the top search results.
    """
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        return "Error: SERP_API_KEY not found in environment variables."

    params = {
        "api_key": api_key,
        "engine": "google",
        "q": query,
    }

    try:
        client = GoogleSearch(params)
        results = client.get_dict()

        if "organic_results" in results and results["organic_results"]:
            snippets = [
                f"Title: {result.get('title', 'N/A')}\nSnippet: {result.get('snippet', 'N/A')}"
                for result in results["organic_results"][:3] # Get top 3 results
            ]
            return "\n\n".join(snippets)
        else:
            return f"No good search results found for '{query}'."

    except Exception as e:
        return f"Error performing search: {e}"


def parse_rss_feeds(urls: list[str]) -> str:
    """
    Parses RSS feeds from a list of URLs and returns the titles of the latest entries.
    """
    all_titles = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
            # Explicitly cast titles to strings to resolve type errors
            feed_title = str(feed.feed.title)  # type: ignore
            titles = [str(entry.title) for entry in feed.entries[:5]]
            if titles:
                all_titles.append(f"--- From {feed_title} ---\n" + "\n".join(titles))
        except Exception as e:
            all_titles.append(f"Could not parse feed from {url}. Error: {e}")

    if not all_titles:
        return "No RSS feeds could be parsed or they were empty."

    return "\n\n".join(all_titles)