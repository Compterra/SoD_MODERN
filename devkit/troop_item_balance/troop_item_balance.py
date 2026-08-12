#!/usr/bin/env python3
"""Troop + Item Balance Lab for the Mount & Blade 1.011 module system.

This is deliberately a *compatibility bridge* over SoD Modern's two legacy
authoring lists: ``compile/module_items.py`` and ``compile/module_troops.py``.
They are consumed by the M&B 1.011 processor pipeline, but are not rebuilt
from the modular ``src/`` folders.  The Lab therefore makes the distinction
visible instead of pretending that a generated/export file is safe to edit.

Primary interfaces are deterministic JSON CLI and MCP.  The optional Module
Studio surface is only a convenience adapter over these exact functions.

The viewer evaluates the existing legacy module data in a short-lived child
Python process with the same compile/header/ID import ordering used by the
normal builder.  It never writes during evaluation.  Semantic edits are
limited to balance-oriented record fields, produce an exact unified diff, are
SHA-guarded, dry-run by default, and require an explicit acknowledgement
before the legacy compile authoring input is changed.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Any, Iterable, Mapping, Sequence


TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = TOOL_DIR.parents[1]

BALANCE_VERSION = "0.8.0"
MAX_QUERY_LENGTH = 500
MAX_RESULT_LIMIT = 500
MAX_DIFF_LINES = 700
SHA256_RE = re.compile(r"[0-9a-f]{64}")
ITEM_CODE_RE = re.compile(r"(?:itm_)?([A-Za-z_][A-Za-z0-9_]*)$")
TROOP_CODE_RE = re.compile(r"(?:trp_)?([A-Za-z_][A-Za-z0-9_]*)$")
ID_LINE_RE = re.compile(r"^\s*(?P<symbol>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<value>-?\d+)\s*$")
STRING_ASSIGNMENT_RE = re.compile(
    r"^\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<quote>[\"'])(?P<value>[^\"']+)(?P=quote)",
    re.MULTILINE,
)

ITEM_SOURCE_RELATIVE = Path("compile/module_items.py")
TROOP_SOURCE_RELATIVE = Path("compile/module_troops.py")
PARTY_TEMPLATE_SOURCE_RELATIVE = Path("compile/module_party_templates.py")
ITEM_IDS_RELATIVE = Path("compile/ids/ID_items.py")
TROOP_IDS_RELATIVE = Path("compile/ids/ID_troops.py")
FACTION_IDS_RELATIVE = Path("compile/ids/ID_factions.py")
PARTY_IDS_RELATIVE = Path("compile/ids/ID_parties.py")
FAITH_ASCENSION_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_troop_get_faith_upgrade.py")
FAITH_CANDIDATE_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_troop_find_faith_candidate.py")
IMPERIAL_EXPEDITION_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_imperial_expedition.py")
IMPERIAL_PRE_INVASION_SOURCE_RELATIVE = Path("src/triggers/ST03_daily/entry_0088.py")
IMPERIAL_GAME_START_SOURCE_RELATIVE = Path("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
IMPERIAL_DOCTRINE_SOURCE_RELATIVE = Path("src/scripts/_preamble/00_imports.py")
PLAYER_FACTION_ACTIVATION_SOURCE_RELATIVE = Path("src/scripts/ZF_factions/activate_deactivate_player_faction.py")
PARTY_REINFORCEMENT_SOURCE_RELATIVE = Path("src/scripts/ZC_parties/cf_reinforce_party.py")
CONSTANTS_SOURCE_RELATIVE = Path("src/constants/module_constants.py")
IMPERIAL_CORE_TEMPLATE_CODES = (
    "kingdom_6_reinforcements_a",
    "kingdom_6_reinforcements_b",
    "kingdom_6_reinforcements_c",
)
IMPERIAL_AUXILIARY_TEMPLATE_CODE = "legion_mercenaries"

# The cultures below are alternative player starts, not an aggregate in-world
# faction. The template bindings are read from the activation script so the
# profile follows the currently selected culture rather than template names.
PLAYER_START_CULTURES: tuple[dict[str, str], ...] = (
    {
        "id": "antarian",
        "name": "Antarian",
        "country": "cb_antares",
        "roster_id": "culture:antarian",
        "cohort_id": "campaign:player-start:antarian",
        "doctrine": "Armored foot and shielded javelin formations with secondary cavalry.",
    },
    {
        "id": "marinian",
        "name": "Marinian",
        "country": "cb_marina",
        "roster_id": "culture:marinian",
        "cohort_id": "campaign:player-start:marinian",
        "doctrine": "Disciplined foot and crossbow formations with limited scouting cavalry.",
    },
    {
        "id": "adenian",
        "name": "Adenian",
        "country": "cb_aden",
        "roster_id": "culture:adenian",
        "cohort_id": "campaign:player-start:adenian",
        "doctrine": "Combined-arms chivalric cavalry backed by practical foot and bow support.",
    },
    {
        "id": "villianese",
        "name": "Villianese",
        "country": "cb_villian",
        "roster_id": "culture:villianese",
        "cohort_id": "campaign:player-start:villianese",
        "doctrine": "Longbow pressure with shielded foot support and mobile scouting screens.",
    },
    {
        "id": "zerrikanian",
        "name": "Zerrikanian",
        "country": "cb_zerrikan",
        "roster_id": "culture:zerrikanian",
        "cohort_id": "campaign:player-start:zerrikanian",
        "doctrine": "Mobile horse-archer and cavalry field force supported by foot garrisons.",
    },
)
PLAYER_START_REINFORCEMENT_CONTEXTS: dict[str, tuple[tuple[str, float], ...]] = {
    "garrison": (("a", 0.65), ("b", 0.35)),
    "lord": (("a", 0.50), ("b", 0.25), ("c", 0.25)),
}
PLAYER_START_MAX_PRESSURE_SPREAD = {"garrison": 1.35, "lord": 1.35}
PLAYER_START_ROSTER_IDS = frozenset(culture["roster_id"] for culture in PLAYER_START_CULTURES)

# Unlike the five SoD player cultures, the Native kingdoms coexist throughout
# a normal campaign. Their A/B/C reinforcement templates therefore form one
# bounded campaign balance group, while their troop themes stay distinct.
NATIVE_KINGDOMS: tuple[dict[str, str], ...] = (
    {
        "id": "kingdom_1",
        "name": "Kingdom of Swadia",
        "faction": "kingdom_1",
        "culture": "culture_1",
        "culture_constant": "fac_culture_1",
        "troop_prefix": "swadian_",
        "cohort_id": "campaign:native:kingdom_1",
        "doctrine": "Heavy cavalry shock supported by crossbows, polearms, and a flexible infantry line.",
    },
    {
        "id": "kingdom_2",
        "name": "Kingdom of Vaegirs",
        "faction": "kingdom_2",
        "culture": "culture_2",
        "culture_constant": "fac_culture_2",
        "troop_prefix": "vaegir_",
        "cohort_id": "campaign:native:kingdom_2",
        "doctrine": "Bow pressure backed by adaptable infantry and a smaller but capable cavalry branch.",
    },
    {
        "id": "kingdom_3",
        "name": "Khergit Khanate",
        "faction": "kingdom_3",
        "culture": "culture_3",
        "culture_constant": "fac_culture_3",
        "troop_prefix": "khergit_",
        "cohort_id": "campaign:native:kingdom_3",
        "doctrine": "All-mounted field pressure built around horse archery, scouting mobility, and lancers.",
    },
    {
        "id": "kingdom_4",
        "name": "Kingdom of Nords",
        "faction": "kingdom_4",
        "culture": "culture_4",
        "culture_constant": "fac_culture_4",
        "troop_prefix": "nord_",
        "cohort_id": "campaign:native:kingdom_4",
        "doctrine": "Shielded axe infantry and thrown weapons with limited but useful bow support.",
    },
    {
        "id": "kingdom_5",
        "name": "Rhodok Republic",
        "faction": "kingdom_5",
        "culture": "culture_5",
        "culture_constant": "fac_culture_5",
        "troop_prefix": "rhodok_",
        "cohort_id": "campaign:native:kingdom_5",
        "doctrine": "Pike-and-shield defense and crossbow fire support with no conventional cavalry branch.",
    },
)
NATIVE_REINFORCEMENT_CONTEXTS = PLAYER_START_REINFORCEMENT_CONTEXTS
NATIVE_KINGDOM_MAX_PRESSURE_SPREAD = {"garrison": 1.45, "lord": 1.45}

# Mercenary guilds coexist with the campaign, but are contract specialists rather
# than territorial peers. Their static report therefore audits job fit, runtime
# roster identity, and access pressure instead of averaging them into factions.
MERCENARY_GUILDS: tuple[dict[str, Any], ...] = (
    {
        "id": "black_army",
        "name": "Black Army",
        "faction": "sod_merc_guild1",
        "doctrine": "Professional security force: reliable patrol, garrison, and field service with limited logistics.",
        "base_troops": ("black_army_fresh_blade", "black_army_line_supporter"),
        "noble_troop": "black_army_raven_captain",
        "primary_roles": ("patrol", "garrison_support", "field_company"),
        "deprioritized_roles": ("supply_column",),
    },
    {
        "id": "conquistadors",
        "name": "Conquistadors",
        "faction": "sod_merc_guild2",
        "doctrine": "Pike, shield, and crossbow formations for protected supply work, walls, and disciplined field battles.",
        "base_troops": ("conquistador_footman", "conquistador_crossbowman"),
        "noble_troop": "conquistador_lancer",
        "primary_roles": ("supply_column", "garrison_support", "field_company"),
        "deprioritized_roles": (),
    },
    {
        "id": "elephant_guard",
        "name": "Elephant Guard",
        "faction": "sod_merc_guild3",
        "doctrine": "Warden infantry for community defense and anti-slaver protection crises.",
        "base_troops": ("elephant_guard_tribesman", "elephant_guard_spearman"),
        "noble_troop": "elephant_guard_battle_shaman",
        "primary_roles": ("garrison_support", "special_world_activity"),
        "deprioritized_roles": ("supply_column",),
    },
    {
        "id": "jotnar_clan",
        "name": "Jotnar Clan",
        "faction": "sod_merc_guild4",
        "doctrine": "Hearth defenders and durable field infantry, with mobile Volva screens but little caravan specialization.",
        "base_troops": ("jotnar_clan_volva", "jotnar_clan_armsman"),
        "noble_troop": "jotnar_clan_norn_mistress",
        "primary_roles": ("garrison_support", "field_company"),
        "deprioritized_roles": ("supply_column", "escort"),
    },
    {
        "id": "serpent_host",
        "name": "Serpent Host",
        "faction": "sod_merc_guild5",
        "doctrine": "Route control and open-field tempo through mobile cavalry screens, not static wall duty.",
        "base_troops": ("serpent_host_akinci", "serpent_host_kapikulu"),
        "noble_troop": "serpent_host_basilisk_knight",
        "primary_roles": ("escort", "patrol", "field_company"),
        "deprioritized_roles": ("garrison_support",),
    },
    {
        "id": "slavers",
        "name": "Slavers",
        "faction": "sod_merc_guild6",
        "doctrine": "Capture and prisoner-economy specialists whose civic service remains intentionally unattractive.",
        "base_troops": ("henchman", "slave"),
        "noble_troop": "tormenter",
        "primary_roles": ("special_world_activity", "field_company"),
        "deprioritized_roles": ("garrison_support", "supply_column"),
    },
    {
        "id": "boar_clan",
        "name": "Boar Clan",
        "faction": "sod_merc_guild7",
        "doctrine": "Frontier pressure and raiding riders for patrols and special work, not relief or town guard duty.",
        "base_troops": ("boar_clan_clansman", "boar_clan_rider"),
        "noble_troop": "boar_clan_tusk_rider",
        "primary_roles": ("patrol", "special_world_activity", "field_company"),
        "deprioritized_roles": ("garrison_support", "supply_column"),
    },
)
MERCENARY_ROLE_LABELS = {
    "field_company": "field company",
    "patrol": "patrol",
    "escort": "escort",
    "supply_column": "supply column",
    "mercenary_lord": "mercenary-lord service",
    "garrison_support": "garrison support",
    "special_world_activity": "special world activity",
}
MERCENARY_ROLE_FIT_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_merc_market_calculate_guild_role_fit.py")
MERCENARY_CONTRACT_ROSTER_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_merc_guild_get_contract_roster.py")
MERCENARY_SELECTION_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_merc_market_select_preferred_guild.py")
MERCENARY_BID_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_merc_market_generate_bid.py")
MERCENARY_ACCEPT_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_merc_market_try_accept_bid.py")
MERCENARY_DEPLOY_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_merc_market_deploy_ai_contract.py")
MERCENARY_SPAWN_SOURCE_RELATIVE = Path("src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py")
MERCENARY_DIALOGUE_SOURCE_RELATIVE = Path("src/scripts/ZY_helper_scripts/sod_merc_market_describe_ai_contract_to_s68.py")

# These roster families are stricter than a raw faction lookup. The five SoD
# cultures share the player-supporter faction at runtime, but their equipment
# themes and progression routes must not be treated as one interchangeable pool.
ROSTER_FAMILY_RULES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("culture:antarian", "Antarian", ("sod_ant_", "sod_peasant1")),
    ("culture:marinian", "Marinian", ("sod_mar_", "sod_peasant2")),
    ("culture:adenian", "Adenian", ("sod_ade_", "sod_peasant3")),
    ("culture:villianese", "Villianese", ("sod_vil_", "sod_peasant4")),
    ("culture:zerrikanian", "Zerrikanian", ("sod_zer_", "sod_peasant5")),
    ("faith:the-one", "Faith: The One", ("sod_faith1_",)),
    ("faith:old-gods", "Faith: Old Gods", ("sod_faith2_",)),
    ("faith:the-void", "Faith: The Void", ("sod_faith3_",)),
    ("faith:enlightenment", "Faith: Enlightenment", ("sod_faith4_",)),
    ("faith:atheism", "Faith: Atheism", ("sod_faith5_",)),
)
RANK_ORDER = {"Normal": 1, "Noble": 2, "Faith/Zealot": 3}

# A roster family says which equipment and troop identity can be reviewed
# together. A campaign cohort says which forces actually coexist in a run.
# These are deliberately separate concepts: the five SoD cultures share a
# runtime faction, but only one is selected at new-game start.
CAMPAIGN_COHORTS: dict[str, dict[str, str]] = {
    "campaign:player-start:antarian": {
        "id": "campaign:player-start:antarian",
        "name": "Player start: Antarian",
        "campaign_group": "player_start_cultures",
        "campaign_role": "mutually_exclusive_player_start",
        "presence": "One culture is selected at new-game start; the other four SoD cultures do not spawn in that campaign.",
        "analysis_policy": "Analyze this culture as its own player-progression baseline; never average all five player-start cultures into a fake in-campaign faction.",
    },
    "campaign:player-start:marinian": {
        "id": "campaign:player-start:marinian",
        "name": "Player start: Marinian",
        "campaign_group": "player_start_cultures",
        "campaign_role": "mutually_exclusive_player_start",
        "presence": "One culture is selected at new-game start; the other four SoD cultures do not spawn in that campaign.",
        "analysis_policy": "Analyze this culture as its own player-progression baseline; never average all five player-start cultures into a fake in-campaign faction.",
    },
    "campaign:player-start:adenian": {
        "id": "campaign:player-start:adenian",
        "name": "Player start: Adenian",
        "campaign_group": "player_start_cultures",
        "campaign_role": "mutually_exclusive_player_start",
        "presence": "One culture is selected at new-game start; the other four SoD cultures do not spawn in that campaign.",
        "analysis_policy": "Analyze this culture as its own player-progression baseline; never average all five player-start cultures into a fake in-campaign faction.",
    },
    "campaign:player-start:villianese": {
        "id": "campaign:player-start:villianese",
        "name": "Player start: Villianese",
        "campaign_group": "player_start_cultures",
        "campaign_role": "mutually_exclusive_player_start",
        "presence": "One culture is selected at new-game start; the other four SoD cultures do not spawn in that campaign.",
        "analysis_policy": "Analyze this culture as its own player-progression baseline; never average all five player-start cultures into a fake in-campaign faction.",
    },
    "campaign:player-start:zerrikanian": {
        "id": "campaign:player-start:zerrikanian",
        "name": "Player start: Zerrikanian",
        "campaign_group": "player_start_cultures",
        "campaign_role": "mutually_exclusive_player_start",
        "presence": "One culture is selected at new-game start; the other four SoD cultures do not spawn in that campaign.",
        "analysis_policy": "Analyze this culture as its own player-progression baseline; never average all five player-start cultures into a fake in-campaign faction.",
    },
    "campaign:native:kingdom_1": {
        "id": "campaign:native:kingdom_1",
        "name": "Native Calradia: Kingdom of Swadia",
        "campaign_group": "native_world_kingdoms",
        "campaign_role": "persistent_world_realm",
        "presence": "Coexists with the other native kingdoms throughout the normal campaign.",
        "analysis_policy": "Compare role, access, reinforcement composition, and campaign pressure without treating it as a player-start culture.",
    },
    "campaign:native:kingdom_2": {
        "id": "campaign:native:kingdom_2",
        "name": "Native Calradia: Kingdom of Vaegirs",
        "campaign_group": "native_world_kingdoms",
        "campaign_role": "persistent_world_realm",
        "presence": "Coexists with the other native kingdoms throughout the normal campaign.",
        "analysis_policy": "Compare role, access, reinforcement composition, and campaign pressure without treating it as a player-start culture.",
    },
    "campaign:native:kingdom_3": {
        "id": "campaign:native:kingdom_3",
        "name": "Native Calradia: Khergit Khanate",
        "campaign_group": "native_world_kingdoms",
        "campaign_role": "persistent_world_realm",
        "presence": "Coexists with the other native kingdoms throughout the normal campaign.",
        "analysis_policy": "Compare role, access, reinforcement composition, and campaign pressure without treating it as a player-start culture.",
    },
    "campaign:native:kingdom_4": {
        "id": "campaign:native:kingdom_4",
        "name": "Native Calradia: Kingdom of Nords",
        "campaign_group": "native_world_kingdoms",
        "campaign_role": "persistent_world_realm",
        "presence": "Coexists with the other native kingdoms throughout the normal campaign.",
        "analysis_policy": "Compare role, access, reinforcement composition, and campaign pressure without treating it as a player-start culture.",
    },
    "campaign:native:kingdom_5": {
        "id": "campaign:native:kingdom_5",
        "name": "Native Calradia: Rhodok Republic",
        "campaign_group": "native_world_kingdoms",
        "campaign_role": "persistent_world_realm",
        "presence": "Coexists with the other native kingdoms throughout the normal campaign.",
        "analysis_policy": "Compare role, access, reinforcement composition, and campaign pressure without treating it as a player-start culture.",
    },
    "campaign:imperial-expedition": {
        "id": "campaign:imperial-expedition",
        "name": "Imperial Expeditionary Force",
        "campaign_group": "endgame_invasion",
        "campaign_role": "delayed_boss_invasion",
        "presence": "Inactive until the invasion event; organized into named reinforcement waves and total war after arrival.",
        "analysis_policy": "Do not normalize this as a steady-state faction. Review wave composition, supply, pressure, total-war behavior, attrition, and counterplay together.",
    },
    "campaign:imperial-auxiliaries": {
        "id": "campaign:imperial-auxiliaries",
        "name": "Imperial advance auxiliaries",
        "campaign_group": "endgame_invasion",
        "campaign_role": "pre_invasion_support",
        "presence": "Legion auxiliaries stage before the main expedition rather than functioning as an ordinary mercenary market.",
        "analysis_policy": "Review as an early-warning and preparation layer of the invasion, not as a player-hireable peer of normal mercenary companies.",
    },
    "campaign:faith-access": {
        "id": "campaign:faith-access",
        "name": "Faith and Zealot access layers",
        "campaign_group": "elite_access_overlays",
        "campaign_role": "gated_elite_overlay",
        "presence": "Faith troops are unlocked through a selected culture's noble and institutional progression, not spawned as five independent territorial factions.",
        "analysis_policy": "Compare against the originating culture's top noble and the full faith-gate burden, not against bulk normal recruitment.",
    },
}
ROSTER_COHORT_IDS = {
    "culture:antarian": "campaign:player-start:antarian",
    "culture:marinian": "campaign:player-start:marinian",
    "culture:adenian": "campaign:player-start:adenian",
    "culture:villianese": "campaign:player-start:villianese",
    "culture:zerrikanian": "campaign:player-start:zerrikanian",
    "faith:the-one": "campaign:faith-access",
    "faith:old-gods": "campaign:faith-access",
    "faith:the-void": "campaign:faith-access",
    "faith:enlightenment": "campaign:faith-access",
    "faith:atheism": "campaign:faith-access",
}
FACTION_COHORT_IDS = {
    "kingdom_1": "campaign:native:kingdom_1",
    "kingdom_2": "campaign:native:kingdom_2",
    "kingdom_3": "campaign:native:kingdom_3",
    "kingdom_4": "campaign:native:kingdom_4",
    "kingdom_5": "campaign:native:kingdom_5",
    "kingdom_6": "campaign:imperial-expedition",
    "kingdom_6_mercenaries": "campaign:imperial-auxiliaries",
}

HARDWIRED_ITEMS = {"no_item": 0, "horse_meat": 1}
HARDWIRED_TROOPS = {
    "player": 0,
    "temp_troop": 1,
    "game": 2,
    "unarmed_troop": 3,
}

ITEM_TYPES = {
    1: "Horse",
    2: "One-handed",
    3: "Two-handed",
    4: "Polearm",
    5: "Arrows",
    6: "Bolts",
    7: "Shield",
    8: "Bow",
    9: "Crossbow",
    10: "Thrown",
    11: "Goods",
    12: "Head armor",
    13: "Body armor",
    14: "Foot armor",
    15: "Hand armor",
    16: "Pistol",
    17: "Musket",
    18: "Bullets",
    19: "Animal",
    20: "Book",
}
ITEM_TYPE_BY_NAME = {name.casefold(): value for value, name in ITEM_TYPES.items()}
ITEM_TYPE_BY_NAME.update(
    {
        "1h": 2,
        "one handed": 2,
        "2h": 3,
        "two handed": 3,
        "head": 12,
        "body": 13,
        "foot": 14,
        "hands": 15,
        "hand": 15,
    }
)

ITEM_TYPE_MELEE = frozenset({2, 3, 4})
ITEM_TYPE_FIREARM = frozenset({16, 17})
ITEM_TYPE_RANGED = frozenset({8, 9, 10, 16, 17})
ITEM_TYPE_AMMO = frozenset({5, 6, 18})
ITEM_TYPE_ARMOR = frozenset({12, 13, 14, 15})

TF_HERO = 0x00000010
TF_MOUNTED = 0x00000400
TF_GUARANTEE_BOOTS = 0x00100000
TF_GUARANTEE_ARMOR = 0x00200000
TF_GUARANTEE_HELMET = 0x00400000
TF_GUARANTEE_GLOVES = 0x00800000
TF_GUARANTEE_HORSE = 0x01000000
TF_GUARANTEE_SHIELD = 0x02000000
TF_GUARANTEE_RANGED = 0x04000000
ITP_MERCHANDISE = 0x00010000
ITP_UNIQUE = 0x00001000

PROFICIENCY_BITS = {
    "one_handed": 0,
    "two_handed": 10,
    "polearm": 20,
    "archery": 30,
    "crossbow": 40,
    "throwing": 50,
    "firearm": 60,
}
PROFICIENCY_FUNCTIONS = {
    "one_handed": "wp_one_handed",
    "two_handed": "wp_two_handed",
    "polearm": "wp_polearm",
    "archery": "wp_archery",
    "crossbow": "wp_crossbow",
    "throwing": "wp_throwing",
    "firearm": "wp_firearm",
}

SKILL_SLOTS = {
    0: "trade",
    1: "leadership",
    2: "prisoner_management",
    3: "reserved_1",
    4: "reserved_2",
    5: "reserved_3",
    6: "reserved_4",
    7: "reserved_5",
    8: "engineer",
    9: "first_aid",
    10: "surgery",
    11: "wound_treatment",
    12: "inventory_management",
    13: "spotting",
    14: "pathfinding",
    15: "tactics",
    16: "tracking",
    17: "trainer",
    18: "reserved_6",
    19: "reserved_7",
    20: "reserved_8",
    21: "reserved_9",
    22: "reserved_10",
    23: "horse_archery",
    24: "riding",
    25: "athletics",
    26: "shield",
    27: "weapon_master",
    28: "reserved_11",
    29: "reserved_12",
    30: "reserved_13",
    31: "reserved_14",
    32: "reserved_15",
    33: "power_draw",
    34: "power_throw",
    35: "power_strike",
    36: "ironflesh",
    37: "reserved_16",
    38: "reserved_17",
    39: "reserved_18",
    40: "reserved_19",
    41: "reserved_20",
}
SKILL_NAME_TO_SLOT = {name: slot for slot, name in SKILL_SLOTS.items()}
COMBAT_SKILL_NAMES = (
    "horse_archery",
    "riding",
    "athletics",
    "shield",
    "weapon_master",
    "power_draw",
    "power_throw",
    "power_strike",
    "ironflesh",
)
HARD_LOADOUT_NOTES = frozenset(
    {
        "shield_guaranteed_but_no_shield_in_inventory",
        "mounted_role_without_mount_item",
        "no_weapon_item",
        "unknown_item_index_in_inventory",
    }
)

STAT_ALIASES = {
    "weight": "weight",
    "difficulty": "difficulty",
    "head_armor": "head_armor",
    "body_armor": "body_armor",
    "leg_armor": "leg_armor",
    "hit_points": "hit_points",
    "speed_rating": "spd_rtng",
    "spd_rtng": "spd_rtng",
    "missile_speed": "shoot_speed",
    "shoot_speed": "shoot_speed",
    "weapon_length": "weapon_length",
    "max_ammo": "max_ammo",
    "abundance": "abundance",
    "accuracy": "accuracy",
    "horse_speed": "horse_speed",
    "horse_maneuver": "horse_maneuver",
    "horse_charge": "horse_charge",
    "food_quality": "food_quality",
    "swing_damage": "swing_damage",
    "thrust_damage": "thrust_damage",
}
DAMAGE_STAT_FUNCTIONS = frozenset({"swing_damage", "thrust_damage"})
DAMAGE_TYPES = frozenset({"cut", "pierce", "blunt"})


class BalanceError(RuntimeError):
    """A troop/item balance request cannot be completed safely."""


@dataclass(frozen=True)
class SourceRecord:
    kind: str
    code: str
    path: Path
    source_text: str
    node: ast.List
    origin: str


@dataclass(frozen=True)
class ItemRecord:
    index: int
    code: str
    data: tuple[Any, ...]


@dataclass(frozen=True)
class TroopRecord:
    index: int
    code: str
    data: tuple[Any, ...]
    origin: str


@dataclass(frozen=True)
class UpgradeEdge:
    source: str
    target: str
    declaration: str
    path: Path
    line: int


@dataclass(frozen=True)
class PartyTemplateStack:
    troop_code: str
    minimum: int
    maximum: int


@dataclass(frozen=True)
class PartyTemplateRecord:
    code: str
    name: str
    faction_code: str | None
    stacks: tuple[PartyTemplateStack, ...]
    path: Path
    line: int


@dataclass(frozen=True)
class Replacement:
    start: int
    end: int
    before: str
    after: str
    label: str


@dataclass
class BalanceIndex:
    root: Path
    items_path: Path
    troops_path: Path
    party_templates_path: Path
    items: tuple[ItemRecord, ...]
    troops: tuple[TroopRecord, ...]
    party_templates: tuple[PartyTemplateRecord, ...]
    item_by_code: dict[str, ItemRecord]
    troop_by_code: dict[str, TroopRecord]
    source_records: dict[tuple[str, str], SourceRecord]
    upgrades: tuple[UpgradeEdge, ...]
    faith_candidate_routes: tuple[UpgradeEdge, ...]
    faith_ascensions: tuple[UpgradeEdge, ...]
    upgrade_depths: dict[str, int]
    faction_by_index: dict[int, str]
    faction_name_by_index: dict[int, str]
    item_ids: dict[str, int]
    troop_ids: dict[str, int]
    party_ids: dict[str, int]
    item_users: dict[int, tuple[str, ...]]
    noble_troop_codes: frozenset[str]
    faith_troop_codes: frozenset[str]
    noble_track_codes: frozenset[str]
    faith_candidate_codes: frozenset[str]
    source_authority: dict[str, Any]


_CACHE: dict[Path, tuple[tuple[tuple[str, int, int], ...], BalanceIndex]] = {}


def project_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def require_string(value: Any, *, name: str, maximum: int = MAX_QUERY_LENGTH) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BalanceError(f"{name} must be a non-empty string.")
    result = value.strip()
    if len(result) > maximum:
        raise BalanceError(f"{name} must be at most {maximum:,} characters.")
    return result


def optional_string(value: Any, *, name: str, maximum: int = MAX_QUERY_LENGTH) -> str | None:
    if value is None or value == "":
        return None
    return require_string(value, name=name, maximum=maximum)


def require_limit(value: Any, *, name: str = "limit", maximum: int = MAX_RESULT_LIMIT) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise BalanceError(f"{name} must be an integer from 1 through {maximum}.")
    return value


def require_int(value: Any, *, name: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise BalanceError(f"{name} must be an integer from {minimum} through {maximum}.")
    return value


def require_number(value: Any, *, name: str, minimum: float, maximum: float) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise BalanceError(f"{name} must be a number.")
    result = float(value)
    if not minimum <= result <= maximum:
        raise BalanceError(f"{name} must be from {minimum:g} through {maximum:g}.")
    return int(value) if isinstance(value, int) else result


def require_mapping(value: Any, *, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise BalanceError(f"{name} must be a JSON object.")
    return value


def require_sha256(value: Any, *, name: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value.strip().lower()) is None:
        raise BalanceError(f"{name} must be a 64-character lowercase SHA-256 returned by balance_patch.")
    return value.strip().lower()


def normalize_item_code(value: Any) -> str:
    raw = require_string(value, name="item_id", maximum=180)
    raw = raw.removeprefix("item:")
    match = ITEM_CODE_RE.fullmatch(raw)
    if match is None:
        raise BalanceError("item_id must be an item code such as sword or itm_sword.")
    return match.group(1)


def normalize_troop_code(value: Any) -> str:
    raw = require_string(value, name="troop_id", maximum=180)
    raw = raw.removeprefix("troop:")
    match = TROOP_CODE_RE.fullmatch(raw)
    if match is None:
        raise BalanceError("troop_id must be a troop code such as swadian_recruit or trp_swadian_recruit.")
    return match.group(1)


def normalize_entity_kind(value: Any) -> str:
    result = require_string(value, name="entity_kind", maximum=40).casefold().replace("_", "-")
    if result in {"item", "items"}:
        return "item"
    if result in {"troop", "troops"}:
        return "troop"
    raise BalanceError("entity_kind must be 'item' or 'troop'.")


def normalize_entity_code(kind: str, value: Any) -> str:
    return normalize_item_code(value) if kind == "item" else normalize_troop_code(value)


def _lookup_item(index: "BalanceIndex", code: str) -> "ItemRecord | None":
    """Resolve an authored item code without making IDs case-sensitive by accident.

    The legacy module source has a small number of mixed-case troop/item
    identifiers while generated ``ID_*.py`` symbols normalize some of them.
    Source retains its exact spelling; lookup accepts an unambiguous
    case-insensitive spelling for agent ergonomics.
    """

    direct = index.item_by_code.get(code)
    if direct is not None:
        return direct
    matches = [record for candidate, record in index.item_by_code.items() if candidate.casefold() == code.casefold()]
    return matches[0] if len(matches) == 1 else None


def _lookup_troop(index: "BalanceIndex", code: str) -> "TroopRecord | None":
    direct = index.troop_by_code.get(code)
    if direct is not None:
        return direct
    matches = [record for candidate, record in index.troop_by_code.items() if candidate.casefold() == code.casefold()]
    return matches[0] if len(matches) == 1 else None


def _read_utf8_source(path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise BalanceError(f"Could not read {path}: {error}") from error
    if raw.startswith(b"\xef\xbb\xbf"):
        raise BalanceError(f"{path.name} has a UTF-8 BOM; Balance Lab refuses to rewrite it because preserving this legacy encoding is ambiguous.")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise BalanceError(f"{path.name} must be UTF-8 for guarded semantic patching: {error}") from error


def _source_signature(root: Path) -> tuple[tuple[str, int, int], ...]:
    relevant = [
        root / ITEM_SOURCE_RELATIVE,
        root / TROOP_SOURCE_RELATIVE,
        root / PARTY_TEMPLATE_SOURCE_RELATIVE,
        root / ITEM_IDS_RELATIVE,
        root / TROOP_IDS_RELATIVE,
        root / FACTION_IDS_RELATIVE,
        root / PARTY_IDS_RELATIVE,
        root / "compile/module_constants.py",
        root / CONSTANTS_SOURCE_RELATIVE,
        root / "compile/module_factions.py",
        root / FAITH_ASCENSION_SOURCE_RELATIVE,
        root / FAITH_CANDIDATE_SOURCE_RELATIVE,
        root / IMPERIAL_EXPEDITION_SOURCE_RELATIVE,
        root / IMPERIAL_PRE_INVASION_SOURCE_RELATIVE,
        root / IMPERIAL_GAME_START_SOURCE_RELATIVE,
        root / IMPERIAL_DOCTRINE_SOURCE_RELATIVE,
        root / "build_module.bat",
        root / "build/build_all.py",
        *sorted((root / "compile/headers").glob("*.py"), key=lambda path: path.name.casefold()),
    ]
    rows: list[tuple[str, int, int]] = []
    for path in relevant:
        try:
            stat = path.stat()
        except OSError:
            continue
        rows.append((project_relative(path, root), stat.st_mtime_ns, stat.st_size))
    return tuple(rows)


_LOADER_MARKER = "__SOD_BALANCE_LOADER_JSON__="
_LOADER_SOURCE = r'''
import importlib
import json
import sys
from pathlib import Path

root = Path.cwd()
paths = [root / "compile" / "ids", root / "compile", root / "compile" / "headers", root / "compile" / "process", root]
for candidate in reversed(paths):
    candidate_text = str(candidate)
    if candidate_text not in sys.path:
        sys.path.insert(0, candidate_text)

module_items = importlib.import_module("module_items")
module_troops = importlib.import_module("module_troops")
module_factions = importlib.import_module("module_factions")
payload = {
    "items": module_items.items,
    "troops": module_troops.troops,
    "factions": module_factions.factions,
    "noble_troops": list(getattr(module_troops, "sod_noble_troops", [])),
    "faith_troops": list(getattr(module_troops, "sod_faith_troops", [])),
}
print("__SOD_BALANCE_LOADER_JSON__=" + json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
'''


def _load_runtime_module_data(root: Path) -> dict[str, Any]:
    """Evaluate legacy compile inputs in an isolated, non-writing child process.

    The M&B module system uses Python helper expressions extensively.  A pure
    AST evaluator would silently diverge from the actual process pipeline for
    helper functions, upgrade calls, and header bit packing.  This evaluates
    only the known local compile/header/ID graph in a short-lived child just as
    the standard build does, captures its data, and keeps the DevKit process
    free of imported authored modules.
    """

    try:
        completed = subprocess.run(
            [sys.executable, "-B", "-c", _LOADER_SOURCE],
            cwd=str(root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=45,
            check=False,
        )
    except OSError as error:
        raise BalanceError(f"Could not start isolated legacy module evaluation: {error}") from error
    except subprocess.TimeoutExpired as error:
        raise BalanceError("Isolated legacy module evaluation exceeded 45 seconds.") from error
    marker_index = completed.stdout.rfind(_LOADER_MARKER)
    if completed.returncode != 0 or marker_index < 0:
        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        detail = stderr or stdout or f"exit code {completed.returncode}"
        raise BalanceError("Could not evaluate legacy troop/item authoring data: " + detail[-2_000:])
    encoded = completed.stdout[marker_index + len(_LOADER_MARKER) :].strip()
    try:
        payload = json.loads(encoded)
    except json.JSONDecodeError as error:
        raise BalanceError(f"Isolated legacy module evaluator returned invalid JSON: {error}") from error
    if not isinstance(payload, dict) or not all(isinstance(payload.get(key), list) for key in ("items", "troops", "factions", "noble_troops", "faith_troops")):
        raise BalanceError("Isolated legacy module evaluator returned an unexpected data shape.")
    return payload


def _parse_id_table(path: Path, prefix: str) -> dict[str, int]:
    if not path.is_file():
        return {}
    source = _read_utf8_source(path)
    result: dict[str, int] = {}
    for line in source.splitlines():
        match = ID_LINE_RE.match(line)
        if match is None:
            continue
        symbol = match.group("symbol")
        if not symbol.startswith(prefix):
            continue
        result[symbol[len(prefix) :]] = int(match.group("value"))
    return result


def _named_string_assignment(source: str, name: str) -> tuple[str, int] | None:
    for match in STRING_ASSIGNMENT_RE.finditer(source):
        if match.group("name") == name:
            return match.group("value"), source.count("\n", 0, match.start()) + 1
    return None


def _list_record_code(node: ast.AST) -> str | None:
    if not isinstance(node, ast.List) or not node.elts:
        return None
    first = node.elts[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value
    return None


def _parse_source_records(path: Path, collection: str, kind: str) -> dict[str, SourceRecord]:
    source = _read_utf8_source(path)
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as error:
        raise BalanceError(f"Could not parse {path.name}: {error.msg} at line {error.lineno}.") from error
    result: dict[str, SourceRecord] = {}

    def add(node: ast.List, origin: str) -> None:
        code = _list_record_code(node)
        if code is None:
            return
        if code in result:
            raise BalanceError(f"Duplicate direct {kind} record {code!r} in {path.name}.")
        result[code] = SourceRecord(kind=kind, code=code, path=path, source_text=source, node=node, origin=origin)

    for statement in tree.body:
        if isinstance(statement, ast.Assign) and isinstance(statement.value, ast.List):
            if any(isinstance(target, ast.Name) and target.id == collection for target in statement.targets):
                for entry in statement.value.elts:
                    if isinstance(entry, ast.List):
                        add(entry, "literal")
        elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
            call = statement.value
            if (
                isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
                and call.func.value.id == collection
                and call.func.attr == "append"
                and len(call.args) == 1
                and isinstance(call.args[0], ast.List)
            ):
                add(call.args[0], "append")
    return result


def _ast_symbol(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _ast_int_literal(node: ast.AST) -> int | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return node.value
    return None


def _parse_party_templates(path: Path) -> tuple[PartyTemplateRecord, ...]:
    """Parse static party-template composition without evaluating map scripts."""

    if not path.is_file():
        return ()
    source = _read_utf8_source(path)
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as error:
        raise BalanceError(f"Could not parse party templates: {error.msg} at line {error.lineno}.") from error
    collection: ast.List | None = None
    for statement in tree.body:
        if not isinstance(statement, ast.Assign) or not isinstance(statement.value, ast.List):
            continue
        if any(isinstance(target, ast.Name) and target.id == "party_templates" for target in statement.targets):
            collection = statement.value
            break
    if collection is None:
        return ()
    records: list[PartyTemplateRecord] = []
    seen: set[str] = set()
    for entry in collection.elts:
        if not isinstance(entry, (ast.Tuple, ast.List)) or len(entry.elts) < 7:
            continue
        code = _ast_symbol(entry.elts[0])
        name = _ast_symbol(entry.elts[1])
        if code is None or name is None:
            continue
        if code in seen:
            raise BalanceError(f"Duplicate party template {code!r} in {path.name}.")
        seen.add(code)
        faction_code = _ast_symbol(entry.elts[4])
        stacks: list[PartyTemplateStack] = []
        stack_list = entry.elts[6]
        if isinstance(stack_list, ast.List):
            for stack in stack_list.elts:
                if not isinstance(stack, (ast.Tuple, ast.List)) or len(stack.elts) < 3:
                    continue
                troop_symbol = _ast_symbol(stack.elts[0])
                minimum = _ast_int_literal(stack.elts[1])
                maximum = _ast_int_literal(stack.elts[2])
                if (
                    troop_symbol is None
                    or not troop_symbol.startswith("trp_")
                    or minimum is None
                    or maximum is None
                    or minimum < 0
                    or maximum < minimum
                ):
                    continue
                stacks.append(PartyTemplateStack(troop_code=troop_symbol[4:], minimum=minimum, maximum=maximum))
        records.append(
            PartyTemplateRecord(
                code=code,
                name=name,
                faction_code=faction_code,
                stacks=tuple(stacks),
                path=path,
                line=entry.lineno,
            )
        )
    return tuple(records)


def _parse_upgrade_edges(path: Path) -> tuple[UpgradeEdge, ...]:
    source = _read_utf8_source(path)
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as error:
        raise BalanceError(f"Could not parse troop upgrades: {error.msg} at line {error.lineno}.") from error
    edges: list[UpgradeEdge] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id not in {"upgrade", "upgrade2"}:
            continue
        if len(node.args) not in {3, 4} or not isinstance(node.args[0], ast.Name) or node.args[0].id != "troops":
            continue
        codes: list[str] = []
        for argument in node.args[1:]:
            if not isinstance(argument, ast.Constant) or not isinstance(argument.value, str):
                codes = []
                break
            codes.append(argument.value)
        if len(codes) < 2:
            continue
        for target in codes[1:]:
            edges.append(UpgradeEdge(source=codes[0], target=target, declaration=node.func.id, path=path, line=node.lineno))
    return tuple(edges)


def _tuple_operation_name(node: ast.AST) -> str | None:
    if not isinstance(node, ast.Tuple) or not node.elts:
        return None
    operator = node.elts[0]
    return operator.id if isinstance(operator, ast.Name) else None


def _tuple_string_argument(node: ast.Tuple, position: int) -> str | None:
    if len(node.elts) <= position:
        return None
    value = node.elts[position]
    return value.value if isinstance(value, ast.Constant) and isinstance(value.value, str) else None


def _faith_troop_code(value: str | None) -> str | None:
    if value is None:
        return None
    match = TROOP_CODE_RE.fullmatch(value)
    return match.group(1) if match is not None else None


def _parse_faith_ascension_edges(path: Path) -> tuple[UpgradeEdge, ...]:
    """Extract the explicit noble-candidate -> faith-result mapping.

    Faith ascension is intentionally not an ``upgrade()`` declaration: the
    player chooses a faith and the script consumes a runtime ``*`` noble shell.
    Parsing the paired condition/assignment preserves that authored route as
    balance evidence without evaluating gameplay script code in the DevKit.
    """

    if not path.is_file():
        return ()
    source = _read_utf8_source(path)
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as error:
        raise BalanceError(f"Could not parse faith ascension routes: {error.msg} at line {error.lineno}.") from error
    edges: list[UpgradeEdge] = []
    seen: set[tuple[str, str]] = set()
    for collection in ast.walk(tree):
        if not isinstance(collection, ast.List):
            continue
        candidate: str | None = None
        for operation in collection.elts:
            if not isinstance(operation, ast.Tuple):
                continue
            operation_name = _tuple_operation_name(operation)
            if operation_name == "eq" and _tuple_string_argument(operation, 1) == ":noble_candidate":
                candidate = _faith_troop_code(_tuple_string_argument(operation, 2))
                continue
            if operation_name != "assign" or candidate is None:
                continue
            if _tuple_string_argument(operation, 1) != ":faith_upgrade":
                continue
            target = _faith_troop_code(_tuple_string_argument(operation, 2))
            if target is None:
                continue
            key = (candidate, target)
            if key not in seen:
                edges.append(
                    UpgradeEdge(
                        source=candidate,
                        target=target,
                        declaration="faith_ascension",
                        path=path,
                        line=operation.lineno,
                    )
                )
                seen.add(key)
            candidate = None
    return tuple(edges)


def _parse_faith_candidate_routes(path: Path) -> tuple[UpgradeEdge, ...]:
    """Extract top-noble -> authored `*` candidate routes from the faith selector."""

    if not path.is_file():
        return ()
    source = _read_utf8_source(path)
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as error:
        raise BalanceError(f"Could not parse faith candidate routes: {error.msg} at line {error.lineno}.") from error
    edges: list[UpgradeEdge] = []
    seen: set[tuple[str, str]] = set()
    for collection in ast.walk(tree):
        if not isinstance(collection, ast.List):
            continue
        base_noble: str | None = None
        for operation in collection.elts:
            if not isinstance(operation, ast.Tuple) or _tuple_operation_name(operation) != "assign":
                continue
            target_name = _tuple_string_argument(operation, 1)
            troop_code = _faith_troop_code(_tuple_string_argument(operation, 2))
            if target_name == ":base_noble":
                base_noble = troop_code
                continue
            if target_name != ":candidate" or base_noble is None or troop_code is None:
                continue
            key = (base_noble, troop_code)
            if key not in seen:
                edges.append(
                    UpgradeEdge(
                        source=base_noble,
                        target=troop_code,
                        declaration="faith_candidate",
                        path=path,
                        line=operation.lineno,
                    )
                )
                seen.add(key)
            base_noble = None
    return tuple(edges)


def _legacy_authority(root: Path, items_path: Path, troops_path: Path) -> dict[str, Any]:
    build_path = root / "build_module.bat"
    build_all_path = root / "build/build_all.py"
    batch = _read_utf8_source(build_path) if build_path.is_file() else ""
    build_all = _read_utf8_source(build_all_path) if build_all_path.is_file() else ""
    processor_items = "process_items.py" in batch
    processor_troops = "process_troops.py" in batch
    fragment_builder_items = bool(re.search(r"\bbuild_items\s*\(", build_all))
    fragment_builder_troops = bool(re.search(r"\bbuild_troops\s*\(", build_all))
    confirmed = items_path.is_file() and troops_path.is_file() and processor_items and processor_troops and not fragment_builder_items and not fragment_builder_troops
    return {
        "layer": "legacy_compile_authoring",
        "confirmed": confirmed,
        "items": {
            "path": project_relative(items_path, root),
            "processor_step_present": processor_items,
            "modular_fragment_builder_detected": fragment_builder_items,
        },
        "troops": {
            "path": project_relative(troops_path, root),
            "processor_step_present": processor_troops,
            "modular_fragment_builder_detected": fragment_builder_troops,
        },
        "evaluation": "short-lived compatible Python evaluation of local compile/header/ID inputs; evaluation performs no DevKit writes",
        "mutation_policy": {
            "allowed_scope": [project_relative(items_path, root), project_relative(troops_path, root)],
            "generated_or_export_writes": False,
            "id_or_order_edits": False,
            "default": "dry_run",
            "non_dry_requirements": ["current source SHA", "current plan SHA", "allow_legacy_compile_authoring=true"],
        },
    }


def _record_tuple(value: Any, *, kind: str, index: int) -> tuple[Any, ...]:
    if not isinstance(value, list) or not value or not isinstance(value[0], str):
        raise BalanceError(f"Legacy {kind} evaluator returned an invalid record at index {index}.")
    return tuple(value)


def _record_origin(code: str, source_records: Mapping[tuple[str, str], SourceRecord], *, kind: str) -> str:
    direct = source_records.get((kind, code))
    if direct is not None:
        return direct.origin
    if kind == "troop" and code.endswith("1") and ("troop", code[:-1]) in source_records:
        return "derived_upgrade"
    return "runtime_generated"


def _compute_upgrade_depths(troop_codes: Iterable[str], upgrades: Sequence[UpgradeEdge]) -> dict[str, int]:
    known = set(troop_codes)
    outgoing: dict[str, list[str]] = defaultdict(list)
    incoming: dict[str, list[str]] = defaultdict(list)
    for edge in upgrades:
        if edge.target not in outgoing[edge.source]:
            outgoing[edge.source].append(edge.target)
        if edge.source not in incoming[edge.target]:
            incoming[edge.target].append(edge.source)
    result = {code: 1 for code in known}
    queue: deque[str] = deque(sorted((code for code in known if not incoming.get(code)), key=str.casefold))
    seen_steps = 0
    max_steps = max(1, len(known) * 4)
    while queue and seen_steps < max_steps:
        source = queue.popleft()
        seen_steps += 1
        for target in outgoing.get(source, []):
            if target not in known:
                continue
            proposed = min(6, result.get(source, 1) + 1)
            if proposed > result.get(target, 1):
                result[target] = proposed
                queue.append(target)
    return result


def _runtime_troop_codes(values: Sequence[Any], troops_by_index: Mapping[int, TroopRecord], *, label: str) -> frozenset[str]:
    result: set[str] = set()
    for value in values:
        record: TroopRecord | None = None
        if isinstance(value, int) and not isinstance(value, bool):
            record = troops_by_index.get(value)
        elif isinstance(value, str):
            code = _faith_troop_code(value)
            if code is not None:
                record = next((candidate for candidate in troops_by_index.values() if candidate.code == code), None)
        if record is None:
            raise BalanceError(f"{label} contains a troop reference that is absent from the evaluated troop list: {value!r}.")
        result.add(record.code)
    return frozenset(result)


def _ancestor_codes(targets: Iterable[str], upgrades: Sequence[UpgradeEdge], known_codes: set[str]) -> frozenset[str]:
    incoming: dict[str, set[str]] = defaultdict(set)
    for edge in upgrades:
        if edge.source in known_codes and edge.target in known_codes:
            incoming[edge.target].add(edge.source)
    result: set[str] = {code for code in targets if code in known_codes}
    queue: deque[str] = deque(sorted(result, key=str.casefold))
    while queue:
        target = queue.popleft()
        for source in incoming.get(target, set()):
            if source not in result:
                result.add(source)
                queue.append(source)
    return frozenset(result)


def build_balance_index(root: Path = DEFAULT_REPO_ROOT) -> BalanceIndex:
    """Build and cache explicit legacy authoring + runtime balance evidence."""

    root = root.resolve()
    signature = _source_signature(root)
    cached = _CACHE.get(root)
    if cached is not None and cached[0] == signature:
        return cached[1]
    items_path = root / ITEM_SOURCE_RELATIVE
    troops_path = root / TROOP_SOURCE_RELATIVE
    party_templates_path = root / PARTY_TEMPLATE_SOURCE_RELATIVE
    if not items_path.is_file() or not troops_path.is_file():
        raise BalanceError("Balance Lab requires compile/module_items.py and compile/module_troops.py.")
    source_records: dict[tuple[str, str], SourceRecord] = {}
    for code, record in _parse_source_records(items_path, "items", "item").items():
        source_records[("item", code)] = record
    for code, record in _parse_source_records(troops_path, "troops", "troop").items():
        source_records[("troop", code)] = record
    party_templates = _parse_party_templates(party_templates_path)
    runtime = _load_runtime_module_data(root)
    items: list[ItemRecord] = []
    item_by_code: dict[str, ItemRecord] = {}
    for index, raw in enumerate(runtime["items"]):
        data = _record_tuple(raw, kind="item", index=index)
        if len(data) < 8:
            raise BalanceError(f"Legacy item {data[0]!r} has fewer than eight standard fields.")
        record = ItemRecord(index=index, code=data[0], data=data)
        if record.code in item_by_code:
            raise BalanceError(f"Duplicate evaluated item code {record.code!r}.")
        items.append(record)
        item_by_code[record.code] = record
    troops: list[TroopRecord] = []
    troop_by_code: dict[str, TroopRecord] = {}
    for index, raw in enumerate(runtime["troops"]):
        data = _record_tuple(raw, kind="troop", index=index)
        if len(data) < 11:
            raise BalanceError(f"Legacy troop {data[0]!r} has fewer than eleven standard fields.")
        code = data[0]
        record = TroopRecord(index=index, code=code, data=data, origin=_record_origin(code, source_records, kind="troop"))
        if record.code in troop_by_code:
            raise BalanceError(f"Duplicate evaluated troop code {record.code!r}.")
        troops.append(record)
        troop_by_code[record.code] = record
    troop_by_index = {troop.index: troop for troop in troops}
    faction_by_index: dict[int, str] = {}
    faction_name_by_index: dict[int, str] = {}
    for index, entry in enumerate(runtime["factions"]):
        if isinstance(entry, list) and entry and isinstance(entry[0], str):
            faction_by_index[index] = entry[0]
            if len(entry) > 1 and isinstance(entry[1], str):
                faction_name_by_index[index] = entry[1]
    item_users_raw: dict[int, set[str]] = defaultdict(set)
    for troop in troops:
        inventory = troop.data[7]
        if not isinstance(inventory, list):
            continue
        for value in inventory:
            if isinstance(value, int) and value in {item.index for item in items}:
                item_users_raw[value].add(troop.code)
    upgrades = _parse_upgrade_edges(troops_path)
    faith_candidate_routes = _parse_faith_candidate_routes(root / FAITH_CANDIDATE_SOURCE_RELATIVE)
    faith_ascensions = _parse_faith_ascension_edges(root / FAITH_ASCENSION_SOURCE_RELATIVE)
    known_troop_codes = set(troop_by_code)
    noble_troop_codes = _runtime_troop_codes(runtime["noble_troops"], troop_by_index, label="sod_noble_troops")
    faith_troop_codes = _runtime_troop_codes(runtime["faith_troops"], troop_by_index, label="sod_faith_troops")
    candidate_roots = {edge.source for edge in faith_candidate_routes if edge.source in known_troop_codes}
    noble_track_codes = frozenset(
        set(_ancestor_codes(noble_troop_codes, upgrades, known_troop_codes))
        | set(_ancestor_codes(candidate_roots, upgrades, known_troop_codes))
    )
    faith_candidate_codes = frozenset(
        edge.source for edge in faith_ascensions if edge.source in known_troop_codes
    ) | frozenset(edge.target for edge in faith_candidate_routes if edge.target in known_troop_codes)
    index = BalanceIndex(
        root=root,
        items_path=items_path,
        troops_path=troops_path,
        party_templates_path=party_templates_path,
        items=tuple(items),
        troops=tuple(troops),
        party_templates=party_templates,
        item_by_code=item_by_code,
        troop_by_code=troop_by_code,
        source_records=source_records,
        upgrades=upgrades,
        faith_candidate_routes=faith_candidate_routes,
        faith_ascensions=faith_ascensions,
        upgrade_depths=_compute_upgrade_depths((troop.code for troop in troops), upgrades),
        faction_by_index=faction_by_index,
        faction_name_by_index=faction_name_by_index,
        item_ids=_parse_id_table(root / ITEM_IDS_RELATIVE, "itm_"),
        troop_ids=_parse_id_table(root / TROOP_IDS_RELATIVE, "trp_"),
        party_ids=_parse_id_table(root / PARTY_IDS_RELATIVE, "p_"),
        item_users={key: tuple(sorted(value, key=str.casefold)) for key, value in item_users_raw.items()},
        noble_troop_codes=noble_troop_codes,
        faith_troop_codes=faith_troop_codes,
        noble_track_codes=noble_track_codes,
        faith_candidate_codes=faith_candidate_codes,
        source_authority=_legacy_authority(root, items_path, troops_path),
    )
    _CACHE[root] = (signature, index)
    return index


def invalidate_balance_index(root: Path) -> None:
    _CACHE.pop(root.resolve(), None)


def _item_type(record: ItemRecord) -> int:
    return int(record.data[3]) & 0xFF


def _item_type_name(record: ItemRecord) -> str:
    return ITEM_TYPES.get(_item_type(record), f"Unknown ({_item_type(record)})")


def _damage_parts(raw: int) -> dict[str, Any]:
    amount = raw & 0xFF
    kind = (raw >> 8) & 0x03
    label = {0: "cut", 1: "pierce", 2: "blunt"}.get(kind, "unknown")
    multiplier = {0: 1.0, 1: 1.5, 2: 1.25}.get(kind, 1.0)
    return {"amount": amount, "type": label, "effective": round(amount * multiplier, 2), "label": f"{amount}{label[:1] if label != 'unknown' else '?'}"}


def _item_stats(record: ItemRecord) -> dict[str, Any]:
    stats = int(record.data[6])
    return {
        "weight": round(((stats >> 24) & 0xFF) * 0.25, 2),
        "head_armor": stats & 0xFF,
        "body_armor": (stats >> 8) & 0xFF,
        "leg_armor": (stats >> 16) & 0xFF,
        "difficulty": (stats >> 32) & 0xFF,
        "hit_points": (stats >> 40) & 0xFFFF,
        "speed_rating": (stats >> 80) & 0xFF,
        "missile_speed": (stats >> 90) & 0x3FF,
        "weapon_length": (stats >> 70) & 0x3FF,
        "max_ammo": (stats >> 100) & 0xFF,
        "abundance": ((stats >> 110) & 0xFF) or 100,
        "accuracy": (stats >> 16) & 0xFF,
        "swing_damage": _damage_parts((stats >> 50) & 0x3FF),
        "thrust_damage": _damage_parts((stats >> 60) & 0x3FF),
        "raw_bits": str(stats),
    }


def _effective_damage(parts: Mapping[str, Any]) -> float:
    return float(parts["effective"])


def item_combat_score(record: ItemRecord) -> int:
    stats = _item_stats(record)
    item_type = _item_type(record)
    value = int(record.data[5])
    if item_type in ITEM_TYPE_MELEE:
        raw = max(_effective_damage(stats["swing_damage"]), _effective_damage(stats["thrust_damage"]))
        return int(raw + int(stats["speed_rating"]) / 4 + int(stats["weapon_length"]) / 10)
    if item_type in ITEM_TYPE_RANGED:
        return int(_effective_damage(stats["thrust_damage"]) + int(stats["missile_speed"]) / 3 + int(stats["max_ammo"]) / 2)
    if item_type in ITEM_TYPE_AMMO:
        return int(int(stats["thrust_damage"]["amount"]) + int(stats["max_ammo"]) / 2)
    if item_type == 7:
        return int(int(stats["hit_points"]) / 12 + int(stats["body_armor"]) * 3 + int(stats["speed_rating"]) / 4)
    if item_type == 1:
        return int(int(stats["hit_points"]) / 4 + int(stats["body_armor"]) + int(stats["speed_rating"]) + int(stats["leg_armor"]) + int(stats["head_armor"]))
    if item_type == 13:
        return int(stats["body_armor"]) + int(stats["leg_armor"]) + int(stats["head_armor"]) // 2
    if item_type == 12:
        return int(stats["head_armor"])
    if item_type == 14:
        return int(stats["leg_armor"])
    if item_type == 15:
        return int(stats["body_armor"])
    return max(0, value // 100)


def _decode_attributes(raw: Any) -> dict[str, int]:
    value = int(raw)
    return {
        "level": (value >> 32) & 0xFF,
        "str": value & 0xFF,
        "agi": (value >> 8) & 0xFF,
        "int": (value >> 16) & 0xFF,
        "cha": (value >> 24) & 0xFF,
        "raw_bits": str(value),
    }


def _decode_proficiencies(raw: Any) -> dict[str, int]:
    value = int(raw)
    return {name: (value >> bits) & 0x3FF for name, bits in PROFICIENCY_BITS.items()}


def _decode_skills(raw: Any) -> dict[str, int]:
    value = int(raw)
    return {name: (value >> (slot * 4)) & 0xF for slot, name in SKILL_SLOTS.items()}


def _item_source(index: BalanceIndex, record: ItemRecord) -> dict[str, Any]:
    source = index.source_records.get(("item", record.code))
    if source is None:
        return {"path": None, "line": None, "direct_editable": False, "origin": "runtime_generated"}
    return {
        "path": project_relative(source.path, index.root),
        "line": source.node.lineno,
        "end_line": source.node.end_lineno,
        "direct_editable": True,
        "origin": source.origin,
        "legacy_compile_authoring": True,
    }


def _troop_source(index: BalanceIndex, record: TroopRecord) -> dict[str, Any]:
    source = index.source_records.get(("troop", record.code))
    if source is not None:
        return {
            "path": project_relative(source.path, index.root),
            "line": source.node.lineno,
            "end_line": source.node.end_lineno,
            "direct_editable": True,
            "origin": source.origin,
            "legacy_compile_authoring": True,
        }
    base = record.code[:-1] if record.origin == "derived_upgrade" else None
    return {
        "path": project_relative(index.troops_path, index.root) if base else None,
        "line": None,
        "direct_editable": False,
        "origin": record.origin,
        "derived_from": f"trp_{base}" if base else None,
        "legacy_compile_authoring": True,
    }


def _item_overview(index: BalanceIndex, record: ItemRecord) -> dict[str, Any]:
    flags = int(record.data[3])
    score = item_combat_score(record)
    users = index.item_users.get(record.index, ())
    heroes = sum(1 for code in users if index.troop_by_code[code].data[3] & TF_HERO)
    regulars = len(users) - heroes
    return {
        "entity_id": f"item:{record.code}",
        "item_id": f"itm_{record.code}",
        "code": record.code,
        "index": record.index,
        "name": str(record.data[1]),
        "type": _item_type_name(record),
        "type_id": _item_type(record),
        "price": int(record.data[5]),
        "combat_score": score,
        "price_per_score": round(int(record.data[5]) / score, 2) if score > 0 else None,
        "merchandise": bool(flags & ITP_MERCHANDISE),
        "unique": bool(flags & ITP_UNIQUE),
        "troop_use_count": regulars,
        "hero_use_count": heroes,
        "all_user_count": len(users),
        "source": _item_source(index, record),
        "protected_legacy_record": HARDWIRED_ITEMS.get(record.code) == record.index,
    }


def _inventory_entries(index: BalanceIndex, record: TroopRecord) -> tuple[list[ItemRecord], list[int]]:
    values = record.data[7]
    if not isinstance(values, list):
        return [], []
    entries: list[ItemRecord] = []
    unknown: list[int] = []
    by_index = {item.index: item for item in index.items}
    for value in values:
        if isinstance(value, int) and value in by_index:
            entries.append(by_index[value])
        elif isinstance(value, int):
            unknown.append(value)
    return entries, unknown


def _role(record: TroopRecord, inventory: Sequence[ItemRecord]) -> str:
    flags = int(record.data[3])
    kinds = {_item_type(item) for item in inventory}
    profs = _decode_proficiencies(record.data[9])
    mounted = bool(flags & (TF_MOUNTED | TF_GUARANTEE_HORSE)) or 1 in kinds
    has_bow = 8 in kinds or 5 in kinds
    has_crossbow = 9 in kinds or 6 in kinds
    has_throw = 10 in kinds
    has_firearm = bool(kinds & ITEM_TYPE_FIREARM) or profs["firearm"] >= 160
    has_ranged = bool(flags & TF_GUARANTEE_RANGED) or has_bow or has_crossbow or has_throw or has_firearm
    has_melee = bool(kinds & ITEM_TYPE_MELEE)
    if mounted and (has_bow or has_crossbow or has_throw or has_firearm or profs["archery"] >= 160):
        return "Mounted ranged"
    if mounted:
        return "Cavalry"
    if has_bow:
        return "Archer"
    if has_crossbow:
        return "Crossbow"
    if has_firearm:
        return "Firearm"
    if has_throw:
        return "Skirmisher"
    if has_melee or has_ranged:
        return "Infantry"
    return "Noncombat/technical"


def _upgrade_maps(index: BalanceIndex) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    outgoing: dict[str, list[str]] = defaultdict(list)
    incoming: dict[str, list[str]] = defaultdict(list)
    for edge in index.upgrades:
        if edge.target not in outgoing[edge.source]:
            outgoing[edge.source].append(edge.target)
        if edge.source not in incoming[edge.target]:
            incoming[edge.target].append(edge.source)
    return outgoing, incoming


def _upgrade_depths(index: BalanceIndex) -> dict[str, int]:
    return index.upgrade_depths


def _level_tier(level: int) -> int:
    if level >= 35:
        return 6
    if level >= 30:
        return 5
    if level >= 25:
        return 4
    if level >= 20:
        return 3
    if level >= 12:
        return 2
    return 1


def _kit_band(tier: int, level: int, role: str, expects_shield: bool) -> tuple[int, int]:
    base = {
        1: (60, 250),
        2: (120, 360),
        3: (200, 470),
        4: (290, 570),
        5: (380, 690),
        6: (460, 760),
    }[min(max(tier, 1), 6)]
    low, high = base
    if level >= 35:
        high += 80
    elif level >= 28:
        high += 45
    if role in {"Cavalry", "Mounted ranged"}:
        low += 40
        high += 70
    elif role == "Archer":
        low -= 50
        high += 35
    elif role in {"Crossbow", "Firearm", "Skirmisher"}:
        low -= 20
        high += 35
    elif role == "Infantry" and not expects_shield:
        low -= 70
        high -= 50
    return max(0, low), high


def _kit_score(index: BalanceIndex, record: TroopRecord) -> dict[str, Any]:
    inventory, unknown = _inventory_entries(index, record)
    rows = [(item, item_combat_score(item)) for item in inventory]
    best_melee = max((score for item, score in rows if _item_type(item) in ITEM_TYPE_MELEE), default=0)
    best_ranged_weapon = max((score for item, score in rows if _item_type(item) in ITEM_TYPE_RANGED), default=0)
    best_ammo = max((score for item, score in rows if _item_type(item) in ITEM_TYPE_AMMO), default=0)
    armor = sum(sorted((score for item, score in rows if _item_type(item) in ITEM_TYPE_ARMOR), reverse=True)[:4])
    shield = max((score for item, score in rows if _item_type(item) == 7), default=0)
    mount = max((score for item, score in rows if _item_type(item) == 1), default=0)
    role = _role(record, inventory)
    attrs = _decode_attributes(record.data[8])
    tree_tier = _upgrade_depths(index).get(record.code, 1)
    tier = min(6, max(tree_tier, _level_tier(attrs["level"])))
    expects_shield = bool(int(record.data[3]) & TF_GUARANTEE_SHIELD)
    low, high = _kit_band(tier, attrs["level"], role, expects_shield)
    kit = best_melee + best_ranged_weapon + best_ammo + armor + shield + mount
    if role == "Noncombat/technical":
        status = "not_scored"
        gap = 0
    elif kit < low:
        status = "under_equipped"
        gap = low - kit
    elif kit > high:
        status = "over_equipped"
        gap = kit - high
    else:
        status = "within_band"
        gap = 0
    notes: list[str] = []
    if expects_shield and shield == 0:
        notes.append("shield_guaranteed_but_no_shield_in_inventory")
    if role in {"Cavalry", "Mounted ranged"} and mount == 0:
        notes.append("mounted_role_without_mount_item")
    if role != "Noncombat/technical" and not best_melee and not best_ranged_weapon:
        notes.append("no_weapon_item")
    if unknown:
        notes.append("unknown_item_index_in_inventory")
    return {
        "role": role,
        "tree_tier": tree_tier,
        "fit_tier": tier,
        "band": {"minimum": low, "maximum": high},
        "melee": best_melee,
        "ranged_weapon": best_ranged_weapon,
        "ammo": best_ammo,
        "ranged": best_ranged_weapon + best_ammo,
        "armor": armor,
        "shield": shield,
        "mount": mount,
        "kit_score": kit,
        "status": status,
        "gap": gap,
        "notes": notes,
    }


def _authored_troop_code(index: BalanceIndex, record: TroopRecord) -> str:
    if record.origin == "derived_upgrade" and record.code.endswith("1") and record.code[:-1] in index.troop_by_code:
        return record.code[:-1]
    return record.code


def _roster_family(index: BalanceIndex, record: TroopRecord) -> dict[str, str]:
    code = _authored_troop_code(index, record)
    for family_id, name, prefixes in ROSTER_FAMILY_RULES:
        if any(code.startswith(prefix) for prefix in prefixes):
            return {"id": family_id, "name": name, "scope": "theme_preserving_roster"}
    faction_index = int(record.data[6]) if isinstance(record.data[6], int) else -1
    faction_code = index.faction_by_index.get(faction_index, str(faction_index))
    faction_name = index.faction_name_by_index.get(faction_index, faction_code)
    return {
        "id": f"faction:{faction_code}",
        "name": f"Faction: {faction_name}",
        "scope": "runtime_faction",
    }


def _campaign_cohort(index: BalanceIndex, record: TroopRecord) -> dict[str, str]:
    """Classify actual campaign coexistence separately from equipment family."""

    family = _roster_family(index, record)
    cohort_id = ROSTER_COHORT_IDS.get(family["id"])
    if cohort_id is not None:
        return dict(CAMPAIGN_COHORTS[cohort_id])
    faction_index = int(record.data[6]) if isinstance(record.data[6], int) else -1
    faction_code = index.faction_by_index.get(faction_index, str(faction_index))
    cohort_id = FACTION_COHORT_IDS.get(faction_code)
    if cohort_id is not None:
        return dict(CAMPAIGN_COHORTS[cohort_id])
    faction_name = index.faction_name_by_index.get(faction_index, faction_code)
    if faction_code.startswith("sod_merc_guild"):
        return {
            "id": f"campaign:mercenary:{faction_code}",
            "name": f"Mercenary market: {faction_name}",
            "campaign_group": "mercenary_market",
            "campaign_role": "contract_or_world_company",
            "presence": "Availability and affiliation are governed by the mercenary market and world-presence systems.",
            "analysis_policy": "Review contract cost, employer budget, demand, availability, and world role with equipment; do not treat this as a territorial faction.",
        }
    return {
        "id": f"campaign:other:{faction_code}",
        "name": f"Other campaign content: {faction_name}",
        "campaign_group": "other_campaign_content",
        "campaign_role": "context_specific",
        "presence": "This content is outside the player-start, native-world, and Imperial invasion cohorts.",
        "analysis_policy": "Establish its spawn and access path before making cross-roster balance claims.",
    }


def _troop_rank(index: BalanceIndex, record: TroopRecord) -> dict[str, Any]:
    code = _authored_troop_code(index, record)
    if code in index.faith_troop_codes:
        group = "Faith/Zealot"
        stage = "faith_elite"
        evidence = "sod_faith_troops"
    elif code in index.faith_candidate_codes:
        group = "Noble"
        stage = "faith_ascension_candidate"
        evidence = "scripted_faith_candidate_route"
    elif code in index.noble_troop_codes:
        group = "Noble"
        stage = "noble_rank"
        evidence = "sod_noble_troops"
    elif code in index.noble_track_codes:
        group = "Noble"
        stage = "noble_route_entry"
        evidence = "explicit_path_to_sod_noble_troops"
    else:
        group = "Normal"
        stage = "normal"
        evidence = "not_on_runtime_noble_or_faith_lists"
    return {
        "group": group,
        "order": RANK_ORDER[group],
        "stage": stage,
        "faith_ascension_candidate": code in index.faith_candidate_codes,
        "evidence": evidence,
        "authored_troop_id": f"trp_{code}",
    }


def _troop_overview(index: BalanceIndex, record: TroopRecord) -> dict[str, Any]:
    attrs = _decode_attributes(record.data[8])
    kit = _kit_score(index, record)
    faction_index = int(record.data[6]) if isinstance(record.data[6], int) else -1
    return {
        "entity_id": f"troop:{record.code}",
        "troop_id": f"trp_{record.code}",
        "code": record.code,
        "index": record.index,
        "name": str(record.data[1]),
        "plural_name": str(record.data[2]),
        "faction": index.faction_by_index.get(faction_index, str(faction_index)),
        "faction_name": index.faction_name_by_index.get(faction_index, index.faction_by_index.get(faction_index, str(faction_index))),
        "faction_index": faction_index,
        "roster": _roster_family(index, record),
        "campaign_cohort": _campaign_cohort(index, record),
        "rank": _troop_rank(index, record),
        "hero": bool(int(record.data[3]) & TF_HERO),
        "level": attrs["level"],
        "role": kit["role"],
        "tree_tier": kit["tree_tier"],
        "fit_tier": kit["fit_tier"],
        "kit_score": kit["kit_score"],
        "kit_status": kit["status"],
        "source": _troop_source(index, record),
        "protected_legacy_record": HARDWIRED_TROOPS.get(record.code) == record.index,
    }


def _id_contract(index: BalanceIndex, kind: str) -> dict[str, Any]:
    records: Sequence[ItemRecord | TroopRecord] = index.items if kind == "item" else index.troops
    table = index.item_ids if kind == "item" else index.troop_ids
    prefix = "itm_" if kind == "item" else "trp_"
    normalized_table = {code.casefold(): value for code, value in table.items()}
    normalized_records = {record.code.casefold() for record in records}
    missing = [f"{prefix}{record.code}" for record in records if record.code.casefold() not in normalized_table]
    shifted = [
        {"symbol": f"{prefix}{record.code}", "expected": record.index, "actual": normalized_table[record.code.casefold()]}
        for record in records
        if record.code.casefold() in normalized_table and normalized_table[record.code.casefold()] != record.index
    ]
    extras = [f"{prefix}{code}" for code in table if code.casefold() not in normalized_records]
    hardwired = HARDWIRED_ITEMS if kind == "item" else HARDWIRED_TROOPS
    protected = [
        {"symbol": f"{prefix}{code}", "expected": expected, "actual": normalized_table.get(code.casefold())}
        for code, expected in hardwired.items()
        if normalized_table.get(code.casefold()) != expected
    ]
    return {
        "kind": kind,
        "id_table_path": project_relative(index.root / (ITEM_IDS_RELATIVE if kind == "item" else TROOP_IDS_RELATIVE), index.root),
        "runtime_record_count": len(records),
        "id_table_record_count": len(table),
        "missing_count": len(missing),
        "shifted_count": len(shifted),
        "extra_count": len(extras),
        "protected_contract_failure_count": len(protected),
        "missing": missing[:100],
        "shifted": shifted[:100],
        "extra": extras[:100],
        "protected_failures": protected,
        "passed": not missing and not shifted and not protected,
    }


def balance_summary(index: BalanceIndex) -> dict[str, Any]:
    item_types = Counter(_item_type_name(item) for item in index.items)
    roles = Counter(_kit_score(index, troop)["role"] for troop in index.troops)
    direct_troops = sum(1 for troop in index.troops if troop.origin in {"literal", "append"})
    derived_troops = sum(1 for troop in index.troops if troop.origin == "derived_upgrade")
    item_contract = _id_contract(index, "item")
    troop_contract = _id_contract(index, "troop")
    warnings = [
        "Combat and kit scores are deterministic triage heuristics, not an in-engine battle or economy simulation.",
        "Normal, noble, and faith/zealot troop ranks are distinct access tiers. Compare battlefield roles and availability before treating any score difference as a balance defect.",
        "Item/troop lists are legacy compile-layer authoring inputs. The normal reviewed build remains required to regenerate exports and to inspect processor/output diffs.",
        "Derived upgrade-variant troops are viewable but not directly editable; change the owning literal troop or upgrade declaration deliberately.",
        "The five SoD player cultures are mutually exclusive campaign starts. Their shared runtime faction must not create an all-cultures balance aggregate.",
        "The Imperial Expedition is a delayed endgame invasion. Its reinforcement waves and campaign pressure need a different review frame than a normal faction roster.",
    ]
    if not index.source_authority["confirmed"]:
        warnings.append("Legacy authoring authority could not be fully confirmed from build_module.bat/build_all.py; mutation is blocked until the build route is restored.")
    return {
        "version": BALANCE_VERSION,
        "authoring": index.source_authority,
        "campaign_topology": {
            "player_start_culture_count": 5,
            "native_world_realm_count": 5,
            "imperial_invasion_cohort": "campaign:imperial-expedition",
            "party_template_source": project_relative(index.party_templates_path, index.root),
            "party_template_count": len(index.party_templates),
            "imperial_core_reinforcement_template_count": sum(
                1 for template in index.party_templates if template.code in IMPERIAL_CORE_TEMPLATE_CODES
            ),
        },
        "items": {
            "count": len(index.items),
            "direct_source_record_count": sum(1 for item in index.items if ("item", item.code) in index.source_records),
            "merchandise_count": sum(1 for item in index.items if int(item.data[3]) & ITP_MERCHANDISE),
            "by_type": dict(sorted(item_types.items())),
            "id_contract": item_contract,
        },
        "troops": {
            "count": len(index.troops),
            "direct_source_record_count": direct_troops,
            "derived_upgrade_variant_count": derived_troops,
            "hero_count": sum(1 for troop in index.troops if int(troop.data[3]) & TF_HERO),
            "by_role": dict(sorted(roles.items())),
            "upgrade_edge_count": len(index.upgrades),
            "elite_tracks": {
                "noble_runtime_list_count": len(index.noble_troop_codes),
                "noble_route_troop_count": len(index.noble_track_codes),
                "faith_runtime_list_count": len(index.faith_troop_codes),
                "faith_candidate_route_edge_count": len(index.faith_candidate_routes),
                "faith_ascension_edge_count": len(index.faith_ascensions),
                "faith_ascension_candidate_count": len(index.faith_candidate_codes),
            },
            "id_contract": troop_contract,
        },
        "warnings": warnings,
    }


def _matches(query: str | None, *values: object) -> bool:
    if query is None:
        return True
    haystack = " ".join(str(value) for value in values).casefold()
    return query.casefold() in haystack


def _normalized_item_type(value: str | None) -> int | None:
    if value is None or value.casefold() in {"all", ""}:
        return None
    result = ITEM_TYPE_BY_NAME.get(value.casefold())
    if result is None:
        raise BalanceError("item_type must be 'all' or one of: " + ", ".join(sorted(ITEM_TYPES.values())))
    return result


def balance_find_items(
    index: BalanceIndex,
    *,
    query: str | None = None,
    item_type: str = "all",
    merchandise: bool | None = None,
    min_score: int | None = None,
    max_score: int | None = None,
    limit: int = 60,
) -> dict[str, Any]:
    checked_query = optional_string(query, name="query")
    checked_type = _normalized_item_type(item_type)
    checked_limit = require_limit(limit)
    if merchandise is not None and not isinstance(merchandise, bool):
        raise BalanceError("merchandise must be true, false, or omitted.")
    if min_score is not None:
        min_score = require_int(min_score, name="min_score", minimum=0, maximum=100_000)
    if max_score is not None:
        max_score = require_int(max_score, name="max_score", minimum=0, maximum=100_000)
    if min_score is not None and max_score is not None and min_score > max_score:
        raise BalanceError("min_score may not exceed max_score.")
    rows = []
    for item in index.items:
        overview = _item_overview(index, item)
        if checked_type is not None and overview["type_id"] != checked_type:
            continue
        if merchandise is not None and overview["merchandise"] is not merchandise:
            continue
        if min_score is not None and overview["combat_score"] < min_score:
            continue
        if max_score is not None and overview["combat_score"] > max_score:
            continue
        if not _matches(checked_query, overview["code"], overview["name"], overview["type"], overview["source"]["path"]):
            continue
        rows.append(overview)
    rows.sort(key=lambda row: (-int(row["combat_score"]), str(row["code"]).casefold()))
    return {
        "match_count": len(rows),
        "returned_count": min(len(rows), checked_limit),
        "items": rows[:checked_limit],
        "filters": {"query": checked_query, "item_type": item_type, "merchandise": merchandise, "min_score": min_score, "max_score": max_score},
        "warnings": ["Rows are sorted by deterministic combat-score estimate, not exact game DPS."]
    }


def _editable_stat_calls(source: SourceRecord) -> list[str]:
    if len(source.node.elts) <= 6:
        return []
    stats = source.node.elts[6]
    calls: set[str] = set()
    for node in ast.walk(stats):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in set(STAT_ALIASES.values()):
            calls.add(node.func.id)
    return sorted(calls)


def balance_item(index: BalanceIndex, item_id: str, *, troop_limit: int = 60) -> dict[str, Any]:
    code = normalize_item_code(item_id)
    checked_limit = require_limit(troop_limit, name="troop_limit", maximum=200)
    record = _lookup_item(index, code)
    if record is None:
        raise BalanceError(f"Unknown item: itm_{code}.")
    users = [index.troop_by_code[value] for value in index.item_users.get(record.index, ())]
    source = index.source_records.get(("item", code))
    flags = int(record.data[3])
    return {
        "item": {
            **_item_overview(index, record),
            "stats": _item_stats(record),
            "flags": {"raw_bits": str(flags), "merchandise": bool(flags & ITP_MERCHANDISE), "unique": bool(flags & ITP_UNIQUE)},
            "capabilities_raw_bits": str(int(record.data[4])),
            "modifier_bits_raw": str(int(record.data[7])),
            "mesh_count": len(record.data[2]) if isinstance(record.data[2], list) else 0,
            "editable_stat_calls": _editable_stat_calls(source) if source else [],
            "semantic_actions": ["set_name", "set_price", "set_existing_stat"] if source else [],
        },
        "troop_users": [_troop_overview(index, troop) for troop in users[:checked_limit]],
        "troop_user_count": len(users),
        "troop_users_truncated": len(users) > checked_limit,
        "warnings": [
            "Stats reflect evaluated M&B header bit packing. A stat is editable only when its constructor is present in this item's direct source record.",
            "Changing price/stat data does not alter item order or generated IDs, but still requires the normal build/export review.",
        ],
    }


def balance_find_troops(
    index: BalanceIndex,
    *,
    query: str | None = None,
    faction: str | None = None,
    role: str | None = None,
    include_heroes: bool = True,
    min_level: int | None = None,
    max_level: int | None = None,
    limit: int = 60,
) -> dict[str, Any]:
    checked_query = optional_string(query, name="query")
    checked_faction = optional_string(faction, name="faction", maximum=160)
    checked_role = optional_string(role, name="role", maximum=80)
    if not isinstance(include_heroes, bool):
        raise BalanceError("include_heroes must be true or false.")
    if min_level is not None:
        min_level = require_int(min_level, name="min_level", minimum=0, maximum=255)
    if max_level is not None:
        max_level = require_int(max_level, name="max_level", minimum=0, maximum=255)
    if min_level is not None and max_level is not None and min_level > max_level:
        raise BalanceError("min_level may not exceed max_level.")
    checked_limit = require_limit(limit)
    rows = []
    for troop in index.troops:
        overview = _troop_overview(index, troop)
        if not include_heroes and overview["hero"]:
            continue
        if checked_faction is not None and checked_faction.casefold() not in str(overview["faction"]).casefold():
            continue
        if checked_role is not None and checked_role.casefold() != str(overview["role"]).casefold():
            continue
        if min_level is not None and overview["level"] < min_level:
            continue
        if max_level is not None and overview["level"] > max_level:
            continue
        if not _matches(checked_query, overview["code"], overview["name"], overview["plural_name"], overview["faction"], overview["role"]):
            continue
        rows.append(overview)
    rows.sort(key=lambda row: (-int(row["kit_score"]), -int(row["level"]), str(row["code"]).casefold()))
    return {
        "match_count": len(rows),
        "returned_count": min(len(rows), checked_limit),
        "troops": rows[:checked_limit],
        "filters": {"query": checked_query, "faction": checked_faction, "role": checked_role, "include_heroes": include_heroes, "min_level": min_level, "max_level": max_level},
        "warnings": ["Kit score chooses the strongest available item per equipment role; it does not model the engine's random inventory selection probability."]
    }


def balance_troop(index: BalanceIndex, troop_id: str, *, item_limit: int = 80) -> dict[str, Any]:
    code = normalize_troop_code(troop_id)
    checked_limit = require_limit(item_limit, name="item_limit", maximum=200)
    record = _lookup_troop(index, code)
    if record is None:
        raise BalanceError(f"Unknown troop: trp_{code}.")
    inventory, unknown = _inventory_entries(index, record)
    outgoing, incoming = _upgrade_maps(index)
    flags = int(record.data[3])
    source = index.source_records.get(("troop", code))
    inventory_rows = [{**_item_overview(index, item), "stats": _item_stats(item)} for item in inventory[:checked_limit]]
    return {
        "troop": {
            **_troop_overview(index, record),
            "attributes": _decode_attributes(record.data[8]),
            "proficiencies": _decode_proficiencies(record.data[9]),
            "skills": _decode_skills(record.data[10]),
            "flags": {
                "raw_bits": str(flags),
                "hero": bool(flags & TF_HERO),
                "mounted": bool(flags & TF_MOUNTED),
                "guarantees": {
                    "boots": bool(flags & TF_GUARANTEE_BOOTS),
                    "armor": bool(flags & TF_GUARANTEE_ARMOR),
                    "helmet": bool(flags & TF_GUARANTEE_HELMET),
                    "gloves": bool(flags & TF_GUARANTEE_GLOVES),
                    "horse": bool(flags & TF_GUARANTEE_HORSE),
                    "shield": bool(flags & TF_GUARANTEE_SHIELD),
                    "ranged": bool(flags & TF_GUARANTEE_RANGED),
                },
            },
            "kit_analysis": _kit_score(index, record),
            "upgrades_to": [f"trp_{target}" for target in outgoing.get(code, [])],
            "upgrades_from": [f"trp_{source_code}" for source_code in incoming.get(code, [])],
            "semantic_actions": (["set_name", "set_plural_name", "set_attributes", "set_proficiencies", "set_skills", "set_inventory"] if source else []),
        },
        "inventory": inventory_rows,
        "inventory_count": len(inventory),
        "inventory_truncated": len(inventory) > checked_limit,
        "unknown_inventory_indices": unknown,
        "warnings": [
            "The inventory is an engine random-choice pool, not a guaranteed complete loadout. The kit score uses the best eligible entries as a pressure heuristic.",
            "A derived upgrade variant has no direct source record. Edit the owning literal troop or its explicit upgrade declaration instead of trying to patch the derived runtime result.",
        ],
    }


def balance_upgrade_tree(index: BalanceIndex, troop_id: str, *, depth: int = 3, limit: int = 120) -> dict[str, Any]:
    code = normalize_troop_code(troop_id)
    root_record = _lookup_troop(index, code)
    if root_record is None:
        raise BalanceError(f"Unknown troop: trp_{code}.")
    code = root_record.code
    checked_depth = require_int(depth, name="depth", minimum=1, maximum=8)
    checked_limit = require_limit(limit, maximum=300)
    outgoing, incoming = _upgrade_maps(index)
    node_depth: dict[str, int] = {code: 0}
    edges: list[dict[str, Any]] = []
    queue: deque[str] = deque([code])
    while queue and len(node_depth) < checked_limit:
        current = queue.popleft()
        current_depth = node_depth[current]
        if current_depth >= checked_depth:
            continue
        for target in outgoing.get(current, []):
            edges.append({"source": f"trp_{current}", "target": f"trp_{target}"})
            if target in index.troop_by_code and target not in node_depth and len(node_depth) < checked_limit:
                node_depth[target] = current_depth + 1
                queue.append(target)
        for parent in incoming.get(current, []):
            edges.append({"source": f"trp_{parent}", "target": f"trp_{current}"})
            if parent in index.troop_by_code and parent not in node_depth and len(node_depth) < checked_limit:
                node_depth[parent] = current_depth + 1
                queue.append(parent)
    nodes = []
    for troop_code, distance in sorted(node_depth.items(), key=lambda item: (item[1], item[0].casefold())):
        overview = _troop_overview(index, index.troop_by_code[troop_code])
        overview["distance"] = distance
        nodes.append(overview)
    unique_edges = list({(edge["source"], edge["target"]): edge for edge in edges}.values())
    return {
        "root": f"trp_{code}",
        "depth": checked_depth,
        "node_count": len(nodes),
        "edge_count": len(unique_edges),
        "truncated": len(node_depth) >= checked_limit,
        "nodes": nodes,
        "edges": unique_edges,
        "warnings": ["Upgrade edges are parsed from explicit upgrade()/upgrade2() declarations. Runtime-derived '*' variants are not independent authored tree nodes."]
    }


def _roster_troop_groups(
    index: BalanceIndex,
    *,
    include_heroes: bool,
    include_derived: bool,
) -> tuple[dict[str, dict[str, str]], dict[str, list[TroopRecord]]]:
    families: dict[str, dict[str, str]] = {}
    groups: dict[str, list[TroopRecord]] = defaultdict(list)
    for troop in index.troops:
        if not include_heroes and bool(int(troop.data[3]) & TF_HERO):
            continue
        if not include_derived and troop.origin == "derived_upgrade":
            continue
        family = _roster_family(index, troop)
        families[family["id"]] = family
        groups[family["id"]].append(troop)
    for records in groups.values():
        records.sort(key=lambda troop: (str(troop.data[1]).casefold(), troop.code.casefold()))
    return families, groups


def _select_roster_group(
    families: Mapping[str, Mapping[str, str]],
    groups: Mapping[str, Sequence[TroopRecord]],
    roster: str | None,
) -> tuple[str | None, list[tuple[dict[str, str], list[TroopRecord]]]]:
    checked_roster = optional_string(roster, name="roster", maximum=160)
    ordered = [
        (dict(families[family_id]), list(groups[family_id]))
        for family_id in sorted(groups, key=lambda value: (families[value]["name"].casefold(), value.casefold()))
    ]
    if checked_roster is None or checked_roster.casefold() == "all":
        return None, ordered
    needle = checked_roster.casefold()
    exact = [
        pair
        for pair in ordered
        if needle in {pair[0]["id"].casefold(), pair[0]["name"].casefold()}
    ]
    matches = exact or [
        pair
        for pair in ordered
        if needle in pair[0]["id"].casefold() or needle in pair[0]["name"].casefold()
    ]
    if not matches:
        choices = ", ".join(pair[0]["name"] for pair in ordered[:30])
        raise BalanceError(f"Unknown roster {checked_roster!r}. Available roster families include: {choices}.")
    if len(matches) > 1:
        choices = ", ".join(pair[0]["name"] for pair in matches[:12])
        raise BalanceError(f"Roster {checked_roster!r} is ambiguous. Use one exact roster ID or name: {choices}.")
    return checked_roster, matches


def _roster_counts(index: BalanceIndex, troops: Sequence[TroopRecord]) -> dict[str, Any]:
    roles = Counter(_kit_score(index, troop)["role"] for troop in troops)
    ranks = Counter(_troop_rank(index, troop)["group"] for troop in troops)
    item_codes: set[int] = set()
    item_occurrences = 0
    for troop in troops:
        inventory, _ = _inventory_entries(index, troop)
        item_codes.update(item.index for item in inventory)
        item_occurrences += len(inventory)
    return {
        "troop_count": len(troops),
        "direct_source_troop_count": sum(1 for troop in troops if troop.origin in {"literal", "append"}),
        "derived_upgrade_variant_count": sum(1 for troop in troops if troop.origin == "derived_upgrade"),
        "rank_counts": {rank: ranks.get(rank, 0) for rank in ("Normal", "Noble", "Faith/Zealot")},
        "role_counts": dict(sorted(roles.items())),
        "unique_equipped_item_count": len(item_codes),
        "inventory_pool_entry_count": item_occurrences,
    }


def _roster_catalog_rows(index: BalanceIndex, selected: Sequence[tuple[dict[str, str], Sequence[TroopRecord]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family, troops in selected:
        rows.append(
            {
                "roster": family,
                "campaign_cohort": _campaign_cohort(index, troops[0]) if troops else None,
                **_roster_counts(index, troops),
            }
        )
    return rows


def _roster_troop_row(index: BalanceIndex, troop: TroopRecord) -> dict[str, Any]:
    inventory, unknown = _inventory_entries(index, troop)
    return {
        **_troop_overview(index, troop),
        "inventory": [f"itm_{item.code}" for item in inventory],
        "unknown_inventory_indices": unknown,
    }


def _roster_item_rows(
    index: BalanceIndex,
    troops: Sequence[TroopRecord],
    *,
    item_limit: int,
) -> tuple[list[dict[str, Any]], bool]:
    selected_codes = {troop.code for troop in troops}
    usage: Counter[int] = Counter()
    users: dict[int, set[str]] = defaultdict(set)
    for troop in troops:
        inventory, _ = _inventory_entries(index, troop)
        for item in inventory:
            usage[item.index] += 1
            users[item.index].add(troop.code)
    rows: list[dict[str, Any]] = []
    for item_index, occurrences in usage.items():
        item = next((candidate for candidate in index.items if candidate.index == item_index), None)
        if item is None:
            continue
        all_users = set(index.item_users.get(item.index, ()))
        local_users = sorted(users[item.index], key=str.casefold)
        outside_users = sorted(all_users - selected_codes, key=str.casefold)
        rows.append(
            {
                **_item_overview(index, item),
                "inventory_pool_occurrence_count": occurrences,
                "roster_user_count": len(local_users),
                "roster_users": [f"trp_{code}" for code in local_users],
                "outside_roster_user_count": len(outside_users),
                "outside_roster_users": [f"trp_{code}" for code in outside_users[:24]],
                "outside_roster_users_truncated": len(outside_users) > 24,
                "sharing": "roster_local" if not outside_users else "shared_outside_roster",
            }
        )
    rows.sort(key=lambda row: (-int(row["roster_user_count"]), -int(row["inventory_pool_occurrence_count"]), str(row["code"]).casefold()))
    return rows[:item_limit], len(rows) > item_limit


def balance_roster_inventory(
    index: BalanceIndex,
    *,
    roster: str | None = None,
    include_heroes: bool = False,
    include_derived: bool = False,
    roster_limit: int = 80,
    troop_limit: int = 100,
    item_limit: int = 160,
) -> dict[str, Any]:
    """Inventory faction-safe equipment pools without collapsing themed rosters."""

    if not isinstance(include_heroes, bool) or not isinstance(include_derived, bool):
        raise BalanceError("include_heroes and include_derived must be true or false.")
    checked_roster_limit = require_limit(roster_limit, name="roster_limit", maximum=200)
    checked_troop_limit = require_limit(troop_limit, name="troop_limit", maximum=300)
    checked_item_limit = require_limit(item_limit, name="item_limit", maximum=300)
    families, groups = _roster_troop_groups(index, include_heroes=include_heroes, include_derived=include_derived)
    checked_roster, selected = _select_roster_group(families, groups, roster)
    catalog = _roster_catalog_rows(index, selected)
    if checked_roster is None:
        return {
            "mode": "catalog",
            "roster_count": len(catalog),
            "returned_roster_count": min(len(catalog), checked_roster_limit),
            "rosters": catalog[:checked_roster_limit],
            "rosters_truncated": len(catalog) > checked_roster_limit,
            "filters": {"roster": None, "include_heroes": include_heroes, "include_derived": include_derived, "roster_limit": checked_roster_limit},
            "warnings": [
                "Supply one exact roster name or ID to receive its detailed troop-by-troop inventory and faction-local/shared item list.",
                "The five player cultures are intentionally split into themed roster families even though they share a runtime faction, and only one exists after a new-game choice.",
            ],
        }
    family, troops = selected[0]
    troop_rows = [_roster_troop_row(index, troop) for troop in troops[:checked_troop_limit]]
    item_rows, items_truncated = _roster_item_rows(index, troops, item_limit=checked_item_limit)
    return {
        "mode": "inventory",
        "roster": family,
        "campaign_cohort": _campaign_cohort(index, troops[0]),
        "summary": catalog[0],
        "troops": troop_rows,
        "troop_count": len(troops),
        "troops_truncated": len(troops) > checked_troop_limit,
        "items": item_rows,
        "item_count": catalog[0]["unique_equipped_item_count"],
        "items_truncated": items_truncated,
        "filters": {
            "roster": checked_roster,
            "include_heroes": include_heroes,
            "include_derived": include_derived,
            "roster_limit": checked_roster_limit,
            "troop_limit": checked_troop_limit,
            "item_limit": checked_item_limit,
        },
        "warnings": [
            "Inventory entries are randomized engine equipment pools, not a guarantee that every listed item spawns together.",
            "roster_local means no evaluated troop outside this selected roster uses the item; shared_outside_roster is a signal to review wider thematic effects before changing it.",
            "This report documents current equipment ownership. It makes no stat or item-placement changes.",
        ],
    }


def _numeric_summary(values: Sequence[int]) -> dict[str, int | float]:
    if not values:
        return {"count": 0, "minimum": 0, "median": 0, "maximum": 0}
    middle = median(values)
    return {
        "count": len(values),
        "minimum": min(values),
        "median": int(middle) if float(middle).is_integer() else middle,
        "maximum": max(values),
    }


def _rank_role_trajectory(index: BalanceIndex, troops: Sequence[TroopRecord]) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, str], list[TroopRecord]] = defaultdict(list)
    for troop in troops:
        rank = _troop_rank(index, troop)["group"]
        role = _kit_score(index, troop)["role"]
        buckets[(rank, role)].append(troop)
    rows: list[dict[str, Any]] = []
    for (rank, role), records in buckets.items():
        kits = [_kit_score(index, troop) for troop in records]
        rows.append(
            {
                "rank": rank,
                "rank_order": RANK_ORDER[rank],
                "role": role,
                "troop_count": len(records),
                "level": _numeric_summary([_decode_attributes(troop.data[8])["level"] for troop in records]),
                "kit_score": _numeric_summary([kit["kit_score"] for kit in kits]),
                "melee": _numeric_summary([kit["melee"] for kit in kits]),
                "ranged": _numeric_summary([kit["ranged"] for kit in kits]),
                "armor": _numeric_summary([kit["armor"] for kit in kits]),
                "shield": _numeric_summary([kit["shield"] for kit in kits]),
                "mount": _numeric_summary([kit["mount"] for kit in kits]),
            }
        )
    rows.sort(key=lambda row: (int(row["rank_order"]), str(row["role"]).casefold()))
    return rows


def _upgrade_edge_row(index: BalanceIndex, edge: UpgradeEdge) -> dict[str, Any] | None:
    source = index.troop_by_code.get(edge.source)
    target = index.troop_by_code.get(edge.target)
    if source is None or target is None:
        return None
    source_kit = _kit_score(index, source)
    target_kit = _kit_score(index, target)
    source_rank = _troop_rank(index, source)
    target_rank = _troop_rank(index, target)
    source_level = _decode_attributes(source.data[8])["level"]
    target_level = _decode_attributes(target.data[8])["level"]
    signals: list[str] = []
    if target_level < source_level:
        signals.append("target_level_decreases")
    if target_kit["kit_score"] < source_kit["kit_score"]:
        signals.append("kit_score_decreases")
    if target_rank["order"] < source_rank["order"]:
        signals.append("rank_order_decreases")
    return {
        "source_id": f"trp_{source.code}",
        "target_id": f"trp_{target.code}",
        "declaration": edge.declaration,
        "source": {"level": source_level, "role": source_kit["role"], "rank": source_rank["group"], "kit_score": source_kit["kit_score"]},
        "target": {"level": target_level, "role": target_kit["role"], "rank": target_rank["group"], "kit_score": target_kit["kit_score"]},
        "delta": {
            "level": target_level - source_level,
            "kit_score": target_kit["kit_score"] - source_kit["kit_score"],
            "melee": target_kit["melee"] - source_kit["melee"],
            "ranged": target_kit["ranged"] - source_kit["ranged"],
            "armor": target_kit["armor"] - source_kit["armor"],
            "shield": target_kit["shield"] - source_kit["shield"],
            "mount": target_kit["mount"] - source_kit["mount"],
        },
        "review_signals": signals,
        "source_location": {"path": project_relative(edge.path, index.root), "line": edge.line},
    }


def _faith_ascension_row(index: BalanceIndex, edge: UpgradeEdge) -> dict[str, Any] | None:
    candidate = index.troop_by_code.get(edge.source)
    target = index.troop_by_code.get(edge.target)
    if candidate is None or target is None:
        return None
    candidate_kit = _kit_score(index, candidate)
    target_kit = _kit_score(index, target)
    candidate_rank = _troop_rank(index, candidate)["group"]
    target_rank = _troop_rank(index, target)["group"]
    candidate_attributes = _decode_attributes(candidate.data[8])
    target_attributes = _decode_attributes(target.data[8])
    candidate_skills = _decode_skills(candidate.data[10])
    target_skills = _decode_skills(target.data[10])
    candidate_combat_skills = sum(candidate_skills[name] for name in COMBAT_SKILL_NAMES)
    target_combat_skills = sum(target_skills[name] for name in COMBAT_SKILL_NAMES)
    candidate_proficiencies = _decode_proficiencies(candidate.data[9])
    target_proficiencies = _decode_proficiencies(target.data[9])
    candidate_proficiency_total = sum(candidate_proficiencies.values())
    target_proficiency_total = sum(target_proficiencies.values())
    target_contract_issues = sorted(
        set(target_kit["notes"]) & HARD_LOADOUT_NOTES,
        key=str.casefold,
    )
    deltas = {
        "level": target_attributes["level"] - candidate_attributes["level"],
        "kit_score": target_kit["kit_score"] - candidate_kit["kit_score"],
        "combat_skill_total": target_combat_skills - candidate_combat_skills,
        "proficiency_total": target_proficiency_total - candidate_proficiency_total,
    }
    advantage_signals = [
        label
        for label, value in (
            ("level", deltas["level"]),
            ("kit", deltas["kit_score"]),
            ("combat_skills", deltas["combat_skill_total"]),
            ("proficiencies", deltas["proficiency_total"]),
        )
        if value > 0
    ]
    rank_transition_valid = candidate_rank == "Noble" and target_rank == "Faith/Zealot"
    static_status = "faith_advantage_present"
    if target_contract_issues or not rank_transition_valid or not advantage_signals:
        static_status = "needs_review"
    return {
        "noble_candidate_id": f"trp_{candidate.code}",
        "faith_target_id": f"trp_{target.code}",
        "source_rank": candidate_rank,
        "target_rank": target_rank,
        "source_role": candidate_kit["role"],
        "target_role": target_kit["role"],
        "source": {
            "level": candidate_attributes["level"],
            "kit_score": candidate_kit["kit_score"],
            "combat_skill_total": candidate_combat_skills,
            "proficiency_total": candidate_proficiency_total,
        },
        "target": {
            "level": target_attributes["level"],
            "kit_score": target_kit["kit_score"],
            "combat_skill_total": target_combat_skills,
            "proficiency_total": target_proficiency_total,
        },
        "kit_score_delta": deltas["kit_score"],
        "delta": deltas,
        "rank_transition_valid": rank_transition_valid,
        "faith_advantage_signals": advantage_signals,
        "target_loadout_contract_issues": target_contract_issues,
        "static_status": static_status,
        "source_location": {"path": project_relative(edge.path, index.root), "line": edge.line},
    }


def balance_faith_ascensions(index: BalanceIndex) -> dict[str, Any]:
    """Audit the full selected-culture Noble-to-Faith ascension matrix."""

    routes = [row for edge in index.faith_ascensions for row in [_faith_ascension_row(index, edge)] if row is not None]
    routes.sort(key=lambda row: (str(row["noble_candidate_id"]).casefold(), str(row["faith_target_id"]).casefold()))
    candidate_codes = sorted(
        {
            edge.target
            for edge in index.faith_candidate_routes
            if edge.target in index.troop_by_code
        },
        key=str.casefold,
    )
    faith_rosters = {
        _roster_family(index, troop)["id"]
        for troop in index.troops
        if troop.code in index.faith_troop_codes
    }
    present_pairs = {
        (
            row["noble_candidate_id"].removeprefix("trp_"),
            _roster_family(index, index.troop_by_code[row["faith_target_id"].removeprefix("trp_")])["id"],
        )
        for row in routes
    }
    missing_route_pairs = [
        {"noble_candidate_id": f"trp_{candidate}", "faith_roster_id": faith_roster}
        for candidate in candidate_codes
        for faith_roster in sorted(faith_rosters, key=str.casefold)
        if (candidate, faith_roster) not in present_pairs
    ]
    review_signals: list[dict[str, Any]] = []
    for route in routes:
        if route["rank_transition_valid"] and route["faith_advantage_signals"] and not route["target_loadout_contract_issues"]:
            continue
        review_signals.append(
            {
                "code": "FAITH_ASCENSION_STATIC_TIER_CONTRACT",
                "message": "A faith ascension lacks a valid Noble-to-Faith rank transition, a visible elite advantage, or a complete target loadout.",
                "route": route,
            }
        )
    if missing_route_pairs:
        review_signals.append(
            {
                "code": "FAITH_ASCENSION_ROUTE_MATRIX_INCOMPLETE",
                "message": "One or more selected-culture faith candidates lack a route to an authored faith roster.",
                "missing_routes": missing_route_pairs,
            }
        )
    state = "within_static_tier_targets" if routes and not review_signals else "needs_static_rebalance"
    return {
        "mode": "faith_ascension_profile",
        "state": state,
        "route_count": len(routes),
        "expected_route_count": len(candidate_codes) * len(faith_rosters),
        "noble_candidate_count": len(candidate_codes),
        "faith_roster_count": len(faith_rosters),
        "routes": routes,
        "missing_route_pairs": missing_route_pairs,
        "review_signals": review_signals,
        "source_authority": {
            "faith_candidate_mapping": project_relative(index.root / FAITH_CANDIDATE_SOURCE_RELATIVE, index.root),
            "faith_ascension_mapping": project_relative(index.root / FAITH_ASCENSION_SOURCE_RELATIVE, index.root),
            "troops": project_relative(index.troops_path, index.root),
        },
        "warnings": [
            "A faith elite must preserve the authored Noble-to-Faith rank transition, avoid hard inventory-contract failures, and show at least one concrete premium in level, kit, combat skills, or proficiencies.",
            "The profile intentionally does not demand every metric rise. Faith doctrines can exchange a shield, weapon class, or generalist proficiency for a distinct elite battlefield job.",
            "Static evidence cannot prove random loadout rolls, battle AI, wages, faith scarcity, center gates, or live campaign outcomes.",
        ],
    }


def _player_start_upgrade_row(index: BalanceIndex, edge: UpgradeEdge) -> dict[str, Any] | None:
    source = index.troop_by_code.get(edge.source)
    target = index.troop_by_code.get(edge.target)
    if source is None or target is None:
        return None
    source_kit = _kit_score(index, source)
    target_kit = _kit_score(index, target)
    source_rank = _troop_rank(index, source)
    target_rank = _troop_rank(index, target)
    source_attributes = _decode_attributes(source.data[8])
    target_attributes = _decode_attributes(target.data[8])
    source_skills = _decode_skills(source.data[10])
    target_skills = _decode_skills(target.data[10])
    source_combat_skills = sum(source_skills[name] for name in COMBAT_SKILL_NAMES)
    target_combat_skills = sum(target_skills[name] for name in COMBAT_SKILL_NAMES)
    source_proficiency_total = sum(_decode_proficiencies(source.data[9]).values())
    target_proficiency_total = sum(_decode_proficiencies(target.data[9]).values())
    target_contract_issues = sorted(set(target_kit["notes"]) & HARD_LOADOUT_NOTES, key=str.casefold)
    deltas = {
        "level": target_attributes["level"] - source_attributes["level"],
        "kit_score": target_kit["kit_score"] - source_kit["kit_score"],
        "combat_skill_total": target_combat_skills - source_combat_skills,
        "proficiency_total": target_proficiency_total - source_proficiency_total,
    }
    training_advantages = [
        label
        for label, value in (
            ("kit", deltas["kit_score"]),
            ("combat_skills", deltas["combat_skill_total"]),
            ("proficiencies", deltas["proficiency_total"]),
        )
        if value > 0
    ]
    rank_order_preserved = target_rank["order"] >= source_rank["order"]
    static_status = "advances"
    if deltas["level"] <= 0 or not rank_order_preserved or not training_advantages or target_contract_issues:
        static_status = "needs_review"
    progression_class = "kit_and_training_upgrade"
    if deltas["kit_score"] < 0:
        progression_class = "training_compensated_kit_trade"
    return {
        "source_id": f"trp_{source.code}",
        "target_id": f"trp_{target.code}",
        "culture": _roster_family(index, source),
        "declaration": edge.declaration,
        "source": {
            "level": source_attributes["level"],
            "rank": source_rank["group"],
            "role": source_kit["role"],
            "kit_score": source_kit["kit_score"],
            "combat_skill_total": source_combat_skills,
            "proficiency_total": source_proficiency_total,
        },
        "target": {
            "level": target_attributes["level"],
            "rank": target_rank["group"],
            "role": target_kit["role"],
            "kit_score": target_kit["kit_score"],
            "combat_skill_total": target_combat_skills,
            "proficiency_total": target_proficiency_total,
        },
        "delta": deltas,
        "rank_order_preserved": rank_order_preserved,
        "training_advantage_signals": training_advantages,
        "target_loadout_contract_issues": target_contract_issues,
        "progression_class": progression_class,
        "static_status": static_status,
        "source_location": {"path": project_relative(edge.path, index.root), "line": edge.line},
    }


def balance_player_start_progression(index: BalanceIndex) -> dict[str, Any]:
    """Audit direct normal and noble upgrades across the five player cultures."""

    routes = []
    for edge in index.upgrades:
        source = index.troop_by_code.get(edge.source)
        target = index.troop_by_code.get(edge.target)
        if source is None or target is None:
            continue
        source_roster = _roster_family(index, source)["id"]
        target_roster = _roster_family(index, target)["id"]
        if source_roster not in PLAYER_START_ROSTER_IDS or source_roster != target_roster:
            continue
        row = _player_start_upgrade_row(index, edge)
        if row is not None:
            routes.append(row)
    routes.sort(key=lambda row: (str(row["culture"]["name"]).casefold(), str(row["source_id"]).casefold(), str(row["target_id"]).casefold()))
    review_signals = [
        {
            "code": "PLAYER_START_UPGRADE_STATIC_CONTRACT",
            "message": "A direct player-culture upgrade does not clearly advance level/training, drops rank, or has a hard target loadout failure.",
            "route": route,
        }
        for route in routes
        if route["static_status"] != "advances"
    ]
    culture_summaries = []
    for culture in PLAYER_START_CULTURES:
        culture_routes = [route for route in routes if route["culture"]["id"] == culture["roster_id"]]
        culture_summaries.append(
            {
                "culture": {"id": culture["id"], "name": culture["name"], "doctrine": culture["doctrine"]},
                "route_count": len(culture_routes),
                "kit_trade_count": sum(route["progression_class"] == "training_compensated_kit_trade" for route in culture_routes),
                "review_route_count": sum(route["static_status"] != "advances" for route in culture_routes),
            }
        )
    state = "within_static_progression_targets"
    if not routes:
        state = "needs_source_review"
    elif review_signals:
        state = "needs_static_rebalance"
    return {
        "mode": "player_start_progression_profile",
        "state": state,
        "route_count": len(routes),
        "culture_summaries": culture_summaries,
        "kit_trade_count": sum(route["progression_class"] == "training_compensated_kit_trade" for route in routes),
        "routes": routes,
        "review_signals": review_signals,
        "source_authority": {"troops": project_relative(index.troops_path, index.root)},
        "warnings": [
            "Every direct culture upgrade must raise troop level, preserve rank order, avoid hard target loadout failures, and show at least one kit, combat-skill, or proficiency advance.",
            "A negative static kit delta can be intentional when the level and training gains clearly compensate for a themed equipment trade. The report exposes those cases instead of silently accepting or automatically flattening them.",
            "Static progression does not prove recruitment cost, upgrade XP, facility gates, randomized inventory rolls, battle AI, or player experience.",
        ],
    }


def balance_progression(
    index: BalanceIndex,
    *,
    roster: str | None = None,
    include_heroes: bool = False,
    include_derived: bool = False,
    roster_limit: int = 80,
    troop_limit: int = 180,
    edge_limit: int = 220,
) -> dict[str, Any]:
    """Show roster progression without erasing noble or faith access gates."""

    if not isinstance(include_heroes, bool) or not isinstance(include_derived, bool):
        raise BalanceError("include_heroes and include_derived must be true or false.")
    checked_roster_limit = require_limit(roster_limit, name="roster_limit", maximum=200)
    checked_troop_limit = require_limit(troop_limit, name="troop_limit", maximum=300)
    checked_edge_limit = require_limit(edge_limit, name="edge_limit", maximum=300)
    families, groups = _roster_troop_groups(index, include_heroes=include_heroes, include_derived=include_derived)
    checked_roster, selected = _select_roster_group(families, groups, roster)
    catalog = _roster_catalog_rows(index, selected)
    if checked_roster is None:
        return {
            "mode": "catalog",
            "roster_count": len(catalog),
            "returned_roster_count": min(len(catalog), checked_roster_limit),
            "rosters": catalog[:checked_roster_limit],
            "rosters_truncated": len(catalog) > checked_roster_limit,
            "filters": {"roster": None, "include_heroes": include_heroes, "include_derived": include_derived, "roster_limit": checked_roster_limit},
            "warnings": [
                "Supply one exact roster name or ID to inspect its normal and noble paths plus cross-roster faith ascension routes.",
                "Faith ascension is a scripted noble-candidate mapping, not a normal upgrade() edge, and is reported separately.",
                "A campaign cohort describes which rosters coexist. The five player-start cultures are alternatives, not a single all-cultures in-game force.",
            ],
        }
    family, troops = selected[0]
    selected_codes = {troop.code for troop in troops}
    standard_edges = [
        row
        for edge in index.upgrades
        if edge.source in selected_codes and edge.target in selected_codes
        for row in [_upgrade_edge_row(index, edge)]
        if row is not None
    ]
    standard_edges.sort(key=lambda row: (str(row["source_id"]).casefold(), str(row["target_id"]).casefold()))
    candidate_edges = [
        row
        for edge in index.faith_candidate_routes
        if edge.source in selected_codes and edge.target in selected_codes
        for row in [_upgrade_edge_row(index, edge)]
        if row is not None
    ]
    candidate_edges.sort(key=lambda row: (str(row["source_id"]).casefold(), str(row["target_id"]).casefold()))
    faith_edges = []
    for edge in index.faith_ascensions:
        row = _faith_ascension_row(index, edge)
        if row is None:
            continue
        if row["noble_candidate_id"].removeprefix("trp_") in selected_codes or row["faith_target_id"].removeprefix("trp_") in selected_codes:
            faith_edges.append(row)
    faith_edges.sort(key=lambda row: (str(row["noble_candidate_id"]).casefold(), str(row["faith_target_id"]).casefold()))
    progression_edges = [
        edge
        for edge in (*index.upgrades, *index.faith_candidate_routes)
        if edge.source in selected_codes and edge.target in selected_codes
    ]
    incoming = {edge.target for edge in progression_edges}
    outgoing = {edge.source for edge in progression_edges}
    outgoing.update(edge.source for edge in index.faith_ascensions if edge.source in selected_codes)
    roots = [f"trp_{troop.code}" for troop in troops if troop.code not in incoming]
    endpoints = [f"trp_{troop.code}" for troop in troops if troop.code not in outgoing]
    troop_rows = [_roster_troop_row(index, troop) for troop in troops[:checked_troop_limit]]
    return {
        "mode": "progression",
        "roster": family,
        "campaign_cohort": _campaign_cohort(index, troops[0]),
        "summary": catalog[0],
        "rank_role_trajectory": _rank_role_trajectory(index, troops),
        "explicit_upgrade_edges": standard_edges[:checked_edge_limit],
        "explicit_upgrade_edge_count": len(standard_edges),
        "explicit_upgrade_edges_truncated": len(standard_edges) > checked_edge_limit,
        "faith_candidate_routes": candidate_edges[:checked_edge_limit],
        "faith_candidate_route_count": len(candidate_edges),
        "faith_candidate_routes_truncated": len(candidate_edges) > checked_edge_limit,
        "faith_ascensions": faith_edges[:checked_edge_limit],
        "faith_ascension_count": len(faith_edges),
        "faith_ascensions_truncated": len(faith_edges) > checked_edge_limit,
        "upgrade_roots": roots,
        "upgrade_endpoints": endpoints,
        "troops": troop_rows,
        "troop_count": len(troops),
        "troops_truncated": len(troops) > checked_troop_limit,
        "rank_evidence": {
            "noble_runtime_list": "compile/module_troops.py:sod_noble_troops",
            "faith_runtime_list": "compile/module_troops.py:sod_faith_troops",
            "faith_candidate_mapping": project_relative(index.root / FAITH_CANDIDATE_SOURCE_RELATIVE, index.root),
            "faith_ascension_mapping": project_relative(index.root / FAITH_ASCENSION_SOURCE_RELATIVE, index.root),
        },
        "filters": {
            "roster": checked_roster,
            "include_heroes": include_heroes,
            "include_derived": include_derived,
            "roster_limit": checked_roster_limit,
            "troop_limit": checked_troop_limit,
            "edge_limit": checked_edge_limit,
        },
        "warnings": [
            "Normal, noble, and faith/zealot tiers are access tiers. Their aggregate scores are evidence for role-specific review, not a requirement that every metric rise on every branch.",
            "kit_score chooses strongest entries from randomized pools and cannot establish exact spawned loadout, battle outcome, wage value, or upgrade availability by itself.",
            "Authored '*' candidate troops remain visible as Noble faith candidates. Their scripted top-noble-to-candidate and candidate-to-faith links are reported separately from ordinary upgrade() edges.",
        ],
    }


def _campaign_cohort_groups(
    index: BalanceIndex,
    *,
    include_heroes: bool,
    include_derived: bool,
) -> tuple[dict[str, dict[str, str]], dict[str, list[TroopRecord]], dict[str, dict[str, dict[str, str]]]]:
    cohorts: dict[str, dict[str, str]] = {}
    groups: dict[str, list[TroopRecord]] = defaultdict(list)
    rosters: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for troop in index.troops:
        if not include_heroes and bool(int(troop.data[3]) & TF_HERO):
            continue
        if not include_derived and troop.origin == "derived_upgrade":
            continue
        cohort = _campaign_cohort(index, troop)
        cohorts[cohort["id"]] = cohort
        groups[cohort["id"]].append(troop)
        family = _roster_family(index, troop)
        rosters[cohort["id"]][family["id"]] = family
    for troops in groups.values():
        troops.sort(key=lambda troop: (str(troop.data[1]).casefold(), troop.code.casefold()))
    return cohorts, groups, rosters


def _select_campaign_cohort(
    cohorts: Mapping[str, Mapping[str, str]],
    groups: Mapping[str, Sequence[TroopRecord]],
    rosters: Mapping[str, Mapping[str, Mapping[str, str]]],
    cohort: str | None,
) -> tuple[str | None, list[tuple[dict[str, str], list[TroopRecord], list[dict[str, str]]]]]:
    checked_cohort = optional_string(cohort, name="cohort", maximum=160)
    ordered = [
        (
            dict(cohorts[cohort_id]),
            list(groups[cohort_id]),
            [dict(value) for _, value in sorted(rosters[cohort_id].items(), key=lambda item: (item[1]["name"].casefold(), item[0].casefold()))],
        )
        for cohort_id in sorted(
            groups,
            key=lambda value: (
                cohorts[value]["campaign_group"].casefold(),
                cohorts[value]["name"].casefold(),
                value.casefold(),
            ),
        )
    ]
    if checked_cohort is None or checked_cohort.casefold() == "all":
        return None, ordered
    needle = checked_cohort.casefold()
    exact = [
        entry
        for entry in ordered
        if needle in {entry[0]["id"].casefold(), entry[0]["name"].casefold()}
    ]
    matches = exact or [
        entry
        for entry in ordered
        if needle in entry[0]["id"].casefold() or needle in entry[0]["name"].casefold()
    ]
    if not matches:
        choices = ", ".join(entry[0]["name"] for entry in ordered[:30])
        raise BalanceError(f"Unknown campaign cohort {checked_cohort!r}. Available cohorts include: {choices}.")
    if len(matches) > 1:
        choices = ", ".join(entry[0]["name"] for entry in matches[:12])
        raise BalanceError(f"Campaign cohort {checked_cohort!r} is ambiguous. Use one exact cohort ID or name: {choices}.")
    return checked_cohort, matches


def _campaign_cohort_row(
    index: BalanceIndex,
    cohort: Mapping[str, str],
    troops: Sequence[TroopRecord],
    rosters: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    return {
        "cohort": dict(cohort),
        "roster_count": len(rosters),
        "rosters": [dict(roster) for roster in rosters],
        **_roster_counts(index, troops),
    }


def balance_campaign_cohorts(
    index: BalanceIndex,
    *,
    cohort: str | None = None,
    include_heroes: bool = False,
    include_derived: bool = False,
    cohort_limit: int = 80,
    troop_limit: int = 180,
) -> dict[str, Any]:
    """Expose campaign coexistence so balance reports cannot invent factions."""

    if not isinstance(include_heroes, bool) or not isinstance(include_derived, bool):
        raise BalanceError("include_heroes and include_derived must be true or false.")
    checked_cohort_limit = require_limit(cohort_limit, name="cohort_limit", maximum=120)
    checked_troop_limit = require_limit(troop_limit, name="troop_limit", maximum=300)
    cohorts, groups, rosters = _campaign_cohort_groups(
        index,
        include_heroes=include_heroes,
        include_derived=include_derived,
    )
    checked_cohort, selected = _select_campaign_cohort(cohorts, groups, rosters, cohort)
    catalog = [_campaign_cohort_row(index, current, troops, roster_rows) for current, troops, roster_rows in selected]
    if checked_cohort is None:
        return {
            "mode": "catalog",
            "cohort_count": len(catalog),
            "returned_cohort_count": min(len(catalog), checked_cohort_limit),
            "cohorts": catalog[:checked_cohort_limit],
            "cohorts_truncated": len(catalog) > checked_cohort_limit,
            "filters": {
                "cohort": None,
                "include_heroes": include_heroes,
                "include_derived": include_derived,
                "cohort_limit": checked_cohort_limit,
            },
            "warnings": [
                "Campaign cohorts are not equipment pools. Use roster-inventory for item ownership and progression for a single troop route.",
                "The five SoD player-start cultures are mutually exclusive. Only the selected culture belongs to a given campaign; the other four are comparison baselines, not allied or enemy rosters.",
                "The Imperial Expedition is deliberately separate from native-world averages because it is a delayed invasion with its own wave, supply, and total-war behavior.",
            ],
        }
    selected_cohort, troops, roster_rows = selected[0]
    return {
        "mode": "cohort",
        "cohort": selected_cohort,
        "summary": catalog[0],
        "troops": [_roster_troop_row(index, troop) for troop in troops[:checked_troop_limit]],
        "troop_count": len(troops),
        "troops_truncated": len(troops) > checked_troop_limit,
        "filters": {
            "cohort": checked_cohort,
            "include_heroes": include_heroes,
            "include_derived": include_derived,
            "cohort_limit": checked_cohort_limit,
            "troop_limit": checked_troop_limit,
        },
        "warnings": [
            selected_cohort["analysis_policy"],
            "Static troop evidence does not prove a campaign party's actual spawned mix, wages, facilities, availability, or battle result.",
        ],
    }


def _display_expected(value: float) -> int | float:
    return int(value) if value.is_integer() else round(value, 2)


def _stack_mix(rows: Sequence[Mapping[str, Any]], field: str) -> dict[str, dict[str, int | float]]:
    minimum: Counter[str] = Counter()
    maximum: Counter[str] = Counter()
    expected: Counter[str] = Counter()
    for row in rows:
        label = str(row[field])
        minimum[label] += int(row["minimum"])
        maximum[label] += int(row["maximum"])
        expected[label] += float(row["expected"])
    return {
        label: {
            "minimum": minimum[label],
            "maximum": maximum[label],
            "expected": _display_expected(float(expected[label])),
        }
        for label in sorted(expected, key=str.casefold)
    }


def _weighted_static_average(rows: Sequence[Mapping[str, Any]], field: str) -> int | float:
    total_weight = sum(float(row["expected"]) for row in rows if row.get(field) is not None)
    if total_weight <= 0:
        return 0
    total = sum(float(row["expected"]) * float(row[field]) for row in rows if row.get(field) is not None)
    return _display_expected(total / total_weight)


def _party_template_profile(index: BalanceIndex, template: PartyTemplateRecord) -> dict[str, Any]:
    stack_rows: list[dict[str, Any]] = []
    missing_troops: list[str] = []
    for stack in template.stacks:
        expected = (stack.minimum + stack.maximum) / 2.0
        troop = index.troop_by_code.get(stack.troop_code)
        if troop is None:
            missing_troops.append(f"trp_{stack.troop_code}")
            stack_rows.append(
                {
                    "troop_id": f"trp_{stack.troop_code}",
                    "minimum": stack.minimum,
                    "maximum": stack.maximum,
                    "expected": _display_expected(expected),
                    "missing_from_evaluated_troops": True,
                }
            )
            continue
        kit = _kit_score(index, troop)
        rank = _troop_rank(index, troop)
        stack_rows.append(
            {
                "troop_id": f"trp_{troop.code}",
                "name": str(troop.data[1]),
                "minimum": stack.minimum,
                "maximum": stack.maximum,
                "expected": _display_expected(expected),
                "role": kit["role"],
                "rank": rank["group"],
                "level": _decode_attributes(troop.data[8])["level"],
                "kit_score": kit["kit_score"],
            }
        )
    minimum_total = sum(int(row["minimum"]) for row in stack_rows)
    maximum_total = sum(int(row["maximum"]) for row in stack_rows)
    return {
        "template_id": f"pt_{template.code}",
        "name": template.name,
        "source_location": {"path": project_relative(template.path, index.root), "line": template.line},
        "member_total": {
            "minimum": minimum_total,
            "maximum": maximum_total,
            "expected": _display_expected(sum(float(row["expected"]) for row in stack_rows)),
        },
        "role_mix": _stack_mix([row for row in stack_rows if "role" in row], "role"),
        "rank_mix": _stack_mix([row for row in stack_rows if "rank" in row], "rank"),
        "static_stack_weighted_evidence": {
            "average_level": _weighted_static_average(stack_rows, "level"),
            "average_kit_score": _weighted_static_average(stack_rows, "kit_score"),
        },
        "stacks": stack_rows,
        "missing_troop_ids": missing_troops,
    }


def _aggregate_invasion_waves(waves: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    stacks = [stack for wave in waves for stack in wave["stacks"] if "role" in stack]
    return {
        "meaning": "Reference composition if each listed core template is applied once. Engine cadence and selection decide actual party composition.",
        "member_total": {
            "minimum": sum(int(stack["minimum"]) for stack in stacks),
            "maximum": sum(int(stack["maximum"]) for stack in stacks),
            "expected": _display_expected(sum(float(stack["expected"]) for stack in stacks)),
        },
        "role_mix": _stack_mix(stacks, "role"),
        "rank_mix": _stack_mix(stacks, "rank"),
        "static_stack_weighted_evidence": {
            "average_level": _weighted_static_average(stacks, "level"),
            "average_kit_score": _weighted_static_average(stacks, "kit_score"),
        },
    }


def _scaled_member_total(member_total: Mapping[str, int | float], multiplier: int) -> dict[str, int | float]:
    return {
        key: _display_expected(float(member_total[key]) * multiplier)
        for key in ("minimum", "maximum", "expected")
    }


def _imperial_entry_range(index: BalanceIndex) -> dict[str, Any]:
    path = index.root / CONSTANTS_SOURCE_RELATIVE
    result: dict[str, Any] = {
        "source": project_relative(path, index.root),
        "status": "missing_source",
        "begin_party_id": None,
        "end_party_id_exclusive": None,
        "begin_index": None,
        "end_index_exclusive": None,
        "entry_point_count": None,
    }
    if not path.is_file():
        return result
    source = _read_utf8_source(path)
    begin = _named_string_assignment(source, "imperial_invasion_entry_villages_begin")
    end = _named_string_assignment(source, "imperial_invasion_entry_villages_end")
    if begin is None or end is None:
        result["status"] = "missing_constants"
        return result
    begin_party, begin_line = begin
    end_party, end_line = end
    result.update(
        {
            "begin_party_id": begin_party,
            "end_party_id_exclusive": end_party,
            "constant_locations": {"begin_line": begin_line, "end_line": end_line},
        }
    )
    if not begin_party.startswith("p_") or not end_party.startswith("p_"):
        result["status"] = "invalid_party_constants"
        return result
    begin_index = index.party_ids.get(begin_party[2:])
    end_index = index.party_ids.get(end_party[2:])
    result.update({"begin_index": begin_index, "end_index_exclusive": end_index})
    if begin_index is None or end_index is None:
        result["status"] = "missing_party_ids"
        return result
    if end_index <= begin_index:
        result["status"] = "invalid_range"
        return result
    result["entry_point_count"] = end_index - begin_index
    result["status"] = "present"
    return result


def _pre_invasion_staging(
    index: BalanceIndex,
    auxiliary_template: PartyTemplateRecord | None,
) -> dict[str, Any]:
    path = index.root / IMPERIAL_PRE_INVASION_SOURCE_RELATIVE
    result: dict[str, Any] = {
        "source": project_relative(path, index.root),
        "status": "missing_auxiliary_template",
        "entry_range": _imperial_entry_range(index),
        "stages": [],
        "cumulative_upper_bound_across_entry_range": None,
    }
    if auxiliary_template is None:
        return result
    template = _party_template_profile(index, auxiliary_template)
    result["auxiliary_template_id"] = template["template_id"]
    result["template_member_total"] = template["member_total"]
    if not path.is_file():
        result["status"] = "missing_source"
        return result
    source = _read_utf8_source(path)
    pattern = re.compile(
        r'\(eq,\s*":delta",\s*(?P<days>90|60|30)\s*\),(?P<body>.*?)(?=^\s*\(else_try\),|^\s*\(try_end\),)',
        re.DOTALL | re.MULTILINE,
    )
    staged: dict[int, dict[str, Any]] = {}
    for match in pattern.finditer(source):
        days = int(match.group("days"))
        body = match.group("body")
        spawn_count = len(re.findall(r"\(\s*spawn_around_party\s*,", body))
        add_count = len(re.findall(r"\(\s*party_add_template\s*,", body))
        applications = spawn_count + add_count
        if applications <= 0:
            continue
        staged[days] = {
            "days_before_invasion": days,
            "source_line": source.count("\n", 0, match.start()) + 1,
            "spawn_template_applications": spawn_count,
            "party_add_template_applications": add_count,
            "template_applications_per_successful_spawn": applications,
            "member_total_per_successful_spawn": _scaled_member_total(template["member_total"], applications),
        }
    entry_count = result["entry_range"].get("entry_point_count")
    stages: list[dict[str, Any]] = []
    for days in (90, 60, 30):
        stage = staged.get(days)
        if stage is None:
            continue
        if isinstance(entry_count, int):
            stage["upper_bound_across_entry_range"] = _scaled_member_total(
                template["member_total"],
                int(stage["template_applications_per_successful_spawn"]) * entry_count,
            )
        else:
            stage["upper_bound_across_entry_range"] = None
        stages.append(stage)
    result["stages"] = stages
    if isinstance(entry_count, int) and stages:
        total_applications = sum(int(stage["template_applications_per_successful_spawn"]) for stage in stages)
        result["cumulative_upper_bound_across_entry_range"] = _scaled_member_total(
            template["member_total"],
            total_applications * entry_count,
        )
    result["status"] = "present" if len(stages) == 3 and result["entry_range"]["status"] == "present" else "needs_review"
    result["warnings"] = [
        "This is a source-level upper bound if every listed entry point spawns successfully and all staged auxiliary parties survive. It is not a live party-count measurement.",
        "spawn_around_party creates the initial template party; each following party_add_template is counted as one additional template application.",
    ]
    return result


def _source_contract_row(
    index: BalanceIndex,
    check_id: str,
    relative: Path,
    description: str,
    tokens: Sequence[str],
) -> dict[str, Any]:
    path = index.root / relative
    if not path.is_file():
        return {
            "id": check_id,
            "description": description,
            "source": project_relative(path, index.root),
            "status": "missing_source",
            "missing_tokens": list(tokens),
            "matches": [],
        }
    source = _read_utf8_source(path)
    matches = []
    missing = []
    for token in tokens:
        offset = source.find(token)
        if offset < 0:
            missing.append(token)
            continue
        matches.append({"token": token, "line": source.count("\n", 0, offset) + 1})
    return {
        "id": check_id,
        "description": description,
        "source": project_relative(path, index.root),
        "status": "present" if not missing else "needs_review",
        "missing_tokens": missing,
        "matches": matches,
    }


def _imperial_source_evidence(index: BalanceIndex) -> list[dict[str, Any]]:
    checks: tuple[tuple[str, Path, str, tuple[str, ...]], ...] = (
        (
            "pre_invasion_auxiliary_staging",
            IMPERIAL_PRE_INVASION_SOURCE_RELATIVE,
            "Imperial auxiliary parties stage before the main invasion and the core faction activates on the invasion day.",
            ("pt_legion_mercenaries", "$g_sod_invasion_begin", "fac_kingdom_6"),
        ),
        (
            "core_reinforcement_binding",
            IMPERIAL_GAME_START_SOURCE_RELATIVE,
            "The Imperial culture binds all three named core reinforcement templates during campaign initialization.",
            ("pt_kingdom_6_reinforcements_a", "pt_kingdom_6_reinforcements_b", "pt_kingdom_6_reinforcements_c"),
        ),
        (
            "invasion_pressure_and_supply",
            IMPERIAL_EXPEDITION_SOURCE_RELATIVE,
            "The daily expedition system tracks pressure and supply, preserves total war, and applies a low-supply power penalty.",
            ("sod_imperial_expedition_process_campaign", "slot_faction_imperial_expedition_supply", 'lt, ":supply", 20'),
        ),
        (
            "coalition_counterplay",
            IMPERIAL_EXPEDITION_SOURCE_RELATIVE,
            "Native-realm and mini-faction relationships contribute to anti-Legion delay and counterplay.",
            ("sod_imperial_expedition_calculate_anti_legion_coalition", "native_kingdoms_begin, native_kingdoms_end", "fac_sod_merc_guild7"),
        ),
        (
            "autoresolve_doctrine_alignment",
            IMPERIAL_DOCTRINE_SOURCE_RELATIVE,
            "The autoresolve doctrine modifier recognizes the actual ief_ troop IDs used by the core Expedition.",
            ('troop_name.startswith("ief_")',),
        ),
    )
    return [_source_contract_row(index, check_id, relative, description, tokens) for check_id, relative, description, tokens in checks]


def balance_imperial_invasion(
    index: BalanceIndex,
    *,
    include_auxiliaries: bool = False,
) -> dict[str, Any]:
    """Inspect Imperial wave composition and campaign controls without flattening it."""

    if not isinstance(include_auxiliaries, bool):
        raise BalanceError("include_auxiliaries must be true or false.")
    templates = {template.code: template for template in index.party_templates}
    missing_core = [f"pt_{code}" for code in IMPERIAL_CORE_TEMPLATE_CODES if code not in templates]
    core_waves = [_party_template_profile(index, templates[code]) for code in IMPERIAL_CORE_TEMPLATE_CODES if code in templates]
    auxiliary_template = templates.get(IMPERIAL_AUXILIARY_TEMPLATE_CODE)
    auxiliary = None
    if include_auxiliaries and auxiliary_template is not None:
        auxiliary = _party_template_profile(index, auxiliary_template)
    pre_invasion_staging = _pre_invasion_staging(index, auxiliary_template)
    source_evidence = _imperial_source_evidence(index)
    source_contracts_present = all(row["status"] == "present" for row in source_evidence)
    readiness = (
        "source_contracts_present"
        if not missing_core and source_contracts_present and pre_invasion_staging["status"] == "present"
        else "needs_source_review"
    )
    return {
        "mode": "imperial_invasion_profile",
        "cohort": dict(CAMPAIGN_COHORTS["campaign:imperial-expedition"]),
        "source_authority": {
            "party_templates": project_relative(index.party_templates_path, index.root),
            "troops": project_relative(index.troops_path, index.root),
            "campaign_script": project_relative(index.root / IMPERIAL_EXPEDITION_SOURCE_RELATIVE, index.root),
        },
        "core_waves": core_waves,
        "core_wave_count": len(core_waves),
        "missing_core_template_ids": missing_core,
        "core_wave_reference_composition": _aggregate_invasion_waves(core_waves),
        "auxiliary_staging": auxiliary,
        "pre_invasion_staging": pre_invasion_staging,
        "source_contracts": source_evidence,
        "readiness": readiness,
        "filters": {"include_auxiliaries": include_auxiliaries},
        "warnings": [
            "Core wave totals are template composition evidence, not a prediction of a spawned party or a battle result.",
            "The Imperial Expedition is intentionally reviewed as a delayed invasion with supply, pressure, total-war, centurion, and coalition-counterplay systems; it is not a normal faction-average target.",
            "Pre-invasion auxiliary totals are intentionally labeled as source-level upper bounds. Spawn failure, casualties, despawn, and player intervention must be measured in a live campaign.",
            "Static kit scores and template counts do not replace live tests of invasion timing, lord wealth, party growth, siege pressure, player preparation, or attrition.",
        ],
    }


def _player_start_template_bindings(index: BalanceIndex) -> dict[str, Any]:
    path = index.root / PLAYER_FACTION_ACTIVATION_SOURCE_RELATIVE
    result: dict[str, Any] = {
        "source": project_relative(path, index.root),
        "status": "missing_source",
        "cultures": {},
        "missing_country_markers": [],
    }
    if not path.is_file():
        return result
    source = _read_utf8_source(path)
    binding_anchor = source.find("slot_faction_deserter_troop")
    binding_start = source.rfind("(try_begin)", 0, binding_anchor) if binding_anchor >= 0 else 0
    if binding_start < 0:
        binding_start = 0
    markers: list[tuple[int, Mapping[str, str]]] = []
    for culture in PLAYER_START_CULTURES:
        marker = f'(eq, "$g_sod_country", {culture["country"]})'
        offset = source.find(marker, binding_start)
        if offset < 0:
            result["missing_country_markers"].append(culture["country"])
            continue
        markers.append((offset, culture))
    markers.sort(key=lambda row: row[0])
    for position, (start, culture) in enumerate(markers):
        end = markers[position + 1][0] if position + 1 < len(markers) else len(source)
        block = source[start:end]
        template_codes: dict[str, str] = {}
        missing_slots: list[str] = []
        for slot in ("a", "b", "c"):
            slot_name = f"slot_faction_reinforcements_{slot}"
            pattern = re.compile(
                rf'\(\s*faction_set_slot\s*,\s*"fac_player_supporters_faction"\s*,\s*{re.escape(slot_name)}\s*,\s*"pt_(?P<template>[A-Za-z_][A-Za-z0-9_]*)"\s*\)'
            )
            match = pattern.search(block)
            if match is None:
                missing_slots.append(slot)
                continue
            template_codes[slot] = match.group("template")
        result["cultures"][culture["id"]] = {
            "country": culture["country"],
            "source_line": source.count("\n", 0, start) + 1,
            "template_codes": template_codes,
            "missing_template_slots": missing_slots,
            "status": "present" if not missing_slots else "needs_review",
        }
    result["status"] = "present" if len(markers) == len(PLAYER_START_CULTURES) and not result["missing_country_markers"] and all(row["status"] == "present" for row in result["cultures"].values()) else "needs_review"
    return result


def _native_template_bindings(index: BalanceIndex) -> dict[str, Any]:
    """Read the campaign initializer's actual Native A/B/C assignments."""

    path = index.root / IMPERIAL_GAME_START_SOURCE_RELATIVE
    result: dict[str, Any] = {
        "source": project_relative(path, index.root),
        "status": "missing_source",
        "kingdoms": {},
        "missing_culture_markers": [],
    }
    if not path.is_file():
        return result
    source = _read_utf8_source(path)
    markers: list[tuple[int, Mapping[str, str]]] = []
    for kingdom in NATIVE_KINGDOMS:
        marker = f'(faction_slot_eq, ":faction_no", slot_faction_culture, "{kingdom["culture_constant"]}")'
        offset = source.find(marker)
        if offset < 0:
            result["missing_culture_markers"].append(kingdom["culture_constant"])
            continue
        markers.append((offset, kingdom))
    markers.sort(key=lambda row: row[0])
    for position, (start, kingdom) in enumerate(markers):
        end = markers[position + 1][0] if position + 1 < len(markers) else len(source)
        block = source[start:end]
        template_codes: dict[str, str] = {}
        missing_slots: list[str] = []
        for slot in ("a", "b", "c"):
            slot_name = f"slot_faction_reinforcements_{slot}"
            pattern = re.compile(
                rf'\(\s*faction_set_slot\s*,\s*":faction_no"\s*,\s*{re.escape(slot_name)}\s*,\s*"pt_(?P<template>[A-Za-z_][A-Za-z0-9_]*)"\s*\)'
            )
            match = pattern.search(block)
            if match is None:
                missing_slots.append(slot)
                continue
            template_codes[slot] = match.group("template")
        result["kingdoms"][kingdom["id"]] = {
            "culture": kingdom["culture"],
            "culture_constant": kingdom["culture_constant"],
            "source_line": source.count("\n", 0, start) + 1,
            "template_codes": template_codes,
            "missing_template_slots": missing_slots,
            "status": "present" if not missing_slots else "needs_review",
        }
    result["status"] = "present" if len(markers) == len(NATIVE_KINGDOMS) and not result["missing_culture_markers"] and all(row["status"] == "present" for row in result["kingdoms"].values()) else "needs_review"
    return result


def _template_mix_pressure(
    template_profiles: Mapping[str, Mapping[str, Any]],
    selections: Sequence[tuple[str, float]],
) -> dict[str, Any]:
    selected: list[dict[str, Any]] = []
    missing_slots: list[str] = []
    expected_members = 0.0
    pressure = 0.0
    for slot, probability in selections:
        profile = template_profiles.get(slot)
        if profile is None or profile.get("status") != "present":
            missing_slots.append(slot)
            continue
        member_total = float(profile["member_total"]["expected"])
        kit_score = float(profile["static_stack_weighted_evidence"]["average_kit_score"])
        expected_members += probability * member_total
        pressure += probability * member_total * kit_score
        selected.append(
            {
                "template_slot": slot,
                "template_id": profile["template_id"],
                "selection_probability": _display_expected(probability),
                "member_total_expected": _display_expected(member_total),
                "static_average_kit_score": _display_expected(kit_score),
            }
        )
    if missing_slots:
        return {
            "status": "missing_template_profile",
            "selection": selected,
            "missing_template_slots": missing_slots,
            "expected_members_per_reinforcement_call": None,
            "static_average_kit_score": None,
            "static_pressure_proxy": None,
        }
    return {
        "status": "present",
        "selection": selected,
        "missing_template_slots": [],
        "expected_members_per_reinforcement_call": _display_expected(expected_members),
        "static_average_kit_score": _display_expected(pressure / expected_members) if expected_members else 0,
        "static_pressure_proxy": _display_expected(pressure),
    }


def _player_start_pressure_spread(
    cultures: Sequence[Mapping[str, Any]],
    context: str,
) -> dict[str, Any]:
    target_ratio = float(PLAYER_START_MAX_PRESSURE_SPREAD[context])
    values = [
        (str(culture["culture"]["name"]), float(culture["reinforcement_contexts"][context]["static_pressure_proxy"]))
        for culture in cultures
        if culture["reinforcement_contexts"][context]["status"] == "present"
    ]
    if len(values) != len(PLAYER_START_CULTURES):
        return {
            "status": "missing_culture_profiles",
            "target_max_ratio": target_ratio,
            "within_target": False,
            "values": [],
        }
    lowest_name, lowest = min(values, key=lambda row: (row[1], row[0].casefold()))
    highest_name, highest = max(values, key=lambda row: (row[1], row[0].casefold()))
    ratio = highest / lowest if lowest else 0.0
    return {
        "status": "present",
        "target_max_ratio": target_ratio,
        "within_target": ratio <= target_ratio,
        "lowest": {"culture": lowest_name, "static_pressure_proxy": _display_expected(lowest)},
        "highest": {"culture": highest_name, "static_pressure_proxy": _display_expected(highest)},
        "ratio": round(ratio, 3),
        "values": [
            {"culture": name, "static_pressure_proxy": _display_expected(value)}
            for name, value in sorted(values, key=lambda row: (row[1], row[0].casefold()))
        ],
    }


def balance_player_start_factions(index: BalanceIndex) -> dict[str, Any]:
    """Compare selected-culture reinforcement pressure without flattening doctrine."""

    bindings = _player_start_template_bindings(index)
    templates = {template.code: template for template in index.party_templates}
    culture_rows: list[dict[str, Any]] = []
    missing_template_ids: list[str] = []
    for culture in PLAYER_START_CULTURES:
        binding = bindings["cultures"].get(culture["id"])
        template_profiles: dict[str, dict[str, Any]] = {}
        for slot in ("a", "b", "c"):
            template_code = None if binding is None else binding["template_codes"].get(slot)
            template = None if template_code is None else templates.get(template_code)
            if template is None:
                if template_code is not None:
                    missing_template_ids.append(f"pt_{template_code}")
                template_profiles[slot] = {
                    "template_id": None if template_code is None else f"pt_{template_code}",
                    "status": "missing_binding" if template_code is None else "missing_template",
                    "member_total": {"minimum": 0, "maximum": 0, "expected": 0},
                    "static_stack_weighted_evidence": {"average_kit_score": 0},
                    "stacks": [],
                    "missing_troop_ids": [],
                }
                continue
            profile = _party_template_profile(index, template)
            profile["status"] = "present" if not profile["missing_troop_ids"] else "needs_review"
            template_profiles[slot] = profile
        contexts = {
            context: _template_mix_pressure(template_profiles, selections)
            for context, selections in PLAYER_START_REINFORCEMENT_CONTEXTS.items()
        }
        culture_rows.append(
            {
                "culture": {"id": culture["id"], "name": culture["name"], "country": culture["country"]},
                "cohort": dict(CAMPAIGN_COHORTS[culture["cohort_id"]]),
                "roster": {"id": culture["roster_id"], "name": culture["name"]},
                "doctrine": culture["doctrine"],
                "activation_binding": binding,
                "templates": template_profiles,
                "reinforcement_contexts": contexts,
            }
        )
    source_contracts = [
        _source_contract_row(
            index,
            "player_culture_template_binding",
            PLAYER_FACTION_ACTIVATION_SOURCE_RELATIVE,
            "Each selected SoD culture binds its player-supporter faction to three reinforcement templates.",
            tuple(culture["country"] for culture in PLAYER_START_CULTURES) + ("slot_faction_reinforcements_a", "slot_faction_reinforcements_b", "slot_faction_reinforcements_c"),
        ),
        _source_contract_row(
            index,
            "reinforcement_context_selection",
            PARTY_REINFORCEMENT_SOURCE_RELATIVE,
            "Towns and castles select A 65% / B 35%; kingdom hero parties select A 50% / B 25% / C 25%.",
            ('(lt, ":rand", 65)', '(lt, ":rand", 50)', '(lt, ":rand", 75)', "slot_faction_reinforcements_a", "slot_faction_reinforcements_b", "slot_faction_reinforcements_c"),
        ),
    ]
    pressure_spreads = {
        context: _player_start_pressure_spread(culture_rows, context)
        for context in PLAYER_START_REINFORCEMENT_CONTEXTS
    }
    review_signals: list[dict[str, Any]] = []
    for context, spread in pressure_spreads.items():
        if spread["status"] != "present" or spread["within_target"]:
            continue
        review_signals.append(
            {
                "code": "PLAYER_START_REINFORCEMENT_PRESSURE_SPREAD",
                "context": context,
                "message": "Static reinforcement pressure exceeds the selected-culture review target.",
                "evidence": spread,
            }
        )
    source_contracts_present = bindings["status"] == "present" and all(row["status"] == "present" for row in source_contracts)
    profiles_present = all(
        profile["status"] == "present"
        for culture in culture_rows
        for profile in culture["templates"].values()
    )
    state = "within_static_balance_targets"
    if not source_contracts_present or not profiles_present:
        state = "needs_source_review"
    elif review_signals:
        state = "needs_static_rebalance"
    return {
        "mode": "player_start_faction_profile",
        "player_start_culture_count": len(culture_rows),
        "source_authority": {
            "party_templates": project_relative(index.party_templates_path, index.root),
            "culture_activation": project_relative(index.root / PLAYER_FACTION_ACTIVATION_SOURCE_RELATIVE, index.root),
            "reinforcement_selection": project_relative(index.root / PARTY_REINFORCEMENT_SOURCE_RELATIVE, index.root),
        },
        "cultures": culture_rows,
        "pressure_spreads": pressure_spreads,
        "missing_template_ids": sorted(set(missing_template_ids), key=str.casefold),
        "source_contracts": source_contracts,
        "review_signals": review_signals,
        "state": state,
        "warnings": [
            "The five cultures are mutually exclusive player-start choices. This profile compares alternative campaign baselines, not five coexisting allied or enemy factions.",
            "Static pressure is expected template size multiplied by stack-weighted kit score. It is a review aid for reinforcement composition, not battle simulation, wage cost, upgrade availability, siege AI, or live economic proof.",
            "The spread targets constrain bulk garrison and lord reinforcement pressure only. They intentionally preserve role doctrine, noble access, faith gates, and the Imperial Expedition as separate design problems.",
        ],
    }


def _native_pressure_spread(kingdoms: Sequence[Mapping[str, Any]], context: str) -> dict[str, Any]:
    target_ratio = float(NATIVE_KINGDOM_MAX_PRESSURE_SPREAD[context])
    values = [
        (str(kingdom["kingdom"]["name"]), float(kingdom["reinforcement_contexts"][context]["static_pressure_proxy"]))
        for kingdom in kingdoms
        if kingdom["reinforcement_contexts"][context]["status"] == "present"
    ]
    if len(values) != len(NATIVE_KINGDOMS):
        return {
            "status": "missing_kingdom_profiles",
            "target_max_ratio": target_ratio,
            "within_target": False,
            "values": [],
        }
    lowest_name, lowest = min(values, key=lambda row: (row[1], row[0].casefold()))
    highest_name, highest = max(values, key=lambda row: (row[1], row[0].casefold()))
    ratio = highest / lowest if lowest else 0.0
    return {
        "status": "present",
        "target_max_ratio": target_ratio,
        "within_target": ratio <= target_ratio,
        "lowest": {"kingdom": lowest_name, "static_pressure_proxy": _display_expected(lowest)},
        "highest": {"kingdom": highest_name, "static_pressure_proxy": _display_expected(highest)},
        "ratio": round(ratio, 3),
        "values": [
            {"kingdom": name, "static_pressure_proxy": _display_expected(value)}
            for name, value in sorted(values, key=lambda row: (row[1], row[0].casefold()))
        ],
    }


def _native_upgrade_row(index: BalanceIndex, edge: UpgradeEdge, kingdom: Mapping[str, str]) -> dict[str, Any] | None:
    source = index.troop_by_code.get(edge.source)
    target = index.troop_by_code.get(edge.target)
    if source is None or target is None:
        return None
    source_kit = _kit_score(index, source)
    target_kit = _kit_score(index, target)
    source_rank = _troop_rank(index, source)
    target_rank = _troop_rank(index, target)
    source_attributes = _decode_attributes(source.data[8])
    target_attributes = _decode_attributes(target.data[8])
    source_skills = _decode_skills(source.data[10])
    target_skills = _decode_skills(target.data[10])
    source_combat_skills = sum(source_skills[name] for name in COMBAT_SKILL_NAMES)
    target_combat_skills = sum(target_skills[name] for name in COMBAT_SKILL_NAMES)
    source_proficiency_total = sum(_decode_proficiencies(source.data[9]).values())
    target_proficiency_total = sum(_decode_proficiencies(target.data[9]).values())
    target_contract_issues = sorted(set(target_kit["notes"]) & HARD_LOADOUT_NOTES, key=str.casefold)
    deltas = {
        "level": target_attributes["level"] - source_attributes["level"],
        "kit_score": target_kit["kit_score"] - source_kit["kit_score"],
        "combat_skill_total": target_combat_skills - source_combat_skills,
        "proficiency_total": target_proficiency_total - source_proficiency_total,
    }
    training_advantages = [
        label
        for label, value in (
            ("kit", deltas["kit_score"]),
            ("combat_skills", deltas["combat_skill_total"]),
            ("proficiencies", deltas["proficiency_total"]),
        )
        if value > 0
    ]
    rank_order_preserved = target_rank["order"] >= source_rank["order"]
    static_status = "advances"
    if deltas["level"] <= 0 or not rank_order_preserved or not training_advantages or target_contract_issues:
        static_status = "needs_review"
    return {
        "source_id": f"trp_{source.code}",
        "target_id": f"trp_{target.code}",
        "kingdom": {"id": kingdom["id"], "name": kingdom["name"], "faction": kingdom["faction"]},
        "declaration": edge.declaration,
        "source": {
            "level": source_attributes["level"],
            "rank": source_rank["group"],
            "role": source_kit["role"],
            "kit_score": source_kit["kit_score"],
            "combat_skill_total": source_combat_skills,
            "proficiency_total": source_proficiency_total,
        },
        "target": {
            "level": target_attributes["level"],
            "rank": target_rank["group"],
            "role": target_kit["role"],
            "kit_score": target_kit["kit_score"],
            "combat_skill_total": target_combat_skills,
            "proficiency_total": target_proficiency_total,
        },
        "delta": deltas,
        "rank_order_preserved": rank_order_preserved,
        "training_advantage_signals": training_advantages,
        "target_loadout_contract_issues": target_contract_issues,
        "progression_class": "training_compensated_kit_trade" if deltas["kit_score"] < 0 else "kit_and_training_upgrade",
        "static_status": static_status,
        "source_location": {"path": project_relative(edge.path, index.root), "line": edge.line},
    }


def balance_native_kingdoms(index: BalanceIndex) -> dict[str, Any]:
    """Profile Native campaign peers without converting doctrine into a flat average."""

    bindings = _native_template_bindings(index)
    templates = {template.code: template for template in index.party_templates}
    kingdom_rows: list[dict[str, Any]] = []
    missing_template_ids: list[str] = []
    routes: list[dict[str, Any]] = []
    for kingdom in NATIVE_KINGDOMS:
        binding = bindings["kingdoms"].get(kingdom["id"])
        template_profiles: dict[str, dict[str, Any]] = {}
        for slot in ("a", "b", "c"):
            template_code = None if binding is None else binding["template_codes"].get(slot)
            template = None if template_code is None else templates.get(template_code)
            if template is None:
                if template_code is not None:
                    missing_template_ids.append(f"pt_{template_code}")
                template_profiles[slot] = {
                    "template_id": None if template_code is None else f"pt_{template_code}",
                    "status": "missing_binding" if template_code is None else "missing_template",
                    "member_total": {"minimum": 0, "maximum": 0, "expected": 0},
                    "static_stack_weighted_evidence": {"average_kit_score": 0},
                    "stacks": [],
                    "missing_troop_ids": [],
                }
                continue
            profile = _party_template_profile(index, template)
            profile["status"] = "present" if not profile["missing_troop_ids"] else "needs_review"
            template_profiles[slot] = profile
        kingdom_routes: list[dict[str, Any]] = []
        prefix = kingdom["troop_prefix"]
        for edge in index.upgrades:
            if not edge.source.startswith(prefix) or not edge.target.startswith(prefix):
                continue
            route = _native_upgrade_row(index, edge, kingdom)
            if route is not None:
                kingdom_routes.append(route)
        kingdom_routes.sort(key=lambda route: (str(route["source_id"]).casefold(), str(route["target_id"]).casefold()))
        routes.extend(kingdom_routes)
        kingdom_rows.append(
            {
                "kingdom": {"id": kingdom["id"], "name": kingdom["name"], "faction": kingdom["faction"], "culture": kingdom["culture"]},
                "cohort": dict(CAMPAIGN_COHORTS[kingdom["cohort_id"]]),
                "doctrine": kingdom["doctrine"],
                "runtime_binding": binding,
                "templates": template_profiles,
                "reinforcement_contexts": {
                    context: _template_mix_pressure(template_profiles, selections)
                    for context, selections in NATIVE_REINFORCEMENT_CONTEXTS.items()
                },
                "progression": {
                    "route_count": len(kingdom_routes),
                    "kit_trade_count": sum(route["progression_class"] == "training_compensated_kit_trade" for route in kingdom_routes),
                    "review_route_count": sum(route["static_status"] != "advances" for route in kingdom_routes),
                    "routes": kingdom_routes,
                },
            }
        )
    routes.sort(key=lambda route: (str(route["kingdom"]["name"]).casefold(), str(route["source_id"]).casefold(), str(route["target_id"]).casefold()))
    source_contracts = [
        _source_contract_row(
            index,
            "native_culture_template_binding",
            IMPERIAL_GAME_START_SOURCE_RELATIVE,
            "Each Native culture binds its campaign faction to three A/B/C reinforcement templates during initialization.",
            tuple(kingdom["culture_constant"] for kingdom in NATIVE_KINGDOMS)
            + tuple(f"pt_{kingdom['id']}_reinforcements_{slot}" for kingdom in NATIVE_KINGDOMS for slot in ("a", "b", "c")),
        ),
        _source_contract_row(
            index,
            "reinforcement_context_selection",
            PARTY_REINFORCEMENT_SOURCE_RELATIVE,
            "Towns and castles select A 65% / B 35%; kingdom hero parties select A 50% / B 25% / C 25%.",
            ('(lt, ":rand", 65)', '(lt, ":rand", 50)', '(lt, ":rand", 75)', "slot_faction_reinforcements_a", "slot_faction_reinforcements_b", "slot_faction_reinforcements_c"),
        ),
    ]
    pressure_spreads = {
        context: _native_pressure_spread(kingdom_rows, context)
        for context in NATIVE_REINFORCEMENT_CONTEXTS
    }
    review_signals: list[dict[str, Any]] = []
    for context, spread in pressure_spreads.items():
        if spread["status"] != "present" or spread["within_target"]:
            continue
        review_signals.append(
            {
                "code": "NATIVE_REINFORCEMENT_PRESSURE_SPREAD",
                "context": context,
                "message": "Static Native reinforcement pressure exceeds the doctrine-preserving campaign review target.",
                "evidence": spread,
            }
        )
    for route in routes:
        if route["static_status"] == "advances":
            continue
        review_signals.append(
            {
                "code": "NATIVE_UPGRADE_STATIC_CONTRACT",
                "message": "A Native direct upgrade does not clearly advance level/training, drops rank, or has a hard target loadout failure.",
                "route": route,
            }
        )
    source_contracts_present = bindings["status"] == "present" and all(contract["status"] == "present" for contract in source_contracts)
    profiles_present = all(
        profile["status"] == "present"
        for kingdom in kingdom_rows
        for profile in kingdom["templates"].values()
    )
    progression_present = all(kingdom["progression"]["route_count"] > 0 for kingdom in kingdom_rows)
    state = "within_static_balance_targets"
    if not source_contracts_present or not profiles_present or not progression_present:
        state = "needs_source_review"
    elif review_signals:
        state = "needs_static_rebalance"
    return {
        "mode": "native_kingdom_profile",
        "state": state,
        "kingdom_count": len(kingdom_rows),
        "progression_route_count": len(routes),
        "kingdoms": kingdom_rows,
        "pressure_spreads": pressure_spreads,
        "missing_template_ids": sorted(set(missing_template_ids), key=str.casefold),
        "source_contracts": source_contracts,
        "review_signals": review_signals,
        "source_authority": {
            "party_templates": project_relative(index.party_templates_path, index.root),
            "campaign_initializer": project_relative(index.root / IMPERIAL_GAME_START_SOURCE_RELATIVE, index.root),
            "reinforcement_selection": project_relative(index.root / PARTY_REINFORCEMENT_SOURCE_RELATIVE, index.root),
            "troops": project_relative(index.troops_path, index.root),
        },
        "warnings": [
            "The Native kingdoms coexist and can be compared as a campaign group, but their infantry, ranged, cavalry, and mobility doctrines remain constraints rather than normalization targets.",
            "A negative static kit delta is preserved as a visible training-compensated role trade when level and training still advance. It is not an automatic instruction to equalize branch equipment.",
            "Static reinforcement pressure is expected stack size multiplied by stack-weighted kit score. It cannot establish map speed, reinforcement timing, wages, casualty replacement, battle AI, siege performance, or live economic results.",
        ],
    }


def balance_mercenary_guilds(index: BalanceIndex) -> dict[str, Any]:
    """Audit mercenary doctrine as contract specialization, not territorial symmetry."""

    source_contracts = [
        _source_contract_row(
            index,
            "guild_role_fit_authority",
            MERCENARY_ROLE_FIT_SOURCE_RELATIVE,
            "Every guild has an explicit job-fit branch, including negative civic-service fit for the Slavers and Boar Clan.",
            tuple(f'"fac_{guild["faction"]}"' for guild in MERCENARY_GUILDS)
            + ("sod_merc_contract_role_garrison_support", "sod_merc_contract_role_supply_column"),
        ),
        _source_contract_row(
            index,
            "contract_roster_authority",
            MERCENARY_CONTRACT_ROSTER_SOURCE_RELATIVE,
            "AI contract formation starts from the public guild roster and changes only base-line composition for the assigned job.",
            (
                "script_sod_merc_guild_get_roster",
                "black_army_tier_1_unit_3",
                "sod_merc_contract_role_patrol",
                "sod_merc_contract_role_garrison_support",
                "sod_merc_contract_role_supply_column",
            ),
        ),
        _source_contract_row(
            index,
            "role_aware_preferred_guild",
            MERCENARY_SELECTION_SOURCE_RELATIVE,
            "Preferred-guild selection passes the employer's demand type into guild weighting.",
            ("script_sod_merc_market_calculate_kingdom_guild_weight", ":demand_type"),
        ),
        _source_contract_row(
            index,
            "bid_role_score_once",
            MERCENARY_BID_SOURCE_RELATIVE,
            "Bid scoring uses the shared role fit once and keeps relationship weighting role-neutral to avoid double counting doctrine.",
            ("script_sod_merc_market_calculate_guild_role_fit", "sod_merc_contract_role_none", ":role_fit_score"),
        ),
        _source_contract_row(
            index,
            "accepted_bid_propagates_role",
            MERCENARY_ACCEPT_SOURCE_RELATIVE,
            "The accepted contract resolves its deployable role before passing it into AI company formation.",
            ("script_sod_merc_market_resolve_ai_contract_role", ":effective_demand_type", "script_cf_spawn_ai_mercs"),
        ),
        _source_contract_row(
            index,
            "deployment_role_resolution",
            MERCENARY_DEPLOY_SOURCE_RELATIVE,
            "Formation and later deployment share one resolver, so a live role cannot silently diverge from a job-shaped AI roster.",
            (
                "script_sod_merc_market_resolve_ai_contract_role",
                "sod_merc_contract_role_escort",
                "sod_merc_contract_role_mercenary_lord",
                "sod_merc_contract_role_special_world_activity",
            ),
        ),
        _source_contract_row(
            index,
            "ai_company_contract_roster",
            MERCENARY_SPAWN_SOURCE_RELATIVE,
            "AI spawning resolves the contract roster before world spawn and swaps specialists from an existing base line, preserving party size.",
            ("script_sod_merc_guild_get_contract_roster", ":demand_type", ":specialist_units", "val_sub, \":t1_2_units\", \":specialist_units\""),
        ),
        _source_contract_row(
            index,
            "contract_dialogue_identity",
            MERCENARY_DIALOGUE_SOURCE_RELATIVE,
            "Contract dialogue names the guild specialist and the company job from live party state.",
            tuple(f'"fac_{guild["faction"]}"' for guild in MERCENARY_GUILDS)
            + ("slot_party_sod_merc_contract_role", "slot_party_sod_merc_contract_guild", "{s72}"),
        ),
    ]
    guild_rows: list[dict[str, Any]] = []
    missing_troop_ids: list[str] = []
    for guild in MERCENARY_GUILDS:
        faction = str(guild["faction"])
        roster_codes = tuple(guild["base_troops"]) + (str(guild["noble_troop"]),)
        roster_rows: list[dict[str, Any]] = []
        external_roster_members: list[str] = []
        for code in roster_codes:
            troop = index.troop_by_code.get(code)
            if troop is None:
                missing_troop_ids.append(f"trp_{code}")
                roster_rows.append({"troop_id": f"trp_{code}", "status": "missing_from_evaluated_troops"})
                continue
            row = _troop_overview(index, troop)
            roster_rows.append(
                {
                    "troop_id": row["troop_id"],
                    "name": row["name"],
                    "level": row["level"],
                    "rank": row["rank"]["group"],
                    "role": row["role"],
                    "kit_score": row["kit_score"],
                    "faction": row["faction"],
                }
            )
            if row["faction"] != faction:
                external_roster_members.append(row["troop_id"])
        guild_records = [
            troop
            for troop in index.troops
            if index.faction_by_index.get(int(troop.data[6]) if isinstance(troop.data[6], int) else -1) == faction
        ]
        guild_codes = {troop.code for troop in guild_records} | set(roster_codes)
        direct_routes = [
            {"source_id": f"trp_{edge.source}", "target_id": f"trp_{edge.target}"}
            for edge in index.upgrades
            if edge.source in guild_codes and edge.target in guild_codes
        ]
        direct_routes.sort(key=lambda row: (str(row["source_id"]).casefold(), str(row["target_id"]).casefold()))
        guild_rows.append(
            {
                "guild": {"id": guild["id"], "name": guild["name"], "faction": f"fac_{faction}"},
                "doctrine": guild["doctrine"],
                "contract_niche": {
                    "primary_roles": [
                        {"id": role, "label": MERCENARY_ROLE_LABELS[role]}
                        for role in guild["primary_roles"]
                    ],
                    "deprioritized_roles": [
                        {"id": role, "label": MERCENARY_ROLE_LABELS[role]}
                        for role in guild["deprioritized_roles"]
                    ],
                },
                "runtime_roster": {
                    "base_and_noble": roster_rows,
                    "guild_faction_troop_count": len(guild_records),
                    "external_roster_members": external_roster_members,
                    "direct_upgrade_count": len(direct_routes),
                    "direct_upgrades": direct_routes,
                },
            }
        )
    source_contracts_present = all(contract["status"] == "present" for contract in source_contracts)
    roster_present = not missing_troop_ids and len(guild_rows) == len(MERCENARY_GUILDS)
    state = "within_static_niche_targets" if source_contracts_present and roster_present else "needs_source_review"
    return {
        "mode": "mercenary_guild_profile",
        "state": state,
        "guild_count": len(guild_rows),
        "guilds": guild_rows,
        "missing_troop_ids": sorted(set(missing_troop_ids), key=str.casefold),
        "source_contracts": source_contracts,
        "source_authority": {
            "troops": project_relative(index.troops_path, index.root),
            "role_fit": project_relative(index.root / MERCENARY_ROLE_FIT_SOURCE_RELATIVE, index.root),
            "contract_roster": project_relative(index.root / MERCENARY_CONTRACT_ROSTER_SOURCE_RELATIVE, index.root),
            "bid": project_relative(index.root / MERCENARY_BID_SOURCE_RELATIVE, index.root),
            "deployment": project_relative(index.root / MERCENARY_DEPLOY_SOURCE_RELATIVE, index.root),
            "company_spawn": project_relative(index.root / MERCENARY_SPAWN_SOURCE_RELATIVE, index.root),
        },
        "warnings": [
            "This profile checks that a job-aware contract path and themed base roster exist. It does not simulate randomized equipment, player formations, map speed, battle AI, wages, casualties, prisoner capture, or the final upgraded composition of a live party.",
            "Player-facing hire menus retain their selected mix. Job-aware composition is applied only to AI contracts, so a player is never silently assigned an AI fallback role.",
            "Mercenary guilds are intentionally asymmetric service providers. A lower fit for civic garrison or relief work is a role boundary, not a claim that the faction's troops are universally weaker.",
        ],
    }


def balance_compare(index: BalanceIndex, entity_ids: Sequence[str]) -> dict[str, Any]:
    if not isinstance(entity_ids, Sequence) or isinstance(entity_ids, (str, bytes)):
        raise BalanceError("entity_ids must be an array of two through eight item/troop IDs.")
    if not 2 <= len(entity_ids) <= 8:
        raise BalanceError("entity_ids must contain two through eight values.")
    items: list[dict[str, Any]] = []
    troops: list[dict[str, Any]] = []
    for value in entity_ids:
        raw = require_string(value, name="entity_ids entry", maximum=180)
        if raw.startswith("item:") or raw.startswith("itm_") or raw in index.item_by_code:
            code = normalize_item_code(raw)
            record = _lookup_item(index, code)
            if record is None:
                raise BalanceError(f"Unknown item: itm_{code}.")
            items.append({**_item_overview(index, record), "stats": _item_stats(record)})
        else:
            code = normalize_troop_code(raw)
            record = _lookup_troop(index, code)
            if record is None:
                raise BalanceError(f"Unknown troop: trp_{code}.")
            troops.append({**_troop_overview(index, record), "attributes": _decode_attributes(record.data[8]), "proficiencies": _decode_proficiencies(record.data[9]), "kit_analysis": _kit_score(index, record)})
    if len(items) > 1:
        baseline = int(items[0]["combat_score"])
        for row in items:
            row["combat_score_delta_from_first"] = int(row["combat_score"]) - baseline
    if len(troops) > 1:
        baseline = int(troops[0]["kit_score"])
        for row in troops:
            row["kit_score_delta_from_first"] = int(row["kit_score"]) - baseline
    return {
        "item_comparison": items,
        "troop_comparison": troops,
        "warnings": ["Comparison normalizes current evaluated values and static score heuristics only; it does not prove battlefield outcome parity."]
    }


def _percentile(values: Sequence[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    low = int(position)
    high = min(len(ordered) - 1, low + 1)
    weight = position - low
    return ordered[low] * (1 - weight) + ordered[high] * weight


def _item_outliers(index: BalanceIndex) -> list[dict[str, Any]]:
    rows = [_item_overview(index, item) for item in index.items]
    groups: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["combat_score"] > 0 and row["price"] > 0:
            groups[int(row["type_id"])].append(row)
    median_ratio = {
        group: median([float(row["price_per_score"]) for row in values if row["price_per_score"] is not None])
        for group, values in groups.items()
        if len(values) >= 5
    }
    p90 = {group: _percentile([float(row["combat_score"]) for row in values], 0.90) for group, values in groups.items() if values}
    findings: list[dict[str, Any]] = []
    for row in rows:
        score = int(row["combat_score"])
        price = int(row["price"])
        group = int(row["type_id"])
        ratio = row["price_per_score"]
        if score >= 40 and price <= 1:
            findings.append({"severity": "high", "code": "POWER_NEAR_FREE", "entity_id": row["entity_id"], "message": "Strong score with near-zero price.", "evidence": row})
        baseline = median_ratio.get(group)
        if baseline and ratio is not None and score >= 10:
            if float(ratio) < baseline * 0.35:
                findings.append({"severity": "warning", "code": "CHEAP_FOR_TYPE", "entity_id": row["entity_id"], "message": "Price-per-score is far below its item-type median.", "evidence": {**row, "type_median_price_per_score": round(baseline, 2)}})
            elif float(ratio) > baseline * 3.0:
                findings.append({"severity": "warning", "code": "EXPENSIVE_FOR_TYPE", "entity_id": row["entity_id"], "message": "Price-per-score is far above its item-type median.", "evidence": {**row, "type_median_price_per_score": round(baseline, 2)}})
        if bool(row["merchandise"]) and score >= p90.get(group, float("inf")) and score >= 40:
            findings.append({"severity": "info", "code": "TOP_SHOP_POWER", "entity_id": row["entity_id"], "message": "Top-decile score in a shop-available item type.", "evidence": row})
        if score >= 55 and int(row["all_user_count"]) == 0 and not bool(row["unique"]):
            findings.append({"severity": "info", "code": "UNUSED_HIGH_POWER", "entity_id": row["entity_id"], "message": "High-score item has no evaluated troop inventory users.", "evidence": row})
    return findings


def _troop_outliers(index: BalanceIndex, *, include_heroes: bool) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    outgoing, _incoming = _upgrade_maps(index)
    for record in index.troops:
        overview = _troop_overview(index, record)
        if overview["hero"] and not include_heroes:
            continue
        kit = _kit_score(index, record)
        if kit["status"] in {"under_equipped", "over_equipped"}:
            findings.append({
                "severity": "warning",
                "code": kit["status"].upper(),
                "entity_id": overview["entity_id"],
                "message": "Kit score sits outside its role-adjusted static band.",
                "evidence": {**overview, "kit_analysis": kit},
            })
        for note in kit["notes"]:
            if note in {"shield_guaranteed_but_no_shield_in_inventory", "mounted_role_without_mount_item", "no_weapon_item"}:
                findings.append({"severity": "high", "code": note.upper(), "entity_id": overview["entity_id"], "message": note.replace("_", " ") + ".", "evidence": {**overview, "kit_analysis": kit}})
        for target in outgoing.get(record.code, []):
            target_record = index.troop_by_code.get(target)
            if target_record is None:
                findings.append({"severity": "high", "code": "UPGRADE_TARGET_MISSING", "entity_id": overview["entity_id"], "message": f"Explicit upgrade target trp_{target} is absent from evaluated troops.", "evidence": overview})
                continue
            source_level = int(_decode_attributes(record.data[8])["level"])
            target_level = int(_decode_attributes(target_record.data[8])["level"])
            if target_level <= source_level:
                findings.append({"severity": "warning", "code": "NON_ASCENDING_UPGRADE_LEVEL", "entity_id": overview["entity_id"], "message": f"Upgrade target trp_{target} has level {target_level}, not above source level {source_level}.", "evidence": overview})
    return findings


def balance_outliers(
    index: BalanceIndex,
    *,
    domain: str = "all",
    include_heroes: bool = False,
    limit: int = 100,
) -> dict[str, Any]:
    checked_domain = require_string(domain, name="domain", maximum=20).casefold()
    if checked_domain not in {"all", "items", "troops"}:
        raise BalanceError("domain must be 'all', 'items', or 'troops'.")
    if not isinstance(include_heroes, bool):
        raise BalanceError("include_heroes must be true or false.")
    checked_limit = require_limit(limit)
    findings: list[dict[str, Any]] = []
    if checked_domain in {"all", "items"}:
        findings.extend(_item_outliers(index))
    if checked_domain in {"all", "troops"}:
        findings.extend(_troop_outliers(index, include_heroes=include_heroes))
    rank = {"high": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda row: (rank.get(str(row["severity"]), 3), str(row["code"]), str(row["entity_id"])))
    return {
        "finding_count": len(findings),
        "returned_count": min(len(findings), checked_limit),
        "findings": findings[:checked_limit],
        "filters": {"domain": checked_domain, "include_heroes": include_heroes},
        "model": {
            "item_score": "type-aware static combat/equipment heuristic",
            "troop_kit_score": "best melee + ranged weapon + ammo + top four armor + best shield + best mount",
            "band": "role-adjusted upgrade/level tier band",
        },
        "warnings": [
            "Outliers are ranking and review candidates. They are not compile errors, runtime combat proofs, or automatic balance prescriptions.",
            "Troop inventories are random-choice pools; a troop may not spawn with every listed item at once.",
        ],
    }


def _offset_for_position(source: str, line: int, column_bytes: int) -> int:
    lines = source.splitlines(keepends=True)
    if line < 1 or line > len(lines):
        raise BalanceError("Source AST position was outside its source file.")
    prefix = sum(len(value) for value in lines[: line - 1])
    encoded = lines[line - 1].encode("utf-8")
    try:
        partial = encoded[:column_bytes].decode("utf-8")
    except UnicodeDecodeError as error:
        raise BalanceError("Source AST column split a UTF-8 character.") from error
    return prefix + len(partial)


def _node_range(source: str, node: ast.AST) -> tuple[int, int]:
    if not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
        raise BalanceError("Source node has no position information.")
    return (
        _offset_for_position(source, int(node.lineno), int(node.col_offset)),
        _offset_for_position(source, int(node.end_lineno), int(node.end_col_offset)),
    )


def _replacement_for_node(source: str, node: ast.AST, after: str, label: str) -> Replacement:
    start, end = _node_range(source, node)
    return Replacement(start=start, end=end, before=source[start:end], after=after, label=label)


def _apply_replacements(source: str, replacements: Sequence[Replacement]) -> str:
    if not replacements:
        raise BalanceError("The requested balance patch would make no source change.")
    ordered = sorted(replacements, key=lambda replacement: (replacement.start, replacement.end))
    previous = -1
    for replacement in ordered:
        if replacement.start < previous:
            raise BalanceError("Balance patch contains overlapping source replacements.")
        if replacement.start > replacement.end or source[replacement.start : replacement.end] != replacement.before:
            raise BalanceError("Balance patch source anchor is stale; rebuild the plan.")
        previous = replacement.end
    result = source
    for replacement in reversed(ordered):
        result = result[: replacement.start] + replacement.after + result[replacement.end :]
    return result


def _literal_string(value: Any, *, name: str) -> str:
    text = require_string(value, name=name, maximum=4_000)
    return json.dumps(text, ensure_ascii=False)


def _field_node(source: SourceRecord, index: int, label: str) -> ast.AST:
    if index >= len(source.node.elts):
        raise BalanceError(f"Direct {source.kind} record {source.code!r} has no {label} field.")
    return source.node.elts[index]


def _stat_calls(node: ast.AST) -> dict[str, list[ast.Call]]:
    result: dict[str, list[ast.Call]] = defaultdict(list)
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id in set(STAT_ALIASES.values()):
            result[child.func.id].append(child)
    return result


def _number_literal(value: int | float) -> str:
    if isinstance(value, float):
        return format(value, ".12g")
    return str(value)


def _item_replacements(index: BalanceIndex, record: ItemRecord, source: SourceRecord, changes: Mapping[str, Any]) -> tuple[list[Replacement], list[str]]:
    unknown = sorted(set(changes) - {"name", "price", "stats"})
    if unknown:
        raise BalanceError("Unsupported item balance change(s): " + ", ".join(unknown) + ".")
    replacements: list[Replacement] = []
    notes: list[str] = []
    if "name" in changes:
        replacements.append(_replacement_for_node(source.source_text, _field_node(source, 1, "name"), _literal_string(changes["name"], name="changes.name"), "item name"))
    if "price" in changes:
        price = require_int(changes["price"], name="changes.price", minimum=0, maximum=100_000_000)
        replacements.append(_replacement_for_node(source.source_text, _field_node(source, 5, "price"), str(price), "item price"))
    if "stats" in changes:
        requested = require_mapping(changes["stats"], name="changes.stats")
        if not requested:
            raise BalanceError("changes.stats must not be empty.")
        stat_node = _field_node(source, 6, "stats")
        available = _stat_calls(stat_node)
        seen: set[str] = set()
        for name, requested_value in requested.items():
            if not isinstance(name, str):
                raise BalanceError("changes.stats keys must be strings.")
            canonical = STAT_ALIASES.get(name.casefold())
            if canonical is None:
                raise BalanceError("Unsupported item stat " + repr(name) + ". Use: " + ", ".join(sorted(STAT_ALIASES)) + ".")
            if canonical in seen:
                raise BalanceError(f"Stat {canonical!r} was requested more than once through aliases.")
            seen.add(canonical)
            calls = available.get(canonical, [])
            if len(calls) != 1:
                if not calls:
                    raise BalanceError(f"itm_{record.code} has no direct {canonical}(...) constructor to edit. Inspect editable_stat_calls before proposing this patch.")
                raise BalanceError(f"itm_{record.code} has multiple {canonical}(...) constructors, so an automatic balance patch would be ambiguous.")
            call = calls[0]
            if not call.args:
                raise BalanceError(f"itm_{record.code}'s {canonical}(...) call has no value argument.")
            if canonical == "weight":
                value = require_number(requested_value, name=f"changes.stats.{name}", minimum=0.0, maximum=63.75)
            elif canonical in DAMAGE_STAT_FUNCTIONS:
                damage = require_mapping(requested_value, name=f"changes.stats.{name}")
                unknown_damage = sorted(set(damage) - {"value", "damage_type"})
                if unknown_damage:
                    raise BalanceError("Unknown damage change key(s): " + ", ".join(unknown_damage) + ".")
                value = require_int(damage.get("value"), name=f"changes.stats.{name}.value", minimum=0, maximum=255)
                if "damage_type" in damage:
                    damage_type = require_string(damage["damage_type"], name=f"changes.stats.{name}.damage_type", maximum=20).casefold()
                    if damage_type not in DAMAGE_TYPES:
                        raise BalanceError("damage_type must be cut, pierce, or blunt.")
                    if len(call.args) < 2:
                        raise BalanceError(f"itm_{record.code}'s {canonical}(...) has no damage-type argument to edit.")
                    replacements.append(_replacement_for_node(source.source_text, call.args[1], damage_type, f"{canonical} damage type"))
            else:
                maximum = 65_535 if canonical == "hit_points" else 1_023 if canonical in {"shoot_speed", "weapon_length"} else 255
                value = require_int(requested_value, name=f"changes.stats.{name}", minimum=0, maximum=maximum)
            replacements.append(_replacement_for_node(source.source_text, call.args[0], _number_literal(value), f"{canonical} value"))
    if "stats" in changes:
        notes.append("Only existing item stat constructors are changed; the patch does not add duplicate bit-packed stat fields.")
    return replacements, notes


def _canonical_attributes(values: Mapping[str, int]) -> str:
    for name in ("str", "agi", "int", "cha"):
        if not 3 <= int(values[name]) <= 30:
            raise BalanceError(f"Cannot canonicalize attribute {name}={values[name]}; header_troops.py provides symbolic {name}_3 through {name}_30 only.")
    return "|".join((f"str_{values['str']}", f"agi_{values['agi']}", f"int_{values['int']}", f"cha_{values['cha']}", f"level({values['level']})"))


def _canonical_proficiencies(values: Mapping[str, int]) -> str:
    return "|".join(f"{PROFICIENCY_FUNCTIONS[name]}({values[name]})" for name in PROFICIENCY_BITS)


def _canonical_skills(values: Mapping[str, int]) -> str:
    terms = []
    for slot, name in SKILL_SLOTS.items():
        value = int(values[name])
        if value:
            if value > 10:
                raise BalanceError(f"Cannot canonicalize skill {name}={value}; header_skills.py symbols cover levels 1 through 10.")
            terms.append(f"knows_{name}_{value}")
    return "|".join(terms) or "0"


def _canonical_inventory(index: BalanceIndex, values: Any) -> str:
    if not isinstance(values, list):
        raise BalanceError("changes.inventory must be an array of item IDs/codes.")
    if len(values) > 64:
        raise BalanceError("changes.inventory may contain at most 64 item entries.")
    codes: list[str] = []
    for value in values:
        code = normalize_item_code(value)
        record = _lookup_item(index, code)
        if record is None:
            raise BalanceError(f"Unknown item for inventory: itm_{code}.")
        codes.append(f"itm_{record.code}")
    return "[" + ", ".join(codes) + "]"


def _troop_replacements(index: BalanceIndex, record: TroopRecord, source: SourceRecord, changes: Mapping[str, Any]) -> tuple[list[Replacement], list[str]]:
    allowed = {"name", "plural_name", "attributes", "proficiencies", "skills", "inventory"}
    unknown = sorted(set(changes) - allowed)
    if unknown:
        raise BalanceError("Unsupported troop balance change(s): " + ", ".join(unknown) + ".")
    replacements: list[Replacement] = []
    notes: list[str] = []
    if "name" in changes:
        replacements.append(_replacement_for_node(source.source_text, _field_node(source, 1, "name"), _literal_string(changes["name"], name="changes.name"), "troop name"))
    if "plural_name" in changes:
        replacements.append(_replacement_for_node(source.source_text, _field_node(source, 2, "plural name"), _literal_string(changes["plural_name"], name="changes.plural_name"), "troop plural name"))
    if "attributes" in changes:
        requested = require_mapping(changes["attributes"], name="changes.attributes")
        allowed_attributes = {"str", "agi", "int", "cha", "level"}
        unknown_attributes = sorted(set(requested) - allowed_attributes)
        if unknown_attributes:
            raise BalanceError("Unknown attribute change(s): " + ", ".join(unknown_attributes) + ".")
        if not requested:
            raise BalanceError("changes.attributes must not be empty.")
        current = _decode_attributes(record.data[8])
        values = {name: int(current[name]) for name in allowed_attributes}
        for name, value in requested.items():
            values[name] = require_int(value, name=f"changes.attributes.{name}", minimum=0 if name == "level" else 3, maximum=255 if name == "level" else 30)
        replacements.append(_replacement_for_node(source.source_text, _field_node(source, 8, "attributes"), _canonical_attributes(values), "troop attributes"))
        notes.append("Attributes are rewritten as explicit evaluated header_troops.py symbols to avoid accidental bitwise-OR carryover from helper aliases.")
    if "proficiencies" in changes:
        requested = require_mapping(changes["proficiencies"], name="changes.proficiencies")
        unknown_profs = sorted(set(requested) - set(PROFICIENCY_BITS))
        if unknown_profs:
            raise BalanceError("Unknown proficiency change(s): " + ", ".join(unknown_profs) + ".")
        if not requested:
            raise BalanceError("changes.proficiencies must not be empty.")
        values = _decode_proficiencies(record.data[9])
        for name, value in requested.items():
            values[name] = require_int(value, name=f"changes.proficiencies.{name}", minimum=0, maximum=1023)
        replacements.append(_replacement_for_node(source.source_text, _field_node(source, 9, "weapon proficiencies"), _canonical_proficiencies(values), "troop proficiencies"))
        notes.append("Proficiency helper expressions are canonicalized to their current evaluated per-weapon values, then the requested values are changed.")
    if "skills" in changes:
        requested = require_mapping(changes["skills"], name="changes.skills")
        unknown_skills = sorted(set(requested) - set(SKILL_NAME_TO_SLOT))
        if unknown_skills:
            raise BalanceError("Unknown skill change(s): " + ", ".join(unknown_skills) + ".")
        if not requested:
            raise BalanceError("changes.skills must not be empty.")
        values = _decode_skills(record.data[10])
        for name, value in requested.items():
            values[name] = require_int(value, name=f"changes.skills.{name}", minimum=0, maximum=10)
        replacements.append(_replacement_for_node(source.source_text, _field_node(source, 10, "skills"), _canonical_skills(values), "troop skills"))
        notes.append("Skill helper expressions are canonicalized to explicit current evaluated skill symbols before the requested balance changes are made.")
    if "inventory" in changes:
        replacements.append(_replacement_for_node(source.source_text, _field_node(source, 7, "inventory"), _canonical_inventory(index, changes["inventory"]), "troop inventory"))
        notes.append("Inventory is rewritten as a direct ordered item-code list. This preserves evaluated entries but intentionally removes local inventory formatting/helper comments inside that field.")
    return replacements, notes


def _deduplicate_replacements(replacements: Iterable[Replacement]) -> list[Replacement]:
    result: dict[tuple[int, int], Replacement] = {}
    for replacement in replacements:
        key = (replacement.start, replacement.end)
        existing = result.get(key)
        if existing is not None and existing.after != replacement.after:
            raise BalanceError(f"Two requested semantic changes conflict at {replacement.label}.")
        result[key] = replacement
    return list(result.values())


def balance_patch(index: BalanceIndex, entity_kind: str, entity_id: str, *, changes: Mapping[str, Any]) -> dict[str, Any]:
    kind = normalize_entity_kind(entity_kind)
    code = normalize_entity_code(kind, entity_id)
    checked_changes = require_mapping(changes, name="changes")
    if not checked_changes:
        raise BalanceError("changes must not be empty.")
    record: ItemRecord | TroopRecord
    if kind == "item":
        record = _lookup_item(index, code)  # type: ignore[assignment]
    else:
        record = _lookup_troop(index, code)  # type: ignore[assignment]
    if record is None:
        raise BalanceError(f"Unknown {kind}: {code}.")
    code = record.code
    source = index.source_records.get((kind, code))
    if source is None:
        origin = record.origin if isinstance(record, TroopRecord) else "runtime_generated"
        raise BalanceError(f"{kind} {code!r} is {origin} and has no direct editable legacy source record.")
    if kind == "item":
        replacements, notes = _item_replacements(index, record, source, checked_changes)  # type: ignore[arg-type]
    else:
        replacements, notes = _troop_replacements(index, record, source, checked_changes)  # type: ignore[arg-type]
    replacements = _deduplicate_replacements(replacements)
    after = _apply_replacements(source.source_text, replacements)
    if after == source.source_text:
        raise BalanceError("The requested balance patch makes no effective source change.")
    path = source.path
    before_raw = path.read_bytes()
    base_sha = sha256_bytes(before_raw)
    if before_raw.decode("utf-8") != source.source_text:
        raise BalanceError("Source changed while the balance index was being built; rebuild the plan.")
    relative = project_relative(path, index.root)
    diff_lines = list(
        difflib.unified_diff(
            source.source_text.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=relative,
            tofile=relative,
            n=3,
        )
    )
    truncated = len(diff_lines) > MAX_DIFF_LINES
    diff = "".join(diff_lines[:MAX_DIFF_LINES])
    if truncated:
        diff += f"\n... Balance Lab diff truncated after {MAX_DIFF_LINES} lines.\n"
    protected = (HARDWIRED_ITEMS.get(code) == record.index) if kind == "item" else (HARDWIRED_TROOPS.get(code) == record.index)
    plan_identity = {
        "version": BALANCE_VERSION,
        "kind": kind,
        "code": code,
        "path": relative,
        "base_sha256": base_sha,
        "after_sha256": sha256_text(after),
        "changes": checked_changes,
        "replacements": [{"label": replacement.label, "start": replacement.start, "end": replacement.end, "after": replacement.after} for replacement in sorted(replacements, key=lambda item: item.start)],
    }
    plan_sha = sha256_text(json.dumps(plan_identity, sort_keys=True, ensure_ascii=False, separators=(",", ":")))
    warnings = [
        "This is a legacy compile-authoring patch plan, not a generated/export write. Review its diff before even a dry-run rehearsal.",
        "A non-dry apply requires current file SHA, current plan SHA, and allow_legacy_compile_authoring=true. It never changes ID tables, ordering, or exports.",
        *notes,
    ]
    if protected:
        warnings.append("This record is engine/legacy hardwired. Non-dry apply additionally requires allow_protected_legacy_record_change=true.")
    if not index.source_authority["confirmed"]:
        warnings.append("Build-route authority is not confirmed; non-dry apply is blocked.")
    return {
        "plan_kind": "legacy_compile_balance_patch",
        "entity": _item_overview(index, record) if kind == "item" else _troop_overview(index, record),
        "target": {"path": relative, "base_sha256": base_sha, "after_sha256": sha256_text(after), "source_authority": index.source_authority},
        "plan_sha256": plan_sha,
        "replacements": [
            {"label": replacement.label, "before": replacement.before, "after": replacement.after}
            for replacement in sorted(replacements, key=lambda item: item.start)
        ],
        "unified_diff": diff,
        "diff_truncated": truncated,
        "apply_contract": {
            "dry_run_default": True,
            "expected_sha256": base_sha,
            "expected_plan_sha256": plan_sha,
            "allow_legacy_compile_authoring_required_for_non_dry": True,
            "allow_protected_legacy_record_change_required_for_non_dry": protected,
            "writes": [relative],
            "never_writes": ["compile/ids/*", "_export/*", "*.txt exports", "src/**/_order*.txt"],
        },
        "warnings": warnings,
    }


def _atomic_write_utf8(path: Path, content: str) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except OSError as error:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise BalanceError(f"Could not atomically write guarded legacy authoring change: {error}") from error


def balance_apply(
    index: BalanceIndex,
    entity_kind: str,
    entity_id: str,
    *,
    changes: Mapping[str, Any],
    expected_sha256: str,
    expected_plan_sha256: str,
    dry_run: bool = True,
    allow_legacy_compile_authoring: bool = False,
    allow_protected_legacy_record_change: bool = False,
) -> dict[str, Any]:
    if not isinstance(dry_run, bool):
        raise BalanceError("dry_run must be true or false.")
    if not isinstance(allow_legacy_compile_authoring, bool):
        raise BalanceError("allow_legacy_compile_authoring must be true or false.")
    if not isinstance(allow_protected_legacy_record_change, bool):
        raise BalanceError("allow_protected_legacy_record_change must be true or false.")
    checked_sha = require_sha256(expected_sha256, name="expected_sha256")
    checked_plan_sha = require_sha256(expected_plan_sha256, name="expected_plan_sha256")
    fresh = build_balance_index(index.root)
    plan = balance_patch(fresh, entity_kind, entity_id, changes=changes)
    base_sha = plan["target"]["base_sha256"]
    plan_sha = plan["plan_sha256"]
    if checked_sha != base_sha:
        raise BalanceError("expected_sha256 does not match the current legacy authoring file. Rebuild and review the patch plan.")
    if checked_plan_sha != plan_sha:
        raise BalanceError("expected_plan_sha256 does not match the current semantic patch. Rebuild and review the patch plan.")
    entity = plan["entity"]
    protected = bool(entity["protected_legacy_record"])
    if not dry_run:
        if not bool(fresh.source_authority["confirmed"]):
            raise BalanceError("Legacy item/troop authoring authority is not confirmed by the current build route; non-dry apply is blocked.")
        if not allow_legacy_compile_authoring:
            raise BalanceError("Non-dry legacy compile-authoring apply requires allow_legacy_compile_authoring=true after reviewing the diff and build route.")
        if protected and not allow_protected_legacy_record_change:
            raise BalanceError("This hardwired legacy record requires allow_protected_legacy_record_change=true for a non-dry apply.")
    if not dry_run:
        path = fresh.root / str(plan["target"]["path"])
        current = _read_utf8_source(path)
        replacements: list[Replacement]
        # Reconstruct through the same plan anchors. The freshly planned unified
        # diff is not applied as text; the deterministic semantic replacements
        # are reconstructed by asking balance_patch above and using source text
        # anchors from the fresh source record.
        kind = normalize_entity_kind(entity_kind)
        code = normalize_entity_code(kind, entity_id)
        record = _lookup_item(fresh, code) if kind == "item" else _lookup_troop(fresh, code)
        if record is None:  # balance_patch above already proved this, but retain a narrow guard for direct API callers.
            raise BalanceError(f"Unknown {kind}: {code}.")
        source = fresh.source_records[(kind, record.code)]
        if kind == "item":
            replacements, _notes = _item_replacements(fresh, record, source, require_mapping(changes, name="changes"))  # type: ignore[arg-type]
        else:
            replacements, _notes = _troop_replacements(fresh, record, source, require_mapping(changes, name="changes"))  # type: ignore[arg-type]
        after = _apply_replacements(current, _deduplicate_replacements(replacements))
        _atomic_write_utf8(path, after)
        invalidate_balance_index(fresh.root)
    return {
        "applied": not dry_run,
        "dry_run": dry_run,
        "legacy_authoring_acknowledgement_used": bool(not dry_run and allow_legacy_compile_authoring),
        "protected_legacy_acknowledgement_used": bool(not dry_run and protected and allow_protected_legacy_record_change),
        "plan": plan,
        "warnings": [
            "Dry-run proves the current source SHA/semantic plan contract without writing.",
            "After a non-dry apply, run the normal reviewed build, inspect generated module/ID/export diffs, and smoke-test the intended troop/item behavior in-game.",
        ],
    }


def balance_verify(index: BalanceIndex, *, limit: int = 100) -> dict[str, Any]:
    checked_limit = require_limit(limit)
    item_contract = _id_contract(index, "item")
    troop_contract = _id_contract(index, "troop")
    issues: list[dict[str, Any]] = []
    for contract in (item_contract, troop_contract):
        if not contract["passed"]:
            issues.append({"severity": "high", "code": "ID_TABLE_PARITY", "kind": contract["kind"], "message": "Evaluated records do not match their generated ID table.", "evidence": contract})
    known_items = {item.index for item in index.items}
    for troop in index.troops:
        values = troop.data[7]
        if not isinstance(values, list):
            issues.append({"severity": "high", "code": "INVENTORY_NOT_LIST", "entity_id": f"troop:{troop.code}", "message": "Evaluated troop inventory is not a list."})
            continue
        unknown = [value for value in values if isinstance(value, int) and value not in known_items]
        if unknown:
            issues.append({"severity": "high", "code": "UNKNOWN_ITEM_INDEX", "entity_id": f"troop:{troop.code}", "message": "Troop inventory references an absent evaluated item index.", "unknown_item_indices": unknown[:10]})
    known_troops = set(index.troop_by_code)
    for edge in index.upgrades:
        if edge.source not in known_troops or edge.target not in known_troops:
            issues.append({"severity": "high", "code": "UPGRADE_REFERENCE_MISSING", "source": f"trp_{edge.source}", "target": f"trp_{edge.target}", "line": edge.line, "message": "Explicit upgrade declaration references an absent evaluated troop."})
    state = "ready_for_build_review" if not issues and bool(index.source_authority["confirmed"]) else "blocked"
    return {
        "state": state,
        "issue_count": len(issues),
        "returned_issue_count": min(len(issues), checked_limit),
        "issues": issues[:checked_limit],
        "truncated": len(issues) > checked_limit,
        "authoring": index.source_authority,
        "item_id_contract": item_contract,
        "troop_id_contract": troop_contract,
        "manual_gates": [
            "Run build_module.bat (or the existing reviewed build entry point) after a source apply.",
            "Inspect compile/module_items.py and compile/module_troops.py source diff, generated ID table parity, and _export item/troop text output before replacing a live module export.",
            "Smoke-test shop availability, troop spawning/loadout randomness, upgrade path, and the intended in-game encounter for the changed record.",
        ],
        "evidence_boundary": "Verification proves legacy source parse/evaluation, direct inventory indices, explicit upgrade target existence, and current generated-ID parity. It does not simulate economy, random equipment rolls, battle AI, save compatibility, or engine runtime behavior.",
        "warnings": ["No build or export is run by balance_verify."]
    }


def _write_payload(root: Path, payload: Mapping[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def _load_changes(value: str) -> Mapping[str, Any]:
    try:
        result = json.loads(value)
    except json.JSONDecodeError as error:
        raise BalanceError(f"changes JSON is invalid: {error}") from error
    return require_mapping(result, name="changes")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LLM-first troop/item viewer, balance analyzer, and guarded legacy-authoring editor for M&B 1.011 SoD Modern.")
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=False)
    subparsers.add_parser("summary")
    find_items = subparsers.add_parser("items")
    find_items.add_argument("--query")
    find_items.add_argument("--item-type", default="all")
    find_items.add_argument("--merchandise", choices=("all", "true", "false"), default="all")
    find_items.add_argument("--min-score", type=int)
    find_items.add_argument("--max-score", type=int)
    find_items.add_argument("--limit", type=int, default=60)
    item = subparsers.add_parser("item")
    item.add_argument("item_id")
    item.add_argument("--troop-limit", type=int, default=60)
    find_troops = subparsers.add_parser("troops")
    find_troops.add_argument("--query")
    find_troops.add_argument("--faction")
    find_troops.add_argument("--role")
    find_troops.add_argument("--exclude-heroes", action="store_true")
    find_troops.add_argument("--min-level", type=int)
    find_troops.add_argument("--max-level", type=int)
    find_troops.add_argument("--limit", type=int, default=60)
    troop = subparsers.add_parser("troop")
    troop.add_argument("troop_id")
    troop.add_argument("--item-limit", type=int, default=80)
    tree = subparsers.add_parser("upgrade-tree")
    tree.add_argument("troop_id")
    tree.add_argument("--depth", type=int, default=3)
    tree.add_argument("--limit", type=int, default=120)
    roster_inventory = subparsers.add_parser("roster-inventory")
    roster_inventory.add_argument("--roster")
    roster_inventory.add_argument("--include-heroes", action="store_true")
    roster_inventory.add_argument("--include-derived", action="store_true")
    roster_inventory.add_argument("--roster-limit", type=int, default=80)
    roster_inventory.add_argument("--troop-limit", type=int, default=100)
    roster_inventory.add_argument("--item-limit", type=int, default=160)
    progression = subparsers.add_parser("progression")
    progression.add_argument("--roster")
    progression.add_argument("--include-heroes", action="store_true")
    progression.add_argument("--include-derived", action="store_true")
    progression.add_argument("--roster-limit", type=int, default=80)
    progression.add_argument("--troop-limit", type=int, default=180)
    progression.add_argument("--edge-limit", type=int, default=220)
    campaign_cohorts = subparsers.add_parser("campaign-cohorts")
    campaign_cohorts.add_argument("--cohort")
    campaign_cohorts.add_argument("--include-heroes", action="store_true")
    campaign_cohorts.add_argument("--include-derived", action="store_true")
    campaign_cohorts.add_argument("--cohort-limit", type=int, default=80)
    campaign_cohorts.add_argument("--troop-limit", type=int, default=180)
    imperial_invasion = subparsers.add_parser("imperial-invasion")
    imperial_invasion.add_argument("--include-auxiliaries", action="store_true")
    subparsers.add_parser("player-start-factions")
    subparsers.add_parser("player-start-progression")
    subparsers.add_parser("native-kingdoms")
    subparsers.add_parser("mercenary-guilds")
    subparsers.add_parser("faith-ascensions")
    compare = subparsers.add_parser("compare")
    compare.add_argument("entity_ids", nargs="+")
    outliers = subparsers.add_parser("outliers")
    outliers.add_argument("--domain", choices=("all", "items", "troops"), default="all")
    outliers.add_argument("--include-heroes", action="store_true")
    outliers.add_argument("--limit", type=int, default=100)
    patch = subparsers.add_parser("patch")
    patch.add_argument("entity_kind", choices=("item", "troop"))
    patch.add_argument("entity_id")
    patch.add_argument("--changes", required=True, help="JSON object of bounded semantic balance changes.")
    apply = subparsers.add_parser("apply")
    apply.add_argument("entity_kind", choices=("item", "troop"))
    apply.add_argument("entity_id")
    apply.add_argument("--changes", required=True, help="The exact JSON object from the reviewed patch plan.")
    apply.add_argument("--expected-sha256", required=True)
    apply.add_argument("--expected-plan-sha256", required=True)
    apply.add_argument("--apply", action="store_true", help="Actually write the guarded legacy source record. Default is dry-run.")
    apply.add_argument("--allow-legacy-compile-authoring", action="store_true")
    apply.add_argument("--allow-protected-legacy-record-change", action="store_true")
    verify = subparsers.add_parser("verify")
    verify.add_argument("--limit", type=int, default=100)
    args = parser.parse_args(argv)
    command = args.command or "summary"
    try:
        index = build_balance_index(args.root.resolve())
        if command == "summary":
            payload = balance_summary(index)
        elif command == "items":
            merchandise = None if args.merchandise == "all" else args.merchandise == "true"
            payload = balance_find_items(index, query=args.query, item_type=args.item_type, merchandise=merchandise, min_score=args.min_score, max_score=args.max_score, limit=args.limit)
        elif command == "item":
            payload = balance_item(index, args.item_id, troop_limit=args.troop_limit)
        elif command == "troops":
            payload = balance_find_troops(index, query=args.query, faction=args.faction, role=args.role, include_heroes=not args.exclude_heroes, min_level=args.min_level, max_level=args.max_level, limit=args.limit)
        elif command == "troop":
            payload = balance_troop(index, args.troop_id, item_limit=args.item_limit)
        elif command == "upgrade-tree":
            payload = balance_upgrade_tree(index, args.troop_id, depth=args.depth, limit=args.limit)
        elif command == "roster-inventory":
            payload = balance_roster_inventory(
                index,
                roster=args.roster,
                include_heroes=args.include_heroes,
                include_derived=args.include_derived,
                roster_limit=args.roster_limit,
                troop_limit=args.troop_limit,
                item_limit=args.item_limit,
            )
        elif command == "progression":
            payload = balance_progression(
                index,
                roster=args.roster,
                include_heroes=args.include_heroes,
                include_derived=args.include_derived,
                roster_limit=args.roster_limit,
                troop_limit=args.troop_limit,
                edge_limit=args.edge_limit,
            )
        elif command == "campaign-cohorts":
            payload = balance_campaign_cohorts(
                index,
                cohort=args.cohort,
                include_heroes=args.include_heroes,
                include_derived=args.include_derived,
                cohort_limit=args.cohort_limit,
                troop_limit=args.troop_limit,
            )
        elif command == "imperial-invasion":
            payload = balance_imperial_invasion(
                index,
                include_auxiliaries=args.include_auxiliaries,
            )
        elif command == "player-start-factions":
            payload = balance_player_start_factions(index)
        elif command == "player-start-progression":
            payload = balance_player_start_progression(index)
        elif command == "native-kingdoms":
            payload = balance_native_kingdoms(index)
        elif command == "mercenary-guilds":
            payload = balance_mercenary_guilds(index)
        elif command == "faith-ascensions":
            payload = balance_faith_ascensions(index)
        elif command == "compare":
            payload = balance_compare(index, args.entity_ids)
        elif command == "outliers":
            payload = balance_outliers(index, domain=args.domain, include_heroes=args.include_heroes, limit=args.limit)
        elif command == "patch":
            payload = balance_patch(index, args.entity_kind, args.entity_id, changes=_load_changes(args.changes))
        elif command == "apply":
            payload = balance_apply(
                index,
                args.entity_kind,
                args.entity_id,
                changes=_load_changes(args.changes),
                expected_sha256=args.expected_sha256,
                expected_plan_sha256=args.expected_plan_sha256,
                dry_run=not args.apply,
                allow_legacy_compile_authoring=args.allow_legacy_compile_authoring,
                allow_protected_legacy_record_change=args.allow_protected_legacy_record_change,
            )
        else:
            payload = balance_verify(index, limit=args.limit)
        _write_payload(index.root, payload)
        return 0
    except BalanceError as error:
        parser.error(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
