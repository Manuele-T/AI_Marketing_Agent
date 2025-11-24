# Autonomous AI Marketing Assistant: Project Plan

## 1. System Overview

This system is a multi-agent AI application designed to function as an autonomous marketing assistant for a small business, such as a local cafe.

The core problem it solves is time poverty for the business owner, who often lacks the time and resources to maintain a consistent and relevant social media presence.

The system automates the marketing workflow by:
1.  **Scanning Local Opportunities:** Each day, it scans online sources like weather forecasts, local news RSS feeds, and Google for events to find a timely "hook" for a social media post.
2.  **Strategic Alignment:** It cross-references this external opportunity with the cafe's internal context (menu, specials, brand identity, goals) to formulate a specific, strategic marketing angle.
3.  **Content Creation & Refinement:** It then generates a complete, ready-to-publish social media post, including a caption and an image prompt. A key feature is its internal self-correction loop, where it drafts the post, critiques its own work against brand guidelines, and then refines it for a high-quality final output.

The final result is a daily, on-brand social media post that is contextually relevant, requiring only a single click for approval by the owner.

## 2. Tech Stack

*   **Programming Language:** Python
*   **Orchestration Framework:** LangGraph (for structuring the AI workflow as a stateful graph of interacting agents).
*   **Language Model (LLM):** OpenAI API (e.g., GPT-4 series) will serve as the reasoning engine for all agents.
*   **User Interface:** Streamlit (for creating a simple, local web interface for the cafe owner to interact with the system).
*   **External Data APIs:**
    *   **Weather API:** A service like OpenWeatherMap to fetch daily weather data.
    *   **Internet Search API:** A service like SerpApi to perform Google Searches for local events, news, and trending topics.
    *   **RSS Feed Parser:** The `feedparser` Python library to parse local news blogs and community calendars.
*   **Environment & Dependency Management:**
    *   **Virtual Environment:** Python `venv` to isolate project dependencies.
    *   **Credential Management:** `python-dotenv` to securely manage API keys via a `.env` file.

## 3. Developer Tools

*   **Code Editor:** VS Code (or any preferred code editor).
*   **Terminal:** The integrated terminal within VS Code is sufficient for running the application and installing packages.
*   **Workflow Visualization:** **Graphviz**. This is a prerequisite tool used by LangGraph to visually render the agent interaction graph. It must be installed on the system to generate the workflow diagrams.
    *   **System-Level Install:** Install Graphviz on your operating system (e.g., via Homebrew on Mac, `apt-get` on Linux, or the official installer on Windows).
    *   **Python Library:** Install the Python wrapper via pip: `pip install pygraphviz`.

## 4. Development Steps

This project will be built in a chronological order that prioritizes foundational components first.

### Phase 1: Setup and Foundations
1.  **Environment Setup:** Create a Python virtual environment (`venv`) and install all necessary libraries from a `requirements.txt` file (`langchain`, `langgraph`, `openai`, `streamlit`, `python-dotenv`, `feedparser`, `serpapi-google-search`, etc.).
2.  **API & Service Access:** Obtain API keys for OpenAI, a Weather API, and a Google Search API service.
3.  **Secure Credentials:** Create a `.env` file and store all API keys within it.
4.  **Cafe Context File:** Create a `cafe_context.txt` file. Populate it with initial details about the cafe's menu, brand voice (e.g., "cozy, artisanal"), and marketing goals (e.g., "sell more baked goods").

### Phase 2: Define Core Components in Code
1.  **The Tools:** Create a `tools.py` file. Write the plain Python functions that will be the agent's capabilities: `get_weather(location)`, `perform_internet_search(query)`, and `parse_rss_feeds(urls)`.
2.  **The State:** Define the shared `AgentState` using Python's `TypedDict`. This class will act as the "memory" of the graph and will include fields like `scout_brief: str`, `strategist_instruction: str`, and `final_social_post: dict`.

### Phase 3: Build the Agent Nodes
Each agent is a Python function that receives the current state and returns an updated state.
1.  **Scout Node:** Write the function for the `Local Opportunity Scout`. This node will:
    *   Call the tool functions (weather, search, RSS).
    *   Pass the collected data to the LLM with a prompt asking it to summarize the key marketing hooks for the day.
    *   Return the state with the `scout_brief` field updated.
2.  **Strategist Node:** Write the function for the `Daily Strategist`. This node will:
    *   Read the `scout_brief` and the `cafe_context` from the state.
    *   Use an LLM call with a prompt that asks it to connect a hook to a menu item and produce a clear instruction.
    *   Return the state with the `strategist_instruction` field updated.
3.  **Content Creator Node:** Write the function for the `Content Creator`. This node implements the self-correction loop:
    *   It uses a single, sophisticated multi-part prompt that instructs the LLM to perform three steps in order:
        1.  **Draft:** Generate a first draft of the social media post.
        2.  **Critique:** Review the draft against a predefined checklist (e.g., brand voice, call to action, clarity).
        3.  **Revise:** Generate the final, improved version based on the critique.
    *   Return the state with the `final_social_post` field updated with the revised content.

### Phase 4: Assemble and Visualize the Graph
1.  **Instantiate Graph:** In your main script, create an instance of `langgraph.graph.StateGraph(AgentState)`.
2.  **Add Nodes:** Add each agent function as a node to the graph (e.g., `workflow.add_node("scout", scout_node)`).
3.  **Define Edges:** Create the sequential pathways. For this linear workflow, it will be `workflow.set_entry_point("scout")` followed by `workflow.add_edge("scout", "strategist")`, etc.
4.  **Compile:** Compile the graph into a runnable application: `app = workflow.compile()`.
5.  **Visualize:** Immediately after compiling, add the line `app.get_graph().draw_png('workflow_diagram.png')` to automatically generate a visual diagram of the agent system.

### Phase 5: Build UI and Package for Delivery
1.  **Streamlit UI:** Create the user interface in a file like `ui.py`.
    *   Add a title and a simple explanation.
    *   Create a text area that allows the user to view and edit the `cafe_context.txt` file.
    *   Add a "Generate Today's Post" button.
    *   Include a display area to show a "loading" status and present the `final_social_post` once ready.
2.  **Integration:** Wire the "Generate" button to call the compiled LangGraph app (`app.invoke(...)`) and display the result.
3.  **Packaging for Friend:** To make it easy for the non-technical friend to run:
    *   Organize all code into a single folder.
    *   Include a `requirements.txt` file.
    *   Create a simple `run.bat` (for Windows) or `run.sh` (for Mac/Linux) script that automatically installs the dependencies (`pip install -r requirements.txt`) and then launches the application (`streamlit run ui.py`).