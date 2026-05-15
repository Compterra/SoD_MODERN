# COST: trivial
SCRIPTS = [
("sod_show_center_market_contact_portrait",
  [
    (store_script_param, ":center_no", 1),

    (assign, ":contact_troop", 0),
    (try_begin),
      (party_slot_ge, ":center_no", slot_town_merchant, 1),
      (party_get_slot, ":contact_troop", ":center_no", slot_town_merchant),
    (else_try),
      (party_slot_ge, ":center_no", slot_town_weaponsmith, 1),
      (party_get_slot, ":contact_troop", ":center_no", slot_town_weaponsmith),
    (else_try),
      (party_slot_ge, ":center_no", slot_town_armorer, 1),
      (party_get_slot, ":contact_troop", ":center_no", slot_town_armorer),
    (else_try),
      (party_slot_ge, ":center_no", slot_town_horse_merchant, 1),
      (party_get_slot, ":contact_troop", ":center_no", slot_town_horse_merchant),
    (else_try),
      (party_slot_ge, ":center_no", slot_town_elder, 1),
      (party_get_slot, ":contact_troop", ":center_no", slot_town_elder),
    (try_end),
    (call_script, "script_sod_show_troop_portrait", ":contact_troop"),
  ]),

("sod_show_guild_contact_portrait",
  [
    (store_script_param, ":guild_faction", 1),

    (try_begin),
      (is_between, ":guild_faction", guilds_begin, guilds_end),
      (faction_get_slot, ":contact_troop", ":guild_faction", slot_guild_representative),
      (try_begin),
        (neg|is_between, ":contact_troop", 0, "trp_last_troop"),
        (faction_get_slot, ":contact_troop", ":guild_faction", slot_guild_master),
      (try_end),
      (call_script, "script_sod_show_troop_portrait", ":contact_troop"),
    (try_end),
  ]),
]
