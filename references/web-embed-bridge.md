# Web Embed Bridge

diagrams.net supports an official embed mode for integrating the editor into a host page.

## Protocol

Use an iframe URL like:

```text
https://embed.diagrams.net/?embed=1&proto=json&spin=1&libraries=1&saveAndExit=1
```

With `proto=json`, the editor and host page exchange JSON messages via `postMessage`.

Basic sequence:

1. The editor sends `{event: "init"}`.
2. The host sends `{action: "load", xml: "<mxfile>...</mxfile>"}`.
3. The editor sends save/autosave events containing XML.
4. The host may request export:

```json
{"action": "export", "format": "png", "scale": 2, "border": 20, "background": "#ffffff"}
```

or:

```json
{"action": "export", "format": "xml"}
```

## Use The Script

```bash
python C:\Users\Administrator\.codex\skills\drawio\scripts\make_drawio_web_bridge.py input.drawio output.html
```

Open `output.html` in Browser or a normal browser. Edit the diagram in the embedded diagrams.net editor, then click:

- `下载 .drawio` to download the edited source.
- `导出 PNG` and then `下载 PNG` to download a PNG render.

## Limits

- Browser security prevents a local HTML page from silently writing back to the original local `.drawio` file.
- Downloads go through the browser download mechanism.
- For fully automatic read/write edits in an already-open canvas, use a draw.io MCP server or a browser automation tool that can access downloads and upload files.
