# Castle Mercenary Guild Hall Playtest Checklist

## Purpose

Use this checklist to verify that castle Mercenary Guild Halls feel useful without turning castles into infinite mercenary printers. The hall should be a local contract office: ordinary mercenaries without a pact, limited pact troops with a pact, and modest AI support only when lords are actually resting at a suitable castle.

## Setup Cases

- [ ] Build a Mercenary Guild Hall in a player-owned castle with no active guild pact.
- [ ] Build a Mercenary Guild Hall in a player-owned castle with an active guild pact.
- [ ] Give an AI kingdom a castle with a Mercenary Guild Hall and a guild pact.
- [ ] Give an AI kingdom a castle with a Mercenary Guild Hall and no pact.
- [ ] Create or load a save where a castle changes owner after stock has already been generated.
- [ ] Create or load a save where the player changes guild pact after stock has already been generated.

## Player Hiring

- [ ] Enter a no-pact castle hall and confirm the text says it is an independent/local office.
- [ ] Confirm no-pact stock uses ordinary mercenaries such as Watchmen, Caravan Guards, Mercenary Crossbowmen, Mercenary Swordsmen, or low-count Horsemen.
- [ ] Confirm Hired Blades do not appear as default stock.
- [ ] Hire one troop and confirm player gold decreases by normal join cost plus hall premium.
- [ ] Hire five troops and confirm stock decreases by five.
- [ ] Confirm the five-troop option disappears when fewer than five remain.
- [ ] Leave and re-enter the castle on the same day and confirm stock does not refill.
- [ ] Wait until the weekly refresh window and confirm stock can refresh.

## Pact Behavior

- [ ] Enter a pact-backed castle hall and confirm the text names the pact guild.
- [ ] Confirm pact-backed stock draws from that guild's roster.
- [ ] Hire pact troops and confirm guild manpower decreases.
- [ ] Confirm guild manpower never goes below zero.
- [ ] Create guild debt for the player and confirm player pact stock is blocked or unavailable.
- [ ] Clear the debt and confirm stock can appear again after refresh.
- [ ] End or change the pact and confirm the castle refreshes into the new pact or vanilla fallback instead of preserving stale enemy pact stock.

## Upgrade Behavior

- [ ] In a no-pact castle hall, confirm ordinary mercenary upgrades still work where vanilla mercenary rules allow them.
- [ ] In a pact castle hall, confirm matching guild troop upgrades are allowed.
- [ ] Try to upgrade wrong-guild troops at a pact castle and confirm they are blocked.
- [ ] Confirm the hall does not bypass faith ascension, doctrine facilities, or elite faction locks.

## AI Behavior

- [ ] Let an AI lord rest at a same-faction castle with a Mercenary Guild Hall and local stock.
- [ ] Confirm the lord can receive a small number of local hall troops while reinforcing.
- [ ] Confirm the local castle stock decreases when the AI lord uses it.
- [ ] Confirm pact-backed AI hall reinforcement drains guild manpower.
- [ ] Confirm AI lords do not draw hall stock from enemy, neutral, besieged, or non-castle centers.
- [ ] Confirm older pact reinforcement respects guild supply/refusal states and does not fire when the guild is overextended.

## Reports

- [ ] Open the Mercenary Market report and confirm active castle halls are listed by kingdom.
- [ ] Open the guild ledger and confirm hall totals, player-held hall count, and local stock count appear.
- [ ] Open the fief report and confirm player-held castle guild hall stock appears.
- [ ] Confirm report wording stays factual and does not imply a scene NPC exists.

## Balance Notes

- [ ] Castle prosperity and security should make stock a little better or worse, not wildly swing availability.
- [ ] One castle hall should feel helpful but not enough to replace a full guild contract.
- [ ] Multiple pact-backed castle halls should improve guild supply modestly, not create infinite companies.
- [ ] Hiring from halls should remain more expensive than free recruitment.
- [ ] AI use should be visible over time but should not instantly refill every lord.

## Regression Checks

- [ ] Existing town mercenary guild menus still work.
- [ ] Existing external mercenary companies still spawn and renew correctly.
- [ ] Castle patrol orders are unaffected.
- [ ] Center construction reports show the Mercenary Guild Hall as castle-only.
- [ ] Old saves without hall slots load with empty inactive stock.
