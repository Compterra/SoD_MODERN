DIALOGS = [
[anyone|plyr, "companion_objection_response", [
                    (eq, "$npc_praise_not_complaint", 0),
      ],  "Your objection is noted. Now fall back in line.", "close_window", [
                    (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_dismissed),
                    (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_morality_penalties),
                    (val_add, ":grievance", 10),
                    (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":grievance"),
          ]],
]
