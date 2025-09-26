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

from graph import app
from state import AgentState
from notifier import send_to_discord

def run_workflow():
    """
    Loads context, defines initial state, and runs the agent workflow.
    """
    # 1. Load the cafe context from the file
    try:
        with open("cafe_context.md", "r", encoding="utf-8") as f:
            cafe_context = f.read()
    except FileNotFoundError:
        print("Error: cafe_context.md not found.")
        return

    # 2. Define the initial state for the workflow
    # This is the input that kicks off the graph.
    initial_state = AgentState(
        cafe_context=cafe_context,
        weather_summary=None,
        food_recommendation=None,
        events=None,
        message_ideas=None,
        final_social_post=None,
        errors=[]
    )

    print("🚀 Starting AI Marketing Assistant Workflow...")

    # 3. Invoke the graph to run the full agent process
    # The `app` object is our compiled workflow from graph.py
    final_state = app.invoke(initial_state)

    print("\n🏁 Workflow Finished.")
    print("--------------------")

    # 4. Check the final state and send notification
    if not final_state:
        print("❌ Workflow failed to return a final state.")
        return

    errors = final_state.get("errors", [])
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Final post generated successfully.")
        # 5. Call the notifier to send the post to Discord
        send_to_discord(final_state)

# This allows us to run the workflow directly from the terminal
# for testing purposes before we build the UI.
if __name__ == "__main__":
    run_workflow()
