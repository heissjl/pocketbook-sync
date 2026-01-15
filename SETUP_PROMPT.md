# Claude Code Setup Prompt

Copy and paste this prompt into Claude Code to set up Pocketbook Highlights Sync on your system:

---

## Setup Prompt

```
I want to set up the Pocketbook Highlights Sync tool to automatically sync highlights from my Pocketbook e-reader to my note-taking app.

Please help me with the following:

1. Clone the repository from https://github.com/heissjl/pocketbook-sync to ~/pocketbook-sync

2. Run the setup wizard (python3 setup.py) and help me configure:
   - My Pocketbook mount path (auto-detect if possible)
   - My note-taking app vault location (default: Obsidian at ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault 13)
   - My Calibre library location (default: ~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Calibre Library)
   - Highlights folder name (default: "Book Highlights")

3. After setup is complete:
   - Show me the configuration that was saved
   - Explain how to run the sync (both via the app and command line)
   - Help me test the first sync if my Pocketbook is connected

4. If there are any issues:
   - Help me troubleshoot connectivity or path problems
   - Verify that all dependencies are met
   - Check that the Pocketbook database is accessible

Please guide me through each step and explain what's happening along the way.
```

---

## Alternative: Quick Setup (Advanced Users)

If you're comfortable with the command line, use this shorter prompt:

```
Clone https://github.com/heissjl/pocketbook-sync to ~/pocketbook-sync and run the setup wizard. Use these defaults:
- Pocketbook: /Volumes/PB626 (auto-detect)
- Notes app: Obsidian
- Vault: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault 13
- Calibre: ~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Calibre Library
- Folder: Book Highlights

Then show me the config and help me run the first sync.
```

---

## What to Expect

Claude Code will:

1. **Clone the repository** to your specified location
2. **Run the setup wizard** interactively
3. **Auto-detect paths** when possible (Pocketbook, Calibre, Obsidian)
4. **Save your configuration** to `~/.pocketbook_sync_config.json`
5. **Verify the setup** by checking all paths exist
6. **Help with the first sync** if your Pocketbook is connected
7. **Troubleshoot** any issues that arise

## Tips

- **Have your Pocketbook connected** via USB before starting
- **Know your vault path** for your note-taking app
- **Have Calibre installed** if you want deep linking (optional)
- **Be ready to confirm paths** that Claude auto-detects

## After Setup

Once setup is complete, you can sync highlights:

**Option 1: Double-click the app**
- Navigate to `~/pocketbook-sync/`
- Double-click `Pocketbook Sync.app`

**Option 2: Command line**
```bash
cd ~/pocketbook-sync
python3 sync_highlights.py
```

**Option 3: Ask Claude Code**
```
Run the Pocketbook sync for me
```

## Customization

You can customize the setup by modifying your prompt. For example:

```
Set up Pocketbook sync with:
- Notes app: Logseq
- Vault: ~/Documents/Logseq
- Highlights folder: "Reading Notes"
- Skip Calibre integration
```

---

## Need Help?

If you encounter issues during setup, ask Claude Code:

```
I'm having trouble with the Pocketbook sync setup:
[describe your issue]

Please help me troubleshoot.
```

Common issues:
- **Pocketbook not detected**: Make sure it's connected via USB and mounted
- **Vault path not found**: Double-check the path to your notes folder
- **Calibre integration fails**: This is optional, you can skip it
- **Permission errors**: Ensure you have write access to the vault folder
