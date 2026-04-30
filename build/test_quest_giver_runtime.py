# -*- coding: utf-8 -*-
from __future__ import annotations

from src.quests.quest_domain import quest_npc_state
from src.quests.quest_generation import DEFAULT_DYNAMIC_QUEST_TEMPLATES, QuestGenerationContext
from src.quests.quest_giver_runtime import quest_giver_manager


def main() -> int:
    context = QuestGenerationContext(
        faction_war_state=1,
        settlement_danger=4,
        economy_state=-2,
        player_relation=20,
        player_renown=450,
        party_size=95,
        nearby_threats=4,
        recent_battles=2,
        center_ownership=1,
        prisoner_state=1,
        trade_routes=2,
        regional_unrest=4,
        faction_id="fac_kingdom_1",
        center_id="p_town_1",
        region="heartlands",
    )
    npc_state = quest_npc_state(
        "npc_quest_giver_1",
        personality="honorable",
        faction_alignment="fac_kingdom_1",
    )
    manager = quest_giver_manager(
        templates=DEFAULT_DYNAMIC_QUEST_TEMPLATES,
        npc_states=[npc_state],
        metadata={"source": "runtime_test"},
    )
    offers = manager.refresh_npc("npc_quest_giver_1", context)
    if not offers:
        raise AssertionError("Expected at least one generated quest-giver offer")

    generated = offers[0]
    offer = generated.offer
    quest_id = offer.effective_quest_id
    if not offer.can_be_offered_by(npc_state, context=offer.offer_context(context.to_mapping())):
        raise AssertionError("Generated offer should be valid for the NPC state")

    presented = manager.present_offer("npc_quest_giver_1", generated, context=context)
    if presented.offer_id != offer.offer_id:
        raise AssertionError("Presented offer did not match the generated offer")
    if npc_state.state != "offered":
        raise AssertionError(f"Expected NPC state 'offered' after presentation, got {npc_state.state!r}")
    if npc_state.last_quest_id != quest_id:
        raise AssertionError("NPC last_quest_id was not updated on presentation")

    manager.accept_offer("npc_quest_giver_1", generated, context=context)
    if npc_state.state != "engaged":
        raise AssertionError(f"Expected NPC state 'engaged' after acceptance, got {npc_state.state!r}")

    manager.complete_offer(
        "npc_quest_giver_1",
        generated,
        context=context,
        cooldown_days=2,
    )
    if not npc_state.has_completed_quest(quest_id):
        raise AssertionError("NPC completion state was not recorded")
    if npc_state.cooldown_for(quest_id) != 2:
        raise AssertionError("Expected quest cooldown to be set after completion")

    expired = manager.tick_cooldowns(2, context=context)
    if quest_id not in expired["npc_quest_giver_1"]:
        raise AssertionError("Cooldown expiry was not reported")
    if npc_state.cooldown_for(quest_id) != 0:
        raise AssertionError("Cooldown should expire after ticking")

    diagnostics = manager.diagnostics()
    if diagnostics:
        raise AssertionError(f"Expected clean diagnostics, got: {diagnostics}")

    print(
        f"[quest_giver_runtime] OK: {len(offers)} offer(s), "
        f"quest {quest_id!r} completed and cooldown expired"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
