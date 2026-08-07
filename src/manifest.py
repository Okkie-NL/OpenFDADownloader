from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .config import Settings


class Manifest:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.started = datetime.now()

    def write(
        self,
        pages_downloaded: int,
        records_downloaded: int,
    ) -> None:

        finished = datetime.now()

        manifest = {
            "endpoint": self.settings.endpoint,
            "search": self.settings.search,
            "sort": self.settings.sort,
            "page_size": self.settings.page_size,
            "pages_downloaded": pages_downloaded,
            "records_downloaded": records_downloaded,
            "download_started": self.started.isoformat(timespec="seconds"),
            "download_finished": finished.isoformat(timespec="seconds"),
            "duration_seconds": round(
                (finished - self.started).total_seconds(),
                2,
            ),
            "application": "OpenFDA Downloader",
            "version": "0.3",
        }

        filename = (
            self.settings.output_directory
            / "manifest.json"
        )

        filename.write_text(
            json.dumps(
                manifest,
                indent=4,
            ),
            encoding="utf-8",
        )