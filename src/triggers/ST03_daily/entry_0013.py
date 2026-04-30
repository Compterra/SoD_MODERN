SIMPLE_TRIGGERS = [
(24,
   [
    (eq, "$g_player_banner_granted", 1),
    (troop_slot_eq, "trp_player", slot_troop_banner_scene_prop, 0),
    (le, "$auto_menu", 0),
    #normal_banner_begin
    #(start_presentation, "prsnt_banner_selection"),
    # custom_banner_begin
    (start_presentation, "prsnt_custom_banner"),
    ]),
]
