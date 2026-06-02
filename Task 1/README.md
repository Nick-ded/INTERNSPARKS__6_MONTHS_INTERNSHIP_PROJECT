# File Automator

A command-line automation script that performs common file management tasks — renaming, sorting, cleaning, and inspecting directories — with full logging support.

---

## Features

| Operation | Description |
|-----------|-------------|
| **Rename** | Batch-rename files using find-and-replace on filenames |
| **Sort** | Move files into sub-folders organised by file extension |
| **Clean** | Delete files matching specified extensions |
| **List** | Display a tree view of a directory with file sizes |

---

## Requirements

- Python 3.7 or higher
- Standard library only — no third-party packages needed

---

## Project Structure

```
Task 1/
├── file_automator.py   # Main script
├── sample_io.txt       # Sample inputs and expected outputs
├── README.md           # This file
└── logs/               # Auto-created; contains timestamped log files
```

---

## How to Run

```bash
cd "Task 1"
python file_automator.py
```

A `logs/` folder is created automatically. Each session writes a new log file named `file_automator_YYYYMMDD_HHMMSS.log`.

---

## Menu Options

```
====================================================
         FILE AUTOMATOR  -  Main Menu
====================================================
  1. Rename files  (find & replace in filename)
  2. Sort files by extension into sub-folders
  3. Clean directory  (delete files by extension)
  4. List directory tree
  5. Exit
====================================================
```

---

## Usage Examples

### 1 — Rename

```
Enter directory path: C:\Users\user\Documents\reports
Text to find in filename: draft
Replace with: final
```
Renames every file whose name contains `draft`, replacing it with `final`.

### 2 — Sort

```
Enter directory path: C:\Users\user\Downloads
```
Moves all files into sub-folders: `PDF/`, `JPG/`, `TXT/`, etc.

### 3 — Clean

```
Enter directory path: C:\Users\user\Temp
Extensions to delete (comma-separated, e.g. tmp,log,bak): tmp,log,bak
WARNING: This permanently deletes files with ['.tmp', '.log', '.bak']. Confirm? (yes/no): yes
```

### 4 — List

```
Enter directory path: C:\Users\user\Project
```
Prints an indented tree with file sizes.

---

## Logging

Every operation is recorded in `logs/file_automator_<timestamp>.log`:

```
2024-06-01 14:30:12,345 | INFO     | Log file created: logs/file_automator_20240601_143012.log
2024-06-01 14:30:20,112 | INFO     | [RENAME] Directory: ... | 'draft' -> 'final'
2024-06-01 14:30:20,115 | INFO     |   Renamed: report_draft_jan.docx  ->  report_final_jan.docx
2024-06-01 14:30:20,118 | INFO     | [RENAME] Done - 1 file(s) renamed.
```

---

## Error Handling

The script handles the following gracefully (logged + user-friendly message):

- Directory does not exist
- Path is a file, not a directory
- `PermissionError` on restricted files
- `OSError` for general OS-level failures
- Destination file already exists (skipped with warning)
- `KeyboardInterrupt` / `EOFError` during input

---

## License

MIT — free to use and modify.
