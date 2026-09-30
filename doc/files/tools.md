# `tools.py`

[← Về README](../../README.md)

## Mục đích

Định nghĩa các **tool**, tức các hàm Python mà LLM có thể yêu cầu gọi. Hiện tại có 3 tool thao tác file:

| Tool | Tham số | Trả về |
|---|---|---|
| `read_file` | `path` | Nội dung file |
| `write_file` | `path`, `content` | Thông báo đã ghi (tạo thư mục cha nếu chưa có, ghi đè nếu đã tồn tại) |
| `list_files` | `path` (mặc định `.`) | Danh sách file/thư mục; thư mục có dấu `/` ở cuối |

## Hoạt động

- Decorator `@tool` biến hàm thành tool LangChain. **Tên hàm, type hint và docstring** được chuyển thành JSON schema gửi cho LLM, nên docstring cần viết rõ vì LLM dựa vào đó để quyết định dùng tool nào và truyền gì.
- `WORKSPACE = <thư mục dự án>/workspace`, tự tạo khi import.
- `_resolve(path)`: nối path vào `WORKSPACE`, chuẩn hoá, và **chặn** nếu kết quả nằm ngoài workspace (ví dụ `../.env`).
- Lỗi không bị ném ra mà được trả về dạng chuỗi `"Lỗi ...: ..."`, để LLM đọc được và tự xử lý (thử lại, báo người dùng).
- `TOOLS` là danh sách export cho `agent.py`.

## Thêm tool mới

```python
@tool
def my_tool(arg: str) -> str:
    """Mô tả rõ tool làm gì, khi nào dùng.

    Args:
        arg: Ý nghĩa tham số.
    """
    return "kết quả"

TOOLS = [read_file, write_file, list_files, my_tool]
```

Không cần sửa `agent.py` vì graph tự dùng `TOOLS`.
