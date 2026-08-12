from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    path = ROOT / "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_talk_24.py"
    raw = path.read_text(encoding="utf-8", errors="replace")

    assert '[anyone|plyr, "gm_talk", [' in raw
    assert '"Goodbye.", "close_window", []' in raw
    assert "finish_mission" not in raw
    assert "$g_leave_encounter" not in raw

    print("[guild_scene_dialogue_exit] OK")


if __name__ == "__main__":
    main()
