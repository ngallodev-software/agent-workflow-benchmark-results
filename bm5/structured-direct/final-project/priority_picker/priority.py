from __future__ import annotations

import json
import math
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable


class BacklogValidationError(ValueError):
    """Raised when the supplied backlog does not match the frozen contract."""


_FACTORS = ("impact", "urgency", "effort", "confidence", "risk")
_STATUSES = {"planned", "ready", "in_progress", "blocked"}
_SORT_KEYS = {"priority", "score", "id", "title", "impact", "urgency", "effort", "confidence", "risk", "status"}


def _number(value: Any, field: str, item_id: str) -> int | float | Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise BacklogValidationError(f"item {item_id!r}: {field} must be a number from 1 through 5")
    try:
        valid = math.isfinite(value) and 1 <= value <= 5
    except (TypeError, OverflowError):
        valid = False
    if not valid:
        raise BacklogValidationError(f"item {item_id!r}: {field} must be a finite number from 1 through 5")
    return value


def validate_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate an iterable and return deep copies without changing its contents."""
    if isinstance(items, (str, bytes, dict)):
        raise BacklogValidationError("backlog must be an iterable of item objects")
    try:
        values = list(items)
    except TypeError as exc:
        raise BacklogValidationError("backlog must be an iterable of item objects") from exc
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    required = {"id", "title", *_FACTORS, "status", "description"}
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            raise BacklogValidationError(f"item at index {index} must be an object")
        item = deepcopy(value)
        item_id = item.get("id")
        label = item_id if isinstance(item_id, str) else f"index {index}"
        missing = required.difference(item)
        if missing:
            raise BacklogValidationError(f"item {label!r}: missing required field(s): {', '.join(sorted(missing))}")
        if not isinstance(item_id, str) or not item_id.strip():
            raise BacklogValidationError(f"item at index {index}: id must be a non-empty string")
        if item_id in seen:
            raise BacklogValidationError(f"duplicate item id {item_id!r}")
        seen.add(item_id)
        if not isinstance(item["title"], str) or not item["title"].strip():
            raise BacklogValidationError(f"item {item_id!r}: title must be a non-empty string")
        for factor in _FACTORS:
            item[factor] = _number(item[factor], factor, item_id)
        if not isinstance(item["status"], str) or item["status"] not in _STATUSES:
            raise BacklogValidationError(f"item {item_id!r}: status must be one of {', '.join(sorted(_STATUSES))}")
        if not isinstance(item["description"], str):
            raise BacklogValidationError(f"item {item_id!r}: description must be a string")
        result.append(item)
    return result


def calculate_priority(item: dict[str, Any]) -> float:
    """Calculate the frozen score, rounded to four decimal places."""
    checked = validate_items([item])[0]
    impact, urgency, effort, confidence, risk = (float(checked[field]) for field in _FACTORS)
    score = (2 * impact + 1.5 * urgency + confidence + 0.5 * risk) / max(effort, 1)
    return round(score, 4)


def rank_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked = [{**item, "priority": calculate_priority(item)} for item in validate_items(items)]
    return sorted(ranked, key=lambda item: (-item["priority"], -item["urgency"], -item["impact"], item["id"]))


def filter_items(
    items: Iterable[dict[str, Any]], query: str = "", status: str = "all", risk: str = "all"
) -> list[dict[str, Any]]:
    values = validate_items(items)
    needle = query.casefold().strip() if isinstance(query, str) else ""
    return [item for item in values
            if (not needle or needle in " ".join((item["id"], item["title"], item["description"])).casefold())
            and (status == "all" or item["status"] == status)
            and (risk == "all" or str(item["risk"]) == str(risk))]


def sort_items(
    items: Iterable[dict[str, Any]], key: str = "priority", direction: str = "desc"
) -> list[dict[str, Any]]:
    if not isinstance(key, str) or key not in _SORT_KEYS:
        raise BacklogValidationError(f"unsupported sort key {key!r}; expected one of {', '.join(sorted(_SORT_KEYS))}")
    if not isinstance(direction, str) or direction not in {"asc", "desc"}:
        raise BacklogValidationError("unsupported sort direction; expected 'asc' or 'desc'")
    values = validate_items(items)
    decorated = [{**item, "priority": calculate_priority(item)} for item in values]
    reverse = direction == "desc"
    if key == "priority" or key == "score":
        # Keep the frozen tie-breakers deterministic in either direction.
        primary = "priority"
        return sorted(decorated, key=lambda item: ((-item[primary] if reverse else item[primary]),
                       (-item["urgency"] if reverse else item["urgency"]),
                       (-item["impact"] if reverse else item["impact"]), item["id"]))
    return sorted(decorated, key=lambda item: (item[key].casefold() if isinstance(item[key], str) else item[key]), reverse=reverse)


def export_ordering(items: Iterable[dict[str, Any]], destination: str | Path) -> Path:
    values = validate_items(items)
    output = [{**item, **{factor: float(item[factor]) for factor in _FACTORS},
               "priority": calculate_priority(item)} for item in values]
    path = Path(destination)
    path.write_text(json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    return path


def load_backlog(path: str | Path) -> list[dict[str, Any]]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BacklogValidationError(f"invalid JSON: {exc.msg}") from exc
    if not isinstance(value, list):
        raise BacklogValidationError("backlog root must be a JSON array")
    return validate_items(value)
