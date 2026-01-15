#!/usr/bin/env python3
"""
Pocketbook to Obsidian Highlights Sync
Extracts highlights from Pocketbook Touch Lux 3 and formats them for Obsidian.
"""

import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime
import json
from urllib.parse import quote

CONFIG_FILE = Path.home() / '.pocketbook_sync_config.json'


def load_config():
    """Load configuration from file or create new one."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_config(config):
    """Save configuration to file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_pocketbook_path():
    """Find or prompt for Pocketbook mount path."""
    config = load_config()

    if 'pocketbook_path' in config:
        path = Path(config['pocketbook_path'])
        if path.exists():
            print(f"Using Pocketbook path: {path}")
            return path

    # Try to auto-detect common mount points on macOS
    common_paths = [
        Path('/Volumes/PB626'),
        Path('/Volumes/PocketBook'),
        Path('/Volumes/POCKETBOOK'),
    ]

    for path in common_paths:
        if path.exists():
            db_path = path / 'system' / 'config' / 'books.db'
            if db_path.exists():
                print(f"Auto-detected Pocketbook at: {path}")
                config['pocketbook_path'] = str(path)
                save_config(config)
                return path

    # Prompt user
    print("\nPocketbook device not auto-detected.")
    print("Please connect your Pocketbook via USB and enter the mount path.")
    print("Common paths: /Volumes/PocketBook or /Volumes/POCKETBOOK")

    while True:
        user_path = input("Enter Pocketbook mount path: ").strip()
        path = Path(user_path)
        db_path = path / 'system' / 'config' / 'books.db'

        if db_path.exists():
            config['pocketbook_path'] = str(path)
            save_config(config)
            return path
        else:
            print(f"Error: Could not find books.db at {db_path}")
            print("Please check the path and try again.")


def get_obsidian_path():
    """Get or prompt for Obsidian vault path."""
    config = load_config()

    if 'obsidian_vault_path' in config:
        path = Path(config['obsidian_vault_path'])
        if path.exists():
            print(f"Using Obsidian vault: {path}")
            return path

    print("\nEnter the path to your Obsidian vault.")

    while True:
        user_path = input("Obsidian vault path: ").strip()
        path = Path(user_path).expanduser()

        if path.exists() and path.is_dir():
            config['obsidian_vault_path'] = str(path)
            save_config(config)
            return path
        else:
            print(f"Error: Directory not found at {path}")
            print("Please check the path and try again.")


def get_calibre_library_path():
    """Get or prompt for Calibre library path."""
    config = load_config()

    if 'calibre_library_path' in config:
        path = Path(config['calibre_library_path'])
        if path.exists():
            print(f"Using Calibre library: {path}")
            return path

    # Try default location
    default_path = Path.home() / 'Library' / 'Mobile Documents' / 'com~apple~CloudDocs' / 'Documents' / 'Calibre Library'
    if default_path.exists():
        metadata_db = default_path / 'metadata.db'
        if metadata_db.exists():
            print(f"Found Calibre library at: {default_path}")
            config['calibre_library_path'] = str(default_path)
            save_config(config)
            return default_path

    print("\nEnter the path to your Calibre library (or press Enter to skip backlinks).")

    user_path = input("Calibre library path (optional): ").strip()
    if not user_path:
        return None

    path = Path(user_path).expanduser()
    if path.exists() and path.is_dir():
        config['calibre_library_path'] = str(path)
        save_config(config)
        return path
    else:
        print(f"Warning: Calibre library not found at {path}")
        print("Continuing without backlinks...")
        return None


def lookup_calibre_book(calibre_db_path, book_title, book_author):
    """Look up book ID and path in Calibre library."""
    if not calibre_db_path or not calibre_db_path.exists():
        return None

    try:
        conn = sqlite3.connect(calibre_db_path / 'metadata.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Try exact title match first
        cursor.execute("""
            SELECT books.id, books.title, books.path, data.format, data.name
            FROM books
            JOIN data ON books.id = data.book
            WHERE books.title = ? AND data.format = 'EPUB'
        """, (book_title,))

        result = cursor.fetchone()

        if not result:
            # Try fuzzy match on title
            cursor.execute("""
                SELECT books.id, books.title, books.path, data.format, data.name
                FROM books
                JOIN data ON books.id = data.book
                WHERE books.title LIKE ? AND data.format = 'EPUB'
                LIMIT 1
            """, (f"%{book_title}%",))
            result = cursor.fetchone()

        conn.close()

        if result:
            return {
                'id': result['id'],
                'title': result['title'],
                'path': result['path'],
                'format': result['format'],
                'filename': result['name']
            }

        return None

    except sqlite3.Error as e:
        print(f"Calibre database error: {e}")
        return None


def extract_highlights(db_path):
    """Extract highlights from Pocketbook books.db database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Get TagIDs we need
        cursor.execute("SELECT OID FROM TagNames WHERE TagName = 'bm.quotation'")
        quotation_tag_id = cursor.fetchone()['OID']

        cursor.execute("SELECT OID FROM TagNames WHERE TagName = 'doc.book-title'")
        title_tag_id = cursor.fetchone()['OID']

        cursor.execute("SELECT OID FROM TagNames WHERE TagName = 'ro.authors'")
        author_tag_id = cursor.fetchone()['OID']

        cursor.execute("SELECT OID FROM TagNames WHERE TagName = 'bm.note'")
        note_result = cursor.fetchone()
        note_tag_id = note_result['OID'] if note_result else None

        # Query to get all bookmark items (type 4) with quotations
        highlights_query = """
        SELECT
            Items.OID as HighlightID,
            Items.ParentID,
            Items.TimeAlt,
            Tags.Val as QuotationData
        FROM Items
        JOIN Tags ON Items.OID = Tags.ItemID
        WHERE Items.TypeID = 4
          AND Tags.TagID = ?
          AND Tags.Val NOT LIKE '%"text":"Bookmark"%'
        ORDER BY Items.ParentID, Items.TimeAlt
        """

        cursor.execute(highlights_query, (quotation_tag_id,))
        highlights = cursor.fetchall()

        if not highlights:
            print("No highlights found.")
            conn.close()
            return []

        # Group highlights by book
        books_dict = {}

        for highlight in highlights:
            parent_id = highlight['ParentID']

            # Get book metadata from parent item
            cursor.execute("""
                SELECT Tags.Val, TagNames.TagName
                FROM Tags
                JOIN TagNames ON Tags.TagID = TagNames.OID
                WHERE Tags.ItemID = ?
                  AND TagNames.TagName IN ('doc.book-title', 'ro.authors', 'doc.authors')
            """, (parent_id,))

            book_tags = {row['TagName']: row['Val'] for row in cursor.fetchall()}

            title = book_tags.get('doc.book-title', 'Unknown Title')
            author = book_tags.get('ro.authors', book_tags.get('doc.authors', 'Unknown Author'))

            # Parse quotation JSON to get the highlighted text and position
            import json as json_lib
            try:
                quotation_data = json_lib.loads(highlight['QuotationData'])
                highlight_text = quotation_data.get('text', '')

                # Extract position data (page, EPUB CFI)
                begin_position = quotation_data.get('begin', '')
                page_num = None
                epubcfi = None

                if begin_position:
                    # Parse: "pbr:/word?page=243&offs=534#epubcfi(/6/96!/4/40/1:404)"
                    import re
                    page_match = re.search(r'page=(\d+)', begin_position)
                    if page_match:
                        page_num = int(page_match.group(1))

                    epubcfi_match = re.search(r'epubcfi\(([^)]+)\)', begin_position)
                    if epubcfi_match:
                        epubcfi = f"epubcfi({epubcfi_match.group(1)})"

            except (json_lib.JSONDecodeError, TypeError):
                continue

            if not highlight_text or highlight_text.strip() == '':
                continue

            # Check if there's a note for this highlight
            note_text = None
            if note_tag_id:
                cursor.execute("""
                    SELECT Val FROM Tags
                    WHERE ItemID = ? AND TagID = ?
                """, (highlight['HighlightID'], note_tag_id))
                note_result = cursor.fetchone()
                if note_result:
                    note_text = note_result['Val']

            # Group by book title
            if title not in books_dict:
                books_dict[title] = {
                    'title': title,
                    'author': author,
                    'highlights': []
                }

            books_dict[title]['highlights'].append({
                'text': highlight_text.strip(),
                'annotation': note_text,
                'position': page_num,
                'epubcfi': epubcfi,
                'timestamp': highlight['TimeAlt'],
                'type': 'highlight'
            })

        # Convert to list
        books_with_highlights = list(books_dict.values())

        conn.close()
        return books_with_highlights

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()
        conn.close()
        return []


def sanitize_filename(filename):
    """Convert title to safe filename."""
    # Remove or replace characters not allowed in filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    return filename.strip()


def format_timestamp(timestamp):
    """Format Unix timestamp to readable date."""
    if timestamp:
        try:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        except (ValueError, OSError):
            return None
    return None


def create_obsidian_note(book, obsidian_path, calibre_info=None, calibre_library_path=None, highlights_folder_name='Book Highlights'):
    """Create Obsidian markdown file for a book with highlights."""
    highlights_folder = obsidian_path / highlights_folder_name
    highlights_folder.mkdir(exist_ok=True)

    # Create safe filename
    filename = sanitize_filename(f"{book['title']}.md")
    filepath = highlights_folder / filename

    # Build markdown content
    content = []

    # Frontmatter
    content.append('---')
    content.append(f"title: {book['title']}")
    content.append(f"author: {book['author']}")
    content.append(f"type: book-highlights")
    content.append(f"sync_date: {datetime.now().strftime('%Y-%m-%d')}")
    if calibre_info:
        content.append(f"calibre_id: {calibre_info['id']}")
    content.append('---')
    content.append('')

    # Title and metadata
    content.append(f"# {book['title']}")
    content.append(f"**Author:** {book['author']}")
    content.append(f"**Synced:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Add book-level links if Calibre info available
    if calibre_info and calibre_library_path:
        content.append('')
        content.append('**Open in Calibre:**')

        # calibre:// URL - use _ for current library
        calibre_url = f"calibre://show-book/_/{calibre_info['id']}"
        content.append(f"- [View in Calibre](<{calibre_url}>)")

        # file:// path to EPUB
        epub_path = calibre_library_path / calibre_info['path'] / f"{calibre_info['filename']}.epub"
        if epub_path.exists():
            file_url = epub_path.as_uri()
            content.append(f"- [Open EPUB file](<{file_url}>)")

    content.append('')
    content.append('---')
    content.append('')

    # Highlights
    content.append('## Highlights')
    content.append('')

    for idx, highlight in enumerate(book['highlights'], 1):
        # Main highlight text
        if highlight['text']:
            content.append(f"> {highlight['text']}")
            content.append('')

        # Add annotation/note if exists
        if highlight['annotation']:
            content.append(f"**Note:** {highlight['annotation']}")
            content.append('')

        # Add metadata with page/link info
        metadata_parts = []

        # Page number
        if highlight.get('position'):
            metadata_parts.append(f"Page {highlight['position']}")

        # Timestamp
        timestamp = format_timestamp(highlight['timestamp'])
        if timestamp:
            metadata_parts.append(f"Added: {timestamp}")

        if metadata_parts:
            content.append(f"*{' | '.join(metadata_parts)}*")

        # Add Calibre deep link
        if calibre_info and calibre_library_path and highlight.get('epubcfi'):
            # Use _ for current library, URL-encode the EPUB CFI
            epubcfi_encoded = quote(highlight['epubcfi'], safe='')
            calibre_url = f"calibre://view-book/_/{calibre_info['id']}/EPUB?open_at={epubcfi_encoded}"
            content.append(f"[📖 Open in Calibre](<{calibre_url}>)")
        elif calibre_info and calibre_library_path:
            # Fallback if no EPUB CFI available
            calibre_url = f"calibre://view-book/_/{calibre_info['id']}/EPUB"
            content.append(f"[📖 Open in Calibre](<{calibre_url}>)")

        content.append('')

        # Add separator between highlights
        if idx < len(book['highlights']):
            content.append('---')
            content.append('')

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    return filepath


def main():
    """Main sync function."""
    print("=" * 60)
    print("Pocketbook to Obsidian Highlights Sync")
    print("=" * 60)
    print()

    # Load config for highlights folder name
    config = load_config()
    highlights_folder_name = config.get('highlights_folder', 'Book Highlights')

    # Get paths
    pocketbook_path = get_pocketbook_path()
    obsidian_path = get_obsidian_path()
    calibre_library_path = get_calibre_library_path()

    # Find database
    db_path = pocketbook_path / 'system' / 'config' / 'books.db'

    if not db_path.exists():
        print(f"\nError: Database not found at {db_path}")
        print("Please check that your Pocketbook is properly connected.")
        sys.exit(1)

    print(f"\nExtracting highlights from: {db_path}")

    # Extract highlights
    books_with_highlights = extract_highlights(db_path)

    if not books_with_highlights:
        print("\nNo highlights found in the database.")
        print("Make sure you have highlighted text in some books on your Pocketbook.")
        sys.exit(0)

    print(f"\nFound {len(books_with_highlights)} book(s) with highlights:")
    for book in books_with_highlights:
        print(f"  - {book['title']} by {book['author']} ({len(book['highlights'])} highlights)")

    # Create Obsidian notes
    print(f"\nCreating notes in: {obsidian_path / highlights_folder_name}")

    if calibre_library_path:
        print(f"Looking up books in Calibre library...")

    created_files = []
    for book in books_with_highlights:
        # Look up book in Calibre if library path is available
        calibre_info = None
        if calibre_library_path:
            calibre_info = lookup_calibre_book(calibre_library_path, book['title'], book['author'])

        filepath = create_obsidian_note(book, obsidian_path, calibre_info, calibre_library_path, highlights_folder_name)
        created_files.append(filepath)

        if calibre_info:
            print(f"  ✓ Created: {filepath.name} (with Calibre links)")
        else:
            print(f"  ✓ Created: {filepath.name}")

    print(f"\n{'=' * 60}")
    print(f"Sync complete! Created {len(created_files)} file(s).")
    if calibre_library_path:
        matched = sum(1 for book in books_with_highlights if lookup_calibre_book(calibre_library_path, book['title'], book['author']))
        print(f"Matched {matched} book(s) to Calibre library.")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSync cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
