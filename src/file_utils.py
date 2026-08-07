from pathlib import Path


def clean_output_directory(output_directory: Path) -> int:
    """
    Delete all page_*.json files from the output directory.

    Returns the number of files deleted.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    deleted = 0

    for file in output_directory.glob("page_*.json"):
        file.unlink()
        deleted += 1

    return deleted