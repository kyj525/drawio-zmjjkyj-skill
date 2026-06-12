#!/usr/bin/env python3
"""Generate a diagrams.net/draw.io XML file from a small JSON spec."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


STYLE_PRESETS = {
    "title": "text;html=1;align=center;verticalAlign=middle;fontFamily=SimHei;fontSize=30;fontColor=#172033;fontStyle=1;",
    "text": "text;html=1;align=left;verticalAlign=middle;fontFamily=SimHei;fontSize=16;fontColor=#374151;fontStyle=0;",
    "panel": "rounded=1;arcSize=7;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#dbe1ea;strokeWidth=1;shadow=0;",
    "io": "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#e8eef6;strokeColor=#aebbd0;strokeWidth=1.2;fontColor=#1d2b3a;fontFamily=SimHei;fontSize=18;fontStyle=1;spacing=8;shadow=1;",
    "process": "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#e5eefb;strokeColor=#a9bedc;strokeWidth=1.2;fontColor=#17355f;fontFamily=SimHei;fontSize=16;fontStyle=1;spacing=8;shadow=1;",
    "conv": "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#e5eefb;strokeColor=#a9bedc;strokeWidth=1.2;fontColor=#17355f;fontFamily=SimHei;fontSize=16;fontStyle=1;spacing=8;shadow=1;",
    "residual": "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#e9e9ea;strokeColor=#b8b8ba;strokeWidth=1.2;fontColor=#2d2d2d;fontFamily=SimHei;fontSize=17;fontStyle=1;spacing=8;shadow=1;",
    "accent": "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#fce8da;strokeColor=#e7b996;strokeWidth=1.2;fontColor=#5b321d;fontFamily=SimHei;fontSize=17;fontStyle=1;spacing=8;shadow=1;",
    "success": "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#dff1e3;strokeColor=#9ccba6;strokeWidth=1.2;fontColor=#204c2a;fontFamily=SimHei;fontSize=16;fontStyle=1;spacing=8;shadow=1;",
    "danger": "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#f7dcdc;strokeColor=#dca8a8;strokeWidth=1.2;fontColor=#642525;fontFamily=SimHei;fontSize=16;fontStyle=1;spacing=8;shadow=1;",
    "add": "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#5f6b7a;strokeWidth=1.4;fontColor=#172033;fontFamily=SimHei;fontSize=28;fontStyle=1;shadow=1;",
    "flow_stage_1": "swimlane;startSize=32;fillColor=#EBF5FF;strokeColor=#2563EB;strokeWidth=2;fontSize=16;fontStyle=1;fontColor=#1e40af;rounded=0;collapsible=0;",
    "flow_stage_2": "swimlane;startSize=32;fillColor=#F0FDF4;strokeColor=#16a34a;strokeWidth=2;fontSize=16;fontStyle=1;fontColor=#047857;rounded=0;collapsible=0;",
    "flow_stage_3": "swimlane;startSize=32;fillColor=#FAF5FF;strokeColor=#7c3aed;strokeWidth=2;fontSize=16;fontStyle=1;fontColor=#6d28d9;rounded=0;collapsible=0;",
    "flow_stage_4": "swimlane;startSize=32;fillColor=#F0FDF4;strokeColor=#059669;strokeWidth=2;fontSize=16;fontStyle=1;fontColor=#047857;rounded=0;collapsible=0;",
    "flow_stage_5": "swimlane;startSize=32;fillColor=#FFF7ED;strokeColor=#ea580c;strokeWidth=2;fontSize=16;fontStyle=1;fontColor=#c2410c;rounded=0;collapsible=0;",
    "flow_node": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6c8ebf;fontColor=#172033;fontFamily=SimHei;fontSize=13;fontStyle=1;align=center;spacing=8;",
    "flow_note": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontColor=#555555;fontFamily=SimHei;fontSize=12;fontStyle=2;align=center;",
    "decision": "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#5f4a00;fontFamily=SimHei;fontSize=13;fontStyle=1;align=center;spacing=8;",
}

EDGE_PRESETS = {
    "arrow": "endArrow=block;html=1;rounded=0;strokeColor=#7a7a7a;strokeWidth=2;",
    "dashed": "endArrow=block;html=1;rounded=0;strokeColor=#7a7a7a;strokeWidth=2;dashed=1;",
    "skip": "endArrow=block;html=1;rounded=0;strokeColor=#3f8f55;strokeWidth=2.4;",
    "plain": "endArrow=none;html=1;rounded=0;strokeColor=#7a7a7a;strokeWidth=2;",
    "flow_main": "edgeStyle=orthogonalEdgeStyle;endArrow=block;html=1;rounded=0;strokeWidth=3;strokeColor=#2563EB;fontColor=#2563EB;fontSize=12;fontStyle=1;",
    "flow_internal": "edgeStyle=orthogonalEdgeStyle;endArrow=block;html=1;rounded=0;strokeWidth=2;strokeColor=#6c8ebf;",
    "flow_loop": "edgeStyle=orthogonalEdgeStyle;endArrow=block;html=1;rounded=0;dashed=1;strokeColor=#d97706;strokeWidth=2;fontColor=#d97706;fontSize=11;fontStyle=1;",
}


def label(value: Any) -> str:
    text = "" if value is None else str(value)
    return escape(text).replace("\n", "<br>")


def style_for(item: dict[str, Any], presets: dict[str, str]) -> str:
    if "style_raw" in item:
        return str(item["style_raw"])
    style_name = str(item.get("style", "process"))
    style = presets.get(style_name, presets["process"] if "process" in presets else "")
    overrides = item.get("style_overrides") or {}
    if overrides:
        if style and not style.endswith(";"):
            style += ";"
        style += "".join(f"{key}={value};" for key, value in overrides.items())
    return style


def add_geometry(parent: ET.Element, attrs: dict[str, Any]) -> ET.Element:
    geom = ET.SubElement(parent, "mxGeometry")
    for key, value in attrs.items():
        geom.set(key, str(value))
    geom.set("as", "geometry")
    return geom


def build(spec: dict[str, Any]) -> ET.ElementTree:
    page = spec.get("page") or {}
    width = int(page.get("width", 1500))
    height = int(page.get("height", 1050))
    diagram_name = str(spec.get("diagram_name", "Diagram"))

    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "24.0.0"})
    diagram = ET.SubElement(mxfile, "diagram", {"id": str(spec.get("diagram_id", "diagram-1")), "name": diagram_name})
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": str(page.get("dx", width)),
            "dy": str(page.get("dy", height)),
            "grid": "0",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": str(width),
            "pageHeight": str(height),
            "math": "0",
            "shadow": "0",
        },
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    for cell in spec.get("cells", []):
        cell_id = str(cell["id"])
        attrs = {
            "id": cell_id,
            "value": str(cell["value_raw"]) if "value_raw" in cell else label(cell.get("text", "")),
            "style": style_for(cell, STYLE_PRESETS),
            "vertex": "1",
            "parent": str(cell.get("parent", "1")),
        }
        if "connectable" in cell:
            attrs["connectable"] = "1" if cell["connectable"] else "0"
        mx = ET.SubElement(root, "mxCell", attrs)
        add_geometry(
            mx,
            {
                "x": cell.get("x", 0),
                "y": cell.get("y", 0),
                "width": cell.get("w", cell.get("width", 120)),
                "height": cell.get("h", cell.get("height", 60)),
            },
        )

    for edge in spec.get("edges", []):
        attrs = {
            "id": str(edge["id"]),
            "style": style_for(edge, EDGE_PRESETS),
            "edge": "1",
            "parent": str(edge.get("parent", "1")),
        }
        if edge.get("source"):
            attrs["source"] = str(edge["source"])
        if edge.get("target"):
            attrs["target"] = str(edge["target"])
        mx = ET.SubElement(root, "mxCell", attrs)
        geom = add_geometry(mx, {"relative": "1"})
        points = edge.get("points") or []
        if points:
            arr = ET.SubElement(geom, "Array", {"as": "points"})
            for point in points:
                ET.SubElement(arr, "mxPoint", {"x": str(point["x"]), "y": str(point["y"])})

    return ET.ElementTree(mxfile)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="JSON diagram spec")
    parser.add_argument("output", type=Path, help="Output .drawio path")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    tree = build(spec)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(args.output, encoding="utf-8", xml_declaration=True)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
