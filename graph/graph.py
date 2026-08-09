from langgraph.graph import StateGraph, START, END

from graph.state import GraphState
from graph.nodes import (
    resume_parser_node,
    matching_node,
    scoring_node,
    reviewer_node,
    improvement_node,
    route_after_scoring
)


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("resume_parser", resume_parser_node)
    builder.add_node("matcher", matching_node)
    builder.add_node("scorer", scoring_node)
    builder.add_node("reviewer", reviewer_node)
    builder.add_node("improvement", improvement_node)

    builder.add_edge(START, "resume_parser")
    builder.add_edge("resume_parser", "matcher")
    builder.add_edge("matcher", "scorer")

    builder.add_conditional_edges(
        "scorer",
        route_after_scoring,
        {
            "reviewer": "reviewer",
            "improvement": "improvement",
            "end": END
        }
    )

    builder.add_edge("reviewer", END)
    builder.add_edge("improvement", END)

    return builder.compile()


resume_graph = build_graph()