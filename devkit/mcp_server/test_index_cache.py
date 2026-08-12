"""Focused regression tests for the in-process MCP index cache."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory


SERVER_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVER_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.mcp_server import server


def test_cached_workspace_index_reuses_and_invalidates() -> None:
    server.INDEX_CACHE.clear()
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "src" / "example.py"
        source.parent.mkdir(parents=True)
        source.write_text("value = 1\n", encoding="utf-8")
        calls: list[Path] = []

        def builder(actual_root: Path) -> dict[str, int]:
            calls.append(actual_root)
            return {"call": len(calls)}

        first = server.cached_workspace_index("test", root, builder)
        second = server.cached_workspace_index("test", root, builder)
        assert first is second
        assert first == {"call": 1}

        source.write_text("value = 2  # different revision\n", encoding="utf-8")
        third = server.cached_workspace_index("test", root, builder)
        assert third == {"call": 2}
        assert calls == [root.resolve(), root.resolve()]

    server.INDEX_CACHE.clear()


def test_cached_workspace_index_includes_root_build_inputs() -> None:
    server.INDEX_CACHE.clear()
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "src").mkdir()
        build_entry = root / "build_module.bat"
        build_entry.write_text("@echo first\n", encoding="utf-8")
        calls: list[int] = []

        def builder(_: Path) -> int:
            calls.append(1)
            return len(calls)

        assert server.cached_workspace_index("root-build-test", root, builder) == 1
        assert server.cached_workspace_index("root-build-test", root, builder) == 1
        build_entry.write_text("@echo second build revision\n", encoding="utf-8")
        assert server.cached_workspace_index("root-build-test", root, builder) == 2

    server.INDEX_CACHE.clear()


def test_cache_root_builder_does_not_cache_temporary_roots() -> None:
    calls: list[Path] = []

    def builder(root: Path) -> int:
        calls.append(root)
        return len(calls)

    cached = server.cache_root_builder("isolated-test", builder)
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        assert cached(root) == 1
        assert cached(root) == 2
    assert len(calls) == 2


if __name__ == "__main__":
    test_cached_workspace_index_reuses_and_invalidates()
    test_cached_workspace_index_includes_root_build_inputs()
    test_cache_root_builder_does_not_cache_temporary_roots()
    print("test_index_cache: OK")
