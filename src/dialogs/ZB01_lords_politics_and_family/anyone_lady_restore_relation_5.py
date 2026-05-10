DIALOGS = [
[anyone, "lady_restore_relation_5", [], "Excellent. Then I'll choose an appropriate gift for you and send it to {s10} with your compliments.\
 I am sure {reg4?she:he} will appreciate the gesture.", "lady_restore_relation_6", [
     (call_script, "script_sod_player_charge_gold", "$temp_2"),
     (play_sound, "snd_money_paid"),
     (call_script, "script_change_player_relation_with_troop", "$troop_to_restore_relations_with", "$temp"),
     (troop_get_type, reg4, "$troop_to_restore_relations_with"),
     ]],
]
