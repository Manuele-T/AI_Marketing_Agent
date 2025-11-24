# graph.py
"""
This file defines and compiles the LangGraph workflow.

It assembles the individual agent nodes into a sequential graph, defining the
flow of data and control from the Scout, to the Strategist, to the Creator.
"""

from langgraph.graph import StateGraph, END
from src.core.state import AgentState
from agents import scout_node, strategist_node, creator_node

# 1. Create a new StateGraph with our AgentState
workflow = StateGraph(AgentState)

# 2. Add the agent nodes to the graph
# Each node corresponds to a function we defined in agents.py
workflow.add_node("scout", scout_node)
workflow.add_node("strategist", strategist_node)
workflow.add_node("creator", creator_node)

# 3. Define the edges that control the flow
# This is a simple, linear workflow.
workflow.set_entry_point("scout")
workflow.add_edge("scout", "strategist")
workflow.add_edge("strategist", "creator")

# The creator_node is the final step, so we add an edge from it to the END
workflow.add_edge("creator", END)

# 4. Compile the graph into a runnable application
# This creates the final, executable object.
app = workflow.compile()

# 5. (Optional but Recommended) Generate a visualization of the graph
# This will create a PNG file that shows the structure of your agent workflow.
# You must have pygraphviz and graphviz installed for this to work.
try:
    # Get the graph as a bytes object
    image_bytes = app.get_graph().draw_png()  # type: ignore

    # Write the bytes to a file
    with open("workflow_graph.png", "wb") as f:
        f.write(image_bytes)
    print("Successfully generated workflow_graph.png")

except Exception as e:
    print(f"Warning: Could not generate graph visualization. Make sure Graphviz is installed. Error: {e}")
