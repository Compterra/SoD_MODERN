MENUS = [
(
    "invite_player_to_faction_without_center", mnf_scale_picture,
    "You receive an offer of vassalage!^^{s8} of {s9} has sent a royal herald to bring you an invititation in his own hand."\
    " You would be granted the honour of becoming a vassal {lord/lady} of {s9}, and in return {s8} asks you to swear an oath of homage to him and fight in his military campaigns,"\
    " although he offers you no lands or titles. He will surely be offended if you do not take the offer...",
    "none",
    [
      (set_background_mesh, "mesh_pic_messenger"),
      (faction_get_slot, "$g_invite_faction_lord", "$g_invite_faction", slot_faction_leader),
      (call_script, "script_store_troop_name", s8, "$g_invite_faction_lord"),
      (str_store_faction_name, s9, "$g_invite_faction"),
    ],
    [
      ("faction_accept", [], "Accept!",
       [(call_script, "script_store_troop_name", s1, "$g_invite_faction_lord"),
        (setup_quest_text, "qst_join_faction"),

        (call_script, "script_store_troop_name_link", s3, "$g_invite_faction_lord"),
        (str_store_faction_name_link, s4, "$g_invite_faction"),
        (quest_set_slot, "qst_join_faction", slot_quest_giver_troop, "$g_invite_faction_lord"),
        (quest_set_slot, "qst_join_faction", slot_quest_expiration_days, 30),
        (str_store_string, s2, "@Find and speak with {s3} of {s4} to give him your oath of homage."),
        (call_script, "script_start_quest", "qst_join_faction", "$g_invite_faction_lord"),
        (call_script, "script_report_quest_troop_positions", "qst_join_faction", "$g_invite_faction_lord", 3),
        (jump_to_menu, "mnu_invite_player_to_faction_accepted"),
        ]),
      ("faction_reject", [], "Decline the invitation.",
       [(call_script, "script_change_player_relation_with_troop", "$g_invite_faction_lord", -3),
        (call_script, "script_change_player_relation_with_faction", "$g_invite_faction", -10),
        (assign, "$g_invite_faction", 0),
        (assign, "$g_invite_faction_lord", 0),
        (assign, "$g_invite_offered_center", 0),
        (change_screen_return),
        ]),
     ]
  ),
]
