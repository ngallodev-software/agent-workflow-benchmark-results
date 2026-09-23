from __future__ import annotations

import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
from numbers import Real
from pathlib import Path
from typing import Any, Iterable


class BacklogValidationError(ValueError):
    """Raised when the supplied backlog does not match the frozen contract."""


_FACTORS = ("impact", "urgency", "effort", "confidence", "risk")
_STATUSES = {"planned", "ready", "in_progress", "blocked"}
_SORT_KEYS = {"priority", "score", "id", "title", "status", *_FACTORS}


def calculate_priority(item: dict[str, Any]) -> float:
    """Return the frozen score rounded to four decimal places."""
    try:
        score = (2 * Decimal(str(item["impact"])) +
                 Decimal("1.5") * Decimal(str(item["urgency"])) +
                 Decimal(str(item["confidence"])) +
                 Decimal("0.5") * Decimal(str(item["risk"]))) / max(Decimal(str(item["effort"])), Decimal(1))
        return float(score.quantize(Decimal("0.0001"), rounding=ROUND_HALF_EVEN))
    except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
        raise BacklogValidationError(f"cannot calculate priority: {exc}") from exc


def validate_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate a backlog and return shallow copies without changing its input."""
    if isinstance(items, (str, bytes, dict)):
        raise BacklogValidationError("backlog must be an iterable of item objects")
    try:
        source = list(items)
    except TypeError as exc:
        raise BacklogValidationError("backlog must be an iterable of item objects") from exc
    required = {"id", "title", *_FACTORS, "status", "description"}
    seen: set[str] = set()
    result = []
    for index, item in enumerate(source):
        label = f"item {index}"
        if not isinstance(item, dict):
            raise BacklogValidationError(f"{label} must be an object")
        missing = required - item.keys()
        if missing:
            raise BacklogValidationError(f"{label} missing required field(s): {', '.join(sorted(missing))}")
        if not isinstance(item["id"], str) or not item["id"].strip():
            raise BacklogValidationError(f"{label} id must be a non-empty string")
        if item["id"] in seen:
            raise BacklogValidationError(f"duplicate id {item['id']!r}")
        seen.add(item["id"])
        if not isinstance(item["title"], str) or not item["title"].strip():
            raise BacklogValidationError(f"{label} title must be a non-empty string")
        if not isinstance(item["description"], str):
            raise BacklogValidationError(f"{label} description must be a string")
        if not isinstance(item["status"], str) or item["status"] not in _STATUSES:
            raise BacklogValidationError(f"{label} status must be one of {', '.join(sorted(_STATUSES))}")
        for name in _FACTORS:
            value = item[name]
            if isinstance(value, bool) or not isinstance(value, (Real, Decimal)):
                raise BacklogValidationError(f"{label} {name} must be a number from 1 through 5")
            try:
                number = Decimal(str(value))
            except (InvalidOperation, TypeError, ValueError) as exc:
                raise BacklogValidationError(f"{label} {name} must be a number from 1 through 5") from exc
            if not number.is_finite() or not Decimal(1) <= number <= Decimal(5):
                raise BacklogValidationError(f"{label} {name} must be a number from 1 through 5")
        result.append(item.copy())
    return result


def rank_items(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    values = validate_items(items)
    return sorted(values, key=lambda item: (
        -calculate_priority(item), -Decimal(str(item["urgency"])),
        -Decimal(str(item["impact"])), item["id"],
    ))


def filter_items(
    items: Iterable[dict[str, Any]], query: str = "", status: str = "all", risk: str = "all"
) -> list[dict[str, Any]]:
    values = validate_items(items)
    needle = query.casefold().strip()
    return [item for item in values
            if (not needle or needle in item["title"].casefold() or needle in item["description"].casefold() or needle in item["id"].casefold())
            and (status == "all" or item["status"] == status)
            and (risk == "all" or str(item["risk"]) == str(risk))]


def sort_items(
    items: Iterable[dict[str, Any]], key: str = "priority", direction: str = "desc"
) -> list[dict[str, Any]]:
    if not isinstance(key, str) or key not in _SORT_KEYS:
        raise BacklogValidationError(f"unsupported sort key: {key!r}")
    if not isinstance(direction, str) or direction not in {"asc", "desc"}:
        raise BacklogValidationError(f"unsupported sort direction: {direction!r}")
    values = validate_items(items)
    field = "priority" if key in {"priority", "score"} else key
    return sorted(values, key=lambda item: calculate_priority(item) if field == "priority" else item[field], reverse=direction == "desc")


def export_ordering(items: Iterable[dict[str, Any]], destination: str | Path) -> Path:
    path = Path(destination)
    values = validate_items(items)
    path.write_text(json.dumps(values, indent=2, ensure_ascii=False, default=float) + "\n", encoding="utf-8")
    return path


def load_backlog(path: str | Path) -> list[dict[str, Any]]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BacklogValidationError(f"invalid backlog JSON: {exc}") from exc
    if not isinstance(value, list):
        raise BacklogValidationError("backlog root must be a JSON array")
    return validate_items(value)
