#!/usr/bin/env python3
"""Quickly save and search short notes.

Notes are stored one per line as JSON in a plain text file, so the
file stays readable and grep-able.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_FILE = Path.home() / ".local" / "share" / "note-taker" / "notes.jsonl"


def load(path):
    notes = []
    if not path.exists():
        return notes
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            notes.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return notes


def append(path, note):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(note) + "\n")


def show(note, index=None):
    prefix = f"{index}. " if index is not None else ""
    tags = f" [{', '.join(note.get('tags', []))}]" if note.get("tags") else ""
    print(f"{prefix}[{note['created']}] {note['text']}{tags}")


def main():
    parser = argparse.ArgumentParser(description="Save and search short notes.")
    parser.add_argument("--file", default=str(DEFAULT_FILE),
                        help="Notes file (default: ~/.local/share/note-taker/notes.jsonl)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Save a note")
    p_add.add_argument("text", help="Note text")
    p_add.add_argument("--tag", action="append", default=[],
                       help="Tag for the note (repeatable)")

    p_list = sub.add_parser("list", help="List notes")
    p_list.add_argument("--limit", type=int, default=20,
                        help="Max notes to show (default: 20)")

    p_search = sub.add_parser("search", help="Search notes")
    p_search.add_argument("query", help="Text to search for (case-insensitive)")
    p_search.add_argument("--tag", default=None, help="Only notes with this tag")

    p_del = sub.add_parser("delete", help="Delete a note by number (see list)")
    p_del.add_argument("number", type=int, help="Note number from list output")
    args = parser.parse_args()
    path = Path(args.file).expanduser()

    if args.command == "add":
        note = {"created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "text": args.text, "tags": args.tag}
        append(path, note)
        print(f"Saved: {args.text}")
    elif args.command == "list":
        notes = load(path)
        if not notes:
            print("No notes yet.")
            return
        for i, note in enumerate(notes[-args.limit:], start=max(1, len(notes) - args.limit + 1)):
            show(note, i)
    elif args.command == "search":
        notes = load(path)
        query = args.query.lower()
        hits = [n for n in notes
                if query in n["text"].lower()
                and (not args.tag or args.tag in n.get("tags", []))]
        if not hits:
            print(f"No notes matching {args.query!r}.")
            return
        print(f"{len(hits)} match(es):")
        for note in hits:
            show(note)
    elif args.command == "delete":
        notes = load(path)
        if not 1 <= args.number <= len(notes):
            print(f"Error: no note #{args.number}.", file=sys.stderr)
            sys.exit(1)
        removed = notes.pop(args.number - 1)
        path.write_text("".join(json.dumps(n) + "\n" for n in notes),
                        encoding="utf-8")
        print(f"Deleted: {removed['text']}")


if __name__ == "__main__":
    main()
