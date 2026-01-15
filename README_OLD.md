# Pocketbook to Obsidian Highlights Sync

Sync highlights from your Pocketbook Touch Lux 3 e-reader to your Obsidian vault.

## Features

- Extracts highlights from Pocketbook's SQLite database
- Creates one Markdown file per book in your Obsidian vault
- Formats highlights with metadata (author, sync date, timestamps)
- Preserves your notes/annotations alongside highlights
- Stores configuration for easy repeated use

## Prerequisites

- Python 3.6 or higher (check with `python3 --version`)
- Your Pocketbook Touch Lux 3 connected via USB
- Obsidian vault location

## Installation

1. No installation needed - the script is standalone
2. Make the script executable (optional):
   ```bash
   chmod +x sync_highlights.py
   ```

## Usage

### Easy Way: Double-Click the App (Recommended)

1. Connect your Pocketbook to your Mac via USB
2. Double-click **Pocketbook Sync.app**
3. A Terminal window will open and run the sync
4. Follow the prompts for first-time setup (paths will be saved for next time)

### Alternative: Command Line

1. Connect your Pocketbook to your Mac via USB
2. Run the script:
   ```bash
   python3 sync_highlights.py
   ```
3. The script will prompt you for paths on first run:
   - **Pocketbook mount path** (e.g., `/Volumes/PocketBook`)
   - **Obsidian vault path**: `/Users/julian/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault 13`

4. These paths are saved in `~/.pocketbook_sync_config.json` for future use

## Output

The script creates files in your Obsidian vault at:
```
/Users/julian/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault 13/Book Highlights/
```

Each file is named after the book title and contains:

```markdown
---
title: Book Title
author: Author Name
type: book-highlights
sync_date: 2026-01-14
---

# Book Title
**Author:** Author Name
**Synced:** 2026-01-14 15:30

---

## Highlights

> This is a highlighted passage from the book.

**Note:** Your annotation or note about this highlight

*Added: 2026-01-10 14:23*

---

> Another highlight here.

*Added: 2026-01-11 09:15*
```

## Configuration

Configuration is stored in `~/.pocketbook_sync_config.json`:

```json
{
  "pocketbook_path": "/Volumes/PocketBook",
  "obsidian_vault_path": "/Users/julian/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault 13"
}
```

To change paths, either:
- Delete the config file and run the script again, or
- Edit the JSON file directly

## Troubleshooting

### "Database not found" error
- Ensure your Pocketbook is connected via USB
- Check that you can see the device in Finder
- Verify the mount path (usually `/Volumes/PocketBook` or `/Volumes/POCKETBOOK`)

### "No highlights found"
- Make sure you've highlighted text in books on your Pocketbook
- Try highlighting a test passage and syncing again

### Database schema errors
- The Pocketbook database structure may vary by firmware version
- If you get SQL errors, please open an issue with your firmware version

### Permission errors
- Ensure you have write permissions to your Obsidian vault folder
- The script creates a `Book Highlights` subfolder automatically

## How It Works

1. Connects to the SQLite database at `system/config/books.db` on your Pocketbook
2. Queries for all books that have highlights (type 1 or 3 in the items table)
3. Extracts highlight text, annotations, timestamps, and positions
4. Formats each book's highlights into a Markdown file
5. Saves files to the `Book Highlights` folder in your Obsidian vault

## File Updates

If you sync again, the script will **overwrite** existing files with the same book title. This ensures you always have the latest highlights, but means:
- Manual edits to generated files will be lost
- If you want to preserve edits, rename the file or move it to another folder

## Future Improvements

Potential enhancements:
- Incremental sync (only add new highlights)
- Export to other formats (CSV, JSON, HTML)
- Automatic sync when Pocketbook is connected
- Page numbers (if available in database)

## References

Based on research about Pocketbook database structure:
- [Pocketbook Annotations Extraction (MobileRead)](http://www.mobileread.mobi/forums/showthread.php?t=281744&page=3)
- [pocketbook-export-highlights GitHub](https://github.com/habdenscrimen/pocketbook-export-highlights)
- [pocketbook-notes GitHub](https://github.com/FrapiFrance/pocketbook-notes)

## License

Free to use and modify for personal use.
