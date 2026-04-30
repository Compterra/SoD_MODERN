# -*- coding: utf-8 -*-
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from src.quests.quest_domain import QuestNPCState, QuestOffer, quest_npc_state, validate_quest_id
from src.quests.quest_generation import (
    DynamicQuestTemplate,
    GeneratedQuestOffer,
    QuestGenerationContext,
    generate_dynamic_quest_offers,
    quest_generation_context_from_mapping,
)

__all__ = [
    "QuestGiverManager",
    "QuestGiverRuntime",
    "quest_giver_manager",
    "quest_giver_runtime",
]


def _coerce_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    return dict(value or {})


def _coerce_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return default
    return default


def _coerce_sequence(value: Any) -> tuple[Any, ...]:
    if value in (None, ""):
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(value)
    return (value,)


def _normalize_offer_id(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip().lower()
    return str(value).strip().lower()


def _template_identifier(template: Any) -> str:
    return str(
        getattr(template, "template_id", "")
        or getattr(template, "quest_id", "")
        or getattr(template, "id", "")
        or ""
    ).strip()


def _normalize_offer_template_id(offer: QuestOffer) -> str:
    if offer.template is not None:
        template_id = _template_identifier(offer.template)
        if template_id:
            return template_id
    return offer.effective_quest_id or offer.offer_id


def _normalize_recent_ids(values: Sequence[str] | Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for value in values:
        quest_id = validate_quest_id(str(value).strip().lower())
        if quest_id not in normalized:
            normalized.append(quest_id)
    return normalized


def _coerce_generation_context(
    context: QuestGenerationContext | Mapping[str, Any] | None,
    fallback: QuestGenerationContext | Mapping[str, Any] | None = None,
) -> QuestGenerationContext:
    if isinstance(context, QuestGenerationContext):
        return context.validate()
    if isinstance(fallback, QuestGenerationContext):
        if context is None:
            return fallback.validate()
    if isinstance(context, Mapping):
        return quest_generation_context_from_mapping(context)
    if isinstance(fallback, Mapping):
        return quest_generation_context_from_mapping(fallback)
    return quest_generation_context_from_mapping({})


def _merge_context_data(
    generation_context: QuestGenerationContext,
    *,
    npc_state: QuestNPCState,
    context: Mapping[str, Any] | QuestGenerationContext | None = None,
    world_context: QuestGenerationContext | Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
    event_type: str = "quest_giver",
    quest_id: str = "",
) -> dict[str, Any]:
    context_data = generation_context.to_mapping()

    if isinstance(world_context, QuestGenerationContext):
        context_data.update(world_context.to_mapping())
    elif isinstance(world_context, Mapping):
        context_data.update(dict(world_context))

    if isinstance(context, QuestGenerationContext):
        context_data.update(context.to_mapping())
    elif isinstance(context, Mapping):
        context_data.update(dict(context))

    context_data.update(_coerce_mapping(metadata))
    context_data["world_context"] = generation_context.to_world_context()
    context_data["npc_id"] = npc_state.npc_id
    context_data["giver_id"] = npc_state.npc_id
    context_data["npc_state"] = npc_state.to_snapshot()
    context_data["npc_state_snapshot"] = npc_state.to_snapshot()
    context_data["personality"] = npc_state.personality
    context_data["faction_personality"] = npc_state.personality
    context_data["faction_alignment"] = npc_state.faction_alignment
    context_data["dialogue_state"] = npc_state.dialogue_state
    context_data["dialogue_mode"] = npc_state.resolved_dialogue_mode(
        event_type or npc_state.state,
        quest_id,
        context=context_data,
    )
    context_data["available_quests"] = tuple(npc_state.available_quests)
    context_data["completed_quests"] = tuple(npc_state.completed_quests)
    context_data["failed_quests"] = tuple(npc_state.failed_quests)
    context_data["locked_chains"] = tuple(npc_state.locked_chains)
    context_data["cooldowns"] = dict(npc_state.cooldowns)
    context_data["relationship_thresholds"] = dict(npc_state.relationship_thresholds)
    context_data["player_reputation"] = dict(npc_state.player_reputation)
    context_data["special_flags"] = dict(npc_state.special_flags)
    context_data["story_arc_progression"] = dict(npc_state.story_arc_progression)
    return context_data


def _find_offer(
    offers: Sequence[GeneratedQuestOffer],
    offer: str | QuestOffer | GeneratedQuestOffer,
) -> GeneratedQuestOffer | None:
    if isinstance(offer, GeneratedQuestOffer):
        return offer
    if isinstance(offer, QuestOffer):
        target_offer_id = _normalize_offer_id(offer.offer_id)
        target_quest_id = _normalize_offer_id(offer.effective_quest_id)
        target_template_id = _normalize_offer_id(_normalize_offer_template_id(offer))
    else:
        target_offer_id = _normalize_offer_id(offer)
        target_quest_id = target_offer_id
        target_template_id = target_offer_id

    for candidate in offers:
        candidate_offer = candidate.offer
        candidate_offer_id = _normalize_offer_id(candidate_offer.offer_id)
        candidate_quest_id = _normalize_offer_id(candidate_offer.effective_quest_id)
        candidate_template_id = _normalize_offer_id(_normalize_offer_template_id(candidate_offer))
        if target_offer_id in {candidate_offer_id, candidate_quest_id, candidate_template_id}:
            return candidate
        if target_quest_id in {candidate_offer_id, candidate_quest_id, candidate_template_id}:
            return candidate
        if target_template_id in {candidate_offer_id, candidate_quest_id, candidate_template_id}:
            return candidate
    return None


def _record_history(
    history: list[dict[str, Any]],
    *,
    action: str,
    generated_offer: GeneratedQuestOffer,
    npc_state: QuestNPCState,
    context: Mapping[str, Any] | None = None,
) -> None:
    offer = generated_offer.offer
    template_id = _template_identifier(offer.template) if offer.template is not None else ""
    history.append(
        {
            "action": action,
            "npc_id": npc_state.npc_id,
            "offer_id": offer.offer_id,
            "quest_id": offer.effective_quest_id,
            "template_id": template_id,
            "weight": generated_offer.weight,
            "difficulty": generated_offer.difficulty,
            "reasons": list(generated_offer.reasons),
            "state": npc_state.state,
            "dialogue_state": npc_state.dialogue_state,
            "dialogue_mode": npc_state.dialogue_mode,
            "context": dict(context or {}),
        }
    )


@dataclass
class QuestGiverRuntime:
    npc_state: QuestNPCState
    templates: tuple[DynamicQuestTemplate | Mapping[str, Any], ...] = ()
    world_context: QuestGenerationContext | Mapping[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    default_limit: int = 3
    history_limit: int = 12
    current_offers: list[GeneratedQuestOffer] = field(default_factory=list)
    recent_offer_ids: list[str] = field(default_factory=list)
    recent_template_ids: list[str] = field(default_factory=list)
    offer_history: list[dict[str, Any]] = field(default_factory=list)
    last_context: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.npc_state.validate()
        self.templates = tuple(self.templates)
        self.metadata = _coerce_mapping(self.metadata)
        self.default_limit = max(0, _coerce_int(self.default_limit, 3))
        self.history_limit = max(1, _coerce_int(self.history_limit, 12))
        self.recent_offer_ids = _normalize_recent_ids(self.recent_offer_ids)
        self.recent_template_ids = _normalize_recent_ids(self.recent_template_ids)

    @property
    def npc_id(self) -> str:
        return self.npc_state.npc_id

    def validate(self) -> "QuestGiverRuntime":
        self.npc_state.validate()
        self.templates = tuple(self.templates)
        self.metadata = _coerce_mapping(self.metadata)
        self.default_limit = max(0, _coerce_int(self.default_limit, 3))
        self.history_limit = max(1, _coerce_int(self.history_limit, 12))
        self.recent_offer_ids = _normalize_recent_ids(self.recent_offer_ids)
        self.recent_template_ids = _normalize_recent_ids(self.recent_template_ids)
        for generated_offer in self.current_offers:
            generated_offer.offer.validate()
        return self

    def bind_world_context(
        self,
        world_context: QuestGenerationContext | Mapping[str, Any] | None,
    ) -> "QuestGiverRuntime":
        self.world_context = world_context
        return self

    def bind_templates(
        self,
        templates: Sequence[DynamicQuestTemplate | Mapping[str, Any]],
    ) -> "QuestGiverRuntime":
        self.templates = tuple(templates)
        return self

    def bind_npc_state(self, npc_state: QuestNPCState) -> "QuestGiverRuntime":
        npc_state.validate()
        self.npc_state = npc_state
        return self

    def _generation_context(
        self,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
    ) -> QuestGenerationContext:
        return _coerce_generation_context(context, self.world_context)

    def _context_data(
        self,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        *,
        event_type: str = "quest_giver",
        quest_id: str = "",
    ) -> dict[str, Any]:
        generation_context = self._generation_context(context)
        context_data = _merge_context_data(
            generation_context,
            npc_state=self.npc_state,
            context=context,
            world_context=self.world_context,
            metadata=self.metadata,
            event_type=event_type,
            quest_id=quest_id,
        )
        self.last_context = dict(context_data)
        return context_data

    def _history_offer_ids(self) -> list[str]:
        merged: list[str] = []
        seen: set[str] = set()
        for value in (*self.recent_template_ids, *self.recent_offer_ids):
            normalized = _normalize_offer_id(value)
            if normalized and normalized not in seen:
                seen.add(normalized)
                merged.append(normalized)
        return merged

    def _trim_history(self) -> None:
        if len(self.recent_template_ids) > self.history_limit:
            self.recent_template_ids = self.recent_template_ids[-self.history_limit :]
        if len(self.recent_offer_ids) > self.history_limit:
            self.recent_offer_ids = self.recent_offer_ids[-self.history_limit :]
        if len(self.offer_history) > self.history_limit:
            self.offer_history = self.offer_history[-self.history_limit :]

    def _record_recent_offer(self, generated_offer: GeneratedQuestOffer, *, action: str, context: Mapping[str, Any] | None = None) -> None:
        offer = generated_offer.offer
        offer_id = _normalize_offer_id(offer.offer_id)
        template_id = _normalize_offer_template_id(offer)
        if offer_id:
            self.recent_offer_ids.append(offer_id)
        if template_id:
            self.recent_template_ids.append(template_id)
        _record_history(
            self.offer_history,
            action=action,
            generated_offer=generated_offer,
            npc_state=self.npc_state,
            context=context,
        )
        self._trim_history()

    def refresh_offers(
        self,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        *,
        limit: int | None = None,
        templates: Sequence[DynamicQuestTemplate | Mapping[str, Any]] | None = None,
        recent_offer_ids: Sequence[str] = (),
    ) -> list[GeneratedQuestOffer]:
        active_templates = tuple(templates if templates is not None else self.templates)
        generation_context = self._generation_context(context)
        context_data = self._context_data(context, event_type="refresh")
        context_data["allow_unlisted_offer"] = True

        recent_ids = _coerce_sequence(recent_offer_ids)
        combined_recent_ids = self._history_offer_ids()
        for value in recent_ids:
            normalized = _normalize_offer_id(value)
            if normalized and normalized not in combined_recent_ids:
                combined_recent_ids.append(normalized)

        generated_offers = generate_dynamic_quest_offers(
            active_templates,
            generation_context,
            npc_state=self.npc_state,
            limit=limit if limit is not None else self.default_limit,
            recent_offer_ids=tuple(combined_recent_ids),
        )

        visible_offers: list[GeneratedQuestOffer] = []
        visible_quest_ids: list[str] = []
        for generated_offer in generated_offers:
            offer = generated_offer.offer
            offer_context = offer.offer_context(context_data)
            offer_context["allow_unlisted_offer"] = True
            if not offer.can_be_offered_by(self.npc_state, context=offer_context):
                continue
            visible_offers.append(generated_offer)
            quest_id = offer.effective_quest_id
            if quest_id and quest_id not in visible_quest_ids:
                visible_quest_ids.append(quest_id)

        self.current_offers = visible_offers
        self.npc_state.available_quests = visible_quest_ids
        if visible_offers and self.npc_state.state in {"idle", "available"}:
            self.npc_state.state = "available"
        elif not visible_offers and self.npc_state.state == "available":
            self.npc_state.state = "idle"
        return visible_offers

    def available_offers(self) -> list[GeneratedQuestOffer]:
        return list(self.current_offers)

    def get_offer(
        self,
        offer: str | QuestOffer | GeneratedQuestOffer,
    ) -> GeneratedQuestOffer | None:
        return _find_offer(self.current_offers, offer)

    def present_offer(
        self,
        offer: str | QuestOffer | GeneratedQuestOffer,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        dialogue_state: str | None = None,
    ) -> QuestOffer:
        generated_offer = self.get_offer(offer) if not isinstance(offer, GeneratedQuestOffer) else offer
        if generated_offer is None:
            raise KeyError(f"Quest offer {offer!r} is not currently available for NPC {self.npc_id!r}.")
        offer_context = self._context_data(context, event_type="offer", quest_id=generated_offer.offer.effective_quest_id)
        offer_context["allow_unlisted_offer"] = True
        quest_offer = generated_offer.offer
        quest_offer.apply_offer_to_npc(
            self.npc_state,
            context=offer_context,
            dialogue_state=dialogue_state,
        )
        self._record_recent_offer(generated_offer, action="offer", context=offer_context)
        return quest_offer

    def accept_offer(
        self,
        offer: str | QuestOffer | GeneratedQuestOffer,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        dialogue_state: str | None = None,
    ) -> QuestNPCState:
        generated_offer = self.get_offer(offer) if not isinstance(offer, GeneratedQuestOffer) else offer
        if generated_offer is None:
            raise KeyError(f"Quest offer {offer!r} is not currently available for NPC {self.npc_id!r}.")
        offer_context = self._context_data(context, event_type="accept", quest_id=generated_offer.offer.effective_quest_id)
        offer_context["allow_unlisted_offer"] = True
        state = generated_offer.offer.apply_acceptance_to_npc(
            self.npc_state,
            context=offer_context,
            dialogue_state=dialogue_state,
        )
        quest_id = generated_offer.offer.effective_quest_id
        if quest_id:
            self.npc_state.mark_quest_unavailable(quest_id)
        self._record_recent_offer(generated_offer, action="accept", context=offer_context)
        return state

    def complete_offer(
        self,
        offer: str | QuestOffer | GeneratedQuestOffer,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        quest_id: str = "",
        cooldown_days: int | None = None,
        dialogue_mode: str = "",
    ) -> QuestNPCState:
        generated_offer = self.get_offer(offer) if not isinstance(offer, GeneratedQuestOffer) else offer
        if generated_offer is None:
            raise KeyError(f"Quest offer {offer!r} is not currently available for NPC {self.npc_id!r}.")
        active_quest_id = quest_id or generated_offer.offer.effective_quest_id
        offer_context = self._context_data(context, event_type="complete", quest_id=active_quest_id)
        offer_context["allow_unlisted_offer"] = True
        state = generated_offer.offer.apply_completion_to_npc(
            self.npc_state,
            context=offer_context,
            quest_id=active_quest_id,
            cooldown_days=cooldown_days,
            dialogue_mode=dialogue_mode,
        )
        self._record_recent_offer(generated_offer, action="complete", context=offer_context)
        self.refresh_offers(context=offer_context, templates=self.templates)
        return state

    def fail_offer(
        self,
        offer: str | QuestOffer | GeneratedQuestOffer,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        quest_id: str = "",
        cooldown_days: int | None = None,
        dialogue_mode: str = "",
    ) -> QuestNPCState:
        generated_offer = self.get_offer(offer) if not isinstance(offer, GeneratedQuestOffer) else offer
        if generated_offer is None:
            raise KeyError(f"Quest offer {offer!r} is not currently available for NPC {self.npc_id!r}.")
        active_quest_id = quest_id or generated_offer.offer.effective_quest_id
        offer_context = self._context_data(context, event_type="fail", quest_id=active_quest_id)
        offer_context["allow_unlisted_offer"] = True
        state = generated_offer.offer.apply_failure_to_npc(
            self.npc_state,
            context=offer_context,
            quest_id=active_quest_id,
            cooldown_days=cooldown_days,
            dialogue_mode=dialogue_mode,
        )
        self._record_recent_offer(generated_offer, action="fail", context=offer_context)
        self.refresh_offers(context=offer_context, templates=self.templates)
        return state

    def resolved_dialogue_mode(
        self,
        event_type: str,
        quest_id: str = "",
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        default: str = "",
    ) -> str:
        offer_context = self._context_data(context, event_type=event_type, quest_id=quest_id)
        return self.npc_state.resolved_dialogue_mode(
            event_type,
            quest_id,
            context=offer_context,
            default=default,
        )

    def dialogue_context(
        self,
        quest_id: str = "",
        *,
        event_type: str = "quest_giver",
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        offer_context = self._context_data(context, event_type=event_type, quest_id=quest_id)
        return self.npc_state.dialogue_context(
            quest_id,
            event_type=event_type,
            context=offer_context,
        )

    def tick_cooldowns(
        self,
        days: int = 1,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
    ) -> list[str]:
        expired = self.npc_state.tick_cooldowns(days)
        self.refresh_offers(context=context, templates=self.templates)
        return expired

    def snapshot(self) -> dict[str, Any]:
        return {
            "npc_state": self.npc_state.to_snapshot(),
            "templates": [
                template.to_snapshot() if hasattr(template, "to_snapshot") else _coerce_mapping(template)  # type: ignore[arg-type]
                for template in self.templates
            ],
            "world_context": (
                self.world_context.to_mapping()
                if isinstance(self.world_context, QuestGenerationContext)
                else dict(self.world_context)
                if isinstance(self.world_context, Mapping)
                else None
            ),
            "current_offers": [generated_offer.to_snapshot() for generated_offer in self.current_offers],
            "recent_offer_ids": list(self.recent_offer_ids),
            "recent_template_ids": list(self.recent_template_ids),
            "offer_history": list(self.offer_history),
            "metadata": dict(self.metadata),
            "last_context": dict(self.last_context),
        }

    def diagnostics(self) -> list[str]:
        issues: list[str] = []
        try:
            self.validate()
        except Exception as exc:  # pragma: no cover - defensive diagnostics
            issues.append(f"{self.npc_id}: {exc}")

        visible_context = dict(self.last_context)
        visible_context["allow_unlisted_offer"] = True
        for generated_offer in self.current_offers:
            offer = generated_offer.offer
            if not offer.can_be_offered_by(self.npc_state, context=visible_context):
                issues.append(
                    f"{self.npc_id}: offer {offer.offer_id!r} is stale for current NPC state"
                )
            quest_id = offer.effective_quest_id
            if quest_id and quest_id not in self.npc_state.available_quests:
                issues.append(
                    f"{self.npc_id}: offer {quest_id!r} is missing from available_quests"
                )
        return issues


@dataclass
class QuestGiverManager:
    templates: tuple[DynamicQuestTemplate | Mapping[str, Any], ...] = ()
    world_context: QuestGenerationContext | Mapping[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    default_limit: int = 3
    history_limit: int = 12
    npc_states: dict[str, QuestNPCState] = field(default_factory=dict)
    runtimes: dict[str, QuestGiverRuntime] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.templates = tuple(self.templates)
        self.metadata = _coerce_mapping(self.metadata)
        self.default_limit = max(0, _coerce_int(self.default_limit, 3))
        self.history_limit = max(1, _coerce_int(self.history_limit, 12))

        initial_states = list(self.npc_states.values())
        initial_runtimes = list(self.runtimes.values())
        self.npc_states = {}
        self.runtimes = {}

        for npc_state in initial_states:
            self.register_npc_state(npc_state)
        for runtime in initial_runtimes:
            self.register_runtime(runtime)

    def validate(self) -> "QuestGiverManager":
        self.metadata = _coerce_mapping(self.metadata)
        self.default_limit = max(0, _coerce_int(self.default_limit, 3))
        self.history_limit = max(1, _coerce_int(self.history_limit, 12))
        for npc_state in self.npc_states.values():
            npc_state.validate()
        for runtime in self.runtimes.values():
            runtime.validate()
        return self

    def load_or_create_npc_state(self, npc_id: str, **kwargs: Any) -> QuestNPCState:
        npc_id = validate_quest_id(npc_id)
        npc_state = self.npc_states.get(npc_id)
        if npc_state is None:
            npc_state = quest_npc_state(npc_id, **kwargs)
            self.npc_states[npc_id] = npc_state
            return npc_state

        for key, value in kwargs.items():
            if hasattr(npc_state, key):
                setattr(npc_state, key, value)
        npc_state.validate()
        return npc_state

    def register_runtime(self, runtime: QuestGiverRuntime) -> QuestGiverRuntime:
        runtime.validate()
        npc_id = runtime.npc_id
        self.npc_states[npc_id] = runtime.npc_state
        if not runtime.templates:
            runtime.templates = self.templates
        if runtime.world_context is None:
            runtime.world_context = self.world_context
        runtime.history_limit = max(runtime.history_limit, self.history_limit)
        self.runtimes[npc_id] = runtime
        return runtime

    def register_npc_state(self, npc_state: QuestNPCState) -> QuestGiverRuntime:
        npc_state.validate()
        npc_id = npc_state.npc_id
        self.npc_states[npc_id] = npc_state
        runtime = self.runtimes.get(npc_id)
        if runtime is None:
            runtime = QuestGiverRuntime(
                npc_state=npc_state,
                templates=self.templates,
                world_context=self.world_context,
                metadata=dict(self.metadata),
                default_limit=self.default_limit,
                history_limit=self.history_limit,
            )
            self.runtimes[npc_id] = runtime
            return runtime
        runtime.bind_npc_state(npc_state)
        if not runtime.templates:
            runtime.bind_templates(self.templates)
        if runtime.world_context is None:
            runtime.bind_world_context(self.world_context)
        runtime.metadata.update(self.metadata)
        runtime.history_limit = max(runtime.history_limit, self.history_limit)
        return runtime

    def get_runtime(
        self,
        npc_id: str,
        *,
        create: bool = True,
        npc_state: QuestNPCState | None = None,
        templates: Sequence[DynamicQuestTemplate | Mapping[str, Any]] | None = None,
        world_context: QuestGenerationContext | Mapping[str, Any] | None = None,
    ) -> QuestGiverRuntime:
        npc_id = validate_quest_id(npc_id)
        runtime = self.runtimes.get(npc_id)
        if runtime is not None:
            if npc_state is not None:
                runtime.bind_npc_state(npc_state)
                self.npc_states[npc_id] = npc_state
            if templates is not None:
                runtime.bind_templates(templates)
            if world_context is not None:
                runtime.bind_world_context(world_context)
            return runtime

        if not create:
            raise KeyError(f"Quest giver runtime {npc_id!r} does not exist")

        state = npc_state or self.npc_states.get(npc_id)
        if state is None:
            state = quest_npc_state(npc_id)
            self.npc_states[npc_id] = state

        runtime = QuestGiverRuntime(
            npc_state=state,
            templates=tuple(templates if templates is not None else self.templates),
            world_context=world_context if world_context is not None else self.world_context,
            metadata=dict(self.metadata),
            default_limit=self.default_limit,
            history_limit=self.history_limit,
        )
        self.runtimes[npc_id] = runtime
        return runtime

    def refresh_npc(
        self,
        npc_id: str,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        *,
        limit: int | None = None,
        templates: Sequence[DynamicQuestTemplate | Mapping[str, Any]] | None = None,
        recent_offer_ids: Sequence[str] = (),
    ) -> list[GeneratedQuestOffer]:
        runtime = self.get_runtime(npc_id, create=True, templates=templates, world_context=self.world_context)
        return runtime.refresh_offers(
            context,
            limit=limit if limit is not None else self.default_limit,
            templates=templates if templates is not None else runtime.templates or self.templates,
            recent_offer_ids=recent_offer_ids,
        )

    def refresh_all(
        self,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        *,
        limit: int | None = None,
    ) -> dict[str, list[GeneratedQuestOffer]]:
        results: dict[str, list[GeneratedQuestOffer]] = {}
        npc_ids = set(self.npc_states) | set(self.runtimes)
        for npc_id in sorted(npc_ids):
            results[npc_id] = self.refresh_npc(npc_id, context, limit=limit)
        return results

    def present_offer(
        self,
        npc_id: str,
        offer: str | QuestOffer | GeneratedQuestOffer,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        dialogue_state: str | None = None,
    ) -> QuestOffer:
        runtime = self.get_runtime(npc_id)
        return runtime.present_offer(offer, context=context, dialogue_state=dialogue_state)

    def accept_offer(
        self,
        npc_id: str,
        offer: str | QuestOffer | GeneratedQuestOffer,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        dialogue_state: str | None = None,
    ) -> QuestNPCState:
        runtime = self.get_runtime(npc_id)
        return runtime.accept_offer(offer, context=context, dialogue_state=dialogue_state)

    def complete_offer(
        self,
        npc_id: str,
        offer: str | QuestOffer | GeneratedQuestOffer,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        quest_id: str = "",
        cooldown_days: int | None = None,
        dialogue_mode: str = "",
    ) -> QuestNPCState:
        runtime = self.get_runtime(npc_id)
        return runtime.complete_offer(
            offer,
            context=context,
            quest_id=quest_id,
            cooldown_days=cooldown_days,
            dialogue_mode=dialogue_mode,
        )

    def fail_offer(
        self,
        npc_id: str,
        offer: str | QuestOffer | GeneratedQuestOffer,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        quest_id: str = "",
        cooldown_days: int | None = None,
        dialogue_mode: str = "",
    ) -> QuestNPCState:
        runtime = self.get_runtime(npc_id)
        return runtime.fail_offer(
            offer,
            context=context,
            quest_id=quest_id,
            cooldown_days=cooldown_days,
            dialogue_mode=dialogue_mode,
        )

    def tick_cooldowns(
        self,
        days: int = 1,
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
    ) -> dict[str, list[str]]:
        results: dict[str, list[str]] = {}
        for npc_id in sorted(set(self.npc_states) | set(self.runtimes)):
            runtime = self.get_runtime(npc_id)
            expired = runtime.tick_cooldowns(days, context=context)
            results[npc_id] = expired
        return results

    def resolved_dialogue_mode(
        self,
        npc_id: str,
        event_type: str,
        quest_id: str = "",
        *,
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
        default: str = "",
    ) -> str:
        runtime = self.get_runtime(npc_id)
        return runtime.resolved_dialogue_mode(
            event_type,
            quest_id,
            context=context,
            default=default,
        )

    def dialogue_context(
        self,
        npc_id: str,
        quest_id: str = "",
        *,
        event_type: str = "quest_giver",
        context: QuestGenerationContext | Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        runtime = self.get_runtime(npc_id)
        return runtime.dialogue_context(
            quest_id,
            event_type=event_type,
            context=context,
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "templates": [
                template.to_snapshot() if hasattr(template, "to_snapshot") else _coerce_mapping(template)  # type: ignore[arg-type]
                for template in self.templates
            ],
            "world_context": (
                self.world_context.to_mapping()
                if isinstance(self.world_context, QuestGenerationContext)
                else dict(self.world_context)
                if isinstance(self.world_context, Mapping)
                else None
            ),
            "metadata": dict(self.metadata),
            "default_limit": self.default_limit,
            "history_limit": self.history_limit,
            "npc_states": {npc_id: state.to_snapshot() for npc_id, state in self.npc_states.items()},
            "runtimes": {npc_id: runtime.snapshot() for npc_id, runtime in self.runtimes.items()},
        }

    def diagnostics(self) -> list[str]:
        issues: list[str] = []
        for npc_id, runtime in sorted(self.runtimes.items()):
            issues.extend(runtime.diagnostics())
            if runtime.npc_state.npc_id != npc_id:
                issues.append(
                    f"{npc_id}: runtime NPC id {runtime.npc_state.npc_id!r} does not match registry key"
                )
        return issues


def quest_giver_runtime(
    npc_id: str,
    *,
    npc_state: QuestNPCState | None = None,
    templates: Sequence[DynamicQuestTemplate | Mapping[str, Any]] = (),
    world_context: QuestGenerationContext | Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
    default_limit: int = 3,
    history_limit: int = 12,
) -> QuestGiverRuntime:
    if npc_state is None:
        npc_state = quest_npc_state(npc_id, metadata=metadata)
    else:
        npc_state.validate()
        if validate_quest_id(npc_id) != npc_state.npc_id:
            raise ValueError(
                f"Quest giver runtime npc_id {npc_id!r} does not match npc_state.npc_id {npc_state.npc_id!r}"
            )
    return QuestGiverRuntime(
        npc_state=npc_state,
        templates=tuple(templates),
        world_context=world_context,
        metadata=_coerce_mapping(metadata),
        default_limit=default_limit,
        history_limit=history_limit,
    )


def quest_giver_manager(
    *,
    templates: Sequence[DynamicQuestTemplate | Mapping[str, Any]] = (),
    world_context: QuestGenerationContext | Mapping[str, Any] | None = None,
    npc_states: Sequence[QuestNPCState] = (),
    metadata: Mapping[str, Any] | None = None,
    default_limit: int = 3,
    history_limit: int = 12,
) -> QuestGiverManager:
    manager = QuestGiverManager(
        templates=tuple(templates),
        world_context=world_context,
        metadata=_coerce_mapping(metadata),
        default_limit=default_limit,
        history_limit=history_limit,
    )
    for npc_state in npc_states:
        manager.register_npc_state(npc_state)
    return manager
