# Cấu hình

[← Về README](../README.md)

## Nguyên tắc

> **Code không chứa giá trị phụ thuộc môi trường.** URL, tên model, key, tham số… đều nằm trong `.env`; code chỉ đọc qua `config.py`.

Lợi ích:
- Mỗi người / mỗi môi trường (dev, staging, prod) dùng server khác nhau mà không phải sửa code.
- Secret (nếu có) không lọt vào Git.
- Đổi model hoặc server chỉ cần sửa 1 dòng trong `.env`.

## Các file liên quan

| File | Commit Git? | Mục đích |
|---|---|---|
| `.env` | ❌ Không (đã có trong `.gitignore`) | Giá trị thật của từng máy |
| `.env.example` | ✅ Có | Mẫu liệt kê đủ các biến, để người mới copy |
| `config.py` | ✅ Có | Đọc biến + giá trị mặc định + ép kiểu |

Khi thêm biến mới: thêm vào **cả** `.env.example` và `config.py`.

## Danh sách biến

| Biến | Mặc định | Tương ứng trong body `/api/chat` | Ý nghĩa |
|---|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | – | Địa chỉ gốc server, **không** kèm `/api/chat` |
| `OLLAMA_MODEL` | `qwen3.5:9b` | `model` | Tên model trên server |
| `OLLAMA_API_KEY` | *(trống)* | header `Authorization` | Chỉ dùng khi server nằm sau proxy có xác thực |
| `OLLAMA_NUM_CTX` | `8192` | `options.num_ctx` | Kích thước context (token) |
| `OLLAMA_NUM_PREDICT` | `512` | `options.num_predict` | Số token tối đa mỗi câu trả lời |
| `OLLAMA_KEEP_ALIVE` | `-1` | `keep_alive` | Thời gian giữ model trong bộ nhớ; `-1` = mãi mãi |

Các giá trị cố định trong code (`agent.py`), không phải cấu hình:
`stream=false`, `think=false` (`reasoning=False`), `temperature=0`.

