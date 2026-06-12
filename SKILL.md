---
name: drawio
description: Generate, edit, validate, beautify, export, and open diagrams.net/draw.io diagrams from natural language, existing .drawio XML, screenshots, or rough notes. Use when the user asks for draw.io, drawio, diagrams.net, editable diagram XML, architecture diagrams, academic figures, method pipelines, model structure figures, technical roadmaps, process diagrams, workflow diagrams, flowcharts, decision trees, PNG export, or direct browser/MCP drawing in draw.io.
---

# Drawio

Create polished, editable diagrams.net/draw.io figures. This skill merges three modes: local XML generation and validation, high-quality flowchart/swimlane layout, and publication-style academic diagrams with optional PNG export.

## Default Workflow

1. Identify the figure type: architecture, roadmap, workflow/flowchart, model structure, or paper schematic.
2. Clarify only when missing details affect labels, topology, or intended use. Otherwise infer a clean conservative layout.
3. Build the editable `.drawio` first:
   - Use `scripts/spec_to_drawio.py` for standard block diagrams, flowcharts, and staged workflows.
   - Hand-edit XML when exact layout, existing diagrams, or custom academic figures need finer control.
4. Save deliverables under the workspace `outputs/` directory unless the user gave another path.
5. Validate with `scripts/validate_drawio.py <file.drawio> --strict-overlap`; fix errors, garbled text, overlaps, bad references, and clipping.
6. Export PNG when the user asks, when publication output is expected, or when diagrams.net desktop is available:
   `powershell -ExecutionPolicy Bypass -File scripts/export_drawio_png.ps1 <file.drawio>`.
7. If the user asks to edit the browser canvas, discover draw.io/diagrams.net MCP tools first, especially `next-ai-draw-io`. If no MCP exists, generate a web bridge with `scripts/make_drawio_web_bridge.py <file.drawio> <bridge.html>` and open it in a browser.

## Design Profiles

- **Academic / thesis / paper figure**: read `references/academic-quality.md` and `references/figure-types.md`. Use light backgrounds, low-saturation colors, strong typography, orthogonal connectors, and spacious grid alignment. Default to `.drawio + PNG` when possible.
- **Flowchart / workflow / process map**: read `references/flowchart-swimlane.md`. Use swimlane containers for stages, centered node text, orthogonal connectors, blue 3px main arrows, stage palette, and left-margin routed loop arrows.
- **Custom XML / browser/MCP integration**: read `references/drawio-xml-patterns.md` for minimal XML skeletons, style recipes, waypoint edges, and troubleshooting. Read `references/next-ai-draw-io-mcp.md` when the user wants direct browser control or mentions `next-ai-draw-io`.

## Web draw.io Bridge

First choice for direct control is a draw.io MCP server such as `next-ai-draw-io`. Use `tool_search` for `next-ai-draw-io draw.io diagrams.net mcp` before falling back to the bridge. When that MCP is available, prefer MCP operations for direct canvas/file actions such as opening a diagram, creating/updating shapes, importing XML, exporting XML/PNG, screenshotting, and saving.

Use the bridge when no direct MCP tool is available and the user still wants to connect to the web version of draw.io / diagrams.net:

```bash
python C:\Users\Administrator\.codex\skills\drawio\scripts\make_drawio_web_bridge.py input.drawio output.html
```

Open `output.html` in a browser. It embeds `https://embed.diagrams.net` with `embed=1&proto=json`, loads the `.drawio` XML via `postMessage`, listens for Save/Autosave events, and provides download buttons for the edited `.drawio` and exported PNG.

Important limits:

- A normal webpage cannot silently overwrite local files. The bridge can download the updated `.drawio`; Codex must read the downloaded file or the user must import it back.
- If a draw.io MCP server exists, prefer MCP for direct canvas/file updates.
- If Browser automation is available, use it to open the bridge and visually verify the canvas.

## Spec Generator

Create a JSON spec, then run:

```bash
python C:\Users\Administrator\.codex\skills\drawio\scripts\spec_to_drawio.py spec.json output.drawio
python C:\Users\Administrator\.codex\skills\drawio\scripts\validate_drawio.py output.drawio --strict-overlap
```

Supported cell styles include:

- `title`, `text`, `panel`
- `io`, `process`, `conv`, `residual`, `accent`, `success`, `danger`, `add`
- `flow_stage_1` ... `flow_stage_5`, `flow_node`, `flow_note`, `decision`

Supported edge styles include:

- `arrow`, `dashed`, `skip`, `plain`
- `flow_main`, `flow_internal`, `flow_loop`

Example:

```json
{
  "diagram_name": "Flow",
  "page": {"width": 800, "height": 1200},
  "cells": [
    {"id": "g1", "style": "flow_stage_1", "text": "① 输入", "x": 20, "y": 60, "w": 720, "h": 180, "connectable": false},
    {"id": "n1", "parent": "g1", "style": "flow_node", "text": "收集需求", "x": 30, "y": 55, "w": 200, "h": 70},
    {"id": "n2", "parent": "g1", "style": "decision", "text": "是否完整？", "x": 270, "y": 55, "w": 150, "h": 80}
  ],
  "edges": [
    {"id": "e1", "parent": "g1", "style": "flow_internal", "source": "n1", "target": "n2"}
  ]
}
```

## Quality Gate

Do not call the diagram finished until:

- XML opens in diagrams.net.
- No duplicate IDs or missing edge references.
- No mojibake or fake characters in Chinese labels.
- Text is readable and not clipped; legends have enough spacing.
- Connectors do not cross labels or pass through boxes.
- Layout matches the intended figure type instead of mixing structure, progression, and execution in one overloaded view.
- When PNG export is requested, `.drawio` and `.png` both exist and correspond to the same final content.
