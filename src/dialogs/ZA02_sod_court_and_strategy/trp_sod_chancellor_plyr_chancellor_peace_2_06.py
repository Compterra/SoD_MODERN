DIALOGS = [
[trp_sod_chancellor|plyr, "chancellor_peace_2", [
        (eq, 0, 1),
        (faction_slot_eq, "fac_kingdom_6", slot_faction_state, sfs_active), 
      (store_relation, ":rln", "fac_player_supporters_faction", "fac_kingdom_6"),
	(lt, ":rln", 0),], "To the Imperial Expeditionary Force.", "chancellor_peace_3", [(assign, "$temp", "fac_kingdom_6") ]],
]
