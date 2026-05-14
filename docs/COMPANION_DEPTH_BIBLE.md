# Companion Depth Bible

This document is the narrative and systems reference for making companions feel closer to Dragon Age: Origins companions: opinionated, reactive, wounded, loyal for reasons, and dangerous to disappoint. It sits beside the existing cohesion and grievance system.

## Design Pillars

- Approval answers: does this companion believe in the player?
- Cohesion answers: can the company survive its own internal friction?
- Warnings come before departures. A companion should confront the player before a final break.
- Approval is shown in story bands, not raw numbers: devoted, loyal, steady, wary, troubled, near breaking.
- Campfire conversations are the player-facing surface for mood, warnings, role assignments, and personal quest leads.
- Advisor roles are small bonuses tied to trust. Low approval should weaken or disable the role.
- Personal quests should reveal why the companion fights, what they fear becoming, and what kind of commander they can follow.

## Shared Action Vocabulary

These action types should feed `script_sod_companion_apply_player_action` as more systems are expanded:

- Freeing captives or refugees.
- Buying slaves, selling slaves, or strengthening the Slaver market.
- Sparing prisoners, executing lords, or using terror as policy.
- Helping villages, training peasants, stealing supplies, or looting villages.
- Winning against hard odds, fleeing battles, heavy casualties, and failing quests.
- Supporting Jotnar hearth work, Elephant Guard protection, or other defensive mini-factions.
- Paying Black Khergit tribute, bribing raiders toward another target, or breaking the horde.
- Defeating Imperial Expeditionary Force armies or adopting Imperial cruelty.
- Diplomatic choices: honorable peace, opportunistic betrayal, expansionist war, or restraint.

## Roster Matrix

| Companion | Core Fantasy | Best Roles | Strong Likes | Sharp Dislikes | First Quest Hook |
| --- | --- | --- | --- | --- | --- |
| Borcha | Road-hardened pathfinder | Scout, Quartermaster | Survival, roadcraft, low losses, Marnid | Heavy casualties, noble posturing, rash command | The Road Keeps Its Own |
| Marnid | Ledger cavalry trader | Quartermaster, Envoy | Trade, completed work, orderly profit, Borcha | Village theft, failed quests, waste | The Honest Price |
| Ymira | Mercy under arms | Surgeon, Envoy | Freeing captives, helping villages, Alayen | Slavery, executions, village abuse, Lezalit | Mercy Under Arms |
| Rolf | Fallen noble longbowman | Envoy, Captain | Reputation, titles, audacity, Baheshtur | Commoner insolence, Bunduk, Deshavi | A Name Worth Wearing |
| Baheshtur | Proud steppe scout | Scout, Captain | Mobility, independence, Rolf | Heavy casualties, Marnid, Katrin | The Unbroken Saddle |
| Firentis | Atoning veteran | Captain, Envoy | Discipline with mercy, Jeremus | Cruelty, village abuse, too much fighting | Debt of the Sword |
| Deshavi | Dvor archer survivor | Scout, Spymaster | Food security, caution, Klethi | Hunger, wasted lives, Borcha, Rolf | Tracks Through Ash |
| Matheld | Proud cavalry shield | Captain | Courage, hard charges, Nizar | Fleeing battle, soft restraint, Ymira | No Backward Step |
| Alayen | Antarian noble tactician | Envoy, Captain | Honor, victory, Ymira | Failed obligations, Marnid, Nizar | The Standard and the Self |
| Bunduk | Practical crossbow sergeant | Captain, Quartermaster | Soldiers' welfare, Katrin | Village abuse, heavy losses, Rolf, Lezalit | The Men Who Hold the Line |
| Katrin | Camp matron and trader | Quartermaster, Surgeon | Pay, food, Bunduk | Hunger, unpaid troops, Baheshtur, Firentis | The Last Coin in Camp |
| Jeremus | Healer with a conscience | Surgeon, Envoy | Peace, healing, Firentis | Village abuse, too much fighting, Matheld | Hands That Will Not Harden |
| Nizar | Daring boyar son | Captain, Scout | Glory, tough odds, Matheld | Caution, Firentis, Alayen | The Impossible Charge |
| Lezalit | Discipline without chains | Captain | Training, order, Artimenner | Weak command, Ymira, Bunduk | Discipline Without Chains |
| Artimenner | Engineer quartermaster | Engineer, Quartermaster | Plans, sieges, Lezalit | Hunger, failed quests, Jeremus, Klethi | The Siege That Should Have Worked |
| Klethi | Knife and pathfinder | Spymaster, Scout | Quiet opportunity, Deshavi | Hunger, failed quests, Borcha, Artimenner | A Knife With a Name |

## Borcha

**Theme:** The road teaches faster than lords do.

Borcha should feel like a man who has survived by reading mud, hoofprints, lies, and weather. He is not romantic about war. He respects commanders who keep the party fed, avoid pointless losses, and understand that the map is also a weapon.

**Background:** Borcha grew up around roads used by smugglers, tax men, deserters, and frightened villagers. He learned early that law and safety are not the same thing. His skill is not just tracking; it is knowing which promises are traps.

**Core wound:** He expects every commander to eventually spend poor men like loose coin. He laughs first so nobody hears the fear underneath.

**What he wants from the player:** Proof that the player can listen to rough knowledge instead of only noble counsel.

**Inner conflict:** Borcha wants to be trusted, but he also survives by never fully trusting anyone. His best arc lets him become the company's road conscience instead of merely its scout.

**Approval rises from:** low-casualty victories, scouting choices, breaking Black Khergit pressure, keeping the party fed, pragmatic mercy that prevents future trouble, and trusting pathfinders over noble advice.

**Approval falls from:** heavy losses, starving the party, charging blindly, noble vanity, ignoring ambush signs, and using peasants as expendable cover.

**Relationships:** Likes Marnid because both understand practical survival. Clashes with Rolf over rank and with Deshavi/Klethi over rival road instincts.

**Role design:** Scout should improve map movement, tracking, or ambush warnings. Quartermaster should reduce food strain only while Borcha remains steady or better.

**Quest pitch - The Road Keeps Its Own:** Borcha recognizes signs of a hidden raider route. The player can help local scouts, exploit the route for plunder, or ignore it. Good resolution gives a scout role boost and a campfire talk about trust.

**Voice guide:** Borcha speaks in short, dry lines with road images: mud, hoofprints, weather, smoke, tracks, knives in sleeves. He dislikes fancy names for simple dangers. His humor is sideways and defensive. When affectionate, he gives practical warnings before anyone asks. When angry, he stops joking and becomes flatly specific.

**Taboo language:** Avoid courtly abstractions from Borcha unless he is mocking them. He should not say "honor demands" or "destiny" sincerely. He should say things like "that road is too clean" or "men do not ride that slow unless they want to be seen."

**Approval reaction tiers:**

- Minor approval: low-casualty victory, scouting choice, feeding the party, avoiding an obvious ambush.
- Major approval: breaking a Black Khergit raid route, trusting his warning over a noble source, saving villagers through roadcraft instead of glory.
- Warning: repeated heavy casualties, ignored ambush signs, starving the party, using scouts as expendable bait.
- Breaking point: the player knowingly marches into disaster for pride and then blames the dead or the scouts.

**Quest outcome index:**

- Trust resolution: Borcha becomes a loyal Scout. Map movement or ambush-warning effects improve while approval is steady or better.
- Pragmatic resolution: Borcha accepts the player as competent but guarded. Mechanical bonus is smaller, but he remains stable.
- Exploitative resolution: the player uses the hidden route for plunder. Borcha gains respect for cunning but loses trust; this can open darker underworld options later.
- Failure or dismissal: Borcha becomes wary, warns the player, and may refuse the Scout role bonus until repaired.

**Focused implementation notes:** Borcha is the best first full companion because his arc can reuse existing world systems without new scenes: Black Khergit routes, Slaver caravans, road patrols, village danger, party food, and casualty results. His first content pass should add campfire mood lines, a Scout role refinement, and the opening stage of `The Road Keeps Its Own`.

## Marnid

**Theme:** Profit is not evil, but careless profit is rot.

Marnid should be worldly, commercial, and more morally flexible than Ymira or Jeremus, but not mindless. He wants stable routes, paid contracts, and exchanges that leave tomorrow's trade possible.

**Background:** Marnid comes from ledgers, caravans, tolls, and bad bargains. He has seen towns starve because a lord wanted glory and traders ruined because a "just" army paid in promises.

**Core wound:** He fears poverty more than dishonor, because he has seen poverty strip people of choice. This makes him vulnerable to rationalizing ugly commerce.

**What he wants from the player:** A commander who understands that money is a nervous system, not a decoration.

**Inner conflict:** Marnid can become either the company's humane quartermaster or the man who explains why every dirty bargain is necessary.

**Approval rises from:** successful quests, trade profits, paid troops, caravan protection, sensible ransoms, and diplomatic settlements that reopen roads.

**Approval falls from:** taking from villagers, failing promised work, wasteful bribes, unpaid troops, and chaos that destroys markets.

**Relationships:** Likes Borcha's road sense. Dislikes Baheshtur's pride and Alayen's noble assumptions.

**Role design:** Quartermaster can reduce wage or food friction. Envoy can improve trade-facing negotiations.

**Quest pitch - The Honest Price:** Marnid's old contacts offer access to a profitable but dirty prisoner market. The player can cleanly break the link, exploit it, or turn it against Slaver brokers.

## Ymira

**Theme:** Mercy under arms.

Ymira should be the conscience who has learned that kindness in wartime must be chosen deliberately. She is not naive; she sees danger early and values tactical retreats when they save lives.

**Background:** Ymira was taught to be quiet before she learned to be brave. War put her among wounded soldiers, frightened captives, and commanders who called cruelty "necessity."

Her first real usefulness in a war camp was not a grand act. She held bowls, tore linen, remembered names, and watched how quickly commanders stopped seeing the people who could not stand. That memory should make her gentle without making her soft. Ymira knows mercy needs guards, food, routes, and orders. She respects force when it protects the vulnerable, but recoils when force starts feeding on them.

**Core wound:** She believes helpless people disappear when nobody important insists on seeing them.

**What she wants from the player:** Evidence that power can protect without becoming predatory.

**Inner conflict:** Ymira must learn that mercy sometimes needs force behind it, while the player must prove that force will not swallow the mercy.

**Approval rises from:** freeing captives, sparing prisoners, helping villages, anti-Slaver choices, healing decisions, and withdrawing to protect troops.

**Approval falls from:** buying or selling slaves, lord executions, needless cruelty, village abuse, and treating captives as inventory.

**Relationships:** Likes Alayen's better version of honor. Clashes with Matheld's hardness and Lezalit's doctrine.

**Role design:** Surgeon is her natural role. Her personal quest can unlock a stronger recovery bonus if resolved mercifully.

**Quest - Mercy Under Arms:** A refugee or captive crisis forces the player to choose mercy, ransom, or expedience. A good resolution grants permanent loyalty and a campfire reflection. A bad resolution makes her wary and can trigger a warning.

**Voice notes:** Ymira should speak plainly, with quiet moral pressure rather than sermons. She rarely says "you are evil"; she says what the order did to the person under it. Her sharpest lines should come when the player turns people into categories: slaves, prisoners, mouths, losses, inventory.

**Gameplay expression:** Ymira should react most strongly to captive outcomes, Slaver cooperation, freed refugees, village protection, healing infrastructure, and unnecessary executions. If her Surgeon role is trusted and Mercy Under Arms ends well, freeing captives should feel organized rather than symbolic: water, bandages, names, routes, and morale.

**Triangle pressure:** Ymira, Lezalit, and Bunduk should turn post-battle decisions into a command argument. Ymira asks who is protected, Lezalit asks whether the army remains disciplined, and Bunduk asks whether ordinary soldiers are being spent or abused.

## Rolf

**Theme:** A name can be armor, or a lie.

Rolf should feel like a man performing nobility until performance and identity blur. He values command presence, lineage, and the appearance of rightful order, but can be pushed to ask whether his title still means anything.

**Background:** Rolf's past should remain partly suspect by design. Whether he truly lost a noble inheritance or built one out of smoke matters less than his need for a world where names command respect.

**Core wound:** He is terrified that without title, story, and ceremony, he is ordinary.

**What he wants from the player:** Public legitimacy. He wants the company to look like destiny, not a band of armed strays.

**Inner conflict:** Rolf can grow from a man hiding inside a title into someone worthy of the authority he claims.

**Approval rises from:** public honors, decisive victories, diplomatic recognition, noble etiquette, and bold gambits.

**Approval falls from:** humiliation, being contradicted by common soldiers, peasant-first policy, and choices that make the company look shabby or lawless.

**Relationships:** Likes Baheshtur's proud bearing. Clashes with Deshavi and Bunduk, who see through rank too quickly.

**Role design:** Envoy can improve noble-facing diplomacy. Captain can provide morale through command presence.

**Quest pitch - A Name Worth Wearing:** A claimant or local lord challenges Rolf's identity. The player can expose, defend, or redefine him.

## Baheshtur

**Theme:** Pride rides faster than fear.

Baheshtur should be mobile, proud, and intolerant of being caged by town rules. He respects strength and independence, but hates waste.

**Background:** Baheshtur was shaped by open country, clan expectation, and the knowledge that a rider who cannot choose his own direction is already half captured.

**Core wound:** He fears becoming dependent on settled powers that smile while tightening reins.

**What he wants from the player:** A commander with enough strength to bargain freely and enough pride not to crawl.

**Inner conflict:** Baheshtur's independence can become wisdom or isolation. His arc should ask whether loyalty chosen freely is still freedom.

**Approval rises from:** fast campaigns, mounted victories, successful raids against predators, refusing humiliation, and bold travel through dangerous territory.

**Approval falls from:** heavy casualties, timid command, excessive bargaining, hunger, and being trapped in slow defensive wars.

**Relationships:** Likes Rolf's pride. Dislikes Marnid's ledger mindset and Katrin's camp economy.

**Role design:** Scout improves speed and pursuit. Captain improves cavalry confidence.

**Quest pitch - The Unbroken Saddle:** A steppe rival or Black Khergit warband tests whether Baheshtur's pride protects the company or endangers it.

## Firentis

**Theme:** A sword can serve penance, but never erase it.

Firentis should be a soldier trying to make discipline into atonement. He can fight hard, but repeated cruelty convinces him the company is becoming the thing he fears.

**Background:** Firentis carries a private history of blood and shame. He understands violence too well to romanticize it, and that makes him both useful and haunted.

**Core wound:** He does not believe he deserves forgiveness, but he keeps testing whether service can still mean something.

**What he wants from the player:** A command that gives discipline a moral purpose.

**Inner conflict:** Firentis needs to fight without using war as punishment for himself. His best arc lets him accept duty without self-erasure.

**Approval rises from:** honorable restraint, protecting villages, training troops, sparing the helpless, and fighting necessary wars cleanly.

**Approval falls from:** village abuse, pointless fighting, failed promises, executions, and cruelty used as convenience.

**Relationships:** Likes Jeremus. Dislikes Katrin and Nizar for different kinds of temptation: hard practicality and reckless glory.

**Role design:** Captain can improve discipline and morale after hard choices. Envoy can help honor-facing diplomacy.

**Quest pitch - Debt of the Sword:** A victim from Firentis's past appears. The player chooses confession, concealment, restitution, or violence.

## Deshavi

**Theme:** Hunger makes truth simple.

Deshavi should speak from survival. She cares about food, caution, and not wasting lives. She distrusts rank and polished speech.

**Background:** Deshavi learned the world from margins: forests, cold tracks, empty stores, and people who could not afford noble mistakes. She knows how quickly hunger turns law into theatre.

**Core wound:** She expects leaders to notice villages only after they burn.

**What she wants from the player:** Practical protection for people who never get speeches made about them.

**Inner conflict:** Deshavi trusts hardship more than hope. Her arc should let her believe the company can protect the forgotten without making her soft.

**Approval rises from:** keeping stores full, avoiding needless casualties, scouting enemy movements, protecting poor villages, and ambushing raiders before they strike.

**Approval falls from:** hunger, heavy losses, vanity, ignoring local guides, and using desperate people.

**Relationships:** Likes Klethi's quiet competence. Dislikes Borcha as a rival tracker and Rolf as a symbol of rank.

**Role design:** Scout improves detection and pathfinding. Spymaster improves ambush and warning events.

**Quest pitch - Tracks Through Ash:** Deshavi finds signs of a destroyed settlement tied to raiders or slavers. The player can pursue justice, rescue survivors, or keep marching.

## Matheld

**Theme:** Courage is the last law.

Matheld should be blunt, hard, and proud. She believes survival belongs to those who stand their ground, and she has little patience for retreat dressed as wisdom.

**Background:** Matheld comes from a culture where reputation is armor and fear spreads faster than wounds. She learned that one public retreat can invite ten private humiliations.

**Core wound:** She fears that mercy, compromise, and withdrawal will be read as weakness by enemies who only understand force.

**What she wants from the player:** Courage that does not apologize for itself.

**Inner conflict:** Matheld must learn the difference between bravery and refusing to bend even when bending saves lives.

**Approval rises from:** refusing flight, winning hard battles, direct challenges, punishing raiders, and protecting the company's honor.

**Approval falls from:** fleeing battle, repeated mercy that creates danger, hesitating before weaker enemies, and letting insults stand.

**Relationships:** Likes Nizar's daring. Clashes with Ymira and Jeremus over mercy and restraint.

**Role design:** Captain improves morale in difficult fights and reduces fear penalties.

**Quest pitch - No Backward Step:** Matheld demands a direct answer to a threat that wiser voices would avoid. The quest tests courage against needless bloodshed.

## Alayen

**Theme:** Honor is not polish; it is obligation.

Alayen should begin as noble and severe, but his best arc turns honor from status into responsibility. He wants victories that can be defended in memory.

**Background:** Alayen was raised to believe noble blood carries duties as well as privileges. He has seen enough corruption to be defensive about the idea of honor, but not enough humility to stop sounding superior.

**Core wound:** He fears his birth means nothing if he cannot prove himself worthy of it.

**What he wants from the player:** A commander who treats promises, banners, and reputation as binding things.

**Inner conflict:** Alayen must decide whether honor is a mirror for himself or a burden carried for others.

**Approval rises from:** honorable victories, completed oaths, protecting villages, disciplined tactics, and mercy that preserves dignity.

**Approval falls from:** failed quests, crude profiteering, dishonorable deals, and being shown up by swagger without discipline.

**Relationships:** Likes Ymira's moral clarity. Dislikes Marnid's commercial flexibility and Nizar's flamboyance.

**Role design:** Envoy improves noble diplomacy. Captain improves formation discipline.

**Quest pitch - The Standard and the Self:** Alayen must choose between family pride and a humbler act of genuine honor.

## Bunduk

**Theme:** The line holds because ordinary soldiers do.

Bunduk should be the voice of rank-and-file sanity. He dislikes cruelty from above and noble vanity, but he is not soft. He wants practical discipline that keeps soldiers alive.

**Background:** Bunduk's loyalty belongs first to the line soldier: the tired crossbowman, the man with bad boots, the recruit ordered to die for a banner he cannot read.

**Core wound:** He has watched officers call waste "discipline" and then blame the dead for obeying.

**What he wants from the player:** Respect for ordinary soldiers as people, not ammunition.

**Inner conflict:** Bunduk distrusts command, yet he is a natural commander when he stops defining leadership by the worst officers he has known.

**Approval rises from:** protecting troops, paying wages, avoiding heavy casualties, defending villages, and respecting common soldiers.

**Approval falls from:** village abuse, heavy losses, noble arrogance, cruel discipline, and sacrificing soldiers for spectacle.

**Relationships:** Likes Katrin's practical care. Dislikes Rolf and Lezalit, especially when discipline becomes domination.

**Role design:** Captain can reduce casualty shock. Quartermaster can improve wage stability.

**Quest pitch - The Men Who Hold the Line:** Veterans ask Bunduk to speak for them against a brutal officer, noble, or player policy.

## Katrin

**Theme:** Somebody has to count the food.

Katrin should be practical, older in spirit, and allergic to heroic nonsense that leaves the camp hungry. She may sound mercenary, but her care is material: food, pay, medicine, blankets.

**Background:** Katrin has survived by keeping accounts nobody else wanted to keep: grain gone moldy, wages overdue, widows unpaid, wounded men needing clean cloth.

**Core wound:** She believes people praise sacrifice mostly when someone else is doing the sacrificing.

**What she wants from the player:** Competence in the unglamorous duties that keep a company alive.

**Inner conflict:** Katrin can hide tenderness behind scolding and arithmetic. Her arc should show that practicality is one of her forms of love.

**Approval rises from:** feeding the party, paying troops, sensible trading, caring for wounded, and avoiding waste.

**Approval falls from:** hunger, unpaid troops, reckless spending, endless glory campaigns, and choices that make camp life harder.

**Relationships:** Likes Bunduk. Dislikes Baheshtur's pride and Firentis's moral burden when it gets impractical.

**Role design:** Quartermaster improves stores and wage pressure. Surgeon gives modest practical care.

**Quest pitch - The Last Coin in Camp:** A shortage forces the player to choose between soldiers' wages, refugees, bribes, or future supplies.

## Jeremus

**Theme:** Healing is a rebellion against the age.

Jeremus should be gentle but not weak. He knows war may be necessary, but too much fighting makes him believe the commander has stopped looking for another road.

**Background:** Jeremus has seen the inside of wounds and the silence after fever. He understands the cost of victory in bodies, not songs.

**Core wound:** He fears that healing only patches men long enough for commanders to spend them again.

**What he wants from the player:** A reason to believe the company fights toward an end to suffering, not merely through it.

**Inner conflict:** Jeremus must decide when refusal to harm becomes permission for worse harm. His arc should test compassion under pressure.

**Approval rises from:** healing choices, restraint, peace, sparing civilians, helping villages, and supporting Firentis's atonement.

**Approval falls from:** village abuse, excessive fighting, executions, slavery, and choosing violence when diplomacy would work.

**Relationships:** Likes Firentis. Clashes with Matheld and Artimenner when hard realism overrides mercy.

**Role design:** Surgeon is primary. Envoy can help peace-facing diplomacy.

**Quest pitch - Hands That Will Not Harden:** Jeremus faces a battlefield triage choice where the player decides whether enemies, allies, or civilians receive care first.

## Nizar

**Theme:** Glory is a fire that wants feeding.

Nizar should be charming, reckless, and obsessed with the story people will tell afterward. His approval system should reward impossible victories and punish dreary caution.

**Background:** Nizar grew up close enough to privilege to taste glory, but not secure enough to rest in it. He performs brilliance because being merely competent feels like vanishing.

**Core wound:** He fears being forgotten more than being killed.

**What he wants from the player:** A campaign worthy of song, rumor, and envy.

**Inner conflict:** Nizar's hunger for legend can inspire the company or get people killed for applause. His best arc turns style into courage with responsibility.

**Approval rises from:** winning against tough odds, daring charges, public renown, high-risk rescues, and bold defiance of stronger enemies.

**Approval falls from:** excessive caution, moral lectures, retreats without style, and commanders who hide behind procedure.

**Relationships:** Likes Matheld. Dislikes Firentis's guilt and Alayen's stiff honor.

**Role design:** Captain improves morale after unlikely victories. Scout can improve pursuit and chase events.

**Quest pitch - The Impossible Charge:** Nizar pushes for a heroic action that may inspire allies or cost lives if mishandled.

## Lezalit

**Theme:** Discipline without chains.

Lezalit should be the uncomfortable test of whether strength requires cruelty. He values training, order, and punishment, but the player's choices can push him toward reform or colder doctrine.

**Background:** Lezalit was formed by instructors who believed fear was the cleanest path to obedience. He learned the lesson well, then spent years mistaking obedience for excellence.

**Core wound:** He fears disorder because he has seen weak command turn men into a mob and mobs into graves.

**What he wants from the player:** A commander strong enough to make standards real.

**Inner conflict:** Lezalit must confront whether discipline is meant to forge soldiers or break people until they stop resisting.

**Approval rises from:** disciplined command, training troops, defeating Imperial forces, holding formation, and refusing cowardice.

**Approval falls from:** weak command, repeated retreats, unpaid troops, chaotic mercy that harms the army, and sentimental decisions that get soldiers killed.

**Relationships:** Likes Artimenner's technical rigor. Dislikes Ymira and Bunduk, who challenge the human cost of his doctrine.

**Role design:** Captain is primary. A good quest resolution can improve training without requiring cruelty.

**Quest - Discipline Without Chains:** An Imperial-related discipline test forces punishment, reform, or defiance. Resolution grants improved Captain role, a unique training bonus, or a colder but stable loyalty state.

## Artimenner

**Theme:** Bad plans kill more men than bad swords.

Artimenner should think in structures, logistics, timetables, walls, and failure points. He has little patience for soft hearts that ignore engineering reality.

**Background:** Artimenner's life has been shaped by things that stand or fall according to design. He trusts stone, angles, measurements, and preparation more than speeches.

**Core wound:** Somewhere in his past, a preventable failure killed people while fools argued over blame.

**What he wants from the player:** Respect for expertise before disaster proves it right.

**Inner conflict:** Artimenner can be so focused on systems that he forgets people are not load-bearing beams. His arc should make him better without making him sentimental.

**Approval rises from:** prepared sieges, engineering investments, good supplies, completed objectives, and respecting specialist advice.

**Approval falls from:** hunger, failed quests, heavy casualties, improvising when planning was possible, and ignoring siege logic.

**Relationships:** Likes Lezalit. Dislikes Jeremus and Klethi, one for mercy-first instincts and the other for informal opportunism.

**Role design:** Engineer improves siege preparation. Quartermaster improves logistical planning.

**Quest pitch - The Siege That Should Have Worked:** Artimenner revisits a failed design or siege and must choose whether to admit error, blame others, or build something better.

## Klethi

**Theme:** A small knife can change a large war.

Klethi should be quick, wary, and allergic to grand speeches. She survives through opportunity, quiet routes, and knowing when nobody is looking.

**Background:** Klethi grew up in spaces where nobody asked permission because permission was never granted. Doors, purses, and secrets all open if a person is patient enough.

**Core wound:** She believes belonging is usually a trick used to make people easier to betray.

**What she wants from the player:** Freedom to be useful without being owned, shamed, or preached at.

**Inner conflict:** Klethi can either remain a knife for hire or become someone who chooses a side without feeling trapped by it.

**Approval rises from:** ambushes, successful scouting, clever theft from enemies, feeding the party, freeing captives through stealth, and giving scouts autonomy.

**Approval falls from:** hunger, failed quests, heavy casualties, loud honor displays, and plans too rigid to exploit luck.

**Relationships:** Likes Deshavi. Dislikes Borcha as a rival survivor and Artimenner as a planner who distrusts improvisation.

**Role design:** Spymaster improves covert warnings and underworld options. Scout improves route safety.

**Quest pitch - A Knife With a Name:** Klethi is recognized by someone from a job gone wrong. The player can protect her, sell her out, or make her face the damage.

## Companion Voice Guides

These are compact writing rules for campfire lines, warnings, quest dialogue, and companion reactions.

| Companion | Sentence Style | Humor | Affection | Anger |
| --- | --- | --- | --- | --- |
| Borcha | Short, practical, roadwise | Dry, evasive | Gives warnings and route advice | Flat, specific, stops joking |
| Marnid | Measured, transactional, observant | Wry merchant irony | Finds a better price or safer bargain | Talks about cost, waste, and broken trust |
| Ymira | Gentle but direct | Rare, soft, self-aware | Notices suffering and thanks the player quietly | Hurt first, then morally firm |
| Rolf | Ornate, self-important, theatrical | Grandiose boasting | Public praise and ceremonious loyalty | Insults status and legitimacy |
| Baheshtur | Lean, proud, open-country imagery | Sharp and disdainful | Respects freedom and courage | Calls out cowardice or weakness |
| Firentis | Restrained, grave, plain | Almost none | Offers service and sober gratitude | Sounds ashamed of the company |
| Deshavi | Sparse, sensory, survival-focused | Bitter, quiet | Shares food, signs, and warnings | Names the harm without decoration |
| Matheld | Blunt, forceful, physical | Mocking and martial | Stands beside the player openly | Challenges courage and resolve |
| Alayen | Formal, severe, duty-bound | Dry noble disapproval | Speaks of trust as obligation | Accuses the player of dishonor |
| Bunduk | Soldierly, grounded, direct | Barracks sarcasm | Speaks for the men and includes the player | Condemns waste and officer cruelty |
| Katrin | Practical, domestic, exact | Scolding, warm when trusted | Keeps the camp fed and fusses over details | Counts the damage aloud |
| Jeremus | Soft, careful, morally precise | Gentle, sad irony | Offers healing and counsel | Disappointed, wounded, persistent |
| Nizar | Flourished, charming, dramatic | Frequent and performative | Makes the player part of the legend | Calls the player dull or small |
| Lezalit | Clipped, doctrinal, precise | Rare, cutting | Acknowledges standards met | Names weakness and disorder |
| Artimenner | Technical, impatient, exact | Acidic professional contempt | Shares plans and improvements | Lists preventable failures |
| Klethi | Quick, sly, under-the-breath | Mischievous, dark | Gives secrets or quiet help | Withdraws, then strikes verbally |

## Approval Reaction Tiers

Every companion should eventually have four scripted reaction tiers. Not every tier needs a full dialogue scene; small world messages, campfire lines, and report callouts are enough until a personal quest is active.

| Companion | Minor Approval | Major Approval | Warning | Breaking Point |
| --- | --- | --- | --- | --- |
| Borcha | Safe route, food, low losses | Trusting his warning saves lives | Heavy losses or ignored scouts | Prideful disaster blamed on scouts |
| Marnid | Profit with order | Stabilizing trade or rejecting dirty money | Village theft or failed contracts | Ruining livelihoods for short-term gain |
| Ymira | Free captive, help village | Defy Slavers at real cost | Slave trade or execution | Treating helpless people as inventory |
| Rolf | Public honor | Recognition by noble powers | Humiliation or shabby conduct | Denying his claimed dignity publicly |
| Baheshtur | Fast victory | Free, bold action against a stronger foe | Timid command or wasteful losses | Submission to a humiliating power |
| Firentis | Mercy with discipline | Atonement through protection | Cruelty or endless war | Making him complicit in atrocity |
| Deshavi | Food and caution | Saving poor villages through scouting | Hunger or wasted lives | Sacrificing the forgotten for prestige |
| Matheld | Standing firm | Winning a hard direct fight | Retreat without necessity | Cowardice that endangers reputation |
| Alayen | Honorable conduct | Keeping oath under pressure | Dishonorable bargain | Betrayal of sworn obligation |
| Bunduk | Protect soldiers | Refuse cruel officer logic | Heavy losses or abuse of villagers | Spending common soldiers for vanity |
| Katrin | Pay and supplies | Save camp through hard logistics | Hunger or unpaid troops | Heroic waste that ruins the company |
| Jeremus | Heal or spare | Choose peace when war is easy | Needless violence | Becoming a machine for suffering |
| Nizar | Daring success | Impossible victory | Dull caution or retreat | Refusing every chance at greatness |
| Lezalit | Training and order | Defeat IEF with discipline | Weak command or disorder | Command collapse through sentiment |
| Artimenner | Preparation | Siege success through planning | Improvising into avoidable losses | Ignoring expertise until people die |
| Klethi | Clever ambush | Trusting stealth over spectacle | Hunger or rigid plans | Trapping or betraying her autonomy |

## Quest Outcome Index

Personal quests should not all resolve into the same reward. Each companion needs at least three meaningful outcomes: trust, compromise, and rupture. A darker or exploitative path can exist when it fits the companion.

| Companion | Trust Outcome | Compromise Outcome | Rupture Outcome | Mechanical Direction |
| --- | --- | --- | --- | --- |
| Borcha | Road conscience and loyal Scout | Guarded but reliable tracker | Scout bonus disabled until repaired | Ambush warning, map movement |
| Marnid | Clean trade network | Profitable but uneasy contacts | Quartermaster trust damaged | Trade, wages, market reports |
| Ymira | Permanent loyalty through mercy | Wary acceptance of hard necessity | Warning after cruelty | Surgeon recovery, captive mercy |
| Rolf | Earned dignity | Title preserved but questioned | Public humiliation wound | Envoy prestige, morale |
| Baheshtur | Chosen loyalty without submission | Mutual respect at a distance | Leaves before being leashed | Cavalry speed, pursuit |
| Firentis | Service becomes atonement | Duty without peace | Refuses further cruelty | Discipline, honor reactions |
| Deshavi | Protects the forgotten | Survival first, hope second | Withdraws from trust | Detection, village warnings |
| Matheld | Courage tempered by judgment | Strength without introspection | Rejects cautious command | Hard battle morale |
| Alayen | Honor becomes responsibility | Noble pride softened | Break over dishonor | Envoy, formation discipline |
| Bunduk | Soldiers' advocate in command | Practical but suspicious | Condemns officer cruelty | Casualty shock, wages |
| Katrin | Camp mother fully trusted | Keeps accounts, keeps distance | Quartermaster bonus falters | Food, pay, recovery |
| Jeremus | Compassion under pressure | Heals despite doubts | Moral warning escalates | Surgery, peace diplomacy |
| Nizar | Glory with responsibility | Charming risk remains dangerous | Scorns small command | Morale after hard victories |
| Lezalit | Discipline without cruelty | Cold but stable doctrine | Formal warning | Training, Captain role |
| Artimenner | Expertise respected and humanized | Effective but abrasive | Engineer refuses extra effort | Siege preparation |
| Klethi | Chooses belonging freely | Useful but unowned | Vanishes behind distrust | Spymaster, stealth options |

## Cross-Companion Triangles

These triangles should drive banter, campfire disputes, and quest pressure. A triangle is stronger than a simple pair because the player can triangulate values instead of merely picking a favorite.

| Triangle | Core Tension | Use Cases |
| --- | --- | --- |
| Borcha, Rolf, Deshavi | Road truth vs noble performance vs poor survival | Scouting disputes, noble escorts, village ambushes |
| Borcha, Marnid, Klethi | Practical travel vs trade order vs opportunistic stealth | Black Khergit routes, caravan deals, underworld jobs |
| Ymira, Lezalit, Bunduk | Mercy vs discipline vs soldier welfare | Captives, punishment, training, post-battle choices |
| Firentis, Jeremus, Matheld | Atonement vs healing vs courage | Retreats, triage, whether a fight is necessary |
| Alayen, Nizar, Rolf | Duty vs glory vs claimed status | Noble courts, public honors, duel or tournament content |
| Katrin, Artimenner, Baheshtur | Logistics vs planning vs freedom of movement | Long campaigns, sieges, supply shortages |
| Deshavi, Klethi, Katrin | Hunger, theft, and practical care | Camp shortages, desperate villages, stealth resupply |
| Ymira, Marnid, Firentis | Mercy, money, and moral debt | Ransom choices, Slaver markets, prisoner policy |

## Expansion Roadmap

1. **Prototype foundation:** Ymira and Lezalit already define the mercy and discipline poles.
2. **Road and underworld layer:** Borcha, Marnid, Deshavi, and Klethi should deepen scouting, Black Khergit pressure, Slaver market reactions, and camp survival.
3. **Company conscience layer:** Firentis, Jeremus, Bunduk, and Katrin should make food, wages, mercy, and soldier welfare matter.
4. **Honor and command layer:** Rolf, Baheshtur, Matheld, Alayen, Nizar, and Artimenner should sharpen rank, glory, engineering, and battlefield identity.

## Implementation Checklist

- Add individual approval deltas in `sod_companion_apply_player_action`.
- Add one campfire thought per companion for steady, loyal, troubled, and near-breaking bands.
- Add one warning confrontation per companion before quitting logic.
- Add one personal quest stage slot path per companion.
- Add role-specific bonuses that degrade below steady approval.
- Add company report callouts for strongest loyalty and sharpest warning.
- Add static tests for every companion entry, role, and quest hook.
