from header_dialogs import *
from header_operations import *
from module_troops import *

# Banter context:
# 0 = quiet camp / routine
# 1 = friction
# 2 = mutual respect
# 3 = de-escalation / settling down

DIALOGS = [
	[trp_npc9, "event_triggered", [
		(ge, "$g_companion_banter_context", 0),
		(eq, "$g_companion_banter_pair_a", trp_npc9),
		(eq, "$g_companion_banter_pair_b", trp_npc10),
	], "Bunduk gives Marnid a sideways look. A neat ledger does not stop an arrow, but I will admit it keeps a camp from losing track of its own troubles.", "close_window", []],
	[trp_npc10, "event_triggered", [
		(ge, "$g_companion_banter_context", 0),
		(eq, "$g_companion_banter_pair_a", trp_npc9),
		(eq, "$g_companion_banter_pair_b", trp_npc10),
	], "And your habit of scowling at every plan does not improve it, Bunduk. Still, a man who watches the track for traps is worth listening to when weather turns ugly.", "close_window", []],
	[trp_npc9, "event_triggered", [
		(ge, "$g_companion_banter_context", 0),
		(eq, "$g_companion_banter_pair_a", trp_npc10),
		(eq, "$g_companion_banter_pair_b", trp_npc9),
	], "He talks like every coin has a sermon attached to it. Fine. Ledgers keep people honest, and honesty is easier to trust than charm.", "close_window", []],
	[trp_npc10, "event_triggered", [
		(ge, "$g_companion_banter_context", 0),
		(eq, "$g_companion_banter_pair_a", trp_npc10),
		(eq, "$g_companion_banter_pair_b", trp_npc9),
	], "He listens like the world expects him to be wrong. That is one way to survive. I prefer counting supplies before the survival is tested.", "close_window", []],

	[trp_npc11, "event_triggered", [
		(ge, "$g_companion_banter_context", 0),
		(eq, "$g_companion_banter_pair_a", trp_npc11),
		(eq, "$g_companion_banter_pair_b", trp_npc12),
	], "Jeremus, stop treating every bruised arm like a philosophical puzzle and help me finish the bandages. The wounded heal faster when we stop admiring their misery.", "close_window", []],
	[trp_npc12, "event_triggered", [
		(ge, "$g_companion_banter_context", 0),
		(eq, "$g_companion_banter_pair_a", trp_npc11),
		(eq, "$g_companion_banter_pair_b", trp_npc12),
	], "And you complain like the whole camp should thank you for every stitch. Still, I would rather hear a blunt hand than miss a wound because someone was too proud to point it out.", "close_window", []],
	[trp_npc11, "event_triggered", [
		(ge, "$g_companion_banter_context", 0),
		(eq, "$g_companion_banter_pair_a", trp_npc12),
		(eq, "$g_companion_banter_pair_b", trp_npc11),
	], "She keeps the camp from falling apart and pretends it is only habit. That is either modesty or discipline. I have not decided which is more dangerous.", "close_window", []],
	[trp_npc12, "event_triggered", [
		(ge, "$g_companion_banter_context", 0),
		(eq, "$g_companion_banter_pair_a", trp_npc12),
		(eq, "$g_companion_banter_pair_b", trp_npc11),
	], "He can sound stern, but he notices the practical side of a problem before most people notice there is a problem at all. That is useful when the camp is already tired.", "close_window", []],

	[trp_npc9, "event_triggered", [
		(eq, "$g_companion_banter_context", 1),
		(eq, "$g_companion_banter_variant", 0),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc9),
		(eq, "$g_companion_banter_pair_b", trp_npc9),
	], "If we are delayed, I would rather it be by bad weather than by sloppy discipline. The march is cruel enough without us giving it help.", "close_window", []],
	[trp_npc10, "event_triggered", [
		(eq, "$g_companion_banter_context", 1),
		(eq, "$g_companion_banter_variant", 0),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc10),
		(eq, "$g_companion_banter_pair_b", trp_npc10),
	], "And I would rather people learn to look past your frown and into the actual supplies. Anger is cheaper than repairs, but repairs keep us moving.", "close_window", []],
	[trp_npc11, "event_triggered", [
		(eq, "$g_companion_banter_context", 1),
		(eq, "$g_companion_banter_variant", 1),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc11),
		(eq, "$g_companion_banter_pair_b", trp_npc11),
	], "If everyone is restless, then I am restless. We have enough injuries already without inviting more through pride and bad timing.", "close_window", []],
	[trp_npc12, "event_triggered", [
		(eq, "$g_companion_banter_context", 1),
		(eq, "$g_companion_banter_variant", 1),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc12),
		(eq, "$g_companion_banter_pair_b", trp_npc12),
	], "Then stop pacing and count the straps. A quiet hand does more useful work than a loud conscience ever will.", "close_window", []],

	[trp_npc9, "event_triggered", [
		(eq, "$g_companion_banter_context", 2),
		(eq, "$g_companion_banter_variant", 0),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc9),
		(eq, "$g_companion_banter_pair_b", trp_npc9),
	], "Marnid is more useful than his habits suggest. He worries about the little things before the little things become a grave problem.", "close_window", []],
	[trp_npc10, "event_triggered", [
		(eq, "$g_companion_banter_context", 2),
		(eq, "$g_companion_banter_variant", 0),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc10),
		(eq, "$g_companion_banter_pair_b", trp_npc10),
	], "Bunduk is more sensible than he wants anyone to know. That sort of caution looks like stubbornness until the first ambush proves it right.", "close_window", []],
	[trp_npc11, "event_triggered", [
		(eq, "$g_companion_banter_context", 2),
		(eq, "$g_companion_banter_variant", 2),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc11),
		(eq, "$g_companion_banter_pair_b", trp_npc11),
	], "If somebody has to keep the camp from slipping into nonsense, I am content for it to be me. It is less dramatic than heroics, but it leaves fewer scars.", "close_window", []],
	[trp_npc12, "event_triggered", [
		(eq, "$g_companion_banter_context", 2),
		(eq, "$g_companion_banter_variant", 2),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc12),
		(eq, "$g_companion_banter_pair_b", trp_npc12),
	], "He is blunt, but he is right more often than he pretends to be. I can work with that. The wounded care less about style than results.", "close_window", []],

	[trp_npc9, "event_triggered", [
		(eq, "$g_companion_banter_context", 3),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc9),
		(eq, "$g_companion_banter_pair_b", trp_npc9),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc10),
		(eq, "$g_companion_banter_pair_b", trp_npc10),
	], "Let it lie. We survive by knowing when to shut our mouths, tie down the tents, and save temper for the fight that matters.", "close_window", []],
	[trp_npc10, "event_triggered", [
		(eq, "$g_companion_banter_context", 3),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc10),
		(eq, "$g_companion_banter_pair_b", trp_npc10),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc9),
		(eq, "$g_companion_banter_pair_b", trp_npc9),
	], "Agreed. The argument has done enough work for one night. Now we keep the gear dry and let morning decide who was wise.", "close_window", []],
	[trp_npc11, "event_triggered", [
		(eq, "$g_companion_banter_context", 3),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc11),
		(eq, "$g_companion_banter_pair_b", trp_npc11),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc12),
		(eq, "$g_companion_banter_pair_b", trp_npc12),
	], "If the quarrel is over, then so am I. Put the pride away and let the watches do their work. That is enough peace for one evening.", "close_window", []],
	[trp_npc12, "event_triggered", [
		(eq, "$g_companion_banter_context", 3),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc12),
		(eq, "$g_companion_banter_pair_b", trp_npc12),
		(this_or_next|eq, "$g_companion_banter_pair_a", trp_npc11),
		(eq, "$g_companion_banter_pair_b", trp_npc11),
	], "Good. We have spent enough words for now. If anyone wants more peace, they can start by keeping complaints quiet until dawn.", "close_window", []],
]
