SCRIPTS = [
("init_auto_loot",
                    [
                      # we pass this in so that we can distinguish creating a new game vs. updating an old one
                      (store_script_param, ":game_start", 1),
                      (assign, reg0, ":game_start"), # avoid unused variable error

                      (try_begin),
                        # only do the initialization if it hasn't been done for this version of autoloot yet
                        (lt, "$g_auto_loot_version", auto_loot_version),
                        # reinitialize autoloot if we've installed a newer version of it (update a saved game automatically)
                        # NOTE: if the system changes radically enough - we'll need to clear out the old troop slots and ask the player to reassign them from scratch

                        # initialize the difficulty slots
                        (call_script, "script_init_item_difficulties"),

                        # initialize additional item slots
                        (call_script, "script_init_item_base_score"),

                        # initialize the imod slot data
                        (call_script, "script_init_imod_effects"),

                        # record the version of autoloot that we've initialized for
                        (assign, "$g_auto_loot_version", auto_loot_version),
                      (try_end),
                    ]
                  ),
]
