DIALOGS = [
[anyone|plyr, "companion_objection_response", [
                    (eq, "$npc_praise_not_complaint", 0),
      ],  "Noted. Back to your post.", "close_window", [
                    (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_dismissed),
                    (call_script, "script_sod_companion_shift_approval", "$map_talk_troop", -2),
                    (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_morality_penalties),
                    (val_add, ":grievance", 10),
                    (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":grievance"),
          ]],
]
