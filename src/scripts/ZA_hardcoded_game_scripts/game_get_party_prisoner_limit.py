SCRIPTS = [
("game_get_party_prisoner_limit",
    [
#      (store_script_param_1, ":party_no"),
      (assign, ":troop_no", "trp_player"),
		#SoD Base 10
      (assign, ":limit", 10),
	  #SoD Law Now Leadership will be responsible for prisoners, prisoner managment is changed to Administration
      (store_skill_level, ":skill", "skl_leadership", ":troop_no"),
      #MORDACHAI - max prisoners = 7 x skill + leadership (was 5x + nothing)
	  #let's make it even 10
      (val_mul, ":skill", 10),
	  (val_add, ":limit", ":skill"),
      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
  ]),
]
