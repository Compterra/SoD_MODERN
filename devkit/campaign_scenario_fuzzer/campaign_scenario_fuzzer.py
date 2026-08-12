#!/usr/bin/env python3
"""Safe subset campaign scenario fuzzer for M&B 1.011 source scripts.

This is deliberately not an engine emulator. It executes only a documented,
in-memory subset of literal script operations against generated *valid* state
domains, and reports unsupported operations as inconclusive boundaries. That
makes it useful for catching a missing guard or impossible scripted transition
before an in-game test, without pretending that Python can reproduce map AI,
saves, parties created by the engine, or every native operation.
"""

from __future__ import annotations

import argparse
import copy
import json
import random
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
DEFAULT_SCENARIOS_PATH = TOOL_DIR / "scenarios.json"
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.campaign_state_doctor import campaign_state_doctor as doctor


FUZZER_VERSION = "1.0.0"
CONTROL_OPEN = doctor.CONTROL_OPEN
CONTROL_ALTERNATE = doctor.CONTROL_ALTERNATE
CONTROL_CLOSE = doctor.CONTROL_CLOSE
NUMBER_RE = re.compile(r"^-?\d+$")


class ScenarioFuzzerError(RuntimeError):
    """A bounded scenario-fuzz query cannot be answered safely."""


class UnknownExecution(RuntimeError):
    """The requested path crossed an intentionally unsupported engine boundary."""


@dataclass
class Party:
    identifier: int
    active: bool = True
    template: str = ""
    slots: dict[str, Any] = field(default_factory=dict)
    ai: dict[str, Any] = field(default_factory=dict)
    attachment: Any = None
    position: Any = None


@dataclass
class RuntimeState:
    parties: dict[int, Party]
    party_aliases: dict[str, int]
    factions: dict[str, dict[str, Any]]
    globals: dict[str, Any]
    registers: dict[str, Any]
    clock: dict[str, int]
    frames: list[dict[str, Any]] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)
    boundaries: list[dict[str, Any]] = field(default_factory=list)
    depth: int = 0

    def current_frame(self) -> dict[str, Any]:
        if not self.frames:
            raise UnknownExecution("No active script frame.")
        return self.frames[-1]


@dataclass
class RunResult:
    status: str
    assertions: list[dict[str, Any]]
    trace: list[dict[str, Any]]
    boundaries: list[dict[str, Any]]
    state: dict[str, Any]


@dataclass
class ScenarioIndex:
    root: Path
    scenarios_path: Path
    state_index: doctor.StateDoctorIndex
    scenarios: dict[str, dict[str, Any]]
    warnings: list[str]


_CACHE: dict[tuple[Path, Path], tuple[tuple[tuple[str, int, int], ...], ScenarioIndex]] = {}


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def require_limit(value: int, maximum: int = 1000) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise ScenarioFuzzerError(f"iterations must be an integer from 1 through {maximum}.")
    return value


def require_query(value: str | None, *, name: str = "scenario_id") -> str:
    if not isinstance(value, str) or not value.strip():
        raise ScenarioFuzzerError(f"{name} must not be empty.")
    if len(value) > 160:
        raise ScenarioFuzzerError(f"{name} must be at most 160 characters.")
    return value.strip()


def load_scenarios(path: Path) -> dict[str, dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ScenarioFuzzerError(f"Could not read scenario catalog at {path}: {error}") from error
    if not isinstance(payload, dict) or payload.get("schema") != "devkit.campaign-scenario-fuzzer.v1":
        raise ScenarioFuzzerError("Scenario catalog must use schema devkit.campaign-scenario-fuzzer.v1.")
    raw = payload.get("scenarios")
    if not isinstance(raw, list):
        raise ScenarioFuzzerError("Scenario catalog must contain a scenarios list.")
    scenarios: dict[str, dict[str, Any]] = {}
    for scenario in raw:
        if not isinstance(scenario, dict):
            raise ScenarioFuzzerError("Each scenario must be an object.")
        identifier = scenario.get("id")
        entry = scenario.get("entry_script")
        assertions = scenario.get("assertions")
        if not isinstance(identifier, str) or not identifier or identifier in scenarios:
            raise ScenarioFuzzerError("Scenario IDs must be unique non-empty strings.")
        if not isinstance(entry, str) or not entry.startswith("script_"):
            raise ScenarioFuzzerError(f"Scenario {identifier!r} needs an entry_script beginning script_.")
        if not isinstance(assertions, list) or not assertions:
            raise ScenarioFuzzerError(f"Scenario {identifier!r} needs at least one assertion.")
        scenarios[identifier] = copy.deepcopy(scenario)
    return scenarios


def input_signature(root: Path, scenarios_path: Path) -> tuple[tuple[str, int, int], ...]:
    paths = [scenarios_path, *root.joinpath("src", "scripts").rglob("*.py"), *root.joinpath("src", "triggers").rglob("*.py")]
    rows = []
    for path in sorted(set(paths), key=lambda value: str(value).casefold()):
        try:
            stat = path.stat()
        except OSError:
            rows.append((project_relative(path, root), -1, -1))
        else:
            rows.append((project_relative(path, root), stat.st_mtime_ns, stat.st_size))
    return tuple(rows)


def build_scenario_fuzzer(
    root: Path = DEFAULT_REPO_ROOT,
    *,
    scenarios_path: Path | None = None,
    state_contracts_path: Path | None = None,
) -> ScenarioIndex:
    root = root.resolve()
    checked = (scenarios_path or (root / "devkit" / "campaign_scenario_fuzzer" / "scenarios.json")).resolve()
    if not checked.is_file() and scenarios_path is None:
        checked = DEFAULT_SCENARIOS_PATH
    if not checked.is_file():
        raise ScenarioFuzzerError(f"Missing scenario catalog: {checked}")
    key = (root, checked)
    current = input_signature(root, checked)
    cached = _CACHE.get(key)
    if cached is not None and cached[0] == current:
        return cached[1]
    try:
        state_index = doctor.build_state_doctor(root, contracts_path=state_contracts_path)
    except doctor.CampaignStateError as error:
        raise ScenarioFuzzerError(str(error)) from error
    scenarios = load_scenarios(checked)
    missing = sorted({scenario["entry_script"] for scenario in scenarios.values()} - set(state_index.scripts))
    warnings = [
        "The scenario fuzzer executes only its documented literal-operation subset in memory. Unsupported operations, dynamic selectors, loops, recursive calls, and unresolved condition scripts produce inconclusive evidence instead of a fictional pass/fail.",
        "A fuzz failure is a concrete counterexample inside the modeled subset; it still needs normal source and in-game review before changing gameplay.",
        *state_index.warnings,
    ]
    if missing:
        warnings.append("Scenario catalog references source scripts not currently modeled: " + ", ".join(missing))
    index = ScenarioIndex(root, checked, state_index, scenarios, list(dict.fromkeys(warnings)))
    _CACHE[key] = (current, index)
    return index


def initial_state(spec: Mapping[str, Any], rng: random.Random) -> RuntimeState:
    raw_state = spec.get("state", {})
    if not isinstance(raw_state, dict):
        raise ScenarioFuzzerError("scenario.state must be an object.")
    raw_parties = raw_state.get("parties", {})
    if not isinstance(raw_parties, dict):
        raise ScenarioFuzzerError("scenario.state.parties must be an object.")
    parties: dict[int, Party] = {}
    aliases: dict[str, int] = {}
    next_identifier = 1
    for alias, raw_party in raw_parties.items():
        if not isinstance(alias, str) or not isinstance(raw_party, dict):
            raise ScenarioFuzzerError("scenario parties must map aliases to objects.")
        identifier = raw_party.get("id", next_identifier)
        if isinstance(identifier, bool) or not isinstance(identifier, int) or identifier <= 0 or identifier in parties:
            raise ScenarioFuzzerError(f"Party {alias!r} needs a unique positive numeric id.")
        next_identifier = max(next_identifier, identifier + 1)
        party = Party(
            identifier=identifier,
            active=bool(raw_party.get("active", True)),
            template=str(raw_party.get("template", "")),
            slots=copy.deepcopy(raw_party.get("slots", {})) if isinstance(raw_party.get("slots", {}), dict) else {},
            ai=copy.deepcopy(raw_party.get("ai", {})) if isinstance(raw_party.get("ai", {}), dict) else {},
            attachment=raw_party.get("attachment"),
            position=raw_party.get("position", f"position:{alias}"),
        )
        parties[identifier] = party
        aliases[alias] = identifier
    globals_state = copy.deepcopy(raw_state.get("globals", {})) if isinstance(raw_state.get("globals", {}), dict) else {}
    registers = copy.deepcopy(raw_state.get("registers", {})) if isinstance(raw_state.get("registers", {}), dict) else {}
    factions = copy.deepcopy(raw_state.get("factions", {})) if isinstance(raw_state.get("factions", {}), dict) else {}
    clock_raw = raw_state.get("clock", {})
    clock = {"day": int(clock_raw.get("day", 0)), "hours": int(clock_raw.get("hours", 0))} if isinstance(clock_raw, dict) else {"day": 0, "hours": 0}
    runtime = RuntimeState(parties, aliases, factions, globals_state, registers, clock)
    apply_fuzz_domains(runtime, spec.get("fuzz", {}), rng)
    return runtime


def apply_fuzz_domains(state: RuntimeState, raw: Any, rng: random.Random) -> None:
    if raw is None:
        return
    if not isinstance(raw, dict):
        raise ScenarioFuzzerError("scenario.fuzz must be an object.")
    ranges = raw.get("integer_ranges", {})
    if not isinstance(ranges, dict):
        raise ScenarioFuzzerError("scenario.fuzz.integer_ranges must be an object.")
    for target, bounds in ranges.items():
        if not isinstance(target, str) or not isinstance(bounds, list) or len(bounds) != 2 or any(isinstance(value, bool) or not isinstance(value, int) for value in bounds):
            raise ScenarioFuzzerError("Each integer fuzz range must be a target and [minimum, maximum].")
        lower, upper = bounds
        if lower > upper:
            raise ScenarioFuzzerError("Fuzz range minimum must not exceed maximum.")
        value = rng.randint(lower, upper)
        if target.startswith("$"):
            state.globals[target] = value
        elif target.startswith(("reg", "s")):
            state.registers[target] = value
        elif target in {"day", "hours"}:
            state.clock[target] = value
        else:
            raise ScenarioFuzzerError("Integer fuzz targets must be globals, registers, day, or hours.")
    slots = raw.get("party_slots", [])
    if not isinstance(slots, list):
        raise ScenarioFuzzerError("scenario.fuzz.party_slots must be a list.")
    for item in slots:
        if not isinstance(item, dict):
            raise ScenarioFuzzerError("party slot fuzz entries must be objects.")
        alias, slot = item.get("party"), item.get("slot")
        lower, upper = item.get("minimum"), item.get("maximum")
        if not isinstance(alias, str) or not isinstance(slot, str) or any(isinstance(value, bool) or not isinstance(value, int) for value in (lower, upper)) or lower > upper:
            raise ScenarioFuzzerError("party slot fuzz needs party, slot, and valid integer minimum/maximum.")
        if alias not in state.party_aliases:
            raise ScenarioFuzzerError(f"Unknown fuzz party alias {alias!r}.")
        state.parties[state.party_aliases[alias]].slots[slot] = rng.randint(lower, upper)


def resolve_parameter(value: Any, state: RuntimeState) -> Any:
    if isinstance(value, dict) and set(value) == {"party"} and isinstance(value["party"], str):
        alias = value["party"]
        if alias not in state.party_aliases:
            raise ScenarioFuzzerError(f"Scenario parameter references unknown party alias {alias!r}.")
        return state.party_aliases[alias]
    return value


def resolve(token: str, state: RuntimeState) -> Any:
    if NUMBER_RE.fullmatch(token):
        return int(token)
    if token.startswith(":"):
        return state.current_frame().get(token)
    if token.startswith("$"):
        return state.globals.get(token)
    if (token.startswith("s") and token[1:].isdigit()) or (token.startswith("reg") and token[3:].isdigit()):
        return state.registers.get(token)
    if state.frames and token in state.current_frame():
        return state.current_frame()[token]
    # Engine constants, party-template IDs, positions, and operation flags are
    # symbolic values. They are valid in equality checks without a lookup.
    return token


def assign(destination: str, value: Any, state: RuntimeState) -> None:
    if destination.startswith(":"):
        state.current_frame()[destination] = value
    elif destination.startswith("$"):
        state.globals[destination] = value
    elif destination.startswith(("reg", "s")):
        state.registers[destination] = value
    else:
        state.current_frame()[destination] = value


def party_for(value: Any, state: RuntimeState) -> Party:
    if isinstance(value, bool) or not isinstance(value, int) or value not in state.parties:
        raise UnknownExecution(f"Party selector {value!r} is not a generated valid scenario party.")
    return state.parties[value]


def compare(operator: str, left: Any, right: Any) -> bool:
    if left is None or right is None:
        raise UnknownExecution("Comparison uses an unresolved runtime value.")
    if operator == "eq":
        return left == right
    if operator == "neq":
        return left != right
    if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
        raise UnknownExecution(f"{operator} requires numeric values, got {left!r} and {right!r}.")
    return {"ge": left >= right, "gt": left > right, "le": left <= right, "lt": left < right}[operator]


def condition_result(operation: doctor.Operation, state: RuntimeState, index: ScenarioIndex, rng: random.Random) -> bool:
    raw_name = operation.name
    negated = raw_name.startswith("neg|")
    name = doctor.base_operation(raw_name)
    args = [resolve(value, state) for value in operation.args]
    if name in {"eq", "neq", "ge", "gt", "le", "lt"} and len(args) >= 2:
        result = compare(name, args[0], args[1])
    elif name == "is_between" and len(args) >= 3:
        if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in args[:3]):
            raise UnknownExecution("is_between requires numeric resolved values.")
        result = args[1] <= args[0] < args[2]
    elif name == "party_is_active" and args:
        result = party_for(args[0], state).active
    elif name.startswith("party_slot_") and len(args) >= 3:
        party = party_for(args[0], state)
        operator = name.rsplit("_", 1)[-1]
        result = compare(operator, party.slots.get(str(operation.args[1]), 0), args[2])
    elif name.startswith("faction_slot_") and len(args) >= 3:
        faction = state.factions.get(str(args[0]), {})
        operator = name.rsplit("_", 1)[-1]
        result = compare(operator, faction.get(str(operation.args[1]), 0), args[2])
    elif name == "call_script" and operation.args and operation.args[0].startswith("script_cf_"):
        result = execute_script(operation.args[0], args[1:], state, index, rng) == "completed"
    else:
        raise UnknownExecution(f"Unsupported condition operation {raw_name}.")
    return not result if negated else result


def matching_try_end(operations: Sequence[doctor.Operation], start: int) -> int:
    depth = 0
    for position in range(start, len(operations)):
        name = doctor.base_operation(operations[position].name)
        if name in CONTROL_OPEN:
            depth += 1
        elif name in CONTROL_CLOSE:
            depth -= 1
            if depth == 0:
                return position
    raise UnknownExecution("Unclosed try block in modeled script source.")


def try_branches(operations: Sequence[doctor.Operation], start: int, end: int) -> list[list[doctor.Operation]]:
    branches: list[list[doctor.Operation]] = [[]]
    depth = 0
    for operation in operations[start + 1 : end]:
        name = doctor.base_operation(operation.name)
        if name in CONTROL_OPEN:
            depth += 1
        elif name in CONTROL_CLOSE:
            depth -= 1
        if name in CONTROL_ALTERNATE and depth == 0:
            branches.append([])
            continue
        branches[-1].append(operation)
    return branches


def branch_prefix(branch: Sequence[doctor.Operation]) -> tuple[list[doctor.Operation], list[doctor.Operation]]:
    conditions: list[doctor.Operation] = []
    for position, operation in enumerate(branch):
        name = doctor.base_operation(operation.name)
        if name in CONTROL_OPEN:
            return conditions, list(branch[position:])
        if doctor.is_condition_operation(operation):
            conditions.append(operation)
            continue
        return conditions, list(branch[position:])
    return conditions, []


def trace(state: RuntimeState, operation: doctor.Operation, effect: str, **details: Any) -> None:
    state.trace.append(
        {
            "effect": effect,
            "operation": {
                "id": operation.id,
                "scope_id": operation.scope_id,
                "name": operation.name,
                "args": list(operation.args),
                "source": doctor.source_payload(operation.source),
            },
            **details,
        }
    )


def numeric(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise UnknownExecution(f"{label} needs an integer runtime value, got {value!r}.")
    return value


def apply_action(operation: doctor.Operation, state: RuntimeState, index: ScenarioIndex, rng: random.Random) -> str:
    name = doctor.base_operation(operation.name)
    raw_args = operation.args
    args = [resolve(value, state) for value in raw_args]
    if name == "store_script_param" and len(raw_args) >= 2:
        assign(raw_args[0], state.current_frame().get("__params", [])[numeric(args[1], "script parameter") - 1], state)
        trace(state, operation, "store_script_param")
    elif name == "assign" and len(raw_args) >= 2:
        assign(raw_args[0], args[1], state)
        trace(state, operation, "assign", destination=raw_args[0], value=args[1])
    elif name in {"store_add", "store_sub", "store_mul", "store_div", "store_mod"} and len(raw_args) >= 3:
        left, right = numeric(args[1], name), numeric(args[2], name)
        value = {
            "store_add": left + right,
            "store_sub": left - right,
            "store_mul": left * right,
            "store_div": left // right if right else None,
            "store_mod": left % right if right else None,
        }[name]
        if value is None:
            raise UnknownExecution(f"{name} divides by zero.")
        assign(raw_args[0], value, state)
        trace(state, operation, name, destination=raw_args[0], value=value)
    elif name in {"val_add", "val_sub", "val_mul", "val_div", "val_mod"} and len(raw_args) >= 2:
        current = numeric(resolve(raw_args[0], state), name)
        delta = numeric(args[1], name)
        value = {
            "val_add": current + delta,
            "val_sub": current - delta,
            "val_mul": current * delta,
            "val_div": current // delta if delta else None,
            "val_mod": current % delta if delta else None,
        }[name]
        if value is None:
            raise UnknownExecution(f"{name} divides by zero.")
        assign(raw_args[0], value, state)
        trace(state, operation, name, destination=raw_args[0], value=value)
    elif name == "store_random_in_range" and len(raw_args) >= 3:
        lower, upper = numeric(args[1], name), numeric(args[2], name)
        if lower >= upper:
            raise UnknownExecution("store_random_in_range has an empty range.")
        value = rng.randrange(lower, upper)
        assign(raw_args[0], value, state)
        trace(state, operation, name, destination=raw_args[0], value=value)
    elif name == "store_current_day" and raw_args:
        assign(raw_args[0], state.clock["day"], state)
        trace(state, operation, name)
    elif name == "store_current_hours" and raw_args:
        assign(raw_args[0], state.clock["hours"], state)
        trace(state, operation, name)
    elif name == "party_get_template_id" and len(raw_args) >= 2:
        assign(raw_args[0], party_for(args[1], state).template, state)
        trace(state, operation, name)
    elif name == "party_get_slot" and len(raw_args) >= 3:
        party = party_for(args[1], state)
        assign(raw_args[0], party.slots.get(raw_args[2], 0), state)
        trace(state, operation, name)
    elif name == "party_set_slot" and len(raw_args) >= 3:
        party = party_for(args[0], state)
        party.slots[raw_args[1]] = args[2]
        trace(state, operation, name, party=party.identifier, slot=raw_args[1], value=args[2])
    elif name == "faction_get_slot" and len(raw_args) >= 3:
        faction = state.factions.setdefault(str(args[1]), {})
        assign(raw_args[0], faction.get(raw_args[2], 0), state)
        trace(state, operation, name)
    elif name == "faction_set_slot" and len(raw_args) >= 3:
        state.factions.setdefault(str(args[0]), {})[raw_args[1]] = args[2]
        trace(state, operation, name, faction=args[0], slot=raw_args[1], value=args[2])
    elif name == "party_get_position" and len(raw_args) >= 2:
        assign(raw_args[0], party_for(args[1], state).position, state)
        trace(state, operation, name)
    elif name == "party_set_flags" and len(raw_args) >= 3:
        # Flags do not affect any currently supported assertion, but this
        # literal, deterministic write is safe to pass through rather than
        # turning an otherwise complete camp-lock scenario inconclusive.
        trace(state, operation, name, party=party_for(args[0], state).identifier, flag=args[1], value=args[2])
    elif name.startswith("party_set_ai_") and len(raw_args) >= 2:
        party = party_for(args[0], state)
        field = {
            "party_set_ai_behavior": "behavior",
            "party_set_ai_initiative": "initiative",
            "party_set_ai_object": "object",
            "party_set_ai_target_position": "target_position",
            "party_set_ai_patrol_radius": "patrol_radius",
        }.get(name)
        if field is None:
            raise UnknownExecution(f"Unsupported party AI write {name}.")
        party.ai[field] = args[1]
        trace(state, operation, name, party=party.identifier, field=field, value=args[1])
    elif name == "party_attach_to_party" and len(raw_args) >= 2:
        party = party_for(args[0], state)
        party.attachment = args[1]
        trace(state, operation, name, party=party.identifier, attachment=args[1])
    elif name == "party_detach" and raw_args:
        party = party_for(args[0], state)
        party.attachment = None
        trace(state, operation, name, party=party.identifier)
    elif name == "remove_party" and raw_args:
        party = party_for(args[0], state)
        party.active = False
        trace(state, operation, name, party=party.identifier)
    elif name == "call_script" and raw_args:
        target = raw_args[0]
        if not target.startswith("script_"):
            raise UnknownExecution("call_script has a dynamic target.")
        trace(state, operation, name, target=target)
        return execute_script(target, args[1:], state, index, rng)
    else:
        raise UnknownExecution(f"Unsupported action operation {operation.name}.")
    return "completed"


def execute_sequence(operations: Sequence[doctor.Operation], state: RuntimeState, index: ScenarioIndex, rng: random.Random) -> str:
    position = 0
    while position < len(operations):
        operation = operations[position]
        name = doctor.base_operation(operation.name)
        if name in CONTROL_OPEN:
            if name != "try_begin":
                raise UnknownExecution(f"Unsupported loop/control operation {operation.name}.")
            end = matching_try_end(operations, position)
            selected = False
            for branch in try_branches(operations, position, end):
                conditions, body = branch_prefix(branch)
                try:
                    matches = all(condition_result(candidate, state, index, rng) for candidate in conditions)
                except UnknownExecution:
                    raise
                if matches:
                    selected = True
                    trace(state, operation, "try_branch_selected", branch_condition_count=len(conditions))
                    result = execute_sequence(body, state, index, rng)
                    if result != "completed":
                        return result
                    break
            if not selected:
                trace(state, operation, "try_no_branch_matched")
            position = end + 1
            continue
        if name in CONTROL_ALTERNATE or name in CONTROL_CLOSE:
            raise UnknownExecution(f"Unexpected unpaired control operation {operation.name}.")
        if doctor.is_condition_operation(operation):
            if not condition_result(operation, state, index, rng):
                trace(state, operation, "condition_failed")
                return "failed_condition"
            trace(state, operation, "condition_passed")
        else:
            result = apply_action(operation, state, index, rng)
            if result != "completed":
                return result
        position += 1
    return "completed"


def execute_script(symbol: str, parameters: Sequence[Any], state: RuntimeState, index: ScenarioIndex, rng: random.Random) -> str:
    if state.depth >= 16:
        raise UnknownExecution("Script recursion/depth cutoff reached.")
    record = index.state_index.scripts.get(symbol)
    if record is None:
        raise UnknownExecution(f"Called script {symbol} has no modeled canonical source definition.")
    state.depth += 1
    state.frames.append({"__params": list(parameters)})
    state.trace.append({"effect": "script_enter", "script_symbol": symbol, "parameters": list(parameters)})
    try:
        result = execute_sequence(record.operations, state, index, rng)
        state.trace.append({"effect": "script_exit", "script_symbol": symbol, "status": result})
        return result
    finally:
        state.frames.pop()
        state.depth -= 1


def serialize_state(state: RuntimeState) -> dict[str, Any]:
    return {
        "parties": {
            alias: {
                "id": identifier,
                "active": state.parties[identifier].active,
                "template": state.parties[identifier].template,
                "slots": state.parties[identifier].slots,
                "ai": state.parties[identifier].ai,
                "attachment": state.parties[identifier].attachment,
            }
            for alias, identifier in sorted(state.party_aliases.items())
        },
        "factions": state.factions,
        "globals": state.globals,
        "registers": state.registers,
        "clock": state.clock,
    }


def assertion_result(assertion: Mapping[str, Any], state: RuntimeState) -> dict[str, Any]:
    kind = assertion.get("kind")
    if kind == "party_ai_equals":
        alias, field, expected = assertion.get("party"), assertion.get("field"), assertion.get("equals")
        if not isinstance(alias, str) or alias not in state.party_aliases or not isinstance(field, str):
            return {"kind": kind, "passed": False, "reason": "Invalid party_ai_equals assertion."}
        actual = state.parties[state.party_aliases[alias]].ai.get(field)
        return {"kind": kind, "party": alias, "field": field, "expected": expected, "actual": actual, "passed": actual == expected}
    if kind == "party_slot_equals":
        alias, slot, expected = assertion.get("party"), assertion.get("slot"), assertion.get("equals")
        if not isinstance(alias, str) or alias not in state.party_aliases or not isinstance(slot, str):
            return {"kind": kind, "passed": False, "reason": "Invalid party_slot_equals assertion."}
        actual = state.parties[state.party_aliases[alias]].slots.get(slot, 0)
        return {"kind": kind, "party": alias, "slot": slot, "expected": expected, "actual": actual, "passed": actual == expected}
    if kind == "party_active_equals":
        alias, expected = assertion.get("party"), assertion.get("equals")
        if not isinstance(alias, str) or alias not in state.party_aliases or not isinstance(expected, bool):
            return {"kind": kind, "passed": False, "reason": "Invalid party_active_equals assertion."}
        actual = state.parties[state.party_aliases[alias]].active
        return {"kind": kind, "party": alias, "expected": expected, "actual": actual, "passed": actual == expected}
    if kind == "faction_slot_equals":
        faction, slot, expected = assertion.get("faction"), assertion.get("slot"), assertion.get("equals")
        if not isinstance(faction, str) or not isinstance(slot, str):
            return {"kind": kind, "passed": False, "reason": "Invalid faction_slot_equals assertion."}
        actual = state.factions.get(faction, {}).get(slot, 0)
        return {"kind": kind, "faction": faction, "slot": slot, "expected": expected, "actual": actual, "passed": actual == expected}
    return {"kind": kind, "passed": False, "reason": f"Unsupported assertion kind {kind!r}."}


def run_once(index: ScenarioIndex, scenario: Mapping[str, Any], *, seed: int) -> RunResult:
    rng = random.Random(seed)
    state = initial_state(scenario, rng)
    parameters = [resolve_parameter(value, state) for value in scenario.get("parameters", [])]
    try:
        execution = execute_script(str(scenario["entry_script"]), parameters, state, index, rng)
        if execution != "completed":
            state.boundaries.append({"kind": "script_condition_failed", "entry_script": scenario["entry_script"], "status": execution})
        assertions = [assertion_result(assertion, state) for assertion in scenario["assertions"]]
        failed = [assertion for assertion in assertions if not assertion["passed"]]
        status = "failed" if failed else "inconclusive" if state.boundaries else "passed"
    except (UnknownExecution, IndexError, KeyError, TypeError, ValueError) as error:
        state.boundaries.append({"kind": "unsupported_or_unresolved_execution", "message": str(error)})
        assertions = [assertion_result(assertion, state) for assertion in scenario["assertions"]]
        status = "inconclusive"
    return RunResult(status, assertions, list(state.trace), list(state.boundaries), serialize_state(state))


def scenario_catalog_payload(index: ScenarioIndex, *, scenario_id: str | None = None) -> dict[str, Any]:
    checked = require_query(scenario_id) if scenario_id is not None else None
    scenarios = []
    for identifier, scenario in sorted(index.scenarios.items()):
        if checked is not None and identifier != checked:
            continue
        scenarios.append(
            {
                "id": identifier,
                "description": scenario.get("description", ""),
                "entry_script": scenario["entry_script"],
                "parameter_count": len(scenario.get("parameters", [])),
                "assertion_count": len(scenario["assertions"]),
                "fuzz_domains": scenario.get("fuzz", {}),
                "entry_script_modeled": scenario["entry_script"] in index.state_index.scripts,
            }
        )
    if checked is not None and not scenarios:
        raise ScenarioFuzzerError(f"No scenario with id {checked!r}.")
    return {
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
        "warnings": index.warnings,
    }


def fuzz_payload(index: ScenarioIndex, scenario_id: str, *, iterations: int = 50, seed: int = 1, trace_limit: int = 80) -> dict[str, Any]:
    identifier = require_query(scenario_id)
    maximum = require_limit(iterations)
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ScenarioFuzzerError("seed must be an integer.")
    if isinstance(trace_limit, bool) or not isinstance(trace_limit, int) or not 1 <= trace_limit <= 500:
        raise ScenarioFuzzerError("trace_limit must be an integer from 1 through 500.")
    scenario = index.scenarios.get(identifier)
    if scenario is None:
        raise ScenarioFuzzerError(f"No scenario with id {identifier!r}.")
    outcomes = []
    counts = {"passed": 0, "failed": 0, "inconclusive": 0}
    for offset in range(maximum):
        run_seed = seed + offset
        result = run_once(index, scenario, seed=run_seed)
        counts[result.status] += 1
        if result.status != "passed":
            outcomes.append(
                {
                    "iteration": offset + 1,
                    "seed": run_seed,
                    "status": result.status,
                    "assertions": result.assertions,
                    "boundaries": result.boundaries,
                    "trace": result.trace[:trace_limit],
                    "trace_truncated": len(result.trace) > trace_limit,
                    "state": result.state,
                }
            )
    first_failure = next((item for item in outcomes if item["status"] == "failed"), None)
    status = "failed" if counts["failed"] else "inconclusive" if counts["inconclusive"] else "passed"
    return {
        "scenario_id": identifier,
        "entry_script": scenario["entry_script"],
        "iterations": maximum,
        "seed": seed,
        "status": status,
        "outcomes": counts,
        "first_counterexample": first_failure,
        "nonpassing_sample": outcomes[:20],
        "nonpassing_sample_truncated": len(outcomes) > 20,
        "interpretation": {
            "passed": "Every generated valid state completed inside the supported subset and satisfied the assertions.",
            "failed": "At least one generated valid state completed inside the supported subset and violated an assertion; inspect its counterexample trace before editing.",
            "inconclusive": "At least one run crossed an unsupported/unresolved engine boundary; no pass/fail claim is made for that run.",
        }[status],
        "warnings": index.warnings,
    }


def summary_payload(index: ScenarioIndex) -> dict[str, Any]:
    entry_status = {
        "modeled": sum(scenario["entry_script"] in index.state_index.scripts for scenario in index.scenarios.values()),
        "missing": sum(scenario["entry_script"] not in index.state_index.scripts for scenario in index.scenarios.values()),
    }
    return {
        "campaign_scenario_fuzzer_version": f"devkit.campaign-scenario-fuzzer.v{FUZZER_VERSION}",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": {
            "repo_root": str(index.root),
            "read_only": True,
            "scenario_catalog": project_relative(index.scenarios_path, index.root),
            "authoritative_layer": "literal src/scripts subset interpreted in memory",
        },
        "coverage": {
            "scenario_count": len(index.scenarios),
            "entry_scripts": entry_status,
            "supported_operations": [
                "assign/store/val integer operations", "literal comparisons and slot checks", "party/faction slots", "party AI fields", "attachment/removal", "literal call_script", "try_begin/else_try/try_end",
            ],
        },
        "next_steps": [
            "Use campaign_scenario_catalog to inspect the checked-in valid-state domains and assertions.",
            "Use campaign_scenario_fuzz with a fixed seed for deterministic reproduction of an inconclusive run or counterexample.",
            "Turn a confirmed runtime issue into an explicit Campaign State Doctor contract as well as a scenario so static and bounded execution evidence agree.",
        ],
        "warnings": index.warnings,
    }


def render_markdown(payload: Mapping[str, Any], command: str) -> str:
    if command == "summary":
        coverage = payload["coverage"]
        lines = ["# Campaign Scenario Fuzzer", "", f"- Scenarios: {coverage['scenario_count']}; modeled entry scripts: {coverage['entry_scripts']['modeled']}."]
    elif command == "fuzz":
        lines = ["# Campaign Scenario Fuzz", "", f"- {payload['scenario_id']}: {payload['status']} across {payload['iterations']} iteration(s)."]
    else:
        lines = ["# Campaign Scenario Catalog", "", f"- Scenarios: {payload['scenario_count']}."]
    if payload.get("warnings"):
        lines.extend(["", "## Boundaries", "", *(f"- {warning}" for warning in payload["warnings"])])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safe bounded campaign-state scenario fuzzer for SoD Modern.")
    parser.add_argument("command", choices=("summary", "catalog", "fuzz"), nargs="?", default="summary")
    parser.add_argument("scenario_id", nargs="?")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--scenarios", type=Path)
    parser.add_argument("--state-contracts", type=Path)
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--trace-limit", type=int, default=80)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        index = build_scenario_fuzzer(
            args.root.resolve(),
            scenarios_path=args.scenarios.resolve() if args.scenarios else None,
            state_contracts_path=args.state_contracts.resolve() if args.state_contracts else None,
        )
        if args.command == "summary":
            payload = summary_payload(index)
        elif args.command == "catalog":
            payload = scenario_catalog_payload(index, scenario_id=args.scenario_id)
        else:
            payload = fuzz_payload(index, require_query(args.scenario_id), iterations=args.iterations, seed=args.seed, trace_limit=args.trace_limit)
        if args.format == "markdown":
            sys.stdout.write(render_markdown(payload, args.command))
        else:
            sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    except ScenarioFuzzerError as error:
        print(f"campaign_scenario_fuzzer: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
