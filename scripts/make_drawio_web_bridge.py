#!/usr/bin/env python3
"""Create a local HTML bridge that loads a .drawio file in diagrams.net embed mode."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path


HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    html, body {{
      margin: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
      color: #172033;
      background: #f6f8fb;
    }}
    .toolbar {{
      height: 48px;
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 0 14px;
      box-sizing: border-box;
      border-bottom: 1px solid #dbe1ea;
      background: #ffffff;
    }}
    .title {{
      font-weight: 700;
      margin-right: auto;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    button, a.button {{
      appearance: none;
      border: 1px solid #b9c2cf;
      background: #fff;
      color: #172033;
      border-radius: 6px;
      padding: 7px 10px;
      font-size: 13px;
      text-decoration: none;
      cursor: pointer;
    }}
    button.primary, a.primary {{
      border-color: #3f6fb5;
      background: #3f6fb5;
      color: #fff;
    }}
    #status {{
      font-size: 12px;
      color: #667085;
      min-width: 160px;
      text-align: right;
    }}
    iframe {{
      display: block;
      width: 100%;
      height: calc(100vh - 48px);
      border: 0;
      background: #fff;
    }}
  </style>
</head>
<body>
  <div class="toolbar">
    <div class="title">{title_html}</div>
    <button id="getXml">取回 XML</button>
    <button id="exportPng">导出 PNG</button>
    <a id="downloadDrawio" class="button primary" download="{download_name}" href="#">下载 .drawio</a>
    <a id="downloadPng" class="button" download="{png_name}" href="#" style="display:none">下载 PNG</a>
    <span id="status">正在连接 diagrams.net...</span>
  </div>
  <iframe id="drawio" src="https://embed.diagrams.net/?embed=1&proto=json&spin=1&libraries=1&saveAndExit=1"></iframe>
  <script>
    const initialXml = {xml_json};
    const frame = document.getElementById('drawio');
    const statusEl = document.getElementById('status');
    const drawioLink = document.getElementById('downloadDrawio');
    const pngLink = document.getElementById('downloadPng');
    let latestXml = initialXml;
    const targetOrigin = 'https://embed.diagrams.net';

    function setStatus(text) {{
      statusEl.textContent = text;
    }}

    function send(message) {{
      frame.contentWindow.postMessage(JSON.stringify(message), targetOrigin);
    }}

    function setDrawioDownload(xml) {{
      latestXml = xml || latestXml;
      const blob = new Blob([latestXml], {{ type: 'application/xml;charset=utf-8' }});
      const url = URL.createObjectURL(blob);
      if (drawioLink.href && drawioLink.href !== '#') URL.revokeObjectURL(drawioLink.href);
      drawioLink.href = url;
    }}

    function setPngDownload(dataUri) {{
      pngLink.href = dataUri;
      pngLink.style.display = 'inline-block';
    }}

    document.getElementById('getXml').addEventListener('click', () => {{
      setStatus('正在取回 XML...');
      send({{ action: 'export', format: 'xml' }});
    }});

    document.getElementById('exportPng').addEventListener('click', () => {{
      setStatus('正在导出 PNG...');
      send({{ action: 'export', format: 'png', scale: 2, border: 20, background: '#ffffff' }});
    }});

    drawioLink.addEventListener('click', () => {{
      if (!drawioLink.href || drawioLink.href === '#') setDrawioDownload(latestXml);
    }});

    window.addEventListener('message', (event) => {{
      if (event.origin !== targetOrigin) return;
      let msg = event.data;
      if (typeof msg === 'string') {{
        try {{ msg = JSON.parse(msg); }} catch (_) {{}}
      }}
      if (!msg || typeof msg !== 'object') return;

      if (msg.event === 'init') {{
        send({{
          action: 'load',
          xml: initialXml,
          title: {title_json},
          autosave: 1,
          saveAndExit: 1,
          noSaveBtn: 0,
          noExitBtn: 0,
          modified: 0
        }});
        setDrawioDownload(initialXml);
        setStatus('已连接，可编辑');
      }} else if (msg.event === 'load') {{
        setStatus('图已加载');
      }} else if (msg.event === 'autosave' || msg.event === 'save') {{
        if (msg.xml) setDrawioDownload(msg.xml);
        setStatus(msg.event === 'save' ? '已保存，可下载' : '已自动保存');
      }} else if (msg.event === 'export') {{
        if (msg.format === 'xml' && msg.xml) {{
          setDrawioDownload(msg.xml);
          setStatus('XML 已取回');
        }} else if ((msg.format === 'png' || msg.format === 'xmlpng') && msg.data) {{
          if (msg.xml) setDrawioDownload(msg.xml);
          setPngDownload(msg.data);
          setStatus('PNG 已生成');
        }} else {{
          setStatus('导出完成');
        }}
      }} else if (msg.event === 'exit') {{
        setStatus('编辑器已退出');
      }}
    }});
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drawio", type=Path, help="Input .drawio file")
    parser.add_argument("output", type=Path, help="Output bridge .html file")
    parser.add_argument("--title", help="Editor title")
    args = parser.parse_args()

    xml = args.drawio.read_text(encoding="utf-8")
    title = args.title or args.drawio.stem
    args.output.parent.mkdir(parents=True, exist_ok=True)
    html = HTML_TEMPLATE.format(
        title=escape(title),
        title_html=escape(title),
        title_json=json.dumps(title, ensure_ascii=False),
        xml_json=json.dumps(xml, ensure_ascii=False),
        download_name=args.drawio.name,
        png_name=args.drawio.with_suffix(".png").name,
    )
    args.output.write_text(html, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
