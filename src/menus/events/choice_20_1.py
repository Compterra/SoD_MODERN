MENUS = [
(
    "event_20", mnf_disable_all_keys,
    "You overhear some fuss coming from your troops. Upon inquiry, some men inform you that a group of peasant women from {s1} have been caught while you were discussing with your advisors your next move. One of your men smiles warily at you and wonders if you would allow them to have some fun with the womem just to rise the troops' morale. You look at one of your advisors, who looks back at you and shrugs. You...",
    "none",
    [
    ],
    [
      ("choice_20_1", [], "Punish the soldiers who captured the women.", [
          (change_screen_return),
        ]
       ),
           ("choice_20_2", [], "Order your men to let the women go in peace.", [
          (change_screen_return),
        ]
       ),
           ("choice_20_3", [], "Decide to allow your men to do as they please.", [
          (change_screen_return),
        ]
       ),
           ("choice_20_4", [], "Order your men to kill women after they are finished toleave no traces.", [
          (change_screen_return),
        ]
       ),
      ]
  ),
]
