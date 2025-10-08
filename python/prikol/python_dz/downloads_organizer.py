#!/usr/bin/env python3
"""Downloads organizer: moves files into category folders.

Creates folders for categories and moves files. Logs actions to downloads_organizer.log.
"""
from pathlib import Path
import logging
import argparse

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".md", ".rtf"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".dmg"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".json"],
    "Scripts": [".exe", ".msi", ".bat", ".sh", ".deb"],
    "Torrents": [".torrent"],
}


def setup_logger(log_path: Path):
    logger = logging.getLogger('downloads_organizer')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_path, encoding='utf-8')
    fmt = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    fh.setFormatter(fmt)
    if not logger.handlers:
        logger.addHandler(fh)
    return logger


def categorize_file(p: Path) -> str:
    suf = p.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if suf in exts:
            return cat
    return 'Other'


def unique_target(target: Path) -> Path:
    """If target exists, append _1, _2, ... before suffix."""
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    parent = target.parent
    i = 1
    while True:
        new_name = f"{stem}_{i}{suffix}"
        cand = parent / new_name
        if not cand.exists():
            return cand
        i += 1


def organize(folder: Path, logger=None):
    if logger is None:
        logger = setup_logger(folder / 'downloads_organizer.log')

    for p in folder.iterdir():
        if p.is_file():
            try:
                cat = categorize_file(p)
                dest_dir = folder / cat
                dest_dir.mkdir(exist_ok=True)

                target = dest_dir / p.name
                safe_target = unique_target(target)

                p.replace(safe_target)
                logger.info(f"Moved: {p.name} -> {safe_target}")
            except PermissionError as e:
                logger.error(f"PermissionError moving {p}: {e}")
            except Exception as e:
                logger.error(f"Error moving {p}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Organize download folder by file types')
    parser.add_argument('path', nargs='?', default=None, help='Path to folder (default: Downloads in home)')
    args = parser.parse_args()
    if args.path:
        folder = Path(args.path).expanduser().resolve()
    else:
        folder = Path.home() / 'Downloads'

    log_path = folder / 'downloads_organizer.log'
    logger = setup_logger(log_path)

    logger.info(f"Starting organization for: {folder}")
    organize(folder, logger)
    logger.info("Finished organization")


if __name__ == '__main__':
    main()
