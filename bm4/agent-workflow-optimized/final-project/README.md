# Priority Picker

A dependency-free backlog dashboard and Python priority API. From the repository root, run:

```sh
python -m priority_picker.server --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>. The server reads `data/backlog.json`; edit that file to change the backlog. Search matches IDs, titles, and descriptions. Status and risk filters can be combined with the sort control. Select **View details** to read the description and factor breakdown. **Export JSON** downloads the currently filtered and sorted items.

The score is `(2 × impact + 1.5 × urgency + confidence + 0.5 × risk) ÷ max(effort, 1)`, rounded to four decimal places. Default ties sort by urgency, impact, then ID. Invalid records are reported in the dashboard and rejected by the Python API.

The public API is in `priority_picker.priority`; run its tests with `python -m unittest discover -s tests/public -v`.
