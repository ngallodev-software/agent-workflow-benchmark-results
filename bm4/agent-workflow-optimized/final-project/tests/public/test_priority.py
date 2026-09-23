from __future__ import annotations

import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from urllib.request import urlopen

from priority_picker.priority import (
    BacklogValidationError, calculate_priority, export_ordering, filter_items,
    rank_items, sort_items, validate_items,
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

    def test_decimal_score_and_caller_data_are_preserved(self) -> None:
        value = {**ITEM, "impact": Decimal("1.25"), "urgency": Decimal("2.5")}
        original = value.copy()
        self.assertEqual(calculate_priority(value), 5.125)
        result = rank_items([value])
        self.assertEqual(result[0]["impact"], Decimal("1.25"))
        self.assertEqual(value, original)

    def test_rejects_duplicate_ids_and_non_numeric_factors(self) -> None:
        with self.assertRaisesRegex(BacklogValidationError, "duplicate id"):
            validate_items([ITEM, dict(ITEM)])
        with self.assertRaises(BacklogValidationError):
            validate_items([{**ITEM, "risk": "3"}])

    def test_empty_and_unsupported_sort_inputs(self) -> None:
        self.assertEqual(rank_items([]), [])
        self.assertEqual(filter_items([]), [])
        for key, direction in (("unknown", "asc"), ("title", "sideways")):
            with self.subTest(key=key, direction=direction), self.assertRaises(BacklogValidationError):
                sort_items([], key=key, direction=direction)
        with self.assertRaises(BacklogValidationError):
            sort_items([], key=[])  # type: ignore[arg-type]

    def test_filter_and_sort(self) -> None:
        values = [{**ITEM, "id": "B", "title": "Zulu"}, {**ITEM, "id": "A", "title": "Alpha", "status": "blocked"}]
        self.assertEqual([x["id"] for x in filter_items(values, query="alpha", status="blocked")], ["A"])
        self.assertEqual([x["id"] for x in sort_items(values, key="title", direction="asc")], ["A", "B"])

    def test_export_and_server_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = export_ordering([{**ITEM, "id": "B"}, {**ITEM, "id": "A"}], Path(directory) / "ordering.json")
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual([item["id"] for item in value], ["B", "A"])
        from priority_picker.server import Handler
        self.assertTrue(callable(getattr(Handler, "do_GET", None)))

if __name__ == "__main__":
    unittest.main()
