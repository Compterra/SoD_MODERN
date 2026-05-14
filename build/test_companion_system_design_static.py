from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_companion_system_design_doc_tracks_advanced_layers() -> None:
    raw = read("docs/companions/COMPANION_SYSTEM_DESIGN_CHECKLIST.md")
    for token in (
        "# Companion System Design And Checklist",
        "Companion Categories",
        "Native-Style Core Companions",
        "Special Quest Companions",
        "Troop And Range Rules",
        "Recruitment Standards",
        "Approval And Values",
        "Advisor Roles",
        "Personal Quest Standards",
        "World Reaction Coverage",
        "Diego Implementation Checklist",
        "Definition Of Done",
    ):
        assert_contains(raw, token)


def test_companion_system_design_doc_covers_diego_reward() -> None:
    raw = read("docs/companions/COMPANION_SYSTEM_DESIGN_CHECKLIST.md")
    for token in (
        "Diego, added as `trp_diego_companion`",
        "`trp_slave_hero` remains the prison-scene/quest NPC",
        "`trp_diego_companion` is the permanent party version",
        "Diego joins only if he survives the prison-break mission",
        "Diego is outside the tavern rotation",
        "Special quest companions are outside tavern rotation",
        "Their quest NPC and permanent party troop are separate",
    ):
        assert_contains(raw, token)


def test_companion_system_design_doc_defines_diego_values() -> None:
    raw = read("docs/companions/COMPANION_SYSTEM_DESIGN_CHECKLIST.md")
    for token in (
        "Diego Core Design",
        "Core fantasy:",
        "Diego Values",
        "Break chains",
        "Protect the forgotten",
        "Punish predators",
        "Reject ownership of people",
        "Diego Approval Direction",
        "Approval rises from:",
        "Approval falls from:",
        "Diego Lines The Player Can Cross",
        "Diego Role Direction",
        "Chainbreaker",
        "Diego Relationships",
        "Diego Dialogue Deliverables",
    ):
        assert_contains(raw, token)


if __name__ == "__main__":
    test_companion_system_design_doc_tracks_advanced_layers()
    test_companion_system_design_doc_covers_diego_reward()
    test_companion_system_design_doc_defines_diego_values()
    print("test_companion_system_design_static: OK")
