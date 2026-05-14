SIMPLE_TRIGGERS = [
(1,
   [
      (gt, "$auto_besiege_town", 0),
      (party_is_active, "$auto_besiege_town"),
      (gt, "$g_player_besiege_town", 0),
      (party_is_active, "$g_player_besiege_town"),
      (ge, "$g_siege_method", 1),
      (store_current_hours, ":cur_hours"),
      (eq, "$g_siege_force_wait", 0),
      (ge, ":cur_hours", "$g_siege_method_finish_hours"),
      (neg|is_currently_night),
      (rest_for_hours, 0, 0, 0), #stop resting
    ]),
]
