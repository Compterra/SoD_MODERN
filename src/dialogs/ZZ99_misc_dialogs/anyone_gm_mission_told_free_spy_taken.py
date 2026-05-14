DIALOGS = [
[anyone, "gm_mission_told_free_spy_taken", [
  (try_begin),
    (eq, "$g_sod_last_rescue_spawn_ok", 1),
    (str_store_string, s2, "@Good. I knew we could trust you at this.\
 Here is the ransom money, {reg12} denars.\
 Count it before taking it."),
  (else_try),
    (str_store_string, s2, "@The militia column has slipped from our sight. I cannot send coin after a vanished trail. Come back later and we will try again."),
  (try_end),
  ], "{s2}", "close_window",
   [
  (finish_mission),]],
]
