DIALOGS = [
[anyone, "move_cattle_herd_quest_taken", [
   (try_begin),
     (eq, "$g_sod_last_cattle_herd_spawn_ok", 1),
     (str_store_string, s2, "@Splendid. You can find the herd right outside the town. After you take the animals to {s13}, return back to me and I will give you your pay."),
   (else_try),
     (str_store_string, s2, "@The herd cannot be gathered right now. Come back later and I will see whether the drovers have found enough cattle."),
   (try_end),
   ], "{s2}", "mayor_pretalk", []],
]
