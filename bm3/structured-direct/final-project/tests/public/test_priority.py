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

    def test_decimal_empty_duplicate_and_immutable(self) -> None:
        decimal_item = {**ITEM, "id": "decimal", "impact": Decimal("4.5")}
        original = dict(decimal_item)
        self.assertEqual(len(validate_items([])), 0)
        self.assertEqual(calculate_priority(decimal_item), 9.5)
        self.assertEqual(validate_items([decimal_item])[0], original)
        with self.assertRaises(BacklogValidationError):
            validate_items([decimal_item, dict(decimal_item)])

    def test_unsupported_sort_and_large_input(self) -> None:
        with self.assertRaises(BacklogValidationError):
            sort_items([ITEM], key="unknown")
        values = [{**ITEM, "id": str(index)} for index in range(1000)]
        self.assertEqual(len(rank_items(values)), 1000)

    def test_filter_and_sort(self) -> None:
        values = [{**ITEM, "id": "B", "title": "Zulu"}, {**ITEM, "id": "A", "title": "Alpha", "status": "blocked"}]
        self.assertEqual([x["id"] for x in filter_items(values, query="alpha", status="blocked")], ["A"])
        self.assertEqual([x["id"] for x in sort_items(values, key="title", direction="asc")], ["A", "B"])
        tied = [{**ITEM, "id": "B", "title": "Same"}, {**ITEM, "id": "A", "title": "Same"}]
        self.assertEqual([x["id"] for x in sort_items(tied, key="title", direction="desc")], ["A", "B"])

    def test_export_and_server_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = export_ordering([{**ITEM, "impact": Decimal("4.5")}], Path(directory) / "ordering.json")
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(value[0]["id"], "A")
            self.assertEqual(value[0]["impact"], 4.5)
        from priority_picker.server import Handler
        self.assertTrue(callable(getattr(Handler, "do_GET", None)))

if __name__ == "__main__":
    unittest.main()
