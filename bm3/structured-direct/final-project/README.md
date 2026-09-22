# Priority Picker v2

Dependency-free priority dashboard using Python’s standard library and browser-native HTML, CSS, and JavaScript.

Run the tests:

```sh
python -m unittest discover -s tests/public -v
```

Run the dashboard from the repository root:

```sh
python -m priority_picker.server --port 8000
```

Open `http://127.0.0.1:8000/`. The server reads `data/backlog.json`; use
`--data PATH` to inspect another compatible backlog without changing the fixture.
