from typing import TypedDict

from langgraph.graph import StateGraph, START, END

# 1. Define the State
# The state is the data structure that is passed between nodes.
class State(TypedDict):
    message: str

# 2. Define the Nodes
# Nodes are functions that take the current state and return an update to the state.
def node_a(state: State):
    print("---Node A---")
    return {"message": state["message"] + " -> A"}

def node_b(state: State):
    print("---Node B---")
    return {"message": state["message"] + " -> B"}

# 3. Build the Graph
builder = StateGraph(State)

# Add nodes to the graph
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)

# Define the flow (Edges)
builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", END)

# 4. Compile the Graph
graph = builder.compile()

# 5. Run the Graph
initial_state = {"message": "Start"}
print(f"Initial State: {initial_state}")

# invoke runs the graph synchronously
result = graph.invoke(initial_state)

print(f"Final Result: {result}")
