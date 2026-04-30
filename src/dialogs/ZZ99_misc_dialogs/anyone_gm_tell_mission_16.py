DIALOGS = [
[anyone, "gm_tell_mission", [
   (this_or_next|eq, "$random_quest_no", "qst_elephant_guard_troublesome_bandits"),
   (this_or_next|eq, "$random_quest_no", "qst_conquistadors_troublesome_bandits"),
   (this_or_next|eq, "$random_quest_no", "qst_bc_troublesome_bandits"),
   (eq, "$random_quest_no", "qst_serpent_host_troublesome_bandits"),
   (faction_get_slot, ":message_text", "$g_talk_troop_faction", slot_guild_troublesome_bandits_text),
   (str_store_string, s15, ":message_text"),
   ],
 "{s15}", "gm_troublesome_bandits_quest_brief",
   []],
]
