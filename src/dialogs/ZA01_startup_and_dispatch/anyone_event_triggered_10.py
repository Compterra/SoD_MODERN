DIALOGS = [
[anyone, "event_triggered", [
    (eq, "$talk_context", tc_rebel_thanks),
    (troop_get_slot, ":old_faction", "$g_talk_troop", slot_troop_original_faction),
    (str_store_faction_name, s3, ":old_faction"),
    (str_store_string, s6, "@{playername}, when we started our long walk, few people had the courage to support me.\
 And fewer still would be willing to put their lives at risk for my cause.\
 But you didn't hesitate for a moment in throwing yourself at my enemies.\
 We have gone through a lot together, and there were times I came close to losing all hope.\
 But with God's help, we prevailed. It is now time for me to leave your company and take what's rightfully mine.\
 From now on, I will carry out the great responsibility of ruling {s3}.\
 There still lie many challanges ahead and I count on your help in overcoming those.\
 And of course, you will always remain as my foremost vassal."),
    ],
   "{s6}", "rebel_thanks_answer",
   [
     (call_script, "script_end_quest", "qst_rebel_against_kingdom"),
       ]],
]
