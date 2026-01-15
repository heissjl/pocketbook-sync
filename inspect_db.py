#!/usr/bin/env python3
"""
Quick script to inspect the Pocketbook database schema.
Run this to see what tables and columns exist in your books.db
"""

import sqlite3
import sys
from pathlib import Path

def inspect_database(db_path):
    """Inspect database structure and show sample data."""
    print(f"Inspecting: {db_path}\n")

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]

        print(f"Found {len(tables)} tables:")
        print("=" * 60)

        for table in tables:
            print(f"\n📊 Table: {table}")
            print("-" * 60)

            # Get column info
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()

            print("Columns:")
            for col in columns:
                print(f"  - {col['name']:20} {col['type']:15} {'PRIMARY KEY' if col['pk'] else ''}")

            # Get row count
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = cursor.fetchone()['count']
            print(f"\nRow count: {count}")

            # Show sample data if table has rows
            if count > 0:
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                rows = cursor.fetchall()
                if rows:
                    print("\nSample data (first 3 rows):")
                    for i, row in enumerate(rows, 1):
                        print(f"\n  Row {i}:")
                        for key in row.keys():
                            value = row[key]
                            if value is not None:
                                # Truncate long values
                                if isinstance(value, str) and len(value) > 50:
                                    value = value[:47] + "..."
                                print(f"    {key}: {value}")

        conn.close()
        print("\n" + "=" * 60)
        print("Inspection complete!")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        db_path = Path(sys.argv[1])
    else:
        # Prompt for path
        print("Enter the path to books.db:")
        print("(Usually: /Volumes/PocketBook/system/config/books.db)")
        db_path_str = input("Path: ").strip()
        db_path = Path(db_path_str)

    if not db_path.exists():
        print(f"Error: File not found at {db_path}")
        sys.exit(1)

    inspect_database(db_path)
