# Mercenary Economy Audit

## Purpose

This document audits every mercenary-adjacent system currently visible in the module source and frames the next refactor/overhaul discussion. The goal is not to flatten all mercenary content into one generic system. The goal is to understand which systems are meant to feel different, which systems accidentally overlap, and where money, debt, wages, relation, contracts, and party ownership should be centralized.

The strongest finding is that "mercenary economy" currently describes several distinct economies:

- Player-hired external mercenary companies.
- Player guild pacts.
- AI-hired mercenary companies.
- Mercenary lords and guild employer pacts.
- Player-as-mercenary service for a kingdom.
- Tavern mercenary hiring.
- Guild stock and upgrade permission.
- Mercenary-guild world activity and mini-faction pressure systems.
- Slaver, Boar Clan, Jotnar, Elephant Guard, Serpent Host, Black Army, and Conquistador special economies.
- Company accounts, weekly wages, and companion retinue costs that now intersect with mercenary troops and external parties.

These layers are flavorful, but their economic language is not always clear to the player, and their code paths are only partially centralized.

## Core Mercenary Identity

### Guild Factions

The main mercenary guild range is defined in `src/constants/module_constants.py`:

- `guilds_begin = "fac_sod_merc_guild1"`
- `guilds_end = "fac_kingdom_6_mercenaries"`

The seven visible guilds are initialized in `src/scripts/ZA_hardcoded_game_scripts/game_start.py`:

- `fac_sod_merc_guild1`: Black Army.
- `fac_sod_merc_guild2`: Conquistadors.
- `fac_sod_merc_guild3`: Elephant Guard.
- `fac_sod_merc_guild4`: Jotnar Clan.
- `fac_sod_merc_guild5`: Serpent Host.
- `fac_sod_merc_guild6`: Slavers.
- `fac_sod_merc_guild7`: Boar Clan.

Key faction slots:

- `slot_faction_merc_pact`
- `slot_guild_representative`
- `slot_guild_tier_1_unit_1`
- `slot_guild_tier_1_unit_2`
- `slot_guild_noble`
- `slot_guild_troop_proportion`
- `slot_guild_master`
- `slot_guild_base`
- `slot_faction_sod_mercs`
- `slot_faction_mercs_noble`
- `player_debt_to_faction`

### Party Types

Key mercenary party types:

- `spt_ai_mercenaries`
- `spt_player_mercenaries`
- `spt_merc_base`
- `spt_mercenary_lord_party`

Important party slots:

- `slot_party_merc_contract`
- `slot_party_merc_asked`
- `slot_party_orginal_faction`
- `slot_party_boss`
- `slot_party_commander_party`
- `slot_party_starting_base`
- `slot_party_starting_size`

The spelling `slot_party_orginal_faction` is legacy and should be preserved unless a compatibility alias is added.

## Current System Map

### 1. Player-Hired External Mercenary Companies

Primary files:

- `src/scripts/ZY_helper_scripts/merc_calculate_hire_quote.py`
- `src/scripts/ZY_helper_scripts/merc_build_preview_party.py`
- `src/scripts/ZY_helper_scripts/merc_calculate_party_contract_cost.py`
- `src/scripts/ZY_helper_scripts/merc_extend_party_contract.py`
- `src/scripts/ZC_parties/merc_party_change_state.py`
- `src/triggers/ST03_daily/entry_0118.py`
- `src/triggers/ST03_daily/entry_0122.py`
- `src/menus/kingdom/renew_contract1.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_gm_hire*.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_hire*.py`

Current behavior:

- The player hires an external party from a guild.
- Quote calculation creates a temporary preview party, builds the selected roster, sums `script_game_get_join_cost`, then applies:
  - company-size discount,
  - guild price factor,
  - relation price factor,
  - contract duration multiplier.
- The real party is spawned as `pt_player_mercenaries`.
- The party receives:
  - `slot_party_type = spt_player_mercenaries`,
  - `slot_party_boss = trp_player`,
  - `slot_party_orginal_faction = guild faction`,
  - `slot_party_merc_contract = contract end day`.
- Initial orders route through `script_sod_external_party_set_order`.
- Contract expiry is checked daily. When near expiry, the player gets a renewal menu. If the player declines, the party is marked with `slot_party_merc_asked = 1`; once expired it is handed off through `script_merc_party_change_state`.
- Daily reinforcement/upgrading also touches `spt_player_mercenaries` in `src/triggers/ST03_daily/entry_0122.py`.

Economic meaning:

- The up-front cost behaves like a contract purchase or retainer.
- The company is also included in broader weekly wage calculation through `script_calculate_player_faction_wage`.
- The company can replenish and upgrade over time, making it an ongoing military service rather than a static stack of hired troops.

Audit concern:

- The UI does not clearly say whether the up-front contract cost includes wages or only secures service.
- Because external player mercenaries are included in weekly wages, the player may perceive a double charge.
- If weekly wages are intended, the contract text should say "retainer plus field wages."
- If weekly wages are not intended, `calculate_player_faction_wage` needs to exclude `spt_player_mercenaries` or only charge a maintenance surcharge.

Recommended direction:

- Preserve contract parties as external follower parties.
- Define explicitly:
  - `hire quote = retainer + administrative contract fee`,
  - `weekly wage = field wage for active men`,
  - `renewal = retainer extension`.
- Add a status line that estimates weekly field wage during hire and renewal.

### 2. External Follower Party Command System

Primary files:

- `src/scripts/ZC_parties/sod_external_party_set_order.py`
- `src/scripts/ZC_parties/sod_external_party_describe_status_to_s20.py`
- `src/dialogs/ZA01_startup_and_dispatch/anyone_start_151.py`
- external command dialogue files in `src/dialogs/ZZ99_misc_dialogs/anyone_plyr_mate_chat_*`

Current behavior:

- Commandable external parties are limited to `spt_player_mercenaries` and `spt_player_patrol`.
- Orders update map AI and stored state slots.
- Mercenary status text includes strength and remaining contract days.

Audit concern:

- This layer is now cleaner than many older mercenary paths.
- It should remain the single command interface for external player-owned mercenary companies.
- Economic reporting is still outside this helper.

Recommended direction:

- Keep command logic separate from pricing.
- Add an economic status helper that computes:
  - days left,
  - estimated weekly wage,
  - retainer renewal estimate,
  - current replenishment state.

### 3. Guild Pacts

Primary files:

- `src/scripts/ZY_helper_scripts/merc_player_start_guild_pact.py`
- `src/scripts/ZY_helper_scripts/merc_player_end_guild_pact.py`
- `src/scripts/ZY_helper_scripts/merc_sync_player_guild_pact.py`
- `src/scripts/ZY_helper_scripts/merc_describe_pact_status.py`
- `src/menus/kingdom/mercenaries_weekly_payment.py`
- `src/triggers/ST04_weekly/entry_0126.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_pact_*.py`

Current behavior:

- A player guild pact stores the guild in `fac_player_faction` and `fac_player_supporters_faction`.
- Pact start resets debt and payment streaks.
- The weekly trigger opens `mnu_mercenaries_weekly_payment` if the player has a pact.
- Paying uses current weekly fee plus debt.
- Not paying adds that week's fee to `player_debt_to_faction`.
- Paid-in-a-row gives a discount up to 50 percent.
- Missed payments increase not-paid streak.
- Pact status reports trusted/stable/fragile language.

Economic meaning:

- Guild pacts are a subscription/support contract.
- They unlock or improve promotion, stock, discounts, support services, and passive benefits.
- Guild pact also affects `script_game_get_troop_wage` and `script_game_get_join_cost` for troops whose faction matches the pact.

Audit concerns:

- Debt consequences are scattered between weekly menu, dialogue entry, status text, and daily standing perks.
- The weekly AI employer loop in `ST04_weekly/entry_0126.py` iterates `guilds_begin` to `fac_sod_merc_guild6`, which means it covers the first five guilds only. This may be intentional because Slavers and Boar Clan have special world systems, but it should be explicit.
- Pact status text is flavorful but not very specific about mechanical consequences.
- The misspelled globals `$g_sod_merc_weekly_paiment_*` are legacy and should not be renamed casually.

Recommended direction:

- Centralize pact billing and debt into:
  - `script_sod_merc_guild_get_weekly_fee`
  - `script_sod_merc_guild_apply_payment`
  - `script_sod_merc_guild_apply_missed_payment`
  - `script_sod_merc_guild_describe_finances_to_sXX`
- Keep Slavers and Boar Clan special if intended, but document their exclusion from classic employer rotation.

### 4. Guild Stock, Promotions, and Tavern-Like Purchase Pools

Primary files:

- `src/scripts/ZH_heroes/add_merc_troops.py`
- `src/triggers/ST03_daily/entry_0119.py`
- `src/menus/camp/sod_upgrade_camp.py`
- `src/scripts/ZY_helper_scripts/merc_get_elite_relation_requirement.py`
- `src/scripts/ZY_helper_scripts/merc_get_guild_quest_tier.py`
- `src/scripts/ZY_helper_scripts/merc_describe_guild_progression.py`
- `src/menus/0000_hardcoded_mb1011/guilds_relations_report.py`

Current behavior:

- Guild troop pools refill daily.
- Pact with a guild increases stock limits and refill amounts.
- Upgrade permission is lost if relation falls below 10.
- Progression report describes promotion, elite access, special service, trusted favor, active pact, active company, and quest tier.

Economic meaning:

- Relationship controls access.
- Pact improves availability and pricing.
- Guild stock is a local supply economy, separate from contract companies.

Audit concerns:

- Guild stock, contract company creation, and daily player-company reinforcement use similar roster data but separate code.
- Promotion permission and elite access are relation-based, but the player-facing economy report does not fully explain how that affects costs and wages.

Recommended direction:

- Centralize roster and access rules:
  - `script_sod_merc_guild_get_roster`
  - `script_sod_merc_guild_get_access_level`
  - `script_sod_merc_guild_get_stock_limits`

### 5. AI-Hired Mercenary Companies

Primary files:

- `src/scripts/ZI_campaign_ai/ai_hire_mercenaries.py`
- `src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py`
- `src/scripts/ZC_parties/merc_party_change_state.py`
- `src/triggers/ST03_daily/entry_0120.py`
- `src/triggers/ST03_daily/entry_0122.py`

Current behavior:

- Lords can hire AI mercenary companies when they have enough wealth, enough party size, and free mercenary slots.
- Rulers can maintain more mercenary companies than ordinary lords.
- Cost is roughly `size * 10`.
- AI merc companies are spawned from guild rosters and escort the hiring lord.
- Contract expires after roughly 30 days.
- Expired AI mercs try to renew with current boss, transfer to another lord of the same faction, return to their base as commoners, or become unassigned.
- AI mercenary companies also get daily replenishment and upgrades.

Economic meaning:

- AI mercs convert lord wealth into temporary force projection.
- Their presence contributes to faction power.

Audit concerns:

- AI hire cost is not using the same cost model as player hire quote or renewal.
- AI renewal cost uses size-based rough logic in `merc_party_change_state`.
- AI companies can be rehomed intelligently, but financial logic is local to the party lifecycle script.

Recommended direction:

- Use a shared quote/maintenance formula with AI-specific multipliers:
  - AI should probably receive a discount or strategic subsidy, but it should be explicit.
- Separate "party ownership transition" from "can afford renewal."

### 6. Mercenary Lords

Primary files:

- `src/triggers/ST03_daily/entry_0129.py`
- `src/dialogs/ZB01_lords_politics_and_family/anyone_merc_lord_*.py`
- `src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_mercenary_lord_party_start.py`
- `src/scripts/ZC_parties/sod_sanitize_unique_hero_party_stacks.py`
- `src/scripts/ZY_helper_scripts/sod_campaign_party_sanity.py`

Current behavior:

- Mercenary lords spawn daily when valid.
- Slaver mercenary lords behave specially, using a random town and guild faction.
- Other mercenary lords look for an employer whose faction pact matches their guild.
- Spawned parties use guild roster slots and are upgraded repeatedly.
- They patrol around employer/base and use special party type `spt_mercenary_lord_party`.

Economic meaning:

- A faction's guild pact can project named mercenary commanders onto the map.
- Mercenary lords are not just purchased troops; they are a strategic consequence of guild employment.

Audit concerns:

- Employer resolution and spawn rules are separate from the guild pact billing system.
- The player sees pact payments, but the exact connection to mercenary lord activity is not obvious.

Recommended direction:

- Tie pact report text to actual active mercenary lords.
- Consider a helper:
  - `script_sod_merc_guild_count_active_support_parties`
  - `script_sod_merc_guild_describe_active_support`

### 7. Player-As-Kingdom-Mercenary Service

Primary files:

- `src/scripts/ZY_helper_scripts/merc_begin_service.py`
- `src/scripts/ZY_helper_scripts/merc_accrue_service_pay.py`
- `src/scripts/ZY_helper_scripts/merc_collect_service_pay.py`
- `src/scripts/ZY_helper_scripts/merc_describe_contract_board.py`
- `src/triggers/ST02_every_hour/entry_0010.py`
- `src/triggers/ST03_daily/entry_0011.py`
- `src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mercenary_service*.py`
- `src/dialogs/ZB01_lords_politics_and_family/anyone_lord_pay_mercenary.py`
- `src/menus/0000_hardcoded_mb1011/character_report.py`
- `src/menus/0000_hardcoded_mb1011/party_size_report.py`

Current behavior:

- Player signs with a kingdom as a mercenary.
- Receives signing bonus.
- Accrues pay every seven days based on main-party strength.
- Can collect accumulated pay from a lord.
- Renewal/departure is handled through a native-style oath fulfilled flow.

Economic meaning:

- The player is selling their company as a service.
- This is separate from hiring mercenaries from guilds.

Audit concerns:

- The same word "mercenary contract" is used for both:
  - player working for a kingdom,
  - player hiring an external guild company,
  - guild pact subscription.
- Report text should clearly distinguish "your service contract" from "guild company contract" and "guild pact."

Recommended direction:

- Rename report language, not necessarily code:
  - "Kingdom service contract"
  - "Hired company contract"
  - "Guild pact"

### 8. Tavern Mercenaries and Mercenary Pools

Primary files:

- `src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_mercenary_tavern_talk_hire.py`
- `src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_mercenary_tavern_talk*.py`
- `src/scripts/ZH_heroes/add_merc_troops.py`

Current behavior:

- Town/tavern mercenary stacks are bought directly into `p_main_party`.
- Cost is `script_game_get_join_cost * troop count`.
- The center's mercenary pool is cleared after hiring.
- Town population can be reduced when hiring from a town.

Economic meaning:

- This is classic direct recruitment, not a contract.

Audit concerns:

- This flow respects normal party capacity but does not know about companion retinues or external company alternatives.
- It shares `game_get_join_cost` discounts with guild pact troop faction logic.

Recommended direction:

- Keep as direct recruitment.
- Add optional future retinue-aware prompt: if player lacks personal capacity but companions can take troops, route to retinue transfer flow.

### 9. Weekly Wages, Company Accounts, and Retinues

Primary files:

- `src/scripts/ZB_economy_and_trade/calculate_player_faction_wage.py`
- `src/scripts/ZA_hardcoded_game_scripts/game_get_troop_wage.py`
- `src/menus/0000_hardcoded_mb1011/pay_day.py`
- `src/scripts/ZY_helper_scripts/sod_company_accounts.py`
- `src/menus/camp/company_accounts.py`
- `src/scripts/ZC_parties/sod_companion_retinues.py`

Current behavior:

- `script_calculate_player_faction_wage` includes:
  - main party,
  - owned garrisons,
  - companion retinues,
  - player mercenary external parties,
  - player patrol external parties.
- External player mercenaries not attached to a town appear to cost 150 percent normal wage.
- Attached/resting external parties appear to cost reduced wages.
- Companion retinue wages are calculated through retinue-specific helpers and then integrated into payday.
- Guild pact discounts reduce wages for matching mercenary-guild troops.

Economic meaning:

- Mercenary troops cost more by default.
- Guild pact can make a specific mercenary culture cheaper.
- External companies have ongoing wage pressure.

Audit concerns:

- This is the biggest clarity issue: hired external mercenary companies can have an up-front contract cost and still appear in wages.
- Player-facing reports should identify "external mercenary field wages" separately from ordinary party wages and companion command costs.

Recommended direction:

- Add wage breakdown helpers:
  - `script_sod_calculate_player_personal_party_wage`
  - `script_sod_calculate_external_party_wage`
  - `script_sod_calculate_companion_retinue_wage`
  - `script_sod_calculate_garrison_wage`
  - `script_sod_calculate_total_company_wage`
- Keep the final payday compatible but make details auditable.

### 10. Mini-Faction World Activity

Primary files:

- `src/scripts/ZY_helper_scripts/sod_black_army_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_conquistador_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_elephant_guard_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_jotnar_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_serpent_host_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_slavers_black_market.py`
- `src/scripts/ZY_helper_scripts/sod_boar_clan_world_presence.py`
- `src/scripts/ZY_helper_scripts/sod_boar_clan_encounter.py`
- `src/menus/reports/mercenary_world_activity_report.py`
- guild-specific report menus under `src/menus/reports/`

Current behavior:

- Each guild has its own pressure/resource model:
  - Black Army: security fund/contract heat.
  - Conquistadors: supplies/requisition heat.
  - Elephant Guard: devotion/supplies/omens/slaver alarm.
  - Jotnar: hearth pressure/slaver pressure.
  - Serpent Host: route pressure/intelligence/safe passage.
  - Slavers: demand/supply/heat/bases/transports.
  - Boar Clan: frontier pressure/tribute/intimidation.
- These systems spawn world parties, update reports, and interact with local economy or threats.

Economic meaning:

- These are not just mercenary shops. They are semi-autonomous economies and regional pressure systems.

Audit concerns:

- World activity has rich identity, but it is only loosely connected to the classic guild pact economy.
- The world activity report is good, but player contract reports should cross-reference the practical effects of guild standing and pact support.

Recommended direction:

- Do not centralize these into one bland system.
- Centralize only shared financial primitives:
  - standing,
  - debt,
  - service price,
  - party support count,
  - report phrasing.

### 11. Mercenary Deserters and Hostile Economy Parties

Primary files:

- `src/scripts/ZZ_common_array_processing/spawn_bandits.py`
- `src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_sod_merc_deserters_start*.py`
- `src/scripts/ZY_helper_scripts/cf_sod_party_is_hostile_economy_party.py`
- `src/scripts/ZY_helper_scripts/sod_apply_hostile_noncombat_economy_effects.py`
- `src/scripts/ZY_helper_scripts/sod_store_hostile_economy_report.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_get_archetype.py`

Current behavior:

- Mercenary deserters spawn around mercenary guild bases.
- They are treated as hostile economy parties and may interact with threat board/economy reporting.

Economic meaning:

- Mercenary systems produce instability as well as services.

Audit concerns:

- Deserters are part of the mercenary economy thematically, but should not be commandable, hirable as external followers, or counted as player mercenary assets.

Recommended direction:

- Keep hostile mercenary/deserter templates explicitly excluded from player external-party command systems.
- Add static coverage if refactoring mercenary party categorization.

## Cross-System Findings

### Finding 1: Contract Language Is Ambiguous

The word "contract" currently covers too many things:

- The player serving a kingdom as a mercenary.
- The player hiring a guild company.
- The player maintaining a guild pact.
- AI lords hiring mercenary companies.

Recommendation:

- Use player-facing terms consistently:
  - `Kingdom service`
  - `Hired company`
  - `Guild pact`
  - `AI company contract`
  - `Guild support party`

### Finding 2: Up-Front Company Cost And Weekly Wages Need a Design Decision

External player mercenary companies are contract-priced and wage-counted.

This can be valid if the design says:

- up-front cost buys guild commitment, replenishment, and contract administration;
- weekly wages pay the actual field soldiers.

It feels questionable if the player believes the up-front cost fully pays the company.

Recommendation:

- Keep both costs, but clarify the economic fiction and show estimated weekly wage before hire/renewal.
- If we later decide up-front cost includes wages, remove or reduce weekly wages for `spt_player_mercenaries`.

### Finding 3: Pricing Is Not Centralized

Current pricing sources include:

- `script_game_get_join_cost`
- `script_game_get_troop_wage`
- `script_merc_calculate_hire_quote`
- `script_merc_calculate_party_contract_cost`
- `script_merc_apply_master_service`
- AI hire math in `script_ai_hire_mercenaries`
- AI renewal checks in `script_merc_party_change_state`
- pact fee globals and weekly menu math

Recommendation:

- Centralize pricing behind a small set of helpers while preserving special multipliers.

### Finding 4: AI And Player Hire Formulas Differ

Player hire cost is roster-based and relation-sensitive.
AI hire cost is rough size-based.

Recommendation:

- Use one shared base formula with caller-specific modifiers.
- Keep AI cheap enough to function, but make that a stated subsidy or simplification.

### Finding 5: Guilds 6 And 7 Are Special But Not Always Documented As Special

Slavers and Boar Clan have several special systems and are excluded from some older loops.

Examples:

- The classic weekly employer reassignment loop uses `guilds_begin` to `fac_sod_merc_guild6`, which effectively covers guilds 1-5.
- Slavers and Boar Clan have separate world activity/encounter systems.

Recommendation:

- Add named ranges or helper predicates:
  - `script_cf_sod_merc_guild_uses_classic_employer_rotation`
  - `script_cf_sod_merc_guild_uses_world_presence`
- Avoid magic range endings for guild identity.

### Finding 6: Reports Are Improving But Still Split

Relevant reports:

- Character report uses `script_merc_describe_report_summary`.
- Contract board uses `script_merc_describe_contract_board`.
- Guild relation report uses `script_merc_describe_guild_progression`.
- World activity report summarizes mini-faction pressure.
- Company accounts/payday reports show wages and command costs.

Recommendation:

- Add one "Mercenary Ledger" helper that all reports can draw from:
  - active hired company summary,
  - pact weekly fee/debt,
  - estimated external company wages,
  - active support parties,
  - kingdom service pay owed,
  - relation unlocks.

## Refactor Candidate Architecture

### Preserve As Separate Systems

Do not merge these into one generic path:

- Guild world-activity identities.
- Player-as-kingdom-mercenary service.
- Tavern mercenary hiring.
- External follower command system.
- AI mercenary hiring.
- Mercenary lord strategic presence.

### Centralize Shared Primitives

Good candidates for centralization:

- Guild identity and roster lookup.
- Guild access level.
- Guild standing and unlocks.
- Guild pact fee/debt handling.
- Hired company quote and renewal cost.
- External company wage estimate.
- Active mercenary support count.
- Mercenary report text.

### Proposed Helper Layer

Potential new scripts:

- `script_sod_merc_guild_get_profile(guild)`
  - returns base, master, representative, units, noble, price factor, elite requirement.
- `script_sod_merc_guild_get_access_level(guild)`
  - returns outsider/promote/elite/service/trusted.
- `script_sod_merc_guild_get_roster(guild)`
  - returns tier unit 1, tier unit 2, noble, proportion.
- `script_sod_merc_guild_calculate_company_quote(guild, size, mix, training, term, buyer_mode)`
  - single quote function for player and AI.
- `script_sod_merc_company_calculate_weekly_wage(party)`
  - estimated external-party field wage.
- `script_sod_merc_guild_apply_pact_payment(guild, payment_mode)`
  - full pay, missed pay, favor, debt relief.
- `script_sod_merc_guild_describe_ledger_to_sXX(guild)`
  - compact report text for menus/dialogue.
- `script_cf_sod_party_is_player_hired_merc_company(party)`
  - safer than repeating slot checks.
- `script_cf_sod_party_is_ai_hired_merc_company(party)`
  - safer than repeating slot checks.
- `script_cf_sod_merc_guild_uses_classic_employer_rotation(guild)`
  - documents guild 1-5 behavior.

## Overhaul Options

### Option A: Polish Without Economic Rebalance

Lowest risk.

- Keep all costs and wages.
- Improve text and reporting.
- Add static tests for current intended double-layer payment.
- Add helper wrappers around existing formulas without changing values.

Best if the goal is clarity and robustness.

### Option B: Retainer Plus Wage Model

Moderate risk, likely best long-term.

- Define up-front contract fee as retainer/replenishment/admin cost.
- Keep weekly wages.
- Add explicit replenishment value to contracts.
- Show estimated weekly wage before hire and renewal.
- Let relation/pact reduce retainer and/or wages.

Best if external companies should feel like professional military services.

### Option C: All-Inclusive Contract Model

Higher balance risk.

- Up-front price includes wages.
- Remove or sharply reduce weekly wage burden for `spt_player_mercenaries`.
- Increase renewal costs.
- Rebalance daily replenishment so the player cannot buy underpriced self-healing armies.

Best if the player should not micromanage or pay ongoing company wages.

### Option D: Full Guild Economy Overhaul

Highest risk.

- Guilds have stock, revenue, debt, reputation, active contracts, and support capacity.
- Player pacts consume support capacity.
- AI kingdoms compete for guild contracts.
- World activity affects price and availability.

Best as a later campaign-economy feature, not a first refactor.

## Recommended Refactor Path

### Phase 1: Documentation And Static Safety

- Add static tests for:
  - external player mercenaries being included in weekly wages, if intended;
  - guild pact discount affecting wage and join cost;
  - guild 1-5 classic employer rotation being explicit;
  - Slaver/Boar special handling;
  - player hire and renewal routes using known helpers.

### Phase 2: Reporting And Language

- Update hire quote dialogue to mention retainer plus field wages.
- Update renewal menu with estimated weekly wages.
- Update character/report text to distinguish:
  - kingdom service contract,
  - hired company contract,
  - guild pact,
  - external party wages.

### Phase 3: Helper Centralization

- Add guild profile/access helpers.
- Wrap quote and renewal formulas.
- Keep old outputs numerically compatible at first.

### Phase 4: Economy Decision

Choose between:

- retainer plus wages, or
- all-inclusive contracts.

Do not rebalance before the UI clearly tells the player what is happening.

### Phase 5: AI And Guild World Integration

- Put AI hire/renewal through the same quote layer.
- Add explicit classic/special guild predicates.
- Show active support party counts in pact reports.

## Immediate Improvement Candidates

Small safe changes to consider before any overhaul:

- Add estimated weekly field wage to hired company quote.
- Add estimated weekly field wage to renewal menu.
- Rename report language from generic "contract" to specific service type.
- Add a Mercenary Ledger report/helper.
- Add static tests around `spt_player_mercenaries` wage inclusion.
- Add helper predicate for classic employer guilds instead of `guilds_begin` to `fac_sod_merc_guild6`.
- Clarify Slaver and Boar Clan special-case behavior in code comments and reports.

## Final Assessment

The mercenary economy is thematically strong but structurally layered. It has grown from a classic mercenary-guild system into a much broader ecosystem: guild bases, pacts, hired companies, AI contracts, mercenary lords, world activity, hostile deserters, slaver markets, Boar tolls, and campaign reports.

The system should not be flattened. The best next step is to centralize only the shared economic rules while preserving guild identity and world behavior. The first overhaul should be a clarity pass: make the player understand exactly what they are buying, what they still owe, what wages are ongoing, and what their relationship with each guild changes.
