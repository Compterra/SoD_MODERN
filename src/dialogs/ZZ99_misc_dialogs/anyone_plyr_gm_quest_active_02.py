DIALOGS = [
[anyone|plyr, "gm_quest_active", [],
   "I need to withdraw from the task. I will not leave you waiting on a promise I can no longer keep.", "gm_pretalk", [
   (store_partner_quest, ":lords_quest"),
   (call_script, "script_abort_quest", ":lords_quest", 1),
   ]],
]
