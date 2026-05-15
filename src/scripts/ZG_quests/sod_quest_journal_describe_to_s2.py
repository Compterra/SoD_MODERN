from header_common import *
from header_operations import *
from src.constants.module_constants import *


def _append_line(text):
    return [
        (str_store_string, s68, text),
        (str_store_string_reg, s97, s2),
        (str_store_string, s2, "@{s97}{s68}^"),
    ]


def _append_heading(text):
    return _append_line(text) + _append_line("@------------------------------")


def _append_journal_entry(prefix, include_archive_day=False):
    lines = [
        (str_store_string, s69, "@    [{prefix}] "),
        (str_store_quest_name, s68, ":quest_no"),
        (str_store_string_reg, s97, s2),
        (str_store_string, s2, "@{s97}{s69}{s68}^"),
        (quest_get_slot, reg0, ":quest_no", slot_quest_sod_runtime_stage),
        (quest_get_slot, reg1, ":quest_no", slot_quest_sod_journal_chain_progress),
        (quest_get_slot, reg2, ":quest_no", slot_quest_sod_runtime_state),
    ]
    if include_archive_day:
        lines += [
            (quest_get_slot, reg3, ":quest_no", slot_quest_sod_journal_archive_day),
            (str_store_string, s68, "@        Stage {reg0} | Chain {reg1} | State {reg2} | Archived day {reg3}"),
            (str_store_string_reg, s97, s2),
            (str_store_string, s2, "@{s97}{s68}^"),
        ]
    else:
        lines += [
            (str_store_string, s68, "@        Stage {reg0} | Chain {reg1} | State {reg2}"),
            (str_store_string_reg, s97, s2),
            (str_store_string, s2, "@{s97}{s68}^"),
        ]
    return lines


def _append_journal_section(category, prefix, empty_message, include_archive_day=False):
    return [
        (assign, reg7, 0),
        (try_for_range, ":quest_no", all_quests_begin, all_quests_end),
            (quest_get_slot, ":journal_category", ":quest_no", slot_quest_sod_journal_category),
            (try_begin),
                (eq, ":journal_category", category),
                (assign, reg7, 1),
            ] + _append_journal_entry(prefix, include_archive_day) + [
            (try_end),
        (try_end),
        (try_begin),
            (eq, reg7, 0),
            (str_store_string, s68, empty_message),
            (str_store_string_reg, s97, s2),
            (str_store_string, s2, "@{s97}{s68}^"),
        (try_end),
    ]


def _append_companion_arc_entry(quest_id, companion_label, opening, field_test, resolved_good, resolved_hard):
    return [
        (quest_get_slot, ":companion_state", quest_id, slot_quest_current_state),
        (quest_get_slot, ":companion_stage", quest_id, slot_quest_sod_runtime_stage),
        (try_begin),
            (gt, ":companion_state", 0),
            (assign, reg7, 1),
            (str_store_quest_name, s68, quest_id),
            (try_begin),
                (eq, ":companion_stage", sod_companion_quest_trust_unlocked),
                (str_store_string, s69, opening),
            (else_try),
                (eq, ":companion_stage", sod_companion_quest_test_started),
                (str_store_string, s69, field_test),
            (else_try),
                (eq, ":companion_stage", sod_companion_quest_resolved_good),
                (str_store_string, s69, resolved_good),
            (else_try),
                (eq, ":companion_stage", sod_companion_quest_resolved_hard),
                (str_store_string, s69, resolved_hard),
            (else_try),
                (str_store_string, s69, "@Dormant: waiting for trust or a world trigger"),
            (try_end),
            (assign, reg0, ":companion_stage"),
            (assign, reg1, ":companion_state"),
            (str_store_string, s2, f"@{{s2}}    [COMPANION] {companion_label} - {{s68}}^        {{s69}} | Stage {{reg0}} | Runtime state {{reg1}}^"),
        (try_end),
    ]


def _append_companion_arc_section():
    companion_arcs = (
        ("qst_companion_borcha_road_keeps_own", "Borcha", "@Talk to Borcha: Borcha is ready to speak of old horde roads and why safe tracks still surprise him.", "@Go to the road test: a dangerous road, horde sign, or scouting choice is testing whether fear becomes protection.", "@Resolved well: Borcha remembers a road made safer instead of merely survived.", "@Hard outcome: Borcha records a useful road lesson that still smells of old danger."),
        ("qst_companion_marnid_honest_price", "Marnid", "@Talk to Marnid: he is ready to explain why honest profit matters more than clean arithmetic.", "@Go to a market contact, caravan, or bargain: trade is testing whether fairness survives pressure.", "@Resolved well: Marnid records profit made stable enough to trust.", "@Hard outcome: Marnid records a useful profit that no longer feels entirely honest."),
        ("qst_companion_ymira_mercy_under_arms", "Ymira", "@Talk to Ymira: she is ready to ask whether mercy can survive inside an army.", "@Go to the captive or refugee witness: mercy is testing whether it will be protected, rationed, or spent.", "@Resolved well: Ymira records mercy protected under command.", "@Hard outcome: Ymira records the hard road and the names it cost."),
        ("qst_companion_rolf_name_worth_wearing", "Rolf", "@Talk to Rolf: he is ready to speak of the name he wears and the witnesses it needs.", "@Go to a public witness: a challenge is testing whether the name will be earned or defended as theater.", "@Resolved well: Rolf records dignity earned before witnesses.", "@Hard outcome: Rolf records the grand claim preserved at the cost of belief."),
        ("qst_companion_baheshtur_unbroken_saddle", "Baheshtur", "@Talk to Baheshtur: he is ready to speak of loyalty that must be chosen, not bridled.", "@Find a Black Khergit rider witness, then run Baheshtur's rider-oath trial from camp before judging the beaten riders.", "@Resolved well: Baheshtur records loyalty chosen freely.", "@Hard outcome: Baheshtur records peace kept by reins he can still feel."),
        ("qst_companion_firentis_debt_restitution", "Firentis", "@Talk to Firentis: he is ready to name the debt his sword still carries.", "@Go to the restitution village or battle witness: service is testing whether it becomes repair or another wound.", "@Resolved well: Firentis records service turned toward restitution.", "@Hard outcome: Firentis records a useful victory that left the debt heavier."),
        ("qst_companion_deshavi_tracks_through_ash", "Deshavi", "@Talk to Deshavi: she is ready to speak for the people tracks usually leave unnamed.", "@Go to the survivor, hunter, or trail focus: the company is testing whether it hunts or shelters.", "@Resolved well: Deshavi records survivors hidden before the trail went cold.", "@Hard outcome: Deshavi records a hunt won while some names stayed missing."),
        ("qst_companion_matheld_no_backward_step", "Matheld", "@Talk to Matheld: she is ready to explain why backward steps taste like shame.", "@Ask a ranker what the line learned after battle, then run Matheld's shield-line test from camp before judging the lesson.", "@Resolved well: Matheld records courage kept sharp and disciplined.", "@Hard outcome: Matheld records blood spent for a point she still questions."),
        ("qst_companion_alayen_standard_self", "Alayen", "@Talk to Alayen: he is ready to weigh honor against the self that wants to be seen.", "@Go to a lord, elder, or public witness: duty is testing what the standard serves.", "@Resolved well: Alayen records duty placed before display.", "@Hard outcome: Alayen records prestige won while duty stood aside."),
        ("qst_companion_bunduk_men_hold_line", "Bunduk", "@Talk to Bunduk: he is ready to name the men behind his anger.", "@Go to the rank-and-file witness: wages, casualties, or officer cruelty are testing whether command remembers the line.", "@Resolved well: Bunduk records soldiers defended by command instead of spent by it.", "@Hard outcome: Bunduk records order kept at a cost the ranks will remember."),
        ("qst_companion_katrin_last_coin", "Katrin", "@Talk to Katrin: she is ready to explain why the last coin in camp is never theoretical.", "@Go to the accounts or camp witness, then run Katrin's supply watch before spending the last coin.", "@Resolved well: Katrin records the camp fed before speeches were made.", "@Hard outcome: Katrin records waste paid for by people who did not give the speech."),
        ("qst_companion_jeremus_hands_triage", "Jeremus", "@Talk to Jeremus: he is ready to admit what war is doing to his hands.", "@Go to the wounded or triage witness: healing is testing whether it remains a duty.", "@Resolved well: Jeremus records healing protected even under battlefield pressure.", "@Hard outcome: Jeremus records lives saved by choices that still wounded the healer."),
        ("qst_companion_nizar_impossible_charge", "Nizar", "@Talk to Nizar: he is ready to speak of why impossible moments call to him.", "@Mark the charge in a field setup, then run Nizar's charge-lane test from camp before choosing the legend.", "@Resolved well: Nizar records a charge dramatic enough to remember and careful enough to survive.", "@Hard outcome: Nizar records a legend brightened by blood it did not need."),
        ("qst_companion_lezalit_discipline_without_chains", "Lezalit", "@Talk to Lezalit: he is ready to discuss order, fear, and Imperial doctrine.", "@Go to the drill or troop witness: captured Imperial discipline is testing whether strength requires cruelty.", "@Resolved well: Lezalit records order strengthened without chains.", "@Hard outcome: Lezalit records fear as useful and costly."),
        ("qst_companion_artimenner_siege_that_should", "Artimenner", "@Talk to Artimenner: he is ready to describe the failed design that still follows him.", "@Go to the siege works or construction witness: engineering pressure is testing whether plans are respected before blame begins.", "@Resolved well: Artimenner records a design trusted before disaster.", "@Hard outcome: Artimenner records blame shifted while the structure remained unforgiven."),
        ("qst_companion_klethi_knife_with_name", "Klethi", "@Talk to Klethi: she is ready to admit that some old jobs still know her name.", "@Go to the tavern contact or old-job witness: travel to the named focus town, ask the tavernkeeper, and follow Klethi's old mark into the alley before deciding what the secret buys.", "@Resolved well: Klethi records a choice kept in her own hands.", "@Hard outcome: Klethi records leverage bought at the price of distance."),
    )
    lines = [
        (assign, reg7, 0),
    ]
    for quest_id, companion_label, opening, field_test, resolved_good, resolved_hard in companion_arcs:
        lines += _append_companion_arc_entry(quest_id, companion_label, opening, field_test, resolved_good, resolved_hard)
    lines += [
        (try_begin),
            (eq, reg7, 0),
            (str_store_string, s68, "@    No companion personal arcs have entered the quest framework yet."),
            (str_store_string_reg, s97, s2),
            (str_store_string, s2, "@{s97}{s68}^"),
        (try_end),
    ]
    return lines


script_sod_quest_journal_describe_to_s2 = [
    (call_script, "script_sod_quest_journal_update"),
    (str_clear, s2),
]

script_sod_quest_journal_describe_to_s2 += _append_line("@Quest Journal")
script_sod_quest_journal_describe_to_s2 += _append_line("@A live summary of active quests, companion arcs, priority markers, stage progress, chain progress, and archived reports.")
script_sod_quest_journal_describe_to_s2 += _append_line("@Legend: [PINNED] priority target | [MAIN] main line | [SIDE] optional work | [URGENT] time-sensitive | [COMPANION] personal arc")
script_sod_quest_journal_describe_to_s2 += _append_line("@")
script_sod_quest_journal_describe_to_s2 += _append_line("@Summary:")
script_sod_quest_journal_describe_to_s2 += [
    (assign, reg0, "$sod_quest_journal_active_count"),
    (assign, reg1, "$sod_quest_journal_pinned_count"),
    (assign, reg2, "$sod_quest_journal_main_count"),
    (assign, reg3, "$sod_quest_journal_side_count"),
    (assign, reg4, "$sod_quest_journal_urgent_count"),
    (assign, reg5, "$sod_quest_journal_completed_count"),
    (assign, reg6, "$sod_quest_journal_failed_count"),
    (assign, reg9, "$sod_quest_journal_expiring_count"),
    (assign, reg10, "$sod_quest_journal_capacity"),
]
script_sod_quest_journal_describe_to_s2 += _append_line("@Tracked quests: {reg0}/{reg10} | Pinned: {reg1} | Main: {reg2} | Side: {reg3} | Urgent: {reg4} | Expiring: {reg9} | Completed: {reg5} | Failed: {reg6}")
script_sod_quest_journal_describe_to_s2 += _append_line("@")

script_sod_quest_journal_describe_to_s2 += _append_heading("@Companion Personal Arcs")
script_sod_quest_journal_describe_to_s2 += _append_line("@These entries are fed by companion approval, campfire choices, world incidents, memory records, and quest-framework aftermath.")
script_sod_quest_journal_describe_to_s2 += _append_companion_arc_section()
script_sod_quest_journal_describe_to_s2 += _append_line("@")

script_sod_quest_journal_describe_to_s2 += _append_heading("@Active Quests")
script_sod_quest_journal_describe_to_s2 += _append_journal_section(
    sod_quest_journal_category_active,
    "ACTIVE",
    "@    No active quests are currently tracked in the journal.",
)
script_sod_quest_journal_describe_to_s2 += _append_line("@")

script_sod_quest_journal_describe_to_s2 += _append_heading("@Completed Archive")
script_sod_quest_journal_describe_to_s2 += _append_journal_section(
    sod_quest_journal_category_completed,
    "DONE",
    "@    No completed quests have been archived yet.",
    include_archive_day=True,
)
script_sod_quest_journal_describe_to_s2 += _append_line("@")

script_sod_quest_journal_describe_to_s2 += _append_heading("@Failed Archive")
script_sod_quest_journal_describe_to_s2 += _append_journal_section(
    sod_quest_journal_category_failed,
    "FAILED",
    "@    No failed quests have been archived yet.",
    include_archive_day=True,
)
script_sod_quest_journal_describe_to_s2 += _append_line("@")
script_sod_quest_journal_describe_to_s2 += _append_line("@End of journal.")

script_sod_quest_journal_describe_to_s2 = script_sod_quest_journal_describe_to_s2
SCRIPT = script_sod_quest_journal_describe_to_s2
SCRIPTS = [("sod_quest_journal_describe_to_s2", script_sod_quest_journal_describe_to_s2)]
