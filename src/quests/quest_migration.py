# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

__all__ = [
    "QuestMigrationCandidate",
    "QuestMigrationPlan",
    "build_quest_migration_plan",
]

_LEGACY_FAMILY_HINTS = {
    "prison": "small_chain",
    "mercenary": "repeated_family",
    "lord": "repeated_family",
    "enemy_lord": "repeated_family",
    "army": "repeated_family",
    "lady": "special_case",
    "mayor": "repeated_family",
    "village_elder": "repeated_family",
    "story": "special_case",
    "meta": "special_case",
}


def _score_fragment(path: Path, raw: str) -> int:
    score = 0
    lower = raw.lower()
    if "quest_chain_from_specs" in lower:
        score -= 20
    if "quest_template_spec" in lower:
        score -= 10
    if "quest_stage_spec" in lower:
        score -= 8
    if "metadata={" in lower:
        score -= 4
    if "legacy_fragment" in lower:
        score -= 4
    if path.name.startswith("0001_"):
        score -= 8
    if path.name.startswith("0002_"):
        score -= 6
    if path.name.startswith("0009_"):
        score += 6
    if "special_case" in lower:
        score += 6
    if "repeat" in lower:
        score += 4
    score += min(len(raw) // 800, 12)
    return score


def _classify_fragment(path: Path, raw: str) -> str:
    lower = raw.lower()
    if "quest_chain_from_specs" in lower:
        return "chain_spec"
    if "quest_template_spec" in lower and "quest_stage_spec" in lower:
        return "structured_template"
    if "quest_template_spec" in lower:
        return "template_bundle"
    if "qf_random_quest" in lower:
        return "legacy_tuple_bundle"
    return "legacy_tuple"


def _family_label(path: Path) -> str:
    stem = path.stem.lower()
    for hint, label in _LEGACY_FAMILY_HINTS.items():
        if hint in stem:
            return label
    if stem.startswith("0001_"):
        return "small_chain"
    if stem.startswith("0009_"):
        return "special_case"
    return "general"


@dataclass(frozen=True)
class QuestMigrationCandidate:
    path: str
    family: str
    fragment_type: str
    score: int
    reason: str
    size_bytes: int


@dataclass
class QuestMigrationPlan:
    candidates: list[QuestMigrationCandidate] = field(default_factory=list)

    def ordered(self) -> list[QuestMigrationCandidate]:
        return sorted(self.candidates, key=lambda item: (item.score, item.size_bytes, item.path))

    def summary_lines(self) -> list[str]:
        lines = [
            "Quest Migration Plan",
            "=====================",
            "",
            "Purpose: incremental quest library migration that keeps legacy tuples compiling while converting the smallest, safest fragments first.",
            "",
            "Migration Order Principles",
            "--------------------------",
            "1. Keep legacy tuples compiling.",
            "2. Convert the smallest chain fragments first.",
            "3. Define shared helper patterns.",
            "4. Migrate repeated quest families.",
            "5. Migrate special cases later.",
            "6. Normalize metadata and shared tags.",
            "7. Remove one-off duplication.",
            "8. Consolidate common patterns into DSL helpers.",
            "",
            "Recommended Conversion Order",
            "----------------------------",
        ]
        for idx, candidate in enumerate(self.ordered(), start=1):
            lines.append(
                f"{idx}. {candidate.path} | {candidate.family} | {candidate.fragment_type} | score {candidate.score} | {candidate.reason}"
            )
        return lines


def build_quest_migration_plan(quest_files: Iterable[Path]) -> QuestMigrationPlan:
    candidates: list[QuestMigrationCandidate] = []
    for path in quest_files:
        try:
            raw = path.read_text(encoding="utf-8")
        except Exception:
            continue
        family = _family_label(path)
        fragment_type = _classify_fragment(path, raw)
        score = _score_fragment(path, raw)
        if fragment_type == "chain_spec":
            reason = "already structured; easiest to normalize metadata and reuse shared DSL helpers"
        elif fragment_type == "structured_template":
            reason = "structured template bundle; low-risk to migrate into shared helper patterns"
        elif fragment_type == "template_bundle":
            reason = "template-based quest set; good candidate for repeated family consolidation"
        elif family == "small_chain":
            reason = "small chain fragment; good first conversion target"
        elif family == "repeated_family":
            reason = "repeated family; convert after helper patterns are established"
        elif family == "special_case":
            reason = "special-case quest content; migrate after the common families are stable"
        else:
            reason = "legacy tuple bundle; keep compiling until helper patterns are in place"
        candidates.append(
            QuestMigrationCandidate(
                path=path.name,
                family=family,
                fragment_type=fragment_type,
                score=score,
                reason=reason,
                size_bytes=len(raw.encode("utf-8")),
            )
        )
    return QuestMigrationPlan(candidates)
