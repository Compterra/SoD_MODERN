from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def main():
    source = read("src/presentations/0020_sod_fief_management/sod_fief_management.py")

    assert '(create_slider_overlay, "$g_presentation_object_25", 0, reg11)' in source, (
        "trainer garrison split slider should be created with the object_25 global"
    )
    assert '(eq, ":object", "$g_presentation_object_25")' in source, (
        "trainer garrison split slider event must listen to the same object global it creates"
    )
    assert '(overlay_set_val, "$g_presentation_object_25", ":value")' in source, (
        "trainer garrison split slider must update the same object global it creates"
    )
    assert '(overlay_set_val, "$g_presentation_obj_25", ":value")' not in source, (
        "old typo can crash/dirty the overlay path when dragging the trainer slider"
    )
    assert '(val_clamp, ":value", 0, ":daily_garrisoning")' in source, (
        "dragged slider values must be clamped to the current daily garrison total"
    )
    assert '(store_sub, ":soldiers", ":daily_garrisoning", ":value")' in source, (
        "soldier/ranged split should be recalculated from a stable total"
    )
    assert '(val_max, ":value", 1)' in source, (
        "fief selector slider should reject stale zero/negative drag values"
    )
    assert '(val_clamp, ":value", 1, "$pres_sod_fief_buildings")' in source, (
        "construction selector slider should clamp dragged values to known buildings"
    )

    print("Fief management trainer slider static checks passed")


if __name__ == "__main__":
    main()
