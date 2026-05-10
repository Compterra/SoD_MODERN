# COST: low
SCRIPTS = [
("cf_sod_party_is_hostile_economy_party",
 [
   (store_script_param, ":party_no", 1),
   (party_is_active, ":party_no"),
   (party_get_template_id, ":template", ":party_no"),
   (this_or_next|eq, ":template", "pt_bandits"),
   (this_or_next|eq, ":template", "pt_mountain_bandits"),
   (this_or_next|eq, ":template", "pt_forest_bandits"),
   (this_or_next|eq, ":template", "pt_steppe_bandits"),
   (this_or_next|eq, ":template", "pt_sea_raiders"),
   (this_or_next|eq, ":template", "pt_deserters"),
   (this_or_next|eq, ":template", "pt_sod_deserters"),
   (this_or_next|eq, ":template", "pt_sod_merc_deserters"),
   (this_or_next|eq, ":template", "pt_boar_clan_fighters"),
   (this_or_next|eq, ":template", "pt_boar_clan_fighters_desert"),
   (this_or_next|eq, ":template", "pt_black_khergit_raiders"),
   (this_or_next|eq, ":template", "pt_elephant_guard_ravaging_bandits"),
   (this_or_next|eq, ":template", "pt_conquistadors_ravaging_bandits"),
   (eq, ":template", "pt_serpent_host_ravaging_bandits"),
 ]),
]
