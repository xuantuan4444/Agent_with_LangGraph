# `main.py`

[← Về README](../../README.md)

## Mục đích

Điểm chạy chương trình: vòng lặp chat trên terminal. Chỉ lo **input/output**; toàn bộ logic agent nằm trong `agent.py`.

## Hoạt động

1. Tạo `thread_id` ngẫu nhiên (`uuid4`) cho phiên chat.
2. Lặp: đọc input → xử lý lệnh `/new`, `/exit` → gọi graph.
3. Gọi `graph.stream(..., stream_mode="updates")`: mỗi khi một node chạy xong, ta nhận được phần state node đó vừa thêm. Nhờ đó có thể in từng bước:

| Loại tin nhắn | In ra |
|---|---|
| `AIMessage` có `tool_calls` | `[gọi tool] tên(tham số)` |
| `ToolMessage` | `[kết quả] <200 ký tự đầu>` |
| `AIMessage` thường | `Agent: <câu trả lời>` |

4. `config = {"configurable": {"thread_id": ...}}` được truyền vào mỗi lần gọi để checkpointer biết cần nạp và lưu lịch sử của hội thoại nào.

## Chạy

```powershell
python main.py
```

Xem thêm: [getting-started.md](../getting-started.md).
