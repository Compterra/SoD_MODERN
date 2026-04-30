MENUS = [
(
    "requested_castle_granted_to_another", mnf_scale_picture,
    "You receive a message from your monarch, {s3}.^^"\
    "'I was most pleased to hear of your valiant efforts in the capture of {s2}. Your victory has gladdened all our hearts."\
    " You also requested me to give you ownership of the castle, but that is a favour which I fear I cannot grant,"\
    " as you already hold significant estates in my realm."\
    " Instead I have sent you {reg6} denars to cover the expenses of your campaign, but {s2} I give to {s5}.'",
    "none",
    [(set_background_mesh, "mesh_pic_messenger"),
     (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
     (call_script, "script_store_troop_name", s3, ":faction_leader"),
     (str_store_party_name, s2, "$g_center_to_give_to_player"),
     (party_get_slot, ":new_owner", "$g_center_to_give_to_player", slot_town_lord),
     (call_script, "script_store_troop_name", s5, ":new_owner"),
     (assign, reg6, 900),
    ],
    [
      ("accept_decision", [], "Accept the decision.",
       [
       (call_script, "script_troop_add_gold", "trp_player", reg6),
       (change_screen_return),
        ]),
      ("leave_faction", [], "You have been wronged! Renounce you oath to your liege! ",
       [
         (jump_to_menu, "mnu_leave_faction"),
         (call_script, "script_troop_add_gold", "trp_player", reg6),
        ]),
     ],
  ),
]
