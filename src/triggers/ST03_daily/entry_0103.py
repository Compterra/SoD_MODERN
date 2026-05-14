SIMPLE_TRIGGERS = [
(24,
  [
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    (try_for_range, ":center_no", centers_begin, centers_end),
      (call_script, "script_sod_normalize_center_population", ":center_no"),
      (try_begin),
        (eq, reg0, 1),
        (eq, "$g_sod_debug", 1),
        (str_store_party_name_link, s3, ":center_no"),
        (display_message, "@Center simulation normalized at {s3}", debug_color),
      (try_end),
    (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]),
]
