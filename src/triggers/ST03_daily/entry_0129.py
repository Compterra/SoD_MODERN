SIMPLE_TRIGGERS = [
(48,
    [
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (call_script, "script_sod_merc_lord_try_spawn_for_troop", ":troop_no"),
      (try_end),
      (call_script, "script_sod_merc_guild_repair_ledgers"),
      (eq, "$g_sod_debug", 1),
      (display_message, "@Mercenary lord market pass complete.", debug_color),
    ]),
]
