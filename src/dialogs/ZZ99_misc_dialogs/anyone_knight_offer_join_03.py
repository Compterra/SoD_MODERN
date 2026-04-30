DIALOGS = [
[anyone , "knight_offer_join", [
       (assign, ":num_player_companions", 0),
       (try_for_range, ":hero_id", heroes_begin, heroes_end),
         (troop_slot_eq, ":hero_id", slot_troop_occupation, slto_player_companion),
         (val_add, ":num_player_companions", 1),
       (try_end),
       (assign, reg5, ":num_player_companions"),
       (store_add, reg6, reg5, 1),
       (val_mul, reg6, reg6),
       (val_mul, reg6, 1000),
       (gt, reg6, 0)], #note that we abuse the value of reg6 in the next line.
 "I would be glad to fight at your side, my friend, but there is a problem...\
 The thing is, I've found myself in a bit of debt that I must repay very soon. {reg6} denars altogether,\
 and I am honour-bound to return every coin. Unless you've got {reg6} denars with you that you can spare,\
 I've to keep my mind on getting this weight off my neck.", "knight_offer_join_2", []],
]
