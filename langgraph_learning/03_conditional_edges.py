from typing import TypedDict

from langgraph.graph import StateGraph, START, END

# State that holds a flag
class FlagState(TypedDict):
    flag: bool

def set_true(state: FlagState):
    print("Setting flag to True")
    return {"flag": True}

def check_flag(state: FlagState):
    if state["flag"]:
        print("Flag is True, moving to END")
        return {}
    else:
        print("Flag is False, looping back to set_true")
        return {}

builder = StateGraph(FlagState)
builder.add_node("set_true", set_true)
builder.add_node("check", check_flag)

# Conditional edge based on the flag value
builder.add_edge(START, "set_true")
builder.add_edge("set_true", "check")
# If flag is False, go back to set_true (this won't happen after first run)
builder.add_edge("check", "set_true")
# If flag is True, go to END
builder.add_edge("check", END)

graph = builder.compile()

initial_state = {"flag": False}
print(f"Initial state: {initial_state}")
result = graph.invoke(initial_state)
print(f"Final state: {result}")
