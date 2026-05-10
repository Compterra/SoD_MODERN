DIALOGS = [
[anyone, "deserter_lord_intel", [
    (call_script, "script_sod_store_deserter_lord_intel"),
    (eq, reg0, 1),
], "We saw {s6}'s banners not far from here, maybe {reg1} miles by road. Enough steel to make hungry men keep low.", "deserter_talk", [
    (call_script, "script_sod_note_hostile_reputation", 4),
]],
]
