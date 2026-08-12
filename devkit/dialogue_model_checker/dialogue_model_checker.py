#!/usr/bin/env python3
"""Static model checker for ordered M&B 1.011 dialogue routes.

The compiler validates dialogue tuple shape but cannot answer whether a route
can ever be selected.  This checker reads the generated dialogue list in exact
engine order and models a deliberately small, branch-free conjunction of
common M&B predicate operations.  A condition block with try/else flow or a
state-changing operation is an explicit model boundary: it is never flattened
into a conjunction and therefore never turned into a false proof.

NPC dialogue is first-match within a speaker/start-state group; player lines
are choices and therefore have different ambiguity semantics.  The result is
not a fake playthrough: no save data, script condition body, or engine talker
selection is executed.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.dialogue_inspector import dialogue_inspector as dialogue


MODEL_VERSION = "1.0.0"
INTEGER_RE = re.compile(r"^-?\d+$")
REGISTER_RE = re.compile(r"^(?:s\d+|reg\d+)$")
SLOT_OPERATORS = frozenset(
    {
        "party_slot_eq", "party_slot_neq", "party_slot_ge", "party_slot_gt", "party_slot_le", "party_slot_lt",
        "faction_slot_eq", "faction_slot_neq", "faction_slot_ge", "faction_slot_gt", "faction_slot_le", "faction_slot_lt",
        "troop_slot_eq", "troop_slot_neq", "troop_slot_ge", "troop_slot_gt", "troop_slot_le", "troop_slot_lt",
        "quest_slot_eq", "quest_slot_neq", "quest_slot_ge", "quest_slot_gt", "quest_slot_le", "quest_slot_lt",
    }
)
COMPARATORS = frozenset({"eq", "neq", "ge", "gt", "le", "lt"})
CONTROL_OPERATIONS = frozenset({"try_begin", "else_try", "try_end", "end_try"})
SAFE_BOOLEAN_PREFIXES = (
    "is_",
    "check_",
    "main_party_",
    "party_is_",
    "faction_is_",
    "troop_is_",
    "quest_is_",
    "agent_is_",
    "mission_",
)


class DialogueModelError(RuntimeError):
    """The requested dialogue-model query cannot be completed safely."""


@dataclass(frozen=True)
class Bound:
    value: int
    inclusive: bool


@dataclass
class ConstraintSet:
    equal: dict[str, str] = field(default_factory=dict)
    not_equal: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    lower: dict[str, Bound] = field(default_factory=dict)
    upper: dict[str, Bound] = field(default_factory=dict)
    opaque_positive: set[str] = field(default_factory=set)
    opaque_negative: set[str] = field(default_factory=set)
    unsupported: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)

    def add_eq(self, key: str, value: str) -> None:
        current = self.equal.get(key)
        if current is not None and current != value:
            self.contradictions.append(f"{key} is both {current} and {value}")
            return
        self.equal[key] = value
        if value in self.not_equal.get(key, set()):
            self.contradictions.append(f"{key} is both equal and not equal to {value}")
        integer = integer_value(value)
        if integer is not None:
            self._check_integer(key, integer)

    def add_neq(self, key: str, value: str) -> None:
        self.not_equal[key].add(value)
        if self.equal.get(key) == value:
            self.contradictions.append(f"{key} is both equal and not equal to {value}")

    def add_lower(self, key: str, value: int, inclusive: bool) -> None:
        prior = self.lower.get(key)
        candidate = Bound(value, inclusive)
        if prior is None or (candidate.value > prior.value) or (candidate.value == prior.value and not candidate.inclusive and prior.inclusive):
            self.lower[key] = candidate
        assigned = integer_value(self.equal.get(key))
        if assigned is not None:
            self._check_integer(key, assigned)
        self._check_bounds(key)

    def add_upper(self, key: str, value: int, inclusive: bool) -> None:
        prior = self.upper.get(key)
        candidate = Bound(value, inclusive)
        if prior is None or (candidate.value < prior.value) or (candidate.value == prior.value and not candidate.inclusive and prior.inclusive):
            self.upper[key] = candidate
        assigned = integer_value(self.equal.get(key))
        if assigned is not None:
            self._check_integer(key, assigned)
        self._check_bounds(key)

    def add_opaque(self, atom: str, *, negated: bool = False) -> None:
        target = self.opaque_negative if negated else self.opaque_positive
        target.add(atom)
        if atom in (self.opaque_positive if negated else self.opaque_negative):
            self.contradictions.append(f"{atom} is both required and negated")

    def _check_integer(self, key: str, value: int) -> None:
        lower = self.lower.get(key)
        upper = self.upper.get(key)
        if lower is not None and (value < lower.value or (value == lower.value and not lower.inclusive)):
            self.contradictions.append(f"{key}={value} violates lower bound {lower.value}")
        if upper is not None and (value > upper.value or (value == upper.value and not upper.inclusive)):
            self.contradictions.append(f"{key}={value} violates upper bound {upper.value}")

    def _check_bounds(self, key: str) -> None:
        lower = self.lower.get(key)
        upper = self.upper.get(key)
        if lower is None or upper is None:
            return
        if lower.value > upper.value or (lower.value == upper.value and (not lower.inclusive or not upper.inclusive)):
            self.contradictions.append(f"{key} has incompatible numeric bounds")

    @property
    def unsatisfiable(self) -> bool:
        return bool(self.contradictions)

    @property
    def fully_modeled(self) -> bool:
        return not self.unsupported

    def combine(self, other: "ConstraintSet") -> "ConstraintSet":
        result = ConstraintSet()
        for key, value in self.equal.items():
            result.add_eq(key, value)
        for key, values in self.not_equal.items():
            for value in values:
                result.add_neq(key, value)
        for key, bound in self.lower.items():
            result.add_lower(key, bound.value, bound.inclusive)
        for key, bound in self.upper.items():
            result.add_upper(key, bound.value, bound.inclusive)
        for atom in self.opaque_positive:
            result.add_opaque(atom)
        for atom in self.opaque_negative:
            result.add_opaque(atom, negated=True)
        for key, value in other.equal.items():
            result.add_eq(key, value)
        for key, values in other.not_equal.items():
            for value in values:
                result.add_neq(key, value)
        for key, bound in other.lower.items():
            result.add_lower(key, bound.value, bound.inclusive)
        for key, bound in other.upper.items():
            result.add_upper(key, bound.value, bound.inclusive)
        for atom in other.opaque_positive:
            result.add_opaque(atom)
        for atom in other.opaque_negative:
            result.add_opaque(atom, negated=True)
        result.unsupported = [*self.unsupported, *other.unsupported]
        return result

    def implies(self, other: "ConstraintSet") -> bool:
        """Whether this supported conjunction logically implies ``other``.

        Unsupported operations on the right deliberately block proof.  Extra
        unsupported operations on the left are harmless: they only restrict
        the earlier route further and cannot invalidate a supported implication.
        """

        if self.unsatisfiable:
            return True
        if other.unsatisfiable or other.unsupported:
            return False
        for key, wanted in other.equal.items():
            if self.equal.get(key) != wanted:
                return False
        for key, wanted in other.not_equal.items():
            if not wanted <= self.not_equal.get(key, set()):
                assigned = self.equal.get(key)
                if assigned is None or assigned in wanted:
                    return False
        for key, wanted in other.lower.items():
            assigned = integer_value(self.equal.get(key))
            if assigned is not None:
                if assigned < wanted.value or (assigned == wanted.value and not wanted.inclusive):
                    return False
                continue
            actual = self.lower.get(key)
            if actual is None:
                return False
            if actual.value < wanted.value:
                return False
            if actual.value == wanted.value and wanted.inclusive is False and actual.inclusive:
                return False
        for key, wanted in other.upper.items():
            assigned = integer_value(self.equal.get(key))
            if assigned is not None:
                if assigned > wanted.value or (assigned == wanted.value and not wanted.inclusive):
                    return False
                continue
            actual = self.upper.get(key)
            if actual is None:
                return False
            if actual.value > wanted.value:
                return False
            if actual.value == wanted.value and wanted.inclusive is False and actual.inclusive:
                return False
        if not other.opaque_positive <= self.opaque_positive:
            return False
        if not other.opaque_negative <= self.opaque_negative:
            return False
        return True

    def payload(self) -> dict[str, Any]:
        return {
            "equal": dict(sorted(self.equal.items())),
            "not_equal": {key: sorted(values) for key, values in sorted(self.not_equal.items())},
            "lower": {key: asdict(value) for key, value in sorted(self.lower.items())},
            "upper": {key: asdict(value) for key, value in sorted(self.upper.items())},
            "opaque_positive": sorted(self.opaque_positive),
            "opaque_negative": sorted(self.opaque_negative),
            "unsupported_operations": list(dict.fromkeys(self.unsupported)),
            "contradictions": list(dict.fromkeys(self.contradictions)),
            "fully_modeled": self.fully_modeled,
            "unsatisfiable": self.unsatisfiable,
        }


@dataclass(frozen=True)
class RouteModel:
    entry: dialogue.DialogueEntry
    constraints: ConstraintSet
    condition_signature: str


@dataclass
class DialogueModelIndex:
    root: Path
    inventory: dialogue.DialogueInventory
    routes: tuple[RouteModel, ...]
    findings: list[dict[str, Any]]
    route_status: dict[int, str]
    warnings: list[str]


_CACHE: dict[Path, tuple[tuple[int, int, int], DialogueModelIndex]] = {}


def integer_value(value: str | None) -> int | None:
    if value is None or INTEGER_RE.fullmatch(value) is None:
        return None
    return int(value)


def expression_text(node: ast.AST) -> str:
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return f"{expression_text(node.left)}|{expression_text(node.right)}"
    try:
        return ast.unparse(node).replace("\n", " ").strip()
    except Exception:  # pragma: no cover - defensive AST rendering
        return "<unavailable>"


def operation_head(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return expression_text(node)
    if isinstance(node, (ast.Tuple, ast.List)) and node.elts:
        return expression_text(node.elts[0])
    return None


def operation_arguments(node: ast.AST) -> list[str]:
    if not isinstance(node, (ast.Tuple, ast.List)):
        return []
    return [expression_text(value) for value in node.elts[1:]]


def split_operation_name(name: str) -> tuple[bool, bool, str]:
    parts = name.split("|")
    negated = "neg" in parts[:-1]
    disjunction = "this_or_next" in parts[:-1]
    return negated, disjunction, parts[-1]


def dynamic_symbol(value: str) -> bool:
    return value.startswith((":", "$")) or REGISTER_RE.fullmatch(value) is not None


def relation_key(left: str, right: str) -> tuple[str, str] | None:
    left_dynamic = dynamic_symbol(left)
    right_dynamic = dynamic_symbol(right)
    if left_dynamic and not right_dynamic:
        return left, right
    if right_dynamic and not left_dynamic:
        return right, left
    return None


def inverse_comparator(operator: str) -> str:
    return {"eq": "neq", "neq": "eq", "ge": "lt", "gt": "le", "le": "gt", "lt": "ge"}[operator]


def apply_comparator(constraints: ConstraintSet, operator: str, key: str, value: str) -> None:
    if operator == "eq":
        constraints.add_eq(key, value)
    elif operator == "neq":
        constraints.add_neq(key, value)
    else:
        numeric = integer_value(value)
        if numeric is None:
            constraints.unsupported.append(f"{operator}({key}, {value})")
            return
        if operator == "ge":
            constraints.add_lower(key, numeric, True)
        elif operator == "gt":
            constraints.add_lower(key, numeric, False)
        elif operator == "le":
            constraints.add_upper(key, numeric, True)
        elif operator == "lt":
            constraints.add_upper(key, numeric, False)


def literal_comparison_holds(operator: str, left: int, right: int) -> bool:
    return {
        "eq": left == right,
        "neq": left != right,
        "ge": left >= right,
        "gt": left > right,
        "le": left <= right,
        "lt": left < right,
    }[operator]


def parse_condition(node: ast.AST, constraints: ConstraintSet) -> None:
    raw = expression_text(node)
    name = operation_head(node)
    if name is None:
        constraints.unsupported.append(raw)
        return
    negated, disjunction, operation = split_operation_name(name)
    args = operation_arguments(node)
    if disjunction:
        constraints.unsupported.append(raw)
        return
    if operation in CONTROL_OPERATIONS or operation.startswith("try_for_"):
        constraints.unsupported.append(raw)
        return
    if operation in COMPARATORS and len(args) >= 2:
        pair = relation_key(args[0], args[1])
        if pair is None:
            # Two locals/globals/registers can absolutely contain the same
            # value.  Only a comparison between *literal integers* can be
            # evaluated here; symbolic engine constants and dynamic/dynamic
            # relations remain a boundary rather than a fabricated falsehood.
            left = integer_value(args[0])
            right = integer_value(args[1])
            effective = inverse_comparator(operation) if negated else operation
            if left is not None and right is not None:
                if not literal_comparison_holds(effective, left, right):
                    constraints.contradictions.append(f"literal comparison {args[0]} {effective} {args[1]} is false")
            else:
                constraints.unsupported.append(raw)
            return
        key, value = pair
        apply_comparator(constraints, inverse_comparator(operation) if negated else operation, key, value)
        return
    if operation == "is_between" and len(args) >= 3 and dynamic_symbol(args[0]):
        lower = integer_value(args[1])
        upper = integer_value(args[2])
        if lower is None or upper is None:
            constraints.unsupported.append(raw)
            return
        if negated:
            # A negated range is disjunctive; preserving it as unsupported is
            # safer than fabricating either half of the range.
            constraints.unsupported.append(raw)
            return
        constraints.add_lower(args[0], lower, True)
        constraints.add_upper(args[0], upper, False)
        return
    if operation in SLOT_OPERATORS and len(args) >= 3:
        family, comparator = operation.rsplit("_", 1)
        if dynamic_symbol(args[2]):
            constraints.unsupported.append(raw)
            return
        key = f"{family}({args[0]}, {args[1]})"
        apply_comparator(constraints, inverse_comparator(comparator) if negated else comparator, key, args[2])
        return
    if operation == "call_script" and args and args[0].startswith("script_cf_"):
        constraints.add_opaque(f"{operation}({', '.join(args)})", negated=negated)
        return
    # Common direct boolean engine conditions are deterministic at route
    # selection time, but their relation to another arbitrary condition is not
    # known here.  Preserve an exact opaque atom so identical condition blocks
    # can still prove a shadow or overlap.
    if operation and not args and "<" not in raw:
        constraints.add_opaque(operation, negated=negated)
        return
    if operation.startswith(("party_", "troop_", "faction_", "quest_", "is_", "check_", "main_party_")):
        constraints.add_opaque(f"{operation}({', '.join(args)})", negated=negated)
        return
    constraints.unsupported.append(raw)


def condition_model_boundary(node: ast.AST) -> str | None:
    """Return a reason a route cannot use the branch-free proof core.

    M&B dialogue condition blocks are executable operation lists, not a
    declarative boolean language.  In particular, a `try_begin` / `else_try`
    block may select exactly one branch, so treating every branch condition as
    simultaneously true creates fabricated contradictions.  Rather than
    guessing engine control-flow semantics, one such operation makes the whole
    route *unproven*.  Simple predicate-only conjunctions remain eligible for
    deterministic proofs.
    """

    raw = expression_text(node)
    name = operation_head(node)
    if name is None:
        return f"<unparseable condition operation: {raw}>"
    _negated, disjunction, operation = split_operation_name(name)
    args = operation_arguments(node)
    if disjunction:
        return f"<disjunctive condition operation: {raw}>"
    if operation in CONTROL_OPERATIONS or operation.startswith("try_for_"):
        return f"<branch/loop control flow: {raw}>"
    if operation in COMPARATORS or operation == "is_between" or operation in SLOT_OPERATORS:
        return None
    if operation == "call_script":
        if args and args[0].startswith("script_cf_"):
            return None
        return f"<non-condition script call: {raw}>"
    if operation.startswith(SAFE_BOOLEAN_PREFIXES):
        return None
    return f"<state-changing or unsupported condition operation: {raw}>"


def constraints_for_entry(entry: dialogue.DialogueEntry) -> ConstraintSet:
    constraints = ConstraintSet()
    try:
        expression = ast.parse(entry.conditions, mode="eval").body
    except SyntaxError:
        constraints.unsupported.append("<unparseable generated condition block>")
        return constraints
    if not isinstance(expression, ast.List):
        constraints.unsupported.append("<non-list generated condition block>")
        return constraints
    boundaries = [condition_model_boundary(node) for node in expression.elts]
    boundaries = [boundary for boundary in boundaries if boundary is not None]
    if boundaries:
        constraints.unsupported.extend(dict.fromkeys(boundaries))
        return constraints
    for node in expression.elts:
        parse_condition(node, constraints)
    return constraints


def condition_signature(entry: dialogue.DialogueEntry) -> str:
    return re.sub(r"\s+", "", entry.conditions)


def route_payload(route: RouteModel, status: str | None = None) -> dict[str, Any]:
    payload = dialogue.entry_dict(route.entry)
    payload["model"] = route.constraints.payload()
    if status is not None:
        payload["status"] = status
    return payload


def group_key(route: RouteModel) -> tuple[str, str]:
    return route.entry.speaker, route.entry.start_state


def proven_implication(antecedent: RouteModel, consequent: RouteModel) -> bool:
    """Whether one route's modeled condition set implies another's."""

    if not antecedent.constraints.fully_modeled or not consequent.constraints.fully_modeled:
        return False
    if antecedent.condition_signature == consequent.condition_signature:
        return True
    return antecedent.constraints.implies(consequent.constraints)


def proven_overlap(left: RouteModel, right: RouteModel) -> bool:
    if not left.constraints.fully_modeled or not right.constraints.fully_modeled:
        return False
    if left.condition_signature == right.condition_signature:
        return not left.constraints.unsatisfiable
    return not left.constraints.combine(right.constraints).unsatisfiable


def source_payload(entry: dialogue.DialogueEntry) -> dict[str, Any] | None:
    if entry.source is None:
        return None
    return {"path": entry.source.path, "line_start": entry.source.line_start, "line_end": entry.source.line_end}


def route_finding(
    *,
    identifier: str,
    severity: str,
    category: str,
    summary: str,
    route: RouteModel,
    related: Sequence[RouteModel] = (),
    recommendation: str,
) -> dict[str, Any]:
    return {
        "id": identifier,
        "severity": severity,
        "category": category,
        "summary": summary,
        "route_index": route.entry.index,
        "source": source_payload(route.entry),
        "route": route_payload(route),
        "related_routes": [route_payload(item) for item in related[:8]],
        "recommendation": recommendation,
    }


def analyze_routes(routes: Sequence[RouteModel]) -> tuple[list[dict[str, Any]], dict[int, str]]:
    findings: list[dict[str, Any]] = []
    status: dict[int, str] = {
        route.entry.index: "model_boundary_unproven" if route.constraints.unsupported else "reachable_not_proven"
        for route in routes
    }
    for route in routes:
        if route.constraints.fully_modeled and route.constraints.unsatisfiable:
            status[route.entry.index] = "unreachable_proven"
            findings.append(
                route_finding(
                    identifier=f"unreachable:{route.entry.index}",
                    severity="error",
                    category="route_condition_contradiction",
                    summary=f"Route #{route.entry.index} has contradictory supported conditions and cannot match.",
                    route=route,
                    recommendation="Remove or correct the conflicting equality/range conditions before testing order or text behavior.",
                )
            )
    groups: dict[tuple[str, str], list[RouteModel]] = defaultdict(list)
    for route in routes:
        groups[group_key(route)].append(route)
    for (speaker, state), group in groups.items():
        ordered = sorted(group, key=lambda route: route.entry.index)
        if not ordered or ordered[0].entry.is_player:
            continue
        live_prior: list[RouteModel] = []
        for route in ordered:
            if status[route.entry.index] == "unreachable_proven":
                continue
            # A later NPC route is unreachable only when every state that
            # satisfies *its* conditions also satisfies an earlier route.
            # The opposite implication merely says the earlier route is more
            # specific and leaves the later fallback/general route reachable.
            shadowing = next((prior for prior in live_prior if proven_implication(route, prior)), None)
            if shadowing is not None:
                status[route.entry.index] = "shadowed_proven"
                findings.append(
                    route_finding(
                        identifier=f"shadowed:{shadowing.entry.index}:{route.entry.index}",
                        severity="error",
                        category="npc_route_shadowed_by_precedence",
                        summary=(
                            f"NPC route #{route.entry.index} cannot be selected: earlier route #{shadowing.entry.index} "
                            f"is in the same {speaker}/{state} first-match group and its conditions imply this route's conditions."
                        ),
                        route=route,
                        related=[shadowing],
                        recommendation="Move the specific route earlier, narrow the earlier route, or make the later route's state/conditions distinct.",
                    )
                )
            else:
                live_prior.append(route)
        live = [route for route in ordered if status[route.entry.index] == "reachable_not_proven"]
        for index, left in enumerate(live):
            for right in live[index + 1 :]:
                if not proven_overlap(left, right):
                    continue
                findings.append(
                    route_finding(
                        identifier=f"ambiguous-npc:{left.entry.index}:{right.entry.index}",
                        severity="warning",
                        category="npc_route_conditionally_ambiguous",
                        summary=(
                            f"NPC routes #{left.entry.index} and #{right.entry.index} have a proved overlapping supported condition set; "
                            "engine order selects the earlier route."
                        ),
                        route=right,
                        related=[left],
                        recommendation="Confirm that precedence is intentional or make the conditions mutually exclusive so the route choice is explicit.",
                    )
                )
    for (speaker, state), group in groups.items():
        players = [route for route in group if route.entry.is_player and status[route.entry.index] != "unreachable_proven"]
        for index, left in enumerate(players):
            for right in players[index + 1 :]:
                if left.entry.text != right.entry.text or left.entry.end_state == right.entry.end_state or not proven_overlap(left, right):
                    continue
                findings.append(
                    route_finding(
                        identifier=f"ambiguous-player:{left.entry.index}:{right.entry.index}",
                        severity="warning",
                        category="player_choice_conditionally_ambiguous",
                        summary=(
                            f"Player routes #{left.entry.index} and #{right.entry.index} can present identical text while routing to "
                            "different states under a proved overlapping condition set."
                        ),
                        route=right,
                        related=[left],
                        recommendation="Differentiate the player-facing text or make the conditions exclusive so a choice does not hide a different consequence.",
                    )
                )
    input_groups: dict[str, list[RouteModel]] = defaultdict(list)
    for route in routes:
        input_groups[route.entry.start_state].append(route)
    produced_states = {route.entry.end_state for route in routes}
    for state, outgoing in sorted(input_groups.items()):
        if state in dialogue.ENGINE_ENTRY_STATES or state in produced_states:
            continue
        sample = outgoing[0]
        findings.append(
            route_finding(
                identifier=f"orphan-input:{state}",
                severity="error",
                category="input_state_has_no_producer",
                summary=(
                    f"Dialogue state {state!r} has authored routes but is neither an M&B engine entry state "
                    "nor the target of any authored route; process_dialogs.py will assign an invalid input-state index."
                ),
                route=sample,
                related=outgoing[1:],
                recommendation="Add the intended incoming transition or remove the orphaned handler subgraph before exporting.",
            )
        )
    target_states = sorted({route.entry.end_state for route in routes if route.entry.end_state not in dialogue.ENGINE_HANDOFF_STATES})
    for state in target_states:
        outgoing = input_groups.get(state, [])
        if not outgoing:
            # Keep legacy handoff semantics out of the check but flag a real
            # target-only authored state as a terminal dead end.
            sample = next(route for route in routes if route.entry.end_state == state)
            findings.append(
                route_finding(
                    identifier=f"dead-target:{state}",
                    severity="warning",
                    category="target_state_has_no_authored_routes",
                    summary=f"Dialogue state {state!r} is targeted by route #{sample.entry.index} but has no authored outgoing route or known engine handoff.",
                    route=sample,
                    recommendation="Add the intended state handler or route to a documented engine handoff state.",
                )
            )
            continue
        if all(status[route.entry.index] in {"unreachable_proven", "shadowed_proven"} for route in outgoing):
            sample = outgoing[0]
            findings.append(
                route_finding(
                    identifier=f"terminal-dead:{state}",
                    severity="error",
                    category="dialogue_state_terminally_dead",
                    summary=f"Dialogue state {state!r} has outgoing authored routes, but every modeled candidate is proved unreachable or shadowed.",
                    route=sample,
                    related=outgoing[1:],
                    recommendation="Repair or remove the dead candidates before routing a player/NPC into this state.",
                )
            )
    severity_rank = {"error": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda item: (severity_rank.get(str(item["severity"]), 3), str(item["category"]), str(item["id"])))
    return findings, status


def source_signature(root: Path) -> tuple[int, int, int]:
    compiled = root / "compile" / "module_dialogs.py"
    newest = dialogue.newest_dialogue_input(root)
    compiled_stat = compiled.stat() if compiled.is_file() else None
    source_stat = newest.stat() if newest and newest.is_file() else None
    return (
        compiled_stat.st_mtime_ns if compiled_stat else -1,
        compiled_stat.st_size if compiled_stat else -1,
        source_stat.st_mtime_ns if source_stat else -1,
    )


def build_dialogue_model(root: Path = DEFAULT_REPO_ROOT) -> DialogueModelIndex:
    root = root.resolve()
    current_signature = source_signature(root)
    cached = _CACHE.get(root)
    if cached is not None and cached[0] == current_signature:
        return cached[1]
    try:
        inventory = dialogue.load_inventory(root)
    except dialogue.InspectorError as error:
        raise DialogueModelError(str(error)) from error
    routes = tuple(
        RouteModel(entry=entry, constraints=constraints_for_entry(entry), condition_signature=condition_signature(entry))
        for entry in inventory.entries
    )
    findings, route_status = analyze_routes(routes)
    warnings = [
        "The checker proves only branch-free supported predicate conjunctions, exact condition-block equality, and exact generated NPC route order; try/else flow and state-changing condition operations are explicit model boundaries.",
        "Route targets can be engine/UI handoffs. Only non-handoff target-only states are reported as authored dead ends.",
    ]
    if inventory.source_is_newer:
        warnings.append("Generated dialogue is older than canonical dialogue input; rebuild before treating compiled-order results as current runtime evidence.")
    index = DialogueModelIndex(root=root, inventory=inventory, routes=routes, findings=findings, route_status=route_status, warnings=warnings)
    _CACHE[root] = (current_signature, index)
    return index


def require_limit(value: int, maximum: int = 300) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise DialogueModelError(f"limit must be an integer from 1 through {maximum}.")
    return value


def require_query(value: str | None, *, name: str = "query") -> str:
    if not isinstance(value, str) or not value.strip():
        raise DialogueModelError(f"{name} must not be empty.")
    if len(value) > 500:
        raise DialogueModelError(f"{name} must be at most 500 characters.")
    return value.strip()


def summary_payload(index: DialogueModelIndex, *, limit: int = 30) -> dict[str, Any]:
    maximum = require_limit(limit)
    severity = Counter(str(item["severity"]) for item in index.findings)
    categories = Counter(str(item["category"]) for item in index.findings)
    status = Counter(index.route_status.values())
    unsupported = sum(bool(route.constraints.unsupported) for route in index.routes)
    return {
        "dialogue_model_checker_version": f"devkit.dialogue-model-checker.v{MODEL_VERSION}",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": {
            "repo_root": str(index.root),
            "read_only": True,
            "compiled_dialogue": dialogue.project_relative(index.inventory.compiled_path, index.root),
            "source_is_newer": index.inventory.source_is_newer,
        },
        "coverage": {
            "route_count": len(index.routes),
            "state_count": len({route.entry.start_state for route in index.routes}),
            "fully_modeled_route_count": len(index.routes) - unsupported,
            "partially_modeled_route_count": unsupported,
            "route_statuses": dict(sorted(status.items())),
        },
        "findings": {
            "total": len(index.findings),
            "by_severity": dict(sorted(severity.items())),
            "by_category": dict(sorted(categories.items())),
            "returned_count": min(len(index.findings), maximum),
            "truncated": len(index.findings) > maximum,
            "items": index.findings[:maximum],
        },
        "next_steps": [
            "Use dialogue_model_state to inspect exact compiled precedence and proof status for one state.",
            "Use dialogue_model_route to inspect a route's supported constraints and model boundaries before an order change.",
            "Use Dialogue Composer/Order Control only after this checker identifies a concrete route or precedence decision.",
        ],
        "warnings": index.warnings,
    }


def findings_payload(index: DialogueModelIndex, *, severity: str = "all", query: str | None = None, limit: int = 50) -> dict[str, Any]:
    maximum = require_limit(limit)
    if severity not in {"all", "error", "warning", "info"}:
        raise DialogueModelError("severity must be one of: all, error, warning, info.")
    needle = require_query(query).casefold() if query is not None else None
    selected = [
        item for item in index.findings
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


def state_payload(index: DialogueModelIndex, state: str, *, limit: int = 80) -> dict[str, Any]:
    maximum = require_limit(limit)
    checked = require_query(state, name="state")
    routes = [route for route in index.routes if route.entry.start_state == checked]
    groups: dict[str, list[RouteModel]] = defaultdict(list)
    for route in routes:
        groups[route.entry.speaker].append(route)
    rows = []
    for speaker, group in sorted(groups.items()):
        group.sort(key=lambda route: route.entry.index)
        rows.append(
            {
                "speaker": speaker,
                "selection_mode": "player_choices" if group and group[0].entry.is_player else "npc_first_match",
                "route_count": len(group),
                "routes": [route_payload(route, index.route_status[route.entry.index]) for route in group[:maximum]],
                "truncated": len(group) > maximum,
            }
        )
    return {
        "state": checked,
        "speaker_group_count": len(rows),
        "route_count": len(routes),
        "groups": rows,
        "warnings": index.warnings,
    }


def route_payload_by_index(index: DialogueModelIndex, route_index: int) -> dict[str, Any]:
    if isinstance(route_index, bool) or not isinstance(route_index, int) or not 1 <= route_index <= len(index.routes):
        raise DialogueModelError(f"route_index must be an integer from 1 through {len(index.routes):,}.")
    route = index.routes[route_index - 1]
    group = [candidate for candidate in index.routes if group_key(candidate) == group_key(route)]
    group.sort(key=lambda candidate: candidate.entry.index)
    position = group.index(route)
    previous = group[:position]
    return {
        "route": route_payload(route, index.route_status[route.entry.index]),
        "selection_group": {
            "speaker": route.entry.speaker,
            "start_state": route.entry.start_state,
            "selection_mode": "player_choices" if route.entry.is_player else "npc_first_match",
            "position": position + 1,
            "group_route_count": len(group),
            "preceding_routes": [route_payload(candidate, index.route_status[candidate.entry.index]) for candidate in previous[-20:]],
        },
        "related_findings": [item for item in index.findings if item.get("route_index") == route_index or route_index in [related["index"] for related in item.get("related_routes", [])]],
        "warnings": index.warnings,
    }


def render_markdown(payload: Mapping[str, Any], command: str) -> str:
    if command == "summary":
        coverage = payload["coverage"]
        findings = payload["findings"]
        lines = [
            "# Dialogue Reachability Model Checker",
            "",
            f"- Routes: {coverage['route_count']:,}; states: {coverage['state_count']:,}; fully modeled: {coverage['fully_modeled_route_count']:,}.",
            f"- Findings: {findings['total']} ({', '.join(f'{key}={value}' for key, value in findings['by_severity'].items()) or 'none'}).",
        ]
    else:
        lines = [f"# Dialogue Model: {command}", "", "Use JSON output for source-mapped constraint evidence."]
    if payload.get("warnings"):
        lines.extend(["", "## Model boundaries", "", *(f"- {warning}" for warning in payload["warnings"])])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only path-sensitive dialogue reachability model checker for SoD Modern.")
    parser.add_argument("command", choices=("summary", "findings", "state", "route"), nargs="?", default="summary")
    parser.add_argument("query", nargs="?", help="State for state, route index for route, optional text filter for findings.")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--severity", choices=("all", "error", "warning", "info"), default="all")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        index = build_dialogue_model(args.root.resolve())
        if args.command == "summary":
            payload = summary_payload(index, limit=args.limit)
        elif args.command == "findings":
            payload = findings_payload(index, severity=args.severity, query=args.query, limit=args.limit)
        elif args.command == "state":
            payload = state_payload(index, require_query(args.query, name="state"), limit=args.limit)
        else:
            checked = require_query(args.query, name="route_index")
            try:
                route_index = int(checked, 10)
            except ValueError as error:
                raise DialogueModelError("route_index must be an integer.") from error
            payload = route_payload_by_index(index, route_index)
        if args.format == "markdown":
            sys.stdout.write(render_markdown(payload, args.command))
        else:
            sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    except DialogueModelError as error:
        print(f"dialogue_model_checker: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
