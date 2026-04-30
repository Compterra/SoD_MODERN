SCRIPTS = [
("get_damage_adjusted_for_type",
                    [
                      (store_script_param, ":damage", 1),
                      (store_script_param, ":type", 2),

                      #NOTE: this function must be adjusted if you mess with the soak & reduction factors in module.ini
                      # NOTE: I have no idea how to really generate these numbers - wtf does soak and reduction actually mean?
                      (try_begin),
                        (eq, ":type", idt_cut),
                        (assign, reg0, ":damage"),
                      (else_try),
                        (eq, ":type", idt_pierce),
                        (store_mul, reg0, ":damage", 130),
                        (val_div, reg0, 100),
                      (else_try),
                        (eq, ":type", idt_blunt),
                        (store_mul, reg0, ":damage", 135),
                        (val_div, reg0, 100),
                      (try_end),
                    ]
                  ),
]
