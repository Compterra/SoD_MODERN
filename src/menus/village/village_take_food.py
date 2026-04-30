MENUS = [
(
    "village_hostile_action", 0,
    "What action do you have in mind?",
    "none",
    [],
    [
      ("village_take_food", [
        (party_slot_eq, "$current_town", slot_village_state, 0),
        (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
        (assign, ":town_stores_not_empty", 0),
        (try_for_range, ":slot_no", num_equipment_kinds, max_inventory_items + num_equipment_kinds),
          (troop_get_inventory_slot, ":slot_item", ":merchant_troop", ":slot_no"),
          (ge, ":slot_item", 0),
          (assign, ":town_stores_not_empty", 1),
        (try_end),
        (eq, ":town_stores_not_empty", 1),
      ],
      "Force the peasants to give you supplies.", [
        (jump_to_menu, "mnu_village_take_food_confirm")
      ]),

      ("village_steal_cattle", [
        (party_slot_eq, "$current_town", slot_village_state, 0),
        (party_slot_eq, "$current_town", slot_village_player_can_not_steal_cattle, 0),
        (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        (party_get_slot, ":num_cattle", "$current_town", slot_village_number_of_cattle),
        (neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
        (gt, ":num_cattle", 0),
      ],
      "Steal cattle.", [
        (jump_to_menu, "mnu_village_steal_cattle_confirm")
      ]),

      ("village_loot", [
        (party_slot_eq, "$current_town", slot_village_state, 0),
        (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (store_relation, ":reln", "fac_player_supporters_faction", ":center_faction"),
        (lt, ":reln", 0),
      ],
      "Loot and burn this village.", [
        (jump_to_menu, "mnu_village_start_attack"),
      ]),

      ("forget_it", [], "Forget it.", [(jump_to_menu, "mnu_village")]),
    ],
  ),
]
