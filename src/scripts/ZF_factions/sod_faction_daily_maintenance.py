# COST: light
SCRIPTS = [
("sod_faction_daily_recalculate_strengths",
 [
   (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
     (call_script, "script_faction_recalculate_strength", ":faction_no"),
   (try_end),
 ]),
]
