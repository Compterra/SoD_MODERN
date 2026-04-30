DIALOGS = [
[anyone, "lord_give_oath_go_on_2",
   [
     (assign, reg1, 1),
     (try_begin),
       (le, "$g_invite_offered_center", 0),
       (assign, reg1, 0),
     (else_try),
       (str_store_party_name, s1, "$g_invite_offered_center"),
     (try_end),
     ],
   "Let it be known that from this day forward, you are my sworn {man/follower} and vassal.\
 I give you my protection and grant you the right to bear arms in my name, and I pledge that I shall not deprive you of your life, liberty or properties except by the lawful judgment of your peers or by the law and custom of the land.{reg1? Furthermore I give you the fief of {s1} with all its rents and revenues.:}", "lord_give_oath_go_on_3", []],
]
