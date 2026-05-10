# Surgery And Casualty Care Design

This document outlines a more grounded Surgery system for SoD. The goal is not to remove the value of the Surgery skill. The goal is to make it feel like battlefield triage, casualty recovery, and aftercare instead of a one-sided passive magic shield.

The system must work both ways. Player parties, lord parties, bandits, special quest enemies, garrisons, and auto-resolve battles should all be able to benefit from valid medical skill, supplies, recovery conditions, and command context.

## Design Goals

- Keep Surgery valuable and readable.
- Make battlefield survival depend on skill, supplies, battle outcome, and recovery conditions.
- Make medical companions like Jeremus strategically important without making losses meaningless.
- Apply the same basic logic to player and opposing forces.
- Ensure auto-resolve uses equivalent casualty conversion rules.
- Make defeats, routs, sieges, ambushes, and abandoned wounded feel different from clean victories.
- Add reporting so the player understands why troops died, survived, or worsened later.

## Core Fantasy

Surgery represents more than cutting wounds open. In campaign terms it covers:

- battlefield triage
- stopping bleeding
- arrow and bolt removal
- splints and bandaging
- amputation decisions
- infection prevention
- wagon/horse litter evacuation
- clean cloth, alcohol, herbs, and tools
- organized recovery after the fighting ends

High Surgery should not mean "troops do not die." It should mean "more troops can be recovered if the army has the people, time, and supplies to save them."

## Fairness Rule

Surgery applies to all sides that meet the requirements.

- The player can benefit from party medical skill.
- Enemy lords can benefit from their own medical skill or attached surgeon troops if present.
- Bandit or looter parties usually have poor or no medical support.
- Elite orders, imperial armies, mercenary companies, and campaign bosses may have better field care.
- Garrisons can benefit from settlement medical infrastructure if present.
- Auto-resolve should use the same casualty conversion framework as direct battles.

The player should not have a unique hidden advantage unless a perk, companion, item, or difficulty setting explicitly grants one.

## Casualty Pipeline

Recommended flow after any battle:

1. Battle engine produces killed/wounded raw results.
2. Determine each side's casualty-care context.
3. Convert some would-be deaths into wounded based on Surgery and context.
4. Convert some severe wounds back into deaths if context is terrible.
5. Apply delayed wound-risk flags where appropriate.
6. Consume medical supplies if enabled.
7. Report the final outcome in concise language.

## Context Factors

Surgery should be modified by battle context.

Positive modifiers:

- Side won the battle and controlled the field.
- Side retreated in good order.
- Side has high Surgery.
- Side has medical supplies.
- Side has enough healthy troops to recover wounded.
- Side fought near friendly settlement support.
- Side has a medical companion or surgeon troop.
- Side has wagons, pack animals, or organized camp support.

Negative modifiers:

- Side lost the battle.
- Side routed or was captured.
- Side was ambushed.
- Side fought at night or in bad terrain.
- Side was heavily outnumbered.
- Side fought in a siege assault or breach.
- Side lacked medical supplies.
- Side had too few survivors to recover wounded.
- Wounded were abandoned, captured, or trampled during pursuit.

## Direct Battle Behavior

After a normal player battle:

- Apply Surgery separately to each side.
- If the player wins, player Surgery is strong because the field is controlled.
- If the player loses, player Surgery is weaker unless the retreat was orderly.
- Enemy Surgery should still save some enemy casualties if the enemy won or withdrew in good order.
- Captured enemies should not automatically benefit from their own surgeon unless their side still controls recovery.
- Prisoners rescued after battle should use the rescuer's recovery context, not their original captor's.

## Auto-Resolve Behavior

Auto-resolve must not bypass Surgery.

Auto-resolve should:

- calculate raw casualties for each side
- identify each side's best available medical skill
- apply the same context modifiers
- apply settlement/garrison medical support where relevant
- produce killed/wounded results that resemble direct battles
- avoid double-applying Surgery if direct battle scripts also run

Auto-resolve examples:

- Lord vs lord field battle: each lord party uses its own Surgery context.
- Player orders troops into battle without personally fighting: player side uses player-party medical context.
- Siege auto-resolve: attackers and defenders use different modifiers.
- Village raid defense auto-resolve: villagers/militia have poor field care unless supported.
- Ambush auto-resolve: defeated side has reduced recovery.

## Suggested Formula

Use a readable first-pass formula, then tune.

Base death-to-wound save chance:

- Surgery skill * 4 percent.
- Cap before modifiers: 40 percent.

Context modifiers:

- Victory with field control: +15 percent.
- Orderly retreat: +5 percent.
- Defeat with capture/rout: -20 percent.
- Siege breach or assault: -10 percent.
- Ambush: -10 percent.
- Adequate medical supplies: +10 percent.
- No medical supplies: -10 percent.
- Friendly settlement support nearby: +5 percent.
- Too few healthy survivors: -10 to -25 percent.

Final caps:

- Minimum: 0 percent.
- Normal maximum: 65 percent.
- Exceptional maximum with supplies and field control: 75 percent.

This keeps Surgery powerful, but it cannot erase the cost of catastrophic battles.

## Medical Supplies

Optional but recommended.

Possible supply model:

- Add medical supply item category or abstract party slot.
- Supplies are consumed when Surgery saves casualties.
- Shortage reduces casualty conversion.
- High Surgery spends supplies more efficiently.
- Looters and weak bandits usually lack supplies.
- Elite armies and rich lords may carry supplies.

Supply examples:

- bandages
- clean cloth
- alcohol
- herbs
- surgical tools
- splints
- carts or litters

Do not over-micro the player in v1. A single abstract "medical supplies" pressure is enough.

## Delayed Wound Outcomes

For deeper realism, some wounded can receive a delayed-risk state.

Possible delayed outcomes:

- recovers normally
- remains wounded longer
- dies later from infection or shock
- returns with temporary morale penalty
- becomes unavailable until treated in a town

Use this carefully. Delayed deaths can feel unfair unless reported clearly.

Recommended v1:

- Add delayed-risk only for severe defeats, sieges, and supply shortages.
- Show a report line: "Three badly wounded men may not survive the march without care."
- Let resting in a town, supplies, or a surgeon reduce the risk.

## Opposing Side Medical Support

Enemy medical support can come from:

- lord Surgery skill
- companion-equivalent heroes
- attached surgeon troop
- faction doctrine
- settlement infrastructure
- campaign party template

Suggested identity:

- Looters: almost none.
- Bandits: poor.
- Deserters: low to moderate, depending on origin.
- Mercenaries: moderate if disciplined.
- Lords: skill-dependent.
- Imperial armies: strong organized casualty recovery.
- Religious or knightly orders: strong morale and aftercare.
- Garrisons: improved if town/castle has relevant infrastructure.

This makes fighting elite factions feel more plausible: they recover more wounded, not because they cheat, but because they have orderlies, wagons, discipline, and surgeons.

## Reporting

Reports should explain outcomes without overwhelming the player.

Short battle report examples:

- "Jeremus's triage saved 7 men who would have died on the field."
- "The enemy's surgeons recovered many of their wounded after holding the ground."
- "Without supplies, several grave wounds became deaths before nightfall."
- "The rout scattered the wounded. Surgery could do little."
- "The garrison infirmary helped stabilize the defenders."

Detailed report examples:

- Raw deaths before care.
- Deaths converted to wounded.
- Wounded lost due to terrible recovery conditions.
- Supplies consumed.
- Delayed-risk wounded.
- Enemy casualty recovery if observed.

## Implementation Checklist

### Audit

- [ ] Audit all uses of Surgery skill in direct battle casualty processing.
- [ ] Audit all auto-resolve casualty code.
- [ ] Audit player defeat, capture, and retreat outcomes.
- [ ] Audit siege assault, siege defense, village raid defense, and quest battle casualty flows.
- [ ] Audit lord party skills and whether enemy parties can expose Surgery values.
- [ ] Audit garrison casualty processing.
- [ ] Audit companion medical role hooks, especially Jeremus and Ymira.
- [ ] Audit battle reports and weekly reports that mention wounded/dead.

### Core Scripts

- [ ] Add `script_sod_get_party_surgery_skill`.
- [ ] Add `script_sod_get_party_medical_context`.
- [ ] Add `script_sod_apply_casualty_care_to_party`.
- [ ] Add `script_sod_apply_casualty_care_to_battle_side`.
- [ ] Add `script_sod_describe_casualty_care_to_s1`.
- [ ] Ensure scripts accept a party or side id, not only `p_main_party`.
- [ ] Ensure scripts can run for enemy parties without player-specific assumptions.

### Direct Battle Integration

- [ ] Apply casualty care after direct field battles.
- [ ] Apply casualty care after player victory.
- [ ] Apply casualty care after player defeat.
- [ ] Apply casualty care after retreat.
- [ ] Apply casualty care to enemy survivors when appropriate.
- [ ] Prevent double application if native Surgery already modified the same casualties.
- [ ] Preserve existing wounded/dead stack consistency.

### Auto-Resolve Integration

- [ ] Apply casualty care in lord-vs-lord auto-resolve.
- [ ] Apply casualty care when player auto-resolves.
- [ ] Apply casualty care in siege auto-resolve.
- [ ] Apply casualty care in village raid defense auto-resolve.
- [ ] Apply casualty care in quest/mission auto-resolve if present.
- [ ] Ensure both sides use their own Surgery and context.
- [ ] Ensure auto-resolve and direct battle produce comparable outcomes.

### Enemy And NPC Support

- [ ] Give lord parties access to leader or party Surgery skill.
- [ ] Add optional surgeon/support troops for specific factions or templates.
- [ ] Let elite/organized armies have better medical context.
- [ ] Keep looters and weak bandits medically poor.
- [ ] Let garrisons benefit from settlement support where appropriate.
- [ ] Ensure enemy casualty recovery does not create invisible troop duplication.

### Supplies

- [ ] Decide whether v1 uses abstract medical supplies or item-based supplies.
- [ ] Add party medical supply tracking if abstract.
- [ ] Consume supplies when saving casualties.
- [ ] Reduce effectiveness when supplies are low.
- [ ] Add town restock or merchant purchase path.
- [ ] Give NPC parties reasonable generated supplies by type.
- [ ] Prevent supplies from going below zero.

### Delayed Outcomes

- [ ] Add optional delayed wound-risk state.
- [ ] Apply delayed risk after severe defeat, siege, rout, or supply shortage.
- [ ] Add recovery checks while resting.
- [ ] Add clear player reports before delayed deaths occur.
- [ ] Avoid applying delayed deaths silently.
- [ ] Prevent delayed wound states from affecting heroes unless explicitly designed.

### Reporting And Dialogue

- [ ] Add concise battle result lines for casualty care.
- [ ] Add detailed report entries for player and enemy recovery.
- [ ] Add companion comments for strong medical saves or terrible field conditions.
- [ ] Add Jeremus/Ymira-style medical observations if present.
- [ ] Report enemy Surgery only when the player plausibly observes it.
- [ ] Avoid spam for small casualty numbers.

### Edge Cases

- [ ] Player has no surgeon.
- [ ] Surgeon is wounded.
- [ ] Surgeon is prisoner/captured.
- [ ] Party has Surgery but no supplies.
- [ ] Party has supplies but no Surgery.
- [ ] Party is wiped out.
- [ ] Enemy party is destroyed but some troops are wounded.
- [ ] Prisoners/rescued troops are involved.
- [ ] Battle happens inside a siege scene.
- [ ] Auto-resolve battle has no valid party leader.
- [ ] Save/load occurs before delayed wounds resolve.
- [ ] Old saves lack medical supply slots.

### Exploit Controls

- [ ] Prevent Surgery from being applied twice.
- [ ] Prevent player from farming infinite wounded conversions through retreat loops.
- [ ] Prevent enemy parties from restoring troops beyond pre-battle counts.
- [ ] Prevent medical supplies from duplicating through battle rewards.
- [ ] Prevent delayed wound recovery from reviving dead stacks.
- [ ] Prevent garrison medical support from applying to unrelated field battles.

### Static Tests

- [ ] Add `build/test_surgery_casualty_care_static.py`.
- [ ] Assert casualty-care scripts are side/party generic.
- [ ] Assert direct battle integration calls casualty care.
- [ ] Assert auto-resolve integration calls casualty care.
- [ ] Assert enemy parties can use Surgery.
- [ ] Assert looters/bandits do not receive elite medical support by default.
- [ ] Assert defeat/rout modifiers exist.
- [ ] Assert siege/ambush modifiers exist.
- [ ] Assert supply shortage modifiers exist if supplies are implemented.
- [ ] Assert double-application guard exists.
- [ ] Assert battle reports mention player and enemy recovery where appropriate.

### Manual QA

- [ ] Player battle with high Surgery and supplies.
- [ ] Player battle with high Surgery and no supplies.
- [ ] Player battle with no Surgery.
- [ ] Player victory against enemy lord with high Surgery.
- [ ] Player defeat against enemy lord with high Surgery.
- [ ] Lord-vs-lord auto-resolve.
- [ ] Player auto-resolve.
- [ ] Siege assault.
- [ ] Siege defense.
- [ ] Village raid defense.
- [ ] Ambush or quest battle.
- [ ] Battle where surgeon is wounded.
- [ ] Save/load after battle with delayed wound risk.

## Recommended First Pass

Keep v1 simple:

- Apply revised casualty care to both sides after direct battles.
- Apply the same framework to auto-resolve.
- Use Surgery skill, battle outcome, and field control as the first modifiers.
- Add supplies only as an abstract optional slot if implementation is straightforward.
- Do not add delayed deaths until direct and auto-resolve parity is stable.
- Add report lines for player saves and enemy recovery.

The first pass should prove fairness and parity. Once that works, supplies and delayed wound outcomes can add realism without turning the system into bookkeeping.
