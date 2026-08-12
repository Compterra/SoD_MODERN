DIALOGS = [
[anyone|plyr, "companion_recruit_payment_response", [
                    (is_between, "$g_talk_troop", companions_begin, companions_end),
                    (hero_can_join, "p_main_party"),
                    (troop_get_slot, ":amount_requested", "$g_talk_troop", slot_troop_payment_request), #
                    (store_troop_gold, ":gold", "trp_player"), #
                    (ge, ":gold", ":amount_requested"), #
                    (assign, reg3, ":amount_requested"),
                    (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
                    (store_add, ":dialog_line", "str_npc1_payment_response", ":npc_offset"),
                    (str_store_string, s69, ":dialog_line"),
      ], "{s69}", "companion_recruit_signup_confirm", [
                    (troop_get_slot, ":amount_requested", "$g_talk_troop", slot_troop_payment_request), #
                    (gt, ":amount_requested", 0), #
                    (call_script, "script_sod_player_charge_gold", ":amount_requested"),  #
                    (play_sound, "snd_money_paid"),
                    (troop_set_slot, "$g_talk_troop", slot_troop_payment_request, 0), #
          ]],
]
