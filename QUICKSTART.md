# Quick Start Guide

Get up and running with Pocketbook Highlights Sync in 5 minutes!

## What You'll Need

- ✅ Pocketbook e-reader (connected via USB)
- ✅ A note-taking app (Obsidian, Logseq, Notion, etc.)
- ✅ macOS with Python 3 (pre-installed)
- ⚡ (Optional) Calibre for deep linking

## Installation: Choose Your Path

### 🤖 Option 1: Use Claude Code (Easiest)

Just paste this into Claude Code:

```
Please help me set up Pocketbook Highlights Sync. Clone it from
https://github.com/heissjl/pocketbook-sync to ~/pocketbook-sync,
run the setup wizard, and help me test the first sync.
```

That's it! Claude will guide you through everything.

### 💻 Option 2: Manual Setup (5 minutes)

1. **Download the tool:**
   ```bash
   cd ~
   git clone https://github.com/heissjl/pocketbook-sync.git
   cd pocketbook-sync
   ```

2. **Run setup:**
   ```bash
   python3 setup.py
   ```

3. **Follow the wizard:**
   - Connect your Pocketbook → wizard finds it ✓
   - Point to your notes vault → wizard remembers it ✓
   - (Optional) Add Calibre library ✓

4. **Done!** Configuration saved to `~/.pocketbook_sync_config.json`

## First Sync

### Double-Click Method

1. Connect Pocketbook via USB
2. Navigate to `~/pocketbook-sync/`
3. Double-click **Pocketbook Sync.app**
4. Terminal opens → sync runs → done!

### Command Line Method

```bash
cd ~/pocketbook-sync
python3 sync_highlights.py
```

## What Happens Next?

The tool will:
1. ✨ Find all your highlights
2. 📝 Create one Markdown file per book
3. 💾 Save to your notes vault in `Book Highlights/`
4. 🔗 Add links to open books in Calibre (if configured)

Check your note-taking app - you should see a new `Book Highlights` folder!

## Example Output

```
============================================================
Pocketbook to Obsidian Highlights Sync
============================================================

Found 22 book(s) with highlights:
  - The Fire Next Time by James Baldwin (11 highlights)
  - Pattern Recognition by William Gibson (3 highlights)
  - The Third Policeman by Flann O'Brien (12 highlights)
  ...

Creating notes in: /path/to/vault/Book Highlights
  ✓ Created: The Fire Next Time.md (with Calibre links)
  ✓ Created: Pattern Recognition.md (with Calibre links)
  ✓ Created: The Third Policeman.md (with Calibre links)
  ...

============================================================
Sync complete! Created 22 file(s).
Matched 22 book(s) to Calibre library.
============================================================
```

## Troubleshooting

**"Pocketbook not found"**
- Make sure it's connected and shows up in Finder
- Try `/Volumes/PocketBook` or `/Volumes/PB626`

**"No highlights found"**
- Highlight some text in a book on your Pocketbook first
- Regular bookmarks (without text) don't count

**"Configuration not saved"**
- Make sure you confirmed "Y" when asked to save
- Check `~/.pocketbook_sync_config.json` exists

## Next Steps

- Read the [full README](README.md) for details
- Learn about [Calibre integration](README.md#calibre-integration)
- Customize your [configuration](#customization)

## Customization

Edit `~/.pocketbook_sync_config.json`:

```json
{
  "pocketbook_path": "/Volumes/PB626",
  "notes_app": "Obsidian",
  "notes_vault_path": "/path/to/vault",
  "highlights_folder": "📚 Reading Notes",  ← Change this!
  "calibre_library_path": "/path/to/Calibre Library"
}
```

Or run `python3 setup.py` again to reconfigure.

## Tips

💡 **Sync regularly** - Connect Pocketbook and run sync after finishing a book

💡 **Use with Calibre** - Deep links let you jump back to the source

💡 **Organize in your vault** - Highlights are just Markdown files

💡 **Search across books** - Your note-taking app can search all highlights

## Need Help?

- 📖 Read the [full documentation](README.md)
- 🐛 [Report bugs](https://github.com/heissjl/pocketbook-sync/issues)
- 💬 [Ask questions](https://github.com/heissjl/pocketbook-sync/discussions)

---

Happy highlighting! 📚✨
