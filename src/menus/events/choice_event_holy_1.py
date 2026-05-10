MENUS = [
(
    "event_holy", mnf_disable_all_keys,
    "One of your noble elites requests a private audience. -My liege,- the veteran says, -I have served faithfully, but now I feel {s2}. If you grant leave, I will join {s1} and become a living standard for our cause.-",
    "none",
    [
      (set_background_mesh, "mesh_pic_faith_zealot"),
	  (str_clear, s1),
	  (str_clear, s2),
	  (try_begin),
	  (eq, "$g_sod_faith", cb_the_one),
	  (str_store_string, s1, "@the temple to serve God"),
	  (str_store_string, s2, "@a solemn calling; God himself seems to summon me"),
	  (else_try),
	  (eq, "$g_sod_faith", cb_old_gods),
	  (str_store_string, s1, "@the temple to honor our ancestors"),
	  (str_store_string, s2, "@the weight of the ancestors at my back"),
	  (else_try),
	  (eq, "$g_sod_faith", cb_the_void),
	  (str_store_string, s1, "@the temple to spread the Void"),
	  (str_store_string, s2, "@the pull of the Void, cold and absolute"),
	  (else_try),
	  (eq, "$g_sod_faith", cb_enlightenment),
	  (str_store_string, s1, "@the temple to meditate"),
	  (str_store_string, s2, "@a clarity I can no longer ignore"),
	  (else_try),
	  (eq, "$g_sod_faith", cb_atheism),
	  (str_store_string, s1, "@an academy to study"),
	  (str_store_string, s2, "@that discipline and reason can make me more useful than zeal alone"),
	  (try_end),
    ],
    [
      ("choice_event_holy_1", [(store_troop_gold, ":gold", "trp_player"), (ge, ":gold", 200), (call_script, "script_sod_troop_get_effective_faith"), (ge, reg0, sod_zealot_min_faith)], "Go with my blessing. Serve the cause. (200 denars)",
       [
		(party_remove_members, "p_main_party", "$g_sod_last_noble", 1),
        (party_add_members , "p_main_party", "$g_sod_zealot", 1),             #twan456b
        (call_script, "script_sod_troop_apply_faith_ascension_cost", 1),
        (call_script, "script_sod_player_charge_gold", 200),
        (change_screen_return),
        ]
       ),
      ("choice_event_holy_2", [], "No. Your purse will serve the faith better than your vows.",
       [
	    (store_random_in_range, ":donation", 20, 500), #twan456b there was no reason to chose this
	    (troop_add_gold, "trp_player", ":donation"),
        (call_script, "script_change_player_honor", -1),
        (val_sub, "$g_sod_global_faith", 50),
        (val_clamp, "$g_sod_global_faith", -2000, 2001),
        (change_screen_return),
        ]
       ),
      ("choice_event_holy_3", [], "I release you from your oath. Preach among the people.",
       [
       (call_script, "script_change_player_honor", 2),
       (val_add, "$g_sod_global_faith", 50),
       (val_clamp, "$g_sod_global_faith", -2000, 2001),
       #MORDACHAI - bug fix: was failing to actually remove the unit who presumably goes off to become a priest or librarian
       (party_remove_members , "p_main_party", "$g_sod_last_noble", 1), #twan456b
       (change_screen_return),
        ]
       ),
      ]
  ),
]
