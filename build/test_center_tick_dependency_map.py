from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def assert_contains(text, needle, label):
    if needle not in text:
        raise AssertionError("%s missing %r" % (label, needle))


def assert_ordered(text, needles, label):
    position = -1
    for needle in needles:
        next_position = text.find(needle)
        if next_position == -1:
            raise AssertionError("%s missing %r" % (label, needle))
        if next_position <= position:
            raise AssertionError("%s has %r out of order" % (label, needle))
        position = next_position


def main():
    audit = read("build/audit_center_tick_dependency_map.py")
    report = read("docs/reports/center_tick_dependency_map.md")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    pipeline = read("src/scripts/ZY_helper_scripts/sod_center_simulation_pipeline.py")

    for token in (
        "PIPELINE_STAGES",
        "Center Tick Dependency Map",
        "building_effects",
        "tax_revenue",
        "town_population",
        "migration",
        "security_desperation",
        "construction",
        "late_faith_drift",
        "goods_market_drift",
        "prisoner_pressure",
        "EXPECTED_WRITE_APIS",
    ):
        assert_contains(audit, token, "audit")

    for token in (
        "# Center Tick Dependency Map",
        "## Pipeline Order",
        "## Dependency Edges",
        "## Write APIs / Normalizers",
        "## Write Ownership",
        "## Change Safety Rules",
        "`src/triggers/ST04_weekly/entry_0123.py`",
        "`script_sod_center_apply_population_delta`",
        "| population | town_population, village_population, migration, security_desperation |",
        "| construction progress | construction |",
        "Do not move construction before population, food, health, and security have settled",
    ):
        assert_contains(report, token, "report")

    assert_ordered(
        trigger_order,
        (
            "ST04_weekly/entry_0018.py",
            "ST04_weekly/entry_0038.py",
            "ST04_weekly/entry_0101.py",
            "ST04_weekly/entry_0104.py",
            "ST04_weekly/entry_0105.py",
            "ST04_weekly/entry_0123.py",
            "ST04_weekly/entry_0132_five_faith_drift.py",
            "ST04_weekly/entry_0160.py",
            "ST04_weekly/entry_0162.py",
        ),
        "weekly center trigger order",
    )

    for token in (
        '"sod_get_center_population_floor"',
        '"sod_center_apply_population_delta"',
        '"sod_center_transfer_population"',
        '"sod_center_apply_wealth_delta"',
        '"sod_center_apply_local_prosperity_delta"',
        '"sod_center_apply_health_delta"',
        '"sod_center_apply_rents_delta"',
        '"sod_center_apply_tariffs_delta"',
        '"sod_center_apply_food_delta"',
        '"sod_center_apply_cattle_delta"',
    ):
        assert_contains(pipeline, token, "center simulation pipeline")

    print("[center_tick_dependency_map] OK")


if __name__ == "__main__":
    main()
