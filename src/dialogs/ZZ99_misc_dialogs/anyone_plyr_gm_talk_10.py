DIALOGS = [
[anyone|plyr, "gm_talk", [
   (check_quest_active, "qst_elephant_guard_train_peasants_against_bandits"),
   (eq,"$g_talk_troop", elephant_guard_guild_master),
   ], "I am ready to train your warriors.", "gm_ready_to_fight", []],
]
