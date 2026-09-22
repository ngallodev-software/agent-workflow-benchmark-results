# Priority Picker v2

Priority Picker is a dependency-free backlog dashboard. It validates `data/backlog.json`, calculates the frozen priority score, and serves a ranked, filterable responsive view.

Run the focused test suite:

```sh
python -m unittest discover -s tests/public -v
```

Launch the local dashboard from the repository root:

```sh
python -m priority_picker.server --host 127.0.0.1 --port 8000 --data data/backlog.json
```

Open <http://127.0.0.1:8000/>. The Export ordering button downloads the currently filtered and sorted records as `priority-ordering.json`.
