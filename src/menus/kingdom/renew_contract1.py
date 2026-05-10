MENUS = [
(
    "contract_fulfilled",0,
    "You had a contract with mercenaries to hire them for a certain duration.\
 That contract is about to expire in a few days. What will you do?\
 Mercenary strength: {s49}^^Company profile: {s50}^Replacement pace: {s51}^Base pricing: {s52}^Standing modifier: {s53}^Trusted favor: {s54}^Standing perk: {s56}",
    "none",
    [
      (try_begin),
        (lt, "$temp_size", 20),
        (str_store_string, s49, "@small company"),
      (else_try),
        (lt, "$temp_size", 50),
        (str_store_string, s49, "@respectable company"),
      (else_try),
        (lt, "$temp_size", 90),
        (str_store_string, s49, "@large company"),
      (else_try),
        (str_store_string, s49, "@major field force"),
      (try_end),
      (party_get_slot, ":guild_faction", "$temp_party", slot_party_orginal_faction),
      (call_script, "script_merc_describe_guild_offer", ":guild_faction"),
      (call_script, "script_merc_describe_guild_favor", ":guild_faction"),
      (call_script, "script_merc_describe_standing_report", ":guild_faction"),
      (call_script, "script_merc_calculate_party_contract_cost", "$temp_party", 1),
      (assign, "$merc_cost", reg0),
     ],
    [
      ("renew_contract1",[
	     (assign, reg21, "$merc_cost"),
		 (store_troop_gold, ":gold", "trp_player"),
		 (ge, ":gold", reg21),
	  ], "Renew your contract with that party for another month.({reg21} denars)",
       [
	     (call_script, "script_sod_player_charge_gold", reg21),
         (call_script, "script_merc_extend_party_contract", "$temp_party", 1),
         (change_screen_return),
         ]),
		 
	   ("renew_contract2",[
	     (call_script, "script_merc_calculate_party_contract_cost", "$temp_party", 3),
		 (assign, reg22, reg0),
		 (store_troop_gold, ":gold", "trp_player"),
		 (ge, ":gold", reg22),
	  ], "Renew your contract with that party for another three months.({reg22} denars)",
       [
	     (call_script, "script_sod_player_charge_gold", reg22),
         (call_script, "script_merc_extend_party_contract", "$temp_party", 3),
         (change_screen_return),
         ]),
		 
      ("renew_contract3",[
	     (call_script, "script_merc_calculate_party_contract_cost", "$temp_party", 6),
		 (assign, reg23, reg0),
		 (store_troop_gold, ":gold", "trp_player"),
		 (ge, ":gold", reg23),
	  ], "Renew your contract with that party for another six months.({reg23} denars)",
       [
	     (call_script, "script_sod_player_charge_gold", reg23),
         (call_script, "script_merc_extend_party_contract", "$temp_party", 6),
         (change_screen_return),
         ]),
      ("trusted_favor",[
         (party_get_slot, ":guild_faction", "$temp_party", slot_party_orginal_faction),
         (gt, ":guild_faction", 0),
         (store_relation, ":rel", ":guild_faction", "fac_player_faction"),
         (ge, ":rel", 40),
      ], "Call in a trusted-partner favor for one month. (-5 relation)",
       [
         (call_script, "script_merc_apply_contract_favor", "$temp_party"),
         (change_screen_return),
       ]),
      ("dont_renew_contract",[
	  ],"Don't renew contract with this party.",
       [
	    (party_set_slot, "$temp_party", slot_party_merc_asked, 1),
		(change_screen_return),
	   ]),
    ]
  ),
]
