
"""Customer record matching implementation."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from datetime import datetime
import re


@dataclass
class FieldComparison:
    """How to compare one field."""

    attribute: str
    method: str
    weight: float


@dataclass
class MatchResult:
    confidence: float
    algorithm: str
    field_scores: dict[str, float]


PLAN = [
    FieldComparison("name", "phonetic", 0.25),
    FieldComparison("email", "edit_distance", 0.20),
    FieldComparison("phone", "normalized_phone", 0.20),
    FieldComparison("date_of_birth", "date", 0.20),
    FieldComparison("pin_code", "exact", 0.10),
    FieldComparison("city", "exact", 0.05),
]


def similarity(a: str, b: str) -> float:
    """Compare two strings and return a similarity score between 0 and 1."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def edit_distance(a: str, b: str) -> int:
    """Calculate the minimum number of edits needed to transform one string into another."""
    a = a.lower()
    b = b.lower()

    previous = list(range(len(b) + 1))

    for i, char_a in enumerate(a, start=1):
        current = [i]

        for j, char_b in enumerate(b, start=1):
            cost = 0 if char_a == char_b else 1

            current.append(
                min(
                    previous[j] + 1,
                    current[j - 1] + 1,
                    previous[j - 1] + cost,
                )
            )

        previous = current

    return previous[-1]


def compare_names(a: str, b: str) -> float:
    """Compare names, including reordered words and initials."""
    a = re.sub(r"[^a-z ]", "", a.lower()).split()
    b = re.sub(r"[^a-z ]", "", b.lower()).split()

    if not a or not b:
        return 0.0

    scores = []

    for word_a in a:
        best = 0.0

        for word_b in b:
            # Allow initials to match the beginning of a full name.
            if word_a[0] == word_b[0] and (
                len(word_a) == 1 or len(word_b) == 1
            ):
                score = 0.9
            else:
                score = similarity(word_a, word_b)

            best = max(best, score)

        scores.append(best)

    # Sorting the words makes name order less important.
    ordered_a = " ".join(sorted(a))
    ordered_b = " ".join(sorted(b))
    order_score = similarity(ordered_a, ordered_b)

    word_score = sum(scores) / max(len(a), len(b))

    return max(word_score, order_score)


def normalize_phone(phone: str) -> str:
    """Remove non-digits, Indian country code 91, and leading zero."""
    phone = re.sub(r"\D", "", phone)

    if phone.startswith("91") and len(phone) > 10:
        phone = phone[2:]

    if phone.startswith("0"):
        phone = phone[1:]

    return phone


def parse_date(value: str):
    """Parse supported date formats into a date object."""
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%d-%b-%Y",
        "%d-%b-%y",
        "%d %b %Y",
        "%m/%d/%Y",
        "%d.%m.%y",
        "%d/%m/%y",
        "%d-%m-%y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    return None


def score_pair(
    a: dict[str, object],
    b: dict[str, object],
    plan: list[FieldComparison],
) -> MatchResult:
    """Return a weighted confidence score for whether two records match."""
    field_scores: dict[str, float] = {}
    total_score = 0.0
    total_weight = 0.0
    methods = []

    for item in plan:
        raw_a = a.get(item.attribute)
        raw_b = b.get(item.attribute)

        # Missing values provide no evidence and are skipped.
        if raw_a is None or raw_b is None:
            continue

        value_a = str(raw_a).strip()
        value_b = str(raw_b).strip()

        if not value_a or not value_b:
            continue

        method = item.method

        if method == "phonetic":
            score = compare_names(value_a, value_b)

        elif method == "edit_distance":
            distance = edit_distance(value_a, value_b)
            longest = max(len(value_a), len(value_b))

            score = 1.0 if longest == 0 else 1.0 - distance / longest

        elif method == "normalized_phone":
            score = float(
                normalize_phone(value_a) == normalize_phone(value_b)
            )

        elif method == "date":
            date_a = parse_date(value_a)
            date_b = parse_date(value_b)
            score = float(date_a is not None and date_a == date_b)

        elif method == "exact":
            score = float(value_a.lower() == value_b.lower())

        else:
            continue

        field_scores[item.attribute] = score
        total_score += score * item.weight
        total_weight += item.weight

        if method not in methods:
            methods.append(method)

    # Divide by the weights of fields that were actually compared.
    confidence = total_score / total_weight if total_weight > 0 else 0.0

    return MatchResult(
        confidence=confidence,
        algorithm="+".join(methods),
        field_scores=field_scores,
    )
