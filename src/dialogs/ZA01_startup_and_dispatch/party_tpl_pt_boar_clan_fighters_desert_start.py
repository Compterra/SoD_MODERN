DIALOGS = [
[party_tpl|pt_boar_clan_fighters_desert, "start", [
   (store_relation, ":relation", "fac_sod_merc_guild7", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "Careful in this dry road, laddie. Boar Clan fighters do not need trees to make an ambush, and we do not forgive cheap threats.", "boar_clan_meet", []],
[party_tpl|pt_boar_clan_fighters_desert, "start", [
   (store_relation, ":relation", "fac_sod_merc_guild7", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "A familiar banner in hard country. Boar Clan fighters are watching the dry roads; come close enough to speak, not close enough to startle.", "boar_clan_meet", []],
[party_tpl|pt_boar_clan_fighters_desert, "start", [],
   "Ho there from the dust. Boar Clan fighters are holding this dry road for toll, warning, and whatever trouble thinks itself clever.", "boar_clan_meet", []],
]
