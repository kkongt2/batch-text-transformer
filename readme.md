# Batch Text Transformer

A desktop GUI tool for batch text replacement, deletion, and line filtering across multiple files.

This project is built with Python + Tkinter and provides safe replace workflows with preview, backup, cancel, and undo.


## Key Features

- Multi-file replacement with `src,dst` mapping input
- Delete matched words with `src,`
- Delete lines containing a match with `src,,delete-line`
- Preview with match highlighting
- Replace scope: `All` (default) or `Selected`
- Regex mode and case-sensitive mode
- Context controls for preview (`Context lines`, `Context chars`)
- Safety flow:
  - Confirmation dialog before replace
  - `.bak` backup creation per changed file
  - Undo from backups
  - Cancel running replace
- Mapping validation UI:
  - Duplicate source highlighting
  - Same `src == dst` highlighting
  - CSV parse error lines
  - Invalid regex lines (when Regex mode is enabled)
- Session persistence (`word_replacer_session.json`)

## Requirements

- Python 3.10+
- Tkinter (usually bundled with Python on Windows)
- Optional for drag-and-drop:
  - `tkinterdnd2` (preferred), or
  - `tkdnd`

## Run

```bash
python batch-text-transformer.py
```

## Mapping Format

Enter one mapping per line in the mapping editor:

```text
source_text,target_text
```

Examples:

```text
foo,bar
foo,
foo,,delete-line
"hello world","HELLO_WORLD"
# comment lines are ignored
```

Notes:

- Empty source values are ignored.
- `src,dst` replaces `src` with `dst`.
- `src,` deletes the matched text.
- `src,,delete-line` deletes each line containing `src`.
- A line with only `src` is preview-only and is not applied during replace.
- `delete-line` matches are selected by default in Preview. Click a highlighted delete-line row to toggle whether that line is applied.

## Usage

1. Add input text files (`Browse Files` or drag-and-drop when enabled).
2. Enter mapping lines for replace or delete operations.
3. Choose options:
   - `Regex Mode`
   - `Case Sensitive`
   - `Replace scope` (`All` / `Selected`)
4. Review matches in the preview panel.
5. Click `Apply` and confirm.
6. Use `Cancel` to stop an ongoing run (current file finishes first).
7. Use `Undo` to restore from `.bak` backups.

## Safety and Recovery

- Before any write, each modified file is copied to `<filename>.bak`.
- `Undo` restores from the created `.bak` files.
- Only files with actual content changes are rewritten.

## Project Files

- `batch-text-transformer.py`: main GUI application
- `word_replacer_session.json`: saved UI session state
- `*.bak`: backup files created during replace

