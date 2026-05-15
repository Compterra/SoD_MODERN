from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text, needle, path):
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def test_party_size_report_exposes_centralization_context():
    path = "src/menus/0000_hardcoded_mb1011/party_size_report.py"
    text = read(path)

    for needle in [
        '"{s98}"',
        "script_sod_get_realm_military_centralization_profile",
        "str_store_string_reg, s98, s99",
        "Realm military law",
        "Authority: {s10}",
        "Levy system: {s11}",
        "Host balance: {s12}",
        "Political mood: {s13}",
        "centralization concentrates military support around your own host",
        "centralization pulls military support toward the crown",
    ]:
        assert_contains(text, needle, path)


if __name__ == "__main__":
    test_party_size_report_exposes_centralization_context()
    print("[party_size_report_centralization] OK")
