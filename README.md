# Agent LangGraph

Agent AI cơ bản xây bằng [LangGraph](https://langchain-ai.github.io/langgraph/), dùng LLM chạy trên **Ollama server nội bộ** (`qwen3.5:9b`). Agent có thể:

- Đọc / ghi / liệt kê file trong thư mục `workspace/`
- Nhớ ngữ cảnh hội thoại (short-term memory) trong một phiên chat

> Đây là phiên bản khởi đầu tối giản, sẽ được mở rộng dần.

## Bắt đầu nhanh

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # rồi chỉnh giá trị nếu cần
python main.py
```

Chi tiết: [doc/getting-started.md](doc/getting-started.md)

## Tài liệu

| Tài liệu | Nội dung |
|---|---|
| [doc/getting-started.md](doc/getting-started.md) | Cài đặt, chạy, lệnh trong chat, xử lý lỗi thường gặp |
| [doc/architecture.md](doc/architecture.md) | Kiến trúc tổng thể, luồng chạy của graph, cơ chế memory |
| [doc/configuration.md](doc/configuration.md) | Biến môi trường `.env`, cách quản lý URL / model / secret |
| [doc/files/config.md](doc/files/config.md) | `config.py` – đọc cấu hình |
| [doc/files/tools.md](doc/files/tools.md) | `tools.py` – các tool đọc/ghi file |
| [doc/files/agent.md](doc/files/agent.md) | `agent.py` – LLM + graph LangGraph |
| [doc/files/main.md](doc/files/main.md) | `main.py` – giao diện chat terminal |

## Cấu trúc thư mục

```
agent_langgraph/
├── README.md          # file này
├── requirements.txt   # thư viện Python
├── .env.example       # mẫu cấu hình (commit)
├── .env               # cấu hình thật (KHÔNG commit)
├── config.py          # đọc .env
├── tools.py           # tool cho agent
├── agent.py           # định nghĩa graph
├── main.py            # điểm chạy chương trình
├── doc/               # tài liệu
└── workspace/         # vùng file agent được phép đọc/ghi (tự tạo)
```
# Agent_with_LangGraph
