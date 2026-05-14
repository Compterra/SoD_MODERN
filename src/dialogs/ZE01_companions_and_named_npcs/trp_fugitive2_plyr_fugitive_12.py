DIALOGS = [
[trp_fugitive2|plyr, "fugitive_12", [
     (quest_get_slot, ":quest_target_dna", "$g_cur_fugitive_quest", slot_quest_target_dna),
     (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
     (str_store_string_reg, s4, s50),
      ], "I am looking for a thief by the name of {s4}. You fit his description.", "fugitive_22", []],
]
