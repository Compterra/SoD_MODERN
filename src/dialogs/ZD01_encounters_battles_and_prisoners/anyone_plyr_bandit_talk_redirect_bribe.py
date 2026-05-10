DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (store_troop_gold, ":gold", "trp_player"),
    (ge, ":gold", 600),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (this_or_next|eq, ":template", "pt_sod_merc_deserters"),
    (this_or_next|eq, ":template", "pt_deserters"),
    (this_or_next|eq, ":template", "pt_sod_deserters"),
    (this_or_next|eq, ":template", "pt_sod_merc_deserters"),
    (this_or_next|eq, ":template", "pt_mountain_bandits"),
    (this_or_next|eq, ":template", "pt_forest_bandits"),
    (eq, ":template", "pt_sea_raiders"),
], "Six hundred denars if you find another banner to trouble.", "hostile_redirect_bribe_offer", []],
]
