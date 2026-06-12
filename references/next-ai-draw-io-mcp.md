# next-ai-draw-io MCP

Use this reference when a `next-ai-draw-io` MCP server is installed or the user asks to connect directly to the web draw.io canvas.

## Detection

Use tool discovery first:

```text
tool_search query: next-ai-draw-io draw.io diagrams.net mcp canvas
```

If tools appear, prefer them over Browser UI automation and over the HTML bridge.

## Preferred MCP Workflow

1. Generate or update `.drawio` XML locally with the drawio skill scripts.
2. Validate it with `validate_drawio.py --strict-overlap`.
3. Use `next-ai-draw-io` MCP to load/import the XML into the live canvas.
4. Use MCP canvas operations to modify shapes, labels, geometry, connectors, colors, or grouping.
5. Use MCP screenshot/export/readback tools to verify the diagram.
6. Save/export the final `.drawio` and optional PNG/SVG.
7. Re-run local validation on the read-back XML when available.

## Expected Tool Capabilities

Exact tool names depend on the MCP server. Look for capabilities with these meanings:

- open or attach to a diagrams.net / draw.io page
- import or load `.drawio` XML
- get current XML / save XML
- add or update node geometry, label, style
- add or update edge geometry, label, style, waypoints
- select, group, align, distribute, resize, or delete cells
- export PNG/SVG/PDF/XML
- screenshot or inspect canvas bounds

## Fallbacks

- If MCP is installed but cannot attach to the current browser tab, open a new diagrams.net session through the MCP.
- If MCP can import but not save local files, export/read XML through MCP and write the returned XML locally.
- If no MCP tool is available in the current session, use `scripts/make_drawio_web_bridge.py` to create a browser-editable bridge HTML.
