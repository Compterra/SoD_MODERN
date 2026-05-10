# Companion Quest Immersion Audit

This audit tracks where companion personal quests still feel like camp-menu resolutions and how to move them toward direct dialogue, travel, encounters, and world adventure. The current companion system is mechanically strong: world hooks set incident state, camp menus resolve branches, direct companion talk remembers aftermath, and quest-framework metadata records state. The immersion gap is presentation and staging.

## Current Problem

- Camp action entries expose companion quest decisions as abstract command choices.
- Incident menus narrate companions and witnesses instead of letting those characters speak in dialogue.
- Most arcs trigger from world play, but resolution usually happens from the camp menu rather than from the relevant person, party, center, prisoner, village, or battlefield context.
- Quest stages exist, but they rarely ask the player to travel, inspect, talk to witnesses, escort someone, find a party, or make a choice in the place where the problem exists.
- The campfire is good for reflection and repair, but it should not be the main place where every personal quest climax happens.

## What Already Works

- [x] Every companion has direct member-talk depth dialogue.
- [x] Every companion has approval, warnings, reconciliation, and aftermath state.
- [x] Every companion has at least one world-triggered incident flag.
- [x] Every companion arc has quest-framework identity and journal/memory integration.
- [x] Companion incidents are gated by party membership and pending state.
- [x] Companion reports can summarize unresolved matters and aftermath.

## Highest-Value Migration Rule

Camp menus should become fallback or travel-planning surfaces. The main quest choices should move into one of these:

- Direct companion dialogue through `member_talk`.
- Dialogue with a relevant temporary/world NPC.
- Encounter dialogue with a quest party.
- Center/village menu only when the location itself is the actor.
- Short adventure loops: travel to a center, intercept a party, inspect a trail, escort/protect a group, then talk to the companion.

## Immediate Refactor Pattern

For each existing companion incident menu:

- [x] Keep the current menu as a safe fallback.
- [x] Add a direct-talk option when the incident is pending: "About the matter you raised..."
- [x] Move the three branch choices into companion dialogue states.
- [x] Let the companion speak first, then let the player choose.
- [x] Record the same quest-framework event and apply the same scripts currently called by the menu.
- [x] Change the camp action entry text from a resolution verb to a conversation verb.
- [x] Add static tests that pending incident dialogue exists for each migrated companion.

## Adventure Upgrade Pattern

For arcs with strong world hooks:

- [x] Store a focus center, focus party, or focus cause when the incident is triggered.
- [x] Add a report/journal hint that names the place or actor.
- [x] Add a short optional action before resolution: visit, inspect, escort, intercept, negotiate, or investigate.
- [x] Let the companion comment at the site before the final choice.
- [x] Resolve through dialogue or encounter, not a generic camp decision.

### Adventure Pattern Verification Matrix

| Arc | State stored or derived | Hint surface | Site or actor action | Companion/site comment | Resolution surface |
| --- | --- | --- | --- | --- | --- |
| Ymira - Mercy Under Arms | `$g_sod_ymira_refugee_focus_center`; `$g_sod_ymira_refugee_witnessed` | Quest journal says to go to captive/refugee witness; companion report names quest-framework aftermath | Travel to focus village, speak with elder/town refugee/captive troop | Ymira comments that mercy has witnesses before branch choice | Direct companion dialogue after witness, with camp fallback |
| Marnid - The Honest Price | `$g_sod_marnid_market_contacted`; center trade identity derived at goods merchant | Quest journal says to go to market contact/caravan/bargain | Speak with goods merchant for market account | Merchant gives fair-dealing testimony that Marnid can use | Goods-merchant dialogue advances witness; Marnid/camp dialogue resolves |
| Lezalit - Discipline Without Chains | `$g_sod_lezalit_ief_discipline_pending`; `$g_sod_lezalit_ief_discipline_witnessed` | Quest journal says to go to drill or troop witness | Speak with regular troop over captured Imperial drill | Lezalit comments that the soldier spoke correctly before branch choice | Direct companion dialogue after troop witness, with camp fallback |
| Bunduk - The Men Who Hold the Line | `$g_sod_bunduk_line_pending`; `$g_sod_bunduk_line_cause`; `$g_sod_bunduk_line_witnessed` | Quest journal says to go to rank-and-file witness | Speak with regular troop spokesperson | Bunduk says the player heard it from a ranker before branch choice | Direct companion dialogue after troop witness, with camp fallback |
| Jeremus - Hands That Will Not Harden | `$g_sod_jeremus_triage_pending`; `$g_sod_jeremus_triage_witnessed` | Quest journal says to go to wounded or triage witness | Speak with wounded regular troop | Jeremus says the wounded were heard before branch choice | Direct companion dialogue after wounded witness, with camp fallback |
| Firentis - Debt of the Sword | `$g_sod_firentis_restitution_focus_center`; `$g_sod_firentis_restitution_witnessed` | Quest journal says to go to restitution village or battle witness | Travel to focus village and speak with elder | Firentis references elder/living voice before branch choice | Direct companion dialogue after elder witness, with camp fallback |
| Katrin - The Last Coin in Camp | `$g_sod_katrin_last_coin_pending`; `$g_sod_katrin_last_coin_cause`; `$g_sod_katrin_last_coin_witnessed` | Quest journal says to go to accounts or camp witness | Inspect company accounts petition/ledger witness | Katrin says the player saw the ledger before branch choice | Direct companion dialogue after accounts witness, with camp fallback |
| Deshavi - Tracks Through Ash | `$g_sod_deshavi_trail_focus_center`; `$g_sod_deshavi_trail_warning_cause`; `$g_sod_deshavi_trail_witnessed` | Quest journal says to go to survivor, hunter, or trail focus | Travel to focus village, speak with elder/town survivor/slaver pursuer | Deshavi names the elder/tracks before branch choice | Direct companion dialogue after trail witness, with camp fallback |
| Klethi - A Knife With a Name | `$g_sod_klethi_old_job_pending`; `$g_sod_klethi_old_job_cause`; `$g_sod_klethi_old_job_contacted` | Quest journal says to go to tavern contact or old-job witness | Speak with tavernkeeper contact | Klethi says the old job now has a witness beyond her mouth | Direct companion dialogue after tavern contact, with camp fallback |
| Rolf - A Name Worth Wearing | `$g_sod_rolf_name_challenge_pending`; `$g_sod_rolf_name_challenge_witnessed` | Quest journal says to go to public witness | Speak with town dweller/public witness | Rolf frames the crowd as a poor court before branch choice | Direct companion dialogue after public witness, with camp fallback |
| Alayen - The Standard and the Self | `$g_sod_alayen_standard_pending`; `$g_sod_alayen_standard_cause`; `$g_sod_alayen_standard_witnessed` | Quest journal says to go to lord, elder, or public witness | Speak with lord or village elder witness | Alayen comments on honor before branch choice | Direct companion dialogue after public/protection witness, with camp fallback |
| Nizar - The Impossible Charge | `$g_sod_nizar_charge_pending`; `$g_sod_nizar_charge_witnessed` | Quest journal says to go to field setup or pursuit moment | Use pre-battle/pursuit setup dialogue | Nizar frames the charge around survival and story before branch choice | Direct companion dialogue after field setup, with camp fallback |
| Baheshtur - The Unbroken Saddle | `$g_sod_baheshtur_saddle_pending`; `$g_sod_baheshtur_saddle_cause`; `$g_sod_baheshtur_saddle_witnessed` | Quest journal says to go to rider or horde witness | Speak with Black Khergit rider/guard survivor | Baheshtur says the player heard the rider before branch choice | Direct companion dialogue after rider witness, with camp fallback |
| Matheld - No Backward Step | `$g_sod_matheld_no_backward_step_pending`; `$g_sod_matheld_no_backward_step_cause`; `$g_sod_matheld_no_backward_step_witnessed` | Quest journal says to go to line witness after battle | Speak with regular troop line witness | Matheld names what the line learned before branch choice | Direct companion dialogue after post-battle witness, with camp fallback |
| Artimenner - The Siege That Should Have Worked | `$g_sod_artimenner_siege_pending`; `$g_sod_artimenner_siege_cause`; `$g_sod_artimenner_siege_witnessed` | Quest journal says to go to siege works or construction witness | Inspect ladders or siege tower preparations | Artimenner points out the weak point before branch choice | Direct companion dialogue after siege inspection, with camp fallback |

## Companion-by-Companion Audit

### Ymira - Mercy Under Arms

Current surface: camp menu if Ymira is present, her quest is open, and the party carries at least three slaves.

Immersion issue: the most emotional arc in the set is decided from camp logistics. The captives are not characters, and Ymira does not speak as the decision is made.

Best migration:

- Direct-talk branch: Ymira asks to speak about the captives.
- Add captive/refugee spokesperson dialogue if possible, using existing slave/refugee troops or generic anyone dialogue.
- Optional adventure: escort freed captives to a nearby village, Jotnar camp, Elephant Guard sanctuary, or town.
- Good path: protect and release captives through an escort/shelter action.
- Hard path: ransom or triage who can be moved.
- Bad path: keep/sell captives, with Ymira confronting the player directly.

Priority: Very high. This should be the first conversion because it immediately fixes the worst menu-to-emotion mismatch.

### Lezalit - Discipline Without Chains

Current surface: camp menu after IEF discipline evidence is pending.

Immersion issue: captured Imperial doctrine is abstract. There is no prisoner, document, drillmaster, or soldier reaction.

Best migration:

- Direct-talk branch: Lezalit presents captured manuals and asks for authority.
- Add a company-sergeant or captured Imperial officer dialogue as witness.
- Optional adventure: inspect defeated IEF camp/party aftermath after battle.
- Good path: reform the drill in front of troops.
- Hard path: use fear but avoid pointless cruelty.
- Refusal path: reject the doctrine and force Lezalit to answer what discipline means without it.

Priority: Very high. Strong Dragon Age-style ideological confrontation.

### Bunduk - The Men Who Hold the Line

Current surface: camp menu when casualties, unpaid wages, or line grievance is pending.

Immersion issue: Bunduk speaks for soldiers, but the soldiers never appear.

Best migration:

- Direct-talk branch: Bunduk brings a veteran or wounded ranker.
- Add generic troop spokesperson dialogue from `member_talk` or a temporary camp spokesperson.
- Optional adventure: inspect wages/stores via company accounts, then resolve.
- Good path: improve watches, stores, pay, and orders.
- Compromise path: defer some complaints with a concrete promise.
- Crackdown path: enforce order and create a warning.

Priority: Very high. This naturally connects to the company morale system.

### Jeremus - Hands That Will Not Harden

Current surface: camp triage menu after heavy casualties.

Immersion issue: triage is described after the fact, not experienced as wounded people asking for help.

Best migration:

- Direct-talk branch: Jeremus asks the player to come to the wounded.
- Add wounded soldier/refugee/prisoner dialogue if a temporary actor is feasible.
- Optional adventure: spend medical supplies, denars, or time before marching.
- Good path: treat by need.
- Hard path: hard triage with Jeremus owning the cost.
- Bad path: company-first only.

Priority: High. It pairs well with post-battle consequences.

### Firentis - Debt of the Sword

Current surface: camp/village restitution menu after relevant mercy or village defense.

Immersion issue: the village and victims are absent; Firentis' guilt is narrated rather than witnessed.

Best migration:

- Move resolution to village elder or rescued villager dialogue when a village focus exists.
- Firentis should interrupt through direct dialogue before the player leaves.
- Optional adventure: deliver coin/supplies or leave a guard detachment.
- Good path: restitution and protection.
- Hard path: public confession and negotiated justice.
- Bad path: silence and move on.

Priority: High. Needs a focus village slot for best effect.

### Katrin - The Last Coin in Camp

Current surface: camp shortage menu when food/pay strain is pending.

Immersion issue: this one can remain partly camp-based, but it needs troop and quartermaster voices.

Best migration:

- Direct-talk branch: Katrin opens the ledger in member talk.
- Add company spokesperson/troop petition tie-in.
- Use company accounts and ration policy menus as the actual levers.
- Good path: food, medicine, arrears.
- Hard path: fair rationing.
- Bad path: spend for momentum.

Priority: Medium-high. Best paired with company accounts polish.

### Deshavi - Tracks Through Ash

Current surface: camp trail-warning menu after poor-village, slaver, or raider signs.

Immersion issue: the trail is described, but the player does not follow it.

Best migration:

- Add a map objective: inspect trail near a village, slaver route, or raider area.
- Direct-talk branch: Deshavi gives the clue and asks to move before the tracks die.
- Encounter/center resolution: survivors, hunters, or ambush party.
- Good path: shelter vulnerable people.
- Hard path: ambush first, then move survivors.
- Bad path: hunt only.

Priority: High. This should become the prototype for actual companion adventure.

### Klethi - A Knife With a Name

Current surface: camp old-job menu after underworld/horde/slaver hook.

Immersion issue: an underworld quest should not be a camp button. It needs a contact, locked door, or dangerous meeting.

Best migration:

- Direct-talk branch: Klethi identifies a sign and asks how much trust she has.
- Add town/tavern contact dialogue.
- Optional adventure: meet contact, steal papers, protect Klethi, or expose the old employer.
- Good path: let Klethi choose.
- Hard path: protect her while keeping the job clean.
- Bad path: sell the secret for leverage.

Priority: High. Strong candidate for stealth/adventure content.

### Rolf - A Name Worth Wearing

Current surface: camp menu after public challenge/tournament/honor.

Immersion issue: public legitimacy should happen in public, not in camp.

Best migration:

- Move to tournament, tavern, lord hall, or town dialogue.
- Add heckler/witness/noble dialogue where Rolf must answer.
- Good path: service over embellishment.
- Hard path: defend dignity while keeping the claim alive.
- Bad path: publicly expose him.

Priority: Medium. Needs town/public dialogue but low mechanical complexity.

### Alayen - The Standard and the Self

Current surface: camp standard-oath menu after public honor or protection event.

Immersion issue: the standard matters because witnesses see it; the witnesses are absent.

Best migration:

- Move to village/town/lord aftermath after protection, oath, or diplomacy choice.
- Direct-talk branch: Alayen asks what the banner is for.
- Good path: banner as protection.
- Hard path: costly oath.
- Bad path: prestige and obedience.

Priority: Medium. Stronger when tied to diplomacy or village protection.

### Nizar - The Impossible Charge

Current surface: camp heroic-action menu.

Immersion issue: an impossible charge should be proposed before a battle or pursuit, not after camp reflection.

Best migration:

- Add pre-battle or post-victory pursuit trigger where Nizar proposes a risky maneuver.
- Direct-talk fallback if pending.
- Good path: plan the exit first.
- Hard path: take the dazzling charge.
- Bad path: blood legend.

Priority: Medium-high, but needs careful battle/mission hook selection.

### Baheshtur - The Unbroken Saddle

Current surface: camp rider oath menu after Black Khergit pressure.

Immersion issue: defeated riders should be present as prisoners, defectors, or a camp encounter.

Best migration:

- Encounter Black Khergit survivors or prisoner stack after horde defeat.
- Baheshtur speaks in direct dialogue before the riders answer.
- Good path: freely sworn riders.
- Hard path: pursuit with honorable surrender.
- Bad path: forced submission.

Priority: Medium-high. Strong fit with Black Khergit world system.

### Matheld - No Backward Step

Current surface: camp shield challenge after casualties/retreat.

Immersion issue: courage is judged by the line, but the line has no voice.

Best migration:

- Tie into post-battle morale and troop-category morale.
- Direct-talk branch: Matheld challenges what the next line should learn.
- Add veteran or recruit witness dialogue.
- Good path: courage that saves lives.
- Hard path: stand and answer the next threat.
- Bad path: blood-price.

Priority: Medium-high. Best paired with in-battle/post-battle morale.

### Artimenner - The Siege That Should Have Worked

Current surface: camp siege design menu.

Immersion issue: this one can work as a planning scene, but it should appear during siege/build preparation, not generic camp.

Best migration:

- Trigger inside siege preparation, construction, or engineering report context.
- Direct-talk branch: Artimenner asks the player to inspect the weak point.
- Good path: rebuild with materials.
- Hard path: improvise a leaner plan.
- Bad path: blame him if it fails.

Priority: Medium. Best when tied to actual siege/construction levers.

## Recommended Implementation Slices

### Slice 1: Direct Dialogue Conversion

- [x] Add pending-incident direct-talk entries for Ymira, Lezalit, Bunduk, Jeremus, and Firentis.
- [x] Move their branch choices from camp menus into dialogue.
- [x] Leave camp menus as fallback only.
- [x] Update camp action labels to "Speak with..." rather than "Choose..." for the first migrated slice.
- [x] Add static tests for direct-talk pending options.

Why first: this yields the biggest immersion gain without needing new scenes, parties, or complex travel state.

### Slice 2: Adventure Hooks

- [x] Deshavi gets a trail focus and location-gated center resolution.
- [x] Klethi gets a tavern/contact witness step before resolution.
- [x] Baheshtur gets Black Khergit survivor/rider witness resolution.
- [x] Firentis gets village restitution focus and village elder witness dialogue before resolution.
- [x] Ymira gets shelter destination logic and location-gated captive resolution.

Why second: these arcs most clearly benefit from actual movement and contact with the world.

### Slice 2A: Place-Gated Prototype

- [x] Add focus-center state for Ymira's refugee shelter.
- [x] Add focus-center state for Deshavi's trail warning.
- [x] Pick a nearby village as the first-pass focus center.
- [x] Dialogue names the focus center and tells the player to travel there.
- [x] Final branch choices are withheld until the party is close enough to the focus center.
- [x] Replace nearest-village fallback with smarter target selection by cause, safety, and mini-faction pressure.
- [x] Ymira refugee shelter target selection favors safer, healthier villages and Jotnar/Elephant Guard shelter pressure while avoiding Slaver nodes and unsafe roads.
- [x] Deshavi trail target selection favors threatened, poor, unhealthy, Slaver-pressured, or Black Khergit-pressured villages while still avoiding hopelessly unsafe destinations.
- [x] Firentis restitution focus uses the same selector with a restitution weighting for recovering, harmed, but reachable villages.
- [x] Add first-pass village elder witness dialogue at the focus center for Ymira and Deshavi.
- [x] Add companion follow-up text after the village elder witnesses the matter.
- [x] Add direct villager refugee witness dialogue for Ymira beyond village elder testimony.
- [x] Add direct villager survivor/trail witness dialogue for Deshavi beyond village elder testimony.
- [x] Add direct captive/refugee troop dialogue for Ymira.
- [x] Add direct hunter/pursuer or ambush-party dialogue for Deshavi.

### Slice 1B: Remaining Direct Dialogue Conversion

- [x] Add pending-incident direct-talk entries for Katrin, Deshavi, Klethi, Rolf, Alayen, Nizar, Baheshtur, Matheld, and Artimenner.
- [x] Move their branch choices from camp menus into dialogue.
- [x] Keep camp menus as fallback/compatibility only.
- [x] Add static tests for the remaining direct-talk pending options.
- [x] Update camp action hints so they say "speak with X" before "open camp action."

Why before full adventure hooks: every companion should feel like a person before any individual arc becomes a larger map adventure.

### Slice 3: System-Specific Quest Surfaces

- [x] Lezalit uses regular troop witness dialogue for captured Imperial drill pressure.
- [x] Bunduk uses regular troop spokesperson dialogue for line grievances.
- [x] Jeremus uses wounded regular troop dialogue for triage pressure.
- [x] Katrin uses company accounts/rations/troop petition surfaces.
- [x] Matheld uses post-battle morale and troop line witnesses.
- [x] Nizar uses pre-battle/pursuit setup where possible.
- [x] Artimenner uses siege/construction preparation context.
- [x] Rolf and Alayen use town/lord/public-honor contexts.

Why third: these need clean integration with larger systems rather than standalone dialogue.

## Static Test Targets

- [x] Companion depth static test detects direct-talk pending incident entries.
- [x] Camp menus are allowed only as fallback/resolution compatibility.
- [x] Each companion incident has either a direct dialogue branch or a documented adventure surface.
- [x] Each adventure surface stores or derives a focus center/party/cause.
- [x] Quest-framework journal text distinguishes "talk to companion" from "go to place/actor."

## Checklist Update Needed

The main checklist should stop treating "world-triggered menu incident" as fully DAO-style. Suggested wording:

- [x] Every companion has a pending incident that can be discussed directly with the companion.
- [x] Every companion has at least one quest choice delivered through dialogue, not only a menu.
- [x] At least eight companion arcs have an adventure/world actor step before final resolution.
- [x] Camp menus are fallback or planning surfaces, not the default climax for every companion quest.
