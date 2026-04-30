SCRIPTS = [
("healthbars",
                      [
                        (assign, reg1, "$allies_coh_base"),
                        (assign, reg2, "$enemies_coh"),
                        (assign, reg3, "$new_kills"),
                        (display_message, "@Your troops are at {reg1}% cohesion (+{reg3}% bonus), the enemy at {reg2}%!", 0x6495ed),
                      ]
                    ),
]
