DIALOGS = [
[anyone|plyr|repeat_for_troops, "request_meeting_3", [(store_repeat_object, ":troop_no"),
                                                       (troop_is_hero, ":troop_no"),
                                                       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                                                       (call_script, "script_get_troop_attached_party", ":troop_no"),
                                                       (eq, "$g_encountered_party", reg0),
                                                       (call_script, "script_store_troop_name", s3, ":troop_no"),
                                                       ],
   "{s3}", "request_meeting_4", [(store_repeat_object, "$lord_requested_to_talk_to")]],
]
