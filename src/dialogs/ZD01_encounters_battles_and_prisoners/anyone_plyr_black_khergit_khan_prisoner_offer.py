DIALOGS = [
[anyone|plyr, "black_khergit_khan_talk", [
    (call_script, "script_sod_black_khergits_prepare_prisoner_purchase_offer"),
    (gt, "$g_sod_black_khergit_prisoner_buy_count", 0),
  ], "Some of those prisoners are not yours by right. Name a price for their ropes.", "black_khergit_khan_prisoner_offer", []],
]
