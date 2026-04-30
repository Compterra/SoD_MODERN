DIALOGS = [
[anyone, "lord_mercenary_service_verify_2", [], "That will do. You've made a wise choice, my friend.\
 {s9} does well by its loyal fighters, you will receive many rewards for your service.", "lord_mercenary_service_accept_3", [
     (call_script, "script_merc_begin_service", "$g_talk_troop_faction", "$temp", 90),
     (str_store_faction_name, s9, "$g_talk_troop_faction"), ]],
]
