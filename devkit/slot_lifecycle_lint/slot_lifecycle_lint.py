#!/usr/bin/env python3
"""Declared ownership and lifecycle lint for M&B 1.011 durable slots.

Slots are effectively untyped shared memory in the module system.  This tool
does not pretend a slot name alone proves ownership.  Instead it combines the
Campaign State Doctor's source/branch model with a small checked-in ownership
catalog.  It can therefore distinguish an approved handoff from a new writer
that silently reuses another system's state.

The lint is intentionally source-only and conservative.  A missing clear is a
contract failure only when the owning subsystem explicitly declares that the
slot is lifecycle-bound; all undeclared sharing stays a review candidate.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
DEFAULT_OWNERSHIP_PATH = TOOL_DIR / "ownership.json"
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.campaign_state_doctor import campaign_state_doctor as doctor


LINT_VERSION = "1.0.0"


class SlotLifecycleError(RuntimeError):
    """The requested ownership/lifecycle query cannot be answered safely."""


@dataclass(frozen=True)
class OwnershipRule:
    id: str
    category: str
    slot_prefix: str | None
    slot_names: frozenset[str]
    owner_script_prefixes: tuple[str, ...]
    allowed_handoff_scripts: tuple[str, ...]
    require_clear: bool
    clear_values: frozenset[str]
    description: str


@dataclass
class SlotLifecycleIndex:
    root: Path
    ownership_path: Path
    state: doctor.StateDoctorIndex
    rules: tuple[OwnershipRule, ...]
    findings: list[dict[str, Any]]
    warnings: list[str]


_CACHE: dict[tuple[Path, Path, Path | None], tuple[tuple[tuple[str, int, int], ...], SlotLifecycleIndex]] = {}


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def require_limit(value: int, maximum: int = 200) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise SlotLifecycleError(f"limit must be an integer from 1 through {maximum}.")
    return value


def require_query(value: str | None, *, name: str = "query") -> str:
    if not isinstance(value, str) or not value.strip():
        raise SlotLifecycleError(f"{name} must not be empty.")
    if len(value) > 500:
        raise SlotLifecycleError(f"{name} must be at most 500 characters.")
    return value.strip()


def signature(paths: Iterable[Path], root: Path) -> tuple[tuple[str, int, int], ...]:
    rows: list[tuple[str, int, int]] = []
    for path in sorted(set(paths), key=lambda value: str(value).casefold()):
        try:
            stat = path.stat()
        except OSError:
            rows.append((project_relative(path, root), -1, -1))
        else:
            rows.append((project_relative(path, root), stat.st_mtime_ns, stat.st_size))
    return tuple(rows)


def load_rules(path: Path) -> tuple[OwnershipRule, ...]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SlotLifecycleError(f"Could not read slot ownership catalog at {path}: {error}") from error
    if not isinstance(payload, dict) or payload.get("schema") != "devkit.slot-lifecycle-ownership.v1":
        raise SlotLifecycleError("Slot ownership catalog must use schema devkit.slot-lifecycle-ownership.v1.")
    raw_rules = payload.get("ownership")
    if not isinstance(raw_rules, list):
        raise SlotLifecycleError("Slot ownership catalog must contain an ownership list.")
    rules: list[OwnershipRule] = []
    identifiers: set[str] = set()
    for raw in raw_rules:
        if not isinstance(raw, dict):
            raise SlotLifecycleError("Each ownership rule must be an object.")
        identifier = raw.get("id")
        category = raw.get("category")
        slot_prefix = raw.get("slot_prefix")
        slot_names = raw.get("slot_names", [])
        prefixes = raw.get("owner_script_prefixes", [])
        handoffs = raw.get("allowed_handoff_scripts", [])
        values = raw.get("clear_values", ["0"])
        if not isinstance(identifier, str) or not identifier or identifier in identifiers:
            raise SlotLifecycleError("Ownership rule IDs must be unique non-empty strings.")
        if category not in {"party_slot", "faction_slot", "troop_slot"}:
            raise SlotLifecycleError(f"Ownership rule {identifier!r} has unsupported slot category {category!r}.")
        has_prefix = isinstance(slot_prefix, str) and bool(slot_prefix)
        has_names = isinstance(slot_names, list) and bool(slot_names)
        if not has_prefix and not has_names:
            raise SlotLifecycleError(f"Ownership rule {identifier!r} needs a non-empty slot_prefix or slot_names list.")
        if has_prefix and has_names:
            raise SlotLifecycleError(f"Ownership rule {identifier!r} must use either slot_prefix or slot_names, not both.")
        if slot_prefix is not None and not has_prefix:
            raise SlotLifecycleError(f"Ownership rule {identifier!r} has an invalid slot_prefix.")
        if not isinstance(slot_names, list) or not all(isinstance(value, str) and value for value in slot_names):
            raise SlotLifecycleError(f"Ownership rule {identifier!r} has invalid slot_names.")
        if not isinstance(prefixes, list) or not prefixes or not all(isinstance(value, str) and value for value in prefixes):
            raise SlotLifecycleError(f"Ownership rule {identifier!r} needs owner_script_prefixes.")
        if not isinstance(handoffs, list) or not all(isinstance(value, str) and value for value in handoffs):
            raise SlotLifecycleError(f"Ownership rule {identifier!r} has invalid allowed_handoff_scripts.")
        if not isinstance(values, list) or not all(isinstance(value, (str, int)) and not isinstance(value, bool) for value in values):
            raise SlotLifecycleError(f"Ownership rule {identifier!r} has invalid clear_values.")
        identifiers.add(identifier)
        rules.append(
            OwnershipRule(
                id=identifier,
                category=category,
                slot_prefix=slot_prefix if has_prefix else None,
                slot_names=frozenset(slot_names),
                owner_script_prefixes=tuple(prefixes),
                allowed_handoff_scripts=tuple(handoffs),
                require_clear=bool(raw.get("require_clear", False)),
                clear_values=frozenset(str(value) for value in values),
                description=str(raw.get("description", "")),
            )
        )
    return tuple(rules)


def matches_rule(access: doctor.StateAccess, rule: OwnershipRule) -> bool:
    if access.category != rule.category or not access.slot:
        return False
    return access.slot in rule.slot_names or (rule.slot_prefix is not None and access.slot.startswith(rule.slot_prefix))


def operation_payload(operation: doctor.Operation) -> dict[str, Any]:
    return doctor.operation_payload(operation)


def access_payload(access: doctor.StateAccess) -> dict[str, Any]:
    return {
        "id": access.id,
        "action": access.action,
        "category": access.category,
        "resource": access.resource,
        "subject": access.subject,
        "slot": access.slot,
        "value": access.value,
        "operation": operation_payload(access.operation),
    }


def script_is_owner(symbol: str, rule: OwnershipRule) -> bool:
    return any(symbol.startswith(prefix) for prefix in rule.owner_script_prefixes)


def script_is_allowed_handoff(symbol: str, rule: OwnershipRule) -> bool:
    return symbol in rule.allowed_handoff_scripts


def clear_write(access: doctor.StateAccess, rule: OwnershipRule) -> bool:
    return access.action == "write" and access.value in rule.clear_values


def script_namespace(symbol: str) -> str:
    """Return a compact heuristic label for undeclared-sharing review only."""

    pieces = [piece for piece in symbol.removeprefix("script_").split("_") if piece]
    if pieces[:1] == ["sod"]:
        pieces = pieces[1:]
    if not pieces:
        return "<unknown>"
    return "_".join(pieces[:2])


def finding(
    *,
    finding_id: str,
    severity: str,
    category: str,
    summary: str,
    rule: OwnershipRule | None = None,
    accesses: Sequence[doctor.StateAccess] = (),
    recommendation: str,
) -> dict[str, Any]:
    return {
        "id": finding_id,
        "severity": severity,
        "category": category,
        "summary": summary,
        "ownership_rule": rule.id if rule else None,
        "source": doctor.source_payload(accesses[0].operation.source) if accesses else None,
        "evidence": [access_payload(access) for access in accesses[:12]],
        "recommendation": recommendation,
    }


def declared_rule_findings(state: doctor.StateDoctorIndex, rules: Sequence[OwnershipRule]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for rule in rules:
        accesses = [access for access in state.accesses if matches_rule(access, rule)]
        writes = [access for access in accesses if access.action == "write"]
        slots = sorted({access.slot for access in accesses if access.slot})
        foreign = [
            access
            for access in writes
            if not script_is_owner(access.operation.scope_id, rule)
            and not script_is_allowed_handoff(access.operation.scope_id, rule)
        ]
        for access in foreign:
            findings.append(
                finding(
                    finding_id=f"foreign-owner:{rule.id}:{access.id}",
                    severity="warning",
                    category="declared_slot_written_by_unrelated_system",
                    summary=(
                        f"{access.slot} is declared to {rule.id}, but {access.operation.scope_id} writes it outside "
                        "the owner prefixes and approved handoff list."
                    ),
                    rule=rule,
                    accesses=[access],
                    recommendation="Either route the write through the owning subsystem, add a deliberate handoff entry, or split the state into a separately named slot.",
                )
            )
        for slot in slots:
            slot_writes = [access for access in writes if access.slot == slot]
            sets = [access for access in slot_writes if not clear_write(access, rule)]
            clears = [access for access in slot_writes if clear_write(access, rule)]
            if rule.require_clear and sets and not clears:
                findings.append(
                    finding(
                        finding_id=f"missing-clear:{rule.id}:{slot}",
                        severity="error",
                        category="declared_lifecycle_slot_never_cleared",
                        summary=f"Lifecycle-bound {slot} is assigned but no declared clear value is modeled anywhere in its owner scope.",
                        rule=rule,
                        accesses=sets,
                        recommendation="Add an explicit reset/teardown write before party reuse or removal, then keep that lifecycle path in the ownership scope.",
                    )
                )
            # A direct clear followed by a read of the same exact selector in
            # the same path is a useful stale-state trap.  It remains a warning
            # because later calls can legitimately reinitialize the slot.
            for clear in clears:
                later_reads = [
                    access
                    for access in accesses
                    if access.action == "read"
                    and access.slot == slot
                    and access.subject == clear.subject
                    and access.operation.scope_id == clear.operation.scope_id
                    and access.operation.ordinal > clear.operation.ordinal
                    and not doctor.paths_are_exclusive(clear.operation, access.operation)
                ]
                if later_reads:
                    findings.append(
                        finding(
                            finding_id=f"read-after-clear:{rule.id}:{clear.id}",
                            severity="warning",
                            category="slot_read_after_clear_candidate",
                            summary=f"{slot} is read after an explicit clear in {clear.operation.scope_id} without a proven alternate branch.",
                            rule=rule,
                            accesses=[clear, *later_reads],
                            recommendation="Verify that a deliberate reinitialization occurs before the read; otherwise keep the old value until the final lifecycle cleanup.",
                        )
                    )
    return findings


def undeclared_sharing_findings(state: doctor.StateDoctorIndex, rules: Sequence[OwnershipRule]) -> list[dict[str, Any]]:
    """Surface unowned multi-system writes without silently inventing owners."""

    declared_slots = {
        access.slot
        for rule in rules
        for access in state.accesses
        if matches_rule(access, rule) and access.slot
    }
    findings: list[dict[str, Any]] = []
    for slot, accesses in sorted(
        ((slot, values) for slot, values in _accesses_by_slot(state).items() if slot not in declared_slots),
        key=lambda item: item[0],
    ):
        writers = [access for access in accesses if access.action == "write" and access.operation.scope_kind == "script"]
        namespaces = sorted({script_namespace(access.operation.scope_id) for access in writers})
        if len(namespaces) < 3:
            continue
        findings.append(
            finding(
                finding_id=f"unowned-sharing:{slot}",
                severity="info",
                category="undeclared_slot_multi_system_writer_candidate",
                summary=f"{slot} has writers from {len(namespaces)} script namespaces but no checked-in ownership declaration.",
                accesses=writers,
                recommendation="If this slot is lifecycle-sensitive, declare its owner and approved handoffs; otherwise leave it undeclared and treat this as shared infrastructure.",
            )
        )
    return findings


def _accesses_by_slot(state: doctor.StateDoctorIndex) -> dict[str, list[doctor.StateAccess]]:
    result: dict[str, list[doctor.StateAccess]] = defaultdict(list)
    for access in state.accesses:
        if access.category in {"party_slot", "faction_slot", "troop_slot"} and access.slot:
            result[access.slot].append(access)
    return dict(result)


def build_slot_lifecycle_lint(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    ownership_path: Path | None = None,
    state_contracts_path: Path | None = None,
) -> SlotLifecycleIndex:
    root = root.resolve()
    checked_ownership = (ownership_path or (root / "devkit" / "slot_lifecycle_lint" / "ownership.json")).resolve()
    if not checked_ownership.is_file() and ownership_path is None:
        checked_ownership = DEFAULT_OWNERSHIP_PATH
    if not checked_ownership.is_file():
        raise SlotLifecycleError(f"Missing slot ownership catalog: {checked_ownership}")
    input_paths = [checked_ownership, *root.joinpath("src", "scripts").rglob("*.py"), *root.joinpath("src", "triggers").rglob("*.py")]
    if state_contracts_path is not None:
        input_paths.append(state_contracts_path)
    key = (root, checked_ownership, state_contracts_path.resolve() if state_contracts_path else None)
    current = signature(input_paths, root)
    cached = _CACHE.get(key)
    if cached is not None and cached[0] == current:
        return cached[1]
    try:
        state = doctor.build_state_doctor(root, contracts_path=state_contracts_path)
    except doctor.CampaignStateError as error:
        raise SlotLifecycleError(str(error)) from error
    rules = load_rules(checked_ownership)
    findings = [*declared_rule_findings(state, rules), *undeclared_sharing_findings(state, rules)]
    severity_rank = {"error": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda item: (severity_rank.get(str(item["severity"]), 3), str(item["category"]), str(item["id"])))
    warnings = [
        "Slot ownership is opt-in. Undeclared slots are never assigned a fictional owner from naming alone.",
        "A missing clear is an error only for a rule marked require_clear; retained slots may be intentional durable state.",
        *state.warnings,
    ]
    index = SlotLifecycleIndex(root, checked_ownership, state, rules, findings, list(dict.fromkeys(warnings)))
    _CACHE[key] = (current, index)
    return index


def findings_payload(
    index: SlotLifecycleIndex,
    *,
    severity: str = "all",
    query: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    maximum = require_limit(limit)
    if severity not in {"all", "error", "warning", "info"}:
        raise SlotLifecycleError("severity must be one of: all, error, warning, info.")
    needle = require_query(query).casefold() if query is not None else None
    selected = [
        item
        for item in index.findings
        if (severity == "all" or item["severity"] == severity)
        and (needle is None or needle in json.dumps(item, sort_keys=True).casefold())
    ]
    return {
        "severity": severity,
        "query": query,
        "finding_count": len(selected),
        "returned_count": min(len(selected), maximum),
        "truncated": len(selected) > maximum,
        "findings": selected[:maximum],
        "warnings": index.warnings,
    }


def ownership_payload(index: SlotLifecycleIndex, *, slot: str | None = None, limit: int = 40) -> dict[str, Any]:
    maximum = require_limit(limit)
    needle = require_query(slot, name="slot").casefold() if slot is not None else None
    rows: list[dict[str, Any]] = []
    for rule in index.rules:
        accesses = [access for access in index.state.accesses if matches_rule(access, rule)]
        slots = sorted({access.slot for access in accesses if access.slot})
        rule_selectors = [*rule.slot_names]
        if rule.slot_prefix is not None:
            rule_selectors.append(rule.slot_prefix)
        if needle is not None and not any(needle in value.casefold() for value in [*rule_selectors, *slots]):
            continue
        rows.append(
            {
                "id": rule.id,
                "category": rule.category,
                "slot_prefix": rule.slot_prefix,
                "slot_names": sorted(rule.slot_names),
                "owner_script_prefixes": list(rule.owner_script_prefixes),
                "allowed_handoff_scripts": list(rule.allowed_handoff_scripts),
                "require_clear": rule.require_clear,
                "clear_values": sorted(rule.clear_values),
                "description": rule.description,
                "matched_slot_count": len(slots),
                "matched_slots": slots[:maximum],
                "matched_slots_truncated": len(slots) > maximum,
            }
        )
    return {
        "slot": slot,
        "rule_count": len(rows),
        "returned_count": min(len(rows), maximum),
        "truncated": len(rows) > maximum,
        "ownership": rows[:maximum],
        "warnings": index.warnings,
    }


def slot_payload(index: SlotLifecycleIndex, slot: str, *, limit: int = 50) -> dict[str, Any]:
    maximum = require_limit(limit)
    checked = require_query(slot, name="slot")
    matches = [
        (name, accesses)
        for name, accesses in _accesses_by_slot(index.state).items()
        if checked.casefold() in name.casefold()
    ]
    rows = []
    for name, accesses in sorted(matches, key=lambda item: item[0])[:maximum]:
        rules = [rule.id for rule in index.rules if any(matches_rule(access, rule) for access in accesses)]
        writers = [access for access in accesses if access.action == "write"]
        rows.append(
            {
                "slot": name,
                "ownership_rules": rules,
                "access_count": len(accesses),
                "writer_count": len(writers),
                "reader_count": len(accesses) - len(writers),
                "writer_namespaces": sorted({script_namespace(access.operation.scope_id) for access in writers if access.operation.scope_kind == "script"}),
                "sample_accesses": [access_payload(access) for access in accesses[:maximum]],
            }
        )
    return {
        "slot_query": checked,
        "slot_count": len(matches),
        "returned_count": len(rows),
        "truncated": len(matches) > maximum,
        "slots": rows,
        "warnings": index.warnings,
    }


def summary_payload(index: SlotLifecycleIndex, *, limit: int = 20) -> dict[str, Any]:
    maximum = require_limit(limit)
    severity_counts = Counter(str(item["severity"]) for item in index.findings)
    slots = _accesses_by_slot(index.state)
    declared = {
        slot
        for rule in index.rules
        for slot, accesses in slots.items()
        if any(matches_rule(access, rule) for access in accesses)
    }
    return {
        "slot_lifecycle_lint_version": f"devkit.slot-lifecycle-lint.v{LINT_VERSION}",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": {
            "repo_root": str(index.root),
            "read_only": True,
            "ownership_path": project_relative(index.ownership_path, index.root),
            "authoritative_layer": "src/scripts and src/triggers",
        },
        "coverage": {
            "ownership_rule_count": len(index.rules),
            "observed_slot_count": len(slots),
            "declared_slot_count": len(declared),
            "state_access_count": len(index.state.accesses),
        },
        "findings": {
            "total": len(index.findings),
            "by_severity": dict(sorted(severity_counts.items())),
            "returned_count": min(len(index.findings), maximum),
            "truncated": len(index.findings) > maximum,
            "items": index.findings[:maximum],
        },
        "next_steps": [
            "Use slot_lifecycle_ownership to inspect declared owners and approved handoffs before changing a slot.",
            "Use slot_lifecycle_slot for all reader/writer evidence on one exact slot.",
            "Add an ownership rule only for real subsystem boundaries; shared infrastructure may remain intentionally undeclared.",
        ],
        "warnings": index.warnings,
    }


def render_markdown(payload: Mapping[str, Any], command: str) -> str:
    if command == "summary":
        coverage = payload["coverage"]
        findings = payload["findings"]
        lines = [
            "# Slot Ownership + Lifecycle Lint",
            "",
            f"- Rules: {coverage['ownership_rule_count']}; observed slots: {coverage['observed_slot_count']:,}; declared slots: {coverage['declared_slot_count']:,}.",
            f"- Findings: {findings['total']} ({', '.join(f'{key}={value}' for key, value in findings['by_severity'].items()) or 'none'}).",
        ]
    else:
        lines = [f"# Slot Lifecycle Lint: {command}", "", "Use JSON output for complete branch/source evidence."]
    if payload.get("warnings"):
        lines.extend(["", "## Boundaries", "", *(f"- {warning}" for warning in payload["warnings"])])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only declared slot ownership and lifecycle lint for SoD Modern.")
    parser.add_argument("command", choices=("summary", "findings", "ownership", "slot"), nargs="?", default="summary")
    parser.add_argument("query", nargs="?", help="Optional text filter for findings/ownership; required slot query for slot.")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--ownership", type=Path)
    parser.add_argument("--state-contracts", type=Path)
    parser.add_argument("--severity", choices=("all", "error", "warning", "info"), default="all")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        index = build_slot_lifecycle_lint(
            root,
            ownership_path=args.ownership.resolve() if args.ownership else None,
            state_contracts_path=args.state_contracts.resolve() if args.state_contracts else None,
        )
        if args.command == "summary":
            payload = summary_payload(index, limit=args.limit)
        elif args.command == "findings":
            payload = findings_payload(index, severity=args.severity, query=args.query, limit=args.limit)
        elif args.command == "ownership":
            payload = ownership_payload(index, slot=args.query, limit=args.limit)
        else:
            payload = slot_payload(index, require_query(args.query, name="slot"), limit=args.limit)
        if args.format == "markdown":
            sys.stdout.write(render_markdown(payload, args.command))
        else:
            sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    except SlotLifecycleError as error:
        print(f"slot_lifecycle_lint: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
