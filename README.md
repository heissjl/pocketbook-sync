# Pocketbook Highlights Sync

Automatically sync highlights from your Pocketbook e-reader to your note-taking app (Obsidian, Logseq, Notion, etc.) with deep links to open books in Calibre.

## Features

- ✨ **Extract highlights** from Pocketbook e-readers (Touch Lux 3 and compatible models)
- 📝 **Create formatted Markdown files** - one file per book with all highlights
- 🔗 **Deep links to Calibre** - click to open books at exact highlight locations
- 📚 **Multi-app support** - works with Obsidian, Logseq, Notion, or any Markdown-based system
- ⚙️ **Easy setup wizard** - interactive configuration on first run
- 🔄 **Remembers your settings** - paths saved for future syncs
- 🍎 **macOS app included** - double-click to sync

## What You Get

Each synced book creates a beautifully formatted Markdown file:

```markdown
---
title: The Fire Next Time
author: James Baldwin
type: book-highlights
sync_date: 2026-01-14
calibre_id: 348
---

# The Fire Next Time
**Author:** James Baldwin
**Synced:** 2026-01-14 10:25

**Open in Calibre:**
- [View in Calibre](calibre://show-book/_/348)
- [Open EPUB file](file:///path/to/book.epub)

---

## Highlights

> Your highlighted text appears here as a quote block.

*Page 17 | Added: 2025-09-24 20:14*
[📖 Open in Calibre](calibre://view-book/_/348/EPUB?open_at=...)

---

> Another highlight from the book.

*Page 28 | Added: 2025-09-24 20:45*
[📖 Open in Calibre](calibre://view-book/_/348/EPUB?open_at=...)
```

## Quick Start

### Prerequisites

- **macOS** (tested on macOS 13+)
- **Python 3.6+** (pre-installed on macOS)
- **Pocketbook e-reader** (Touch Lux 3 or compatible)
- **Note-taking app** (Obsidian, Logseq, Notion, or Markdown-based)
- **(Optional) Calibre** for deep linking

### Installation

#### Option 1: Using Claude Code (Recommended)

Simply paste this prompt into Claude Code:

```
Please help me set up the Pocketbook Highlights Sync tool. Clone the repository from https://github.com/heissjl/pocketbook-sync to my home directory, run the setup wizard, and help me test the first sync.
```

See [SETUP_PROMPT.md](SETUP_PROMPT.md) for the full prompt.

#### Option 2: Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/heissjl/pocketbook-sync.git
   cd pocketbook-sync
   ```

2. **Run the setup wizard:**
   ```bash
   python3 setup.py
   ```

3. **Follow the prompts** to configure:
   - Pocketbook mount path
   - Note-taking app vault location
   - (Optional) Calibre library path

That's it! Your configuration is saved in `~/.pocketbook_sync_config.json`

## Usage

### Easy Way: Double-Click the App

1. Connect your Pocketbook via USB
2. Double-click **Pocketbook Sync.app**
3. A Terminal window opens and runs the sync
4. Done! Check your notes app for the new highlight files

### Command Line

```bash
python3 sync_highlights.py
```

## Configuration

The setup wizard creates `~/.pocketbook_sync_config.json`:

```json
{
  "pocketbook_path": "/Volumes/PB626",
  "notes_app": "Obsidian",
  "notes_vault_path": "/path/to/your/vault",
  "highlights_folder": "Book Highlights",
  "calibre_library_path": "/path/to/Calibre Library"
}
```

### Reconfigure

Run the setup wizard again:
```bash
python3 setup.py
```

Or manually edit `~/.pocketbook_sync_config.json`

## Supported Note-Taking Apps

- **Obsidian** - Full support with wikilinks compatibility
- **Logseq** - Markdown files work natively
- **Notion** - Import the generated Markdown files
- **Joplin, Bear, Typora, etc.** - Any app that supports Markdown

## Calibre Integration

If you use Calibre to manage your ebook library, the sync tool can create deep links:

- **Book-level links** - View the book in Calibre or open the EPUB file
- **Highlight-level links** - Attempt to open the book at the exact location (Note: deep positioning may not work reliably, but links will open the book)

### Calibre URL Format

The tool generates `calibre://` URLs:
- `calibre://show-book/_/348` - Opens book in Calibre
- `calibre://view-book/_/348/EPUB?open_at=epubcfi(...)` - Attempts to open at specific location

## How It Works

1. **Reads your Pocketbook database** at `system/config/books.db`
2. **Extracts bookmarks** (TypeID = 4) with highlighted text
3. **Matches books to Calibre** (if configured) by title
4. **Generates Markdown files** with highlights, metadata, and links
5. **Saves to your vault** in the configured highlights folder

## Troubleshooting

### "Database not found" error

- Ensure Pocketbook is connected via USB
- Check the mount path (usually `/Volumes/PocketBook` or `/Volumes/PB626`)
- Verify `system/config/books.db` exists on the device

### "No highlights found"

- Make sure you've highlighted text in books on your Pocketbook
- Bookmarks without text ("Bookmark") are filtered out

### Calibre links don't work

- Ensure Calibre is installed and has opened at least once
- The `calibre://` URL scheme should be automatically registered
- Deep linking to positions may not work reliably - the book will still open

### File permission errors

- Ensure you have write access to your notes vault
- The script creates a `Book Highlights` subfolder automatically

## Technical Details

### Database Schema

Pocketbook uses SQLite to store highlights:
- **Books table**: Book metadata (title, author)
- **Items table**: Highlight items (TypeID = 4 for bookmarks)
- **Tags table**: Highlight text stored as JSON in `bm.quotation`

### Position Data

Each highlight includes:
- **Page number** - Extracted from Pocketbook's internal page tracking
- **EPUB CFI** - Canonical Fragment Identifier for precise positioning
- **Timestamp** - When the highlight was created

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

Based on research about Pocketbook database structure:
- [Pocketbook Annotations Extraction (MobileRead)](http://www.mobileread.mobi/forums/showthread.php?t=281744&page=3)
- [pocketbook-export-highlights GitHub](https://github.com/habdenscrimen/pocketbook-export-highlights)
- [pocketbook-notes GitHub](https://github.com/FrapiFrance/pocketbook-notes)
- [Calibre URL scheme documentation](https://manual.calibre-ebook.com/url_scheme.html)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/heissjl/pocketbook-sync/issues)
- **Discussions**: [GitHub Discussions](https://github.com/heissjl/pocketbook-sync/discussions)

---

Made with ❤️ for book lovers and note-takers
