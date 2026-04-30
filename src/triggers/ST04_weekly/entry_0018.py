SIMPLE_TRIGGERS = [
    (24*7,
     [
        (try_for_range, ":center_no", centers_begin, centers_end),
            (call_script, "script_apply_weekly_building_effects", ":center_no"),
        (try_end,),
     ]),
]
