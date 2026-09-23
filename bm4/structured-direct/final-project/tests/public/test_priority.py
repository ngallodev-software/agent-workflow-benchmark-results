from __future__ import annotations

import json
import time
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

    def test_duplicate_and_malformed_records_are_rejected(self) -> None:
        with self.assertRaisesRegex(BacklogValidationError, "duplicate"):
            validate_items([ITEM, dict(ITEM)])
        with self.assertRaisesRegex(BacklogValidationError, "missing"):
            validate_items([{key: value for key, value in ITEM.items() if key != "risk"}])
        with self.assertRaisesRegex(BacklogValidationError, "title"):
            validate_items([{**ITEM, "title": "  "}])

    def test_decimal_range_and_four_place_rounding(self) -> None:
        item = {**ITEM, "impact": Decimal("1.25"), "urgency": Decimal("2.15"),
                "effort": Decimal("3.1"), "confidence": Decimal("4.2"), "risk": Decimal("1.1")}
        self.assertEqual(calculate_priority(item), 3.379)
        self.assertEqual(validate_items([item])[0]["impact"], 1.25)
        with tempfile.TemporaryDirectory() as directory:
            exported = export_ordering([item], Path(directory) / "decimal.json")
            self.assertEqual(json.loads(exported.read_text(encoding="utf-8"))[0]["impact"], 1.25)
        self.assertIsInstance(item["impact"], Decimal)

    def test_empty_and_inputs_are_not_mutated(self) -> None:
        self.assertEqual(validate_items([]), [])
        self.assertEqual(rank_items([]), [])
        source = [dict(ITEM)]
        before = json.dumps(source)
        rank_items(source)
        sort_items(source)
        filter_items(source, query="example")
        self.assertEqual(json.dumps(source), before)

    def test_unsupported_sort_options_are_rejected(self) -> None:
        for key, direction in (("unknown", "asc"), ("title", "sideways")):
            with self.subTest(key=key, direction=direction), self.assertRaises(BacklogValidationError):
                sort_items([ITEM], key=key, direction=direction)

    def test_thousand_items_rank_quickly(self) -> None:
        values = [{**ITEM, "id": f"item-{index:04d}", "impact": index % 5 + 1} for index in range(1000)]
        started = time.perf_counter()
        ranked = rank_items(values)
        self.assertEqual(len(ranked), 1000)
        self.assertLess(time.perf_counter() - started, 2)

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

if __name__ == "__main__":
    unittest.main()
