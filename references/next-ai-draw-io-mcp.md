# Next AI Draw.io MCP

Use this reference when the `next-ai-draw-io` / Next AI Draw.io MCP server is installed or the user asks to connect directly to the web draw.io canvas.

Project: `DayuanJiang/next-ai-draw-io`

MCP package:

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["@next-ai-drawio/mcp-server@latest"]
    }
  }
}
```

The package starts a stdio MCP server plus an embedded HTTP server. By default, the HTTP server uses port `6002` and the draw.io embed base URL is `https://embed.diagrams.net`.

## Detection

Use tool discovery first:

```text
tool_search query: next-ai-draw-io drawio diagrams.net mcp canvas start_session create_new_diagram
```

If tools appear, prefer them over Browser UI automation and over the HTML bridge.

## Preferred MCP Workflow

1. Generate or update `.drawio` XML locally with the drawio skill scripts.
2. Validate it with `validate_drawio.py --strict-overlap`.
3. Call `start_session` first. This opens a browser with real-time diagram preview.
4. Call `create_new_diagram` with the validated XML.
5. Use `edit_diagram` for ID-based update/add/delete operations when revising shapes, labels, geometry, connectors, colors, or grouping.
6. Use `get_diagram` to read back current XML.
7. Use `export_diagram` to save a `.drawio` file.
8. Save/export optional PNG/SVG if exposed by the current MCP version.
9. Re-run local validation on the read-back XML when available.

## Known Tool Names

The README documents these MCP tools:

- `start_session`: opens browser with real-time diagram preview.
- `create_new_diagram`: creates a new diagram from XML; requires an `xml` argument.
- `edit_diagram`: edits the diagram by ID-based operations such as update/add/delete cells.
- `get_diagram`: gets the current diagram XML.
- `export_diagram`: saves the diagram to a `.drawio` file.

## Configuration

Optional environment variables:

- `PORT`: default `6002`; if occupied, the server tries the next available port up to `6020`.
- `DRAWIO_BASE_URL`: default `https://embed.diagrams.net`; set to a self-hosted draw.io URL for private deployments.

Example with custom port:

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["@next-ai-drawio/mcp-server@latest"],
      "env": {"PORT": "6003"}
    }
  }
}
```

## Fallbacks

- If the MCP reports "No active session", call `start_session` first.
- If the browser is not updating, check that the browser URL contains a `?mcp=` session parameter.
- If MCP is installed but cannot attach to the current browser tab, open a new diagrams.net session through the MCP.
- If MCP can import but not save local files, export/read XML through MCP and write the returned XML locally.
- If no MCP tool is available in the current session, use `scripts/make_drawio_web_bridge.py` to create a browser-editable bridge HTML.
