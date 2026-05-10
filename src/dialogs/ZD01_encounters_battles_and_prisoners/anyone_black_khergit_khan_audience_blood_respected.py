DIALOGS = [
[anyone, "black_khergit_khan_audience", [
    (store_relation, ":relation", "fac_player_supporters_faction", "fac_black_khergits"),
    (ge, ":relation", 100),
    (call_script, "script_sod_black_khergits_describe_status_to_s27"),
  ], "Temujin Black Sky rises when you enter the felt hall. 'Come in from the wind, blood-respected friend. The fire is yours, and no rider of mine will raise a bow against your banner.' {s27}", "black_khergit_khan_talk", []],
]
