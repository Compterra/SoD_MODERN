DIALOGS = [
[anyone, "sod_nemesis_lord_memory", [
    (troop_get_slot, reg21, "$g_talk_troop", slot_troop_sod_nemesis_mercy_count),
    (troop_get_slot, reg22, "$g_talk_troop", slot_troop_sod_nemesis_capture_count),
    (troop_get_slot, reg23, "$g_talk_troop", slot_troop_sod_nemesis_humiliation_count),
    (val_add, reg22, reg23),
    (gt, reg21, reg22),
  ],
  "Your mercy is not forgotten. That is the trouble with it. A clean hatred is easy to carry; a debt carried beside it is heavier.", "lord_pretalk", []],
]
