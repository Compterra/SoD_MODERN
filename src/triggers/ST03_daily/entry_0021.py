SIMPLE_TRIGGERS = [
(48,
    [
    (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        # only active parties on the map
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
		(gt, ":hero_party", 0),
        (party_is_active, ":hero_party"),
		(party_get_battle_opponent, ":opponent", ":hero_party"),
		(lt, ":opponent", 0),

        # scale with player's level, so that the challenge grows as she does
        (store_character_level, ":player_level", "trp_player"),

        (try_begin),
			# roll chance to gain some extra XP
			(store_random_in_range, ":rand", 0, 100),
			(lt, ":rand", chance_hero_party_gain_extra_xp),

			# treat NPCs has having +2 to their trainer level
			(store_skill_level, ":trainer_level", skl_trainer, ":troop_no"),
			(val_add, ":trainer_level", 2),

			# give NPCs an extra bonus trainer level per 4 player levels
			(val_div, ":player_level", 4),
			(val_add, ":trainer_level", ":player_level"),

			# distribute 500 XP per trainer level to the stack
			(store_mul, ":xp_gain", ":trainer_level", 500),
			(call_script, "script_cf_party_upgrade_with_xp", ":hero_party", ":xp_gain"),
        (try_end),
    (try_end),

    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", chance_garrison_gain_extra_xp),
        (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
        (neq, ":center_lord", "trp_player"),
		(party_get_battle_opponent, ":opponent", ":center_no"),
		(lt, ":opponent", 0),
        (call_script, "script_cf_party_upgrade_with_xp", ":center_no", 3000),
    (try_end),
   ]),
]
