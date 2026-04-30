DIALOGS = [
[anyone, "merchant_quest_brief",
   [
     (eq, "$random_merchant_quest_no", "qst_deal_with_looters"),
     (try_begin),
       (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
       (str_store_string, s5, "@town"),
     (else_try),
       (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
       (str_store_string, s5, "@village"),
     (try_end),
     ],
   "We've had some fighting near the {s5} lately, with all the chaos that comes with it,\
 and that's led some of our less upstanding locals to try and make their fortune out of looting the shops and farms during the confusion.\
 A lot of valuable goods were taken. I need somebody to teach those bastards a lesson.\
 Sound like your kind of work?", "merchant_quest_looters_choice", []],
]
