import re

from dotenv import load_dotenv
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


def reduce_results(a: str, b: str) -> str:
    print(f"Reducing results:\nA: {a}\nB: {b}")
    return b


class AgentState(TypedDict):
    task: str
    result: Annotated[str, reduce_results]


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


def think(state: AgentState):
    print(f"Thinking about task: {state['task']}")
    response = llm.invoke(f"Solve this task: {state['task']}")
    return {"result": response.content}


def review(state: AgentState):
    print(f"Reviewing result: {state['result']}")
    feedback = llm.invoke(f"Review this result: {state['result']}")
    return {"result": feedback.content}


def calculator(expression: str) -> str:
    print(f"Calculating: {expression}")
    return str(eval(expression))


def use_tool(state: AgentState):
    print(f"Using tool for task: {state['task']}")
    if "calculate" in state["task"]:
        match = re.search(r'[\d+\-*/().\s]+', state["task"])
        if match:
            result = calculator(match.group().strip())
        return {"result": result}


def should_continue(state: AgentState):
    print(f"Deciding whether to continue based on result: {state['result']}")
    result_lower = state["result"].lower()
    if "improve" in result_lower and not any(
        word in result_lower for word in ["no improve", "not improve", "without improve", "doesn't need improve", "don't need improve", "no need for improve"]
    ):
        return "think"
    return "end"


def main():
    builder = StateGraph(AgentState)

    builder.add_node("think", think)
    builder.set_entry_point("think")

    builder.add_node("review", review)
    builder.add_edge("think", "review")

    builder.add_node("tool", use_tool)
    builder.add_edge("think", "tool")

    builder.add_conditional_edges(
        "review",
        should_continue,
        {
            "think": "think",
            "end": END
        }
    )

    graph = builder.compile()

    png = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png)

    result = graph.invoke({"task": "calculate 6-2 and improve the result if needed"})
    print(result)


if __name__ == "__main__":
    main()
