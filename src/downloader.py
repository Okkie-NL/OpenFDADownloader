from .api import OpenFDAApiClient
from .config import Settings
from .file_utils import clean_output_directory
from .logger import create_logger
from .manifest import Manifest
from .page_writer import PageWriter


class Downloader:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenFDAApiClient(settings)
        self.writer = PageWriter(settings.pages_directory)
        self.manifest = Manifest(settings)
        self.logger = create_logger()

    def run(self) -> None:

        total_records = 0
        page_count = 0

        self.logger.info("=" * 60)
        self.logger.info("OpenFDA Downloader")
        self.logger.info("=" * 60)
        self.logger.info("Endpoint : %s", self.settings.endpoint)
        self.logger.info("Search   : %s", self.settings.search)
        self.logger.info("PageSize : %d", self.settings.page_size)
        self.logger.info("Output   : %s", self.settings.output_directory)
        self.logger.info("")

        try:

            deleted = clean_output_directory(
                self.settings.pages_directory
            )

            self.logger.info(
                "Deleted %d existing page files.",
                deleted,
            )

            for page in self.client.pages():

                filename = self.writer.write(
                    page.number,
                    page.raw_json,
                )

                page_count += 1
                total_records += page.record_count

                self.logger.info(
                    "Page %6d | Records: %4d | Total: %8d | %s",
                    page.number,
                    page.record_count,
                    total_records,
                    filename.name,
                )

                if (
                    self.settings.max_pages > 0
                    and page.number >= self.settings.max_pages
                ):
                    self.logger.info(
                        "Reached configured limit of %d pages.",
                        self.settings.max_pages,
                    )
                    break

            self.manifest.write(
                pages_downloaded=page_count,
                records_downloaded=total_records,
            )

            self.logger.info("")
            self.logger.info("Manifest written.")
            self.logger.info("Download completed successfully.")

        except KeyboardInterrupt:

            self.logger.warning("")
            self.logger.warning("Download interrupted by user.")

        except Exception:

            self.logger.exception("Unexpected error during download.")

        finally:

            self.logger.info("")
            self.logger.info("=" * 60)
            self.logger.info("Summary")
            self.logger.info("=" * 60)
            self.logger.info("Pages downloaded   : %d", page_count)
            self.logger.info("Records downloaded : %d", total_records)
            self.logger.info("=" * 60)