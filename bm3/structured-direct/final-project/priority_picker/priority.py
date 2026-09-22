from __future__ import annotations

import json
import math
import numbers
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable


class BacklogValidationError(ValueError):
    """Raised when the supplied backlog does not match the frozen contract."""


def calculate_priority(item: dict[str, Any]) -> float:
    try:
        impact, urgency = item["impact"], item["urgency"]
        confidence, risk, effort = item["confidence"], item["risk"], item["effort"]
    except (KeyError, TypeError) as exc:
        raise BacklogValidationError(f"missing scoring field: {exc}") from exc
    values = {"impact": impact, "urgency": urgency, "confidence": confidence,
              "risk": risk, "effort": effort}
    for name, value in values.items():
        if not _valid_number(value):
            raise BacklogValidationError(f"{name} must be a finite number from 1 through 5")
    impact, urgency, confidence, risk, effort = map(float, (impact, urgency, confidence, risk, effort))
    return round((2 * impact + 1.5 * urgency + confidence + 0.5 * risk) / max(effort, 1), 4)


def validate_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(items, (str, bytes)):
        raise BacklogValidationError("backlog must be an iterable of records")
    required = {"id", "title", "impact", "urgency", "effort", "confidence", "risk", "status", "description"}
    statuses = {"planned", "ready", "in_progress", "blocked"}
    result, seen = [], set()
    try:
        records = iter(items)
    except TypeError as exc:
        raise BacklogValidationError("backlog must be an iterable of records") from exc
    for index, item in enumerate(records):
        if not isinstance(item, dict):
            raise BacklogValidationError(f"item {index} must be an object")
        missing = required - item.keys()
        if missing:
            raise BacklogValidationError(f"item {index} missing required field(s): {', '.join(sorted(missing))}")
        if not isinstance(item["id"], str) or not item["id"].strip():
            raise BacklogValidationError(f"item {index} id must be a non-empty string")
        if item["id"] in seen:
            raise BacklogValidationError(f"duplicate id: {item['id']}")
        if not isinstance(item["title"], str) or not item["title"].strip():
            raise BacklogValidationError(f"item {index} title must be a non-empty string")
        if not isinstance(item["description"], str):
            raise BacklogValidationError(f"item {index} description must be a string")
        if item["status"] not in statuses:
            raise BacklogValidationError(f"item {index} status must be one of: {', '.join(sorted(statuses))}")
        calculate_priority(item)
        seen.add(item["id"])
        result.append(dict(item))
    return result


def rank_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    values = validate_items(items)
    return sorted(values, key=lambda item: (-calculate_priority(item), -item["urgency"], -item["impact"], item["id"]))


def filter_items(
    items: Iterable[dict[str, Any]],
    query: str = "",
    status: str = "all",
    risk: str = "all",
) -> list[dict[str, Any]]:
    values = validate_items(items)
    if status != "all" and status not in {"planned", "ready", "in_progress", "blocked"}:
        raise BacklogValidationError("unsupported status filter")
    if risk != "all":
        try:
            risk_value = float(risk)
        except (TypeError, ValueError) as exc:
            raise BacklogValidationError("risk filter must be all or a value from 1 through 5") from exc
        if risk_value not in range(1, 6):
            raise BacklogValidationError("risk filter must be all or a value from 1 through 5")
    else:
        risk_value = None
    needle = str(query).strip().casefold()
    return [item for item in values if (not needle or needle in item["id"].casefold() or needle in item["title"].casefold() or needle in item["description"].casefold()) and (status == "all" or item["status"] == status) and (risk_value is None or item["risk"] == risk_value)]


def sort_items(
    items: Iterable[dict[str, Any]], key: str = "priority", direction: str = "desc"
) -> list[dict[str, Any]]:
    values = validate_items(items)
    keys = {"priority", "id", "title", "status", "impact", "urgency", "effort", "confidence", "risk"}
    if key not in keys:
        raise BacklogValidationError(f"unsupported sort key: {key}")
    if direction not in {"asc", "desc"}:
        raise BacklogValidationError(f"unsupported sort direction: {direction}")
    def value(item: dict[str, Any]) -> Any:
        return calculate_priority(item) if key == "priority" else item[key]
    # Sort IDs first so ties stay deterministic and ascending in either direction.
    values.sort(key=lambda item: item["id"])
    return sorted(values, key=value, reverse=direction == "desc")


def export_ordering(items: Iterable[dict[str, Any]], destination: str | Path) -> Path:
    path = Path(destination)
    path.write_text(json.dumps(validate_items(items), indent=2, default=_json_default) + "\n", encoding="utf-8")
    return path


def _valid_number(value: object) -> bool:
    return (isinstance(value, numbers.Real) or isinstance(value, Decimal)) and not isinstance(value, bool) and math.isfinite(value) and 1 <= value <= 5


def _json_default(value: object) -> object:
    if isinstance(value, Decimal):
        return float(value)
    raise TypeError(f"value is not JSON serializable: {type(value).__name__}")


def load_backlog(path: str | Path) -> list[dict[str, Any]]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise BacklogValidationError("backlog root must be a JSON array")
    return validate_items(value)
