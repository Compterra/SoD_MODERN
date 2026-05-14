from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


ADAPTERS = (
    "src/scripts/ZG_quests/sod_quest_runtime_accept.py",
    "src/scripts/ZG_quests/sod_quest_runtime_update.py",
    "src/scripts/ZG_quests/sod_quest_runtime_complete.py",
    "src/scripts/ZG_quests/sod_quest_runtime_fail.py",
    "src/scripts/ZG_quests/sod_quest_runtime_abort.py",
    "src/scripts/ZG_quests/sod_quest_runtime_init_metadata.py",
    "src/scripts/ZG_quests/sod_quest_event_dispatch.py",
    "src/scripts/ZG_quests/sod_quest_dispatch_active_event.py",
    "src/scripts/ZG_quests/sod_quest_battle_advance_action.py",
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"{label}: missing {needle!r}")


def main() -> None:
    bridge = read("src/quests/quest_runtime_bridge.py")
    for symbol in (
        "CONTEXT_KEYS",
        "normalise_payload",
        "emit_dialogue_memory",
        "apply_runtime_transition",
        "dispatch_event_payload",
        "initialise_runtime_defaults",
        "has_stage_or_progress_changed",
    ):
        assert_contains(bridge, symbol, "quest runtime bridge")

    for rel in ADAPTERS:
        text = read(rel)
        assert_contains(text, "src.quests.quest_runtime_bridge", rel)
        if rel.endswith(("sod_quest_runtime_accept.py", "sod_quest_runtime_complete.py", "sod_quest_runtime_fail.py", "sod_quest_runtime_abort.py")):
            assert_contains(text, "apply_runtime_transition", rel)
        if rel.endswith("sod_quest_runtime_update.py"):
            assert_contains(text, "has_stage_or_progress_changed", rel)
        if rel.endswith("sod_quest_runtime_init_metadata.py"):
            assert_contains(text, "initialise_runtime_defaults", rel)
        if rel.endswith("sod_quest_event_dispatch.py"):
            assert_contains(text, "debug_print", rel)
        if rel.endswith("sod_quest_dispatch_active_event.py"):
            assert_contains(text, "dispatch_event_payload", rel)
        if rel.endswith("sod_quest_battle_advance_action.py"):
            assert_contains(text, "resolve_battle_objective", rel)

        forbidden_duplicates = (
            "def _normalise_payload(",
            "def _call_best_effort(",
            "def _emit_dialogue_memory(",
            "def _first_source(",
            "def _set_value(",
            "def _get_value(",
        )
        for needle in forbidden_duplicates:
            if needle in text:
                raise AssertionError(f"{rel}: duplicated bridge helper {needle}")


if __name__ == "__main__":
    main()
