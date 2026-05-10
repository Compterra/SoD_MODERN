from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    menu = read("src/menus/kingdom/peace_offer_accept.py")
    assert "You receive a peace offer from {s1}" in menu
    assert "truce until {s4}" in menu
    assert "truce untill" not in menu
    assert '(str_store_faction_name, s1, "$g_notification_menu_var1")' in menu
    assert "No claim, castle, or vassal of another kingdom is part of this truce." in menu
    assert '(call_script, "script_diplomacy_start_peace_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1)' in menu

    print("Peace offer text static checks passed")


if __name__ == "__main__":
    main()

