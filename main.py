"""Chạy agent dạng chat trên terminal.

Lệnh đặc biệt:
  /new   - bắt đầu hội thoại mới (thread mới, xoá short-term memory)
  /exit  - thoát
"""
import uuid

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from agent import graph


def main():
    thread_id = str(uuid.uuid4())
    print("Agent sẵn sàng. Gõ /new để hội thoại mới, /exit để thoát.\n")

    while True:
        try:
            user_input = input("Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input == "/exit":
            break
        if user_input == "/new":
            thread_id = str(uuid.uuid4())
            print("-- Đã bắt đầu hội thoại mới --\n")
            continue

        config = {"configurable": {"thread_id": thread_id}}
        # stream_mode="updates" để in ra từng bước (gọi tool, kết quả tool, câu trả lời)
        for update in graph.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config,
            stream_mode="updates",
        ):
            for node_output in update.values():
                for msg in node_output["messages"]:
                    if isinstance(msg, AIMessage) and msg.tool_calls:
                        for tc in msg.tool_calls:
                            print(f"  [gọi tool] {tc['name']}({tc['args']})")
                    elif isinstance(msg, ToolMessage):
                        preview = msg.content[:200].replace("\n", " ")
                        print(f"  [kết quả] {preview}")
                    elif isinstance(msg, AIMessage):
                        print(f"\nAgent: {msg.content}\n")


if __name__ == "__main__":
    main()
