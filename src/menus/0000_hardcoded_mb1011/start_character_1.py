MENUS = [
(
    "start_character_1", mnf_disable_all_keys,
    "As you left your burned land you realized there is no returning. Calradia with it's petty constant wars lies before you. You have no doubt that this small kingdom will be the next target of the Imperial Hound, Legate Gaius Marius. And Calradia will fall just like your beloved motherland...",
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
        (str_store_string, s10, "@You came into the world a {reg3?daughter:son} of Antarian nobility, owning vast areas of land with many villages and an ancient castle. You received, the best education and were trained from childhood for the rigors of aristocracy and life at court."),
        (jump_to_menu, "mnu_start_character_2"),
      ]),

      ("start_marina", [], "Wealthy Republic of Marina.", [
        (assign, "$background_type", cb_marina),
        (assign, reg3, "$character_gender"),
        (str_store_string, s10, "@You were born the {reg3?daughter:son} of a merchant. Your family was insanely rich even for standards of Marina. Your family banner was borne by merchants, warehouses, royal envoys and shops all over the country. A fleet of your ships were travelling to the borders of the known world."),
        (jump_to_menu, "mnu_start_character_2"),
      ]),

      ("start_aden", [], "Proud Kingdom of Aden.", [
        (assign, "$background_type", cb_aden),
        (assign, reg3, "$character_gender"),
        (str_store_string, s10, "@As a child, you ware under the sole supervision of your father, a gallant Lord in service of King of Aden. You spent all your days training at the courtyard of the castle. You wanted to be just like him, strong and brave."),
        (jump_to_menu, "mnu_start_character_2"),
      ]),

      ("start_villian", [], "Idyllic Duchy of Villian.", [
        (assign, "$background_type", cb_villian),
        (assign, reg3, "$character_gender"),
        (str_store_string, s11, "@{reg3?daughter:son}"),
        (str_store_string, s10, "@You were the {reg3?daughter:son} of a noble Villianese family. They were spending whole days on royal hunts and nights at feasts."),
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
