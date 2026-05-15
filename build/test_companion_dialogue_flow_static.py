# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected text: {needle}")


def assert_not_contains(raw: str, needle: str) -> None:
    if needle in raw:
        raise AssertionError(f"Unexpected stale wording: {needle}")


def assert_short_line(path: str, line: str, max_chars: int = 130) -> None:
    if len(line) > max_chars:
        raise AssertionError(f"{path} line is too wordy ({len(line)} chars): {line}")
    assert_contains(read(path), line)


def assert_approval_delta(path: str, troop_ref: str, delta: int) -> None:
    raw = read(path)
    expected = f'(call_script, "script_sod_companion_shift_approval", "{troop_ref}", {delta})'
    assert_contains(raw, expected)


def main() -> int:
    quitting_prompt = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting.py"
    quitting_yes = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_quitting_response.py"
    quitting_hear = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_quitting_response_02.py"
    quitting_firm = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_quitting_response_03.py"
    quitting_depart = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting_yes.py"
    quitting_stay = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting_no_confirmed.py"
    objection_ack = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_objection_response_02.py"
    objection_dismiss = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_objection_response_03.py"
    clash_respect = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_personalityclash_response_02.py"
    clash_hard = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_personalityclash_response_03.py"
    clash2_open = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_personalityclash2_response.py"
    clash2_hear = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_personalityclash2_response_02.py"
    clash2_steady = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_personalityclash2_response_03.py"
    match_response = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_personalitymatch_response.py"
    dialog_order = "src/dialogs/_order_dialogs.txt"
    quitting_intro_2 = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_quitting_2.py"
    ymira_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_ymira.py"
    jeremus_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_jeremus.py"
    bunduk_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_bunduk.py"
    katrin_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_katrin.py"
    nizar_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_nizar.py"
    rolf_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_rolf.py"
    marnid_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_marnid.py"
    lezalit_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_lezalit.py"
    alayen_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_alayen.py"
    artimenner_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_artimenner.py"
    baheshtur_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_baheshtur.py"
    borcha_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_borcha.py"
    deshavi_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_deshavi.py"
    firentis_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_firentis.py"
    klethi_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_klethi.py"
    matheld_depth = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_depth_matheld.py"
    home_2 = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_home_description_2.py"
    home_3 = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_home_description_3.py"
    home_hear = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_home_description.py"
    home_dismiss = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_home_description_03.py"
    rehire_refused = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_rehire_refused.py"
    rehire_yes = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_rehire.py"
    was_dismissed = "src/dialogs/ZE01_companions_and_named_npcs/anyone_companion_was_dismissed.py"
    recruit_full = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_recruit_signup_response.py"
    recruit_again = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_recruit_meet_again.py"
    recruit_second = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_recruit_secondchance.py"
    prompt_alayen = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_alayen.py"
    prompt_artimenner = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_artimenner.py"
    prompt_baheshtur = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_baheshtur.py"
    prompt_borcha = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_borcha.py"
    prompt_bunduk = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_bunduk.py"
    prompt_deshavi = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_deshavi.py"
    prompt_firentis = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_firentis.py"
    prompt_jeremus = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_jeremus.py"
    prompt_katrin = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_katrin.py"
    prompt_klethi = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_klethi.py"
    prompt_lezalit = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_lezalit.py"
    prompt_marnid = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_marnid.py"
    prompt_matheld = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_matheld.py"
    prompt_nizar = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_nizar.py"
    prompt_rolf = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_rolf.py"
    prompt_ymira = "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_depth_ymira.py"
    banter_01_04 = "src/dialogs/ZE01_companions_and_named_npcs/companions_banter_01_04.py"
    banter_05_08 = "src/dialogs/ZE01_companions_and_named_npcs/companions_banter_05_08.py"
    banter_09_12 = "src/dialogs/ZE01_companions_and_named_npcs/companions_banter_09_12.py"
    banter_13_16 = "src/dialogs/ZE01_companions_and_named_npcs/companions_banter_13_16.py"

    for path, line in (
        (quitting_prompt, "If you mean to send me away, say it cleanly. I can take a hard order; I will not be managed out by silence."),
        (quitting_yes, "Then go with my thanks. No bad blood between us."),
        (quitting_hear, "You have a place here. Tell me what made leaving look better."),
        (quitting_firm, "No. Stay, and we settle this now."),
        (quitting_depart, "Then I will take you at your word. No bitterness."),
        (quitting_stay, "Then I stay. Respect runs both ways."),
        (objection_ack, "You are heard. I will do better."),
        (objection_dismiss, "Noted. Back to your post."),
        (clash_respect, "You are right. I should have stepped in sooner. Tell me what mends this."),
        (clash_hard, "Drop it. Your temper is not command."),
        (clash2_open, "Then we deal with it in the open before it poisons the ranks."),
        (match_response, "Agreed. We can disagree and still keep the company whole."),
        (ymira_depth, "Ransom the able-bodied. Release the weakest."),
        (ymira_depth, "War cannot be clean, but a commander can put guards around mercy and mean it."),
        (ymira_depth, "riders who hunt freed people"),
        (ymira_depth, "captives are where command shows its real face"),
        (jeremus_depth, "You heard the wounded and saw the infirmary under pressure. Now choose the rule I follow when blood outruns clean cloth."),
        (jeremus_depth, "The wounded mend slowly, honestly, and never as cleanly as reports suggest."),
        (bunduk_depth, "Compromise. Fix what we can; the rest waits."),
        (bunduk_depth, "The line sees more than officers think: boots, food, pay, who gets buried, who gets blamed."),
        (katrin_depth, "Spend for speed. Rations can suffer later."),
        (katrin_depth, "No choice is cheap."),
        (katrin_depth, "I have seen brave companies fail because nobody wanted to count spoons."),
        (nizar_depth, "Spend blood for a legend."),
        (nizar_depth, "a costly mix of both"),
        (rolf_depth, "Strip the performance away in public."),
        (rolf_depth, "conduct can make a name heavier"),
        (marnid_depth, "Use the evidence. Make them pay us to stay quiet."),
        (marnid_depth, "The figures balance too neatly."),
        (marnid_depth, "it is a choice about who gets paid."),
        (lezalit_depth, "Use fear. Obedience first; understanding later."),
        (lezalit_depth, "A commander must separate poison from structure."),
        (alayen_depth, "Make the standard protect those beneath it."),
        (alayen_depth, "A standard is honored by what is done beneath it, not by polish."),
        (artimenner_depth, "If the works fail, you answer for it."),
        (artimenner_depth, "Ignored tolerances are a timetable."),
        (baheshtur_depth, "Force submission. Useful riders are useful."),
        (baheshtur_depth, "My trust in your hand on the reins"),
        (baheshtur_depth, "A hard ride can still be freely chosen."),
        (baheshtur_depth, "I am watching which riders you call free."),
        (borcha_depth, "Profit from the route before others learn it."),
        (borcha_depth, "The route runs from {s3} to {s4}"),
        (borcha_depth, "I am still watching the route you choose"),
        (deshavi_depth, "Hunt the pursuers. The vulnerable can keep moving."),
        (deshavi_depth, "I am watching whether your command learns that habit."),
        (firentis_depth, "Stay silent. The village needed swords, not confession."),
        (firentis_depth, "public witness"),
        (firentis_depth, "Conscience is not a comfort. It keeps watch."),
        (klethi_depth, "Use the secret as leverage."),
        (matheld_depth, "Make every insult cost blood."),
        (matheld_depth, "courage is not who dies loudest"),
        (home_2, "Home is a camp that speaks honestly, keeps the fire lit, and remembers names when shares are counted."),
        (home_3, "If this camp can be that, I will guard it. If not, I will serve, but I will not call it home."),
        (home_dismiss, "Homesickness does not change my orders."),
        (rehire_refused, "Then call me when you mean it. I was dismissed once; I will not wait on a half-open door."),
        (rehire_yes, "Welcome back. Take your place again."),
        (was_dismissed, "Then I go. Pride dented, not broken. If you want me back, ask directly."),
        (recruit_full, "I have no room now. If that changes, I will come back with a real offer."),
        (recruit_again, "What has changed since we last met?"),
        (recruit_second, "I spoke poorly before. Tell me again."),
        (prompt_alayen, "Alayen, what does the standard ask of us?"),
        (prompt_alayen, "Alayen, does my command still honor it?"),
        (prompt_artimenner, "Artimenner, show me the weak point."),
        (prompt_baheshtur, "Baheshtur, speak for the beaten riders."),
        (prompt_baheshtur, "Baheshtur, is this ride still freely chosen?"),
        (prompt_borcha, "Borcha, show me the road before it chooses us."),
        (prompt_bunduk, "Bunduk, bring me the line's grievance."),
        (prompt_deshavi, "Deshavi, show me the trail before it fades."),
        (prompt_firentis, "Firentis, what does restitution ask of us?"),
        (prompt_firentis, "Firentis, how does the company sit with you?"),
        (prompt_jeremus, "Jeremus, take me to the wounded."),
        (prompt_jeremus, "Jeremus, how are the wounded? And how are you?"),
        (prompt_katrin, "Katrin, show me the ledger."),
        (prompt_klethi, "Klethi, whose old work found your knife?"),
        (prompt_lezalit, "Lezalit, what do you see in my command?"),
        (prompt_marnid, "Marnid, show me the suspect contract."),
        (prompt_matheld, "Matheld, what did the line learn?"),
        (prompt_nizar, "Nizar, show me the charge before it becomes a song."),
        (prompt_rolf, "Rolf, answer the question of your name plainly."),
        (prompt_ymira, "Ymira, speak for the captives."),
        (prompt_ymira, "Ymira, how is this road wearing on you?"),
    ):
        assert_short_line(path, line)

    for path, phrase in (
        (banter_01_04, "Steel settles arguments faster than speeches; he seems determined"),
        (banter_01_04, "Rank is useful until trouble starts."),
        (banter_01_04, "For them, that is nearly peace."),
        (banter_01_04, "argue again after dawn."),
        (banter_01_04, "A quarrel settled early can still reach the next town with coin left."),
        (banter_01_04, "hard miles reward the stubborn"),
        (banter_01_04, "People say hard travel makes them honest."),
        (banter_05_08, "Baheshtur, leave a gate"),
        (banter_05_08, "We survive by thinking together"),
        (banter_05_08, "reasoned into agreement."),
        (banter_05_08, "travel turns mean."),
        (banter_05_08, "Baheshtur watches a trail"),
        (banter_05_08, "If the night stays calm"),
        (banter_05_08, "I do not mind hard miles."),
        (banter_05_08, "Quiet is still useful."),
        (banter_09_12, "watches the track for traps"),
        (banter_09_12, "Ledgers keep people honest"),
        (banter_09_12, "The march is cruel enough"),
        (banter_09_12, "people learn to look past your frown"),
        (banter_09_12, "If everyone is restless"),
        (banter_09_12, "A quiet hand does more useful work"),
        (banter_09_12, "We survive by knowing when to shut our mouths"),
        (banter_09_12, "If anyone wants more peace"),
        (banter_13_16, "the fire were his audience"),
        (banter_13_16, "everyone to hear danger before it arrives"),
        (banter_13_16, "old builder has a point"),
        (banter_13_16, "every listener ought to be politely impressed"),
        (banter_13_16, "shape of every watch"),
    ):
        assert_contains(read(path), phrase)

    stale_wording = "\n".join(
        read(path)
        for path in (
            quitting_prompt,
            quitting_yes,
            quitting_hear,
            quitting_firm,
            quitting_depart,
            quitting_stay,
            objection_ack,
            objection_dismiss,
            clash_respect,
            clash_hard,
            clash2_open,
            match_response,
            ymira_depth,
            jeremus_depth,
            bunduk_depth,
            katrin_depth,
            nizar_depth,
            rolf_depth,
            marnid_depth,
            lezalit_depth,
            alayen_depth,
            artimenner_depth,
            baheshtur_depth,
            borcha_depth,
            deshavi_depth,
            firentis_depth,
            klethi_depth,
            matheld_depth,
            home_2,
            home_3,
            home_hear,
            home_dismiss,
            rehire_refused,
            rehire_yes,
            was_dismissed,
            recruit_full,
            recruit_again,
            recruit_second,
            prompt_alayen,
            prompt_artimenner,
            prompt_baheshtur,
            prompt_borcha,
            prompt_bunduk,
            prompt_deshavi,
            prompt_firentis,
            prompt_jeremus,
            prompt_katrin,
            prompt_klethi,
            prompt_lezalit,
            prompt_marnid,
            prompt_matheld,
            prompt_nizar,
            prompt_rolf,
            prompt_ymira,
            banter_01_04,
            banter_05_08,
            banter_09_12,
            banter_13_16,
        )
    )
    for stale in (
        "I would rather a hard truth than a gentle lie",
        "A camp cannot stay strong if it forgets",
        "what is hurting you enough to make leaving feel easier",
        "pretending departure is the cure",
        "Hopefully it won't happen again",
        "Your objection is noted. Now fall back in line.",
        "If this is the hill you want to die on",
        "We are a company, not a feast hall",
        "tired and short-tempered",
        "Use the evidence for leverage",
        "Make a practical compromise",
        "Enforce command authority",
        "The camp can tighten belts later",
        "Take the dazzling charge before anyone can make it sensible",
        "Strip away the performance",
        "The Imperial method is poison",
        "Keep the oath publicly",
        "Improvise a leaner plan",
        "Broken riders are useful riders",
        "Use the route for profit before it becomes common knowledge",
        "The weak must keep moving on their own",
        "Say nothing more",
        "Use the old secret",
        "No one calls the company soft",
        "Home is not a roof",
        "I prefer my companions not to bother me",
        "You dismissed me once",
        "pride dented, not broken. If you want me back one day",
        "Welcome back, my friend",
        "Unfortunately, I cannot take on any more hands",
        "So... What have you been doing",
        "My apologies if I was rude",
        "tell me what the standard is asking",
        "weak point before it kills anyone",
        "before I answer them",
        "before someone else chooses it for us",
        "grievance plainly",
        "before it goes cold",
        "restitution still asks",
        "I will give the order myself",
        "put the ledger in my hands",
        "tell me whose old work",
        "speak plainly. What do you see",
        "walk me through the suspect contract",
        "tell me what the line learned",
        "show me this impossible charge",
        "answer the question about your name here",
        "before I decide their fate",
        "I want to know how this road is wearing",
        "At present, my trust in your honor",
        "how often pride will ask me to become a bucket",
        "before or after it becomes an epitaph",
        "As for my faith in this company",
        "A commander who cannot separate poison from structure",
        "At present, my confidence is {s2}",
        "Right now, my trust is {s2}",
        "Right now my trust in your command",
        "saddle hand",
        "honest taxmen",
        "grandeur is presently nursing",
        "become too sensible",
        "blood pretending to be both",
        "before the pot is empty",
        "company survives hard roads",
        "We part honestly, not as enemies",
        "Tell me the wound before you walk away",
        "anger chooses for us",
        "I will try not to repeat it",
        "Now fall back in line",
        "I should have spoken sooner",
        "Keep your temper and your place",
        "one mind to keep one road",
        "speaks plainly",
        "spoils are counted",
        "Your homesickness is not command business",
        "Ride with us again",
        "What has the road done with you",
        "Tell me your story again",
        "Beheshtur",
        "old smith has a point",
        "road turns mean",
        "road is cruel enough",
        "reasoned into the same camp",
        "People say the road makes them honest",
        "A camp survives by knowing when",
        "camp were his audience",
        "watches a road",
        "camp stays honest",
        "Rank is useful right up until",
        "road rewards the stubborn",
        "If the road stays calm",
        "I do not mind the road",
        "A quiet camp is still a camp",
        "If the camp wants more peace",
        "shape of every camp",
        "camp to hear the danger",
        "Then I will take you at your word. Farewell.",
        "Very well. I will stay.",
        "So be it. I leave",
        "Road says {s3} to {s4}",
        "road has two mouths",
        "road that tried to eat someone",
        "swallow another caravan",
        "until the road is clean",
        "their own road",
        "skin a road",
        "Roads feed people",
        "That road will still lie",
        "Profit is a road too",
        "I am still watching your road",
        "measuring rope against road",
        "saddle is road or rope",
        "which roads you call free",
        "horse finds a cliff",
        "calls the saddle free when steel is near",
        "A road chosen can be hard",
        "A road forced is a chain",
        "who chose the road",
        "Baheshtur, is this road still freely chosen?",
        "Slaver hunters",
        "quiet camp learns",
        "before it becomes smoke",
        "Hunt the pursuers. The weak move on alone.",
        "your camp learns that habit",
        "I am still watching your camp",
        "The figures balance too easily",
        "That is the smell",
        "clean ink hides its missing names",
        "Now the account is not numbers",
        "Use the evidence as leverage. Take the discount.",
        "made memory",
        "No romance left in it",
        "People get philosophical about shortages",
        "The brave version is expensive",
        "Spend for momentum. Belts tighten later.",
        "riders who follow freed names",
        "not a camp order from here",
        "before a ledger decides anything",
        "This is the part that matters after victory",
        "living voice",
        "campfire guilt",
        "Say nothing. The village needed swords, not confession.",
        "fine shield until",
        "more honest than another speech beside a sword",
        "Conscience is not a comfort, my friend",
    ):
        assert_not_contains(stale_wording, stale)

    assert_approval_delta(objection_ack, "$map_talk_troop", 1)
    assert_approval_delta(objection_dismiss, "$map_talk_troop", -2)
    assert_approval_delta(clash_respect, "$map_talk_troop", 3)
    assert_approval_delta(clash_hard, "$map_talk_troop", -2)
    assert_approval_delta(clash2_open, "$map_talk_troop", 2)
    assert_approval_delta(match_response, "$g_talk_troop", 2)
    for path in (
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_companion_personalityclash_response.py",
        clash_respect,
        clash_hard,
    ):
        raw = read(path)
        assert_contains(raw, '(assign, "$npc_with_personality_clash", 0)')
        assert_contains(raw, '(assign, "$npc_map_talk_context", 0)')
    for path in (clash2_open, clash2_hear, clash2_steady):
        raw = read(path)
        assert_contains(raw, '(troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, 1)')
        assert_contains(raw, '(assign, "$npc_with_personality_clash_2", 0)')
        assert_contains(raw, '(assign, "$npc_map_talk_context", 0)')
    match_raw = read(match_response)
    assert_contains(match_raw, '(troop_set_slot, "$g_talk_troop", slot_troop_personalitymatch_state, 1)')
    assert_contains(match_raw, '(assign, "$npc_with_personality_match", 0)')
    assert_contains(match_raw, '(assign, "$npc_map_talk_context", 0)')
    assert_not_contains(read(dialog_order), "ZA01_startup_and_dispatch/anyone_event_triggered_08.py")
    assert_contains(read(quitting_prompt), '[anyone, "companion_quitting", []')
    assert_contains(read(quitting_prompt), '"companion_quitting_2"')
    assert_contains(read(quitting_intro_2), '[anyone, "companion_quitting_2"')
    assert_contains(read(quitting_intro_2), '"companion_quitting_response"')
    assert_contains(read(rehire_refused), '[anyone, "companion_rehire_refused", []')
    assert_not_contains(read(rehire_refused), '[anyone, "companion_rehire", []')
    assert_approval_delta(ymira_depth, "trp_npc3", 4)
    assert_approval_delta(ymira_depth, "trp_npc3", -4)
    assert_approval_delta(jeremus_depth, "trp_npc12", 3)
    assert_approval_delta(jeremus_depth, "trp_npc12", -4)
    assert_approval_delta(bunduk_depth, "trp_npc10", 3)
    assert_approval_delta(bunduk_depth, "trp_npc10", -4)
    assert_approval_delta(katrin_depth, "trp_npc11", 3)
    assert_approval_delta(katrin_depth, "trp_npc11", -3)
    assert_approval_delta(nizar_depth, "trp_npc13", 2)
    assert_approval_delta(nizar_depth, "trp_npc13", -3)
    assert_approval_delta(rolf_depth, "trp_npc4", 2)
    assert_approval_delta(rolf_depth, "trp_npc4", -3)
    assert_approval_delta(marnid_depth, "trp_npc2", 3)
    assert_approval_delta(marnid_depth, "trp_npc2", -3)
    assert_approval_delta(lezalit_depth, "trp_npc14", 2)
    assert_approval_delta(alayen_depth, "trp_npc9", 3)
    assert_approval_delta(alayen_depth, "trp_npc9", -3)
    assert_approval_delta(artimenner_depth, "trp_npc15", 3)
    assert_approval_delta(artimenner_depth, "trp_npc15", -3)
    assert_approval_delta(baheshtur_depth, "trp_npc5", 3)
    assert_approval_delta(baheshtur_depth, "trp_npc5", -4)
    assert_approval_delta(borcha_depth, "trp_npc1", 3)
    assert_approval_delta(borcha_depth, "trp_npc1", -3)
    assert_approval_delta(deshavi_depth, "trp_npc7", 3)
    assert_approval_delta(deshavi_depth, "trp_npc7", -4)
    assert_approval_delta(firentis_depth, "trp_npc6", 3)
    assert_approval_delta(firentis_depth, "trp_npc6", -3)
    assert_approval_delta(klethi_depth, "trp_npc16", 3)
    assert_approval_delta(klethi_depth, "trp_npc16", -3)
    assert_approval_delta(matheld_depth, "trp_npc8", 3)
    assert_approval_delta(matheld_depth, "trp_npc8", -3)
    assert_approval_delta(home_hear, "$g_talk_troop", 1)
    assert_approval_delta(home_dismiss, "$g_talk_troop", -2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
