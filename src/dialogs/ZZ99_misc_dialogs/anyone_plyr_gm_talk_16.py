DIALOGS = [
[anyone|plyr, "gm_talk", [
   (neq,"$g_talk_troop", "trp_boar_clan_guild_master"),
   (neq,"$g_talk_troop", "trp_boar_clan_representative"),
   (faction_get_slot, ":faction_base", "$g_talk_troop_faction", slot_guild_base),
   (party_get_slot, "$hero_requested_to_learn_location", ":faction_base", slot_town_lord),
   (str_store_troop_name, s43, "$hero_requested_to_learn_location"),
   ], "I need {s43}. Where was that banner last seen?", "gm_ask_location", []],
]
