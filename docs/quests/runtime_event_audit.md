# Runtime Event Audit

> Status: this document audits **seams** and documented hook surfaces. It does **not** claim that every seam is already wired into one unified dispatcher.

This audit records the quest-related event families that appear in the current documentation and source-backed runtime vocabulary.

## Scope note

- **audited seam**: a documented hook surface or runtime entry point that the quest framework can observe or connect to.
- **current implementation**: the event categories already supported by the audit vocabulary.
- **target-state**: any higher-level consolidation of these seams into a single dispatcher or orchestration layer.
- **build-time verification**: not the focus of this audit; see the build pipeline documentation for lowering and verification details.

## Support matrix

The matrix below separates audited hook surfaces from documented runtime seams and from target-state integration ideas.

| Event family | Audited seam | Current implementation evidence | Target-state integration | Status |
| --- | --- | --- | --- | --- |
| Battle | Battle-related quest hook surface | Battle events are called out in the audit vocabulary and treated as a supported seam | A future unified battle adapter could normalize more battle callbacks | audited seam |
| Mission | Mission-related quest hook surface | Mission events are part of the documented runtime seam set | A future orchestration layer could consolidate mission flow handling | audited seam |
| Dialogue | Dialogue-related quest hook surface | Dialogue events are part of the documented runtime seam set | A future dialogue bridge could normalize conversation-triggered quest reactions | audited seam |
| Hourly | Hourly tick seam | Hourly progression is documented as a runtime hook family | A future scheduler layer could group time-based hooks | audited seam |
| Daily | Daily tick seam | Daily progression is documented as a runtime hook family | A future scheduler layer could group time-based hooks | audited seam |
| Frame | Frame tick seam | Frame-level runtime observation is documented as a seam | A future runtime aggregator could collect frame-driven updates | audited seam |

## What this audit does and does not say

### It does say

- The quest framework recognizes battle, mission, dialogue, hourly, daily, and frame event families.
- These families are represented as **audited seams** in the documentation set.
- The runtime vocabulary is narrow enough to discuss hooks without inventing a larger event architecture.

### It does not say

- That every seam already routes through a single shared dispatcher.
- That all event families are exposed by one unified public API.
- That an additional event-bus layer is already implemented.

Those ideas remain **target-state** unless a source file or build artifact explicitly proves them.

## Current implementation vocabulary

Use the following terms when describing the current implementation:

- **audited seam**
- **runtime hook surface**
- **event family**
- **hook handling**
- **current implementation**

Use the following terms only for future or not yet implemented ideas:

- **target-state**
- **not yet implemented**
- **unified dispatcher**
- **single orchestration layer**

## Cross-reference

For the runtime terms that sit behind these seams, see:

- [`quest_runtime_api.md`](./quest_runtime_api.md)

For architecture and storage taxonomy, see:

- [`quest_framework_architecture.md`](./quest_framework_architecture.md)