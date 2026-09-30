# Cài đặt & chạy

[← Về README](../README.md)

## Yêu cầu

- Python 3.12+
- Kết nối mạng tới Ollama server (mặc định `http://10.101.122.147:11434` – mạng nội bộ/VPN)
- Model `qwen3.5:9b` đã được `ollama pull` trên server

## Cài đặt

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Mở `.env` và chỉnh giá trị nếu cần (xem [configuration.md](configuration.md)).

## Kiểm tra kết nối server (nên làm trước)

```powershell
curl http://10.101.122.147:11434/api/tags
```

Nếu trả về JSON danh sách model thì server OK. Nếu timeout: kiểm tra VPN / mạng LAN / firewall.

## Chạy

```powershell
python main.py
```

Ví dụ phiên chat:

```
Bạn: Tên tôi là An. Ghi "xin chào" vào file hello.txt
  [gọi tool] write_file({'path': 'hello.txt', 'content': 'xin chào'})
  [kết quả] Đã ghi 8 ký tự vào hello.txt

Agent: Đã ghi xong vào hello.txt.

Bạn: Tên tôi là gì?

Agent: Tên bạn là An.
```

Dòng `[gọi tool]` / `[kết quả]` cho thấy agent đang dùng tool – hữu ích khi debug.

## Lệnh trong chat

| Lệnh | Tác dụng |
|---|---|
| `/new` | Bắt đầu hội thoại mới (xoá short-term memory) |
| `/exit` | Thoát (hoặc `Ctrl+C`) |

## Lỗi thường gặp

| Triệu chứng | Nguyên nhân / cách xử lý |
|---|---|
| `ConnectError` / treo lâu | Không tới được server → kiểm tra `OLLAMA_BASE_URL`, VPN |
| `model "..." not found` | Server chưa có model → `ollama pull qwen3.5:9b` trên server |
| Câu trả lời bị cụt | Tăng `OLLAMA_NUM_PREDICT` trong `.env` |
| Agent "quên" đầu cuộc hội thoại dài | Vượt `OLLAMA_NUM_CTX` → tăng giá trị (tốn VRAM hơn) |
| Lỗi tiếng Việt trên terminal | Chạy `$env:PYTHONIOENCODING="utf-8"` trước |
