from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_book_helper_scripts_exist() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_books.py")
    for token in (
        "sod_books_describe_book_to_s20",
        "sod_books_get_reading_pace_to_regs",
        "sod_books_describe_current_reading_to_s20",
        "sod_books_describe_bookseller_advice_to_s20",
        "sod_books_describe_library_report_to_s20",
        "itm_book_tactics",
        "itm_book_trade",
        "itm_book_chirurgeons_ledger",
        "itm_book_anatomy_of_mercy",
        "itm_book_drill_camp_company",
        "itm_book_roads_before_armies",
        "itm_book_quartermasters_burden",
        "itm_book_embassies_in_wartime",
        "itm_book_wound_treatment_reference",
        "raises Wound Treatment when finished",
        "raises Surgery when finished",
        "raises Trainer when finished",
        "raises Path-finding when finished",
        "raises Inventory Management when finished",
        "Reading progress",
        "Reference books do their work from your baggage",
        "camp rest gives you quiet hours",
        "high morale keeps the camp quiet enough for study",
        "hungry tempers and low morale",
        "recent caravan business makes the trade lessons bite",
        "nearby construction turns engineering theory into examples",
        "Reading pace changes with conditions",
        "Last recorded reading pace",
    ):
        assert_contains(raw, token)


def test_bookseller_dialogue_has_advice_surface() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    for token in (
        "anyone_plyr_bookseller_talk_advice.py",
        "anyone_plyr_bookseller_talk_current.py",
        "anyone_bookseller_advice.py",
        "anyone_bookseller_current.py",
    ):
        assert_contains(order, token)
    assert_contains(read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_116.py"), "quieter voices than tavern men")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/anyone_bookseller_advice.py"), "script_sod_books_describe_bookseller_advice_to_s20")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/anyone_bookseller_current.py"), "script_sod_books_describe_current_reading_to_s20")
    assert_contains(read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_bookseller_talk.py"), "Show me the books you have for sale")


def test_camp_reading_and_reports_use_book_ledger() -> None:
    menu_order = read("src/menus/_order_game_menus.txt")
    assert_contains(menu_order, "reports/book_ledger_report.py")
    assert_contains(read("src/menus/0000_hardcoded_mb1011/reports.py"), "mnu_book_ledger_report")
    assert_contains(read("src/menus/reports/book_ledger_report.py"), "script_sod_books_describe_library_report_to_s20")
    assert_contains(read("src/menus/camp/camp_action.py"), "Choose a book for the road")
    read_menu = read("src/menus/camp/camp_action_read_book.py")
    assert_contains(read_menu, "({reg1}% read)")
    assert_contains(read_menu, "Review your book ledger")
    assert_contains(read_menu, "Stop reading {s1} for now")
    assert_contains(read_menu, "You have no unread study books ready")
    assert_contains(read("src/menus/camp/camp_action_read_book_start.py"), "script_sod_books_describe_book_to_s20")
    assert_contains(read("src/menus/camp/character_report.py"), "script_sod_books_describe_current_reading_to_s20")


def test_book_completion_message_is_polished() -> None:
    raw = read("src/triggers/ST02_every_hour/entry_0072.py")
    assert_contains(raw, "script_sod_books_get_reading_pace_to_regs")
    assert_contains(raw, "(val_add, \":book_reading_progress\", reg24)")
    assert_contains(raw, "250")
    assert_contains(raw, "500")
    assert_contains(raw, "750")
    assert_contains(raw, "The first quarter is behind you")
    assert_contains(raw, "is half read")
    assert_contains(raw, "is nearly finished")
    assert_contains(raw, "script_sod_books_describe_book_to_s20")
    assert_contains(raw, "Your administration skill has increased by 1")
    assert_contains(raw, "itm_book_chirurgeons_ledger")
    assert_contains(raw, "skl_wound_treatment")
    assert_contains(raw, "itm_book_anatomy_of_mercy")
    assert_contains(raw, "skl_surgery")
    assert_contains(raw, "itm_book_drill_camp_company")
    assert_contains(raw, "skl_trainer")
    assert_contains(raw, "itm_book_roads_before_armies")
    assert_contains(raw, "skl_pathfinding")
    assert_contains(raw, "itm_book_quartermasters_burden")
    assert_contains(raw, "skl_inventory_management")
    assert_contains(raw, "itm_book_embassies_in_wartime")
    assert "administartion" not in raw


def test_new_readable_stat_books_exist_and_are_sold() -> None:
    items = read("compile/module_items.py")
    troops = read("compile/module_troops.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    read_menu = read("src/menus/camp/camp_action_read_book.py")
    for token in (
        "book_chirurgeons_ledger",
        "The Chirurgeon's Ledger",
        "book_anatomy_of_mercy",
        "The Anatomy of Mercy",
        "book_drill_camp_company",
        "Drill, Camp, and Company",
        "book_roads_before_armies",
        "Roads Before Armies",
        "book_quartermasters_burden",
        "The Quartermaster's Burden",
        "book_embassies_in_wartime",
        "Embassies in Wartime",
    ):
        assert_contains(items, token)
    for token in (
        "itm_book_chirurgeons_ledger",
        "itm_book_anatomy_of_mercy",
        "itm_book_drill_camp_company",
        "itm_book_roads_before_armies",
        "itm_book_quartermasters_burden",
        "itm_book_embassies_in_wartime",
    ):
        assert_contains(troops, token)
        assert_contains(game_start, token)
        assert_contains(read_menu, token)


if __name__ == "__main__":
    test_book_helper_scripts_exist()
    test_bookseller_dialogue_has_advice_surface()
    test_camp_reading_and_reports_use_book_ledger()
    test_book_completion_message_is_polished()
    test_new_readable_stat_books_exist_and_are_sold()
    print("test_books_system_static: OK")



