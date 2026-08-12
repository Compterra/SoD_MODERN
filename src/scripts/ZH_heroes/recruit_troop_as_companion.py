SCRIPTS = [
("recruit_troop_as_companion",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":recruitment_succeeded", 0),

      # Confirm the party mutation before any optional companion-system work.
      # Retinue setup can be deferred when the map-party pool is exhausted; that
      # must not turn a successfully recruited companion into a false failure.
      (try_begin),
        (is_between, ":troop_no", 0, "trp_last_troop"),
        (troop_is_hero, ":troop_no"),
        (party_force_add_members, "p_main_party", ":troop_no", 1),
        (main_party_has_troop, ":troop_no"),
        (assign, ":recruitment_succeeded", 1),
      (try_end),

      (try_begin),
        (eq, ":recruitment_succeeded", 1),
        (troop_set_slot, ":troop_no", slot_troop_occupation, slto_player_companion),
        (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
        (troop_set_auto_equip, ":troop_no", 0),
        (try_begin),
          (is_between, ":troop_no", companions_begin, companions_end),
          # These helpers are intentionally isolated from recruitment success.
          (try_begin),
            (call_script, "script_sod_companion_retinue_ensure_party", ":troop_no"),
          (try_end),
          (try_begin),
            (call_script, "script_sod_companion_retinue_update_warning_state", ":troop_no"),
          (try_end),
        (try_end),
        (store_character_level, ":current_level", ":troop_no"),
        (troop_set_slot, ":troop_no", slot_troop_level_up, ":current_level"),
        (str_store_troop_name, s68, ":troop_no"),
        (display_message, "@{s68} has joined your party.", bannana),
      (try_end),

      # Public result: 1 only after the hero is confirmed in the main party.
      # Invalid callers are intentionally silent in player-facing play.
      (assign, reg0, ":recruitment_succeeded"),
  ]),
]
