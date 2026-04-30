DIALOGS = [
[anyone|plyr|repeat_for_100, "mayor_looters_quest_goods_response", [
      (store_repeat_object, ":goods"),
      (val_add, ":goods", trade_goods_begin),
      (is_between, ":goods", trade_goods_begin, trade_goods_end),
      (player_has_item, ":goods"),
      (str_store_item_name, s5, ":goods"),
  ],
   "{s5}.", "mayor_looters_quest_goods_2", [
      (store_repeat_object, ":goods"),
      (val_add, ":goods", trade_goods_begin),
      (troop_remove_items, "trp_player", ":goods", 1),
      (assign, ":value", reg0),
      (call_script, "script_troop_add_gold", "trp_player", ":value"),
      (quest_get_slot, ":gold_num", "qst_deal_with_looters", slot_quest_target_item),
      (val_sub, ":gold_num", ":value"),
      (quest_set_slot, "qst_deal_with_looters", slot_quest_target_item, ":gold_num"),
      (str_store_item_name, s6, ":goods"),
   ]],
]
