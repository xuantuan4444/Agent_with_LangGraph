# `config.py`

[← Về README](../../README.md)

## Mục đích

Là **nơi duy nhất** đọc biến môi trường. Các module khác `import config` rồi dùng `config.OLLAMA_BASE_URL`, … thay vì gọi `os.getenv` rải rác.

## Hoạt động

1. `load_dotenv()` nạp file `.env` vào biến môi trường (biến có sẵn trong hệ thống được ưu tiên hơn `.env`).
2. Mỗi hằng số đọc bằng `os.getenv("TÊN", "mặc định")`.
3. Biến số được ép kiểu `int(...)`, nên nếu `.env` sai định dạng thì chương trình báo lỗi ngay lúc khởi động.

## Thêm biến mới

```python
# config.py
MY_SETTING = os.getenv("MY_SETTING", "default")
```

Sau đó thêm dòng tương ứng vào `.env.example`. Chi tiết các biến hiện có: [configuration.md](../configuration.md).
