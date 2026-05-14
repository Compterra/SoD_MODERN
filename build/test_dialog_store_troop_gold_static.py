from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SRC_DIALOGS = ROOT / "src" / "dialogs"
TARGETS = (
    ROOT / "src" / "dialogs" / "ZZ99_misc_dialogs" / "anyone_plyr_lost_sh_spy_4.py",
    ROOT / "src" / "dialogs" / "ZC02_townsfolk_and_special_npcs" / "anyone_plyr_bandits_awaiting_ransom_b2.py",
    ROOT / "src" / "dialogs" / "ZC02_townsfolk_and_special_npcs" / "anyone_plyr_militia_awaiting_ransom_b2.py",
    ROOT / "src" / "dialogs" / "ZC02_townsfolk_and_special_npcs" / "party_tpl_pt_bandits_awaiting_ransom_plyr_bandits_awaiting_ransom_intro_1.py",
    ROOT / "src" / "dialogs" / "ZC02_townsfolk_and_special_npcs" / "party_tpl_pt_militia_awaiting_ransom_plyr_militia_awaiting_ransom_intro_1.py",
    ROOT / "src" / "dialogs" / "ZD01_encounters_battles_and_prisoners" / "anyone_plyr_deserter_barter_2.py",
)

ONE_ARG_STORE_TROOP_GOLD = re.compile(r"\(store_troop_gold,\s*(?:reg\(\d+\)|[^,()]+)\)")


def main() -> None:
    for path in TARGETS:
        source = path.read_text(encoding="utf-8")
        assert '(store_troop_gold, ":gold")' not in source, str(path)
        assert '(store_troop_gold, ":cur_gold")' not in source, str(path)
        assert "trp_player" in source, str(path)

    offenders = []
    for path in SRC_DIALOGS.rglob("*.py"):
        if "ZE01_companions_and_named_npcs" in path.parts:
            continue
        source = path.read_text(encoding="utf-8")
        for match in ONE_ARG_STORE_TROOP_GOLD.finditer(source):
            offenders.append(f"{path.relative_to(ROOT)}: {match.group(0)}")

    assert not offenders, "store_troop_gold must name a troop:\n" + "\n".join(offenders)

    print("test_dialog_store_troop_gold_static: OK")


if __name__ == "__main__":
    main()
