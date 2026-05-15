DIALOGS = [
[anyone, "start", [
  (gt, "$fight_guild_troops_quest", 1),
  (eq, "$fgtq_state", fgtq_next),
  (str_store_string_reg, s68, s1),
  ], "{s68}", "fgtq_gm_next", [] ],
]
