from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, path: str) -> None:
    if needle not in text:
        raise AssertionError(f"{path} missing {needle!r}")


def assert_not_contains(text: str, needle: str, path: str) -> None:
    if needle in text:
        raise AssertionError(f"{path} must not expose raw telemetry: {needle!r}")


def main() -> None:
    recon_path = "src/scripts/ZD_centers/update_center_recon_notes.py"
    brief_path = "src/scripts/ZY_helper_scripts/sod_store_center_recon_brief_to_s68.py"
    recon = read(recon_path)
    brief = read(brief_path)

    assert_contains(recon, "script_sod_store_center_recon_brief_to_s68", recon_path)
    assert_contains(recon, "quick field read", recon_path)

    for needle in (
        "script_sod_center_public_health_compute_causes",
        "script_sod_get_center_food_profile",
        "script_sod_get_center_goods_market_profile",
        "script_sod_get_center_security_profile",
        "script_sod_get_center_faith_profile",
        "The people are in fair health.",
        "Food stores are adequate.",
        "Trade is steady.",
        "The roads are quiet.",
        "The village is devastated.",
    ):
        assert_contains(brief, needle, brief_path)

    for needle in (
        "Village root economy",
        "Public health:",
        "Current outbreak:",
        "Recommendation:",
        "Goods market:",
        "weekly wealth drift",
        "Tax extraction:",
        "Local tax burden:",
        "Security infrastructure:",
        "Village garrison",
        "Effective threat",
        "Faith: dominant",
    ):
        assert_not_contains(recon, needle, recon_path)
        assert_not_contains(brief, needle, brief_path)

    print("[center_recon_note_presentation] OK")


if __name__ == "__main__":
    main()
