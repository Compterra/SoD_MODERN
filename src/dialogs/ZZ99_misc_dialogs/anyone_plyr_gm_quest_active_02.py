DIALOGS = [
[anyone|plyr, "gm_quest_active", [],
   "I'm affraid I won't be able complete this task.", "gm_pretalk", [
   (store_partner_quest, ":lords_quest"),
   (call_script, "script_abort_quest", ":lords_quest", 1),
   ]],
]
