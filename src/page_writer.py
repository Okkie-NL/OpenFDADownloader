from pathlib import Path


class PageWriter:
    def __init__(self, output_directory: Path) -> None:

        self.output_directory = output_directory
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write(
        self,
        page_number: int,
        json_text: str,
    ) -> Path:

        filename = (
            self.output_directory
            / f"page_{page_number:06d}.json"
        )

        filename.write_text(
            json_text,
            encoding="utf-8",
        )

        return filename