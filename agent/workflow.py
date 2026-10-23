from langgraph.graph import StateGraph, START, END

from agent.state import AgentState
from agent.nodes import plan_node, execute_node, answer_node


def build_workflow():
    graph = StateGraph(AgentState)

    graph.add_node("plan", plan_node)
    graph.add_node("execute", execute_node)
    graph.add_node("answer", answer_node)

    graph.add_edge(START, "plan")
    graph.add_edge("plan", "execute")
    graph.add_edge("execute", "answer")
    graph.add_edge("answer", END)

    return graph.compile()
