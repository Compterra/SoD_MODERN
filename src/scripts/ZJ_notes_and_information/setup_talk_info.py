SCRIPTS = [
("setup_talk_info",
    [
      # Disabled for M&B 1.011 stability. The talk-info panel operations are
      # unsafe in map conversations and can hard-crash before dialog appears.
      (assign, reg0, reg0),
  ]),
]
