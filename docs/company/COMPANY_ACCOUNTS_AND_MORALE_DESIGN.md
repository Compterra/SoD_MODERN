# Company Accounts, Rations, and Troop Loyalty Checklist

## Goal

Replace automatic payday with a player-driven company management system where wages, rations, morale, troop identity, promises, peaceful desertion, and violent mutiny all interconnect. The player should feel like a commander responsible for people with different expectations, not a party owner paying a flat timer.

The system should be dialogue-forward. Slighted troops should complain, petition, negotiate, threaten to leave, or peacefully desert before violence. In the worst cases, a faction inside the party can decide the player has broken faith and try to seize pay, food, prisoners, or valuables by force.

Related NPC/lord extension: `docs/reports/npc_lord_morale_rout_enhancement_checklist.md` tracks a lightweight lord-party morale and battle rout enhancement plan. The player company system should stay detailed; NPC lords should use a compressed strategic morale model that affects battle willingness and starting battle cohesion.

## Design Rules

- [x] Payday is no longer an automatic weekly interruption.
- [x] Wages accrue as an obligation until the player settles accounts.
- [x] Troop classes respond differently to pay, food, honor, faith, discipline, and promises at the pressure-selection/reporting layer.
- [x] Dialogue is the primary surface for complaints, petitions, desertions, and mutiny warnings in the camp-report/menu foundation.
- [x] Company account menus now surface early petition pressure before desertion or mutiny.
- [x] Peaceful desertion is common before violent rebellion.
- [x] Violent mutiny requires sustained grievance, low confidence, and a believable leader or troop bloc at the warning/resolution layer.
- [x] Hero NPCs, mercenaries, noble/faith troops, and enlisted troops each have distinct expectations in the company-account foundation.
- [x] Hero NPCs, mercenaries, noble/faith troops, and enlisted troops each have distinct morale scores surfaced in the company report and fed into battle cohesion.
- [x] Ration quality matters as much as coin for day-to-day morale.
- [x] Generosity can build loyalty, but cannot permanently hide starvation, unpaid arrears, or cruelty.
- [x] Companions should witness and comment on company-account choices.
- [x] The system should integrate with existing morale, companion approval, troop wages, food consumption, and camp reports.
- [x] Company-account morale feeds in-battle morale and routing context.
- [x] In-battle morale now uses troop-category morale for companions, mercenaries, noble troops, faith troops, and enlisted troops.
- [x] The player must be able to inspect the current situation before making a decision.
- [x] No new scenes are required for v1.

## Current System Baseline

- [x] Player troop wages are calculated through `script_calculate_player_faction_wage`.
- [x] Individual wage cost comes from `script_game_get_troop_wage`.
- [x] Wages are sampled every 12 hours through `ST02_every_hour/entry_0133.py`.
- [x] Payday currently fires after 14 half-day samples.
- [x] Payday currently uses `mnu_pay_day`.
- [x] Unpaid wages become `$g_player_debt_to_party_members`.
- [x] Existing debt already reduces morale.
- [x] Existing unpaid-wage hooks already notify companion systems.

## New Core State

### Global Company Account State

- [x] Add `$g_sod_company_accrued_wages`.
- [x] Add `$g_sod_company_wage_samples`.
- [x] Add `$g_sod_company_last_pay_day`.
- [x] Add `$g_sod_company_last_full_pay_day`.
- [x] Add `$g_sod_company_last_bonus_pay_day`.
- [x] Add `$g_sod_company_pay_confidence`.
- [x] Add `$g_sod_company_camp_strain`.
- [x] Add `$g_sod_company_ration_policy`.
- [x] Add `$g_sod_company_ration_confidence`.
- [x] Add `$g_sod_company_wage_promise_day`.
- [x] Add `$g_sod_company_wage_promise_due_day`.
- [x] Add `$g_sod_company_wage_promise_amount`.
- [x] Add `$g_sod_company_battle_promise_day`.
- [x] Add `$g_sod_company_battle_promise_amount`.
- [x] Add `$g_sod_company_battle_promise_active`.
- [x] Add `$g_sod_company_battle_promise_broken`.
- [x] Add `$g_sod_company_last_petition_day`.
- [x] Add `$g_sod_company_last_desertion_day`.
- [x] Add `$g_sod_company_last_mutiny_day`.
- [x] Add `$g_sod_company_last_mutiny_answer_day`.

### Derived Bands

- [x] Pay confidence bands:
  - [x] Trusted
  - [x] Steady
  - [x] Watchful
  - [x] Doubtful
  - [x] Angry
  - [x] Broken
- [x] Camp strain bands:
  - [x] Calm
  - [x] Frayed
  - [x] Bitter
  - [x] Dangerous
  - [x] Splintering
- [x] Ration confidence bands:
  - [x] Well fed
  - [x] Adequate
  - [x] Thin
  - [x] Hungry
  - [x] Starving

## Troop Class Split

### Hero NPCs and Companions

Hero NPCs do not behave like wage stacks. They are personal witnesses, advisors, rivals, and pressure valves.

- [x] Companions do not desert silently from unpaid wages.
- [x] Companions confront the player through existing companion-depth warning/reconciliation systems.
- [x] Companions can mediate troop petitions if their role and approval support it.
- [x] Companions can worsen crises if ignored, slighted, or ideologically opposed.
- [x] Companion reactions should use `script_sod_companion_apply_player_action`.
- [x] Bunduk reacts strongly to unfair pay, veteran neglect, and officer cruelty.
- [x] Katrin reacts strongly to food, debt, wages, and practical shortages.
- [x] Ymira and Jeremus react strongly to wounded/dependent support and starvation.
- [x] Lezalit reacts strongly to discipline, order, broken promises, and mutiny leniency.
- [x] Marnid reacts strongly to clean accounts, contracts, and debt honesty.
- [x] Borcha reacts strongly to practical survival, road hardship, and empty speeches.

### Mercenaries

Mercenaries are contract-minded. They tolerate harshness better than idealists, but not broken terms.

- [x] Mercenaries expect timely coin more than generous rations.
- [x] Mercenary grievance is preferred when pay arrears dominate.
- [x] Mercenary grievance falls faster from bonus pay.
- [x] Mercenaries can be selected for peaceful leave when arrears dominate and pressure is severe.
- [x] Veteran mercenaries may demand hazard pay after repeated high-casualty battles.
- [x] Mercenaries can become the most likely violent mutiny bloc if many are unpaid and armed.
- [x] Mercenary guild pacts affect wage expectations and negotiation options in v1 through contract-flavored pressure and mercenary-world hooks.
- [x] Mercenary dialogue should sound contractual, not feudal or sentimental.

### Noble and Faith Troops

Noble and faith troops care about honor, doctrine, prestige, and obligations beyond wages.

- [x] Noble troops tolerate delayed pay better if honor, victories, and prestige are high through battle/public prestige pressure relief.
- [x] Noble troops are the only non-hero troop class that becomes restless if the company goes too long without battle, tournament glory, or prestigious action.
- [x] Noble idleness should create noble-specific restlessness and petition pressure, not a flat party morale chip.
- [x] Noble troops dislike thin rations if common troops are favored too visibly.
- [x] Faith troops react to ration generosity, mercy, sacrilege, slavery, and holy obligations.
- [x] Noble/faith troops may ask for ceremonial pay, offerings, or restitution instead of normal coin.
- [x] Noble/faith troops are less likely to steal supplies during desertion.
- [x] Noble/faith troops are identified as distinct pressure classes for future formal rebuke dialogue.
- [x] Faith troops can support the player during mutiny if the player's conduct aligns with their doctrine.
- [x] Noble troops are the hardest troop class to please through tavern recreation.
- [x] Noble troops respond strongly to arena tournaments, public victories, honorable duels, and visible prestige.
- [x] Noble/faith dialogue should emphasize honor, oath, purity, shame, or sacred duty.

### Normal Enlisted Troops

Enlisted troops are the body of the army. They care about pay, food, safety, victories, and whether officers spend them cheaply.

- [x] Enlisted troops are preferred when ration grievance dominates.
- [x] Enlisted troops are most sensitive to repeated unpaid wages.
- [x] Enlisted troops forgive delay after victories if pay confidence is high.
- [x] Enlisted troops are likely to petition before desertion.
- [x] Enlisted troops may peacefully desert in small groups if pay/food are bad.
- [x] Enlisted troops may follow a mercenary or veteran stack into violent mutiny warning pressure if strain is extreme.
- [x] Enlisted dialogue should sound practical: coin, bread, boots, wounds, families, and fear.

## Ration Policy

### Policies

- [x] Add Thin Rations.
  - [x] Food lasts longer.
  - [x] Morale slowly falls.
  - [x] Camp strain rises if used too long.
  - [x] Peaceful desertion risk rises for enlisted troops.
- [x] Add Standard Rations.
  - [x] Baseline consumption and morale.
  - [x] No special effect unless food variety is poor.
- [x] Add Generous Rations.
  - [x] Food is consumed faster.
  - [x] Morale improves.
  - [x] Pay confidence softens slightly when wages are delayed.
  - [x] Katrin/Ymira/Jeremus generally approve if supplies permit.
- [x] Add Officer Austerity.
  - [x] Officers/companions publicly share hardship.
  - [x] Slows strain from thin rations.
  - [x] Lezalit may respect discipline; some proud nobles may resent it.
- [x] Add Spoils Feast.
  - [x] Available after major victories or raids.
  - [x] Ration-feast v1 consumes food from company stores.
  - [x] Gives a short morale boost.
  - [x] Can be honorable celebration or ugly indulgence depending source of supplies.

### Food Variety

- [x] Keep existing food morale logic.
- [x] Add a ration policy multiplier to food consumption.
- [x] Add report text explaining if food variety is helping or hurting.
- [x] Make starvation overpower wage generosity.
- [x] Make generous rations less effective if the party is eating only one poor food type.

## Recreation and Settlement Relief

### Design Inspiration

Battle Brothers uses settlement services, especially taverns, as a pressure valve for company mood and as a source of rumors. Ponavosa should use the same broad lesson in its own style: taverns, temples, arenas, feasts, bathhouses if available, and local festivals can give the player non-wage ways to keep the company human, but they should not erase broken promises, starvation, or months of abuse.

### Recreation State

- [x] Add `$g_sod_company_last_recreation_day`.
- [x] Add `$g_sod_company_recreation_memory`.
- [x] Add `$g_sod_company_recreation_quality`.
- [x] Add `$g_sod_company_recreation_excess`.
- [x] Add `$g_sod_company_last_tavern_round_day`.
- [x] Add `$g_sod_company_last_religious_observance_day`.
- [x] Add `$g_sod_company_last_arena_spectacle_day`.

### Recreation Venues

- [x] Taverns provide drink, stories, rumor, gambling, and a broad morale lift.
- [x] Temples provide solemn relief, burial rites, recovery, and faith-troop confidence.
- [x] Arenas/tournaments provide spectacle, pride, and discipline-flavored morale.
  - [x] Arena tournaments are the primary recreation relief for noble troop restlessness.
  - [x] Arena success should improve noble confidence more than tavern spending.
- [x] Town feasts provide prestige, noble approval, and a larger but rarer morale lift through victory feast/public honor support.
- [x] Village festivals provide low-cost enlisted morale when relations are good.
- [x] Campfire recreation provides a small free recovery option when no settlement is nearby.

### Tavern Actions

- [x] Buy a round for the company.
  - [x] Costs denars based on party size.
  - [x] Improves morale and lowers camp strain.
  - [x] Helps enlisted troops and mercenaries most.
  - [x] Helps noble troops least unless paired with public honor, feast status, or tournament victory.
  - [x] Has diminishing returns if repeated too often.
- [x] Buy a proper night of lodging and drink.
  - [x] Costs more than a round.
  - [x] Improves pay confidence slightly if wages are not badly overdue.
  - [x] Helps wounded and exhausted troops recover mood.
  - [x] Requires a town or suitable walled center where local recreation quality supports it.
- [x] Let the men drink on their own coin.
  - [x] Low or no direct cost.
  - [x] Small morale lift.
  - [x] Small risk of brawls, arrests, gambling debts, or companion complaints.
- [x] Keep strict discipline in town.
  - [x] Prevents disorder.
  - [x] Lezalit and some nobles approve.
  - [x] Enlisted and mercenary morale do not recover.
- [x] Ask for tavern rumors.
  - [x] Reveals local road risk, contracts, deserters, market trouble, or mini-faction pressure.
  - [x] Should support trade network and company account decisions.

### Religious and Healing Relief

- [x] Pay for burial rites after high casualties.
  - [x] Lowers camp strain after bloody battles.
  - [x] Helps faith troops, Ymira, Jeremus, and Firentis-style companions.
- [x] Make an offering for the company.
  - [x] Improves faith troop confidence.
  - [x] Can soften broken-pay anger only if wages are not severe.
- [x] Pay for care of the wounded.
  - [x] Helps wounded/dependent pay choice.
  - [x] Improves morale after casualties.
  - [x] Interacts with Surgeon/wounded-care companion pressure through healing and wounded-pay hooks.

### Arena and Prestige Relief

- [x] Enter or sponsor an arena tournament.
  - [x] Strongly lowers noble restlessness if the player performs well or the company is publicly honored.
  - [x] Improves noble/faith confidence if the victory is framed as honorable.
  - [x] Improves enlisted morale modestly through spectacle.
  - [x] Improves mercenary morale only slightly unless prize money is shared.
- [x] Hold public honors after a tournament or battle victory.
  - [x] Costs denars or prestige.
  - [x] Greatly helps noble troops.
  - [x] Slightly helps enlisted troops.
  - [x] Can irritate Bunduk/Katrin if wages or wounded are neglected.
- [x] Share tournament or battle prize money with the company.
  - [x] Helps mercenaries and enlisted troops more than nobles.
  - [x] Helps pay confidence if wage arrears are modest.
- [x] Refuse public spectacle.
  - [x] Avoids cost.
  - [x] Lezalit may respect focus if there is active war.
  - [x] Noble restlessness continues if the company has been idle.

### Recreation Risks

- [x] Drunken brawl incident.
- [x] Gambling debt incident.
- [x] Missing soldier incident.
- [x] Insulted noble/faith troop incident.
- [x] Mercenary overindulgence incident.
- [x] Local authority fine.
- [x] Companion warning if recreation is used while wages or food are neglected.

### Balance Rules

- [x] Recreation lowers camp strain faster than it raises pay confidence.
- [x] Recreation cannot fully offset unpaid wages past the `Angry` pay confidence band.
- [x] Recreation cannot offset starvation.
- [x] Recreation has diminishing returns if used repeatedly within a few days.
- [x] Recreation works best after victories, hard marches, sieges, or long travel.
- [x] Recreation should be cheaper than bonus pay but weaker and less reliable.
- [x] Recreation should create occasional rumor/intelligence value even when morale is already stable.
- [x] Tavern recreation is intentionally inefficient for noble restlessness.
- [x] Arena/tournament recreation is intentionally efficient for noble restlessness.
- [x] Noble restlessness should push petitions, requests for tournaments, requests for battle, or formal withdrawal before any violent outcome.

## Pay Choices

### Camp Menu: Settle Company Accounts

- [x] Add camp menu entry: `Settle company accounts`.
- [x] Show current owed wages.
- [x] Show pay confidence.
- [x] Show ration policy.
- [x] Show camp strain.
- [x] Show days since full pay.
- [x] Show current wage promise, if any.
- [x] Show troop-class pressure summary.

### Player Options

- [x] Pay full wages.
  - [x] Clears current accrued wages.
  - [x] Improves or maintains pay confidence.
  - [x] Lowers camp strain.
- [x] Pay half wages.
  - [x] Reduces accrued wages.
  - [x] Slightly lowers pay confidence unless explained through dialogue.
  - [x] May trigger petitions if repeated.
- [x] Pay bonus wages.
  - [x] Clears current wages and pays extra.
  - [x] Improves pay confidence.
  - [x] Boosts morale.
  - [x] Mercenaries and enlisted troops approve most.
- [x] Pay veterans first.
  - [x] Helps elite/enlisted veteran stacks through confidence/strain relief.
  - [x] Risks recruit resentment by leaving remaining debt in place.
  - [x] Lezalit and Bunduk can react depending fairness.
- [x] Pay wounded/dependents first.
  - [x] Helps morale after costly battles.
  - [x] Ymira/Jeremus approve.
  - [x] Some mercenaries may dislike delayed contractual pay.
  - [x] Battle casualties create persistent compensation pressure until addressed.
- [x] Delay payment.
  - [x] Costs no gold now.
  - [x] Raises camp strain.
  - [x] Lowers pay confidence.
- [x] Promise payment by a date.
  - [x] Temporarily stabilizes morale.
  - [x] Creates a tracked promise.
  - [x] Breaking the promise causes a larger penalty.
- [x] Promise payment after the next battle.
  - [x] Stabilizes a desertion request without paying immediately.
  - [x] Converts to a short due-date promise after victory.
  - [x] Converts to a short due-date promise after defeat, with lower patience and higher crisis pressure.
  - [x] Surfaces in the company account report while active.
  - [x] Can be made directly from the company accounts menu, not only from desertion negotiation.
- [x] Threaten discipline.
  - [x] Suppresses immediate petition/desertion risk.
  - [x] Hurts pay confidence and companion approval.
  - [x] Raises violent mutiny risk later if conditions do not improve.
- [x] Open the stores for a ration feast.
  - [x] Improves morale.
  - [x] Reduces food stores.
  - [x] Can temporarily soften unpaid wage pressure.

## Dialogue-Driven Escalation

### Stage 0: Quiet Accounting

- [x] No petition pressure if wages are current, rations are adequate, nobles are calm, and camp strain is low.
- [x] Camp report quietly shows pay, ration, recreation, noble pressure, and petition risk values.

### Stage 1: Murmurs

- [x] Trigger when wages, rations, noble idleness, or camp strain cross murmur thresholds.
- [x] Display low-frequency world/camp messages.
- [x] Companion comments can surface the issue.
- [x] No desertion occurs during the current murmur implementation.

### Stage 2: Petition

- [x] A company petition menu lets the player hear the dominant complaint.
- [x] Petition type depends on dominant grievance:
  - [x] Pay arrears.
  - [x] Thin rations.
  - [x] Broken promise.
  - [x] Casualties without compensation.
  - [x] Cruel or dishonorable conduct.
  - [x] Noble restlessness after prolonged idleness.
  - [x] Wounded care neglect.
  - [x] General camp strain.
- [x] Player can answer with pay, promise, ration change, persuasion, threat, or dismissal.
- [x] Player can redirect pay, ration, and relief complaints to the relevant company menus.
- [x] Player can hear out, reassure, or dismiss the complaint for modest pressure changes.
- [x] Noble-restlessness petitions can be answered with tournament glory, honorable battle, public honors, feasts, or permission to leave in the current menu/report foundation.
- [x] Companion advisor may intervene if assigned and trusted.

### Stage 3: Peaceful Desertion Request

- [x] A group can ask to leave with some owed pay once pressure becomes severe enough.
- [x] Player can:
  - [x] Pay them and let them go.
  - [x] Persuade them to stay.
  - [x] Promise pay after next battle.
  - [x] Let them leave unpaid, causing confidence loss.
  - [x] Forbid desertion, raising future pressure.
- [x] Peaceful deserters remove a small number of troops from an affected non-hero stack when the player allows them to leave.
- [x] Peaceful deserters now leave as a real `pt_deserters` map party made from the departing stack.
- [x] Desertion pressure reacts to morale, unpaid wages, hunger, camp strain, and current petition severity.
- [x] Desertion prefers the troop class implied by the dominant grievance.

### Stage 4: Theft and Flight

- [x] Trigger when grievance is high and peaceful requests are denied or ignored.
- [x] A group deserts and takes modest food/gold where appropriate.
- [x] Harsher desertion can take non-hero prisoners.
- [x] Harsher desertion can take horses, trade goods, or equipment later.
- [x] Player receives a report showing gold/food taken by unpaid deserters.
- [x] Borcha/Klethi/Deshavi-style companions may offer tracking or prevention hooks later; v1 routes their reactions through companion depth incidents.

### Stage 5: Armed Mutiny

- [x] Mutiny warning triggers only under severe conditions:
  - [x] High accrued wages or unresolved grievance pressure.
  - [x] Low pay confidence.
  - [x] Dangerous camp strain.
  - [x] Low morale.
  - [x] A substantial slighted troop bloc exists.
- [x] Split party into loyalists and mutineers.
- [x] Loyalists should be based on high morale, high relation troop classes, companions, and recently rewarded stacks.
- [x] Mutiny warning bloc selection is based on slighted troop class, unpaid mercenaries, starving enlisted troops, or abused faith/noble troops.
- [x] A battle can break out between the player/loyalists and mutineers.
- [x] v1 includes final warning, negotiation pressure, and an optional battle route.
  - [x] Expelled mutiny ringleaders can take modest gold/food, shown in the resolution message.
- [x] Expelled ringleaders can seize non-hero prisoners.
- [x] Armed mutineers seek horses, trade goods, or equipment later.
- [x] Victory consequences:
  - [x] Mutiny can be suppressed administratively by expelling ringleaders.
  - [x] Expelled ringleaders leave as a real deserter party.
  - [x] Surviving mutineers may become prisoners or dead after future armed mutiny battles.
  - [x] Lezalit/Bunduk/Ymira/Jeremus reactions depend on player response.
- [x] Defeat consequences:
  - [x] Player loses gold/supplies/troops.
  - [x] Expelled mutineers leave as a deserter party.
  - [x] Defeating armed mutineers can create prisoner/dead/deserter splits.
  - [x] Companions may warn or leave depending approval through companion-depth warnings/reconciliation.

## Reports

### Company Accounts Report

- [x] Add camp report: `Company Accounts`.
- [x] Show wages owed.
- [x] Show wages due by troop class.
- [x] Show likely petition/desertion/mutiny voice by troop class.
- [x] Show days since full pay.
- [x] Show pay confidence band.
- [x] Show current ration policy.
- [x] Show ration confidence band.
- [x] Show camp strain band.
- [x] Show recent recreation and whether the company needs relief.
- [x] Show noble restlessness if noble troops have gone too long without battle, tournament glory, or prestige.
- [x] Show active promise.
- [x] Show risk of petition in in-world language.
- [x] Show risk of peaceful desertion in in-world language.
- [x] Show risk of mutiny in in-world language.
- [x] Show companion advisor comments if available.

### Example Report Text

```text
Company Accounts

Wages owed: 3,420 denars
Days since full pay: 8
Rations: Thin
Pay confidence: Watchful
Camp strain: Bitter

The enlisted men are counting meals and coin. The mercenaries are quieter, which is worse. Bunduk says the line will hold better when pay stops being rumor. Katrin says grain is cheaper than desertion.
```

## Scripts

### Core API

- [x] Add `script_sod_company_accounts_initialize`.
- [x] Add `script_sod_company_accounts_accrue_wages`.
- [x] Add `script_sod_company_accounts_get_due_to_regs`.
- [x] Add `script_sod_company_accounts_apply_pay_choice`.
- [x] Add `script_sod_company_accounts_set_ration_policy`.
- [x] Add `script_sod_company_accounts_apply_recreation`.
- [x] Add `script_sod_company_accounts_describe_recreation_to_s26`.
- [x] Add `script_sod_company_accounts_update_noble_restlessness`.
- [x] Add `script_sod_company_accounts_apply_arena_prestige`.
- [x] Add `script_sod_company_accounts_update_morale_pressure`.
- [x] Add `script_sod_company_accounts_get_troop_class`.
- [x] Add `script_sod_company_accounts_describe_to_s20`.
- [x] Add `script_sod_company_accounts_try_petition`.
- [x] Add `script_sod_company_accounts_process_petition_check`.
- [x] Add `script_sod_company_accounts_apply_petition_response`.
- [x] Add `script_sod_company_accounts_describe_petition_to_s36`.
- [x] Add `script_sod_company_accounts_try_peaceful_desertion`.
- [x] Add `script_sod_company_accounts_process_desertion_check`.
- [x] Add `script_sod_company_accounts_resolve_desertion`.
- [x] Add `script_sod_company_accounts_describe_desertion_to_s40`.
- [x] Add `script_sod_company_accounts_set_battle_pay_promise`.
- [x] Add `script_sod_company_accounts_try_mutiny`.
- [x] Add `script_sod_company_accounts_process_mutiny_check`.
- [x] Add `script_sod_company_accounts_apply_mutiny_warning_response`.
- [x] Add `script_sod_company_accounts_describe_mutiny_to_s44`.
- [x] Add `script_sod_company_accounts_resolve_mutiny`.

### Integration API

- [x] Add helper call from food consumption logic.
- [x] Add helper call from morale calculation.
- [x] Add helper call from companion depth actions.
- [x] Add helper call from battle victory/loss resolution.
- [x] Add helper call from troop upgrade/hiring if debt should affect confidence.
- [x] Add helper call from village raid/help choices if ration supplies are affected through companion/faith/slaver/village support hooks where present.
- [x] Add helper call from tavern, temple, arena, feast, and campfire recreation menus.
- [x] Add helper call from arena tournament completion hooks.
- [x] Add helper call from duel victory hooks through arena/prestige/tournament glory pathways.

## Trigger Changes

- [x] Replace automatic payday jump in `ST02_every_hour/entry_0133.py`.
- [x] Keep 12-hour wage accrual.
- [x] Accrue wages into company account state instead of forcing `mnu_pay_day`.
- [x] Add daily or half-daily pressure update.
- [x] Add low-frequency petition checks.
- [x] Add low-frequency desertion checks.
- [x] Add safety clamps for all wage/debt globals.
- [x] Keep compatibility with existing `$g_player_debt_to_party_members` until fully migrated.

## Menu Changes

- [x] Keep old `mnu_pay_day` temporarily as compatibility or convert it into manual settlement.
- [x] Add `mnu_company_accounts`.
- [x] Add `mnu_company_accounts_pay_full`.
- [x] Add `mnu_company_accounts_pay_half`.
- [x] Add `mnu_company_accounts_pay_bonus`.
- [x] Add `mnu_company_accounts_pay_veterans`.
- [x] Add `mnu_company_accounts_pay_wounded`.
- [x] Add `mnu_company_accounts_delay`.
- [x] Add `mnu_company_accounts_promise`.
- [x] Add `mnu_company_accounts_threaten`.
- [x] Add `mnu_company_rations`.
- [x] Add `mnu_company_recreation`.
- [x] Add `mnu_company_recreation_tavern_round`.
- [x] Add `mnu_company_recreation_lodging`.
- [x] Add `mnu_company_recreation_religious_rites`.
- [x] Add `mnu_company_recreation_arena_prestige` through arena prestige relief and tournament completion hooks.
- [x] Add `mnu_company_recreation_campfire`.
- [x] Add `mnu_company_petition`.
- [x] Add `mnu_company_desertion_petition`.
- [x] Add `mnu_company_mutiny_warning`.
- [x] Add `mnu_company_mutiny_resolution`.

## Dialogue Surfaces

### Petition Dialogue

- [x] Add generic company petition menu text for pay, ration, noble, and camp-strain grievances.
- [x] Add enlisted troop petition dialogue.
- [x] Add mercenary petition dialogue.
- [x] Add noble troop petition dialogue.
- [x] Add faith troop petition dialogue.
- [x] Add companion-mediated petition dialogue.

### Peaceful Desertion Dialogue

- [x] Add generic peaceful desertion request menu.
- [x] Add enlisted peaceful desertion dialogue.
- [x] Add mercenary contract-exit dialogue.
- [x] Add noble formal-withdrawal dialogue.
- [x] Add faith oath-crisis dialogue.
- [x] Add player persuasion route.
- [x] Add player payment route.
- [x] Add player forbid route.

### Mutiny Dialogue

- [x] Add final warning menu text.
- [x] Add loyalist rally dialogue.
- [x] Add mutineer demand dialogue.
- [x] Add peaceful last-chance settlement route.
- [x] Add ringleader expulsion route.
- [x] Add battle-start route if negotiations fail.
- [x] Add aftermath dialogue after suppression.
- [x] Add aftermath dialogue after losses/theft.

## Companion Reactions

- [x] Add companion action: fair pay.
- [x] Add companion action: bonus pay.
- [x] Add companion action: half pay.
- [x] Add companion action: delayed pay.
- [x] Add companion action: broken pay promise.
- [x] Add companion action: generous rations.
- [x] Add companion action: thin rations.
- [x] Add companion action: officer austerity.
- [x] Add companion action: ration feast.
- [x] Add companion action: tavern recreation.
- [x] Add companion action: solemn rites.
- [x] Add companion action: arena prestige.
- [x] Add companion action: noble idleness petition through noble-restlessness, honor, and strict-discipline hooks.
- [x] Add companion action: drunken disorder.
- [x] Add companion action: threatened troops.
- [x] Add companion action: peaceful desertion allowed.
- [x] Add companion action: peaceful desertion forbidden.
- [x] Add companion action: mutiny suppressed.
- [x] Add companion action: mutiny negotiated.

## Troop Selection Rules

### Petition Representative

- [x] Prefer the largest affected troop class.
- [x] Prefer higher-tier troops as representatives through stack weighting and troop-class pressure.
- [x] Prefer mercenaries if wage grievance dominates.
- [x] Prefer enlisted troops if ration grievance dominates.
- [x] Prefer noble/faith troops if honor or doctrine grievance dominates.

### Peaceful Desertion Group

- [x] Select small stack portion, not whole army by default.
- [x] Weight by morale, unpaid wages, hunger, and class grievance pressure.
- [x] Prefer the troop class implied by the dominant grievance.
- [x] Never remove companions through this path.
- [x] Respect story-critical troop exceptions if any exist by never removing heroes and limiting desertion to non-hero stacks.

### Mutiny Group

- [x] Build mutiny party from affected stacks.
- [x] Select a warning/suppression bloc from affected stacks.
- [x] Build loyalist side from player, companions, high-confidence troops, and recently rewarded stacks.
- [x] Ensure mutiny cannot fire with trivial force.
- [x] Ensure mutiny cannot chain repeatedly without cooldown.

## Economy and Balance

- [x] Full pay should be the expected baseline.
- [x] Bonus pay should be strong but expensive.
- [x] Half pay should be viable once, dangerous as a habit.
- [x] Generous rations should not replace pay forever.
- [x] Threats should be a short-term fix with long-term risk.
- [x] Faith/noble troop demands should be rarer but sharper.
- [x] Mercenary desertion should be predictable and contract-flavored.
- [x] Enlisted unrest should build slowly but become serious if ignored.

## Implementation Milestones

### Milestone 1: Manual Accounts

- [x] Add company account globals.
- [x] Stop automatic payday menu.
- [x] Accrue wages manually into company state.
- [x] Add company accounts report.
- [x] Add full pay, half pay, delay, bonus pay, veteran pay, and wounded/dependent pay.
- [x] Preserve existing unpaid debt morale penalty.
- [x] Add static tests for new scripts/menu/trigger wiring.

### Milestone 2: Ration Policy

- [x] Add ration policy globals/constants.
- [x] Add ration policy menu.
- [x] Hook ration policy into morale.
- [x] Hook ration policy into food consumption.
- [x] Add ration report text.
- [x] Add companion reaction hooks.
- [x] Add ration feast action that spends food, boosts morale, and softens camp strain.

### Milestone 3: Recreation and Settlement Relief

- [x] Add recreation globals/constants.
- [x] Add recreation menu/report text.
- [x] Add tavern round option.
- [x] Add lodging/drink option.
- [x] Add religious rites option.
- [x] Add arena prestige option.
- [x] Add campfire recreation option.
- [x] Add village festival recreation option gated by friendly village relation and healthy village state.
- [x] Add recreation diminishing returns.
- [x] Add noble restlessness tracking.
- [x] Add arena/tournament relief for noble restlessness.
- [x] Add tavern rumor/intelligence hook.
- [x] Add companion reaction hooks.

### Milestone 4: Dialogue Petitions

- [x] Add dominant-grievance petition triggers.
- [x] Add generic representative menu.
- [x] Add troop-class petition triggers.
- [x] Add troop-class representative dialogue.
- [x] Add companion mediation.
- [x] Add player promise route.
- [x] Add broken promise consequence.

### Milestone 5: Peaceful Desertion

- [x] Add desertion request menu.
- [x] Add troop removal logic.
- [x] Add pay-to-leave option.
- [x] Add persuasion-to-stay option.
- [x] Add forbid-desertion risk path.
- [x] Add report and companion reactions.
- [x] Add class-specific dialogue variants.

### Milestone 6: Mutiny

- [x] Add final warning menu.
- [x] Add loyalist/mutineer split logic.
- [x] Add battle route.
- [x] Add deserter-party aftermath for peaceful company desertion.
- [x] Add food/gold/prisoner theft aftermath for unpaid desertion and expelled mutiny ringleaders.
- [x] Add cargo aftermath for harsher desertion and mutiny paths.
- [x] Add suppression/negotiation aftermath.
- [x] Add companion reactions and cooldowns.
- [x] Add non-battle mutiny resolution path.
- [x] Add full battle mutiny resolution path.

### Milestone 7: Polish and Expansion

- [x] Add battle-result bonus pay prompt.
- [x] Add casualty compensation pressure after battles.
- [x] Add post-battle morale consequences for victories, defeats, unpaid wages, and active battle promises.
- [x] Add siege hazard pay demand.
- [x] Add feast after victory.
- [x] Add mini-faction and companion-specific modifiers.
- [x] Add more report flavor by troop culture/class.
- [x] Add recreation incidents.
- [x] Add town-specific entertainment flavor.
- [x] Add manual QA scenarios below as targeted gameplay QA rows.

## Static Test Plan

- [x] Add `build/test_company_accounts_static.py`.
- [x] Verify company account globals/constants exist.
- [x] Verify wage accrual script exists.
- [x] Verify automatic payday jump is removed or gated.
- [x] Verify camp accounts menu is reachable.
- [x] Verify ration policy menu is reachable.
- [x] Verify recreation menu is reachable.
- [x] Verify noble restlessness tracking exists.
- [x] Verify arena prestige relief exists.
- [x] Verify troop-class split constants exist.
- [x] Verify petition scripts exist.
- [x] Verify desertion scripts exist.
- [x] Verify mutiny warning scripts exist.
- [x] Verify mutiny resolution scripts exist.
- [x] Verify companion action hooks exist.
- [x] Verify report text includes pay confidence, rations, camp strain, and troop class pressure.
- [x] Verify report text includes recent recreation pressure.
- [x] Verify report text includes noble restlessness.

## Build Checks

- [x] `py build\doctor.py --doctor-new-only`
- [x] `py build\test_company_accounts_static.py`
- [x] `py build\test_feature_audit_static.py`
- [x] `cmd /c build_module.bat --no-cache`

## Gameplay QA

- [x] Full pay clears accrued wages and improves confidence.
- [x] Half pay reduces debt but raises concern if repeated.
- [x] Delay payment creates pressure without immediate interruption.
- [x] Broken promise creates a stronger backlash than honest delay.
- [x] Generous rations improve morale but consume more food.
- [x] Thin rations preserve food but increase strain over time.
- [x] Tavern recreation lowers camp strain but does not erase serious unpaid wages.
- [x] Religious rites reduce casualty strain and improve faith troop confidence.
- [x] Noble troops gain little from ordinary tavern recreation.
- [x] Noble troops gain strong relief from arena tournament success.
- [x] Noble troops create petition pressure after long idleness without applying a flat morale chip to the whole party.
- [x] Repeated recreation has diminishing returns.
- [x] Mercenaries peacefully leave after severe unpaid arrears.
- [x] Enlisted troops petition before deserting.
- [x] Noble/faith troops respond to honor/doctrine framing.
- [x] Violent mutiny warnings only occur under severe sustained abuse with minimum bloc size and answer cooldown.
- [x] Loyalist/mutineer split feels plausible.
- [x] Companions react in character.

## Open Questions

- [x] Should troop class be inferred only from troop ranges/factions, or should special troop slots mark class explicitly? Decision: infer from doctrine/troop metadata for v1; add explicit slots only if edge cases appear.
- [x] Should the player be allowed to prepay wages? Decision: not in v1; bonus pay is the current loyalty-building prepayment analogue.
- [x] Should party loot automatically offer a `pay from spoils` option? Decision: no automatic post-loot interruption in v1; recent victories already unlock `Share victory spoils with the company` in camp accounts.
- [x] Should high Leadership delay petitions or improve promise credibility? Decision: Leadership and Persuasion affect dialogue/resolution rather than silently suppressing pressure.
- [x] Should Persuasion help in dialogue only, or also soften pressure calculations? Decision: dialogue only for v1.
- [x] Should noble/faith troop unrest ever become violent, or should they mostly withdraw with honor? Decision: mostly formal withdrawal/oath crisis in v1; violent faith/noble mutiny is v2 only.
- [x] Should mutineers become a map party after theft or only disappear in v1? Decision: deserters/expelled ringleaders become real `pt_deserters` map parties in v1.
- [x] Should recreation quality depend on town prosperity, tavern availability, or player relation with the center?
- [x] Should tavern disorder create legal trouble with the center owner? Decision: yes, local-fine incidents also reduce nearby center relation.
- [x] Should strict discipline prevent recreation incidents at the cost of troop strain? Decision: yes, represented by strict-discipline recreation.
- [x] How many days without battle/tournament/prestige should create noble restlessness? Decision: current thresholds begin around 10 days and escalate from there.
- [x] Should noble restlessness count honorable diplomacy or only martial/public prestige? Decision: v1 counts battle, tournament, public honors, feast, and honor/prestige-style hooks.
