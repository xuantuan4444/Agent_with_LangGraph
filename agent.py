"""Định nghĩa graph của agent.

Luồng:  START -> agent -> (có tool_calls?) -> tools -> agent -> ... -> END
Short-term memory: InMemorySaver lưu lịch sử hội thoại theo thread_id.
"""
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

import config
from tools import TOOLS

SYSTEM_PROMPT = (
    "Bạn là một trợ lý hữu ích. Bạn có thể đọc, ghi và liệt kê file "
    "trong thư mục workspace bằng các tool được cung cấp. "
    "Hãy trả lời bằng tiếng Việt, ngắn gọn."
)

# ChatOllama gọi POST {base_url}/api/chat, map tham số như sau:
#   model        -> "model"
#   reasoning    -> "think"
#   keep_alive   -> "keep_alive"
#   num_ctx      -> "options.num_ctx"
#   num_predict  -> "options.num_predict"
#   stream=False -> "stream" (truyền qua bind_tools bên dưới)
llm = ChatOllama(
    base_url=config.OLLAMA_BASE_URL,
    model=config.OLLAMA_MODEL,
    reasoning=False,
    keep_alive=config.OLLAMA_KEEP_ALIVE,
    num_ctx=config.OLLAMA_NUM_CTX,
    num_predict=config.OLLAMA_NUM_PREDICT,
    temperature=0,
    client_kwargs=(
        {"headers": {"Authorization": f"Bearer {config.OLLAMA_API_KEY}"}}
        if config.OLLAMA_API_KEY
        else {}
    ),
)
llm_with_tools = llm.bind_tools(TOOLS, stream=False)


def agent_node(state: MessagesState):
    """Gọi LLM với system prompt + toàn bộ lịch sử tin nhắn."""
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def build_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(TOOLS))

    builder.add_edge(START, "agent")
    # Nếu LLM yêu cầu gọi tool -> "tools", ngược lại -> END
    builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    builder.add_edge("tools", "agent")

    return builder.compile(checkpointer=InMemorySaver())


graph = build_graph()
