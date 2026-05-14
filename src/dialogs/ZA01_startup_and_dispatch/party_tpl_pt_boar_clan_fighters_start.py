DIALOGS = [
[party_tpl|pt_boar_clan_fighters, "start", [
   (store_relation, ":relation", "fac_sod_merc_guild7", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "Ho there. If you're here to make trouble with the Boar Clan, speak quickly. We charge toll for roads and interest for insults.", "boar_clan_meet", []],
[party_tpl|pt_boar_clan_fighters, "start", [
   (store_relation, ":relation", "fac_sod_merc_guild7", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "Well now, a road-friend. Boar Clan fighters keep this dust honest enough. What brings you to our fire?", "boar_clan_meet", []],
[party_tpl|pt_boar_clan_fighters, "start", [],
   "Ho there. We're Boar Clan fighters: road teeth, toll hands, and no patience for sneaking. What's your business?", "boar_clan_meet", []],
]
