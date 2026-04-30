DIALOGS = [
[trp_sod_chancellor|plyr, "chancellor_peace_2", [
        (faction_slot_eq, "fac_kingdom_5", slot_faction_state, sfs_active), 
      (store_relation, ":rln", "fac_player_supporters_faction", "fac_kingdom_5"),
	(lt, ":rln", 0),], "To the Republic of Rhodoks.", "chancellor_peace_3", [(assign, "$temp", "fac_kingdom_5") ]],
]
