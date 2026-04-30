DIALOGS = [
[anyone|plyr, "convince_options", [
  (this_or_next|eq, "$g_convince_quest", "qst_collect_debt"),
  (this_or_next|eq, "$g_convince_quest", "qst_conquistadors_collect_debt"),
  (this_or_next|eq, "$g_convince_quest", "qst_black_army_collect_debt"),
  (eq, "$g_convince_quest", "qst_slavers_collect_debt"),
  ], "I propose you a deal, we'll fight a duel. I win - you pay the debt, You win - I'll pay the debt instead of you. (Renown)", "convince_duel", []],
]
