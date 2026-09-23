# Priority Picker

A dependency-free backlog dashboard and Python scoring module.

## Run the dashboard

From the repository root, start the standard-library server:

```sh
python -m priority_picker.server --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>. The app reads `data/backlog.json`; pass `--data PATH` to serve a different JSON backlog.

## Python API

Import `calculate_priority`, `validate_items`, `rank_items`, `filter_items`, `sort_items`, `export_ordering`, or `load_backlog` from `priority_picker.priority`. Validation errors raise `BacklogValidationError`.

Run the public tests with:

```sh
python -m unittest discover -s tests/public -v
```
