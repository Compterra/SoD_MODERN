# Companion Interactive Quest Playtest Matrix

Use this file for live Warband QA of the companion interactive quest campaign slices. Static tests prove the content is wired; this matrix proves the campaign feels correct in-engine.

Keep one save before accepting the companion incident and one save after the witness/clue step. That gives QA a clean way to test companion absence, wrong target suppression, success paths, hard paths, defeat recovery, and departure cleanup without replaying the entire campaign setup each time.

For fast setup, use `docs/COMPANION_INTERACTIVE_QUEST_QA_COMMANDS.md`. The debug accelerators can recruit companions, open trust, and prime a quest to the live climax or final aftermath, but they do not replace the live checks below.

## Universal Smoke Route

Run this route for every companion before testing branch-specific outcomes:

- [ ] Recruit the companion and confirm the quest trigger or direct-talk opening appears only while they are in the party.
- [ ] Remove or separate the companion and confirm the same trigger, witness, camp action, and final resolution do not appear.
- [ ] Start the quest, note the journal text, and verify it gives a world-facing target or action.
- [ ] Visit the wrong target first and confirm witness/contact options are suppressed.
- [ ] Visit the correct target or encounter surface with the companion present and confirm the witness/contact step advances progress.
- [ ] Try to resolve immediately after the witness step and confirm the final moral choice is still blocked until the confrontation/climax.
- [ ] Complete the interactive climax once by success and once by retreat/defeat where applicable.
- [ ] Resolve through companion dialogue or the intended fallback menu and confirm the companion comments on the method used.
- [ ] Check the companion report or follow-up dialogue for result-grade aftermath.
- [ ] Remove the companion after starting but before resolving and verify cleanup or recoverable blocking.

## Ymira - Mercy Under Arms

Focus: captive shelter, refugee witness, and a defense/standoff.

- [ ] Companion absence: Ymira-specific captive/refugee hooks do not appear without Ymira in party.
- [ ] Wrong target: refugee witness does not appear outside the selected focus center.
- [ ] Witness route: freed captive, elder, or refugee testimony sets the witnessed state and updates the journal.
- [ ] Climax success: win the refugee defense/standoff and verify final choices unlock.
- [ ] Defeat recovery: lose or retreat from the defense and verify the quest remains recoverable or records the intended failure grade.
- [ ] Best route: shelter, guard, and feed the vulnerable.
- [ ] Good route: protect them while rationing aid.
- [ ] Hard route: ransom, turn away, or exploit captives.
- [ ] Cleanup: Ymira departure clears refugee focus, witness, confrontation, and result state.

## Firentis - Debt Of The Sword

Focus: village restitution, witness testimony, and a public hearing or defense.

- [ ] Companion absence: restitution prompt does not appear without Firentis.
- [ ] Wrong village: witness option is absent outside the focus village.
- [ ] Refusal route: refuse restitution and verify Firentis reacts with withdrawal or warning.
- [ ] Payment/protection route: spend resources or leave guards and confirm progress.
- [ ] Public confession route: let truth be spoken and verify best/good aftermath.
- [ ] Combat victory: win the restitution defense.
- [ ] Combat defeat: lose or retreat and verify result grade/failure handling.
- [ ] Cleanup: Firentis departure clears focus, witness, confrontation, and result state.

## Deshavi - Tracks Through Ash

Focus: survivor testimony, trail pursuit, and rescue or hunt.

- [ ] Companion absence: trail or pursuer hooks do not appear without Deshavi.
- [ ] Wrong village: survivor witness does not appear outside the focus village.
- [ ] Witness route: survivor or hunter testimony marks the trail and updates the journal.
- [ ] Rescue victory: win the trail confrontation and verify aftermath unlocks.
- [ ] Rescue defeat: lose the rescue mission and verify recoverable failure behavior.
- [ ] Best route: protect survivors and captives.
- [ ] Good route: defeat raiders while limiting losses.
- [ ] Hard route: prioritize hunt or revenge over survivors.
- [ ] Cleanup: Deshavi departure clears village, trail, warning, witness, confrontation, and result state.

## Borcha - The Road Keeps Its Own

Focus: route witness, side road, and counter-ambush.

- [ ] Companion absence: Borcha road scouting content is blocked without Borcha.
- [ ] Route invalidation: travel away, change context, or use old save state and verify safe repair/fallback.
- [ ] Wrong town: tavernkeeper or road witness does not appear outside the route endpoint.
- [ ] Witness route: road witness marks the side road and updates the journal.
- [ ] Combat victory: win the counter-ambush.
- [ ] Combat defeat: lose or retreat and verify the failure grade.
- [ ] Bypass route: avoid the ambush cleanly.
- [ ] Profit route: exploit the road and confirm Borcha reacts to the method.
- [ ] Cleanup: Borcha departure clears route endpoints, witness, confrontation, and result state.

## Marnid - The Honest Price

Focus: market account, dirty contract, and warehouse/public resolution.

- [ ] Companion absence: Marnid market content does not appear without Marnid.
- [ ] Wrong town: goods merchant evidence does not appear outside the focus town.
- [ ] Evidence missing: final choices stay blocked before market evidence is collected.
- [ ] Public audit route: expose the dirty contract.
- [ ] Restitution route: repay losses while preserving order.
- [ ] Blackmail route: use the evidence for leverage and verify hard aftermath.
- [ ] Combat victory: win the warehouse confrontation.
- [ ] Combat defeat: lose or retreat and verify result grade/failure handling.
- [ ] Cleanup: Marnid departure clears focus, contact, evidence, confrontation, and result state.

## Bunduk - The Men Who Hold The Line

Focus: soldier grievance, line test, and command ethics.

- [ ] Companion absence: rank-and-file petition is blocked without Bunduk.
- [ ] Camp/garrison edge: verify the petition behaves in camp and valid center contexts.
- [ ] Morale edge: test low morale or strained company state and confirm fitting text.
- [ ] Witness route: regular soldier complaint sets witnessed state.
- [ ] Combat victory: win the line test.
- [ ] Combat defeat: lose or retreat and verify failure grade.
- [ ] Reform route: back the soldiers and improve conditions.
- [ ] Compromise route: solve the tactical issue without full reform.
- [ ] Hard-drive route: enforce command authority and confirm Bunduk's reaction.
- [ ] Cleanup: Bunduk departure clears focus, witness, confrontation, and result state.

## Jeremus - Hands That Will Not Harden

Focus: wounded witness, supply crisis, and infirmary defense.

- [ ] Companion absence: wounded/triage content is blocked without Jeremus.
- [ ] Low-supply flavor: start with low supplies and confirm shortage language or cost pressure.
- [ ] Witness route: wounded soldier/civilian/enemy account sets witnessed state.
- [ ] Infirmary route: enter the crisis only after witness state is set.
- [ ] Defend route: win the infirmary defense.
- [ ] Defeat route: lose or retreat and verify failure grade.
- [ ] Reorder route: use hard triage and confirm Jeremus's moral assessment.
- [ ] Company-first route: prioritize company strength and confirm hard aftermath.
- [ ] Cleanup: Jeremus departure clears witness, supplies, confrontation, and result state.

## Lezalit - Discipline Without Chains

Focus: recruit witness, captured drill, and controlled trial.

- [ ] Companion absence: drill content is blocked without Lezalit.
- [ ] Troop shortage: test with too few suitable troops and verify graceful flavor/blocking.
- [ ] Morale edge: test low morale and confirm discipline text is coherent.
- [ ] Witness route: recruit or regular soldier testimony sets witnessed state.
- [ ] Combat victory: win the drill trial.
- [ ] Combat defeat: lose or retreat and verify failure grade.
- [ ] Corrected drill route: reform the drill with discipline and restraint.
- [ ] Harsh-mark route: use fear and confirm warning/hard aftermath.
- [ ] Refusal route: reject the lesson and confirm Lezalit's reaction.
- [ ] Cleanup: Lezalit departure clears witness, confrontation, and result state.

## Artimenner - The Siege That Should Have Worked

Focus: siege-work inspection, repair witness, and repair watch.

- [ ] Companion absence: inspection is blocked without Artimenner.
- [ ] Invalid center: non-siege or missing target state repairs safely or blocks cleanly.
- [ ] Old-save repair: clear focus state in a test save and verify fallback behavior.
- [ ] Ladder inspection: inspect ladder works and verify witness/progress.
- [ ] Tower inspection: inspect siege tower works and verify witness/progress.
- [ ] Repair-watch victory: win the repair mission and unlock final resolution.
- [ ] Repair-watch defeat: lose or retreat and verify failure grade.
- [ ] Proper rebuild route: spend/commit to real repair.
- [ ] Simplify route: improvise a leaner plan.
- [ ] Blame-workers route: choose the hard shortcut and verify Artimenner's reaction.
- [ ] Cleanup: Artimenner departure clears focus, cause, witness, confrontation, and result state.

## Alayen - The Standard And The Self

Focus: public witness, banner duty, and standard test.

- [ ] Companion absence: public challenge is blocked without Alayen.
- [ ] Invalid center/faction: old or unsuitable focus state repairs safely or blocks cleanly.
- [ ] Village elder witness: elder challenge sets witnessed state.
- [ ] Lord witness: lord/court challenge sets witnessed state.
- [ ] Standard-test victory: win the public standard test.
- [ ] Standard-test defeat: lose or retreat and verify failure grade.
- [ ] Public-cost route: make honor serve dependents.
- [ ] Prestige route: choose obedience/display and verify hard aftermath.
- [ ] Cleanup: Alayen departure clears focus, witness, confrontation, and result state.

## Rolf - A Name Worth Wearing

Focus: public claim, witness pressure, and proof.

- [ ] Companion absence: Rolf name challenge is blocked without Rolf.
- [ ] Witness absence: final resolution is blocked before the public witness.
- [ ] Wrong town: witness does not appear outside the focus town.
- [ ] Public proof victory: win the public proof mission.
- [ ] Combat loss/public failure: lose or retreat and verify result grade.
- [ ] Service route: answer with useful conduct.
- [ ] Theater route: defend Rolf theatrically without cruelty.
- [ ] Exposure route: strip away the performance and verify hard aftermath.
- [ ] Cleanup: Rolf departure clears focus, witness, confrontation, and result state.

## Baheshtur - The Unbroken Saddle

Focus: rider witness, oath custom, and mounted trial.

- [ ] Companion absence: rider-oath content is blocked without Baheshtur.
- [ ] Black Khergit raider witness: raider testimony sets witnessed state.
- [ ] Night guard witness: alternate Black Khergit guard testimony sets witnessed state.
- [ ] No-witness camp suppression: rider-oath trial is absent before witness state.
- [ ] Rider-oath combat win: win the trial and unlock final choices.
- [ ] Rider-oath combat loss: lose or retreat and verify failure grade.
- [ ] Free oath route: let riders swear freely.
- [ ] Clean surrender route: defeat and spare riders.
- [ ] Bind route: force submission and verify hard aftermath.
- [ ] Cleanup: Baheshtur departure clears focus party, witness, confrontation, and result state.

## Matheld - No Backward Step

Focus: ranker witness, shield-line test, and cost of courage.

- [ ] Companion absence: shield-line content is blocked without Matheld.
- [ ] Ranker witness: regular member testimony sets witnessed state.
- [ ] No-witness camp suppression: shield-line test is absent before witness state.
- [ ] Shield-line combat win: win the test and unlock final choices.
- [ ] Shield-line combat loss: lose or retreat and verify failure grade.
- [ ] Breathing-wall route: temper courage and protect the line.
- [ ] Stand-firm route: win the stand with acceptable losses.
- [ ] Blood-roar route: choose blood-price and verify hard aftermath.
- [ ] Cleanup: Matheld departure clears focus party, witness, confrontation, and result state.

## Nizar - The Impossible Charge

Focus: field setup, charge-lane test, and glory with consequences.

- [ ] Companion absence: charge setup is blocked without Nizar.
- [ ] Field setup: battle reason option marks the charge and updates the journal.
- [ ] No-field-setup camp suppression: charge-lane test is absent before witnessed state.
- [ ] Charge-lane combat win: win the lane mission and unlock final choices.
- [ ] Charge-lane combat loss: lose or retreat and verify failure grade.
- [ ] Exit-first route: prioritize the escape plan.
- [ ] Dazzling route: choose survivable spectacle.
- [ ] Applause-first route: choose glory over safety and verify hard aftermath.
- [ ] Cleanup: Nizar departure clears pending, cause, witness, confrontation, and result state.

## Katrin - The Last Coin In Camp

Focus: account witness, supply pressure, and supply watch.

- [ ] Companion absence: ledger/account content is blocked without Katrin.
- [ ] Low-money account witness: low-cash route gives appropriate account pressure.
- [ ] Low-food regular-member witness: food shortage route sets witness state.
- [ ] No-witness camp suppression: supply watch is absent before witness state.
- [ ] Supply-watch combat win: win the supply watch and unlock final choices.
- [ ] Supply-watch combat loss: lose or retreat and verify failure grade.
- [ ] Open-books route: pay the real cost and stabilize the camp.
- [ ] Stretch-stores route: ration without cruelty.
- [ ] Hide-shortage route: conceal or squeeze losses and verify hard aftermath.
- [ ] Cleanup: Katrin departure clears pending, witness, confrontation, and result state.

## Sign-Off

When a companion passes every row, mark the matching manual QA line in `docs/COMPANION_INTERACTIVE_QUEST_CHECKLIST.md`. Leave failures unchecked and record the save, companion, route, observed behavior, expected behavior, and likely file surface.
