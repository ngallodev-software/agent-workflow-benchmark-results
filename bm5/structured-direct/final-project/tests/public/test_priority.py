from __future__ import annotations

import json
import tempfile
import time
import unittest
from copy import deepcopy
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

    def test_decimal_values_and_four_place_rounding(self) -> None:
        value = {**ITEM, "impact": Decimal("4.25"), "urgency": Decimal("3.5")}
        self.assertEqual(calculate_priority(value), round((2 * 4.25 + 1.5 * 3.5 + 3 + .5 * 2) / 2, 4))

    def test_rejects_duplicates_missing_fields_and_unsupported_sort(self) -> None:
        with self.assertRaisesRegex(BacklogValidationError, "duplicate"):
            validate_items([ITEM, dict(ITEM)])
        with self.assertRaisesRegex(BacklogValidationError, "missing"):
            validate_items([{key: value for key, value in ITEM.items() if key != "risk"}])
        for key, direction in (("unknown", "asc"), ("title", "sideways")):
            with self.subTest(key=key, direction=direction), self.assertRaises(BacklogValidationError):
                sort_items([ITEM], key=key, direction=direction)

    def test_empty_input_and_operations_do_not_mutate_callers(self) -> None:
        self.assertEqual(validate_items([]), [])
        self.assertEqual(rank_items([]), [])
        original = [{**ITEM, "metadata": {"keep": True}}]
        snapshot = deepcopy(original)
        ranked = rank_items(original)
        ranked[0]["metadata"]["keep"] = False
        self.assertEqual(original, snapshot)
        self.assertEqual(original[0]["metadata"]["keep"], True)

    def test_thousand_items_rank_comfortably(self) -> None:
        values = [{**ITEM, "id": f"item-{index:04}", "impact": index % 5 + 1} for index in range(1000)]
        start = time.perf_counter()
        ranked = rank_items(values)
        self.assertEqual(len(ranked), 1000)
        self.assertLess(time.perf_counter() - start, 2)

    def test_export_accepts_decimal_values(self) -> None:
        value = {**ITEM, "risk": Decimal("4.5")}
        with tempfile.TemporaryDirectory() as directory:
            path = export_ordering([value], Path(directory) / "ordering.json")
            self.assertEqual(json.loads(path.read_text())[0]["risk"], 4.5)

if __name__ == "__main__":
    unittest.main()
