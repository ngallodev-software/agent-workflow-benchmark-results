from __future__ import annotations

import json
import math
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable


class BacklogValidationError(ValueError):
    """Raised when the supplied backlog does not match the frozen contract."""


NUMERIC_FIELDS = ("impact", "urgency", "effort", "confidence", "risk")
STATUSES = ("planned", "ready", "in_progress", "blocked")
SORT_KEYS = ("priority", "title", "id", "impact", "urgency", "effort", "confidence", "risk", "status")


def _number(value: Any, field: str, item_id: str = "") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise BacklogValidationError(f"{field} for {item_id or 'item'} must be a number from 1 through 5")
    try:
        numeric = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise BacklogValidationError(f"{field} for {item_id or 'item'} must be a number from 1 through 5") from exc
    if not math.isfinite(numeric) or not 1 <= value <= 5:
        raise BacklogValidationError(f"{field} for {item_id or 'item'} must be a number from 1 through 5")
    return numeric


def _copy_and_validate(item: Any, index: int) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise BacklogValidationError(f"item {index + 1} must be an object")
    missing = [field for field in ("id", "title", *NUMERIC_FIELDS, "status", "description") if field not in item]
    if missing:
        raise BacklogValidationError(f"item {index + 1} is missing required field(s): {', '.join(missing)}")
    item_id = item["id"]
    if not isinstance(item_id, str) or not item_id.strip():
        raise BacklogValidationError(f"item {index + 1} id must be a non-empty string")
    if not isinstance(item["title"], str) or not item["title"].strip():
        raise BacklogValidationError(f"title for {item_id} must be a non-empty string")
    if not isinstance(item["description"], str):
        raise BacklogValidationError(f"description for {item_id} must be a string")
    for field in NUMERIC_FIELDS:
        _number(item[field], field, item_id)
    if item["status"] not in STATUSES:
        raise BacklogValidationError(f"status for {item_id} must be one of: {', '.join(STATUSES)}")
    return dict(item)


def calculate_priority(item: dict[str, Any]) -> float:
    """Return the frozen four-decimal priority score for one valid item."""
    checked = _copy_and_validate(item, 0)
    values = {field: Decimal(str(checked[field])) for field in NUMERIC_FIELDS}
    score = (
        2 * values["impact"]
        + Decimal("1.5") * values["urgency"]
        + values["confidence"]
        + Decimal("0.5") * values["risk"]
    ) / max(values["effort"], Decimal(1))
    return float(round(score, 4))


def validate_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate and shallow-copy every backlog record without mutating the input."""
    try:
        values = list(items)
    except TypeError as exc:
        raise BacklogValidationError("backlog must be an iterable of objects") from exc
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(values):
        checked = _copy_and_validate(item, index)
        if checked["id"] in seen:
            raise BacklogValidationError(f"duplicate id: {checked['id']}")
        seen.add(checked["id"])
        result.append(checked)
    return result


def rank_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    values = validate_items(items)
    return sorted(
        values,
        key=lambda item: (-calculate_priority(item), -float(item["urgency"]), -float(item["impact"]), item["id"]),
    )


def filter_items(
    items: Iterable[dict[str, Any]],
    query: str = "",
    status: str = "all",
    risk: str = "all",
) -> list[dict[str, Any]]:
    values = validate_items(items)
    if not isinstance(query, str):
        raise BacklogValidationError("query must be a string")
    if status != "all" and status not in STATUSES:
        raise BacklogValidationError(f"unknown status filter: {status}")
    if risk != "all":
        try:
            risk_value = int(risk)
        except (TypeError, ValueError) as exc:
            raise BacklogValidationError("risk filter must be all or a value from 1 through 5") from exc
        if str(risk_value) != str(risk) or not 1 <= risk_value <= 5:
            raise BacklogValidationError("risk filter must be all or a value from 1 through 5")
    needle = query.casefold().strip()
    return [
        item
        for item in values
        if (not needle or needle in f"{item['id']} {item['title']} {item['description']}".casefold())
        and (status == "all" or item["status"] == status)
        and (risk == "all" or item["risk"] == int(risk))
    ]


def sort_items(
    items: Iterable[dict[str, Any]], key: str = "priority", direction: str = "desc"
) -> list[dict[str, Any]]:
    values = validate_items(items)
    if key not in SORT_KEYS:
        raise BacklogValidationError(f"unsupported sort key: {key}")
    if direction not in ("asc", "desc"):
        raise BacklogValidationError(f"unsupported sort direction: {direction}")
    value = (lambda item: calculate_priority(item)) if key == "priority" else (lambda item: item[key])
    values.sort(key=lambda item: item["id"])
    values.sort(key=value, reverse=direction == "desc")
    return values


def export_ordering(items: Iterable[dict[str, Any]], destination: str | Path) -> Path:
    values = validate_items(items)
    path = Path(destination)
    path.write_text(json.dumps(values, indent=2, default=float) + "\n", encoding="utf-8")
    return path


def load_backlog(path: str | Path) -> list[dict[str, Any]]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BacklogValidationError(f"invalid backlog JSON: {exc.msg}") from exc
    if not isinstance(value, list):
        raise BacklogValidationError("backlog root must be a JSON array")
    return validate_items(value)
