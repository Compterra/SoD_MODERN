DIALOGS = [
[anyone|plyr, "goods_merchant_talk", [],
   "What are the caravans saying about the roads?", "goods_merchant_trade_rumor",
   [(call_script, "script_get_closest_center", "p_main_party"),
    (assign, ":center_no", reg0),
    (call_script, "script_sod_trade_network_describe_center_identity_to_s23", ":center_no")]],
]
