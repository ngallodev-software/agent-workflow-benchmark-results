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
    load_backlog, rank_items, sort_items, validate_items,
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

    def test_duplicate_ids_and_malformed_records_are_rejected(self) -> None:
        with self.assertRaisesRegex(BacklogValidationError, "duplicate id"):
            validate_items([ITEM, dict(ITEM)])
        with self.assertRaisesRegex(BacklogValidationError, "title"):
            validate_items([{**ITEM, "title": ""}])

    def test_decimal_values_and_empty_input(self) -> None:
        item = {**ITEM, "impact": Decimal("4.5"), "effort": Decimal("2.5")}
        self.assertEqual(calculate_priority(item), 7.6)
        self.assertEqual(validate_items([]), [])
        self.assertEqual(rank_items([]), [])
        with tempfile.TemporaryDirectory() as directory:
            path = export_ordering([item], Path(directory) / "decimal.json")
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))[0]["impact"], 4.5)

    def test_public_functions_do_not_mutate_inputs(self) -> None:
        original = dict(ITEM)
        sequence = [original]
        result = rank_items(sequence)
        self.assertIsNot(result, sequence)
        self.assertIsNot(result[0], original)
        self.assertEqual(original, ITEM)
        self.assertEqual(sequence, [ITEM])

    def test_sort_rejects_unknown_key_and_direction(self) -> None:
        with self.assertRaisesRegex(BacklogValidationError, "sort key"):
            sort_items([ITEM], key="nonsense")
        with self.assertRaisesRegex(BacklogValidationError, "sort direction"):
            sort_items([ITEM], direction="sideways")

    def test_sort_ties_keep_id_ascending_in_both_directions(self) -> None:
        values = [{**ITEM, "id": "B"}, {**ITEM, "id": "A"}]
        self.assertEqual([x["id"] for x in sort_items(values, key="risk", direction="desc")], ["A", "B"])

    def test_thousand_item_ranking_is_deterministic_and_fast(self) -> None:
        values = [{**ITEM, "id": f"item-{index:04d}", "impact": index % 5 + 1} for index in range(1000)]
        started = time.perf_counter()
        ranked = rank_items(values)
        elapsed = time.perf_counter() - started
        self.assertEqual(ranked, rank_items(values))
        self.assertLess(elapsed, 2.0)

    def test_loader_rejects_non_array_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "backlog.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(BacklogValidationError, "JSON array"):
                load_backlog(path)

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
