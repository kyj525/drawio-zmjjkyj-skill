# Academic Quality Rules

Use these rules for thesis, paper, report, architecture, method pipeline, roadmap, model structure, and experiment figures.

## Delivery

- Default to an editable `.drawio` file.
- Also export a matching PNG when a diagrams.net desktop executable is available or the user asks for image output.
- Keep the `.drawio` and `.png` filenames aligned.

## Style

- Prefer white or very light backgrounds.
- Use low-saturation accent colors and sparse semantic color.
- Use consistent line weight, corner radius, arrowhead style, and typography.
- Reduce heavy shadows, gradients, gloss, and decorative clutter.
- Use one dominant reading direction: top-to-bottom or left-to-right.

## Typography

- Keep node text short; prefer noun phrases.
- For publication figures, use very readable text. A `26px` target is appropriate for large academic canvases, but scale down consistently for smaller diagrams.
- Shorten wording and enlarge boxes before shrinking text.
- Titles and major section labels should be visibly larger than ordinary node text.

## Layout

- Keep siblings on a visible grid.
- Keep adjacent nodes separated by roughly 24-40 px at starter-canvas scale.
- Keep major layers/groups separated by roughly 40-80 px.
- Use labeled containers or background bands for related subsystems.
- Prefer a slightly spacious figure over a dense one.

## Connectors

- Use orthogonal routing by default.
- Do not route connectors through text or box interiors.
- Attach connectors to sensible side anchors.
- Use explicit waypoints when a line must turn around other content.
- Reduce crossings aggressively; move boxes before accepting tangled lines.

## Final Gate

Before final response:

- XML parses.
- No duplicate IDs.
- All edge references point to existing cells.
- No garbled Chinese / mojibake markers.
- No avoidable overlap, cramped legend, or page clipping.
- The figure remains understandable without oral explanation.
- The figure type matches its purpose: architecture for structure, roadmap for progression, workflow for execution.
