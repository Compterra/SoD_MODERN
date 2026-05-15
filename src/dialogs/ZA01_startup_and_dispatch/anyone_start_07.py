DIALOGS = [
[anyone, "start", [
  (gt, "$fight_guild_troops_quest", 1),
  (eq, "$fgtq_state", fgtq_end),
  (str_store_string_reg, s68, s0),
  ], "{s68}", "close_window", [(assign, "$fgtq_state", -1),
  (assign, "$fight_guild_troops_quest", -1),(finish_mission)] ],
]
