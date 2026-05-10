# -*- coding: cp1254 -*-

"""Compatibility wrapper for legacy building-effect totals.

The center modifier system is now the canonical source. This script preserves
the old register contract used by existing center logic.
"""

from src.constants.module_constants import *


def _build_effect_total_ops():
    ops = [
        (store_script_param, ":center_no", 1),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_relations_weekly_flat),
        (assign, ":weekly_relations", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_prosperity_growth_flat),
        (assign, ":weekly_prosperity", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_local_faith_growth_flat),
        (assign, ":weekly_local_faith", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_global_faith_growth_flat),
        (assign, ":weekly_global_faith", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_renown_weekly_flat),
        (assign, ":weekly_renown", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_tax_efficiency_pct),
        (store_sub, ":weekly_income_percent", reg0, 100),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_health_cap_flat),
        (assign, ":center_health_bonus", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_prosperity_cap_flat),
        (assign, ":prosperity_cap_bonus", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_demesne_cost_flat),
        (assign, ":demesne_cost", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_weekly_upkeep_flat),
        (assign, ":weekly_upkeep", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_prosperity_growth_pct),
        (store_sub, ":prosperity_multiplier_percent", reg0, 100),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_population_capacity_flat),
        (assign, ":population_capacity_bonus", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_population_growth_flat),
        (assign, ":weekly_population_growth_bonus", reg0),
        (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_raid_recovery_flat),
        (assign, ":raid_recovery_bonus", reg0),
    ]
    ops.extend([
        (assign, reg0, ":weekly_relations"),
        (assign, reg1, ":weekly_prosperity"),
        (assign, reg2, ":weekly_local_faith"),
        (assign, reg3, ":weekly_global_faith"),
        (assign, reg4, ":weekly_renown"),
        (assign, reg5, ":weekly_income_percent"),
        (assign, reg6, ":center_health_bonus"),
        (assign, reg7, ":prosperity_cap_bonus"),
        (assign, reg8, ":demesne_cost"),
        (assign, reg9, ":weekly_upkeep"),
        (assign, reg10, ":prosperity_multiplier_percent"),
        (assign, reg11, ":population_capacity_bonus"),
        (assign, reg12, ":weekly_population_growth_bonus"),
        (assign, reg13, ":raid_recovery_bonus"),
    ])
    return ops


SCRIPTS = [
    ("get_center_building_effect_totals", _build_effect_total_ops()),
]
