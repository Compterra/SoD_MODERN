MENUS = [
(
    "castle_outside", mnf_enable_hot_keys,
    "You are outside {s2}.{s11} {s3} {s4}",
    "none",
    [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (assign, "$g_ally_party", -1),
      (str_store_party_name, s2, "$g_encountered_party"),
      (call_script, "script_encounter_calculate_fit"),
      (assign, "$all_doors_locked", 1),
      (assign, "$current_town", "$g_encountered_party"),
      (try_begin),
        (eq, "$new_encounter", 1),
        #(display_message, "@new encounter", debug_color), #####DEBUG ONLY#####
        (assign, "$new_encounter", 0),
        (call_script, "script_let_nearby_parties_join_current_battle", 1, 0),
        (call_script, "script_encounter_init_variables"),
        (assign, "$entry_to_town_forbidden", 0),
        (assign, "$sneaked_into_town", 0),
        (assign, "$town_entered", 0),
        (assign, "$encountered_party_hostile", 0),
        (assign, "$encountered_party_friendly", 0),

        # clear any current siege if it isn't this center
        (try_begin),
          (gt, "$g_player_besiege_town", 0),
          (neq, "$g_player_besiege_town", "$g_encountered_party"),
          (party_slot_eq, "$g_player_besiege_town", slot_center_is_besieged_by, "p_main_party"),
          (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
          (assign, "$g_player_besiege_town", -1),
        (try_end),

        # mark that the player can't just waltz in here - hostile!
        (try_begin),
          (lt, "$g_encountered_party_relation", 0),
          (assign, "$encountered_party_hostile", 1),
          (assign, "$entry_to_town_forbidden", 1),
        (try_end),

        # determine if sneaking is an option
        (assign, "$cant_sneak_into_town", 0),
        (try_begin),
          (eq, "$current_town", "$last_sneak_attempt_town"),
          (store_current_hours, reg(2)),
          (val_sub, reg(2), "$last_sneak_attempt_time"),
          (lt, reg(2), 12),
          (assign, "$cant_sneak_into_town", 1),
        (try_end),

      (else_try),
        #second or more turn
        (eq, "$g_leave_encounter", 1),
        (change_screen_return),
      (try_end),

      # get menu text for whether they can sneak in or not
      (str_clear, s4),
      (try_begin),
        (eq, "$entry_to_town_forbidden", 1),
        (try_begin),
          (eq, "$cant_sneak_into_town", 1),
          (str_store_string, s4, "str_sneaking_to_town_impossible"),
        (else_try),
          (str_store_string, s4, "str_entrance_to_town_forbidden"),
        (try_end),
      (try_end),

      # determine text for who is lord of this place
      (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
      (store_faction_of_party, ":center_faction", "$current_town"),
      (str_store_faction_name, s9, ":center_faction"),
      (try_begin),
        (ge, ":center_lord", 0),
        (call_script, "script_store_troop_name", s8, ":center_lord"),
        (str_store_string, s7, "@{s8} of {s9}"),
      (try_end),

      # generate menu text indicating who is the lord of this locale
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_castle),
        (try_begin),
          (eq, ":center_lord", "trp_player"),
          (str_store_string, s11, "@ Your own banner flies over the castle gate."),
        (else_try),
          (ge, ":center_lord", 0),
          (str_store_string, s11, "@ You see the banner of {s7} over the castle gate."),
        (else_try),
          (str_store_string, s11, "@ This castle seems to belong to no one."),
        (try_end),
      (else_try),
        (try_begin),
          (eq, ":center_lord", "trp_player"),
          (str_store_string, s11, "@ Your own banner flies over the town gates."),
        (else_try),
          (ge, ":center_lord", 0),
          (str_store_string, s11, "@ You see the banner of {s7} over the town gates."),
        (else_try),
          (str_store_string, s11, "@ The townsfolk here have declared their independence."),
        (try_end),
      (try_end),

      # check if this place is defended or not
      (party_get_num_companions, reg(7), "p_collective_enemy"),
      (assign, "$castle_undefended", 0),
      (str_clear, s3),
      (try_begin),
        (eq, reg(7), 0),
        (assign, "$castle_undefended", 1),
        (str_store_string, s3, "str_castle_is_abondened"),
      (else_try),
        (eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
        (str_store_string, s3, "str_place_is_occupied_by_player"),
      (else_try),
        (lt, "$g_encountered_party_relation", 0),
        (str_store_string, s3, "str_place_is_occupied_by_enemy"),
        (party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
        (call_script, "script_center_get_food_consumption", "$current_town"),
        (assign, ":food_consumption", reg0),
        (store_div, reg3, ":town_food_store", ":food_consumption"),
        (str_store_string, s3, "@{s3} It has enough food to hold out for another {reg3} days."),
      (try_end),

      (try_begin),
        # leaving...
        (eq, "$g_leave_town_outside", 1),
        (assign, "$g_leave_town_outside", 0),
        (assign, "$g_permitted_to_center", 0),
        (change_screen_return),
      (else_try),
        # escort a lady quest...
        (check_quest_active, "qst_escort_lady"),
        (quest_slot_eq, "qst_escort_lady", slot_quest_target_center, "$g_encountered_party"),
        (quest_get_slot, ":quest_object_troop", "qst_escort_lady", slot_quest_object_troop),
        (modify_visitors_at_site, "scn_conversation_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 17, ":quest_object_troop"),
        (set_jump_mission, "mt_conversation_encounter"),
        (jump_to_scene, "scn_conversation_scene"),
        (assign, "$talk_context", tc_entering_center_quest_talk),
        (change_screen_map_conversation, ":quest_object_troop"),
      (else_try),
        # kidnap quest...
        (check_quest_active, "qst_kidnapped_girl"),
        (quest_slot_eq, "qst_kidnapped_girl", slot_quest_giver_center, "$g_encountered_party"),
        (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3),
        (modify_visitors_at_site, "scn_conversation_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 17, "trp_kidnapped_girl"),
        (set_jump_mission, "mt_conversation_encounter"),
        (jump_to_scene, "scn_conversation_scene"),
        (assign, "$talk_context", tc_entering_center_quest_talk),
        (change_screen_map_conversation, "trp_kidnapped_girl"),
      (else_try),
        # interrupted resting here...
        (eq, "$g_town_visit_after_rest", 1),
        (assign, "$g_town_visit_after_rest", 0),
        (jump_to_menu, "mnu_town"),
      (else_try),
        # our own center
        (party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
        (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
        # MORDACHAI - simply let me at my own holdings!
        (jump_to_menu, "mnu_town"),
      (else_try),
        # allowed to just waltz in to this castle...
        (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
        (ge, "$g_encountered_party_relation", 0),
        (this_or_next|eq, "$castle_undefended", 1),
        (eq, "$g_permitted_to_center", 1),
        (jump_to_menu, "mnu_town"),
      (else_try),
        # allowed to just waltz in to this town...
        (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
        (ge, "$g_encountered_party_relation", 0),
        (jump_to_menu, "mnu_town"),
      (else_try),
        # the player is the one besieging this locale...
        (eq, "$g_player_besiege_town", "$g_encountered_party"),
        (jump_to_menu, "mnu_castle_besiege"),
      (try_end),

      # choose a background based on the location and time of day
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_town),
        (store_sub, "$g_sod_town_background", "$current_town", "p_town_1"),
        (val_mul, "$g_sod_town_background", 2),
        (val_add, "$g_sod_town_background", "mesh_pic_town_1_outside"),
      (else_try),
        (store_sub, "$g_sod_town_background", "$current_town", "p_castle_1"),
        (val_mul, "$g_sod_town_background", 2),
        (val_add, "$g_sod_town_background", "mesh_pic_castle_1_outside"),
      (try_end),
      (try_begin),
        (store_time_of_day, ":cur_hour"),
        (ge, ":cur_hour", 5),
        (lt, ":cur_hour", 21),
        (assign, "$town_nighttime", 0),
      (else_try),
        (assign, "$town_nighttime", 1),
      (try_end),
      (val_add, "$g_sod_town_background", "$town_nighttime"),
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("approach_gates",
        [(this_or_next|eq, "$entry_to_town_forbidden", 1),
         (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle)],
       "Approach the gates and hail the guard.", [(jump_to_menu, "mnu_castle_guard"), ]),

      ("town_sneak",
        [(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
         (eq, "$entry_to_town_forbidden", 1),
         (eq, "$cant_sneak_into_town", 0)],
       "Disguise yourself and try to sneak into the town.",
       [
         (faction_get_slot, ":player_alarm", "$g_encountered_party_faction", slot_faction_player_alarm),
         (party_get_num_companions, ":num_men", "p_main_party"),
         (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
         (val_add, ":num_men", ":num_prisoners"),
         (val_mul, ":num_men", 2),
         (val_div, ":num_men", 3),
         (store_add, ":get_caught_chance", ":player_alarm", ":num_men"),
         (store_random_in_range, ":random_chance", 0, 100),
         (try_begin),
           (this_or_next|ge, ":random_chance", ":get_caught_chance"),
           (eq, "$g_last_defeated_bandits_town", "$g_encountered_party"),
           (assign, "$g_last_defeated_bandits_town", 0),
           (assign, "$sneaked_into_town", 1),
           (assign, "$town_entered", 1),
           (jump_to_menu, "mnu_sneak_into_town_suceeded"),
         (else_try),
           (jump_to_menu, "mnu_sneak_into_town_caught"),
         (try_end)
       ]
     ),

      # give player the option to siege this town or castle
      ("castle_start_siege",
       [
         # MORDACHAI - allow the marshall or King to commandeer the siege
         (assign, ":can_siege", 0),
         (try_begin),
           # nobody sieging here yet, or its the player who is in the process of sieging here...
           (this_or_next|party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
           (             party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),

           # and no second party involved
           (lt, "$g_encountered_party_2", 1),

           (assign, ":can_siege", 1),

         (else_try),

           # player outranks those doing the siege...
           (party_get_slot, ":siege_party", "$g_encountered_party", slot_center_is_besieged_by),
           (ge, ":siege_party", 0),
           (party_is_active, ":siege_party"),
           (store_faction_of_party, ":siege_party_faction", ":siege_party"),
           (ge, ":siege_party_faction", 0),
           (this_or_next|faction_slot_eq, ":siege_party_faction", slot_faction_marshall, "trp_player"),
           (             faction_slot_eq, ":siege_party_faction", slot_faction_leader, "trp_player"),

           (assign, ":can_siege", 1),

         (try_end),
         (eq, ":can_siege", 1),

         #MORDACHAI - allow sieges against what what a neutral or friendly faction (acts as a declaration of war)
         #(store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
         #(lt, ":reln", 0),

         #MORDACHAI - but also disallow you from attacking your own kingdom's centers!
         (neq, "$g_encountered_party_faction", "$players_kingdom"),
         (neq, "$g_encountered_party_faction", "fac_player_faction"),
         (neq, "$g_encountered_party_faction", "fac_player_supporters_faction"),

         # the player must still have enough troops to proceed
         (call_script, "script_party_count_fit_for_battle", "p_main_party"),
         (gt, reg(0), 5),
         (try_begin),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (assign, reg6, 1),
         (else_try),
           (assign, reg6, 0),
         (try_end),
       ],
       "Besiege the {reg6?town:castle}.",
       [
         #MORDACHAI - give the player a chance to confirm if this means war
         (try_begin),
           (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
           (gt, ":reln", -1), #twanx
           (jump_to_menu, "mnu_castle_siege_confirm"),
         (else_try),
           (assign, "$g_player_besiege_town", "$g_encountered_party"),
          (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -10), #twanx
           (call_script, "script_update_all_notes"),
           (jump_to_menu, "mnu_castle_besiege"),
         (try_end),
         ]),

      ("castle_leave", [], "Leave.", [(change_screen_return, 0)]),
    ]
  ),
]
