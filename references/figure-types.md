# Figure Types

## System Architecture

Use when the reader needs to understand modules, boundaries, data flow, component interaction, or runtime responsibility.

Quality cues:

- Group major subsystems clearly.
- Show boundaries and interaction paths, not procedural chronology.
- Avoid turning architecture into a step-by-step flowchart.

## Technical Roadmap

Use when the reader needs to understand research stages, method progression, experiment path, stage outputs, or validation sequence.

Quality cues:

- Keep progression directional and stage-based.
- Limit stage count to a readable set.
- Make outputs visible at major stage ends.

## Workflow / Process

Use when the reader needs to understand ordered steps, branching, loops, triggers, fallback paths, or decisions.

Quality cues:

- Make branching explicit.
- Label ambiguous decisions.
- Keep loops readable with routed back-edges.

## Granularity Rule

Ask: is this figure explaining structure, progression, or execution?

- Structure: use architecture.
- Progression: use roadmap.
- Execution: use workflow.

Split the figure if it tries to explain all three at once.
