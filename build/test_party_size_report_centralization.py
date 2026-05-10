from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text, needle, path):
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def main():
    path = "src/menus/camp/party_size_report.py"
    text = read(path)

    for needle in [
        "script_sod_get_realm_military_centralization_profile",
        "Realm military law",
        "Centralization: {reg10}",
        "Militarization: {reg11}",
        "Ruler host modifier: {reg12}",
        "Vassal host modifier: {reg13}",
        "Noble happiness: {reg14}",
        "Unrest pressure: {reg15}",
        "centralization concentrates military support around your own host",
        "centralization pulls military support toward the crown",
    ]:
        assert_contains(text, needle, path)

    print("[party_size_report_centralization] OK")


if __name__ == "__main__":
    main()
