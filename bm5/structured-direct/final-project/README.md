# Priority Picker v3

A dependency-free backlog dashboard and Python priority-scoring module.

## Run

From the project root, start the standard-library server, then open `http://127.0.0.1:8000`:

```sh
python -m priority_picker.server
```

The server reads `data/backlog.json`. Use search, status and risk filters, and sort controls to explore the ranked backlog. Select an item for its description and scoring breakdown; **Export JSON** downloads the current filtered ordering. **Show debug** reveals request and UI state details.

## Verify

```sh
python -m unittest discover -s tests/public -v
```
