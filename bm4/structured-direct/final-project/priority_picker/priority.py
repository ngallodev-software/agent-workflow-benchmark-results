from __future__ import annotations

import json
import math
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable


class BacklogValidationError(ValueError):
    """Raised when the supplied backlog does not match the frozen contract."""


FACTORS = ("impact", "urgency", "effort", "confidence", "risk")
STATUSES = ("planned", "ready", "in_progress", "blocked")
SORT_KEYS = ("priority", "title", "status", "urgency", "impact", "effort", "confidence", "risk", "id")


def calculate_priority(item: dict[str, Any]) -> float:
    """Calculate the frozen score, rounded to four decimal places."""
    try:
        values = [item[key] for key in FACTORS]
        if any(isinstance(value, bool) or not isinstance(value, (int, float, Decimal)) for value in values):
            raise ValueError("factors must be numeric")
        numbers = [Decimal(str(value)) for value in values]
        if any(not value.is_finite() or not 1 <= value <= 5 for value in numbers):
            raise ValueError("factors must be from 1 through 5")
        impact, urgency, effort, confidence, risk = numbers
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        raise BacklogValidationError("item must include numeric impact, urgency, effort, confidence, and risk") from exc
    score = (2 * impact + Decimal("1.5") * urgency + confidence + Decimal("0.5") * risk) / max(effort, Decimal(1))
    return float(round(score, 4))


def validate_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate records and return fresh dictionaries."""
    if isinstance(items, (str, bytes, dict)):
        raise BacklogValidationError("backlog must be an iterable of item objects")
    try:
        source = list(items)
    except TypeError as exc:
        raise BacklogValidationError("backlog must be an iterable of item objects") from exc

    required = ("id", "title", *FACTORS, "status", "description")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(source):
        label = f"item {index + 1}"
        if not isinstance(item, dict):
            raise BacklogValidationError(f"{label} must be an object")
        missing = [key for key in required if key not in item]
        if missing:
            raise BacklogValidationError(f"{label} is missing required field(s): {', '.join(missing)}")
        item_id = item["id"]
        if not isinstance(item_id, str) or not item_id.strip():
            raise BacklogValidationError(f"{label} id must be a non-empty string")
        if item_id in seen:
            raise BacklogValidationError(f"duplicate item id: {item_id}")
        seen.add(item_id)
        if not isinstance(item["title"], str) or not item["title"].strip():
            raise BacklogValidationError(f"{label} title must be a non-empty string")
        if not isinstance(item["description"], str):
            raise BacklogValidationError(f"{label} description must be a string")
        if item["status"] not in STATUSES:
            raise BacklogValidationError(f"{label} status must be one of: {', '.join(STATUSES)}")
        clean = dict(item)
        for key in FACTORS:
            value = item[key]
            if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
                raise BacklogValidationError(f"{label} {key} must be a number from 1 through 5")
            try:
                numeric = float(value)
            except (ValueError, OverflowError) as exc:
                raise BacklogValidationError(f"{label} {key} must be a number from 1 through 5") from exc
            if not math.isfinite(numeric) or not 1 <= numeric <= 5:
                raise BacklogValidationError(f"{label} {key} must be a number from 1 through 5")
        result.append(clean)
    return result


def rank_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked = [{**item, "priority": calculate_priority(item)} for item in validate_items(items)]
    return sorted(ranked, key=lambda item: (-item["priority"], -float(item["urgency"]), -float(item["impact"]), item["id"]))


def filter_items(
    items: Iterable[dict[str, Any]], query: str = "", status: str = "all", risk: str = "all"
) -> list[dict[str, Any]]:
    records = validate_items(items)
    if status != "all" and status not in STATUSES:
        raise BacklogValidationError(f"unsupported status filter: {status}")
    if risk != "all" and (risk not in {"1", "2", "3", "4", "5"}):
        raise BacklogValidationError(f"unsupported risk filter: {risk}")
    needle = str(query).strip().casefold()
    return [item for item in records if
            (not needle or needle in item["title"].casefold() or needle in item["description"].casefold()) and
            (status == "all" or item["status"] == status) and
            (risk == "all" or float(item["risk"]) == int(risk))]


def sort_items(
    items: Iterable[dict[str, Any]], key: str = "priority", direction: str = "desc"
) -> list[dict[str, Any]]:
    if key not in SORT_KEYS:
        raise BacklogValidationError(f"unsupported sort key: {key}")
    if direction not in ("asc", "desc"):
        raise BacklogValidationError(f"unsupported sort direction: {direction}")
    records = validate_items(items)
    for item in records:
        item["priority"] = calculate_priority(item)
    field = (lambda item: item["priority"]) if key == "priority" else (lambda item: item[key])
    # Sort primary values first, then apply stable ascending id tie-breaking.
    records.sort(key=lambda item: item["id"])
    if key == "priority":
        records.sort(key=lambda item: (-item["priority"], -float(item["urgency"]), -float(item["impact"])) if direction == "desc"
                     else (item["priority"], float(item["urgency"]), float(item["impact"])))
    else:
        records.sort(key=field, reverse=direction == "desc")
    return records


def export_ordering(items: Iterable[dict[str, Any]], destination: str | Path) -> Path:
    ordering = validate_items(items)
    for item in ordering:
        for key in FACTORS:
            if isinstance(item[key], Decimal):
                item[key] = float(item[key])
    path = Path(destination)
    path.write_text(json.dumps(ordering, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def load_backlog(path: str | Path) -> list[dict[str, Any]]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BacklogValidationError(f"backlog is not valid JSON: {exc.msg}") from exc
    if not isinstance(value, list):
        raise BacklogValidationError("backlog root must be a JSON array")
    return validate_items(value)
