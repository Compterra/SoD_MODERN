DIALOGS = [
[anyone, "lord_message_delivered", [], "Oh? Let me see that...\
 Well well well! It was good of you to bring me this, {playername}. Take my seal as proof that I've received it.", "lord_pretalk", [
     (call_script, "script_end_quest", "qst_deliver_message"),
     (quest_get_slot, ":quest_giver", "qst_deliver_message", slot_quest_giver_troop),
     (call_script, "script_change_player_relation_with_troop", ":quest_giver", 3),
   ]],
]
