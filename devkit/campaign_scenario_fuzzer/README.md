# Campaign Scenario Fuzzer

`campaign_scenario_fuzzer/` generates valid, bounded campaign-state inputs and
interprets a safe subset of literal source-script operations entirely in memory.
It is designed to find an impossible transition or missing guard before you
need an in-game “box of chocolates” test.

```powershell
py -3 -B devkit\campaign_scenario_fuzzer\campaign_scenario_fuzzer.py summary
py -3 -B devkit\campaign_scenario_fuzzer\campaign_scenario_fuzzer.py catalog
py -3 -B devkit\campaign_scenario_fuzzer\campaign_scenario_fuzzer.py fuzz black-khergit-camped-lock --iterations 100 --seed 42
```

The scenario catalog is checked in and reviewable. Unsupported native
operations, dynamic selectors, loops, missing scripts, recursion, and unknown
condition values produce **inconclusive**, not a fabricated pass. A failure
includes a deterministic seed, state, and operation trace.
