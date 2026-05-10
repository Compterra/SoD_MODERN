# Unique Quest NPCs Checklist

## Purpose
Unique quest NPCs should feel like people caught in specific pressures, not generic menu tokens. They need a clear identity, a safe quest surface, and at least one line or behavior that explains why this encounter matters in the world.

## First Slice
- [x] Audit fugitive, kidnapped girl, runaway serf, runaway slave, Diego, and wine-recipient dialogue surfaces.
- [x] Replace generic fugitive denial lines with characterful defensive lines.
- [x] Improve kidnapped girl road dialogue and no-room fallback.
- [x] Improve runaway serf and runaway slave plea text.
- [x] Fix runaway slave return behavior so it uses the slaver runaway quest target, not the serf quest target.
- [x] Send freed runaway slaves toward the nearest valid village, with a safe random fallback.
- [x] Improve Diego and wine-recipient quest actor openings without changing quest flow.
- [x] Add static coverage for registration, quest-target safety, and non-placeholder lines.
- [x] Preserve the kidnapped girl quest-party woman icon and hold behavior when the player has no party room.
- [x] Replace the battle no-room fallback with a proper `pt_kidnapped_girl` quest party instead of companion-party spawning.
- [x] Harden Diego's secret quest opening so it cannot restart after active, succeeded, or failed chain states.
- [x] Close Diego's refusal path cleanly by failing/ending the return-to-Diego stage.

## NPC Archetype Standard
For each unique quest NPC:

- [ ] Give the NPC a one-sentence identity and immediate pressure.
- [ ] Give the NPC at least one line that names what they fear, want, or owe.
- [ ] Keep the quest path safe if the player lacks room, money, relation, or valid targets.
- [ ] Store or derive a focus center, focus party, or focus cause where possible.
- [ ] Prefer dialogue or encounter resolution over abstract camp-menu resolution.
- [ ] Add a report or journal hint when the next step is not obvious.
- [ ] Add companion reactions when the choice touches mercy, slavery, honor, trade, discipline, or cruelty.

## Priority NPC Groups
- [ ] Fugitives: add village/town witness hints and post-capture flavor.
- [ ] Kidnapped girl: add safer waiting state, family-home hint, and rescue aftermath.
- [ ] Runaway serfs: connect to center health, overtaxing, famine, and lord reputation.
- [ ] Runaway slaves: connect to Slaver heat, Jotnar/Elephant Guard sanctuary, and companion approval.
- [x] Diego: harden secret-quest progression against duplicate reward/release loops.
- [ ] Wine recipient: add smuggling suspicion, route risk, and Slaver market consequences.
- [ ] Quest ransom broker/reward NPCs: verify unique spawn/reward idempotence.

## Static Coverage
- [x] Unique quest NPC dialogue files are registered.
- [x] Fugitive denial lines are no longer generic placeholders.
- [x] Runaway slave return uses the slaver quest target.
- [x] Freed runaway slaves use a validated village destination.
- [x] Diego, wine recipient, and kidnapped girl retain their quest surfaces.
- [x] Kidnapped girl no-room fallbacks preserve quest state, target party, and map icon identity.
- [x] Diego secret quest start/accept/refusal branches have idempotent quest-state guards.
- [ ] Static check for duplicate unique reward NPC creation.
- [ ] Static check for unique quest NPCs using invalid center or party globals.
- [ ] Static check for camp/menu fallback branches that should become direct dialogue.

## Manual QA
- [ ] Hunt fugitive quest can complete through both lord and guild master paths.
- [ ] Kidnapped girl can be rescued, carried, and returned without party-capacity lockout.
- [ ] Runaway serfs can be returned or freed without invalid destination errors.
- [ ] Runaway slaves can be returned or freed without cross-wiring to serf quest state.
- [ ] Diego secret quest cannot be completed repeatedly for duplicate rewards.
- [ ] Wine delivery quest has clear success/failure dialogue and no leaked strings elsewhere.
