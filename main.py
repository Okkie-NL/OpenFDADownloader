from pathlib import Path

from src.config import load_settings
from src.downloader import Downloader


def main() -> None:

    settings = load_settings(Path("config/settings.json"))

    downloader = Downloader(settings)

    downloader.run()


if __name__ == "__main__":
    main()
