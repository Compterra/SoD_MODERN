DIALOGS = [
[anyone|plyr, "companion_objection_response", [
                    (eq, "$npc_praise_not_complaint", 1),
      ], "Thank you. I will remember it.", "close_window", [
                    (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_acknowledged),
                    (call_script, "script_sod_companion_shift_approval", "$map_talk_troop", 1),
          ]],
]
