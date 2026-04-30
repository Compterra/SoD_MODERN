# -*- coding: utf-8 -*-
from __future__ import annotations

from src.quests.quest_generation import (
    DEFAULT_DYNAMIC_QUEST_TEMPLATES,
    QUEST_GENERATION_TYPES,
    QuestGenerationContext,
    generate_dynamic_quest_offers,
)


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
    offers = generate_dynamic_quest_offers(
        DEFAULT_DYNAMIC_QUEST_TEMPLATES,
        context,
        limit=5,
    )
    covered_types = {template.quest_type for template in DEFAULT_DYNAMIC_QUEST_TEMPLATES}
    missing_types = set(QUEST_GENERATION_TYPES) - covered_types
    if missing_types:
        raise AssertionError(f"Dynamic quest templates missing types: {sorted(missing_types)}")
    if not offers:
        raise AssertionError("Expected at least one generated quest offer")
    for generated in offers:
        snapshot = generated.to_snapshot()
        if not snapshot.get("offer_id"):
            raise AssertionError("Generated offer missing offer_id")
        if generated.weight <= 0:
            raise AssertionError("Generated offer should have positive weight")
    print(
        f"[quest_generation] OK: {len(DEFAULT_DYNAMIC_QUEST_TEMPLATES)} templates, "
        f"{len(offers)} generated offer(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
