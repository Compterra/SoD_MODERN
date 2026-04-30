DIALOGS = [
[anyone, "convince_friendship",
   [(store_add, ":min_relation", 5, "$convince_relation_penalty"),
    (ge, "$g_talk_troop_relation", ":min_relation")], "You've done well by me in the past, {playername},\
 and for that I will go along with your request, but know that I do not like you using our relationship this way.", "convince_friendship_verify", []],
]
