MENUS = [
(
    "start_character_1", mnf_disable_all_keys,
    "As you left your burned homeland, you realized there was no returning. Calradia, with its petty and constant wars, lies before you. You have no doubt that these small kingdoms will be the next target of the Imperial Hound, Legate Gaius Marius. Without warning, Calradia may fall just as your beloved motherland did...",
    "none",
    [
      (set_background_mesh, "mesh_pic_chr2_faction"),

      (str_clear, s10),
      (str_clear, s11),
      (str_clear, s12),
      (str_clear, s13),
      (str_clear, s14),
      (str_clear, s15),
    ],
    [
      ("start_antares", [], "Ancient Empire of Antares.", [
        (assign, "$background_type", cb_antares),
        (assign, reg3, "$character_gender"),
        (str_store_string, s10, "@You came into the world as a {reg3?daughter:son} of Antarian nobility, heir to broad lands, many villages, and an ancient castle. You received the finest education and were trained from childhood for the rigors of aristocracy and life at court."),
        (jump_to_menu, "mnu_start_character_2"),
      ]),

      ("start_marina", [], "Wealthy Republic of Marina.", [
        (assign, "$background_type", cb_marina),
        (assign, reg3, "$character_gender"),
        (str_store_string, s10, "@You were born the {reg3?daughter:son} of a merchant. Your family was wealthy even by the standards of Marina. Your family banner was borne by merchants, warehouses, royal envoys, and shops across the country. A fleet of your ships traveled to the borders of the known world."),
        (jump_to_menu, "mnu_start_character_2"),
      ]),

      ("start_aden", [], "Proud Kingdom of Aden.", [
        (assign, "$background_type", cb_aden),
        (assign, reg3, "$character_gender"),
        (str_store_string, s10, "@As a child, you were under the sole supervision of your father, a gallant lord in service to the King of Aden. You spent your days training in the castle courtyard. You wanted to be just like him: strong, brave, and worthy of command."),
        (jump_to_menu, "mnu_start_character_2"),
      ]),

      ("start_villian", [], "Idyllic Duchy of Villian.", [
        (assign, "$background_type", cb_villian),
        (assign, reg3, "$character_gender"),
        (str_store_string, s11, "@{reg3?daughter:son}"),
        (str_store_string, s10, "@You were the {reg3?daughter:son} of a noble Villianese family. They spent their days on royal hunts and their nights at feasts."),
        (jump_to_menu, "mnu_start_character_2"),
      ]),

      ("start_zerrikanian", [], "Fearsome Zerrikanian Sultanate.", [
        (assign, "$background_type", cb_zerrikan),
        (assign, reg3, "$character_gender"),
        (str_store_string, s11, "@{reg3?daughter:son}"),
        (str_store_string, s10, "@You were a child of the steppe, born to a tribe of wandering nomads who lived in great camps throughout the arid grasslands of Zerrikania. Like the other tribesmen, your family revered horses above almost everything else, and they taught you how to ride almost before you learned how to walk."),
        (jump_to_menu, "mnu_start_character_2"),
      ]),

      ("go_back", [], "Go back",
       [(jump_to_menu, "mnu_start_game_1"),
      ]),
    ]
  ),
]
