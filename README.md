## AI Marketing Assistant for Small Business

A **multi-agent AI application** designed to act as an autonomous marketing assistant for small businesses, such as local cafes. Built with **LangGraph** and the **OpenAI API**, this system automates the creation of timely, on-brand social media content by analyzing real-time local data.

-----

## Features

  * **Autonomous Opportunity Scouting**: Scans daily **weather forecasts**, **local news** via RSS, and multiple **Google Search** queries for relevant events to identify marketing "hooks."
  * **Strategic Content Generation**: Cross-references opportunities with a user-editable "**Marketing Playbook**" (`cafe_context.md`) to create strategically aligned content.
  * **Multi-Option Briefing**: Produces a **daily marketing brief** with multiple, ready-to-use post ideas: one tailored to the weather and several unique ideas for local events.
  * **Simple Web Interface**: Built with **Streamlit** for easy interaction, allowing the user to edit the marketing playbook, trigger the workflow, and view results.
  * **Automated Discord Notifications**: Sends the final, gracefully formatted brief directly to a **Discord channel** for easy review and approval.

-----

## Tech Stack & Tools

### AI & Orchestration

| Tool | Description |
| :--- | :--- |
| **Python (3.9+)** | The core programming language for the application. |
| **LangGraph** | The primary framework for building the stateful, multi-agent workflow. |
| **LangChain** | Used for core components and integration with the language model. |
| **OpenAI API (GPT-4)** | Serves as the reasoning engine for all agentic tasks. |

### Frontend & UI

| Tool | Description |
| :--- | :--- |
| **Streamlit** | Used to create and serve the simple, interactive web interface. |

### Data & APIs

| Tool | Description |
| :--- | :--- |
| **SerpApi (Google Search)** | For performing real-time searches for local events and news. |
| **OpenWeatherMap API** | For fetching current local weather conditions. |
| **Feedparser** | A Python library for parsing local news RSS feeds. |

### Development & Deployment

| Tool | Description |
| :--- | :--- |
| **Python** | For managing an isolated project environment. |
| **Streamlit Community Cloud** | For deploying the application as a shareable web app. |
| **Git & GitHub** | For version control. |
| **Graphviz** | To generate a visual representation of the agent workflow. |

-----

## Prerequisites

You will need the following to run the project locally:

  * **Python 3.9** or newer
  * **Git**
  * **Graphviz** (for generating the workflow diagram)
  * An **OpenAI API Key**
  * A **SerpApi API Key**
  * A **Weather API Key** (from OpenWeatherMap)
  * A **Discord Webhook URL**

-----

## Getting Started

Follow these instructions to get a local copy of the project up and running.

### 1\. Clone this repository

```bash
git clone https://github.com/Manuele-T/AI_Marketing_Agent
cd AI_Marketing_Agent
```

### 2\. Set up the Python Environment

Create and activate a virtual environment.

**On macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3\. Configure Your API Keys

Create a file named `.env` in the root of the project directory. Copy and paste the following, replacing the placeholder text with your actual keys and URL:

```env
OPENAI_API_KEY="your_openai_key_here"
WEATHER_API_KEY="your_weather_key_here"
SERP_API_KEY="your_serpapi_key_here"
DISCORD_WEBHOOK_URL="your_discord_webhook_url_here"
```

### 4\. Run the Streamlit Application

Use the Streamlit CLI to launch the web interface:

```bash
streamlit run ui.py
```

### 5\. Access the Application

Open your browser and navigate to the local URL provided by Streamlit, typically:

`http://localhost:8501`

-----

## Project Structure 📁

The project is organized into modular, single-responsibility files:

```
ai-marketing-agent/
├── .env                  # Local environment variables (API keys) - Not committed to Git
├── .gitignore            # Specifies files to ignore for Git
├── README.md             # This file
├── requirements.txt      # Project dependencies for pip
├── agents.py             # Contains the core agent logic (Scout, Strategist)
├── app.py                # Main application runner that invokes the graph
├── cafe_context.md       # The user-editable marketing playbook
├── graph.py              # Defines and compiles the LangGraph workflow
├── notifier.py           # Sends the final brief to Discord
├── state.py              # Defines the shared AgentState for the graph
├── tools.py              # Functions for external API calls
└── ui.py                 # The Streamlit user interface code
```