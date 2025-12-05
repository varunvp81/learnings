from typing import TypedDict

from langgraph.graph import StateGraph, START, END

# Define a state that holds a counter
class CounterState(TypedDict):
    count: int

# Node that increments the counter
def increment(state: CounterState):
    new_count = state["count"] + 1
    print(f"Incremented to {new_count}")
    return {"count": new_count}

# Node that checks threshold and decides next step
def check_threshold(state: CounterState):
    if state["count"] >= 3:
        print("Threshold reached, moving to END")
        return {}
    else:
        print("Threshold not reached, looping back to increment")
        return {}

builder = StateGraph(CounterState)
builder.add_node("increment", increment)
builder.add_node("check", check_threshold)

# Flow: start -> increment -> check -> (conditional) -> increment or END
builder.add_edge(START, "increment")
builder.add_edge("increment", "check")
# Conditional edge based on state
builder.add_conditional_edge(
    "check",
    lambda state: END if state["count"] >= 3 else "increment",
)

graph = builder.compile()

initial_state = {"count": 0}
print(f"Initial state: {initial_state}")
result = graph.invoke(initial_state)
print(f"Final state: {result}")
