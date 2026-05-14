DIALOGS = [
[trp_diego_companion, "diego_companion_chainbreaker",
  [
    (faction_get_slot, reg1, "fac_sod_merc_guild6", slot_faction_slaver_market_heat),
    (faction_get_slot, reg2, "fac_sod_merc_guild6", slot_faction_slaver_market_supply),
    (faction_get_slot, reg3, "fac_sod_merc_guild6", slot_faction_slaver_market_demand),
  ],
  "Their web has three strands: heat, supply, and demand. Right now I read heat at {reg1}, supply at {reg2}, demand at {reg3}. Free runaways, break caravans, and stop feeding their markets. Chains rust faster when no one profits by polishing them.",
  "diego_companion_talk",
  []],
]
