# The Road to the Crown

> Status: **target-state design plus active implementation notes**.  
> This is an implementation-ready narrative and systems brief for module-system lowering. Several vertical slices now exist in runtime form; target-state sections still describe intended full-campaign behavior beyond the current live implementation.

## Overview

- **Campaign ID:** `campaign_road_to_the_crown`
- **Type:** main campaign
- **Length:** long
- **Role:** central rise-from-exile-to-power campaign spine
- **Active or side campaign:** active campaign
- **Primary fantasy:** the player arrives as a survivor of a burned homeland and decides what kind of crown, cause, or settlement will answer that loss.
- **Primary antagonist pressure:** Legate Gaius Marius, called the Imperial Hound.
- **Primary implementation shape:** five acts lowered into quest chains, menus, dialogue states, faction memory flags, companion reactions, and end-state unlocks.

The campaign begins with the premise already present in character creation:

- the player came from a burned land
- the player cannot return unchanged
- Calradia is divided by petty wars
- the Imperial Hound is advancing
- the old world is gone
- the new life must be chosen

The campaign is not simply "become king." It is about whether the player becomes a lawful ruler, a coalition-maker, a paid sword, a conqueror, a restorer, a reformer, an imperial collaborator, or a survivor who refuses every crown offered.

## Design Pillars

1. **Exile is the beginning, not the end**  
   The player starts displaced, poor in certainty, and rich in future consequence.

2. **Identity becomes politics**  
   Origin, faith, adult-life path, and personal motive become persistent narrative tags that affect who trusts the player and how the world names them.

3. **Every route needs a moral cost**  
   Legitimacy can require compromise. Conquest can save lives by ending wars quickly, or ruin the player's own cause. Trade can preserve people or commodify them. Peace can become appeasement.

4. **The Imperial Hound is pressure, not just a boss**  
   Gaius Marius is felt through refugees, scouts, intercepted orders, defectors, burned villages, faction panic, and strategic deadlines before he appears directly.

5. **The crown is a question**  
   The campaign repeatedly asks what authority means: inheritance, victory, recognition, wealth, faith, mercy, fear, survival, or return.

## Starting Identity Tags

The character creation flow sets compact campaign tags. These tags are checked by dialogue, companion reactions, and route gates.

### Origin Tags

#### Antares

- **Tag:** `origin_antares`
- **Campaign identity:** court-bred exile, heir to imperial memory, trained for governance.
- **Default public read:** possible claimant, educated foreign noble, dangerous symbol.
- **Route affinity:** legitimacy, restoration, anti-imperial resistance.
- **Common suspicion:** "another empire in mourning."
- **Opening flavor:** the player understands seals, ranks, logistics, and court language.

#### Marina

- **Tag:** `origin_marina`
- **Campaign identity:** merchant republic survivor, contract-minded, practical, wealthy by instinct even if poor in coin.
- **Default public read:** trader, fixer, negotiator, soft-power operator.
- **Route affinity:** mercenary power, trade coalition, reform through logistics.
- **Common suspicion:** "will sell any banner if the price is right."
- **Opening flavor:** the player knows caravan law, port ledgers, debt pressure, and supply scarcity.

#### Aden

- **Tag:** `origin_aden`
- **Campaign identity:** disciplined martial exile, raised around oath, command, and duty.
- **Default public read:** captain, knight, hard soldier, reliable blade.
- **Route affinity:** conquest, resistance, lawful military order.
- **Common suspicion:** "cannot tell justice from obedience."
- **Opening flavor:** the player recognizes weak formations, poor camp discipline, and frightened levies.

#### Villian

- **Tag:** `origin_villian`
- **Campaign identity:** courtly noble survivor, socially trained, refined but not soft.
- **Default public read:** displaced aristocrat, diplomat, public figure.
- **Route affinity:** legitimacy, coalition, ceremonial rule, noble diplomacy.
- **Common suspicion:** "fine words over hard bread."
- **Opening flavor:** the player understands feasts, hunts, reputation, patronage, and insults disguised as courtesy.

#### Zerrikania

- **Tag:** `origin_zerrikania`
- **Campaign identity:** steppe-bred survivor, mobile, proud, clan-minded, hard to pin down.
- **Default public read:** rider, raider, scout, outsider.
- **Route affinity:** conquest, frontier coalition, mobile defense, independent rule.
- **Common suspicion:** "will not kneel and cannot be held."
- **Opening flavor:** the player reads tracks, weather, horse fatigue, and raiding patterns.

### Faith Tags

#### The One

- **Tag:** `faith_the_one`
- **Legitimacy language:** duty, moral law, rightful order.
- **Companion tension:** mercy companions expect restraint; ruthless companions may see hesitation.
- **Political use:** oaths, coronation rites, reform decrees.

#### The Old Gods

- **Tag:** `faith_old_gods`
- **Legitimacy language:** ancestry, memory, sacred land, honor to the dead.
- **Companion tension:** practical companions may distrust ritual cost.
- **Political use:** restoration, funeral vows, ancestral banners.

#### The Void

- **Tag:** `faith_void`
- **Legitimacy language:** forbidden truth, survival beyond moral comfort, power in darkness.
- **Companion tension:** pious and humane companions may become wary early.
- **Political use:** secret routes, fear, hidden branch discovery, dangerous bargains.

#### Enlightenment

- **Tag:** `faith_enlightenment`
- **Legitimacy language:** discipline, clarity, restraint, wise governance.
- **Companion tension:** passionate companions may object to detachment.
- **Political use:** reform councils, measured justice, faction mediation.

#### Natural Philosophy

- **Tag:** `faith_natural_philosophy`
- **Legitimacy language:** cause and effect, experiment, human choice, practical destiny.
- **Companion tension:** traditionalists may see coldness or arrogance.
- **Political use:** engineering, logistics, market reform, rational settlement.

### Adult-Life Tags

#### Tournaments and Duels

- **Tag:** `life_duelist`
- **Social method:** public honor and visible strength.
- **Early access:** arena masters, duel challenges, noble attention.
- **Route boost:** legitimacy through fame, conquest through martial proof.

#### Intrigues

- **Tag:** `life_intriguer`
- **Social method:** secrets, leverage, false smiles, counterplots.
- **Early access:** informants, court servants, blackmail, hidden evidence.
- **Route boost:** coalition, betrayal, legitimacy sabotage, secret branches.

#### Philosophy

- **Tag:** `life_philosopher`
- **Social method:** counsel, doctrine, public argument, reform.
- **Early access:** scholars, priests, skeptical nobles, policy disputes.
- **Route boost:** coalition, reform, faith endings, lawful rule.

#### Trade

- **Tag:** `life_trader`
- **Social method:** contracts, caravans, debt, supply, safe roads.
- **Early access:** guildmasters, caravan masters, merchants, smugglers.
- **Route boost:** coin crown, mercenary route, coalition logistics.

### Personal Motive Tags

#### Revenge

- **Tag:** `motive_revenge`
- **Crown meaning:** weapon, verdict, repayment.
- **Temptation:** punitive justice, cruelty, betrayal in the name of necessity.
- **Redemption pressure:** mercy must be chosen when vengeance is available.

#### Peace

- **Tag:** `motive_peace`
- **Crown meaning:** settlement, shield, end of cycles.
- **Temptation:** appeasement, compromise with monsters, slow decisions.
- **Redemption pressure:** peace must survive contact with betrayal.

#### Bloodlust

- **Tag:** `motive_bloodlust`
- **Crown meaning:** proof, domination, endless testing.
- **Temptation:** war for its own sake.
- **Redemption pressure:** victory must become something other than appetite.

#### Riches

- **Tag:** `motive_riches`
- **Crown meaning:** security, control, the power never to beg again.
- **Temptation:** exploitation, prisoner markets, abandonment of costly allies.
- **Redemption pressure:** wealth must answer fear instead of feeding it.

## Core Campaign State

Recommended state fields for later implementation:

```md
- campaign_id = campaign_road_to_the_crown
- campaign_status = active | suspended | terminated | archived
- campaign_family_id = campaign_main_crown
- active_act_id = act_01_ashes | act_02_choice | act_03_standing | act_04_crown | act_05_shadow
- active_chapter_id
- active_beat_id
- active_branch_id
- branch_flags
- identity_flags
- world_flags
- companion_flags
- faction_memory_flags
- ending_flags
- unlock_flags
```

### Major Branch Flags

- `branch_legitimacy`
- `branch_mercenary`
- `branch_conquest`
- `branch_coalition`
- `branch_restoration`
- `branch_imperial`
- `branch_hidden_regime_maker`
- `branch_failure_fractured_claim`

### Branch Modifier Flags

These flags modify a main branch instead of replacing it.

- `branch_reform`
- `branch_betrayal`
- `branch_secret`
- `branch_mercy`
- `branch_hardline`

### Major Pressure Flags

- `imperial_pressure_low`
- `imperial_pressure_rising`
- `imperial_pressure_open`
- `imperial_pressure_invasion`
- `imperial_pressure_broken`
- `imperial_pressure_absorbed`

### Reputation Flags

- `reputation_refugee`
- `reputation_foreign_noble`
- `reputation_free_captain`
- `reputation_trade_operator`
- `reputation_avenger`
- `reputation_unproven`
- `reputation_oathbreaker`
- `reputation_peacemaker`
- `reputation_butcher`
- `reputation_trade_prince`
- `reputation_rightful_lord`
- `reputation_hound_marked`

### Trust and Local Pressure Flags

- `commoner_trust_high`
- `commoner_trust_low`
- `merchant_trust_high`
- `merchant_trust_low`
- `noble_trust_high`
- `noble_trust_low`
- `village_fear`
- `underworld_notice`
- `underworld_debt`

### Implemented Local Witness Memory: Price of Bread

The first Act II pressure test now carries one concrete local memory through the implemented campaign spine.

Runtime storage:

```md
slot_quest_target_center = affected bread village
slot_quest_target_troop = Tamsin Reedhand
slot_quest_object_troop = Celeste di Marina
slot_quest_giver_troop = Brother Odran
slot_quest_target_amount = qualitative grain pressure
slot_quest_sod_chain_choice = bread resolution
```

Design rule:

- Keep this memory qualitative in player-facing text.
- Let the same village become rumor, public testimony, Imperial propaganda, threatened witness, final-strategy echo, and ending aftermath.
- Use small local relation/prosperity consequences rather than exact exposed simulation numbers.
- Keep the current menu-compatible route intact until the physical bandit-cache encounter is promoted from simulation bridge to full battle objective.

## Interactive Campaign Contract

Every remaining Road to the Crown chapter should be lowered as an interactive world problem, not only a menu decision.

### Required Chapter Surface

Each chapter should define:

- **World target:** a concrete center, party, troop, route, camp, caravan, battlefield, or witness.
- **Visible pressure:** a qualitative description the player can observe without exact hidden numbers.
- **Player action:** at least one map, dialogue, battle, delivery, escort, investigation, or council action.
- **Witness memory:** at least one named person or place that can repeat what happened later.
- **Complication:** a recoverable failure, timeout, escape, betrayal, counteroffer, or local backlash.
- **Cleanup:** what happens to spawned parties, temporary speakers, route targets, and local slots after resolution.
- **Aftermath:** small local, faction, companion, or campaign-state consequence that later chapters can read.

### Preferred Interaction Types

- **Map pursuit:** track, intercept, shadow, or outrun a party.
- **Witness gathering:** bring a named troop, persuade a local speaker, or preserve a threatened center.
- **Pressure response:** choose where scarce food, coin, troops, legitimacy, or time is spent.
- **Battle with purpose:** fight to rescue, delay, protect, expose, capture, or destroy something specific.
- **Council proof:** present living witnesses, documents, protected roads, or public outcomes rather than selecting an abstract argument.
- **Rumor aftermath:** later menus and dialogue should describe what people say, not reveal exact hidden values.

### Player-Facing Information Rule

Do not expose exact trust, legitimacy, pressure, prosperity, or witness scores. Use qualitative language:

- "thin stores"
- "strained testimony"
- "fearful village"
- "merchant caution"
- "unsteady company"
- "Imperial pressure is rising"
- "the road feels watched"
- "the witness is vulnerable"

Exact values may exist in slots, but the player should read the world through people, places, and consequences.

## Interactive Chapter Upgrade Plan

The campaign spine is already authored. The next design layer is to make each chapter ask the player to act in the world.

### Act III: Standing And Recognition

#### `qst_rtc_three_offers`

Target-state interaction:

- Each offer should be represented by a messenger, patron, caravan factor, militia speaker, or hidden broker.
- The player should be able to inspect why an offer is available before accepting it.
- Offer availability should be explained through rumors and witnesses, not exact requirements.

World targets:

- Noble protection: a court messenger or nearby castle hall witness.
- Paid steel: a caravan master, payroll chest, or mercenary captain.
- People's road: the remembered bread village, a bound village, or refugee speaker.
- Hard claim: an enemy patrol, rival banner party, or public duel challenge.
- Quiet ledger: Vaska's agent, smuggler contact, or suspicious courier.

Interactive outcomes:

- Accepting an offer should create a short route proof objective before finalizing the route when possible.
- Refusing all offers should spawn a recovery rumor instead of simply becoming "unproven."
- A route should feel earned by doing one visible thing, not only chosen from a menu.

Failure and recovery:

- If the player lacks a strong witness, the offer can remain "tentative" and ask for proof.
- If a route proof times out, the route can still proceed but starts with weaker recognition.
- If a patron is attacked or a caravan is lost, the route should bend rather than hard-stop.

#### `qst_rtc_companions_take_sides`

Target-state interaction:

- Campfire disagreement should be tied to who is actually in the party.
- Companions should reference concrete prior actions: saved wounded, forced grain, protected witnesses, accepted Imperial terms.
- The player should get limited responses: reassure, rebuke, compromise, ignore, or promise later action.

World targets:

- Companion involved in strongest approval.
- Companion involved in strongest warning.
- Camp quartermaster/surgeon/scout role if present.
- Remembered village or refugee camp witness when relevant.

Interactive outcomes:

- Reassure: reduces immediate fracture but may create a future promise.
- Rebuke: keeps discipline but worsens mercy/freedom companions.
- Compromise: costs time, coin, food, or route purity.
- Ignore: fastest path but increases fracture pressure.

Failure and recovery:

- A companion near breaking should not instantly vanish from one menu.
- Give one recoverable warning beat when practical.
- If a companion leaves, store why and allow a later redemption or confrontation hook.

#### `qst_rtc_first_recognition`

Target-state interaction:

- Recognition should require a public witness, a protected route, or a visible deed.
- The first recognition label should be something someone says about the player in-world.

World targets:

- Lawful claimant: court witness, oath site, noble messenger.
- Free captain: rescued patrol, paid-company contract, field captain.
- Trade power: caravan master, grain broker, guild hall.
- People's defender: bread village, refugee elder, militia speaker.
- Dangerous warlord: defeated enemy captain, frightened border center.
- Shadow operator: Vaska agent, hidden ledger courier.

Interactive outcomes:

- Player can accept the label, correct it, weaponize it, or reject it.
- Recognition should alter at least one later greeting or offer.
- Bad recognition should become a rumor the Empire can exploit.

Failure and recovery:

- If recognition fails, the player should be able to seek a weaker witness or proceed with "unsettled" recognition.
- Unsettled recognition should increase later council risk rather than stop the campaign.

### Act IV: Crown Council

#### `qst_rtc_crown_council`

Target-state interaction:

- The council should be a witness assembly, not just a route lock menu.
- Each witness category should come from prior gameplay or a concrete substitute.

Witness categories:

- Noble witness: lord, court messenger, legal document, or recognized patron.
- Commoner witness: bread village, protected village, refugee camp, militia speaker.
- Company witness: companion unity, camp discipline, or named companion testimony.
- Fourth witness: faith speaker, scholar, merchant, scout, military captain, or underworld broker.

Player actions:

- Present witness.
- Challenge Maeron.
- Answer Septima.
- Use Vaska's leverage.
- Ask for delay.
- Accept a weaker lock with a future cost.

Interactive outcomes:

- A full witness set locks the route cleanly.
- A partial witness set can lock the route with vulnerability.
- A missing witness should become a named weakness in Act V.
- Vaska leverage should create underworld debt or future blackmail unless paid off.

Failure and recovery:

- The council can fracture without ending live play.
- Fracture should produce a recovery target: protect one surviving witness, expose a forged accusation, or defeat a pressure party.
- Maeron should be able to become rival, temporary ally, exile, or future claimant depending on choices.

### Act V: Imperial Shadow

#### `qst_rtc_hounds_terms`

Target-state interaction:

- The Hound's terms should arrive through an envoy party or heavily guarded messenger.
- The terms should cite real prior actions, especially the bread village and council witnesses.

World targets:

- Imperial envoy party.
- Septima's legal clerk.
- Marius's field captain.
- Threatened witness center.
- Signed terms document or seal.

Player actions:

- Reject terms publicly.
- Delay through negotiation.
- Accept terms openly.
- Accept terms while preparing betrayal.
- Detain or release the envoy.
- Send a counter-demand.

Interactive outcomes:

- Rejecting terms raises open pressure and targets witnesses.
- Delay buys time but can require hostage, coin, or route concession.
- Acceptance bends toward Imperial branch and worsens freedom/mercy companions.
- Envoy mistreatment gives Marius propaganda.

Failure and recovery:

- If talks collapse, the Empire should pick a concrete target rather than only raising a flag.
- If the envoy escapes with damaging testimony, Act V pressure should become harsher.

#### `qst_rtc_war_of_witnesses`

Target-state interaction:

- Marius attacks the claim by attacking the people, documents, routes, and places that made it believable.

World targets by route:

- Legitimacy: court witness or oath document.
- Mercenary: payroll caravan or supply road.
- Conquest: Imperial vanguard.
- Coalition: bread village, militia ally, or refugee speaker.
- Restoration: homeland survivor group or relic carrier.
- Imperial: demanded sacrifice target.
- Hidden regime-maker: ledger witness or blackmail courier.

Player actions:

- Protect directly.
- Evacuate witness.
- Use route-specific answer.
- Sacrifice one witness to save the route.
- Hand off to Last Banner side crisis.

Interactive outcomes:

- Protected witnesses strengthen final ending.
- Moved witnesses survive but become less publicly useful.
- Sacrificed witnesses preserve momentum but damage trust.
- Route-specific victory should alter final strategy recommendations.

Failure and recovery:

- A witness can be captured, scattered, discredited, killed, or compromised.
- Captured witnesses should create rescue hooks where feasible.
- Discredited witnesses should create investigation or counter-rumor hooks.

#### `qst_rtc_last_road`

Target-state interaction:

- The final strategy should be prepared through a short world action or target selection.

Strategy surfaces:

- Hold the line: choose defensive ground or protect a vulnerable center.
- Strike the Hound: identify Marius's command party or vanguard.
- Starve the Empire: hit supply caravan, depot, bridge, or tax convoy.
- Break the seal: expose forged law, captured orders, or Imperial contradiction.
- Accept the collar: choose submission, infiltration, or client-rule posture.
- Catastrophic loss: triggered by collapse, not only selected voluntarily.

Interactive outcomes:

- The chosen strategy should set final confrontation framing.
- Strong route alignment should improve final outcome text or companion morale.
- Weak route alignment should add warnings, not hard-block.

Failure and recovery:

- Failed preparation can still reach final confrontation, but with worse pressure.
- Catastrophic loss should archive a playable failure state and unlock recovery/exile content.

#### `qst_rtc_final_confrontation`

Target-state interaction:

- The final confrontation should eventually be more than a menu: battle, negotiation, public exposure, or surrender scene depending on final strategy.

Final surfaces:

- Battle against Marius or his captain.
- Public legal confrontation.
- Supply collapse negotiation.
- Imperial vassalage ceremony.
- Council refusal of personal rule.
- Collapse flight.

Interactive outcomes:

- Marius defeated: Empire pressure breaks locally.
- Marius forced back: victory with future threat.
- Marius overlord: Imperial survival route.
- Unworn crown: authority moves to council/charter/witnesses.
- Claim collapse: Crown of Ashes and exile/recovery hooks.

Failure and recovery:

- Collapse must not softlock the player.
- Final outcome should archive exactly one ending and one successor unlock.
- Later content should query the ending instead of replaying the whole chain.

### Chapter-to-Quest Mapping

The chapter IDs are authoring-level handles. The initial implementation can lower them into quest IDs as follows:

- `rtc_01_last_smoke` -> `qst_rtc_last_smoke`
- `rtc_02_borrowed_names` -> `qst_rtc_borrowed_names`
- `rtc_03_hound_sign` -> `qst_rtc_hound_sign`
- `rtc_04_door_into_calradia` -> `qst_rtc_door_into_calradia`
- `rtc_05_price_of_bread` -> `qst_rtc_price_of_bread`
- `rtc_06_banner_tested` -> `qst_rtc_banner_tested`
- `rtc_07_three_offers` -> `qst_rtc_three_offers`
- `rtc_08_companions_take_sides` -> `qst_rtc_companions_take_sides`
- `rtc_09_first_recognition` -> `qst_rtc_first_recognition`
- `rtc_10_crown_council` -> `qst_rtc_crown_council`
- `rtc_11_hounds_terms` -> `qst_rtc_hounds_terms`
- `rtc_12_war_of_witnesses` -> `qst_rtc_war_of_witnesses`
- `rtc_13_last_road` -> `qst_rtc_last_road`
- `rtc_14_final_confrontation` -> `qst_rtc_final_confrontation`

## Custom Unique NPCs

These NPCs are campaign-specific and are intended to be authored as unique troops or named dialogue agents.

### Sir Garran Ashwake

- **ID:** `npc_garran_ashwake`
- **Role:** first rescuer, bitter veteran, living link to the burned homeland.
- **Origin:** Aden or Antares border service, depending on player origin flavor.
- **Personality:** exhausted, loyal to the dead, severe but protective.
- **Function:** starts Act I, teaches the stakes, can become a camp adviser or die if ignored.
- **Route reaction:** approves duty, lawful resistance, and disciplined vengeance; disapproves profiteering from refugees.
- **Possible fate:** survives as marshal adviser, dies covering refugees, leaves if the player joins the Empire.

Sample first line:

> "Do not look back too long. Ash has a way of teaching the feet to stop."

### Lysara Veyne

- **ID:** `npc_lysara_veyne`
- **Role:** refugee chronicler, narrator, archive keeper.
- **Origin:** Villian-educated scribe from the lost homeland's diplomatic circles.
- **Personality:** observant, wounded, dry, brave when truth is at stake.
- **Function:** records campaign choices, frames act transitions, preserves names of the dead.
- **Route reaction:** approves truth, restraint, and restoration; fears Void and bloodlust paths.
- **Possible fate:** writes the player's coronation record, exposes the player, or becomes the voice of the exile ending.

Sample line:

> "A crown is only metal until someone writes what was done beneath it."

### Hafiz al-Qadir

- **ID:** `npc_hafiz_al_qadir`
- **Role:** Zerrikanian scout-master and frontier guide.
- **Origin:** Zerrikania.
- **Personality:** proud, amused by settled panic, hates waste.
- **Function:** opens mobile defense, raiding, scouting, and steppe coalition options.
- **Route reaction:** approves speed, independence, clever retreats; dislikes static court paralysis.
- **Possible fate:** becomes master of scouts, returns to the steppe, or challenges the player over imperial submission.

Sample line:

> "Stone walls are useful. So is knowing when to leave them behind."

### Domina Celeste di Marina

- **ID:** `npc_celeste_di_marina`
- **Role:** merchant exile, contract broker, hard-headed logistician.
- **Origin:** Marina.
- **Personality:** elegant, ruthless with numbers, more compassionate than she admits.
- **Function:** unlocks trade route objectives, supply reforms, mercenary contracts, Crown of Coin route.
- **Route reaction:** approves paid order, protected caravans, strategic bribery; condemns pointless sackings.
- **Possible fate:** becomes chancellor of trade, underworld broker, or hostile creditor.

Sample line:

> "Sentiment feeds no army. But neither does cruelty, once the villages are empty."

### Brother Odran of the Road

- **ID:** `npc_brother_odran`
- **Role:** wandering priest, refugee healer, moral witness.
- **Faith affinity:** The One, but can debate all faiths.
- **Personality:** gentle voice, iron spine, refuses to flatter power.
- **Function:** provides mercy objectives, burial scenes, oath ceremonies, faith-linked legitimacy.
- **Route reaction:** approves mercy and lawful restraint; may publicly denounce cruelty.
- **Possible fate:** crowns the player, refuses the coronation, dies in a refugee camp, or leads a relief order.

Sample line:

> "You may win every field and still lose the road that brought you here."

### Vaska the Black Ledger

- **ID:** `npc_vaska_black_ledger`
- **Role:** underworld broker, smuggler, information seller.
- **Origin:** unknown; claims Marina, speaks like everywhere.
- **Personality:** charming, dangerous, fond of exact prices.
- **Function:** intrigue route contact, secret branch unlock, betrayal-route enabler.
- **Route reaction:** approves leverage, secrets, and profitable restraint; punishes naivety.
- **Possible fate:** ally, blackmailer, executed witness, or hidden kingmaker.

Sample line:

> "Everyone has a price. The trick is learning whether they know it."

### Tamsin Reedhand

- **ID:** `npc_tamsin_reedhand`
- **Role:** village militia leader and voice of common Calradia.
- **Origin:** Calradian commoner.
- **Personality:** practical, suspicious of noble claims, protective of her people.
- **Function:** grounds the campaign in village consequences; unlocks coalition-with-commoners route.
- **Route reaction:** approves protection, fair taxes, food security; despises requisition without payment.
- **Possible fate:** becomes captain of the people's levy, rebel against the player, or martyr in Act V.

Sample line:

> "Lords talk of borders. We count roofs that still have smoke from the chimney."

### Prince-Captain Maeron Vald

- **ID:** `npc_maeron_vald`
- **Role:** rival claimant, mirror of the player.
- **Origin:** Antares or Villian bloodline, adjusted by player origin.
- **Personality:** charismatic, proud, increasingly desperate.
- **Function:** Act IV rival in legitimacy and restoration routes.
- **Route reaction:** can be ally, rival, claimant to defeat, or dynastic partner in a future diplomacy layer.
- **Possible fate:** duel death, negotiated abdication, exile, co-ruler, or imperial collaborator.

Sample line:

> "You call yourself chosen by loss. So do I. The dead are generous with crowns."

### Legate Gaius Marius, the Imperial Hound

- **ID:** `npc_gaius_marius`
- **Role:** final antagonist, imperial commander, embodiment of disciplined conquest.
- **Origin:** Imperial.
- **Personality:** calm, precise, predatory, respectful only of useful strength.
- **Function:** pressure source from Act I, direct opponent in Act V.
- **Route reaction:** offers terms to lawful, mercenary, conquest, and betrayal players differently.
- **Possible fate:** defeated, slain, captured, bargained with, replaced, or acknowledged as overlord.

Sample line:

> "I do not hate the lands I take. Hatred is for men who plan to leave things standing."

### Septima Varro

- **ID:** `npc_septima_varro`
- **Role:** imperial envoy, legal mind, soft face of conquest.
- **Origin:** Imperial.
- **Personality:** polished, patient, sincerely convinced empire prevents chaos.
- **Function:** opens imperial route, peace-with-empire talks, surrender and vassalage branches.
- **Route reaction:** respects order, coin, and logic; dismisses revenge and ritual legitimacy.
- **Possible fate:** hostage, treaty architect, betrayed envoy, late-game administrator.

Sample line:

> "Your people need not die for a word like freedom when another word, province, will feed them."

### The Ashen Herald

- **ID:** `npc_ashen_herald`
- **Role:** masked messenger tied to lost homeland rumors.
- **Origin:** ambiguous; may be survivor, imperial plant, or radical restorer.
- **Personality:** ceremonial, unsettling, speaks in fragments.
- **Function:** hidden restoration and Void-adjacent route hook.
- **Route reaction:** appears only under specific identity/branch conditions.
- **Possible fate:** revealed as survivor network leader, imperial lure, or symbolic mantle inherited by the player.

Sample line:

> "The road does not end at the crown. It ends where the ashes are named."

## Campaign Structure

The campaign is divided into five acts. Each act is implementable as a sequence of quest chains with optional branch beats.

## Act I: Ashes and Arrival

### Act Summary

- **Act ID:** `act_01_ashes`
- **Purpose:** establish exile, immediate danger, refugee stakes, and the first Imperial Hound pressure.
- **Primary question:** "What are you now that home is gone?"
- **Core NPCs:** Garran Ashwake, Lysara Veyne, Brother Odran, Hafiz al-Qadir or Celeste di Marina depending on route.
- **Primary locations:** border road, refugee camp, burned caravan site, first Calradian town.

### Chapter 1: The Last Smoke

- **Chapter ID:** `rtc_01_last_smoke`
- **Quest ID:** `qst_rtc_last_smoke`
- **Entry:** campaign starts after character creation.
- **Objective:** reach the refugee camp before imperial scouts overrun the road.
- **Gameplay targets:** small battle, escort, menu choice, first camp dialogue.

Objective steps:

1. Find survivors on the road.
2. Choose whether to save baggage, wounded people, or military papers.
3. Defeat or evade an imperial scout party.
4. Reach the camp before nightfall.
5. Speak to Garran and Lysara.

Choice outcomes:

- **Save baggage:** gain supplies and trade credibility; lose some refugee trust.
- **Save wounded:** gain mercy trust; lose supplies.
- **Save military papers:** unlock early Imperial intelligence; Garran approval rises.
- **Abandon the road fight:** faster arrival; `reputation_refugee` plus `companion_wary_mercy`.

Journal text:

```md
The road behind you is smoke. The road ahead is Calradia. Between them are the living, the wounded, and the first men of the Empire who have not yet learned your name.
```

### Chapter 2: The Camp of Borrowed Names

- **Chapter ID:** `rtc_02_borrowed_names`
- **Quest ID:** `qst_rtc_borrowed_names`
- **Objective:** stabilize the refugee camp and choose the first public identity.
- **Gameplay targets:** camp menu, resource choice, dialogue web, small reputation assignment.

Public identity choices:

- "I am a noble of a fallen house." -> `reputation_foreign_noble`
- "I am a captain looking for work." -> `reputation_free_captain`
- "I am a trader with surviving contacts." -> `reputation_trade_operator`
- "I am only another exile." -> `reputation_refugee`
- "I am the hand that will answer this." -> `reputation_avenger`

NPC reactions:

- Garran approves captain, noble, and avenger if disciplined.
- Lysara approves truthful refugee and noble lines.
- Odran approves refugee and peace-leaning statements.
- Celeste approves trader.
- Hafiz approves captain and exile.

Sample dialogue:

```md
Lysara: "What name should I write beside yours?"

Player:
- "The name I was born with. Let them know what survived."
- "No house. No titles. Only the company I keep."
- "Write nothing yet. Names are debts."
- "Write that I am owed blood."
- "Write that I intend to buy us another morning."
```

### Chapter 3: Hound Sign

- **Chapter ID:** `rtc_03_hound_sign`
- **Quest ID:** `qst_rtc_hound_sign`
- **Objective:** investigate proof that Gaius Marius is moving toward Calradia.
- **Gameplay targets:** scouting, prisoner interrogation, optional stealth, first imperial evidence.

Evidence options:

- captured courier seal
- burned map with Calradian routes
- survivor testimony
- imperial ration tokens
- coded order naming "pacification corridors"

Branch seeds:

- Duelist can challenge the scout captain.
- Intriguer can steal the order without battle.
- Philosopher can parse imperial doctrine and warn Calradian leaders.
- Trader can identify supply contracts and predict the route.

Act I completion state:

- Set `imperial_pressure_low`.
- Set one public reputation flag.
- Unlock first standing routes in Act II.
- Store `act_01_choice_saved_baggage`, `act_01_choice_saved_wounded`, or `act_01_choice_saved_papers`.

## Act II: Choosing a Life

### Act Summary

- **Act ID:** `act_02_choice`
- **Purpose:** turn character creation identity into visible Calradian social access.
- **Primary question:** "How will you enter this broken land?"
- **Primary locations:** town court, market, arena, monastery/scholarly house, caravan yard, tavern.

Act II does not split into five entirely separate campaigns. It provides four to six early quest chains that can be selected in different order, with identity-specific text and rewards.

### Chapter 1: A Door Into Calradia

- **Chapter ID:** `rtc_04_door_into_calradia`
- **Quest ID:** `qst_rtc_door_into_calradia`
- **Objective:** gain a patron, contract, or public witness.

Entry contacts by identity:

- `origin_antares`: Lord Edwyn Harrowmont, a minor noble interested in foreign legitimacy.
- `origin_marina`: Guildmaster Orsino Bell, a merchant with caravan losses.
- `origin_aden`: Captain Radec of the East Gate, seeking disciplined fighters.
- `origin_villian`: Lady Ysabet de Rienne, court patron and gossip broker.
- `origin_zerrikania`: Hafiz al-Qadir or a horse trader named Batuq.

Faith overlays:

- The One: oath language appears.
- Old Gods: memorial rite appears.
- Void: secret observer appears.
- Enlightenment: debate scene appears.
- Natural Philosophy: practical evidence scene appears.

Objective variants:

- win a public duel
- escort a caravan
- expose a false witness
- mediate a refugee dispute
- recover stolen grain
- protect a village from deserters

### Chapter 2: The Price of Bread

- **Chapter ID:** `rtc_05_price_of_bread`
- **Quest ID:** `qst_rtc_price_of_bread`
- **Objective:** resolve a food crisis between refugees and locals.
- **Core NPCs:** Tamsin Reedhand, Celeste di Marina, Brother Odran.
- **Purpose:** early moral test that affects commoner trust and trade access.

Resolution choices:

- **Pay fairly:** costs coin; improves `commoner_trust`.
- **Requisition by force:** immediate food; creates `village_fear` and possible later rebellion.
- **Negotiate labor for grain:** balanced route; requires speech/trade.
- **Expose hoarding merchant:** improves commoner trust; damages merchant access unless evidence is solid.
- **Raid bandit stores:** battle route; high risk but broad approval.

Sample dialogue:

```md
Tamsin: "You want grain because your people are hungry. Mine are hungry without the poetry."

Player:
- "Then I will pay, and if I cannot pay enough, I will owe you openly."
- "Open the stores. I will remember who refused the dying."
- "Give me ten workers and two carts. I will bring back what the bandits took."
- "Someone is making profit from both our hungers. Give me a name."
```

### Chapter 3: A Banner Tested

- **Chapter ID:** `rtc_06_banner_tested`
- **Quest ID:** `qst_rtc_banner_tested`
- **Objective:** choose an early public method.

Route tests:

- **Honor test:** duel a slandering captain without killing him.
- **Intrigue test:** learn who hired the slanderer.
- **Trade test:** settle damages with contract terms.
- **Philosophy test:** publicly answer the accusation and win witnesses.
- **Faith test:** swear or refuse a public oath.

Failure does not end the campaign. It sets:

- `reputation_unproven`
- one faction `suspicious`
- one companion `wary`
- a cheaper but less honorable recovery quest in Act III

Act II completion state:

- Set one social-method flag: `method_honor`, `method_intrigue`, `method_trade`, `method_counsel`, or `method_faith`.
- Raise or lower `commoner_trust`, `merchant_trust`, `noble_trust`, or `underworld_notice`.
- Unlock companion-specific campfire reactions.

## Act III: Building Standing

### Act Summary

- **Act ID:** `act_03_standing`
- **Purpose:** make the player politically visible and militarily useful.
- **Primary question:** "Are you trying to survive, or are you trying to rule?"
- **Primary locations:** contested village, faction court, caravan road, ruined fort, tavern intelligence network.

Act III is the first act where failure can permanently close a route or create a harder branch.

### Chapter 1: The Three Offers

- **Chapter ID:** `rtc_07_three_offers`
- **Quest ID:** `qst_rtc_three_offers`
- **Objective:** choose one of three simultaneous offers.

Offer A: Noble Protection

- Given by Lady Ysabet or Lord Harrowmont.
- Protect a noble convoy and attend court afterward.
- Seeds `branch_legitimacy`.

Offer B: Paid Steel

- Given by Celeste or a faction marshal.
- Break a siege camp, rescue a payroll, or enforce a contract.
- Seeds `branch_mercenary` or `branch_conquest`.

Offer C: The People's Road

- Given by Tamsin or Odran.
- Secure villages and refugee traffic without noble permission.
- Seeds `branch_coalition` or `branch_reform`.

Hidden Offer D: The Quiet Ledger

- Given by Vaska if `life_intriguer`, `faith_void`, or underworld notice is high.
- Steal imperial route information from a protected agent.
- Seeds `branch_betrayal`, `branch_hidden_regime_maker`, or `branch_imperial`.

### Chapter 2: Companions Take Sides

- **Chapter ID:** `rtc_08_companions_take_sides`
- **Quest ID:** `qst_rtc_companions_take_sides`
- **Objective:** hold the company together after the first major political choice.
- **Gameplay target:** camp dialogue sequence with approval states.

Companion reaction matrix:

- **Borcha:** approves survival logic, scouting, flexible morality; dislikes ceremonial delays.
- **Marnid:** approves trade, stable contracts, protected routes; dislikes unpaid wars.
- **Ymira:** approves mercy and refugee protection; warns against vengeance.
- **Rolf:** approves title, public recognition, noble theater; dislikes being treated as a mere sellsword.
- **Baheshtur:** approves freedom, mobility, pride; dislikes kneeling to weak lords.
- **Firentis:** approves discipline, penance, just war; rejects slaughter.
- **Deshavi:** approves helping villages and the poor; distrusts nobles and requisitions.
- **Matheld:** approves courage and direct action; respects decisive war.
- **Alayen:** approves honor and noble duty; rejects dirty tricks if exposed.
- **Bunduk:** approves soldier welfare and practical command; hates wasting common soldiers.
- **Katrin:** approves stores, pay, camp survival; dislikes romantic risks.
- **Jeremus:** approves restraint and healing; may threaten departure after cruelty.
- **Nizar:** approves glory, audacity, public victories; dislikes dull compromise.
- **Lezalit:** approves order and harsh efficiency; dismisses soft mercy.
- **Artimenner:** approves preparation, roads, siege planning; dislikes improvisation.
- **Klethi:** approves stealth, leverage, opportunism; dislikes pomp.

Warning dialogue examples:

```md
Ymira: "If every grave becomes a reason for another grave, when do we stop digging?"

Lezalit: "Mercy is useful after discipline has made it safe."

Marnid: "A crown that cannot pay wages is only a hat with witnesses."

Bunduk: "Ask the men what they think of glory when the boots split."
```

### Chapter 3: The First Recognition

- **Chapter ID:** `rtc_09_first_recognition`
- **Quest ID:** `qst_rtc_first_recognition`
- **Objective:** force a faction, town, or rival captain to recognize the player's company.

Recognition methods:

- win a field battle
- negotiate a prisoner exchange
- expose an imperial spy
- secure a caravan road
- defend a village without orders
- defeat Maeron Vald's champion

Recognition outcomes:

- `recognized_as_lawful_claimant`
- `recognized_as_free_captain`
- `recognized_as_trade_power`
- `recognized_as_people_defender`
- `recognized_as_dangerous_warlord`
- `recognized_as_shadow_operator`

Act III completion state:

- Set one route seed.
- Set at least two faction memory states.
- Set companion warning or support state.
- Raise `imperial_pressure_rising`.
- Unlock Act IV Crown Council.

## Act IV: The Crown Question

### Act Summary

- **Act ID:** `act_04_crown`
- **Purpose:** force the player to define the kind of authority they are building.
- **Primary question:** "What gives you the right?"
- **Primary locations:** faction court, captured keep, refugee assembly, merchant council, war camp, secret parley.

Act IV is the main branch act. It contains different quest chains that share some locations and NPCs but diverge in objectives and outcomes.

### Crown Council Setup

- **Chapter ID:** `rtc_10_crown_council`
- **Quest ID:** `qst_rtc_crown_council`
- **Objective:** gather witnesses and answer challenges to the player's authority.

Required witnesses:

- one noble or faction representative
- one commoner or village representative
- one companion or company officer
- one faith, scholar, merchant, or military witness

Opposition:

- Maeron Vald challenges the player's claim.
- Septima Varro offers imperial recognition in exchange for submission.
- Vaska offers evidence that can ruin a rival at moral cost.
- Tamsin demands protections for villages.
- Celeste demands a binding supply charter.
- Brother Odran asks what law will restrain the player.

Sample council challenge:

```md
Maeron Vald: "You have victories. So does every brigand with enough horses. Where is your right?"

Player:
- "In law, witness, and the oaths I will bind myself to."
- "In the roads I keep open and the wages I pay."
- "In the enemies I have broken."
- "In the hands that choose to stand together behind me."
- "In the dead, whose names I have not traded away."
- "In the Empire's seal, if Calradia is too proud to save itself."
```

### Branch A: Legitimacy

- **Branch ID:** `branch_legitimacy`
- **Crown meaning:** recognized lawful authority.
- **Best fit:** Antares, Villian, The One, Enlightenment, duelist, philosopher, peace.
- **Primary NPCs:** Lysara, Rolf, Alayen, Brother Odran, Maeron Vald.

Objectives:

1. Secure noble witness.
2. Resolve a succession or oath dispute.
3. Win public recognition without massacring opposition.
4. Draft a restraint oath.
5. Defeat or reconcile Maeron.

Key choices:

- accept an imperfect noble alliance
- expose a noble crime and lose support
- marry or bind houses if future systems support it
- recognize commoner protections as part of legitimacy
- stage trial by combat or trial by witness

Failure risks:

- `failed_legitimacy_public_shame`
- Maeron gains claim strength
- Rolf or Alayen becomes troubled
- commoners call the player another foreign lord

### Branch B: Mercenary Power

- **Branch ID:** `branch_mercenary`
- **Crown meaning:** paid authority, control through contracts and logistics.
- **Best fit:** Marina, Natural Philosophy, trader, riches, Marnid/Katrin support.
- **Primary NPCs:** Celeste, Marnid, Katrin, Vaska, faction marshals.

Objectives:

1. Secure a regional supply contract.
2. Protect caravans from both bandits and faction abuse.
3. Force a noble to honor payment.
4. Decide whether to break a dirty contract.
5. Convert paid service into political leverage.

Key choices:

- take lower pay for clean legitimacy
- enforce debt brutally
- redirect supplies to refugees
- sell intelligence to competing factions
- form a merchant league

Failure risks:

- `failed_mercenary_unpaid_company`
- troop morale drops
- Marnid becomes troubled if trust is squandered
- Celeste becomes creditor or antagonist

### Branch C: Conquest

- **Branch ID:** `branch_conquest`
- **Crown meaning:** authority through victory and fear.
- **Best fit:** Aden, Zerrikania, duelist, revenge, bloodlust, Matheld/Lezalit support.
- **Primary NPCs:** Garran, Hafiz, Lezalit, Matheld, Maeron, imperial scouts.

Objectives:

1. Break a rival warband or claimant force.
2. Capture a strategic fort.
3. Decide how to treat surrendered enemies.
4. Defeat a punitive faction army.
5. Announce rule by strength or convert victory into law.

Key choices:

- execute enemy captains
- spare enemies for oath service
- burn supplies to deny the Empire
- seize grain from neutral villages
- use terror to end resistance quickly

Failure risks:

- `failed_conquest_overextended`
- villages revolt or empty
- Jeremus/Ymira/Firentis may become near breaking
- imperial pressure rises faster because the player looks like a useful rival to crush

### Branch D: Coalition

- **Branch ID:** `branch_coalition`
- **Crown meaning:** leadership by negotiated survival.
- **Best fit:** peace motive, philosopher, Villian, Enlightenment, mixed companion support.
- **Primary NPCs:** Tamsin, Odran, Lysara, Celeste, Hafiz, selected faction envoys.

Objectives:

1. Bring two hostile local powers to the same table.
2. Secure food, patrols, and hostage guarantees.
3. Resolve a revenge demand without collapsing talks.
4. Expose or absorb an imperial disruption attempt.
5. Form a provisional league against the Imperial Hound.

Key choices:

- sacrifice speed for consensus
- force compromise with military pressure
- pardon a hated enemy for alliance value
- let common villages sign the charter
- give merchants voting power in war logistics

Failure risks:

- `failed_coalition_fractured_table`
- one faction defects to the Empire
- companions split between mercy, honor, and practicality
- Act V begins with fewer allied forces

### Branch E: Restoration

- **Branch ID:** `branch_restoration`
- **Crown meaning:** homeland memory reborn as banner, law, or return.
- **Best fit:** Antares, Old Gods, The One, revenge or peace, Lysara/Garran/Odran support.
- **Primary NPCs:** Lysara, Garran, Ashen Herald, Maeron, Septima.

Objectives:

1. Recover names, relics, or survivors from the lost homeland.
2. Decide whether restoration means return, revenge, or new settlement.
3. Confront Maeron or the Ashen Herald over who owns the memory of the dead.
4. Bind refugees into a political body.
5. Declare the restored banner.

Key choices:

- preserve the old name
- found a new name
- punish collaborators
- accept Calradian allies into the restored identity
- trade return for survival

Failure risks:

- `failed_restoration_empty_symbol`
- refugees fracture
- Lysara exposes hypocrisy
- Garran dies or leaves in disillusionment

### Branch F: Imperial Accommodation

- **Branch ID:** `branch_imperial`
- **Crown meaning:** survival through imperial recognition, submission, or weaponized collaboration.
- **Best fit:** Natural Philosophy, intrigue, riches, exhausted coalition, betrayal path.
- **Primary NPCs:** Septima Varro, Gaius Marius, Vaska, Celeste.

Objectives:

1. Meet Septima under truce.
2. Decide whether to trade information, hostages, or territory.
3. Suppress anti-imperial resistance or secretly double-cross the Empire.
4. Receive provisional imperial title or reject it at the final condition.
5. Face company backlash.

Key choices:

- accept province status to spare refugees
- betray a faction to buy time
- feed false intelligence to the Empire
- become imperial client ruler
- lure Marius into overconfidence

Failure risks:

- `failed_imperial_marked_traitor`
- companions depart or revolt
- all major factions become hostile or suspicious
- Act V starts with high imperial pressure but possible internal access

### Hidden Branch: Regime Maker

- **Branch ID:** `branch_hidden_regime_maker`
- **Unlock conditions:** at least moderate legitimacy, controlled fear, coalition trust, and stable supplies.
- **Crown meaning:** authority that combines law, force, logistics, and witness.
- **Primary NPCs:** Lysara, Celeste, Tamsin, Garran, Odran, Vaska.

This branch is hidden because it is not chosen by a single speech option. It emerges if the player has avoided extremes while still making hard decisions.

Requirements:

- one noble witness
- one commoner charter
- one protected supply route
- one decisive military victory
- no companion at `broken`
- no more than one major faction at `retaliating`

Outcome:

- unlocks the strongest stable-rule ending if Act V is handled well
- permits a unified anti-imperial war plan
- reduces rebellion risk after victory

Act IV completion state:

- Lock primary branch unless hidden branch overrides.
- Set `crown_claim_declared`.
- Set `imperial_pressure_open`.
- Store major witnesses and opponents.
- Unlock Act V based on route.

## Act V: The Imperial Shadow

### Act Summary

- **Act ID:** `act_05_shadow`
- **Purpose:** resolve the campaign against the Imperial Hound pressure.
- **Primary question:** "What will your crown do when the Empire arrives?"
- **Primary locations:** border fortress, war council, refugee road, imperial camp, final battlefield or treaty hall.

Act V adapts to the route chosen in Act IV but reuses a shared imperial pressure structure.

### Chapter 1: The Hound's Terms

- **Chapter ID:** `rtc_11_hounds_terms`
- **Quest ID:** `qst_rtc_hounds_terms`
- **Objective:** receive and answer Gaius Marius's terms.

Terms vary by branch:

- **Legitimacy:** surrender crown in exchange for recognized local governorship.
- **Mercenary:** take imperial pay and turn on Calradian employers.
- **Conquest:** meet Marius in battle or be crushed as rival warlord.
- **Coalition:** break the coalition by offering separate peace to each member.
- **Restoration:** trade the homeland's surviving captives or relics for obedience.
- **Imperial:** prove loyalty by sacrificing a named ally.
- **Regime Maker:** Marius offers respect, then total war.

Sample dialogue:

```md
Gaius Marius: "You have built something from smoke. I admire that. Now I will give it a shape that can last."

Player:
- "It already has a shape. You are standing outside it."
- "Name your price. Then hear mine."
- "I did not cross ash and winter to kneel on better carpet."
- "If empire is order, why does it always arrive hungry?"
- "I will take your seal. I will not take your chain."
```

### Chapter 2: War of Witnesses

- **Chapter ID:** `rtc_12_war_of_witnesses`
- **Quest ID:** `qst_rtc_war_of_witnesses`
- **Objective:** protect or exploit the people whose support made the player's crown possible.

Possible targets:

- refugee camp
- supply caravan
- commoner militia village
- noble hostage convoy
- merchant ledger house
- sacred memorial site
- captured imperial defector

Route variants:

- Legitimacy protects witnesses from assassination.
- Mercenary protects payroll and supply routes.
- Conquest breaks an imperial vanguard.
- Coalition prevents ally defection.
- Restoration rescues homeland survivors.
- Imperial proves loyalty or stages a double-cross.
- Regime Maker coordinates all objectives with fewer losses.

### Chapter 3: The Last Road

- **Chapter ID:** `rtc_13_last_road`
- **Quest ID:** `qst_rtc_last_road`
- **Objective:** choose final strategy.

Final strategy choices:

1. **Hold the Line**  
   Defensive battle. Best with coalition, legitimacy, high commoner trust.

2. **Strike the Hound**  
   Decapitation raid or field battle. Best with conquest, duelist, high army strength.

3. **Starve the Empire**  
   Logistics and trade warfare. Best with Marina, trader, mercenary route.

4. **Break the Seal**  
   Expose imperial lies or legal contradictions. Best with philosopher, intrigue, legitimacy.

5. **Sacrifice the Border**  
   Give ground to save core forces. Best with cold pragmatic routes; hurts commoner trust.

6. **Accept the Collar**  
   Submit, infiltrate, or become client ruler. Imperial route only.

7. **Return Through Fire**  
   Use the crisis to reclaim or symbolically restore the lost homeland. Restoration route.

### Chapter 4: Final Confrontation

- **Chapter ID:** `rtc_14_final_confrontation`
- **Quest ID:** `qst_rtc_final_confrontation`
- **Objective:** resolve Marius and the crown.

Possible confrontation forms:

- battlefield duel with Marius's champion
- siege defense
- treaty hall confrontation
- ambush of imperial command
- public trial of collaborators
- refugee evacuation under attack
- imperial investiture ceremony turned reversal

Marius fate options:

- slain in battle
- captured and ransomed
- forced to withdraw
- politically humiliated
- accepted as overlord
- escapes to become future antagonist
- replaced by an even harsher imperial command if the player uses betrayal poorly

Act V completion state:

- Set final ending flag.
- Archive route branch.
- Apply companion end states.
- Set faction memory for follow-up campaigns.
- Unlock post-campaign content.

## Endings

### Ending 1: Crown of Law

- **Flag:** `ending_crown_of_law`
- **Required:** legitimacy route or regime maker; stable witnesses; low cruelty.
- **Result:** player becomes recognized ruler or lawful claimant with enforceable oaths.
- **World effect:** noble trust rises, rebellion risk lowers, some radicals remain unhappy.
- **Companion effect:** Rolf, Alayen, Firentis likely steady; Klethi or Baheshtur may be wary.
- **Unlocks:** governance campaigns, succession disputes, noble reconciliation.

Ending narration:

```md
The crown was not taken in a single battle. It was argued, witnessed, sworn, and paid for in restraint. Some called that weakness. They learned, in time, that law can have teeth.
```

### Ending 2: Crown of Iron

- **Flag:** `ending_crown_of_iron`
- **Required:** conquest route; major military victory; fear above legitimacy.
- **Result:** player rules by strength and deterrence.
- **World effect:** banditry falls, rebellions become harsher, diplomacy suffers.
- **Companion effect:** Lezalit and Matheld likely steady; Ymira/Jeremus/Firentis may be troubled or broken.
- **Unlocks:** rebellion campaigns, military reform, tyrant or protector follow-ups.

### Ending 3: Crown of Coin

- **Flag:** `ending_crown_of_coin`
- **Required:** mercenary or trade route; supply victory; merchant trust high.
- **Result:** player controls roads, pay, caravans, and contracts more than formal thrones.
- **World effect:** trade improves, nobles resent dependency, underworld pressure may rise.
- **Companion effect:** Marnid, Katrin, Artimenner steady; honor companions may be wary.
- **Unlocks:** merchant league campaigns, trade war, city charter reforms.

### Ending 4: Crown of Ashes

- **Flag:** `ending_crown_of_ashes`
- **Required:** collapse, overreach, betrayal spiral, or failure to protect witnesses.
- **Result:** player survives but the claim fails or the people scatter.
- **World effect:** imperial pressure remains, refugees suffer, faction trust collapses.
- **Companion effect:** departures likely; Lysara writes a bitter record.
- **Unlocks:** exile claimant campaign, redemption arc, revenge remnant arc.

### Ending 5: Crown of Faith

- **Flag:** `ending_crown_of_faith`
- **Required:** strong faith route; moral consistency; Odran or equivalent witness.
- **Result:** player creates a religious or moral settlement that legitimizes rule.
- **World effect:** faith-aligned support rises, opposing worldviews become suspicious.
- **Companion effect:** faith-compatible companions steady; skeptics wary if policy becomes rigid.
- **Unlocks:** schism campaigns, reform councils, holy war or peace order arcs.

### Ending 6: Crown of Vengeance

- **Flag:** `ending_crown_of_vengeance`
- **Required:** revenge motive dominant; Marius or collaborators punished.
- **Result:** justice or revenge is achieved, but its cost depends on mercy choices.
- **World effect:** enemies fear the player; peace settlement becomes harder.
- **Companion effect:** Garran may approve or mourn; mercy companions react to excess.
- **Unlocks:** aftermath of reprisals, survivor reckoning, blood-debt campaigns.

### Ending 7: Crown of Return

- **Flag:** `ending_crown_of_return`
- **Required:** restoration route; refugees unified; homeland memory preserved or reborn.
- **Result:** the player restores a people, name, banner, or route home.
- **World effect:** refugee identity becomes permanent factional or cultural force.
- **Companion effect:** Lysara and Garran central; Odran approves if restoration avoids cruelty.
- **Unlocks:** homeland restoration, settlement founding, lost heir disputes.

### Ending 8: Crown of the Empire

- **Flag:** `ending_crown_of_empire`
- **Required:** imperial route; accommodation, collaboration, or successful double-cross.
- **Result:** player becomes imperial client, imperial rival, or imperial successor figure.
- **World effect:** Calradian faction trust heavily altered; imperial systems enter later campaigns.
- **Companion effect:** many companions may become wary or broken unless the route saved lives convincingly.
- **Unlocks:** province governance, rebellion, imperial civil war, liberation campaign.

### Secret Ending: The Unworn Crown

- **Flag:** `ending_unworn_crown`
- **Required:** player rejects personal rule after defeating or neutralizing imperial pressure; coalition or reform trust high.
- **Result:** authority is vested in a council, charter, league, or restored community instead of the player.
- **World effect:** short-term instability but high moral legitimacy.
- **Companion effect:** peace and mercy companions strongly approve; ambition companions disappointed.
- **Unlocks:** republic/league campaign, constitutional crisis, protector without throne arc.

## Dialog Implementation Notes

Dialogue uses a repeated structure:

- identity-specific greeting
- route-specific challenge
- motive-specific emotional line
- companion interruption when relevant
- final player response that sets or confirms a flag

### Dialogue Tone Rules

- Antares lines sound educated, formal, and burdened by memory.
- Marina lines sound contractual, practical, and precise.
- Aden lines sound disciplined and oath-aware.
- Villian lines sound socially fluent and reputation-aware.
- Zerrikania lines sound direct, mobile, and proud.
- The Void is ominous but not cartoonish.
- Natural Philosophy avoids mystical language and favors consequence.
- Revenge is sharp but not always foolish.
- Peace is strong, not passive.
- Bloodlust tempts the player with momentum and glory.
- Riches are rooted in fear of helplessness, not simple greed.

### Reusable Player Response Families

Lawful:

```md
"Then let it be witnessed, sworn, and answerable."
```

Mercenary:

```md
"Put the terms in writing. Then we will see whose word still has weight."
```

Conquest:

```md
"Rights are remembered after victory. Stand aside or become proof."
```

Coalition:

```md
"No one here has enough strength alone. That is not shame. That is arithmetic."
```

Restoration:

```md
"The dead do not command me. They remind me what must not be lost twice."
```

Imperial:

```md
"If empire is the storm, then I will decide whether to be shelter, blade, or lightning rod."
```

## Narrative Interludes

Interludes fire at act transitions and major branch locks. They can be delivered by Lysara, a menu narration, or companion campfire scenes.

### Act I to Act II

```md
The first nights in Calradia did not feel like arrival. They felt like delay. Behind you, smoke. Ahead, lords too busy with old grudges to see the shape moving beyond the hills.
```

### Act II to Act III

```md
By then, people had begun to use your name when asking for help, payment, protection, or blame. That was the first sign of power: not obedience, but expectation.
```

### Act III to Act IV

```md
Every road you guarded, every oath you took, every corpse left unburied or spared had become an argument. Calradia was ready to ask the question all armed men fear: by what right?
```

### Act IV to Act V

```md
The answer reached the Empire before your messengers returned. The Hound had heard there was a crown on the road. He came to decide whether it would be worn, broken, or branded with his seal.
```

## Objective and Quest Journal Examples

These are target-state journal lines for later lowering.

### `qst_rtc_last_smoke`

- Find survivors along the burned road.
- Choose what can be saved before the scouts arrive.
- Escort the survivors to the camp.
- Defeat, evade, or misdirect the imperial scouts.
- Speak with Garran Ashwake.

Success text:

```md
You brought survivors through the smoke. Not all of them. Enough for your name to be spoken beside the fire.
```

Failure text:

```md
The road emptied behind you. The camp received fewer mouths, fewer witnesses, and fewer reasons to trust your promises.
```

### `qst_rtc_price_of_bread`

- Speak to Tamsin Reedhand.
- Learn why the village will not release grain.
- Find payment, proof of hoarding, substitute supplies, or force.
- Resolve the dispute before hunger becomes violence.

Success text:

```md
The grain was measured, argued over, cursed, and finally moved. No one called it justice. They called it supper.
```

### `qst_rtc_crown_council`

- Gather a noble witness.
- Gather a common witness.
- Gather a company witness.
- Answer Maeron Vald's challenge.
- Declare what kind of authority you seek.

Success text:

```md
The council did not give you a crown. It gave you something more dangerous: witnesses who would remember what you promised.
```

### `qst_rtc_hounds_terms`

- Receive Septima Varro or Gaius Marius under truce.
- Hear the imperial terms.
- Consult companions or advisers.
- Accept, reject, twist, or delay the terms.

Success text:

```md
The Hound's offer left the camp quieter than any threat. Some men fear death. Others fear being given a reason to kneel.
```

## Companion Integration

Companion reactions are stored separately from branch flags. The same branch can feel different depending on whether the player used restraint, payment, mercy, or betrayal.

Recommended companion states:

- `steady`
- `wary`
- `troubled`
- `near_breaking`
- `broken`
- `redeemed`

### Major Companion Tests

#### Mercy Test

- Triggered by: wounded refugees, prisoners, surrendered enemies.
- Strong reactions: Ymira, Jeremus, Firentis, Bunduk.
- Cruel outcome risk: mercy companions move toward `near_breaking`.

#### Pay Test

- Triggered by: unpaid wages, broken contracts, caravan obligations.
- Strong reactions: Marnid, Katrin, Bunduk, Artimenner.
- Failure risk: morale loss and mercenary route instability.

#### Honor Test

- Triggered by: duel, oath, public accusation, noble betrayal.
- Strong reactions: Alayen, Rolf, Firentis, Matheld.
- Failure risk: legitimacy route shame.

#### Freedom Test

- Triggered by: vassalage, imperial submission, strict rule.
- Strong reactions: Baheshtur, Deshavi, Klethi, Borcha.
- Failure risk: coalition and Zerrikanian content weakens.

#### Order Test

- Triggered by: camp discipline, siege decisions, punishment.
- Strong reactions: Lezalit, Bunduk, Garran, Artimenner.
- Failure risk: conquest route overextension or disorder.

## Faction and World Effects

The campaign does not require perfect simulation, but it leaves readable state.

### Faction Memory Values

- `friendly`
- `neutral`
- `suspicious`
- `hostile`
- `afraid`
- `respectful`
- `exhausted`
- `fractured`
- `retaliating`

### Common World Flags

- `commoner_trust_high`
- `commoner_trust_low`
- `merchant_trust_high`
- `merchant_trust_low`
- `noble_trust_high`
- `noble_trust_low`
- `underworld_notice`
- `underworld_debt`
- `refugees_unified`
- `refugees_scattered`
- `supply_routes_secured`
- `supply_routes_broken`
- `imperial_spies_exposed`
- `imperial_spies_embedded`
- `maeron_reconciled`
- `maeron_slain`
- `maeron_exiled`
- `marius_defeated`
- `marius_withdrawn`
- `marius_overlord`

## Side Campaign Hooks

The Road to the Crown unlocks or suspends into side campaigns without losing the main spine.

### Recommended Switches

- `overlay_and_return`: refugee crisis, companion moral test, trade route emergency.
- `suspend_and_replace`: imperial invasion spike, claimant war, major betrayal.
- `split_to_branch`: Act IV route lock.
- `merge_back`: branch returns into Act V imperial pressure.
- `unlock_new_active`: post-ending ruler, exile, restoration, or empire campaign.
- `terminate_old_and_start_new`: catastrophic Crown of Ashes failure.

### Hook Candidates

- `campaign_chains_in_the_market`: if prisoner markets or exploitative trade are used.
- `campaign_mercy_under_chains`: if captives become a moral pressure point.
- `campaign_the_quiet_knife`: if intrigue or Vaska's route is active.
- `campaign_a_name_worth_wearing`: if Rolf and legitimacy are central.
- `campaign_the_honest_price`: if Celeste, Marnid, or Crown of Coin route is active.
- `campaign_the_last_banner_of_the_east`: if Act V expands into a larger endgame war.

## Branch Tree and Stop Map

> Status: **target-state campaign graph for lowering**.  
> The current quest runtime supports lifecycle outcomes such as `advance_stage`, `complete`, `fail`, and `abort`. This tree is an authoring map for the advanced quest framework and later lowering, not a claim that a generic branch-graph API already exists.

### Legend

- `advance_stage`: continue inside the current quest chain.
- `complete`: finish the quest or chapter with success or accepted compromise.
- `fail`: finish the quest or chapter with a failure state that still leaves campaign recovery possible unless marked terminal.
- `abort`: stop the current quest early because another campaign, branch, or crisis takes over.
- `split_to_branch`: lock a major route or route modifier.
- `merge_back`: return from a branch into the shared campaign spine.
- `overlay_and_return`: run a side campaign while preserving this campaign's active state.
- `suspend_and_replace`: pause this campaign while a crisis campaign takes active focus.
- `terminate_old_and_start_new`: end this campaign and activate a successor campaign.

### Full Campaign Tree

```md
campaign_road_to_the_crown
|
+-- act_01_ashes
|   |
|   +-- qst_rtc_last_smoke
|   |   |
|   |   +-- save wounded
|   |   |   -> complete
|   |   |   -> set act_01_choice_saved_wounded
|   |   |   -> increase mercy trust
|   |   |
|   |   +-- save baggage
|   |   |   -> complete
|   |   |   -> set act_01_choice_saved_baggage
|   |   |   -> improve supply start
|   |   |
|   |   +-- save military papers
|   |   |   -> complete
|   |   |   -> set act_01_choice_saved_papers
|   |   |   -> unlock stronger imperial intelligence
|   |   |
|   |   +-- abandon road fight
|   |       -> fail
|   |       -> set reputation_refugee and companion_wary_mercy
|   |       -> campaign continues
|   |
|   +-- qst_rtc_borrowed_names
|   |   |
|   |   +-- public identity: fallen noble
|   |   |   -> complete
|   |   |   -> set reputation_foreign_noble
|   |   |
|   |   +-- public identity: free captain
|   |   |   -> complete
|   |   |   -> set reputation_free_captain
|   |   |
|   |   +-- public identity: trader
|   |   |   -> complete
|   |   |   -> set reputation_trade_operator
|   |   |
|   |   +-- public identity: refugee
|   |   |   -> complete
|   |   |   -> set reputation_refugee
|   |   |
|   |   +-- public identity: avenger
|   |       -> complete
|   |       -> set reputation_avenger
|   |
|   +-- qst_rtc_hound_sign
|       |
|       +-- duel scout captain
|       |   -> complete
|       |   -> favors method_honor
|       |
|       +-- steal or decode orders
|       |   -> complete
|       |   -> favors method_intrigue or method_counsel
|       |
|       +-- identify supply route
|       |   -> complete
|       |   -> favors method_trade
|       |
|       +-- miss evidence
|           -> fail
|           -> imperial_pressure_low still set
|           -> later Marius warning arrives with less preparation
|
+-- act_02_choice
|   |
|   +-- qst_rtc_door_into_calradia
|   |   |
|   |   +-- patron route
|   |   |   -> complete
|   |   |   -> increase noble_trust
|   |   |
|   |   +-- contract route
|   |   |   -> complete
|   |   |   -> increase merchant_trust
|   |   |
|   |   +-- public service route
|   |       -> complete
|   |       -> increase commoner_trust
|   |
|   +-- qst_rtc_price_of_bread
|   |   |
|   |   +-- pay fairly
|   |   |   -> complete
|   |   |   -> set commoner_trust_high
|   |   |
|   |   +-- negotiate labor for grain
|   |   |   -> complete
|   |   |   -> balanced trust outcome
|   |   |
|   |   +-- expose hoarding
|   |   |   -> complete if evidence is enough
|   |   |   -> fail if evidence is weak
|   |   |
|   |   +-- requisition by force
|   |   |   -> complete with cost
|   |   |   -> set village_fear
|   |   |
|   |   +-- raid bandit stores
|   |       -> complete if battle won
|   |       -> fail if battle lost
|   |       -> campaign continues with hunger pressure
|   |
|   +-- qst_rtc_banner_tested
|       |
|       +-- honor, intrigue, trade, counsel, or faith test succeeds
|       |   -> complete
|       |   -> set matching method flag
|       |
|       +-- public test fails
|           -> fail
|           -> set reputation_unproven
|           -> unlock recovery beat in Act III
|
+-- act_03_standing
|   |
|   +-- qst_rtc_three_offers
|   |   |
|   |   +-- noble protection
|   |   |   -> split_to_branch seed branch_legitimacy
|   |   |
|   |   +-- paid steel
|   |   |   -> split_to_branch seed branch_mercenary or branch_conquest
|   |   |
|   |   +-- people's road
|   |   |   -> split_to_branch seed branch_coalition with optional branch_reform
|   |   |
|   |   +-- quiet ledger
|   |       -> split_to_branch seed branch_imperial, branch_betrayal, or branch_hidden_regime_maker
|   |
|   +-- qst_rtc_companions_take_sides
|   |   |
|   |   +-- company holds
|   |   |   -> complete
|   |   |   -> companion states steady, wary, or troubled
|   |   |
|   |   +-- company fractures
|   |       -> fail
|   |       -> companion near_breaking or broken
|   |       -> branch_failure_fractured_claim possible
|   |
|   +-- qst_rtc_first_recognition
|       |
|       +-- recognition secured
|       |   -> complete
|       |   -> unlock qst_rtc_crown_council
|       |
|       +-- recognition botched
|           -> fail
|           -> Act IV starts with public weakness or route lock loss
|
+-- act_04_crown
|   |
|   +-- qst_rtc_crown_council
|       |
|       +-- branch_legitimacy
|       |   -> split_to_branch
|       |   -> complete branch quest on recognition
|       |   -> merge_back to act_05_shadow
|       |
|       +-- branch_mercenary
|       |   -> split_to_branch
|       |   -> complete branch quest on contract leverage
|       |   -> merge_back to act_05_shadow
|       |
|       +-- branch_conquest
|       |   -> split_to_branch
|       |   -> complete branch quest on decisive victory
|       |   -> merge_back to act_05_shadow
|       |
|       +-- branch_coalition
|       |   -> split_to_branch
|       |   -> complete branch quest on charter success
|       |   -> merge_back to act_05_shadow
|       |
|       +-- branch_restoration
|       |   -> split_to_branch
|       |   -> complete branch quest on refugee body or restored banner
|       |   -> merge_back to act_05_shadow
|       |
|       +-- branch_imperial
|       |   -> split_to_branch
|       |   -> complete branch quest on imperial terms accepted or subverted
|       |   -> merge_back to act_05_shadow
|       |
|       +-- branch_hidden_regime_maker
|       |   -> split_to_branch
|       |   -> overrides weaker public route
|       |   -> merge_back to act_05_shadow with strongest stability
|       |
|       +-- branch_failure_fractured_claim
|           -> fail
|           -> either recovery beat, Crown of Ashes candidate, or abort into crisis
|
+-- act_05_shadow
    |
    +-- qst_rtc_hounds_terms
    |   |
    |   +-- reject terms
    |   |   -> advance_stage to qst_rtc_war_of_witnesses
    |   |
    |   +-- negotiate delay
    |   |   -> advance_stage with imperial_pressure_open
    |   |
    |   +-- accept terms
    |   |   -> split_to_branch branch_imperial
    |   |
    |   +-- talks collapse
    |       -> fail
    |       -> imperial_pressure_invasion
    |
    +-- qst_rtc_war_of_witnesses
    |   |
    |   +-- protect witnesses
    |   |   -> complete
    |   |   -> strengthens chosen ending
    |   |
    |   +-- sacrifice witnesses
    |   |   -> complete with cost or fail
    |   |   -> increases Crown of Ashes or Crown of Iron chance
    |   |
    |   +-- side crisis overwhelms main route
    |       -> suspend_and_replace
    |       -> possible campaign_the_last_banner_of_the_east
    |
    +-- qst_rtc_last_road
    |   |
    |   +-- hold the line
    |   |   -> advance_stage to final confrontation
    |   |
    |   +-- strike the Hound
    |   |   -> advance_stage to final confrontation
    |   |
    |   +-- starve the Empire
    |   |   -> advance_stage to final confrontation
    |   |
    |   +-- break the seal
    |   |   -> advance_stage to final confrontation
    |   |
    |   +-- accept the collar
    |   |   -> advance_stage to imperial ending path
    |   |
    |   +-- catastrophic loss
    |       -> fail
    |       -> ending_crown_of_ashes candidate
    |
    +-- qst_rtc_final_confrontation
        |
        +-- Marius defeated or forced back
        |   -> complete
        |   -> ending chosen from route, witnesses, and companion state
        |
        +-- Marius accepted as overlord
        |   -> complete
        |   -> ending_crown_of_empire
        |
        +-- player rejects personal rule after victory
        |   -> complete
        |   -> ending_unworn_crown
        |
        +-- claim collapses
            -> fail
            -> ending_crown_of_ashes
            -> terminate_old_and_start_new exile or redemption campaign
```

### Stop Points for Implementation

These are the clean places where the advanced quest framework can safely stop, archive, suspend, or hand control to another quest chain.

| Stop ID | Location | Runtime outcome | Campaign meaning | Follow-up |
| --- | --- | --- | --- | --- |
| `stop_act_01_survived` | after `qst_rtc_hound_sign` | `complete` | opening identity and imperial proof are established | start Act II |
| `stop_act_01_poor_start` | failed Act I objective | `fail` | player reaches Calradia with weaker trust or evidence | start Act II with penalties |
| `stop_act_02_social_entry` | after `qst_rtc_banner_tested` | `complete` | social method and first trust profile are known | start Act III |
| `stop_act_02_unproven` | failed public test | `fail` | player is known but not respected | Act III recovery beat |
| `stop_act_03_route_seeded` | after `qst_rtc_three_offers` | `complete` | major route seed exists | companion side-taking |
| `stop_act_03_company_fracture` | after companion failure | `fail` | company trust is unstable | Crown of Ashes candidate or recovery |
| `stop_act_04_branch_locked` | after `qst_rtc_crown_council` | `complete` | primary route is locked | Act V |
| `stop_act_04_fractured_claim` | failed Crown Council | `fail` or `abort` | claim lacks witnesses | recovery, crisis, or Crown of Ashes candidate |
| `stop_act_05_imperial_crisis` | Act V side crisis | `suspend_and_replace` | larger war overrides local crown arc | `campaign_the_last_banner_of_the_east` |
| `stop_final_success` | final confrontation | `complete` | campaign ends in a crown or settlement | archive ending and unlock successor |
| `stop_final_collapse` | final confrontation failure | `fail` | campaign ends in ruin or exile | terminate and start exile/redemption arc |

### First Implementation Slice Tree

The recommended first implementation slice is small enough to build and verify without implementing all branches.

```md
qst_rtc_last_smoke
|
+-- complete: saved wounded
+-- complete: saved baggage
+-- complete: saved papers
+-- fail: abandoned road fight
    |
    v
qst_rtc_borrowed_names
|
+-- complete: reputation_foreign_noble
+-- complete: reputation_free_captain
+-- complete: reputation_trade_operator
+-- complete: reputation_refugee
+-- complete: reputation_avenger
    |
    v
qst_rtc_hound_sign
|
+-- complete: honor / intrigue / counsel / trade evidence
+-- fail: weak evidence but imperial_pressure_low still set
    |
    v
stop_act_01_survived or stop_act_01_poor_start
    |
    v
qst_rtc_price_of_bread
|
+-- complete: paid fairly
+-- complete: negotiated labor
+-- complete: exposed hoarding
+-- complete with cost: requisitioned by force
+-- fail: hunger pressure remains
```

This slice is ready to implement first because it exercises the important framework behavior without requiring the full campaign graph:

- stage progression through several linked quests
- success and failure outcomes that both continue the campaign
- persistent identity flags
- persistent reputation and trust flags
- first companion reaction hooks
- first imperial pressure state
- first route-method seeds

## Implementation Lowering Plan

Implementation tracking lives in [`the_road_to_the_crown_implementation_checklist.md`](./the_road_to_the_crown_implementation_checklist.md).

### Readiness Verdict

This document is ready to begin implementation at the campaign-slice level. The first pass is the Act I opening plus the first Act II social-access quest, not the full five-act campaign. That slice establishes the durable state contract used by the rest of the campaign.

Ready now:

- identity tags for origin, faith, adult-life path, and motive
- opening NPC set: Garran, Lysara, Odran, plus one route contact
- first three opening chapters with quest IDs
- early reputation, trust, and imperial pressure flags
- sample dialogue and journal text for the first implementation slice
- route seeds that later feed Act III and Act IV

Needs implementation decisions before coding later acts:

- exact troop templates and equipment for custom NPCs
- exact center or scene assignments for refugee camp, first town, and border road
- numeric thresholds for trust, fear, legitimacy, army strength, and companion approval
- final mapping from campaign flags into global variables, quest slots, or troop slots
- whether Maeron's dynastic-partner outcome is deferred or removed for the first release

Recommended first milestone:

1. Add the campaign state flags and identity capture from character creation.
2. Implement `qst_rtc_last_smoke`, `qst_rtc_borrowed_names`, and `qst_rtc_hound_sign`.
3. Add Garran, Lysara, Odran, and the imperial scout evidence dialogue.
4. Verify Act I can end in at least three states: wounded saved, supplies saved, or papers saved.
5. Start Act II with `qst_rtc_price_of_bread` as the first moral and resource test.

### Phase 1: Identity and Opening

- Add campaign identity flags from origin, faith, adult life, and motive choices.
- Implement `qst_rtc_last_smoke`.
- Implement `qst_rtc_borrowed_names`.
- Implement `qst_rtc_hound_sign`.
- Add Garran, Lysara, and Odran dialogue.
- Add first imperial scout evidence.

### Phase 2: Early Social Access

- Implement `qst_rtc_door_into_calradia`.
- Implement `qst_rtc_price_of_bread`.
- Implement `qst_rtc_banner_tested`.
- Add route-specific town contacts.
- Add initial public reputation flags.
- Add first companion reaction campfire scene.

### Phase 3: Standing and Recognition

- Implement `qst_rtc_three_offers`.
- Implement `qst_rtc_companions_take_sides`.
- Implement `qst_rtc_first_recognition`.
- Add faction memory changes.
- Add Maeron as public rival.

### Phase 4: Crown Branches

- Implement `qst_rtc_crown_council`.
- Add route locks for legitimacy, mercenary, conquest, coalition, restoration, and imperial accommodation.
- Add hidden regime maker gate.
- Add route-specific companion warning states.

### Phase 5: Imperial Shadow and Endings

- Implement `qst_rtc_hounds_terms`.
- Implement `qst_rtc_war_of_witnesses`.
- Implement `qst_rtc_last_road`.
- Implement `qst_rtc_final_confrontation`.
- Add Marius and Septima scenes.
- Add final strategy branch.
- Add ending flags and unlocks.
- Add post-campaign archive state.

## QA Checklist for Later Implementation

- Starting identity flags are set from character creation.
- Act I can complete even if the player fails optional objectives.
- Every Act IV route has at least one success, compromise, and failure outcome.
- Companion reactions are not hard-coded only to route; they also check behavior.
- Imperial pressure increases on a predictable schedule.
- Marius is foreshadowed before direct appearance.
- Endings are stored as compact flags.
- Side campaigns can overlay without corrupting the main active branch.
- The campaign can fail into Crown of Ashes without breaking later play.
- Route names and flags match the campaign state model vocabulary.

## Summary

`The Road to the Crown` is the main long-form campaign spine for the module.

It begins with exile, turns identity into political access, tests the player's method through concrete crises, forces a claim to authority, and resolves that claim under the shadow of the Imperial Hound.

Its implementation is modular:

- opening survival quests
- route-colored social access
- companion pressure scenes
- political branch locks
- imperial final act
- durable ending flags

The desired result is a campaign that can later be lowered into Mount & Blade quests and dialogue while preserving the central question:

**What kind of crown can be built from ash, witness, hunger, fear, and choice?**
