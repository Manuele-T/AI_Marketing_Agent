from langgraph.graph import StateGraph, END

# --- FIX: USE RELATIVE IMPORTS ---
# Use a dot (.) to say "from the file in this same folder"
from .state import AgentState

# Use two dots (..) to say "go up one folder (to src), then into agents"
from ..agents.scout import scout_node
from ..agents.strategist import strategist_node
from ..agents.creator import creator_node

# 1. Create a new StateGraph with our AgentState
workflow = StateGraph(AgentState)

# 2. Add the agent nodes to the graph
workflow.add_node("scout", scout_node)
workflow.add_node("strategist", strategist_node)
workflow.add_node("creator", creator_node)

# 3. Define the edges that control the flow
workflow.set_entry_point("scout")
workflow.add_edge("scout", "strategist")
workflow.add_edge("strategist", "creator")

# The creator_node is the final step, so we add an edge from it to the END
workflow.add_edge("creator", END)

# 4. Compile the graph into a runnable application
app = workflow.compile()

# 5. (Optional) Generate a visualization
# Note: To run this specific block to generate the image, you must run from the root:
# python -m src.core.graph
if __name__ == "__main__":
    try:
        image_bytes = app.get_graph().draw_png() # type: ignore
        with open("workflow_graph.png", "wb") as f:
            f.write(image_bytes)
        print("Successfully generated workflow_graph.png")
    except Exception as e:
        print(f"Warning: Could not generate graph visualization. Make sure Graphviz is installed. Error: {e}")