from dataclasses import dataclass
from pathlib import Path
import json
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Settings:
    endpoint: str
    search: str
    sort: str
    page_size: int
    output_directory: Path
    retry_count: int
    retry_delay: float
    timeout: int
    max_pages: int
    api_key: str

    @property
    def pages_directory(self) -> Path:
        return self.output_directory / "pages"


def load_settings(filename: Path) -> Settings:
    """Load settings from a JSON configuration file."""

    with filename.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return Settings(
        endpoint=data["endpoint"],
        search=data["search"],
        sort=data["sort"],
        page_size=data["page_size"],
        output_directory=Path(data["output_directory"]),
        retry_count=data["retry_count"],
        retry_delay=data["retry_delay"],
        timeout=data["timeout"],
        max_pages=data["max_pages"],
        api_key=os.getenv("OPENFDA_API_KEY", ""),
    )