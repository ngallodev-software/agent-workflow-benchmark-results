from __future__ import annotations

import json
import math
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable


class BacklogValidationError(ValueError):
    """Raised when the supplied backlog does not match the frozen contract."""


def calculate_priority(item: dict[str, Any]) -> float:
    validate_items([item])
    return round(
        (2 * float(item["impact"]) + 1.5 * float(item["urgency"]) + float(item["confidence"]) + 0.5 * float(item["risk"]))
        / max(float(item["effort"]), 1),
        4,
    )


def validate_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(items, (str, bytes, dict)):
        raise BacklogValidationError("backlog must be an iterable of item objects")
    try:
        values = list(items)
    except TypeError as exc:
        raise BacklogValidationError("backlog must be an iterable of item objects") from exc
    required = {"id", "title", "impact", "urgency", "effort", "confidence", "risk", "status", "description"}
    statuses = {"planned", "ready", "in_progress", "blocked"}
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for index, item in enumerate(values):
        label = f"item {index}"
        if not isinstance(item, dict):
            raise BacklogValidationError(f"{label} must be an object")
        missing = required - item.keys()
        if missing:
            raise BacklogValidationError(f"{label} is missing required field(s): {', '.join(sorted(missing))}")
        if not isinstance(item["id"], str) or not item["id"].strip():
            raise BacklogValidationError(f"{label} id must be a non-empty string")
        if item["id"] in seen:
            raise BacklogValidationError(f"duplicate id {item['id']!r}")
        seen.add(item["id"])
        if not isinstance(item["title"], str) or not item["title"].strip():
            raise BacklogValidationError(f"{label} title must be a non-empty string")
        for field in ("impact", "urgency", "effort", "confidence", "risk"):
            value = item[field]
            if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
                raise BacklogValidationError(f"{label} {field} must be a number from 1 through 5")
            if not math.isfinite(float(value)) or not 1 <= value <= 5:
                raise BacklogValidationError(f"{label} {field} must be a number from 1 through 5")
        if not isinstance(item["status"], str) or item["status"] not in statuses:
            raise BacklogValidationError(f"{label} status must be one of: {', '.join(sorted(statuses))}")
        if not isinstance(item["description"], str):
            raise BacklogValidationError(f"{label} description must be a string")
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
    needle = str(query).casefold().strip()
    if status != "all" and (not isinstance(status, str) or status not in {"planned", "ready", "in_progress", "blocked"}):
        raise BacklogValidationError(f"unsupported status filter: {status!r}")
    if risk != "all":
        try:
            risk_value = float(risk)
        except (TypeError, ValueError) as exc:
            raise BacklogValidationError(f"unsupported risk filter: {risk!r}") from exc
        if risk_value not in (1, 2, 3, 4, 5):
            raise BacklogValidationError(f"unsupported risk filter: {risk!r}")
    else:
        risk_value = None
    return [item for item in values if (not needle or needle in item["title"].casefold() or needle in item["description"].casefold() or needle in item["id"].casefold()) and (status == "all" or item["status"] == status) and (risk_value is None or item["risk"] == risk_value)]


def sort_items(
    items: Iterable[dict[str, Any]], key: str = "priority", direction: str = "desc"
) -> list[dict[str, Any]]:
    values = validate_items(items)
    keys = {"priority", "title", "id", "impact", "urgency", "effort", "confidence", "risk", "status", "description"}
    if not isinstance(key, str) or key not in keys:
        raise BacklogValidationError(f"unsupported sort key: {key!r}")
    if not isinstance(direction, str) or direction not in {"asc", "desc"}:
        raise BacklogValidationError(f"unsupported sort direction: {direction!r}")
    reverse = direction == "desc"
    if key == "priority":
        values.sort(key=lambda item: item["id"])
        values.sort(key=lambda item: (-item["urgency"], -item["impact"]))
        return sorted(values, key=calculate_priority, reverse=reverse)
    primary = (lambda item: calculate_priority(item)) if key == "priority" else (lambda item: item[key])
    values.sort(key=lambda item: item["id"])
    return sorted(values, key=primary, reverse=reverse)


def export_ordering(items: Iterable[dict[str, Any]], destination: str | Path) -> Path:
    path = Path(destination)
    path.write_text(json.dumps(rank_items(items), indent=2, ensure_ascii=False, default=lambda value: float(value) if isinstance(value, Decimal) else value) + "\n", encoding="utf-8")
    return path


def load_backlog(path: str | Path) -> list[dict[str, Any]]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise BacklogValidationError("backlog root must be a JSON array")
    return validate_items(value)
