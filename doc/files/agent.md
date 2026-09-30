# `agent.py`

[← Về README](../../README.md)

## Mục đích

Tạo LLM và dựng **graph LangGraph**: phần "bộ não" của agent. Export biến `graph` đã compile để `main.py` (hoặc test, API server sau này) sử dụng.

## Thành phần

### 1. LLM: `ChatOllama`

Thư viện `langchain-ollama` gọi `POST {OLLAMA_BASE_URL}/api/chat`. Cách map tham số sang body request:

| Tham số `ChatOllama` | Trường trong body |
|---|---|
| `model` | `model` |
| `reasoning=False` | `think: false` |
| `keep_alive` | `keep_alive` |
| `num_ctx` | `options.num_ctx` |
| `num_predict` | `options.num_predict` |
| `temperature=0` | `options.temperature` |
| `bind_tools(..., stream=False)` | `stream: false` + `tools: [...]` |

`client_kwargs` thêm header `Authorization` **chỉ khi** `OLLAMA_API_KEY` có giá trị.

`llm.bind_tools(TOOLS)` gửi kèm schema các tool trong mỗi request để model biết mình có thể gọi tool nào.

### 2. Node `agent`

```python
def agent_node(state):
    messages = [SystemMessage(SYSTEM_PROMPT)] + state["messages"]
    return {"messages": [llm_with_tools.invoke(messages)]}
```

System prompt được ghép vào **mỗi lần gọi** chứ không lưu trong state, nên sửa prompt sẽ có hiệu lực ngay cả với hội thoại cũ.

### 3. Node `tools`

`ToolNode(TOOLS)` (có sẵn trong LangGraph) đọc `tool_calls` từ tin nhắn AI cuối, chạy hàm tương ứng, rồi trả về các `ToolMessage`.

### 4. Cạnh (edges)

```
START ─▶ agent
agent ─▶ tools   (nếu tin nhắn cuối có tool_calls)
agent ─▶ END     (nếu không)
tools ─▶ agent
```

`tools_condition` là hàm có sẵn thực hiện phép kiểm tra này.

### 5. Checkpointer

`compile(checkpointer=InMemorySaver())` bật short-term memory theo `thread_id`. Xem [architecture.md](../architecture.md#short-term-memory).

## Chỉnh sửa thường gặp

| Muốn | Sửa |
|---|---|
| Đổi tính cách / ngôn ngữ trả lời | `SYSTEM_PROMPT` |
| Đổi model / server | `.env`, không sửa file này |
| Memory lưu vĩnh viễn | Thay `InMemorySaver` bằng `SqliteSaver` |
| Thêm bước xử lý (ví dụ tóm tắt lịch sử) | `builder.add_node(...)` + nối edge |
