# -*- coding: utf-8 -*-
"""Intentional slot aliases for legacy SoD constants.

The verifier uses this to distinguish deliberate shared values from suspicious overlaps.
"""
from __future__ import annotations

ALIAS_GROUPS = [
    {
        "troop_trainer_met",
        "troop_spouse",
        "troop_family_begin",
    },
    {
        "troop_trainer_waiting_for_result",
        "troop_father",
    },
    {
        "troop_trainer_training_fight_won",
        "troop_mother",
    },
    {
        "troop_trainer_num_opponents_to_beat",
        "troop_daughter",
    },
    {
        "troop_trainer_training_system_explained",
        "troop_son",
    },
    {
        "troop_trainer_opponent_troop",
        "troop_sibling",
    },
    {
        "troop_trainer_training_difficulty",
        "troop_lover",
        "troop_family_end",
    },
    {
        "troop_enemy_1",
        "troop_enemies_begin",
    },
    {
        "center_npc_volunteer_troop_type",
        "center_mercenary_troop_type",
    },
    {
        "center_npc_volunteer_troop_amount",
        "center_mercenary_troop_amount",
    },
    {
        "center_sod_local_health",
        "center_health",
    },
    {
        "town_trade_route_1",
        "town_trade_routes_begin",
    },
    {
        "lord_pursuit_state",
        "lord_ai_timer",
    },
    {
        "item_head_armor",
        "item_cant_use_on_horseback",
        "item_horse_speed",
    },
    {
        "item_body_armor",
        "item_thrust_damage",
        "item_shield_size",
        "item_horse_armor",
    },
    {
        "item_leg_armor",
        "item_swing_damage",
        "item_shield_armor",
        "item_horse_charge",
    },
]


EXPLICIT_ALIAS_BY_OWNER_VALUE = {
    ("slot_center_", 90): {
        "slot_center_npc_volunteer_troop_type",
        "slot_center_mercenary_troop_type",
    },
    ("slot_center_", 91): {
        "slot_center_npc_volunteer_troop_amount",
        "slot_center_mercenary_troop_amount",
    },
    ("slot_center_", 247): {
        "slot_center_sod_local_health",
        "slot_center_health",
    },
    ("slot_item_", 6): {
        "slot_item_head_armor",
        "slot_item_cant_use_on_horseback",
        "slot_item_horse_speed",
    },
    ("slot_item_", 7): {
        "slot_item_body_armor",
        "slot_item_thrust_damage",
        "slot_item_shield_size",
        "slot_item_horse_armor",
    },
    ("slot_item_", 8): {
        "slot_item_leg_armor",
        "slot_item_swing_damage",
        "slot_item_shield_armor",
        "slot_item_horse_charge",
    },
    ("slot_lord_", 255): {
        "slot_lord_pursuit_state",
        "slot_lord_ai_timer",
    },
    ("slot_town_", 290): {
        "slot_town_trade_route_1",
        "slot_town_trade_routes_begin",
    },
    ("slot_troop_", 30): {
        "slot_troop_spouse",
        "slot_troop_trainer_met",
        "slot_troop_family_begin",
    },
    ("slot_troop_", 31): {
        "slot_troop_father",
        "slot_troop_trainer_waiting_for_result",
    },
    ("slot_troop_", 32): {
        "slot_troop_mother",
        "slot_troop_trainer_training_fight_won",
    },
    ("slot_troop_", 33): {
        "slot_troop_daughter",
        "slot_troop_trainer_num_opponents_to_beat",
    },
    ("slot_troop_", 34): {
        "slot_troop_son",
        "slot_troop_trainer_training_system_explained",
    },
    ("slot_troop_", 35): {
        "slot_troop_sibling",
        "slot_troop_trainer_opponent_troop",
    },
    ("slot_troop_", 36): {
        "slot_troop_lover",
        "slot_troop_trainer_training_difficulty",
        "slot_troop_family_end",
    },
    ("slot_troop_", 40): {
        "slot_troop_enemy_1",
        "slot_troop_enemies_begin",
    },
}
