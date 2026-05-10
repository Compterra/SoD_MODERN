# COST: party-template counts
SCRIPTS = [
("sod_count_active_deserter_parties",
 [
   (store_num_parties_of_template, ":native_deserters", "pt_deserters"),
   (store_num_parties_of_template, ":sod_deserters", "pt_sod_deserters"),
   (store_num_parties_of_template, ":merc_deserters", "pt_sod_merc_deserters"),
   (store_add, ":total", ":native_deserters", ":sod_deserters"),
   (val_add, ":total", ":merc_deserters"),
   (assign, reg0, ":total"),
   (assign, reg1, ":native_deserters"),
   (assign, reg2, ":sod_deserters"),
   (assign, reg3, ":merc_deserters"),
 ]),
]
