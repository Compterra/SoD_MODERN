from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def main():
    source = read("src/presentations/0012_sliders/sliders.py")

    assert '(val_clamp, ":value", 0, 101)' in source, "slider event values must be clamped"
    assert "(store_random_in_range" not in source, "generic slider should not randomly rebalance during drag events"
    assert '(try_for_range, ":unused", 0, ":difference")' not in source, (
        "generic slider drag handling should not use a mutable difference loop"
    )
    assert '(store_sub, ":delta", ":value", ":old_value")' in source, (
        "generic slider should rebalance from the actual drag delta"
    )
    assert '(val_min, ":transfer", ":remaining_delta")' in source, (
        "generic slider should bound transfers between slider buckets"
    )
    for global_name in [
        "$g_presentation_obj_1_val",
        "$g_presentation_obj_2_val",
        "$g_presentation_obj_3_val",
        "$g_presentation_obj_4_val",
    ]:
        assert f'(val_clamp, "{global_name}", 0, 101)' in source, (
            f"{global_name} should be clamped before overlay updates"
        )

    print("Generic slider presentation static checks passed")


if __name__ == "__main__":
    main()
