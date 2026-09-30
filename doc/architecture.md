# Kiến trúc

[← Về README](../README.md)

## Tổng quan

```
┌──────────┐   input    ┌─────────────────── LangGraph ───────────────────┐
│ main.py  │ ─────────▶ │                                                  │
│ (chat    │            │  START ─▶ [agent] ──có tool_calls?──▶ [tools]    │
│ terminal)│ ◀───────── │              ▲   │ không                   │     │
└──────────┘   output   │              │   ▼                         │     │
                        │              │  END                        │     │
                        │              └─────────────────────────────┘     │
                        │                                                  │
                        │  Checkpointer (InMemorySaver) – lưu state        │
                        └──────────────────────────────────────────────────┘
                                   │                        │
                                   ▼                        ▼
                         Ollama server (LLM)        workspace/ (file)
                         POST /api/chat
```

## Các thành phần

| Thành phần | File | Vai trò |
|---|---|---|
| Config | `config.py` | Đọc `.env`, cung cấp URL/model/tham số |
| Tools | `tools.py` | Hàm Python mà LLM có thể yêu cầu gọi |
| Graph | `agent.py` | Nối LLM + tools thành vòng lặp ReAct |
| UI | `main.py` | Nhận input, stream từng bước ra terminal |

## Luồng xử lý một câu hỏi

1. `main.py` gửi `HumanMessage` vào graph kèm `thread_id`.
2. Checkpointer nạp lại toàn bộ lịch sử của `thread_id` đó → state `messages`.
3. Node **agent**: ghép `SystemMessage` + lịch sử, gửi tới Ollama (`POST /api/chat`) kèm danh sách tool.
4. LLM trả về:
   - **Có `tool_calls`** → `tools_condition` chuyển sang node **tools**, `ToolNode` chạy hàm Python tương ứng, kết quả (`ToolMessage`) được thêm vào state → quay lại bước 3.
   - **Không có `tool_calls`** → đó là câu trả lời cuối → `END`.
5. Checkpointer lưu state mới; `main.py` in kết quả.

Vòng lặp agent ⇄ tools có thể lặp nhiều lần trong một câu hỏi (ví dụ: liệt kê file → đọc file → trả lời).

## Short-term memory

- State của graph là `MessagesState` – một danh sách tin nhắn, reducer tự **nối thêm** tin nhắn mới.
- `InMemorySaver` lưu state theo `thread_id`. Cùng `thread_id` ⇒ agent nhớ các lượt trước.
- `/new` tạo `thread_id` mới ⇒ hội thoại trắng.
- Giới hạn hiện tại:
  - Lưu trong RAM → **mất khi tắt chương trình**.
  - Không cắt bớt lịch sử → hội thoại dài có thể vượt `num_ctx` (8192 token).

## Bảo mật tool file

Mọi đường dẫn được `_resolve()` chuẩn hoá và kiểm tra phải nằm trong `workspace/`. Yêu cầu kiểu `../.env` sẽ bị từ chối, nên LLM không thể đọc secret hay sửa code.

## Hướng phát triển dự kiến

- Memory bền vững: `SqliteSaver` / `PostgresSaver`
- Cắt / tóm tắt lịch sử khi gần đầy context
- Long-term memory (`Store`) giữa các phiên
- Thêm tool: tìm kiếm, chạy lệnh, gọi API nội bộ...
