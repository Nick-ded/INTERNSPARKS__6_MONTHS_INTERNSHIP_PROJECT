"""
File Automator - Automation script for file operations
Supports: renaming, sorting, cleaning, and organizing files

Requirements:
  - Python 3.7+
  - Standard library only (os, shutil, logging, datetime, sys)
"""

import os
import shutil
import logging
import datetime
import sys

# ── Logging Setup ─────────────────────────────────────────────────────────────

def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """Configure file + console logging."""
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"file_automator_{timestamp}.log")

    logger = logging.getLogger("FileAutomator")
    logger.setLevel(logging.DEBUG)

    # File handler – full detail
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))

    # Console handler – info and above
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(levelname)-8s | %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f"Log file created: {log_file}")
    return logger


# ── Helper ────────────────────────────────────────────────────────────────────

def validate_directory(path: str, logger: logging.Logger) -> bool:
    """Return True if path is an existing directory."""
    # Strip accidental surrounding quotes (common copy-paste mistake)
    path = path.strip('"').strip("'")

    if not os.path.exists(path):
        logger.error(f"Path does not exist: {path}")
        print(f"\n  [!] '{path}' does not exist. Check for typos.")
        return False
    if os.path.isfile(path):
        parent = os.path.dirname(path)
        logger.error(f"A file was given instead of a directory: {path}")
        print(f"\n  [!] That path points to a FILE, not a folder.")
        print(f"      Did you mean the parent folder?")
        print(f"      -> {parent}")
        return False
    if not os.path.isdir(path):
        logger.error(f"Path is not a directory: {path}")
        print(f"\n  [!] '{path}' is not a valid directory.")
        return False
    return True


# ── Operations ────────────────────────────────────────────────────────────────

def rename_files(directory: str, old_text: str, new_text: str, logger: logging.Logger) -> int:
    """
    Batch-rename files: replace `old_text` with `new_text` in filenames.
    Returns the number of files renamed.
    """
    logger.info(f"[RENAME] Directory: {directory} | '{old_text}' -> '{new_text}'")
    if not validate_directory(directory, logger):
        return 0

    count = 0
    try:
        for filename in os.listdir(directory):
            # Skip Office temporary lock files (~$filename)
            if filename.startswith("~$"):
                logger.debug(f"  Skipped temp lock file: {filename}")
                continue
            if old_text in filename:
                old_path = os.path.join(directory, filename)
                new_name = filename.replace(old_text, new_text)
                new_path = os.path.join(directory, new_name)

                # Skip if the destination already exists
                if os.path.exists(new_path):
                    logger.warning(f"  Skipped (target exists): {filename} -> {new_name}")
                    continue

                os.rename(old_path, new_path)
                logger.info(f"  Renamed: {filename}  ->  {new_name}")
                count += 1

    except PermissionError as e:
        logger.error(f"Permission denied during rename: {e}")
    except OSError as e:
        logger.error(f"OS error during rename: {e}")

    logger.info(f"[RENAME] Done - {count} file(s) renamed.")
    return count


def sort_files_by_extension(directory: str, logger: logging.Logger) -> dict:
    """
    Sort files into sub-folders named after their extensions.
    Example: report.pdf  ->  PDF/report.pdf
    Returns a dict {extension_folder: count}.
    """
    logger.info(f"[SORT] Directory: {directory}")
    if not validate_directory(directory, logger):
        return {}

    summary: dict = {}
    try:
        entries = os.listdir(directory)
        for filename in entries:
            filepath = os.path.join(directory, filename)
            if not os.path.isfile(filepath):
                continue  # skip sub-directories

            _, ext = os.path.splitext(filename)
            folder_name = ext.lstrip(".").upper() if ext else "NO_EXTENSION"
            dest_dir = os.path.join(directory, folder_name)

            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)

            if os.path.exists(dest_path):
                logger.warning(f"  Skipped (already exists in target): {filename}")
                continue

            shutil.move(filepath, dest_path)
            logger.info(f"  Moved: {filename}  ->  {folder_name}/")
            summary[folder_name] = summary.get(folder_name, 0) + 1

    except PermissionError as e:
        logger.error(f"Permission denied during sort: {e}")
    except OSError as e:
        logger.error(f"OS error during sort: {e}")

    logger.info(f"[SORT] Done - {sum(summary.values())} file(s) sorted into {len(summary)} folder(s).")
    return summary


def clean_directory(directory: str, extensions: list, logger: logging.Logger) -> int:
    """
    Delete files matching any of the given extensions.
    Returns the number of files deleted.
    """
    exts = [e if e.startswith(".") else f".{e}" for e in extensions]
    logger.info(f"[CLEAN] Directory: {directory} | Target extensions: {exts}")
    if not validate_directory(directory, logger):
        return 0

    count = 0
    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if not os.path.isfile(filepath):
                continue

            _, ext = os.path.splitext(filename)
            if ext.lower() in [e.lower() for e in exts]:
                os.remove(filepath)
                logger.info(f"  Deleted: {filename}")
                count += 1

    except PermissionError as e:
        logger.error(f"Permission denied during clean: {e}")
    except OSError as e:
        logger.error(f"OS error during clean: {e}")

    logger.info(f"[CLEAN] Done - {count} file(s) deleted.")
    return count


def unsort_files(directory: str, logger: logging.Logger) -> int:
    """
    Undo a previous sort: move all files from every immediate sub-folder
    back into `directory`, then remove the now-empty sub-folders.
    Returns the number of files moved back.
    """
    logger.info(f"[UNSORT] Directory: {directory}")
    if not validate_directory(directory, logger):
        return 0

    count = 0
    try:
        sub_folders = [
            os.path.join(directory, d)
            for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]

        if not sub_folders:
            logger.info("[UNSORT] No sub-folders found — nothing to undo.")
            print("  No sub-folders found. Nothing to undo.")
            return 0

        for folder in sub_folders:
            for filename in os.listdir(folder):
                # Skip Office temp lock files
                if filename.startswith("~$"):
                    logger.debug(f"  Skipped temp lock file: {filename}")
                    continue

                src = os.path.join(folder, filename)
                if not os.path.isfile(src):
                    continue

                dest = os.path.join(directory, filename)

                # If a file with the same name already exists in the root, keep both
                if os.path.exists(dest):
                    base, ext = os.path.splitext(filename)
                    dest = os.path.join(directory, f"{base}_restored{ext}")
                    logger.warning(f"  Name conflict — restoring as: {os.path.basename(dest)}")

                shutil.move(src, dest)
                logger.info(f"  Restored: {os.path.basename(folder)}/{filename}  ->  {os.path.basename(dest)}")
                count += 1

            # Remove folder if now empty
            try:
                if not os.listdir(folder):
                    os.rmdir(folder)
                    logger.info(f"  Removed empty folder: {os.path.basename(folder)}/")
                else:
                    logger.warning(f"  Folder not empty (skipped removal): {os.path.basename(folder)}/")
            except OSError as e:
                logger.error(f"  Could not remove folder {folder}: {e}")

    except PermissionError as e:
        logger.error(f"Permission denied during unsort: {e}")
    except OSError as e:
        logger.error(f"OS error during unsort: {e}")

    logger.info(f"[UNSORT] Done - {count} file(s) restored.")
    return count


def list_directory_tree(directory: str, logger: logging.Logger) -> None:
    """Print and log a tree view of the directory."""
    logger.info(f"[LIST] Directory tree for: {directory}")
    if not validate_directory(directory, logger):
        return

    print(f"\n{'─' * 52}")
    print(f"  Directory tree: {directory}")
    print(f"{'─' * 52}")

    try:
        for root, dirs, files in os.walk(directory):
            level = root.replace(directory, "").count(os.sep)
            indent = "    " * level
            folder_label = os.path.basename(root) or root
            print(f"{indent}[DIR]  {folder_label}/")
            logger.debug(f"{indent}{folder_label}/")

            sub_indent = "    " * (level + 1)
            for f in sorted(files):
                size = os.path.getsize(os.path.join(root, f))
                print(f"{sub_indent}[FILE] {f}  ({size} bytes)")
                logger.debug(f"{sub_indent}{f} ({size} bytes)")

    except PermissionError as e:
        logger.error(f"Permission denied reading directory tree: {e}")
    except OSError as e:
        logger.error(f"OS error reading directory tree: {e}")

    print(f"{'─' * 52}\n")


# ── Menu ──────────────────────────────────────────────────────────────────────

def print_menu() -> None:
    print("\n" + "=" * 52)
    print("         FILE AUTOMATOR  -  Main Menu")
    print("=" * 52)
    print("  1. Rename files  (find & replace in filename)")
    print("  2. Sort files by extension into sub-folders")
    print("  3. Unsort  (restore files back to parent folder)")
    print("  4. Clean directory  (delete files by extension)")
    print("  5. List directory tree")
    print("  6. Exit")
    print("=" * 52)


def get_input(prompt: str, logger: logging.Logger, strip_quotes: bool = False) -> str:
    """Prompt the user, log the response, and handle interrupts gracefully."""
    try:
        value = input(prompt).strip()
        if strip_quotes:
            value = value.strip('"').strip("'")
        logger.debug(f"User input -> {value!r}")
        return value
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted by user.")
        logger.warning("User interrupted input.")
        sys.exit(0)


# ── Entry Point ───────────────────────────────────────────────────────────────

def main() -> None:
    logger = setup_logging()
    logger.info("=" * 50)
    logger.info("File Automator started.")
    logger.info("=" * 50)

    print("\nWelcome to File Automator!")
    print("All operations are logged to the 'logs/' folder.\n")

    while True:
        print_menu()
        choice = get_input("Enter your choice (1-6): ", logger)

        # ── 1. Rename ──────────────────────────────────────────
        if choice == "1":
            directory = get_input("Enter directory path: ", logger, strip_quotes=True)
            old_text  = get_input("Text to find in filename: ", logger)
            new_text  = get_input("Replace with: ", logger)

            if not old_text:
                print("Search text cannot be empty.")
                logger.warning("Rename skipped - empty search text.")
                continue

            count = rename_files(directory, old_text, new_text, logger)
            print(f"\n  {count} file(s) renamed.")

        # ── 2. Sort ────────────────────────────────────────────
        elif choice == "2":
            directory = get_input("Enter directory path: ", logger, strip_quotes=True)
            summary = sort_files_by_extension(directory, logger)

            if summary:
                print("\n  Sort summary:")
                for folder, cnt in sorted(summary.items()):
                    print(f"    {folder}/  ->  {cnt} file(s)")
            else:
                print("  No files were moved.")

        # ── 3. Unsort ──────────────────────────────────────────
        elif choice == "3":
            directory = get_input("Enter directory path: ", logger, strip_quotes=True)
            confirm = get_input(
                "  This will move ALL files from sub-folders back to the parent. Confirm? (yes/no): ",
                logger,
            )
            if confirm.lower() != "yes":
                print("  Unsort cancelled.")
                logger.info("Unsort cancelled by user.")
                continue

            count = unsort_files(directory, logger)
            print(f"\n  {count} file(s) restored to {directory}")

        # ── 4. Clean ───────────────────────────────────────────
        elif choice == "4":
            directory = get_input("Enter directory path: ", logger, strip_quotes=True)
            ext_input = get_input(
                "Extensions to delete (comma-separated, e.g. tmp,log,bak): ", logger
            )

            if not ext_input:
                print("No extensions provided.")
                logger.warning("Clean skipped - no extensions given.")
                continue

            extensions = [e.strip() for e in ext_input.split(",") if e.strip()]
            confirm = get_input(
                f"  WARNING: This permanently deletes files with {extensions}. "
                f"Confirm? (yes/no): ",
                logger,
            )

            if confirm.lower() != "yes":
                print("  Clean operation cancelled.")
                logger.info("Clean cancelled by user.")
                continue

            count = clean_directory(directory, extensions, logger)
            print(f"\n  {count} file(s) deleted.")

        # ── 5. List ────────────────────────────────────────────
        elif choice == "5":
            directory = get_input("Enter directory path: ", logger, strip_quotes=True)
            list_directory_tree(directory, logger)

        # ── 6. Exit ────────────────────────────────────────────
        elif choice == "6":
            logger.info("File Automator exited by user.")
            print("\nGoodbye!\n")
            break

        else:
            print("  Invalid choice. Please enter a number between 1 and 6.")
            logger.warning(f"Invalid menu choice entered: {choice!r}")


if __name__ == "__main__":
    main()
