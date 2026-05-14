DIALOGS = [
[anyone, "black_khergit_guard_about", [
    (store_random_in_range, ":guard_line", 0, 4),
    (try_begin),
      (eq, ":guard_line", 0),
      (str_store_string, s5, "@The Khan rests by the banked fire, as is his right. His riders do not. One more step toward the tents and you will learn how quietly a sleeping camp can kill."),
    (else_try),
      (eq, ":guard_line", 1),
      (str_store_string, s5, "@The Khan's fire is low and his horses are still. That is when fools mistake silence for weakness. We are the sound they hear last."),
    (else_try),
      (eq, ":guard_line", 2),
      (str_store_string, s5, "@The camp sleeps behind us. The dark belongs to the guards, the dogs, and the men who know better than to test either."),
    (else_try),
      (str_store_string, s5, "@By daylight the horde rides. By night the Khan rests, and we count every shadow that leans toward his tents. Choose where your shadow falls."),
    (try_end),
  ],
  "{s5}",
  "black_khergit_guard_talk", []],
]
