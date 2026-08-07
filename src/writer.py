from pathlib import Path


class JsonWriter:
    def __init__(self, filename: Path) -> None:
        self.filename = filename

    def write(self, text: str) -> None:
        """Write JSON text to a file."""

        self.filename.parent.mkdir(parents=True, exist_ok=True)

        self.filename.write_text(
            text,
            encoding="utf-8",
        )
