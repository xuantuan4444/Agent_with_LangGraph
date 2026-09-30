"""Các tool cho agent: đọc, ghi, liệt kê file.

Mọi thao tác file bị giới hạn trong thư mục WORKSPACE để agent không
đụng tới file ngoài dự án.
"""
from pathlib import Path

from langchain_core.tools import tool

WORKSPACE = Path(__file__).parent / "workspace"
WORKSPACE.mkdir(exist_ok=True)


def _resolve(path: str) -> Path:
    """Chuyển path tương đối thành path tuyệt đối trong WORKSPACE, chặn thoát ra ngoài."""
    full = (WORKSPACE / path).resolve()
    if not full.is_relative_to(WORKSPACE.resolve()):
        raise ValueError(f"Không được truy cập ngoài workspace: {path}")
    return full


@tool
def read_file(path: str) -> str:
    """Đọc nội dung một file text trong workspace.

    Args:
        path: Đường dẫn tương đối tới file, ví dụ "notes.txt".
    """
    try:
        return _resolve(path).read_text(encoding="utf-8")
    except Exception as e:
        return f"Lỗi khi đọc file: {e}"


@tool
def write_file(path: str, content: str) -> str:
    """Ghi (tạo mới hoặc ghi đè) một file text trong workspace.

    Args:
        path: Đường dẫn tương đối tới file, ví dụ "notes.txt".
        content: Nội dung cần ghi.
    """
    try:
        full = _resolve(path)
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        return f"Đã ghi {len(content)} ký tự vào {path}"
    except Exception as e:
        return f"Lỗi khi ghi file: {e}"


@tool
def list_files(path: str = ".") -> str:
    """Liệt kê file và thư mục trong workspace.

    Args:
        path: Thư mục tương đối cần liệt kê, mặc định là gốc workspace.
    """
    try:
        full = _resolve(path)
        items = sorted(full.iterdir())
        if not items:
            return "(trống)"
        return "\n".join(f"{p.name}/" if p.is_dir() else p.name for p in items)
    except Exception as e:
        return f"Lỗi khi liệt kê: {e}"


TOOLS = [read_file, write_file, list_files]
