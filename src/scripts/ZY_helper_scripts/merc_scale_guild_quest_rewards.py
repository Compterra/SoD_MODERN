# COST: trivial
SCRIPTS = [
("merc_scale_guild_quest_rewards",
 [
   (store_script_param_1, ":guild_faction"),
   (store_script_param_2, ":gold_reward"),
   (store_script_param, ":xp_reward", 3),
   (store_script_param, ":dont_give_again_period", 4),

   (call_script, "script_merc_get_guild_quest_tier", ":guild_faction"),
   (assign, ":tier", reg0),
   (store_relation, ":rel", ":guild_faction", "fac_player_faction"),

   (store_mul, ":tier_bonus", ":tier", 8),
   (store_div, ":relation_bonus", ":rel", 10),
   (val_max, ":relation_bonus", 0),
   (store_add, ":reward_factor", 100, ":tier_bonus"),
   (val_add, ":reward_factor", ":relation_bonus"),

   (val_mul, ":gold_reward", ":reward_factor"),
   (val_div, ":gold_reward", 100),
   (val_mul, ":xp_reward", ":reward_factor"),
   (val_div, ":xp_reward", 100),

   (try_begin),
     (gt, ":dont_give_again_period", 5),
     (store_div, ":cooldown_discount", ":rel", 15),
     (val_max, ":cooldown_discount", 0),
     (val_sub, ":dont_give_again_period", ":cooldown_discount"),
     (val_max, ":dont_give_again_period", 5),
   (try_end),

   (assign, reg0, ":gold_reward"),
   (assign, reg1, ":xp_reward"),
   (assign, reg2, ":dont_give_again_period"),
 ]),
]
