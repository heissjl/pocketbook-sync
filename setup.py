#!/usr/bin/env python3
"""
Setup wizard for Pocketbook Highlights Sync
Interactive configuration for first-time setup
"""

import json
import os
import sys
from pathlib import Path

CONFIG_FILE = Path.home() / '.pocketbook_sync_config.json'

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")

def print_step(number, text):
    """Print a step number."""
    print(f"\n{'─' * 60}")
    print(f"Step {number}: {text}")
    print('─' * 60)

def get_input_with_default(prompt, default=None):
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def detect_pocketbook():
    """Try to auto-detect Pocketbook mount point."""
    common_paths = [
        '/Volumes/PB626',
        '/Volumes/PocketBook',
        '/Volumes/POCKETBOOK',
    ]

    for path in common_paths:
        p = Path(path)
        if p.exists() and (p / 'system' / 'config' / 'books.db').exists():
            return str(p)

    return None

def detect_calibre_library():
    """Try to auto-detect Calibre library."""
    common_paths = [
        Path.home() / 'Library' / 'Mobile Documents' / 'com~apple~CloudDocs' / 'Documents' / 'Calibre Library',
        Path.home() / 'Calibre Library',
        Path.home() / 'Documents' / 'Calibre Library',
    ]

    for path in common_paths:
        if path.exists() and (path / 'metadata.db').exists():
            return str(path)

    return None

def detect_obsidian_vault():
    """Try to auto-detect Obsidian vault."""
    common_paths = [
        Path.home() / 'Library' / 'Mobile Documents' / 'iCloud~md~obsidian' / 'Documents' / 'Vault 13',
        Path.home() / 'Documents' / 'Obsidian',
        Path.home() / 'Obsidian',
    ]

    for path in common_paths:
        if path.exists() and path.is_dir():
            return str(path)

    return None

def validate_path(path_str, must_exist=True):
    """Validate a path string."""
    if not path_str:
        return None

    path = Path(path_str).expanduser()

    if must_exist and not path.exists():
        return None

    return path

def main():
    """Run the setup wizard."""
    print_header("Pocketbook Highlights Sync - Setup Wizard")

    print("Welcome! This wizard will help you configure the sync tool.")
    print("\nYou'll need:")
    print("  • Your Pocketbook e-reader connected via USB")
    print("  • Path to your note-taking app vault (Obsidian, Logseq, etc.)")
    print("  • (Optional) Path to your Calibre library for deep links")

    input("\nPress Enter to continue...")

    config = {}

    # Load existing config if it exists
    if CONFIG_FILE.exists():
        print("\n⚠️  Existing configuration found.")
        overwrite = input("Do you want to reconfigure? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("\nSetup cancelled. Your existing configuration is unchanged.")
            sys.exit(0)

        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

    # Step 1: Pocketbook
    print_step(1, "Configure Pocketbook")

    detected_pb = detect_pocketbook()
    if detected_pb:
        print(f"✓ Auto-detected Pocketbook at: {detected_pb}")
        use_detected = input("Use this path? (Y/n): ").strip().lower()
        if use_detected != 'n':
            config['pocketbook_path'] = detected_pb
        else:
            detected_pb = None

    if not detected_pb:
        print("\nPlease connect your Pocketbook via USB if not already connected.")
        print("Common mount points:")
        print("  • /Volumes/PocketBook")
        print("  • /Volumes/PB626")

        while True:
            pb_path = get_input_with_default(
                "\nEnter Pocketbook mount path",
                config.get('pocketbook_path', '/Volumes/PocketBook')
            )

            path = validate_path(pb_path)
            if path and (path / 'system' / 'config' / 'books.db').exists():
                config['pocketbook_path'] = str(path)
                print(f"✓ Pocketbook configured: {path}")
                break
            else:
                print("✗ Invalid path or books.db not found. Please try again.")
                retry = input("Try again? (Y/n): ").strip().lower()
                if retry == 'n':
                    print("\n⚠️  Pocketbook path not configured. You'll need to set this before syncing.")
                    break

    # Step 2: Note-taking app
    print_step(2, "Configure Note-Taking App")

    print("What note-taking app do you use?")
    print("  1. Obsidian (default)")
    print("  2. Logseq")
    print("  3. Notion")
    print("  4. Other Markdown-based app")

    app_choice = get_input_with_default("Enter choice (1-4)", "1")

    app_name_map = {
        '1': 'Obsidian',
        '2': 'Logseq',
        '3': 'Notion',
        '4': 'Other'
    }

    app_name = app_name_map.get(app_choice, 'Obsidian')
    config['notes_app'] = app_name

    detected_vault = detect_obsidian_vault() if app_choice == '1' else None

    if detected_vault:
        print(f"\n✓ Auto-detected {app_name} vault at: {detected_vault}")
        use_detected = input("Use this path? (Y/n): ").strip().lower()
        if use_detected != 'n':
            config['notes_vault_path'] = detected_vault
            # For backwards compatibility
            config['obsidian_vault_path'] = detected_vault
        else:
            detected_vault = None

    if not detected_vault:
        print(f"\nEnter the path to your {app_name} vault/directory.")
        print("This is where your highlight files will be saved.")

        default_vault = config.get('notes_vault_path') or config.get('obsidian_vault_path')

        while True:
            vault_path = get_input_with_default(
                f"\nEnter {app_name} vault path",
                default_vault
            )

            path = validate_path(vault_path)
            if path and path.is_dir():
                config['notes_vault_path'] = str(path)
                # For backwards compatibility
                config['obsidian_vault_path'] = str(path)
                print(f"✓ {app_name} vault configured: {path}")
                break
            else:
                print("✗ Invalid path. Please try again.")
                retry = input("Try again? (Y/n): ").strip().lower()
                if retry == 'n':
                    print(f"\n⚠️  {app_name} vault not configured. You'll need to set this before syncing.")
                    break

    # Configure highlights folder name
    print("\nWhat should the highlights folder be called?")
    folder_name = get_input_with_default(
        "Folder name",
        config.get('highlights_folder', 'Book Highlights')
    )
    config['highlights_folder'] = folder_name

    # Step 3: Calibre (optional)
    print_step(3, "Configure Calibre Library (Optional)")

    print("Calibre integration enables deep links to open books at highlight locations.")
    enable_calibre = input("Enable Calibre integration? (Y/n): ").strip().lower()

    if enable_calibre != 'n':
        detected_calibre = detect_calibre_library()

        if detected_calibre:
            print(f"\n✓ Auto-detected Calibre library at: {detected_calibre}")
            use_detected = input("Use this path? (Y/n): ").strip().lower()
            if use_detected != 'n':
                config['calibre_library_path'] = detected_calibre
            else:
                detected_calibre = None

        if not detected_calibre:
            print("\nEnter the path to your Calibre library.")
            print("(Press Enter to skip)")

            calibre_path = get_input_with_default(
                "\nCalbre library path (optional)",
                config.get('calibre_library_path', '')
            )

            if calibre_path:
                path = validate_path(calibre_path)
                if path and (path / 'metadata.db').exists():
                    config['calibre_library_path'] = str(path)
                    print(f"✓ Calibre library configured: {path}")
                else:
                    print("✗ Invalid path or metadata.db not found. Skipping Calibre integration.")
                    config.pop('calibre_library_path', None)
            else:
                print("Skipping Calibre integration.")
                config.pop('calibre_library_path', None)
    else:
        print("Skipping Calibre integration.")
        config.pop('calibre_library_path', None)

    # Summary
    print_header("Configuration Summary")

    print("Your configuration:")
    print(f"  • Pocketbook: {config.get('pocketbook_path', 'Not configured')}")
    print(f"  • Note-taking app: {config.get('notes_app', 'Obsidian')}")
    print(f"  • Vault path: {config.get('notes_vault_path', 'Not configured')}")
    print(f"  • Highlights folder: {config.get('highlights_folder', 'Book Highlights')}")
    print(f"  • Calibre library: {config.get('calibre_library_path', 'Not configured')}")

    print(f"\nConfiguration will be saved to: {CONFIG_FILE}")

    save = input("\nSave this configuration? (Y/n): ").strip().lower()

    if save != 'n':
        # Save config
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"\n✓ Configuration saved!")

        print_header("Setup Complete!")

        print("You're all set! To sync your highlights:")
        print("\n  Option 1: Double-click 'Pocketbook Sync.app'")
        print("  Option 2: Run 'python3 sync_highlights.py'")

        print("\nTo reconfigure later, run 'python3 setup.py' again.")

    else:
        print("\nSetup cancelled. Configuration not saved.")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
