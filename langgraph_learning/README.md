# LangGraph Learning Journey

This directory contains code and examples for learning **LangGraph**, a library for building stateful, multi-actor applications with LLMs. The examples progress from basic concepts to more complex agentic workflows.

## Prerequisites

*   Python 3.8+
*   `langgraph`
*   `langchain`
*   `langchain-openai` (or other LLM provider integration)

## Contents

1.  **01_hello_langgraph.py**: 
    *   **Concept:** The basics of creating a simple graph.
    *   **What it does:** Sets up a minimal graph structure with a start and end node to demonstrate the core API.

2.  **02_state_management.py**: 
    *   **Concept:** Managing state between nodes.
    *   **What it does:** Demonstrates how to pass data through the graph, ensuring that subsequent steps have access to the context or results from previous steps.

3.  **03_conditional_edges.py**: 
    *   **Concept:** Dynamic routing.
    *   **What it does:** Introduces decision logic where the path of execution changes based on the output of a node (e.g., an LLM decision or tool output).

## how to Run

Make sure you have your API keys set up (e.g., `OPENAI_API_KEY`) if the scripts call an LLM.

```bash
# Example: Run the first script
python3 01_hello_langgraph.py
```

## Resources

*   [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
*   [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
