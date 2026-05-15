MENUS = [
(
    "leave_faction", 0,
    "Renouncing your oath is a grave act. Your lord may condemn you and confiscate your lands and holdings. However, if you return them of your own free will, he may let the betrayal go without a fight.",
    "none",
    [
      (str_store_string, s2, "@the disputed fief"),
      (try_begin),
        (is_between, "$g_center_to_give_to_player", centers_begin, centers_end),
        (str_store_party_name, s2, "$g_center_to_give_to_player"),
      (try_end),
    ],
    [
      ("leave_faction_give_back", [], "Renounce your oath and give up your holdings.",
       [(call_script, "script_player_leave_faction", 1),
        (change_screen_return), ]),

      ("leave_faction_hold", [
        (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
        (is_between, "$g_center_to_give_to_player", centers_begin, centers_end),
        ],
       "Renounce your oath and hold on to your lands, including {s2}.",
       [
        (try_begin),
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          (is_between, "$g_center_to_give_to_player", centers_begin, centers_end),
          (faction_get_slot, ":old_leader", "$players_kingdom", slot_faction_leader),
          (call_script, "script_add_log_entry", logent_renounced_allegiance, "trp_player", -1, ":old_leader", "$players_kingdom"),

          #Initializing renounce war variables
          (assign, "$players_oath_renounced_against_kingdom", "$players_kingdom"),
          (assign, "$players_oath_renounced_given_center", 0),
          (store_current_hours, "$players_oath_renounced_begin_time"),

          (call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0),
          (call_script, "script_player_leave_faction", 0),
          (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
            (store_faction_of_party, ":cur_center_faction", ":cur_center"),
            (party_set_slot, ":cur_center", slot_center_faction_when_oath_renounced, ":cur_center_faction"),
          (try_end),
          (party_set_slot, "$g_center_to_give_to_player", slot_center_faction_when_oath_renounced, "$players_oath_renounced_against_kingdom"),
          (change_screen_return),
        (else_try),
          (assign, "$g_center_to_give_to_player", -1),
          (change_screen_return),
        (try_end),
        ]),

      ("leave_faction_cancel", [], "Remain loyal and accept the decision.", [ (change_screen_return), ]),
    ],
  ),
]
