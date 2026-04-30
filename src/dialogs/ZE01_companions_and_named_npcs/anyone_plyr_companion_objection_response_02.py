DIALOGS = [
[anyone|plyr, "companion_objection_response", [
                    (eq, "$npc_praise_not_complaint", 0),
      ], "Hopefully it won't happen again.", "close_window", [
                    (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_acknowledged),
          ]],
]
