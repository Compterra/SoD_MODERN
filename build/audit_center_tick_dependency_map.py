from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORDER_FILE = ROOT / "src" / "triggers" / "_order_simple_triggers.txt"
PIPELINE_FILE = ROOT / "src" / "scripts" / "ZY_helper_scripts" / "sod_center_simulation_pipeline.py"
REPORT = ROOT / "docs" / "reports" / "center_tick_dependency_map.md"


PIPELINE_STAGES = (
    {
        "id": "building_effects",
        "label": "Building modifier refresh",
        "files": ("src/triggers/ST04_weekly/entry_0018.py",),
        "reads": ("building slots", "building registry"),
        "writes": ("building-derived center modifiers",),
        "depends_on": (),
        "notes": "Refresh derived building effects before tax, economy, health, or population profiles consume modifiers.",
    },
    {
        "id": "regional_goods_snapshot",
        "label": "Regional goods snapshot",
        "files": ("src/triggers/ST04_weekly/entry_0019.py",),
        "reads": ("regional production", "center goods profiles"),
        "writes": ("market snapshot inputs",),
        "depends_on": ("building_effects",),
        "notes": "Keep this before revenue so market-sensitive income reads a stable weekly snapshot.",
    },
    {
        "id": "tax_revenue",
        "label": "Tax and revenue accounting",
        "files": ("src/triggers/ST04_weekly/entry_0038.py",),
        "reads": ("population", "market profile", "tax profile", "health", "faith", "laws", "buildings"),
        "writes": ("wealth", "local prosperity", "rents"),
        "depends_on": ("building_effects", "regional_goods_snapshot"),
        "notes": "Revenue is a snapshot pass. Later population/security drift should not retroactively rewrite this week's accounts.",
    },
    {
        "id": "faith_institutions",
        "label": "Faith and institution drift",
        "files": (
            "src/triggers/ST04_weekly/entry_0089.py",
            "src/triggers/ST04_weekly/entry_0090.py",
            "src/triggers/ST04_weekly/entry_0091.py",
        ),
        "reads": ("faith buildings", "center relation", "health", "prosperity"),
        "writes": ("local faith", "faith support", "health", "prosperity", "relation"),
        "depends_on": ("tax_revenue",),
        "notes": "Institutional effects settle before population health and migration checks read center conditions.",
    },
    {
        "id": "building_food_stability",
        "label": "Building food and stability effects",
        "files": (
            "src/triggers/ST04_weekly/entry_0092.py",
            "src/triggers/ST04_weekly/entry_0093.py",
            "src/triggers/ST04_weekly/entry_0094.py",
            "src/triggers/ST04_weekly/entry_0095.py",
            "src/triggers/ST04_weekly/entry_0096.py",
            "src/triggers/ST04_weekly/entry_0097.py",
        ),
        "reads": ("food stores", "building slots", "prisoner/civic slots"),
        "writes": ("food stores", "civic stability"),
        "depends_on": ("faith_institutions",),
        "notes": "Food and stability bonuses must land before population growth, migration, and construction pressure.",
    },
    {
        "id": "law_pressure",
        "label": "Law pressure",
        "files": ("src/triggers/ST04_weekly/entry_0098.py",),
        "reads": ("law support", "security state"),
        "writes": ("law/security pressure",),
        "depends_on": ("building_food_stability",),
        "notes": "Resolve law pressure before weekly health and security desperation apply their deltas.",
    },
    {
        "id": "health_snapshot",
        "label": "Kingdom health snapshot",
        "files": ("src/triggers/ST04_weekly/entry_0100.py",),
        "reads": ("global health", "kingdom state"),
        "writes": ("weekly health snapshot",),
        "depends_on": ("law_pressure",),
        "notes": "Global health should move once per weekly kingdom snapshot, not once per center loop.",
    },
    {
        "id": "town_population",
        "label": "Town population and health",
        "files": ("src/triggers/ST04_weekly/entry_0101.py",),
        "reads": ("population", "capacity", "food", "tax pressure", "security", "health"),
        "writes": ("population", "health"),
        "depends_on": ("health_snapshot",),
        "notes": "Town growth/decline normalizes population before later migration and construction checks.",
    },
    {
        "id": "village_population",
        "label": "Village population and health",
        "files": ("src/triggers/ST04_weekly/entry_0102.py",),
        "reads": ("population", "capacity", "food", "security", "health"),
        "writes": ("population", "health"),
        "depends_on": ("health_snapshot",),
        "notes": "Village growth/decline runs beside town population before transfer passes.",
    },
    {
        "id": "migration",
        "label": "Migration and population transfers",
        "files": ("src/triggers/ST04_weekly/entry_0104.py",),
        "reads": ("population", "food pressure", "prosperity", "health", "relation"),
        "writes": ("source population", "destination population"),
        "depends_on": ("town_population", "village_population"),
        "notes": "Transfers use normalized post-growth populations and must precede final supply reconciliation.",
    },
    {
        "id": "security_desperation",
        "label": "Security, desperation, and population pressure",
        "files": ("src/triggers/ST04_weekly/entry_0105.py",),
        "reads": ("security profile", "economy profile", "population", "food pressure"),
        "writes": ("security pressure", "population"),
        "depends_on": ("migration",),
        "notes": "Security fallout applies after migration so centers do not both export and lose the same people unpredictably.",
    },
    {
        "id": "population_supply_reconcile",
        "label": "Population supply reconcile",
        "files": ("src/triggers/ST04_weekly/entry_0107.py",),
        "reads": ("final weekly population",),
        "writes": ("population supply",),
        "depends_on": ("security_desperation",),
        "notes": "Reconcile supply only after all weekly population writers have run.",
    },
    {
        "id": "construction",
        "label": "Construction advancement and AI starts",
        "files": ("src/triggers/ST04_weekly/entry_0123.py",),
        "reads": ("construction slots", "health", "prosperity", "food pressure", "buildings"),
        "writes": ("construction progress", "new AI construction project"),
        "depends_on": ("population_supply_reconcile",),
        "notes": "Construction reads the settled weekly center state and should not be moved before population/food/security.",
    },
    {
        "id": "late_faith_drift",
        "label": "Late faith drift",
        "files": ("src/triggers/ST04_weekly/entry_0132_five_faith_drift.py",),
        "reads": ("settled center state", "faith pressure"),
        "writes": ("faith support", "local faith"),
        "depends_on": ("construction",),
        "notes": "This is intentionally modeled as a late side effect because its trigger order is after construction.",
    },
    {
        "id": "goods_market_drift",
        "label": "Goods market drift",
        "files": ("src/triggers/ST04_weekly/entry_0160.py",),
        "reads": ("goods market profile", "settled center state"),
        "writes": ("wealth", "prosperity", "local prosperity"),
        "depends_on": ("late_faith_drift",),
        "notes": "Late market drift keeps economic side effects from fighting the tax snapshot or construction chooser.",
    },
    {
        "id": "prisoner_pressure",
        "label": "Prisoner weekly pressure",
        "files": ("src/triggers/ST04_weekly/entry_0162.py",),
        "reads": ("prisoner state", "center pressure"),
        "writes": ("late population/economy pressure",),
        "depends_on": ("goods_market_drift",),
        "notes": "Prisoner effects are late side effects and should not feed back into this week's core center tick.",
    },
)


EXPECTED_WRITE_APIS = (
    "script_sod_get_center_population_floor",
    "script_sod_center_apply_population_delta",
    "script_sod_center_transfer_population",
    "script_sod_center_apply_wealth_delta",
    "script_sod_center_apply_local_prosperity_delta",
    "script_sod_center_apply_health_delta",
    "script_sod_center_apply_rents_delta",
    "script_sod_center_apply_tariffs_delta",
    "script_sod_center_apply_food_delta",
    "script_sod_center_apply_cattle_delta",
)


WRITE_OWNERS = (
    ("building-derived center modifiers", "building_effects"),
    ("market snapshot inputs", "regional_goods_snapshot"),
    ("rents", "tax_revenue"),
    ("tariffs", "tax_revenue"),
    ("wealth", "tax_revenue, goods_market_drift"),
    ("local prosperity", "tax_revenue, goods_market_drift"),
    ("faith support", "faith_institutions, late_faith_drift"),
    ("local faith", "faith_institutions, late_faith_drift"),
    ("food stores", "building_food_stability"),
    ("civic stability", "building_food_stability"),
    ("law/security pressure", "law_pressure, security_desperation"),
    ("health", "faith_institutions, health_snapshot, town_population, village_population"),
    ("population", "town_population, village_population, migration, security_desperation"),
    ("population supply", "population_supply_reconcile"),
    ("construction progress", "construction"),
    ("new AI construction project", "construction"),
    ("late population/economy pressure", "prisoner_pressure"),
)


SAFETY_RULES = (
    "Do not move construction before population, food, health, and security have settled unless this map and its test are updated.",
    "Treat tax/revenue as a weekly snapshot. Later population or security drift should not retroactively rewrite that snapshot.",
    "Use sod_center_apply_* helpers for bounded writes where practical; legacy direct helpers should be isolated and documented.",
    "Profiles should primarily read. Pipeline stages that write should declare which center slots they mutate.",
    "Do not add a new center weekly pass after prisoner pressure unless it is intentionally a late side effect.",
    "If a pass both reads and writes the same pressure, document whether it is a snapshot pass or a finalization pass.",
)


def rel(path):
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path):
    return path.read_text(encoding="utf-8")


def order_key(path):
    prefix = "src/triggers/"
    if path.startswith(prefix):
        return path[len(prefix):]
    return path


def order_entries():
    entries = []
    for raw_line in read(ORDER_FILE).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(line)
    return entries


def validate_pipeline():
    issues = []
    entries = order_entries()
    order_index = {entry: index for index, entry in enumerate(entries)}
    stage_ids = set()
    seen_files = {}
    stage_order = {}

    previous_index = -1
    for stage_position, stage in enumerate(PIPELINE_STAGES):
        if stage["id"] in stage_ids:
            issues.append("Duplicate pipeline stage id: %s" % stage["id"])
        stage_ids.add(stage["id"])
        stage_order[stage["id"]] = stage_position

        main_file = stage["files"][0]
        key = order_key(main_file)
        full_path = ROOT / main_file
        if not full_path.exists():
            issues.append("Missing trigger file: %s" % main_file)
            continue
        if key not in order_index:
            issues.append("Trigger file is missing from %s: %s" % (rel(ORDER_FILE), key))
            continue
        stage_min_index = order_index[key]
        stage_max_index = order_index[key]
        previous_file_index = -1
        for stage_file in stage["files"]:
            stage_key = order_key(stage_file)
            if stage_file in seen_files:
                issues.append("Trigger file %s is owned by both %s and %s" % (stage_file, seen_files[stage_file], stage["id"]))
            seen_files[stage_file] = stage["id"]
            if stage_key in order_index:
                if order_index[stage_key] <= previous_file_index:
                    issues.append("Trigger file order regression inside %s at %s" % (stage["id"], stage_key))
                previous_file_index = order_index[stage_key]
                stage_min_index = min(stage_min_index, order_index[stage_key])
                stage_max_index = max(stage_max_index, order_index[stage_key])

        if stage_min_index <= previous_index:
            issues.append("Pipeline order regression at %s (%s)" % (stage["id"], key))
        previous_index = stage_max_index

        for extra_file in stage["files"][1:]:
            extra_key = order_key(extra_file)
            if not (ROOT / extra_file).exists():
                issues.append("Missing trigger file: %s" % extra_file)
            elif extra_key not in order_index:
                issues.append("Trigger file is missing from %s: %s" % (rel(ORDER_FILE), extra_key))

        for dependency in stage["depends_on"]:
            if dependency not in stage_ids:
                issues.append("Unknown dependency %s declared by %s" % (dependency, stage["id"]))
            elif stage_order[dependency] >= stage_position:
                issues.append("Dependency %s must run before %s" % (dependency, stage["id"]))

    pipeline_text = read(PIPELINE_FILE)
    for api_name in EXPECTED_WRITE_APIS:
        if api_name not in pipeline_text:
            issues.append("Missing canonical center write API: %s" % api_name)

    declared_writer_stages = set()
    for _, owner_text in WRITE_OWNERS:
        for owner in owner_text.split(","):
            owner = owner.strip()
            if owner:
                declared_writer_stages.add(owner)
    for owner in sorted(declared_writer_stages):
        if owner not in stage_ids:
            issues.append("Write ownership references unknown stage: %s" % owner)

    return issues


def render_report(issues):
    lines = [
        "# Center Tick Dependency Map",
        "",
        "Generated by `build/audit_center_tick_dependency_map.py`.",
        "",
        "This map makes the weekly center simulation order explicit so economy, food, population, security, health, faith, buildings, markets, threats, construction, and modifiers do not silently fight each other.",
        "",
        "## Validation",
        "",
    ]

    if issues:
        lines.append("Status: FAIL")
        lines.append("")
        for issue in issues:
            lines.append("- %s" % issue)
    else:
        lines.append("Status: OK")

    lines.extend([
        "",
        "## Pipeline Order",
        "",
        "| # | Stage | Trigger(s) | Reads | Writes | Depends on | Notes |",
        "| - | - | - | - | - | - | - |",
    ])

    for index, stage in enumerate(PIPELINE_STAGES, start=1):
        triggers = "<br>".join("`%s`" % item for item in stage["files"])
        reads = ", ".join(stage["reads"])
        writes = ", ".join(stage["writes"])
        depends = ", ".join(stage["depends_on"]) if stage["depends_on"] else "none"
        lines.append(
            "| %d | `%s` - %s | %s | %s | %s | %s | %s |"
            % (index, stage["id"], stage["label"], triggers, reads, writes, depends, stage["notes"])
        )

    lines.extend([
        "",
        "## Dependency Edges",
        "",
    ])

    for stage in PIPELINE_STAGES:
        if not stage["depends_on"]:
            lines.append("- root -> `%s`" % stage["id"])
        for dependency in stage["depends_on"]:
            lines.append("- `%s` -> `%s`" % (dependency, stage["id"]))

    lines.extend([
        "",
        "## Write APIs / Normalizers",
        "",
        "Canonical bounded center writes live in `%s`." % rel(PIPELINE_FILE),
        "",
    ])

    for api_name in EXPECTED_WRITE_APIS:
        lines.append("- `%s`" % api_name)

    lines.extend([
        "",
        "Legacy direct helpers still exist in older weekly passes. Prefer routing new center-state mutations through the bounded helpers above unless the older helper is intentionally preserving Native behavior.",
        "",
        "## Write Ownership",
        "",
        "| State family | Owning stage(s) |",
        "| - | - |",
    ])

    for state_family, owners in WRITE_OWNERS:
        lines.append("| %s | %s |" % (state_family, owners))

    lines.extend([
        "",
        "## Change Safety Rules",
        "",
    ])

    for rule in SAFETY_RULES:
        lines.append("- %s" % rule)

    lines.append("")
    return "\n".join(lines)


def main():
    issues = validate_pipeline()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render_report(issues), encoding="utf-8")
    print("Wrote %s" % rel(REPORT))
    if issues:
        print("Found %d center tick dependency issue(s)." % len(issues))
        return 1
    print("[center_tick_dependency_map] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
