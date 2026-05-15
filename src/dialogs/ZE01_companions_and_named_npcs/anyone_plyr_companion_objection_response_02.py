DIALOGS = [
[anyone|plyr, "companion_objection_response", [
                    (eq, "$npc_praise_not_complaint", 0),
      ], "You are heard. I will do better.", "close_window", [
                    (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_acknowledged),
                    (call_script, "script_sod_companion_shift_approval", "$map_talk_troop", 1),
          ]],
]
