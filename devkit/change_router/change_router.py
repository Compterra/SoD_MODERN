#!/usr/bin/env python3
"""LLM-first source discovery, impact analysis, and guarded editing.

The Change Router is deliberately not a generic file-write surface. It indexes
the modular source tree, generated source markers, order manifests, exports,
and the Text Execution Ledger so an agent can move from a search result to the
owning fragment, its downstream evidence, a deterministic patch plan, and
bounded verification.

All edits are source-only, hash-guarded, and dry-run by default. Generated
modules and live exports are never modified by this tool.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]
if str(DEFAULT_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEFAULT_REPO_ROOT))

from devkit.string_integrity import string_integrity as integrity
from devkit.text_execution_ledger import text_execution_ledger as execution_ledger
from devkit.workspace_audit import workspace_audit


ROUTER_VERSION = "0.1.0"
CACHE_VERSION = 1
CACHE_RELATIVE_PATH = "devkit/.cache/change-router-index.v1.json"
MAX_QUERY_LENGTH = 500
MAX_EDIT_TEXT_LENGTH = 30_000
MAX_EDIT_COUNT = 20

SOURCE_AREAS = frozenset(workspace_audit.SOURCE_AREAS)
GENERATED_BY_AREA: dict[str, tuple[str, ...]] = {
    "constants": ("compile/module_constants.py", "compile/module_strings.py"),
    "dialogs": ("compile/module_dialogs.py",),
    "menus": ("compile/module_game_menus.py",),
    "mission_templates": ("compile/module_mission_templates.py",),
    "presentations": ("compile/module_presentations.py",),
    "quests": ("compile/module_quests.py",),
    "scripts": ("compile/module_scripts.py",),
    "triggers": ("compile/module_simple_triggers.py",),
}
EXPORTS_BY_AREA: dict[str, tuple[str, ...]] = {
    "constants": ("strings.txt", "quick_strings.txt"),
    "dialogs": ("conversation.txt", "dialog_states.txt"),
    "menus": ("menus.txt",),
    "mission_templates": ("mission_templates.txt",),
    "presentations": ("presentations.txt",),
    "quests": ("quests.txt",),
    "scripts": ("scripts.txt",),
    "triggers": ("simple_triggers.txt",),
}
BUILD_BY_AREA: dict[str, tuple[str, str]] = {
    "constants": ("build/build_constants.py", "compile/module_constants.py"),
    "dialogs": ("build/build_dialogs.py", "compile/module_dialogs.py"),
    "menus": ("build/build_game_menus.py", "compile/module_game_menus.py"),
    "mission_templates": (
        "build/build_mission_templates.py",
        "compile/module_mission_templates.py",
    ),
    "presentations": ("build/build_presentations.py", "compile/module_presentations.py"),
    "quests": ("build/build_quests.py", "compile/module_quests.py"),
    "scripts": ("build/build_scripts.py", "compile/module_scripts.py"),
    "triggers": ("build/build_simple_triggers.py", "compile/module_simple_triggers.py"),
}
ENTITY_ASSIGNMENTS: dict[str, tuple[str, str, str]] = {
    "menus": ("MENUS", "menu", "mnu_"),
    "mission_templates": ("MISSION_TEMPLATES", "mission_template", "mt_"),
    "presentations": ("PRESENTATIONS", "presentation", "prsnt_"),
    "quests": ("QUESTS", "quest", "qst_"),
    "scripts": ("SCRIPTS", "script", "script_"),
}
AREA_TEST_TERMS: dict[str, tuple[str, ...]] = {
    "constants": ("constant", "string"),
    "dialogs": ("dialog", "dialogue", "conversation"),
    "menus": ("menu",),
    "mission_templates": ("mission", "battle", "siege"),
    "presentations": ("presentation",),
    "quests": ("quest",),
    "scripts": ("script",),
    "triggers": ("trigger",),
}

SOURCE_MARKER_RE = re.compile(
    r"(?m)^\s*#\s*\[\s*(?P<path>src/[^\]\r\n:]+)"
    r"(?::L(?P<start>\d+)(?:-L(?P<end>\d+))?)?\s*\]"
)
TOKEN_RE = re.compile(
    r"\$[A-Za-z_][A-Za-z0-9_]*|"
    r":[A-Za-z_][A-Za-z0-9_]*|"
    r"\b(?:s\d+|reg\d+)\b|"
    r"\b[A-Za-z_][A-Za-z0-9_]*\b"
)
SYMBOL_RE = re.compile(
    r"\$[A-Za-z_][A-Za-z0-9_]*|"
    r":[A-Za-z_][A-Za-z0-9_]*|"
    r"\b(?:s\d+|reg\d+|script_[A-Za-z0-9_]+|mnu_[A-Za-z0-9_]+|"
    r"str_[A-Za-z0-9_]+|qst_[A-Za-z0-9_]+|mt_[A-Za-z0-9_]+|"
    r"prsnt_[A-Za-z0-9_]+)\b"
)
STEM_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9]{2,}")


class ChangeRouterError(RuntimeError):
    """A requested route, patch, or verification cannot be completed safely."""


@dataclass(frozen=True)
class SourceFragment:
    """Immutable metadata for a source fragment or generated preamble."""

    path: str
    area: str
    sha256: str
    mtime_ns: int
    size: int
    line_count: int
    tokens: tuple[str, ...]
    syntax_error: str | None
    order_position: int | None
    order_policy: str | None
    kind: str

    @property
    def id(self) -> str:
        return f"source:{self.path}"


@dataclass(frozen=True)
class GeneratedSegment:
    """A generated source range attributed to a modular source fragment."""

    source_path: str
    compile_path: str
    compile_line_start: int
    compile_line_end: int
    source_line_start: int | None
    source_line_end: int | None


@dataclass(frozen=True)
class PlannedEdit:
    old_text: str
    new_text: str
    occurrence: int
    expected_occurrences: int
    start: int
    end: int
    line_start: int
    line_end: int

    def payload(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("start", None)
        data.pop("end", None)
        return data


@dataclass
class RouterIndex:
    root: Path
    signature: tuple[tuple[str, int, int], ...]
    fragments: dict[str, SourceFragment]
    token_paths: dict[str, tuple[str, ...]]
    ordering: dict[str, list[str]]
    generated_by_source: dict[str, list[GeneratedSegment]]
    generated_signatures: dict[str, tuple[int, int]]
    warnings: list[str]
    cache_status: str
    ledger: execution_ledger.LedgerIndex | None = None
    records_by_source: dict[str, list[execution_ledger.OperationRecord]] | None = None
    sinks_by_source: dict[str, list[dict[str, Any]]] | None = None
    script_callers: dict[str, list[execution_ledger.OperationRecord]] | None = None


_CACHE: dict[Path, tuple[tuple[tuple[str, int, int], ...], RouterIndex]] = {}


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_text_with_encoding(path: Path) -> tuple[str, str, bytes]:
    try:
        raw_bytes = path.read_bytes()
    except OSError as error:
        raise ChangeRouterError(f"Could not read {path}: {error}") from error
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw_bytes.decode(encoding), encoding, raw_bytes
        except UnicodeDecodeError:
            continue
    raise ChangeRouterError(f"Could not decode {path}.")


def source_file_paths(root: Path) -> list[Path]:
    source_root = root / "src"
    if not source_root.is_dir():
        raise ChangeRouterError(f"Missing source directory: {source_root}")
    return sorted(
        (path for path in source_root.rglob("*.py") if path.is_file()),
        key=lambda path: path.as_posix().lower(),
    )


def generated_paths(root: Path) -> list[Path]:
    relative_paths = sorted(
        {relative for values in GENERATED_BY_AREA.values() for relative in values},
        key=str.lower,
    )
    return [root / relative for relative in relative_paths if (root / relative).is_file()]


def order_manifest_paths(root: Path) -> list[Path]:
    source_root = root / "src"
    if not source_root.is_dir():
        return []
    return sorted(
        (path for path in source_root.rglob("_order*.txt") if path.is_file()),
        key=lambda path: path.as_posix().lower(),
    )


def file_signature(path: Path, root: Path) -> tuple[str, int, int]:
    try:
        stat = path.stat()
    except OSError:
        return (project_relative(path, root), -1, -1)
    return (project_relative(path, root), stat.st_mtime_ns, stat.st_size)


def workspace_signature(root: Path, paths: Sequence[Path] | None = None) -> tuple[tuple[str, int, int], ...]:
    if paths is None:
        paths = [
            *source_file_paths(root),
            *generated_paths(root),
            *order_manifest_paths(root),
        ]
    return tuple(file_signature(path, root) for path in paths)


def cache_path(root: Path) -> Path:
    return root / CACHE_RELATIVE_PATH


def load_disk_cache(root: Path) -> dict[str, Any] | None:
    path = cache_path(root)
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if payload.get("cache_version") != CACHE_VERSION:
        return None
    return payload


def write_disk_cache(
    root: Path,
    fragments: dict[str, SourceFragment],
    generated_segments: dict[str, list[GeneratedSegment]],
    generated_signatures: dict[str, tuple[int, int]],
) -> None:
    path = cache_path(root)
    payload = {
        "cache_version": CACHE_VERSION,
        "fragments": {
            relative: {
                **asdict(fragment),
                "tokens": list(fragment.tokens),
            }
            for relative, fragment in fragments.items()
        },
        "generated_segments": {
            source: [asdict(segment) for segment in segments]
            for source, segments in generated_segments.items()
        },
        "generated_signatures": {
            relative: list(signature)
            for relative, signature in generated_signatures.items()
        },
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f"{path.name}.tmp")
        temporary.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
    except OSError:
        # Index persistence is an acceleration only. Diagnostics remain valid
        # when a workspace is read-only or another process has the cache open.
        return


def source_area(relative_path: str) -> str:
    parts = Path(relative_path).parts
    if len(parts) >= 2 and parts[0] == "src":
        return parts[1]
    return "unknown"


def source_kind(relative_path: str) -> str:
    parts = Path(relative_path).parts
    if "_preamble" in parts:
        return "preamble"
    if Path(relative_path).name == "__init__.py":
        return "package_initializer"
    return "fragment"


def token_set(raw: str) -> tuple[str, ...]:
    tokens = {
        token.casefold()
        for token in TOKEN_RE.findall(raw)
        if len(token) >= 2 and not token.startswith("__")
    }
    return tuple(sorted(tokens))


def fragment_from_file(
    root: Path,
    path: Path,
    *,
    order_position: int | None = None,
    order_policy: str | None = None,
) -> SourceFragment:
    raw, _, raw_bytes = read_text_with_encoding(path)
    syntax_error: str | None = None
    try:
        ast.parse(raw, filename=str(path))
    except SyntaxError as error:
        syntax_error = f"{error.msg} at line {error.lineno}, column {error.offset}"
    stat = path.stat()
    relative = project_relative(path, root)
    return SourceFragment(
        path=relative,
        area=source_area(relative),
        sha256=hashlib.sha256(raw_bytes).hexdigest(),
        mtime_ns=stat.st_mtime_ns,
        size=stat.st_size,
        line_count=raw.count("\n") + (1 if raw else 0),
        tokens=token_set(raw),
        syntax_error=syntax_error,
        order_position=order_position,
        order_policy=order_policy,
        kind=source_kind(relative),
    )


def source_ordering(root: Path, paths: Sequence[Path]) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Return deterministic fragment order plus the policy that supplied it."""

    fragments_by_area: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        relative = project_relative(path, root)
        # Preambles are injected by individual builders, not part of the
        # ordinary fragment manifests. Keeping them searchable but outside the
        # entity order avoids inventing a misleading position for every normal
        # dialogue/menu/script fragment.
        if source_kind(relative) == "fragment":
            fragments_by_area[source_area(relative)].append(relative)
    for values in fragments_by_area.values():
        values.sort(key=str.lower)

    ordered: dict[str, list[str]] = {}
    policies: dict[str, str] = {}
    for area, candidates in fragments_by_area.items():
        source_root = root / "src" / area
        preferred: list[str] = []
        seen: set[str] = set()
        for spec in workspace_audit.ORDER_SPECS:
            if spec["source_area"] != area:
                continue
            policy = str(spec.get("policy") or "")
            policies.setdefault(area, policy)
            order_file = root / str(spec["order_file"])
            prefix = str(spec.get("path_prefix") or "").replace("\\", "/")
            for entry in workspace_audit.read_order_entries(order_file):
                normalized = entry.replace("\\", "/")
                if prefix and not normalized.startswith(prefix):
                    continue
                relative = (source_root / normalized).relative_to(root).as_posix()
                if relative in candidates and relative not in seen:
                    seen.add(relative)
                    preferred.append(relative)
        remaining = [path for path in candidates if path not in seen]
        ordered[area] = [*preferred, *remaining]
    return ordered, policies


def cached_fragment(
    cached: dict[str, Any] | None,
    *,
    path: str,
    mtime_ns: int,
    size: int,
    order_position: int | None,
    order_policy: str | None,
) -> SourceFragment | None:
    if not cached:
        return None
    item = cached.get(path)
    if not isinstance(item, dict):
        return None
    if item.get("mtime_ns") != mtime_ns or item.get("size") != size:
        return None
    try:
        return SourceFragment(
            path=path,
            area=str(item["area"]),
            sha256=str(item["sha256"]),
            mtime_ns=mtime_ns,
            size=size,
            line_count=int(item["line_count"]),
            tokens=tuple(str(token) for token in item.get("tokens", [])),
            syntax_error=item.get("syntax_error"),
            order_position=order_position,
            order_policy=order_policy,
            kind=str(item.get("kind") or source_kind(path)),
        )
    except (KeyError, TypeError, ValueError):
        return None


def build_fragments(
    root: Path,
    paths: Sequence[Path],
    cached_files: dict[str, Any] | None,
) -> tuple[dict[str, SourceFragment], dict[str, list[str]], str]:
    ordering, policies = source_ordering(root, paths)
    order_positions = {
        path: position
        for area, entries in ordering.items()
        for position, path in enumerate(entries, start=1)
    }
    fragments: dict[str, SourceFragment] = {}
    reused = 0
    for path in paths:
        relative = project_relative(path, root)
        stat = path.stat()
        area = source_area(relative)
        fragment = cached_fragment(
            cached_files,
            path=relative,
            mtime_ns=stat.st_mtime_ns,
            size=stat.st_size,
            order_position=order_positions.get(relative),
            order_policy=policies.get(area),
        )
        if fragment is None:
            fragment = fragment_from_file(
                root,
                path,
                order_position=order_positions.get(relative),
                order_policy=policies.get(area),
            )
        else:
            reused += 1
        fragments[relative] = fragment
    status = (
        "persistent-cache-hit"
        if fragments and reused == len(fragments)
        else "persistent-cache-partial" if reused else "rebuilt"
    )
    return fragments, ordering, status


def generated_signature_map(root: Path, paths: Sequence[Path]) -> dict[str, tuple[int, int]]:
    result: dict[str, tuple[int, int]] = {}
    for path in paths:
        stat = path.stat()
        result[project_relative(path, root)] = (stat.st_mtime_ns, stat.st_size)
    return result


def parse_generated_segments(root: Path, paths: Sequence[Path]) -> dict[str, list[GeneratedSegment]]:
    by_source: dict[str, list[GeneratedSegment]] = defaultdict(list)
    for path in paths:
        raw, _, _ = read_text_with_encoding(path)
        markers: list[tuple[int, re.Match[str]]] = []
        for match in SOURCE_MARKER_RE.finditer(raw):
            markers.append((raw.count("\n", 0, match.start()) + 1, match))
        if not markers:
            continue
        line_count = raw.count("\n") + (1 if raw else 0)
        relative_compile = project_relative(path, root)
        for index, (compile_start, match) in enumerate(markers):
            source = match.group("path").replace("\\", "/")
            next_start = markers[index + 1][0] if index + 1 < len(markers) else line_count + 1
            by_source[source].append(
                GeneratedSegment(
                    source_path=source,
                    compile_path=relative_compile,
                    compile_line_start=compile_start,
                    compile_line_end=max(compile_start, next_start - 1),
                    source_line_start=(
                        int(match.group("start")) if match.group("start") else None
                    ),
                    source_line_end=(
                        int(match.group("end")) if match.group("end") else None
                    ),
                )
            )
    return {
        source: sorted(
            segments,
            key=lambda segment: (
                segment.compile_path,
                segment.compile_line_start,
                segment.compile_line_end,
            ),
        )
        for source, segments in by_source.items()
    }


def cached_generated_segments(
    payload: dict[str, Any] | None,
    signatures: dict[str, tuple[int, int]],
) -> dict[str, list[GeneratedSegment]] | None:
    if not payload:
        return None
    raw_signatures = payload.get("generated_signatures")
    if not isinstance(raw_signatures, dict):
        return None
    normalized = {
        str(path): tuple(value)
        for path, value in raw_signatures.items()
        if isinstance(value, list) and len(value) == 2
    }
    if normalized != signatures:
        return None
    raw_segments = payload.get("generated_segments")
    if not isinstance(raw_segments, dict):
        return None
    result: dict[str, list[GeneratedSegment]] = {}
    try:
        for source, entries in raw_segments.items():
            result[str(source)] = [GeneratedSegment(**entry) for entry in entries]
    except (TypeError, ValueError):
        return None
    return result


def build_change_router(root: Path = DEFAULT_REPO_ROOT) -> RouterIndex:
    """Build or reuse the source/link index without executing module code."""

    root = root.resolve()
    if not (root / "src").is_dir() or not (root / "compile").is_dir():
        raise ChangeRouterError(f"Not a recognizable SoD Modern workspace: {root}")
    sources = source_file_paths(root)
    generated = generated_paths(root)
    signature = workspace_signature(
        root,
        [*sources, *generated, *order_manifest_paths(root)],
    )
    cached = _CACHE.get(root)
    if cached is not None and cached[0] == signature:
        return cached[1]

    disk_cache = load_disk_cache(root)
    cache_files = disk_cache.get("fragments") if disk_cache else None
    fragments, ordering, cache_status = build_fragments(root, sources, cache_files)
    token_paths: dict[str, list[str]] = defaultdict(list)
    for fragment in fragments.values():
        for token in fragment.tokens:
            token_paths[token].append(fragment.path)
    normalized_tokens = {
        token: tuple(sorted(paths, key=str.lower))
        for token, paths in token_paths.items()
    }
    signatures = generated_signature_map(root, generated)
    segments = cached_generated_segments(disk_cache, signatures)
    if segments is None:
        segments = parse_generated_segments(root, generated)
        if cache_status == "persistent-cache-hit":
            cache_status = "persistent-cache-generated-refresh"
    warnings: list[str] = [
        (
            "Change Router links modular source to generated markers and static "
            "execution evidence; it does not infer runtime game state."
        )
    ]
    missing_generated = [
        relative
        for area in SOURCE_AREAS
        for relative in GENERATED_BY_AREA.get(area, ())
        if not (root / relative).is_file()
    ]
    if missing_generated:
        warnings.append(
            "Some generated modules are unavailable; related generated links may be incomplete."
        )
    router = RouterIndex(
        root=root,
        signature=signature,
        fragments=fragments,
        token_paths=normalized_tokens,
        ordering=ordering,
        generated_by_source=segments,
        generated_signatures=signatures,
        warnings=warnings,
        cache_status=cache_status,
    )
    write_disk_cache(root, fragments, segments, signatures)
    _CACHE[root] = (signature, router)
    return router


def invalidate_router(root: Path) -> None:
    _CACHE.pop(root.resolve(), None)


def require_limit(value: int, *, name: str = "limit", maximum: int = 100) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise ChangeRouterError(f"{name} must be an integer from 1 through {maximum}.")
    return value


def require_query(query: str) -> str:
    if not isinstance(query, str) or not query.strip():
        raise ChangeRouterError("query must not be empty.")
    if len(query) > MAX_QUERY_LENGTH:
        raise ChangeRouterError(f"query must be at most {MAX_QUERY_LENGTH} characters.")
    return query.strip()


def require_scope(scope: str) -> str:
    if scope not in {"all", "source", "generated", "export"}:
        raise ChangeRouterError("scope must be one of: all, source, generated, export.")
    return scope


def router_summary(router: RouterIndex) -> dict[str, Any]:
    area_counts = Counter(fragment.area for fragment in router.fragments.values())
    syntax_errors = [
        fragment.path
        for fragment in router.fragments.values()
        if fragment.syntax_error is not None
    ]
    linked_source_count = sum(
        1 for source in router.generated_by_source if source in router.fragments
    )
    return {
        "router_version": f"devkit.change-router.v{ROUTER_VERSION}",
        "source_fragment_count": len(router.fragments),
        "source_fragment_count_by_area": dict(sorted(area_counts.items())),
        "indexed_token_count": len(router.token_paths),
        "generated_module_count": len(router.generated_signatures),
        "generated_segment_count": sum(
            len(segments) for segments in router.generated_by_source.values()
        ),
        "source_to_generated_linked_fragment_count": linked_source_count,
        "source_syntax_error_count": len(syntax_errors),
        "source_syntax_error_paths": syntax_errors[:20],
        "cache_status": router.cache_status,
    }


def target_fragment(router: RouterIndex, target_id: str) -> SourceFragment:
    if not isinstance(target_id, str) or not target_id.startswith("source:"):
        raise ChangeRouterError("target_id must be a source ID returned by code_find.")
    relative = target_id.removeprefix("source:").replace("\\", "/")
    fragment = router.fragments.get(relative)
    if fragment is None:
        raise ChangeRouterError(f"Unknown source target: {target_id}")
    return fragment


def source_path(router: RouterIndex, fragment: SourceFragment) -> Path:
    path = (router.root / fragment.path).resolve()
    source_root = (router.root / "src").resolve()
    try:
        path.relative_to(source_root)
    except ValueError as error:
        raise ChangeRouterError("Refusing a target outside src/.") from error
    if path.suffix.lower() != ".py":
        raise ChangeRouterError("Change Router only edits Python source fragments.")
    return path


def query_tokens(query: str) -> list[str]:
    tokens = [token.casefold() for token in TOKEN_RE.findall(query)]
    if tokens:
        return list(dict.fromkeys(tokens))
    fallback = query.casefold().strip()
    return [fallback] if fallback else []


def candidate_sources(router: RouterIndex, query: str) -> tuple[list[str], bool]:
    tokens = query_tokens(query)
    postings = [set(router.token_paths.get(token, ())) for token in tokens]
    postings = [posting for posting in postings if posting]
    if not postings:
        return list(router.fragments), False
    intersection = set.intersection(*postings)
    if intersection:
        return sorted(intersection, key=str.lower), False
    union = set().union(*postings)
    paths = sorted(union, key=str.lower)
    return paths[:2_000], len(paths) > 2_000


def line_hits(raw: str, query: str) -> list[tuple[int, str, int]]:
    needle = query.casefold()
    terms = query_tokens(query)
    hits: list[tuple[int, str, int]] = []
    for number, line in enumerate(raw.splitlines(), start=1):
        lowered = line.casefold()
        if needle in lowered:
            score = 100 + min(50, lowered.count(needle) * 5)
        else:
            matched = sum(term in lowered for term in terms)
            if not matched:
                continue
            score = matched * 12
        snippet = line.strip()
        if len(snippet) > 300:
            snippet = snippet[:297] + "..."
        hits.append((number, snippet, score))
    return hits


def fragment_hit(router: RouterIndex, fragment: SourceFragment, line: int, snippet: str, score: int) -> dict[str, Any]:
    return {
        "kind": "source",
        "target_id": fragment.id,
        "path": fragment.path,
        "line": line,
        "snippet": snippet,
        "score": score,
        "area": fragment.area,
        "order_position": fragment.order_position,
        "generated_link_count": len(router.generated_by_source.get(fragment.path, ())),
    }


def source_search(router: RouterIndex, query: str, limit: int) -> tuple[list[dict[str, Any]], int, bool]:
    candidates, candidate_truncated = candidate_sources(router, query)
    results: list[dict[str, Any]] = []
    total = 0
    for relative in candidates:
        fragment = router.fragments[relative]
        raw, _, _ = read_text_with_encoding(source_path(router, fragment))
        for line, snippet, score in line_hits(raw, query):
            total += 1
            results.append(fragment_hit(router, fragment, line, snippet, score))
    results.sort(key=lambda result: (-int(result["score"]), str(result["path"]).lower(), int(result["line"])))
    return results[:limit], total, candidate_truncated or len(results) > limit


def segment_for_generated_line(
    router: RouterIndex,
    compile_path: str,
    line: int,
) -> GeneratedSegment | None:
    for segments in router.generated_by_source.values():
        for segment in segments:
            if (
                segment.compile_path == compile_path
                and segment.compile_line_start <= line <= segment.compile_line_end
            ):
                return segment
    return None


def generated_search(router: RouterIndex, query: str, limit: int) -> tuple[list[dict[str, Any]], int, bool]:
    results: list[dict[str, Any]] = []
    total = 0
    for path in generated_paths(router.root):
        raw, _, _ = read_text_with_encoding(path)
        relative = project_relative(path, router.root)
        for line, snippet, score in line_hits(raw, query):
            total += 1
            segment = segment_for_generated_line(router, relative, line)
            result: dict[str, Any] = {
                "kind": "generated",
                "target_id": (
                    f"source:{segment.source_path}" if segment and segment.source_path in router.fragments else None
                ),
                "path": relative,
                "line": line,
                "snippet": snippet,
                "score": score,
                "source": (
                    {
                        "path": segment.source_path,
                        "line_start": segment.source_line_start,
                        "line_end": segment.source_line_end,
                    }
                    if segment
                    else None
                ),
            }
            results.append(result)
    results.sort(key=lambda result: (-int(result["score"]), str(result["path"]).lower(), int(result["line"])))
    return results[:limit], total, len(results) > limit


def export_paths(root: Path) -> list[Path]:
    names = {spec["filename"] for spec in workspace_audit.EXPORT_SPECS}
    names.update({"strings.txt", "quick_strings.txt"})
    return [
        root / "_export" / name
        for name in sorted(names, key=str.lower)
        if (root / "_export" / name).is_file()
    ]


def export_search(router: RouterIndex, query: str, limit: int) -> tuple[list[dict[str, Any]], int, bool]:
    results: list[dict[str, Any]] = []
    total = 0
    for path in export_paths(router.root):
        raw, _, _ = read_text_with_encoding(path)
        relative = project_relative(path, router.root)
        for line, snippet, score in line_hits(raw, query):
            total += 1
            results.append(
                {
                    "kind": "export",
                    "target_id": None,
                    "path": relative,
                    "line": line,
                    "snippet": snippet,
                    "score": score,
                }
            )
    results.sort(key=lambda result: (-int(result["score"]), str(result["path"]).lower(), int(result["line"])))
    return results[:limit], total, len(results) > limit


def code_find(
    router: RouterIndex,
    query: str,
    *,
    scope: str = "all",
    limit: int = 20,
) -> dict[str, Any]:
    """Find code/text with source IDs that can feed the linked tools."""

    checked_query = require_query(query)
    checked_scope = require_scope(scope)
    maximum = require_limit(limit)
    groups: list[tuple[str, list[dict[str, Any]], int, bool]] = []
    if checked_scope in {"all", "source"}:
        results, total, truncated = source_search(router, checked_query, maximum)
        groups.append(("source", results, total, truncated))
    if checked_scope in {"all", "generated"}:
        results, total, truncated = generated_search(router, checked_query, maximum)
        groups.append(("generated", results, total, truncated))
    if checked_scope in {"all", "export"}:
        results, total, truncated = export_search(router, checked_query, maximum)
        groups.append(("export", results, total, truncated))
    matches = [result for _, results, _, _ in groups for result in results]
    matches.sort(key=lambda result: (-int(result["score"]), str(result["path"]).lower(), int(result["line"])))
    returned = matches[:maximum]
    total = sum(group_total for _, _, group_total, _ in groups)
    return {
        "summary": router_summary(router),
        "query": checked_query,
        "scope": checked_scope,
        "match_count": total,
        "returned_count": len(returned),
        "truncated": any(group_truncated for _, _, _, group_truncated in groups) or len(matches) > maximum,
        "matches": returned,
        "warnings": router.warnings,
    }


def source_excerpt(
    router: RouterIndex,
    fragment: SourceFragment,
    *,
    focus_line: int | None,
    max_lines: int,
) -> dict[str, Any]:
    maximum = require_limit(max_lines, name="max_lines", maximum=400)
    raw, _, _ = read_text_with_encoding(source_path(router, fragment))
    lines = raw.splitlines()
    if focus_line is not None:
        if isinstance(focus_line, bool) or not isinstance(focus_line, int) or focus_line < 1:
            raise ChangeRouterError("focus_line must be a positive integer when supplied.")
        center = min(focus_line, max(1, len(lines)))
        start = max(1, center - maximum // 2)
    else:
        start = 1
    end = min(len(lines), start + maximum - 1)
    if end - start + 1 < maximum and start > 1:
        start = max(1, end - maximum + 1)
    return {
        "line_start": start,
        "line_end": end,
        "line_count": len(lines),
        "truncated": end - start + 1 < len(lines),
        "lines": [
            {"line": number, "text": lines[number - 1]}
            for number in range(start, end + 1)
        ],
    }


def declared_entities(fragment: SourceFragment, raw: str) -> list[dict[str, str]]:
    """Extract module-system entity IDs without importing a fragment."""

    entities: set[tuple[str, str]] = set()
    assignment = ENTITY_ASSIGNMENTS.get(fragment.area)
    try:
        tree = ast.parse(raw)
    except SyntaxError:
        return []
    if assignment is not None:
        variable, kind, prefix = assignment
        for statement in tree.body:
            if not isinstance(statement, ast.Assign):
                continue
            if not any(
                isinstance(target, ast.Name) and target.id == variable
                for target in statement.targets
            ):
                continue
            if not isinstance(statement.value, ast.List):
                continue
            for entry in statement.value.elts:
                if (
                    isinstance(entry, (ast.Tuple, ast.List))
                    and entry.elts
                    and isinstance(entry.elts[0], ast.Constant)
                    and isinstance(entry.elts[0].value, str)
                ):
                    value = entry.elts[0].value
                    symbol = value if value.startswith(prefix) else f"{prefix}{value}"
                    entities.add((kind, symbol))
    if fragment.area == "dialogs":
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Tuple, ast.List)) or len(node.elts) < 5:
                continue
            for index in (1, 4):
                candidate = node.elts[index]
                if isinstance(candidate, ast.Constant) and isinstance(candidate.value, str):
                    value = candidate.value
                    if value:
                        entities.add(("dialogue_state", value))
    return [
        {"kind": kind, "symbol": symbol}
        for kind, symbol in sorted(entities, key=lambda item: (item[0], item[1]))
    ]


def direct_symbols(raw: str, maximum: int) -> list[dict[str, Any]]:
    counts = Counter(symbol for symbol in SYMBOL_RE.findall(raw))
    return [
        {"symbol": symbol, "occurrences": count}
        for symbol, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:maximum]
    ]


def order_payload(router: RouterIndex, fragment: SourceFragment, neighbor_count: int = 3) -> dict[str, Any]:
    entries = router.ordering.get(fragment.area, [])
    try:
        index = entries.index(fragment.path)
    except ValueError:
        index = -1
    if index < 0:
        return {
            "area": fragment.area,
            "position": None,
            "policy": fragment.order_policy,
            "listed": False,
            "previous": [],
            "next": [],
        }
    return {
        "area": fragment.area,
        "position": index + 1,
        "total": len(entries),
        "policy": fragment.order_policy,
        "listed": True,
        "previous": entries[max(0, index - neighbor_count):index],
        "next": entries[index + 1:index + 1 + neighbor_count],
    }


def generated_links_payload(router: RouterIndex, fragment: SourceFragment) -> list[dict[str, Any]]:
    return [
        {
            "compile_path": segment.compile_path,
            "compile_line_start": segment.compile_line_start,
            "compile_line_end": segment.compile_line_end,
            "source_line_start": segment.source_line_start,
            "source_line_end": segment.source_line_end,
        }
        for segment in router.generated_by_source.get(fragment.path, [])
    ]


def export_layers(fragment: SourceFragment) -> list[dict[str, Any]]:
    return [
        {
            "path": f"_export/{name}",
            "role": "generated-export",
            "becomes_stale_after_source_edit": True,
        }
        for name in EXPORTS_BY_AREA.get(fragment.area, ())
    ]


def ensure_execution_index(router: RouterIndex) -> execution_ledger.LedgerIndex:
    if router.ledger is None:
        try:
            router.ledger = execution_ledger.build_ledger(router.root)
        except (
            execution_ledger.LedgerError,
            integrity.StringIntegrityError,
        ) as error:
            raise ChangeRouterError(f"Could not build linked execution evidence: {error}") from error
    if router.records_by_source is not None:
        return router.ledger

    records_by_source: dict[str, list[execution_ledger.OperationRecord]] = defaultdict(list)
    script_callers: dict[str, list[execution_ledger.OperationRecord]] = defaultdict(list)
    for module in router.ledger.modules.values():
        for block in module.blocks.values():
            for record in block.operations:
                if record.source and record.source.get("path"):
                    records_by_source[str(record.source["path"])].append(record)
                if (
                    execution_ledger.base_operation(record.name) == "call_script"
                    and record.args
                    and record.args[0].startswith("script_")
                ):
                    script_callers[record.args[0]].append(record)
    sinks_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for sink in router.ledger.integrity_report["sinks"]:
        source = sink.get("source")
        if source and source.get("path"):
            sinks_by_source[str(source["path"])].append(sink)
    router.records_by_source = {
        source: sorted(
            values,
            key=lambda record: (
                record.module_path,
                record.compile_line,
                record.column,
            ),
        )
        for source, values in records_by_source.items()
    }
    router.sinks_by_source = {
        source: sorted(
            values,
            key=lambda sink: (
                sink["compile_path"],
                sink["compile_line"],
                sink.get("compile_column") or 0,
            ),
        )
        for source, values in sinks_by_source.items()
    }
    router.script_callers = {
        symbol: sorted(
            values,
            key=lambda record: (
                record.module_path,
                record.compile_line,
                record.column,
            ),
        )
        for symbol, values in script_callers.items()
    }
    return router.ledger


def operation_record_payload(record: execution_ledger.OperationRecord) -> dict[str, Any]:
    return execution_ledger.operation_payload(record)


def script_symbols_from_records(
    records: Sequence[execution_ledger.OperationRecord],
) -> list[str]:
    symbols: set[str] = set()
    for record in records:
        if execution_ledger.base_operation(record.name) == "call_script" and record.args:
            candidate = record.args[0]
            if candidate.startswith("script_"):
                symbols.add(candidate)
    return sorted(symbols)


def relevant_source_fragments(
    router: RouterIndex,
    fragment: SourceFragment,
    symbols: Iterable[str],
    *,
    limit: int,
) -> tuple[list[dict[str, Any]], int]:
    related: dict[str, set[str]] = defaultdict(set)
    for symbol in symbols:
        alternatives = {symbol.casefold()}
        for prefix in ("script_", "mnu_", "str_", "qst_", "mt_", "prsnt_"):
            if symbol.startswith(prefix):
                alternatives.add(symbol.removeprefix(prefix).casefold())
        for token in alternatives:
            for path in router.token_paths.get(token, ()):
                if path != fragment.path:
                    related[path].add(symbol)
    payload = [
        {
            "target_id": f"source:{path}",
            "path": path,
            "area": router.fragments[path].area,
            "shared_symbols": sorted(symbols),
        }
        for path, symbols in related.items()
        if path in router.fragments
    ]
    payload.sort(
        key=lambda item: (
            -len(item["shared_symbols"]),
            str(item["path"]).lower(),
        )
    )
    return payload[:limit], len(payload)


def source_relationships(
    router: RouterIndex,
    fragment: SourceFragment,
    entities: Sequence[dict[str, str]],
    *,
    related_limit: int,
) -> dict[str, Any]:
    ledger = ensure_execution_index(router)
    assert router.records_by_source is not None
    assert router.sinks_by_source is not None
    assert router.script_callers is not None
    records = router.records_by_source.get(fragment.path, [])
    source_sinks = router.sinks_by_source.get(fragment.path, [])
    called_scripts = script_symbols_from_records(records)
    declared_scripts = [
        item["symbol"]
        for item in entities
        if item["kind"] == "script"
    ]
    called_by = [
        record
        for symbol in declared_scripts
        for record in router.script_callers.get(symbol, [])
    ]
    reads = sorted({symbol for record in records for symbol in record.reads})
    writes = sorted({symbol for record in records for symbol in record.writes})
    globals_read = [symbol for symbol in reads if symbol.startswith("$")]
    globals_written = [symbol for symbol in writes if symbol.startswith("$")]
    register_reads = [
        symbol
        for symbol in reads
        if symbol.startswith("s") or symbol.startswith("reg") or symbol.startswith(":")
    ]
    register_writes = [
        symbol
        for symbol in writes
        if symbol.startswith("s") or symbol.startswith("reg") or symbol.startswith(":")
    ]
    transitions = [
        record
        for record in records
        if record.category == "transition"
    ]
    anchor_symbols = {
        *called_scripts,
        *declared_scripts,
        *globals_read,
        *globals_written,
        *register_reads,
        *register_writes,
        *(
            item["symbol"]
            for item in entities
            if item["kind"] in {"menu", "quest", "mission_template", "presentation"}
        ),
    }
    related, total_related = relevant_source_fragments(
        router,
        fragment,
        anchor_symbols,
        limit=related_limit,
    )
    return {
        "source_mapped_operation_count": len(records),
        "operations": [operation_record_payload(record) for record in records[:related_limit]],
        "operations_truncated": len(records) > related_limit,
        "called_scripts": called_scripts[:related_limit],
        "called_scripts_truncated": len(called_scripts) > related_limit,
        "called_by": [
            operation_record_payload(record)
            for record in called_by[:related_limit]
        ],
        "called_by_count": len(called_by),
        "called_by_truncated": len(called_by) > related_limit,
        "globals": {
            "reads": globals_read[:related_limit],
            "writes": globals_written[:related_limit],
        },
        "registers": {
            "reads": register_reads[:related_limit],
            "writes": register_writes[:related_limit],
        },
        "visible_text_sinks": [
            {
                "sink_id": sink["id"],
                "kind": sink["kind"],
                "status": sink["status"],
                "compile_path": sink["compile_path"],
                "compile_line": sink["compile_line"],
                "text_input": sink["text_input"],
            }
            for sink in source_sinks[:related_limit]
        ],
        "visible_text_sink_count": len(source_sinks),
        "visible_text_sinks_truncated": len(source_sinks) > related_limit,
        "menu_transitions": [
            operation_record_payload(record)
            for record in transitions[:related_limit]
        ],
        "menu_transition_count": len(transitions),
        "related_source_fragments": related,
        "related_source_fragment_count": total_related,
        "related_source_fragments_truncated": total_related > related_limit,
        "execution_ledger_summary": execution_ledger.ledger_summary(ledger),
    }


def test_candidates(
    router: RouterIndex,
    fragment: SourceFragment,
    *,
    limit: int,
) -> list[dict[str, Any]]:
    maximum = require_limit(limit, name="max_tests", maximum=12)
    test_root = router.root / "build"
    if not test_root.is_dir():
        return []
    source_stem_tokens = {
        token.casefold()
        for token in STEM_TOKEN_RE.findall(Path(fragment.path).stem)
        if len(token) >= 4
    }
    area_terms = set(AREA_TEST_TERMS.get(fragment.area, ()))
    candidates: list[tuple[int, Path, list[str]]] = []
    for path in sorted(test_root.glob("test_*_static.py"), key=lambda item: item.name.lower()):
        name = path.stem.casefold()
        matched = sorted(
            token
            for token in source_stem_tokens | area_terms
            if token in name
        )
        score = len(matched) * 10 + sum(token in name for token in area_terms)
        if score:
            candidates.append((score, path, matched))
    candidates.sort(key=lambda item: (-item[0], item[1].name.lower()))
    return [
        {
            "path": project_relative(path, router.root),
            "score": score,
            "matched_terms": matched,
            "command": f"py -3 -B {project_relative(path, router.root).replace('/', '\\\\')}",
        }
        for score, path, matched in candidates[:maximum]
    ]


def linked_context(
    router: RouterIndex,
    target_id: str,
    *,
    focus_line: int | None = None,
    max_lines: int = 120,
    related_limit: int = 30,
) -> dict[str, Any]:
    """Return a bounded ownership card and all high-value static links."""

    fragment = target_fragment(router, target_id)
    maximum_related = require_limit(related_limit, name="related_limit")
    raw, _, _ = read_text_with_encoding(source_path(router, fragment))
    entities = declared_entities(fragment, raw)
    relationships = source_relationships(
        router,
        fragment,
        entities,
        related_limit=maximum_related,
    )
    return {
        "summary": router_summary(router),
        "target": {
            "target_id": fragment.id,
            "path": fragment.path,
            "area": fragment.area,
            "kind": fragment.kind,
            "sha256": fragment.sha256,
            "line_count": fragment.line_count,
            "syntax_error": fragment.syntax_error,
        },
        "source_excerpt": source_excerpt(
            router,
            fragment,
            focus_line=focus_line,
            max_lines=max_lines,
        ),
        "ordering": order_payload(router, fragment),
        "generated_links": generated_links_payload(router, fragment),
        "export_layers": export_layers(fragment),
        "declared_entities": entities[:maximum_related],
        "declared_entities_truncated": len(entities) > maximum_related,
        "direct_symbols": direct_symbols(raw, maximum_related),
        "relationships": relationships,
        "verification_candidates": test_candidates(
            router,
            fragment,
            limit=min(maximum_related, 12),
        ),
        "warnings": router.warnings,
    }


def risk_level(
    fragment: SourceFragment,
    relationships: dict[str, Any],
) -> tuple[str, list[dict[str, str]]]:
    factors: list[dict[str, str]] = []
    if fragment.area == "dialogs":
        factors.append(
            {
                "level": "high",
                "reason": "Dialogue fragments are first-match-order sensitive.",
            }
        )
    if relationships["called_by_count"]:
        factors.append(
            {
                "level": "high",
                "reason": "The fragment declares scripts with incoming call sites.",
            }
        )
    if relationships["globals"]["writes"]:
        factors.append(
            {
                "level": "high",
                "reason": "The fragment writes cross-screen global state.",
            }
        )
    if relationships["registers"]["writes"]:
        factors.append(
            {
                "level": "medium",
                "reason": "The fragment writes volatile register/local state.",
            }
        )
    if relationships["visible_text_sink_count"]:
        factors.append(
            {
                "level": "medium",
                "reason": "The fragment owns visible text sinks.",
            }
        )
    if fragment.area in {"menus", "mission_templates", "presentations"}:
        factors.append(
            {
                "level": "medium",
                "reason": "The fragment owns a UI or mission-facing execution context.",
            }
        )
    level = "low"
    if any(factor["level"] == "high" for factor in factors):
        level = "high"
    elif factors:
        level = "medium"
    return level, factors


def change_impact(
    router: RouterIndex,
    target_id: str,
    *,
    related_limit: int = 30,
) -> dict[str, Any]:
    """Describe what a source edit can affect before the edit is made."""

    context = linked_context(
        router,
        target_id,
        max_lines=1,
        related_limit=related_limit,
    )
    target = context["target"]
    fragment = target_fragment(router, target_id)
    relationships = context["relationships"]
    risk, factors = risk_level(fragment, relationships)
    builder = BUILD_BY_AREA.get(fragment.area)
    generated_outputs = sorted(
        {
            link["compile_path"]
            for link in context["generated_links"]
        }
        | set(GENERATED_BY_AREA.get(fragment.area, ()))
    )
    return {
        "summary": context["summary"],
        "target": target,
        "risk_level": risk,
        "risk_factors": factors,
        "direct_generated_outputs": generated_outputs,
        "expected_stale_layers_after_source_edit": {
            "generated_modules": generated_outputs,
            "exports": [item["path"] for item in context["export_layers"]],
            "builder": (
                {
                    "path": builder[0],
                    "command": f"py -3 {builder[0].replace('/', '\\\\')}",
                    "writes_live_exports": False,
                }
                if builder
                else None
            ),
            "note": (
                "The Change Router never refreshes compile/ or _export/ automatically. "
                "Use a reviewed build step after source verification."
            ),
        },
        "transitive_impact": {
            "incoming_script_call_count": relationships["called_by_count"],
            "outgoing_script_call_count": len(relationships["called_scripts"]),
            "visible_text_sink_count": relationships["visible_text_sink_count"],
            "menu_transition_count": relationships["menu_transition_count"],
            "related_source_fragment_count": relationships["related_source_fragment_count"],
            "incoming_script_calls": relationships["called_by"],
            "outgoing_scripts": relationships["called_scripts"],
            "visible_text_sinks": relationships["visible_text_sinks"],
            "menu_transitions": relationships["menu_transitions"],
            "related_source_fragments": relationships["related_source_fragments"],
        },
        "ordering_contract": context["ordering"],
        "recommended_static_checks": context["verification_candidates"],
        "warnings": context["warnings"],
    }


def require_sha256(value: str, *, name: str = "expected_sha256") -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", value):
        raise ChangeRouterError(f"{name} must be a 64-character SHA-256 hex string.")
    return value.casefold()


def validate_edits(edits: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(edits, Sequence) or isinstance(edits, (str, bytes)):
        raise ChangeRouterError("edits must be a non-empty list of edit objects.")
    if not 1 <= len(edits) <= MAX_EDIT_COUNT:
        raise ChangeRouterError(f"edits must contain from 1 through {MAX_EDIT_COUNT} entries.")
    normalized: list[dict[str, Any]] = []
    for index, edit in enumerate(edits, start=1):
        if not isinstance(edit, dict):
            raise ChangeRouterError(f"edit {index} must be an object.")
        old_text = edit.get("old_text")
        new_text = edit.get("new_text")
        if not isinstance(old_text, str) or not old_text:
            raise ChangeRouterError(f"edit {index}.old_text must be a non-empty string.")
        if not isinstance(new_text, str):
            raise ChangeRouterError(f"edit {index}.new_text must be a string.")
        if len(old_text) > MAX_EDIT_TEXT_LENGTH or len(new_text) > MAX_EDIT_TEXT_LENGTH:
            raise ChangeRouterError(
                f"edit {index} text exceeds the {MAX_EDIT_TEXT_LENGTH:,}-character safety limit."
            )
        occurrence = edit.get("occurrence", 1)
        expected_occurrences = edit.get("expected_occurrences", 1)
        if (
            isinstance(occurrence, bool)
            or not isinstance(occurrence, int)
            or occurrence < 1
        ):
            raise ChangeRouterError(f"edit {index}.occurrence must be a positive integer.")
        if (
            isinstance(expected_occurrences, bool)
            or not isinstance(expected_occurrences, int)
            or expected_occurrences < 1
        ):
            raise ChangeRouterError(
                f"edit {index}.expected_occurrences must be a positive integer."
            )
        normalized.append(
            {
                "old_text": old_text,
                "new_text": new_text,
                "occurrence": occurrence,
                "expected_occurrences": expected_occurrences,
            }
        )
    return normalized


def all_occurrences(raw: str, needle: str) -> list[int]:
    starts: list[int] = []
    start = 0
    while True:
        index = raw.find(needle, start)
        if index < 0:
            break
        starts.append(index)
        start = index + len(needle)
    return starts


def prepare_edits(raw: str, edits: Sequence[dict[str, Any]]) -> tuple[str, list[PlannedEdit]]:
    normalized = validate_edits(edits)
    planned: list[PlannedEdit] = []
    ranges: list[tuple[int, int]] = []
    for index, edit in enumerate(normalized, start=1):
        starts = all_occurrences(raw, edit["old_text"])
        actual = len(starts)
        expected = edit["expected_occurrences"]
        occurrence = edit["occurrence"]
        if actual != expected:
            raise ChangeRouterError(
                f"edit {index} expected {expected} occurrence(s) of old_text, found {actual}."
            )
        if occurrence > actual:
            raise ChangeRouterError(
                f"edit {index}.occurrence={occurrence} exceeds {actual} matched occurrence(s)."
            )
        start = starts[occurrence - 1]
        end = start + len(edit["old_text"])
        if any(start < other_end and end > other_start for other_start, other_end in ranges):
            raise ChangeRouterError("Patch edits overlap; split or narrow their old_text anchors.")
        ranges.append((start, end))
        planned.append(
            PlannedEdit(
                old_text=edit["old_text"],
                new_text=edit["new_text"],
                occurrence=occurrence,
                expected_occurrences=expected,
                start=start,
                end=end,
                line_start=raw.count("\n", 0, start) + 1,
                line_end=raw.count("\n", 0, end) + 1,
            )
        )
    updated = raw
    for edit in sorted(planned, key=lambda item: item.start, reverse=True):
        updated = updated[:edit.start] + edit.new_text + updated[edit.end:]
    if updated == raw:
        raise ChangeRouterError("The proposed edits do not change the source fragment.")
    return updated, sorted(planned, key=lambda item: item.start)


def validate_python_source(raw: str, path: Path) -> None:
    try:
        ast.parse(raw, filename=str(path))
    except SyntaxError as error:
        raise ChangeRouterError(
            f"Proposed patch would make {path.name} invalid Python: "
            f"{error.msg} at line {error.lineno}, column {error.offset}."
        ) from error


def hash_text(raw: str, encoding: str) -> str:
    try:
        content = raw.encode(encoding)
    except UnicodeEncodeError as error:
        raise ChangeRouterError(
            f"Proposed text cannot be encoded as the fragment's existing {encoding} encoding."
        ) from error
    return hashlib.sha256(content).hexdigest()


def unified_diff(
    fragment: SourceFragment,
    before: str,
    after: str,
) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{fragment.path}",
            tofile=f"b/{fragment.path}",
            n=3,
        )
    )


def patch_plan(
    router: RouterIndex,
    target_id: str,
    edits: Sequence[dict[str, Any]],
    *,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    """Create a deterministic source-only patch plan; never write the file."""

    fragment = target_fragment(router, target_id)
    path = source_path(router, fragment)
    raw, encoding, raw_bytes = read_text_with_encoding(path)
    current_sha = hashlib.sha256(raw_bytes).hexdigest()
    if expected_sha256 is not None and require_sha256(expected_sha256) != current_sha:
        raise ChangeRouterError(
            "expected_sha256 does not match the current source fragment; refresh linked_context and re-plan."
        )
    updated, planned = prepare_edits(raw, edits)
    validate_python_source(updated, path)
    updated_sha = hash_text(updated, encoding)
    diff = unified_diff(fragment, raw, updated)
    identity = hashlib.sha256(
        (
            f"{fragment.id}\n{current_sha}\n{updated_sha}\n"
            + json.dumps([edit.payload() for edit in planned], sort_keys=True)
        ).encode("utf-8")
    ).hexdigest()[:20]
    impact = change_impact(router, target_id)
    return {
        "plan_id": f"change-plan:{identity}",
        "target": {
            "target_id": fragment.id,
            "path": fragment.path,
            "base_sha256": current_sha,
            "proposed_sha256": updated_sha,
            "encoding": encoding,
        },
        "edits": [edit.payload() for edit in planned],
        "unified_diff": diff,
        "changed_line_count": sum(
            max(1, edit.new_text.count("\n") + 1)
            for edit in planned
        ),
        "impact": impact,
        "apply_contract": {
            "tool": "apply_source_edits",
            "dry_run_default": True,
            "required_expected_sha256": current_sha,
            "guarantees": [
                "Only the exact source fragment under src/ may be written.",
                "The SHA-256 must still match when apply is requested.",
                "compile/ and _export/ are never written by this tool.",
            ],
        },
        "warnings": router.warnings,
    }


def atomic_write(path: Path, raw: str, encoding: str) -> None:
    temporary = path.with_name(f"{path.name}.change-router.tmp")
    try:
        temporary.write_text(raw, encoding=encoding, newline="")
        temporary.replace(path)
    except OSError as error:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise ChangeRouterError(f"Could not atomically update {path}: {error}") from error


def apply_source_edits(
    router: RouterIndex,
    target_id: str,
    edits: Sequence[dict[str, Any]],
    *,
    expected_sha256: str,
    dry_run: bool = True,
) -> dict[str, Any]:
    """Apply an explicit, hash-guarded source patch only when dry_run is false."""

    if not isinstance(dry_run, bool):
        raise ChangeRouterError("dry_run must be a boolean.")
    checked_hash = require_sha256(expected_sha256)
    plan = patch_plan(
        router,
        target_id,
        edits,
        expected_sha256=checked_hash,
    )
    if dry_run:
        return {
            "applied": False,
            "dry_run": True,
            "plan": plan,
            "warnings": router.warnings,
        }
    fragment = target_fragment(router, target_id)
    path = source_path(router, fragment)
    raw, encoding, raw_bytes = read_text_with_encoding(path)
    current_sha = hashlib.sha256(raw_bytes).hexdigest()
    if current_sha != checked_hash:
        raise ChangeRouterError(
            "Source changed after planning; refusing to apply stale edits."
        )
    updated, _ = prepare_edits(raw, edits)
    validate_python_source(updated, path)
    atomic_write(path, updated, encoding)
    invalidate_router(router.root)
    return {
        "applied": True,
        "dry_run": False,
        "target": {
            "target_id": fragment.id,
            "path": fragment.path,
            "base_sha256": current_sha,
            "result_sha256": hash_text(updated, encoding),
        },
        "plan_id": plan["plan_id"],
        "verification_required": {
            "tool": "verify_change",
            "target_id": fragment.id,
            "expected_sha256": hash_text(updated, encoding),
            "note": (
                "Source was updated. Generated modules and exports are now expected "
                "to be stale until a separately reviewed build step."
            ),
        },
        "warnings": [
            *router.warnings,
            "Only source was changed. No compile/ or _export/ file was written.",
        ],
    }


def generated_freshness(
    router: RouterIndex,
    fragment: SourceFragment,
) -> list[dict[str, Any]]:
    source_stat = source_path(router, fragment).stat()
    results: list[dict[str, Any]] = []
    generated = {
        *GENERATED_BY_AREA.get(fragment.area, ()),
        *(link.compile_path for link in router.generated_by_source.get(fragment.path, ())),
    }
    for relative in sorted(generated, key=str.lower):
        path = router.root / relative
        if not path.is_file():
            results.append(
                {
                    "path": relative,
                    "status": "missing",
                    "source_is_newer": None,
                }
            )
            continue
        generated_stat = path.stat()
        source_is_newer = source_stat.st_mtime_ns > generated_stat.st_mtime_ns
        results.append(
            {
                "path": relative,
                "status": "stale" if source_is_newer else "current_or_newer",
                "source_is_newer": source_is_newer,
                "source_mtime_ns": source_stat.st_mtime_ns,
                "generated_mtime_ns": generated_stat.st_mtime_ns,
            }
        )
    return results


def run_static_tests(
    router: RouterIndex,
    candidates: Sequence[dict[str, Any]],
    *,
    timeout_seconds: int,
) -> list[dict[str, Any]]:
    timeout = require_limit(timeout_seconds, name="timeout_seconds", maximum=300)
    results: list[dict[str, Any]] = []
    for candidate in candidates:
        relative = str(candidate["path"])
        command = [sys.executable, "-B", relative]
        try:
            completed = subprocess.run(
                command,
                cwd=router.root,
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )
            output = (completed.stdout + completed.stderr).strip()
            if len(output) > 4_000:
                output = output[:3_997] + "..."
            results.append(
                {
                    "path": relative,
                    "exit_code": completed.returncode,
                    "passed": completed.returncode == 0,
                    "output": output,
                }
            )
        except subprocess.TimeoutExpired:
            results.append(
                {
                    "path": relative,
                    "exit_code": None,
                    "passed": False,
                    "output": f"Timed out after {timeout} seconds.",
                }
            )
    return results


def stage_build(
    router: RouterIndex,
    fragment: SourceFragment,
    *,
    timeout_seconds: int,
) -> dict[str, Any]:
    """Build one source area in an isolated temporary workspace."""

    build_spec = BUILD_BY_AREA.get(fragment.area)
    if build_spec is None:
        return {
            "available": False,
            "reason": f"No staged builder is configured for source area {fragment.area!r}.",
        }
    builder_relative, output_relative = build_spec
    builder_source = router.root / builder_relative
    if not builder_source.is_file():
        return {
            "available": False,
            "reason": f"Configured builder is missing: {builder_relative}",
        }
    timeout = require_limit(timeout_seconds, name="timeout_seconds", maximum=300)
    with tempfile.TemporaryDirectory(prefix="sod-change-router-") as temporary_name:
        stage_root = Path(temporary_name)
        try:
            shutil.copytree(
                router.root / "src",
                stage_root / "src",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            shutil.copytree(
                router.root / "build",
                stage_root / "build",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            docs_source = router.root / "docs"
            if docs_source.is_dir():
                shutil.copytree(
                    docs_source,
                    stage_root / "docs",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
                )
            headers = router.root / "compile" / "headers"
            if headers.is_dir():
                shutil.copytree(headers, stage_root / "compile" / "headers")
            stage_output = stage_root / output_relative
            stage_output.parent.mkdir(parents=True, exist_ok=True)
            live_output = router.root / output_relative
            if live_output.is_file():
                shutil.copy2(live_output, stage_output)
            ids_source = router.root / "compile" / "ids"
            if ids_source.is_dir():
                shutil.copytree(ids_source, stage_root / "compile" / "ids")
        except OSError as error:
            return {
                "available": False,
                "reason": f"Could not prepare isolated staging workspace: {error}",
            }
        try:
            completed = subprocess.run(
                [sys.executable, str(stage_root / builder_relative)],
                cwd=stage_root,
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {
                "available": True,
                "passed": False,
                "builder": builder_relative,
                "output": f"Timed out after {timeout} seconds.",
            }
        output = (completed.stdout + completed.stderr).strip()
        if len(output) > 4_000:
            output = output[:3_997] + "..."
        if completed.returncode != 0:
            return {
                "available": True,
                "passed": False,
                "builder": builder_relative,
                "exit_code": completed.returncode,
                "output": output,
            }
        if not stage_output.is_file():
            return {
                "available": True,
                "passed": False,
                "builder": builder_relative,
                "exit_code": completed.returncode,
                "output": output,
                "reason": f"Builder did not produce {output_relative} in staging.",
            }
        staged_raw, _, _ = read_text_with_encoding(stage_output)
        live_raw = ""
        if live_output.is_file():
            live_raw, _, _ = read_text_with_encoding(live_output)
        diff_lines = list(
            difflib.unified_diff(
                live_raw.splitlines(keepends=True),
                staged_raw.splitlines(keepends=True),
                fromfile=f"live/{output_relative}",
                tofile=f"staged/{output_relative}",
                n=2,
            )
        )
        preview = "".join(diff_lines[:240])
        return {
            "available": True,
            "passed": True,
            "builder": builder_relative,
            "exit_code": completed.returncode,
            "output": output,
            "generated_output": output_relative,
            "generated_changed": bool(diff_lines),
            "generated_diff_preview": preview,
            "generated_diff_line_count": len(diff_lines),
            "writes_to_live_workspace": False,
        }


def verify_change(
    router: RouterIndex,
    target_id: str,
    *,
    expected_sha256: str | None = None,
    run_tests: bool = False,
    stage_build_check: bool = False,
    max_tests: int = 3,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    """Validate a current source fragment and optionally build it in isolation."""

    if not isinstance(run_tests, bool) or not isinstance(stage_build_check, bool):
        raise ChangeRouterError("run_tests and stage_build_check must be booleans.")
    fragment = target_fragment(router, target_id)
    path = source_path(router, fragment)
    raw, encoding, raw_bytes = read_text_with_encoding(path)
    current_sha = hashlib.sha256(raw_bytes).hexdigest()
    if expected_sha256 is not None and require_sha256(expected_sha256) != current_sha:
        raise ChangeRouterError(
            "expected_sha256 does not match the current source fragment; verification would be stale."
        )
    syntax: dict[str, Any]
    try:
        validate_python_source(raw, path)
        syntax = {"passed": True, "encoding": encoding}
    except ChangeRouterError as error:
        syntax = {"passed": False, "error": str(error), "encoding": encoding}
    candidates = test_candidates(router, fragment, limit=max_tests)
    tests = (
        run_static_tests(router, candidates, timeout_seconds=timeout_seconds)
        if run_tests
        else []
    )
    staging = (
        stage_build(router, fragment, timeout_seconds=timeout_seconds)
        if stage_build_check
        else {
            "available": True,
            "performed": False,
            "reason": "Set stage_build_check=true to build only this source area in an isolated temporary workspace.",
        }
    )
    freshness = generated_freshness(router, fragment)
    passed_tests = all(result["passed"] for result in tests)
    return {
        "summary": router_summary(router),
        "target": {
            "target_id": fragment.id,
            "path": fragment.path,
            "sha256": current_sha,
        },
        "syntax": syntax,
        "ordering": order_payload(router, fragment),
        "generated_freshness": freshness,
        "static_test_candidates": candidates,
        "tests_run": tests,
        "tests_passed": passed_tests if run_tests else None,
        "staged_build": staging,
        "next_required_step": (
            "Review the source diff, then run the project builder intentionally; "
            "the Change Router does not write compile/ or _export/."
        ),
        "warnings": router.warnings,
    }


def output_path(path_arg: str, root: Path) -> Path:
    path = Path(path_arg)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    export_root = (root / "_export").resolve()
    try:
        path.relative_to(export_root)
    except ValueError:
        return path
    raise ChangeRouterError("Refusing to write a Change Router artifact under _export/.")


def parse_edits_json(value: str) -> list[dict[str, Any]]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise ChangeRouterError(f"--edits must contain valid JSON: {error}") from error
    if not isinstance(parsed, list):
        raise ChangeRouterError("--edits must decode to a JSON list.")
    return [dict(item) if isinstance(item, dict) else item for item in parsed]


def parse_edits_input(
    inline: str | None,
    supplied_path: str | None,
    root: Path,
) -> list[dict[str, Any]]:
    if bool(inline) == bool(supplied_path):
        raise ChangeRouterError("Supply exactly one of --edits or --edits-file.")
    if inline:
        return parse_edits_json(inline)
    assert supplied_path is not None
    path = Path(supplied_path)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise ChangeRouterError("--edits-file must be inside this workspace.") from error
    try:
        return parse_edits_json(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ChangeRouterError(f"Could not read --edits-file: {error}") from error


def write_payload(payload: dict[str, Any], supplied: str | None, root: Path) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if supplied:
        path = output_path(supplied, root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="LLM-first SoD Modern source discovery, impact, and guarded editing."
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--output")

    find_parser = subparsers.add_parser("find")
    find_parser.add_argument("query")
    find_parser.add_argument(
        "--scope",
        choices=("all", "source", "generated", "export"),
        default="all",
    )
    find_parser.add_argument("--limit", type=int, default=20)
    find_parser.add_argument("--output")

    context_parser = subparsers.add_parser("context")
    context_parser.add_argument("target_id")
    context_parser.add_argument("--focus-line", type=int)
    context_parser.add_argument("--max-lines", type=int, default=120)
    context_parser.add_argument("--related-limit", type=int, default=30)
    context_parser.add_argument("--output")

    impact_parser = subparsers.add_parser("impact")
    impact_parser.add_argument("target_id")
    impact_parser.add_argument("--related-limit", type=int, default=30)
    impact_parser.add_argument("--output")

    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("target_id")
    plan_edit_input = plan_parser.add_mutually_exclusive_group(required=True)
    plan_edit_input.add_argument("--edits")
    plan_edit_input.add_argument("--edits-file")
    plan_parser.add_argument("--expected-sha256")
    plan_parser.add_argument("--output")

    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument("target_id")
    apply_edit_input = apply_parser.add_mutually_exclusive_group(required=True)
    apply_edit_input.add_argument("--edits")
    apply_edit_input.add_argument("--edits-file")
    apply_parser.add_argument("--expected-sha256", required=True)
    apply_parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write the hash-guarded source edit. The default is a dry run.",
    )
    apply_parser.add_argument("--output")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("target_id")
    verify_parser.add_argument("--expected-sha256")
    verify_parser.add_argument("--run-tests", action="store_true")
    verify_parser.add_argument("--stage-build", action="store_true")
    verify_parser.add_argument("--max-tests", type=int, default=3)
    verify_parser.add_argument("--timeout-seconds", type=int, default=90)
    verify_parser.add_argument("--output")

    args = parser.parse_args(argv)
    command = args.command or "summary"
    try:
        router = build_change_router(DEFAULT_REPO_ROOT)
        if command == "summary":
            payload = {
                "summary": router_summary(router),
                "warnings": router.warnings,
            }
        elif command == "find":
            payload = code_find(router, args.query, scope=args.scope, limit=args.limit)
        elif command == "context":
            payload = linked_context(
                router,
                args.target_id,
                focus_line=args.focus_line,
                max_lines=args.max_lines,
                related_limit=args.related_limit,
            )
        elif command == "impact":
            payload = change_impact(
                router,
                args.target_id,
                related_limit=args.related_limit,
            )
        elif command == "plan":
            payload = patch_plan(
                router,
                args.target_id,
                parse_edits_input(args.edits, args.edits_file, DEFAULT_REPO_ROOT),
                expected_sha256=args.expected_sha256,
            )
        elif command == "apply":
            payload = apply_source_edits(
                router,
                args.target_id,
                parse_edits_input(args.edits, args.edits_file, DEFAULT_REPO_ROOT),
                expected_sha256=args.expected_sha256,
                dry_run=not args.apply,
            )
        else:
            payload = verify_change(
                router,
                args.target_id,
                expected_sha256=args.expected_sha256,
                run_tests=args.run_tests,
                stage_build_check=args.stage_build,
                max_tests=args.max_tests,
                timeout_seconds=args.timeout_seconds,
            )
        write_payload(payload, getattr(args, "output", None), DEFAULT_REPO_ROOT)
    except (
        ChangeRouterError,
        execution_ledger.LedgerError,
        integrity.StringIntegrityError,
    ) as error:
        print(f"change_router: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
