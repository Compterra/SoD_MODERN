try:
    from src.compiler import *
except:
    from src.module_system import *

from src.constants.module_constants import *


SIMPLE_TRIGGERS = [
(24 * 7,
    [
        (try_for_range, ":center_no", centers_begin, centers_end),
            (call_script, "script_update_center_population_supply", ":center_no"),
        (try_end),
    ]
  ),
]