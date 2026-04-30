SCRIPTS = [
("get_prosperity_bracket",
        [
          (store_script_param, reg0, 1),
          (val_clamp, reg0, 0, 101),
          (val_div, reg0, 20),  # 0..10
        ]
      ),
]
