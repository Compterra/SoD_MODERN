#!/usr/bin/env python3
"""Read-only dialogue and string diagnostics for SoD Modern.

The module system evaluates dialogue candidates in file order.  This tool
parses the generated module rather than importing it, so it can report that
order without executing module-system code or requiring its Python 2-era
dependencies.
"""

from __future__ import annotations

import argparse
import ast
import bisect
import json
import re
import sys
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


TOOL_DIR = Path(__file__).resolve().parent
ROOT = TOOL_DIR.parents[1]
DEFAULT_COMPILED_DIALOGS = ROOT / "compile" / "module_dialogs.py"
SOURCE_DIALOGS = ROOT / "src" / "dialogs"

SOURCE_MARKER_RE = re.compile(
    r"^\s*#\s*\[\s*(?P<path>src/dialogs/[^:\]]+):L(?P<start>\d+)-L(?P<end>\d+)\s*\]"
)
REGISTER_RE = re.compile(r"(?<![A-Za-z0-9_])s(\d+)(?![A-Za-z0-9_])")
STRING_ID_RE = re.compile(r"(?<![A-Za-z0-9_])str_[A-Za-z0-9_]+")
UNSUPPORTED_PLACEHOLDER_RE = re.compile(r"\{s(\d+)\}")

# These are engine/UI hand-off states, rather than states that need another
# authored dialogue line.  Other target-only states remain review candidates.
ENGINE_HANDOFF_STATES = frozenset(
    {
        "close_window",
        "trade",
        "exchange_members",
        "trade_prisoners",
        "buy_mercenaries",
        "view_char",
        "training",
    }
)

# These are the initial dialogue input states recognized by M&B 1.011's
# process_dialogs.py. Any other authored input state must be produced by an
# authored route, or the exporter assigns it an invalid input-state index.
ENGINE_ENTRY_STATES = frozenset(
    {
        "start",
        "party_encounter",
        "prisoner_liberated",
        "enemy_defeated",
        "party_relieved",
        "event_triggered",
        "close_window",
        "trade",
        "exchange_members",
        "trade_prisoners",
        "buy_mercenaries",
        "view_char",
        "training",
        "member_chat",
        "prisoner_chat",
    }
)
STORE_OPERATIONS = frozenset(
    {
        "str_store_string",
        "str_store_string_reg",
        "str_store_troop_name",
        "str_store_party_name",
        "str_store_item_name",
        "str_store_agent_name",
        "str_clear",
    }
)


class InspectorError(RuntimeError):
    """A user-actionable problem while reading or rendering diagnostics."""


@dataclass(frozen=True)
class SourceLocation:
    path: str
    line_start: int
    line_end: int


@dataclass(frozen=True)
class StringStore:
    operation: str
    target: str
    block: str


@dataclass(frozen=True)
class DialogueEntry:
    index: int
    compile_line: int
    source: SourceLocation | None
    speaker: str
    start_state: str
    end_state: str
    text: str
    conditions: str
    consequences: str
    condition_operations: tuple[str, ...]
    consequence_operations: tuple[str, ...]
    string_ids: tuple[str, ...]
    string_registers: tuple[str, ...]
    string_stores: tuple[StringStore, ...]
    is_player: bool
    is_fallback: bool


@dataclass(frozen=True)
class DialogueInventory:
    compiled_path: Path
    entries: tuple[DialogueEntry, ...]
    source_is_newer: bool
    newest_source: Path | None


@dataclass(frozen=True)
class TextHit:
    layer: str
    path: str
    line: int
    text: str
    normalized_export_match: bool = False


def project_relative(path: Path, root: Path = ROOT) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_text_compatible(path: Path) -> str:
    """Read source and generated files without corrupting legacy cp1252 text."""
    last_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError as error:
            last_error = error
    raise InspectorError(f"Could not decode {path}: {last_error}")


def expression_text(node: ast.AST, raw: str) -> str:
    """Render an AST node without repeatedly rescanning the full source file.

    ``ast.get_source_segment`` splits the entire input into lines for every
    call.  A generated dialogue module has many thousands of operation tuples,
    so that otherwise convenient helper turns a linear inspection into an
    impractical one.  ``ast.unparse`` is sufficient here: this tool needs the
    referenced IDs/registers, not original comment or whitespace fidelity.
    """
    try:
        return ast.unparse(node).strip()
    except Exception:
        return "<unavailable>"


def expression_symbol(node: ast.AST, raw: str) -> str:
    """Return a stable operation/speaker spelling without evaluating it."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return f"{expression_symbol(node.left, raw)}|{expression_symbol(node.right, raw)}"
    return expression_text(node, raw)


def literal_string(node: ast.AST, raw: str) -> str:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return expression_text(node, raw)


def direct_operations(block: ast.AST, raw: str) -> tuple[str, ...]:
    if not isinstance(block, ast.List):
        return ()
    operations: list[str] = []
    for statement in block.elts:
        # M&B's Python compiler accepts both tuple and list operation literals.
        # Legacy dialogue fragments use the latter, so treating only tuples as
        # operations makes valid guarded routes look like fallbacks.
        if isinstance(statement, (ast.Tuple, ast.List)) and statement.elts:
            operations.append(expression_symbol(statement.elts[0], raw))
        # M&B also permits zero-argument and flag-qualified conditions such
        # as ``party_can_join`` and ``neg|party_can_join`` directly in the
        # list.  Preserve those guards for first-match analysis.
        elif isinstance(statement, (ast.Name, ast.BinOp)):
            operations.append(expression_symbol(statement, raw))
    return tuple(operations)


def find_string_stores(block: ast.AST, raw: str, block_name: str) -> tuple[StringStore, ...]:
    stores: list[StringStore] = []
    for node in ast.walk(block):
        if not isinstance(node, (ast.Tuple, ast.List)) or len(node.elts) < 2:
            continue
        operation = expression_symbol(node.elts[0], raw)
        if operation not in STORE_OPERATIONS:
            continue
        stores.append(
            StringStore(
                operation=operation,
                target=expression_symbol(node.elts[1], raw),
                block=block_name,
            )
        )
    return tuple(stores)


def source_markers(raw: str) -> tuple[list[int], list[SourceLocation]]:
    lines: list[int] = []
    markers: list[SourceLocation] = []
    for line_no, line in enumerate(raw.splitlines(), start=1):
        match = SOURCE_MARKER_RE.match(line)
        if match is None:
            continue
        lines.append(line_no)
        markers.append(
            SourceLocation(
                path=match.group("path"),
                line_start=int(match.group("start")),
                line_end=int(match.group("end")),
            )
        )
    return lines, markers


def marker_for_line(
    marker_lines: Sequence[int], markers: Sequence[SourceLocation], line_no: int
) -> SourceLocation | None:
    index = bisect.bisect_right(marker_lines, line_no) - 1
    if index < 0:
        return None
    return markers[index]


def dialogs_assignment(tree: ast.Module) -> ast.List:
    for statement in tree.body:
        if not isinstance(statement, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "dialogs" for target in statement.targets):
            continue
        if isinstance(statement.value, ast.List):
            return statement.value
        raise InspectorError("The generated 'dialogs' assignment is not a list.")
    raise InspectorError("Could not find a 'dialogs = [...]' assignment.")


def ordered_registers(text: str) -> tuple[str, ...]:
    numbers = {int(match.group(1)) for match in REGISTER_RE.finditer(text)}
    return tuple(f"s{number}" for number in sorted(numbers))


def parse_dialogue_entries(raw: str) -> tuple[DialogueEntry, ...]:
    """Parse generated dialogue source without importing its module dependencies."""
    try:
        tree = ast.parse(raw)
    except SyntaxError as error:
        raise InspectorError(
            f"Generated dialogue module cannot be parsed at line {error.lineno}: {error.msg}"
        ) from error

    marker_lines, markers = source_markers(raw)
    entries: list[DialogueEntry] = []
    for index, node in enumerate(dialogs_assignment(tree).elts, start=1):
        if not isinstance(node, (ast.List, ast.Tuple)) or len(node.elts) < 6:
            raise InspectorError(
                f"Dialogue entry {index} at compile line {getattr(node, 'lineno', '?')} has an unexpected shape."
            )

        speaker = expression_symbol(node.elts[0], raw)
        start_state = literal_string(node.elts[1], raw)
        conditions_node = node.elts[2]
        text = literal_string(node.elts[3], raw)
        end_state = literal_string(node.elts[4], raw)
        consequences_node = node.elts[5]
        conditions = expression_text(conditions_node, raw)
        consequences = expression_text(consequences_node, raw)
        visible_text = "\n".join((text, conditions, consequences))
        string_ids = tuple(sorted(set(STRING_ID_RE.findall(visible_text))))
        stores = find_string_stores(conditions_node, raw, "conditions") + find_string_stores(
            consequences_node, raw, "consequences"
        )
        is_fallback = isinstance(conditions_node, ast.List) and not conditions_node.elts

        entries.append(
            DialogueEntry(
                index=index,
                compile_line=getattr(node, "lineno", 0),
                source=marker_for_line(marker_lines, markers, getattr(node, "lineno", 0)),
                speaker=speaker,
                start_state=start_state,
                end_state=end_state,
                text=text,
                conditions=conditions,
                consequences=consequences,
                condition_operations=direct_operations(conditions_node, raw),
                consequence_operations=direct_operations(consequences_node, raw),
                string_ids=string_ids,
                string_registers=ordered_registers(visible_text),
                string_stores=stores,
                is_player=bool(re.search(r"(?<![A-Za-z0-9_])plyr(?![A-Za-z0-9_])", speaker)),
                is_fallback=is_fallback,
            )
        )
    return tuple(entries)


def newest_dialogue_input(root: Path) -> Path | None:
    source_root = root / "src" / "dialogs"
    candidates = list(source_root.rglob("*.py")) if source_root.exists() else []
    order = source_root / "_order_dialogs.txt"
    if order.exists():
        candidates.append(order)
    return max(candidates, key=lambda candidate: candidate.stat().st_mtime_ns, default=None)


def load_inventory(root: Path = ROOT, compiled_path: Path | None = None) -> DialogueInventory:
    compiled_path = compiled_path or root / "compile" / "module_dialogs.py"
    if not compiled_path.exists():
        raise InspectorError(
            f"Missing generated dialogue module: {project_relative(compiled_path, root)}. "
            "Run 'py -3 build\\build_dialogs.py' first."
        )
    raw = read_text_compatible(compiled_path)
    newest_source = newest_dialogue_input(root)
    source_is_newer = bool(
        newest_source is not None and newest_source.stat().st_mtime_ns > compiled_path.stat().st_mtime_ns
    )
    return DialogueInventory(
        compiled_path=compiled_path,
        entries=parse_dialogue_entries(raw),
        source_is_newer=source_is_newer,
        newest_source=newest_source,
    )


def compact(text: str, width: int = 156) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."


def source_label(entry: DialogueEntry) -> str:
    if entry.source is None:
        return "<no modular source marker>"
    return f"{entry.source.path}:L{entry.source.line_start}-L{entry.source.line_end}"


def entry_dict(entry: DialogueEntry) -> dict[str, object]:
    result = asdict(entry)
    result["source"] = asdict(entry.source) if entry.source is not None else None
    return result


def filter_entries(
    entries: Iterable[DialogueEntry], states: Sequence[str], contains: str | None, source: str | None
) -> list[DialogueEntry]:
    wanted_states = set(states)
    contains_folded = contains.casefold() if contains else None
    source_folded = source.casefold() if source else None
    selected: list[DialogueEntry] = []
    for entry in entries:
        if wanted_states and entry.start_state not in wanted_states:
            continue
        searchable = "\n".join(
            (
                entry.speaker,
                entry.start_state,
                entry.end_state,
                entry.text,
                entry.conditions,
                entry.consequences,
                source_label(entry),
            )
        ).casefold()
        if contains_folded and contains_folded not in searchable:
            continue
        if source_folded and source_folded not in source_label(entry).casefold():
            continue
        selected.append(entry)
    return selected


def output_warning(inventory: DialogueInventory) -> list[str]:
    if not inventory.source_is_newer:
        return []
    assert inventory.newest_source is not None
    return [
        "WARNING: generated dialogue order may be stale.",
        f"Newest dialogue input: {project_relative(inventory.newest_source)}",
        "Regenerate with: py -3 build\\build_dialogs.py",
        "",
    ]


def render_routes(inventory: DialogueInventory, entries: Sequence[DialogueEntry], limit: int) -> str:
    shown = entries if limit == 0 else entries[:limit]
    lines = [
        "Dialogue routes in compiled order",
        "NPC lines select the first matching route; player lines list all matching routes.",
        f"Matches: {len(entries)} of {len(inventory.entries)} total; showing: {len(shown)}.",
        "",
        *output_warning(inventory),
    ]
    if not shown:
        lines.append("No dialogue entries matched the supplied filters.")
        return "\n".join(lines)

    for entry in shown:
        role = "player choice" if entry.is_player else "NPC first-match candidate"
        lines.extend(
            (
                f"#{entry.index:04d}  {role}  {entry.speaker}",
                f"  route:  {entry.start_state} -> {entry.end_state}",
                f"  source: {source_label(entry)}  (compile line {entry.compile_line})",
                f"  text:   {compact(entry.text)}",
                "  conditions: "
                + (", ".join(entry.condition_operations) if entry.condition_operations else "<none / fallback>"),
            )
        )
        if entry.consequence_operations:
            lines.append("  consequences: " + ", ".join(entry.consequence_operations))
        if entry.string_ids:
            lines.append("  string IDs: " + ", ".join(entry.string_ids))
        if entry.string_registers:
            lines.append("  string registers: " + ", ".join(entry.string_registers))
        if entry.string_stores:
            stores = "; ".join(
                f"{store.block}: {store.operation} -> {store.target}" for store in entry.string_stores
            )
            lines.append("  string writes: " + stores)
        lines.append("")

    if len(shown) < len(entries):
        lines.append(f"{len(entries) - len(shown)} additional entries omitted; use --limit 0 to show all.")
    return "\n".join(lines)


def ordering_sensitive_fallbacks(entries: Sequence[DialogueEntry]) -> list[tuple[DialogueEntry, DialogueEntry]]:
    """Find exact speaker/state groups where a fallback makes later NPC lines unreachable."""
    groups: dict[tuple[str, str], list[DialogueEntry]] = defaultdict(list)
    for entry in entries:
        if not entry.is_player:
            groups[(entry.start_state, entry.speaker)].append(entry)

    findings: list[tuple[DialogueEntry, DialogueEntry]] = []
    for group in groups.values():
        for position, entry in enumerate(group):
            if not entry.is_fallback:
                continue
            later = next((candidate for candidate in group[position + 1 :] if not candidate.is_player), None)
            if later is not None:
                findings.append((entry, later))
    return findings


def unresolved_targets(entries: Sequence[DialogueEntry]) -> list[str]:
    input_states = {entry.start_state for entry in entries}
    targets = {entry.end_state for entry in entries}
    return sorted(targets - input_states - ENGINE_HANDOFF_STATES)


def unsupported_placeholders(entries: Sequence[DialogueEntry]) -> list[tuple[DialogueEntry, str]]:
    findings: list[tuple[DialogueEntry, str]] = []
    for entry in entries:
        examined = "\n".join((entry.text, entry.conditions, entry.consequences))
        registers = sorted(
            {int(match.group(1)) for match in UNSUPPORTED_PLACEHOLDER_RE.finditer(examined) if int(match.group(1)) >= 100}
        )
        for register in registers:
            findings.append((entry, f"s{register}"))
    return findings


def summary_payload(inventory: DialogueInventory) -> dict[str, object]:
    entries = inventory.entries
    by_state = Counter(entry.start_state for entry in entries)
    fallbacks = ordering_sensitive_fallbacks(entries)
    unresolved = unresolved_targets(entries)
    unsupported = unsupported_placeholders(entries)
    return {
        "compiled_path": project_relative(inventory.compiled_path),
        "entry_count": len(entries),
        "state_count": len(by_state),
        "source_marker_count": sum(entry.source is not None for entry in entries),
        "source_is_newer": inventory.source_is_newer,
        "newest_source": project_relative(inventory.newest_source) if inventory.newest_source else None,
        "top_states": [{"state": state, "entries": count} for state, count in by_state.most_common(20)],
        "exact_fallback_shadow_candidates": [
            {"fallback": entry_dict(fallback), "later_route": entry_dict(later)}
            for fallback, later in fallbacks
        ],
        "target_only_states_to_review": unresolved,
        "unsupported_direct_string_placeholders": [
            {"entry": entry_dict(entry), "register": register} for entry, register in unsupported
        ],
    }


def render_summary(inventory: DialogueInventory, limit: int) -> str:
    payload = summary_payload(inventory)
    lines = [
        "Dialogue Inspector summary",
        f"Compiled dialogue entries: {payload['entry_count']}",
        f"Input states: {payload['state_count']}",
        f"Entries with modular source markers: {payload['source_marker_count']}",
        "",
        *output_warning(inventory),
        "Most populated input states:",
    ]
    for item in payload["top_states"][:limit]:  # type: ignore[index]
        lines.append(f"  {item['state']}: {item['entries']}")  # type: ignore[index]

    fallback_findings = payload["exact_fallback_shadow_candidates"]  # type: ignore[index]
    lines.extend(("", "Exact fallback-shadow candidates:"))
    if not fallback_findings:
        lines.append("  none")
    else:
        for finding in fallback_findings[:limit]:
            fallback = finding["fallback"]
            later = finding["later_route"]
            lines.append(
                "  "
                + f"#{fallback['index']:04d} {fallback['start_state']} / {fallback['speaker']} "
                + f"({fallback['source']['path'] if fallback['source'] else '<no marker>'}) "
                + f"precedes #{later['index']:04d} ({later['source']['path'] if later['source'] else '<no marker>'})"
            )
        if len(fallback_findings) > limit:
            lines.append(f"  {len(fallback_findings) - limit} additional candidate(s) omitted.")
    lines.append("  A no-condition NPC line always matches; inspect these in compiled order.")

    target_only = payload["target_only_states_to_review"]  # type: ignore[index]
    lines.extend(("", "Target-only states to review (excluding engine hand-offs):"))
    lines.append("  " + (", ".join(target_only) if target_only else "none"))

    unsupported = payload["unsupported_direct_string_placeholders"]  # type: ignore[index]
    lines.extend(("", "Unsupported direct {s100+} placeholders:"))
    if unsupported:
        lines.extend(
            f"  #{finding['entry']['index']:04d}: {finding['register']}" for finding in unsupported[:limit]
        )
    else:
        lines.append("  none")
    return "\n".join(lines)


def dot_quote(value: str) -> str:
    return json.dumps(value)


def graph_selection(entries: Sequence[DialogueEntry], start_state: str | None, depth: int) -> list[DialogueEntry]:
    if start_state is None:
        return list(entries)
    adjacency: dict[str, list[DialogueEntry]] = defaultdict(list)
    for entry in entries:
        adjacency[entry.start_state].append(entry)

    selected: list[DialogueEntry] = []
    selected_indices: set[int] = set()
    seen_states = {start_state}
    frontier: deque[tuple[str, int]] = deque([(start_state, 0)])
    while frontier:
        state, distance = frontier.popleft()
        if distance >= depth:
            continue
        for entry in adjacency.get(state, []):
            if entry.index not in selected_indices:
                selected.append(entry)
                selected_indices.add(entry.index)
            if entry.end_state not in seen_states:
                seen_states.add(entry.end_state)
                frontier.append((entry.end_state, distance + 1))
    return selected


def render_dot(entries: Sequence[DialogueEntry], start_state: str | None) -> str:
    edge_counts = Counter((entry.start_state, entry.end_state) for entry in entries)
    nodes = {state for edge in edge_counts for state in edge}
    lines = [
        "digraph sod_modern_dialogue {",
        "  rankdir=LR;",
        '  graph [fontname="Segoe UI", labelloc="t", label="SoD Modern dialogue state flow"];',
        '  node [shape=box, style="rounded", fontname="Segoe UI"];',
        '  edge [fontname="Segoe UI"];',
    ]
    for node in sorted(nodes):
        attributes = ' [fillcolor="#dbeafe", style="rounded,filled"]' if node == start_state else ""
        lines.append(f"  {dot_quote(node)}{attributes};")
    for (source, target), count in sorted(edge_counts.items()):
        label = f"{count} route" if count == 1 else f"{count} routes"
        lines.append(f"  {dot_quote(source)} -> {dot_quote(target)} [label={dot_quote(label)}];")
    lines.append("}")
    return "\n".join(lines) + "\n"


def text_layers(root: Path) -> list[tuple[str, list[Path]]]:
    source_root = root / "src"
    source_files = sorted(source_root.rglob("*.py")) if source_root.exists() else []
    explicit = [
        ("generated dialogue module", root / "compile" / "module_dialogs.py"),
        ("generated strings module", root / "compile" / "module_strings.py"),
        ("exported strings", root / "_export" / "strings.txt"),
        ("exported quick strings", root / "_export" / "quick_strings.txt"),
        ("exported conversation", root / "_export" / "conversation.txt"),
    ]
    return [("modular source", source_files)] + [
        (label, [path]) for label, path in explicit if path.exists()
    ]


def search_text(
    root: Path, query: str, regex: bool, case_sensitive: bool, limit: int
) -> tuple[list[TextHit], list[str], list[str]]:
    if not query:
        raise InspectorError("Search query must not be empty.")
    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        pattern = re.compile(query if regex else re.escape(query), flags)
    except re.error as error:
        raise InspectorError(f"Invalid search expression: {error}") from error

    hits: list[TextHit] = []
    missing: list[str] = []
    truncated: list[str] = []
    for layer, paths in text_layers(root):
        if not paths:
            missing.append(layer)
        layer_hits = 0
        for path in paths:
            if limit and layer_hits >= limit:
                truncated.append(layer)
                break
            raw = read_text_compatible(path)
            for line_no, line in enumerate(raw.splitlines(), start=1):
                raw_match = pattern.search(line) is not None
                normalized_export_match = False
                if not raw_match and not regex:
                    # `strings.txt`, `quick_strings.txt`, and `conversation.txt`
                    # encode player-facing spaces as underscores.  Let a copied
                    # in-game phrase still find its exported counterpart.
                    normalized = line.replace("_", " ")
                    normalized_export_match = normalized != line and pattern.search(normalized) is not None
                if not raw_match and not normalized_export_match:
                    continue
                hits.append(
                    TextHit(
                        layer=layer,
                        path=project_relative(path, root),
                        line=line_no,
                        text=compact(line, 220),
                        normalized_export_match=normalized_export_match,
                    )
                )
                layer_hits += 1
                if limit and layer_hits >= limit:
                    truncated.append(layer)
                    break
    return hits, missing, truncated


def render_text_hits(
    query: str, hits: Sequence[TextHit], missing: Sequence[str], truncated: Sequence[str], limit: int
) -> str:
    lines = [
        f"Text search: {query!r}",
        f"Matches: {len(hits)}" + (f" (up to {limit} per layer)" if limit else ""),
        "",
    ]
    if hits:
        for hit in hits:
            suffix = " [underscore-normalized match]" if hit.normalized_export_match else ""
            lines.append(f"[{hit.layer}] {hit.path}:{hit.line}{suffix}")
            lines.append(f"  {hit.text}")
    else:
        lines.append("No matching text was found in the available layers.")
    if missing:
        lines.extend(("", "Unavailable layers: " + ", ".join(missing)))
    if truncated:
        lines.extend(("", "Layers truncated at the requested cap: " + ", ".join(dict.fromkeys(truncated))))
    return "\n".join(lines)


def resolve_output(root: Path, supplied: str) -> Path:
    target = Path(supplied)
    if not target.is_absolute():
        target = root / target
    target = target.resolve()
    export_root = (root / "_export").resolve()
    try:
        target.relative_to(export_root)
    except ValueError:
        return target
    raise InspectorError("Refusing to write a diagnostic artifact under _export/.")


def write_graph(root: Path, supplied: str, content: str) -> Path:
    target = resolve_output(root, supplied)
    if target.exists():
        raise InspectorError(
            f"Refusing to overwrite {project_relative(target, root)}. Choose a new diagnostic filename."
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def emit_json(payload: object) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def add_common_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--state", action="append", default=[], help="Exact input state to include; repeatable.")
    parser.add_argument("--contains", help="Case-insensitive text to match across route metadata and code.")
    parser.add_argument("--source", help="Case-insensitive fragment-path substring to match.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only source-to-export diagnostics for Mount & Blade 1.011 dialogues."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary = subparsers.add_parser("summary", help="Summarize dialogue order and static review candidates.")
    summary.add_argument("--limit", type=int, default=20, help="Maximum findings per section (default: 20).")
    summary.add_argument("--format", choices=("text", "json"), default="text")

    routes = subparsers.add_parser("routes", help="Show dialogue routes in their compiled engine order.")
    add_common_filters(routes)
    routes.add_argument("--limit", type=int, default=40, help="Maximum routes to show; use 0 for all.")
    routes.add_argument("--format", choices=("text", "json"), default="text")

    graph = subparsers.add_parser("graph", help="Export a state-level Graphviz DOT graph.")
    graph_group = graph.add_mutually_exclusive_group(required=True)
    graph_group.add_argument("--state", help="Start state for a bounded outgoing graph.")
    graph_group.add_argument("--all", action="store_true", help="Export the entire dialogue state graph.")
    graph.add_argument("--depth", type=int, default=2, help="Outgoing hops from --state (default: 2).")
    graph.add_argument("--output", help="Optional DOT destination; otherwise write to standard output.")

    text = subparsers.add_parser("text", help="Search source, generated, and exported string layers.")
    text.add_argument("query", help="Text or a regular expression to search for.")
    text.add_argument("--regex", action="store_true", help="Interpret query as a regular expression.")
    text.add_argument("--case-sensitive", action="store_true")
    text.add_argument("--limit", type=int, default=80, help="Maximum matches per layer; use 0 for all.")
    text.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def validate_limit(value: int, label: str) -> None:
    if value < 0:
        raise InspectorError(f"{label} must be zero or a positive integer.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "text":
            validate_limit(args.limit, "--limit")
            hits, missing, truncated = search_text(ROOT, args.query, args.regex, args.case_sensitive, args.limit)
            if args.format == "json":
                emit_json(
                    {
                        "query": args.query,
                        "hits": [asdict(hit) for hit in hits],
                        "unavailable_layers": missing,
                        "truncated_layers": list(dict.fromkeys(truncated)),
                    }
                )
            else:
                print(render_text_hits(args.query, hits, missing, truncated, args.limit))
            return 0

        inventory = load_inventory()
        if args.command == "summary":
            validate_limit(args.limit, "--limit")
            if args.format == "json":
                emit_json(summary_payload(inventory))
            else:
                print(render_summary(inventory, args.limit))
            return 0

        if args.command == "routes":
            validate_limit(args.limit, "--limit")
            entries = filter_entries(inventory.entries, args.state, args.contains, args.source)
            if args.format == "json":
                emit_json(
                    {
                        "match_count": len(entries),
                        "total_count": len(inventory.entries),
                        "entries": [entry_dict(entry) for entry in (entries if args.limit == 0 else entries[: args.limit])],
                    }
                )
            else:
                print(render_routes(inventory, entries, args.limit))
            return 0

        if args.command == "graph":
            if args.depth < 1:
                raise InspectorError("--depth must be at least 1.")
            start_state = None if args.all else args.state
            entries = graph_selection(inventory.entries, start_state, args.depth)
            rendered = render_dot(entries, start_state)
            if args.output:
                target = write_graph(ROOT, args.output, rendered)
                print(f"Wrote {project_relative(target)} ({len(entries)} dialogue route(s)).")
            else:
                print(rendered, end="")
            return 0

        raise InspectorError(f"Unknown command: {args.command}")
    except InspectorError as error:
        print(f"dialogue_inspector: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
