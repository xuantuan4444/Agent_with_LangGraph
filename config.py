"""Cấu hình tập trung, đọc từ biến môi trường (.env).

Mọi thứ phụ thuộc môi trường (URL server, tên model, key...) đều để ở .env,
code chỉ đọc qua module này. Đổi server/model => sửa .env, không sửa code.
"""
import os

from dotenv import load_dotenv

load_dotenv()

# Địa chỉ gốc của Ollama server (KHÔNG kèm /api/chat, thư viện tự nối thêm)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")

# Tuỳ chọn: token nếu server Ollama được đặt sau reverse proxy có xác thực.
# Ollama mặc định không cần key -> để trống.
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")

# Tham số sinh văn bản (tương ứng "options" trong body của /api/chat)
OLLAMA_NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX", "8192"))
OLLAMA_NUM_PREDICT = int(os.getenv("OLLAMA_NUM_PREDICT", "512"))
# -1 = giữ model trong RAM/VRAM vô thời hạn
OLLAMA_KEEP_ALIVE = int(os.getenv("OLLAMA_KEEP_ALIVE", "-1"))
