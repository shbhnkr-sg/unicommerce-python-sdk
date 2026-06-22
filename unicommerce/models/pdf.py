from __future__ import annotations

from pathlib import Path


class PdfResponse:
    """Binary PDF response with convenience methods."""

    __slots__ = ("content",)

    def __init__(self, content: bytes) -> None:
        self.content = content

    def save(self, path: str | Path) -> Path:
        p = Path(path)
        p.write_bytes(self.content)
        return p

    def __len__(self) -> int:
        return len(self.content)

    def __repr__(self) -> str:
        return f"PdfResponse({len(self.content)} bytes)"
