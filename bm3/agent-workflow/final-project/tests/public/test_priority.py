from __future__ import annotations

import json
import time
import tempfile
import unittest
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from urllib.request import urlopen

from priority_picker.priority import (
    BacklogValidationError, calculate_priority, export_ordering, filter_items,
    rank_items, sort_items, validate_items, load_backlog,
)

ITEM = {
    "id": "A", "title": "Example", "impact": 5, "urgency": 4,
    "effort": 2, "confidence": 3, "risk": 2, "status": "ready",
    "description": "Example item",
}

class PriorityTests(unittest.TestCase):
    def test_frozen_formula(self) -> None:
        self.assertEqual(calculate_priority(dict(ITEM)), 10.0)

    def test_ranking_uses_frozen_tie_breakers(self) -> None:
        low_id = {**ITEM, "id": "A", "title": "A"}
        high_id = {**ITEM, "id": "B", "title": "B"}
        self.assertEqual([item["id"] for item in rank_items([high_id, low_id])], ["A", "B"])

    def test_malformed_range_is_rejected(self) -> None:
        with self.assertRaises(BacklogValidationError):
            validate_items([{**ITEM, "effort": 0}])

    def test_filter_and_sort(self) -> None:
        values = [{**ITEM, "id": "B", "title": "Zulu"}, {**ITEM, "id": "A", "title": "Alpha", "status": "blocked"}]
        self.assertEqual([x["id"] for x in filter_items(values, query="alpha", status="blocked")], ["A"])
        self.assertEqual([x["id"] for x in sort_items(values, key="title", direction="asc")], ["A", "B"])

    def test_export_and_server_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = export_ordering([ITEM], Path(directory) / "ordering.json")
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(value[0]["id"], "A")
        from priority_picker.server import Handler
        self.assertTrue(callable(getattr(Handler, "do_GET", None)))

    def test_decimal_and_public_functions_do_not_mutate_input(self) -> None:
        item = {**ITEM, "impact": Decimal("4.5"), "extra": {"keep": True}}
        original = deepcopy(item)
        validated = validate_items([item])
        self.assertEqual(item, original)
        self.assertIsNot(validated[0], item)
        self.assertEqual(calculate_priority(item), 9.5)
        self.assertEqual(item, original)

    def test_validation_rejects_duplicates_missing_fields_and_bad_sort_options(self) -> None:
        with self.assertRaisesRegex(BacklogValidationError, "duplicate"):
            validate_items([ITEM, dict(ITEM)])
        with self.assertRaisesRegex(BacklogValidationError, "missing"):
            validate_items([{key: value for key, value in ITEM.items() if key != "title"}])
        with self.assertRaises(BacklogValidationError):
            sort_items([ITEM], key="bogus")
        with self.assertRaises(BacklogValidationError):
            sort_items([ITEM], direction="sideways")

    def test_empty_and_scale(self) -> None:
        self.assertEqual(validate_items([]), [])
        values = [{**ITEM, "id": f"item-{index:04d}", "urgency": index % 5 + 1} for index in range(1000)]
        started = time.perf_counter()
        ranked = rank_items(values)
        self.assertEqual(len(ranked), 1000)
        self.assertLess(time.perf_counter() - started, 2)

    def test_load_rejects_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaisesRegex(BacklogValidationError, "invalid backlog JSON"):
                load_backlog(path)

if __name__ == "__main__":
    unittest.main()
