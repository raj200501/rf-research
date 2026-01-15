"""Utility functions for distributed jobs (local-only)."""

from pathlib import Path
import shutil

from rf_research.config import RFConfig


def upload_to_local_archive(file_name, archive_dir):
    archive_dir = Path(archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)
    destination = archive_dir / Path(file_name).name
    shutil.copy(file_name, destination)
    print(f"Archived {file_name} to {destination}")
    return destination


if __name__ == "__main__":
    config = RFConfig()
    config.ensure_directories()
    upload_to_local_archive(config.processed_path, config.processed_path.parent / "archive")
