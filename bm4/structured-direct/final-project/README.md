# Priority Picker

A dependency-free backlog dashboard with a deterministic priority score. Run it from the repository root:

```sh
python -m priority_picker.server --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>. To use another backlog file, pass `--data path/to/backlog.json`.

Run the focused public tests with:

```sh
python -m unittest discover -s tests/public -v
```

Priority is `(2 × impact + 1.5 × urgency + confidence + 0.5 × risk) ÷ max(effort, 1)`, rounded to four decimals. Ties rank by urgency, impact, and then ID.
