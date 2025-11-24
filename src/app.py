# app.py
"""
This is the main application script. It runs the entire agent workflow.

This script does the following:
1.  Imports the compiled LangGraph app object.
2.  Loads the cafe context from the .md file.
3.  Defines the initial state for the workflow.
4.  Invokes the agent graph to run the full process.
5.  Checks the final state for errors or a final post.
6.  If successful, it calls the notifier to send the post to Discord.
"""

from src.core.graph import app
from src.core.state import AgentState
from src.tools.notifier import send_to_discord

def run_workflow(cafe_context: str):
    """
    Defines initial state and runs the agent workflow using the provided context.
    """
    # 1. Define the initial state for the workflow
    initial_state = AgentState(
        cafe_context=cafe_context,
        weather_summary=None,
        food_recommendation=None,
        events=None,
        message_ideas=None,
        brief=None,
        errors=[]
    )

    print("🚀 Starting AI Marketing Assistant Workflow...")

    # 2. Invoke the graph
    final_state = app.invoke(initial_state)

    print("\n🏁 Workflow Finished.")
    print("--------------------")

    # 3. Check for errors and get the final brief
    if not final_state:
        print("❌ Workflow failed to return a final state.")
        return None

    errors = final_state.get("errors", [])
    brief = final_state.get("brief")

    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"- {error}")
        return None # Return None if there were errors
    
    if not brief:
        print("\n❌ Workflow finished, but no brief was generated.")
        return None

    print("Final post generated successfully.")
    # 4. Call the notifier to send the post to Discord
    send_to_discord(brief)
    
    # 5. Return the final brief for the UI
    return brief

# This allows us to run the workflow directly from the terminal
if __name__ == "__main__":
    try:
        with open("cafe_context.md", "r", encoding="utf-8") as f:
            context = f.read()
        run_workflow(context)
    except FileNotFoundError:
        print("Error: cafe_context.md not found.")
