DIALOGS = [
[party_tpl|pt_messenger_party, "start", [
    (party_slot_eq, "$g_encountered_party", slot_party_sod_messenger_role, sod_messenger_role_tax_courier),
    (party_slot_eq, "$g_encountered_party", slot_party_sod_tax_courier_recipient_troop, "trp_player"),
    (party_get_slot, ":origin_center", "$g_encountered_party", slot_party_sod_tax_courier_origin_center),
    (try_begin),
      (is_between, ":origin_center", centers_begin, centers_end),
      (str_store_party_name, s1, ":origin_center"),
    (else_try),
      (str_store_string, s1, "@one of your estates"),
    (try_end),
], "My lord, we carry sealed tax from {s1}. We will press on to your party.", "tax_courier_player_talk", []],

[party_tpl|pt_messenger_party, "start", [
    (party_slot_eq, "$g_encountered_party", slot_party_sod_messenger_role, sod_messenger_role_tax_courier),
    (store_faction_of_party, ":courier_faction", "$g_encountered_party"),
    (store_relation, ":relation", ":courier_faction", "fac_player_supporters_faction"),
    (lt, ":relation", 0),
    (party_get_slot, ":origin_center", "$g_encountered_party", slot_party_sod_tax_courier_origin_center),
    (try_begin),
      (is_between, ":origin_center", centers_begin, centers_end),
      (str_store_party_name, s1, ":origin_center"),
    (else_try),
      (str_store_string, s1, "@our lord's estate"),
    (try_end),
], "Keep your distance. We carry sealed tax from {s1}, and our road is not yours to question.", "tax_courier_hostile_talk", []],

[party_tpl|pt_messenger_party, "start", [
    (party_slot_eq, "$g_encountered_party", slot_party_sod_messenger_role, sod_messenger_role_tax_courier),
    (store_faction_of_party, ":courier_faction", "$g_encountered_party"),
    (is_between, ":courier_faction", kingdoms_begin, kingdoms_end),
    (neq, ":courier_faction", "fac_player_supporters_faction"),
    (store_relation, ":relation", ":courier_faction", "fac_player_supporters_faction"),
    (ge, ":relation", 0),
    (party_get_slot, ":origin_center", "$g_encountered_party", slot_party_sod_tax_courier_origin_center),
    (try_begin),
      (is_between, ":origin_center", centers_begin, centers_end),
      (str_store_party_name, s1, ":origin_center"),
    (else_try),
      (str_store_string, s1, "@our lord's estate"),
    (try_end),
], "Good day. We carry sealed tax from {s1} under lawful protection. Let us pass.", "tax_courier_nonhostile_talk", []],

[anyone|plyr, "tax_courier_hostile_talk", [], "Hand over the tax chest and ride away alive.", "tax_courier_surrender_demand", [
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":courier_size", "$g_encountered_party"),
    (val_max, ":courier_size", 1),
    (assign, ":chance", 35),
    (store_mul, ":persuasion_bonus", ":persuasion", 8),
    (val_add, ":chance", ":persuasion_bonus"),
    (store_mul, ":leadership_bonus", ":leadership", 3),
    (val_add, ":chance", ":leadership_bonus"),
    (store_mul, ":courier_double", ":courier_size", 2),
    (try_begin),
      (ge, ":player_size", ":courier_double"),
      (val_add, ":chance", 25),
    (try_end),
    (val_clamp, ":chance", 5, 96),
    (store_random_in_range, ":roll", 0, 100),
    (try_begin),
      (lt, ":roll", ":chance"),
      (assign, "$g_sod_tax_courier_surrender_success", 1),
    (else_try),
      (assign, "$g_sod_tax_courier_surrender_success", 0),
    (try_end),
]],

[anyone|plyr, "tax_courier_nonhostile_talk", [], "Hand over the tax chest and ride away alive.", "tax_courier_surrender_demand", [
    (call_script, "script_sod_tax_courier_apply_nonhostile_coercion_consequence", "$g_encountered_party"),
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":courier_size", "$g_encountered_party"),
    (val_max, ":courier_size", 1),
    (assign, ":chance", 35),
    (store_mul, ":persuasion_bonus", ":persuasion", 8),
    (val_add, ":chance", ":persuasion_bonus"),
    (store_mul, ":leadership_bonus", ":leadership", 3),
    (val_add, ":chance", ":leadership_bonus"),
    (store_mul, ":courier_double", ":courier_size", 2),
    (try_begin),
      (ge, ":player_size", ":courier_double"),
      (val_add, ":chance", 25),
    (try_end),
    (val_clamp, ":chance", 5, 96),
    (store_random_in_range, ":roll", 0, 100),
    (try_begin),
      (lt, ":roll", ":chance"),
      (assign, "$g_sod_tax_courier_surrender_success", 1),
    (else_try),
      (assign, "$g_sod_tax_courier_surrender_success", 0),
    (try_end),
]],

[anyone, "tax_courier_surrender_demand", [
    (eq, "$g_sod_tax_courier_surrender_success", 1),
], "Steel buys no loyalty from a dead messenger. Take the chest. We never saw your banners.", "close_window", [
    (call_script, "script_sod_tax_courier_surrender_to_player", "$g_encountered_party"),
]],

[anyone, "tax_courier_surrender_demand", [], "No. The chest reaches its lord or we die around it.", "close_window", [
    (encounter_attack),
]],

[anyone|plyr, "tax_courier_hostile_talk", [], "Then defend it.", "close_window", [
    (encounter_attack),
]],

[anyone|plyr, "tax_courier_hostile_talk", [], "Ride on. This road has enough blood on it.", "close_window", [
    (assign, "$g_leave_encounter", 1),
]],

[anyone|plyr, "tax_courier_nonhostile_talk", [], "Ride on. Safe roads serve us all.", "close_window", [
    (assign, "$g_leave_encounter", 1),
]],

[anyone|plyr, "tax_courier_player_talk", [], "Ride on. Keep the chest close.", "close_window", [
    (assign, "$g_leave_encounter", 1),
]],
]
