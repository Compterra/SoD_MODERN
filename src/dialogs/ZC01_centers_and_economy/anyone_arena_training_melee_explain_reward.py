DIALOGS = [
[anyone, "arena_training_melee_explain_reward", [
      (assign, reg1, arena_tier1_opponents_to_beat), (assign, reg11, arena_tier1_prize),
      (assign, reg2, arena_tier2_opponents_to_beat), (assign, reg12, arena_tier2_prize),
      (assign, reg3, arena_tier3_opponents_to_beat), (assign, reg13, arena_tier3_prize),
      (assign, reg4, arena_tier4_opponents_to_beat), (assign, reg14, arena_tier4_prize),
      (assign, reg15, arena_grand_prize)
      ], "Some of the wealthy townsmen offer prizes for those fighters who show great skill in the fights.\
 If you can beat {reg1} opponents before going down, you'll earn {reg11} denars. You'll get {reg12} denars for striking down at least {reg2} opponents,\
 {reg13} denars if you can defeat {reg3} opponents, and {reg14} denars if you can survive long enough to beat {reg4} opponents.\
 If you can manage to be the last {man/fighter} standing, you'll earn the great prize of the fights, {reg15} denars. Sounds good, eh?", "arena_master_melee_pretalk", []],
]
