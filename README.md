# note-taker

Quickly save and search short notes.

Notes are stored one per line as JSON in
`~/.local/share/note-taker/notes.jsonl` by default; use `--file` to
choose a different location.

## Requirements

- Python 3
- No third-party packages

## How to run

```bash
python3 main.py [--file notes.jsonl] add "Idea: ..." [--tag idea]
python3 main.py list [--limit 20]
python3 main.py search "keyword" [--tag idea]
python3 main.py delete 1
```

## Example

```bash
python3 main.py --file /tmp/notes.jsonl add "Call supplier about laptops" --tag work
python3 main.py --file /tmp/notes.jsonl search "supplier"
```

Sample output:

```
Saved: Call supplier about laptops
1 match(es):
[2026-11-25 10:15] Call supplier about laptops [work]
```

## License

MIT — see `LICENSE`.
