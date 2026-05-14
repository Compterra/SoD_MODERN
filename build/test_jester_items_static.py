from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def item_entry(raw: str, item_id: str) -> str:
    marker = f'["{item_id}",'
    start = raw.index(marker)
    next_item = raw.find('\n["', start + len(marker))
    next_section = raw.find("\n#", start + len(marker))
    candidates = [pos for pos in (next_item, next_section) if pos != -1]
    end = min(candidates) if candidates else len(raw)
    return raw[start:end]


def test_jester_items_are_not_store_merchandise() -> None:
    items = read("compile/module_items.py")
    for item_id in (
        "jester_tunic",
        "jester_hat_large",
        "jester_hat_small",
        "jester_gloves",
        "jester_boot",
    ):
        entry = item_entry(items, item_id)
        assert "itp_merchandise" not in entry, f"{item_id} should not show up in merchant stores"
        assert_contains(entry, "abundance(0)")


def test_jester_troop_still_has_costume_items() -> None:
    troops = read("compile/module_troops.py")
    assert_contains(troops, '"sod_jester"')
    for token in (
        "itm_jester_tunic",
        "itm_jester_hat_small",
        "itm_jester_gloves",
        "itm_jester_boot",
    ):
        assert_contains(troops, token)


if __name__ == "__main__":
    test_jester_items_are_not_store_merchandise()
    test_jester_troop_still_has_costume_items()
    print("test_jester_items_static: OK")
