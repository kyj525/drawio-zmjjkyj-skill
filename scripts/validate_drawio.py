#!/usr/bin/env python3
"""Validate common diagrams.net/draw.io XML issues."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET


MOJIBAKE_RE = re.compile(r"[鐢鍥脳鈯�]")


def as_float(value: str | None, default: float = 0.0) -> float:
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default


def local_rect(cell: ET.Element) -> dict[str, float] | None:
    geom = cell.find("mxGeometry")
    if geom is None:
        return None
    if not all(key in geom.attrib for key in ("x", "y", "width", "height")):
        return None
    x = as_float(geom.get("x"))
    y = as_float(geom.get("y"))
    w = as_float(geom.get("width"))
    h = as_float(geom.get("height"))
    return {"x": x, "y": y, "w": w, "h": h, "r": x + w, "b": y + h}


def absolute_rect(
    cell: ET.Element,
    by_id: dict[str, ET.Element],
    cache: dict[str, dict[str, float] | None],
) -> dict[str, float] | None:
    cell_id = cell.get("id", "")
    if cell_id in cache:
        return cache[cell_id]

    r = local_rect(cell)
    if r is None:
        cache[cell_id] = None
        return None

    parent_id = cell.get("parent")
    if parent_id and parent_id not in ("0", "1") and parent_id in by_id:
        parent_rect = absolute_rect(by_id[parent_id], by_id, cache)
        if parent_rect is not None:
            r = {
                "x": r["x"] + parent_rect["x"],
                "y": r["y"] + parent_rect["y"],
                "w": r["w"],
                "h": r["h"],
                "r": r["x"] + parent_rect["x"] + r["w"],
                "b": r["y"] + parent_rect["y"] + r["h"],
            }
    cache[cell_id] = r
    return r


def overlaps(a: dict[str, float], b: dict[str, float]) -> bool:
    return a["x"] < b["r"] and a["r"] > b["x"] and a["y"] < b["b"] and a["b"] > b["y"]


def is_ancestor(ancestor_id: str, child: ET.Element, by_id: dict[str, ET.Element]) -> bool:
    current = child.get("parent")
    while current and current in by_id:
        if current == ancestor_id:
            return True
        current = by_id[current].get("parent")
    return False


def validate(path: Path, *, strict_overlap: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    if MOJIBAKE_RE.search(text):
        errors.append("possible mojibake/garbled text marker found")

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"XML parse error: {exc}"], warnings

    root = tree.getroot()
    graph_root = root.find(".//root")
    if graph_root is None:
        errors.append("missing mxGraphModel/root")
        return errors, warnings

    cells = list(graph_root.findall("mxCell"))
    by_id = {cell.get("id", ""): cell for cell in cells if cell.get("id")}
    ids = [cell.get("id") for cell in cells if cell.get("id")]
    seen: set[str] = set()
    for cell_id in ids:
        if cell_id in seen:
            errors.append(f"duplicate id: {cell_id}")
        seen.add(cell_id)

    id_set = set(ids)
    for cell in cells:
        if cell.get("edge") == "1":
            for attr in ("source", "target"):
                ref = cell.get(attr)
                if ref and ref not in id_set:
                    errors.append(f"edge {cell.get('id')} has missing {attr}: {ref}")

    model = root.find(".//mxGraphModel")
    page_w = as_float(model.get("pageWidth") if model is not None else None, 0)
    page_h = as_float(model.get("pageHeight") if model is not None else None, 0)

    container_keywords = ("panel", "legend", "container", "box")
    rect_cache: dict[str, dict[str, float] | None] = {}
    rects: list[tuple[str, dict[str, float], str, ET.Element]] = []
    for cell in cells:
        if cell.get("vertex") != "1":
            continue
        cell_id = cell.get("id", "")
        r = absolute_rect(cell, by_id, rect_cache)
        if r is None:
            continue
        style = cell.get("style", "")
        if page_w and r["r"] > page_w + 0.1:
            warnings.append(f"{cell_id} extends beyond page width")
        if page_h and r["b"] > page_h + 0.1:
            warnings.append(f"{cell_id} extends beyond page height")
        if any(word in cell_id.lower() for word in container_keywords):
            continue
        if "swimlane" in style or cell.get("connectable") == "0":
            continue
        if "fillColor=#ffffff;strokeColor=#dbe1ea" in style:
            continue
        rects.append((cell_id, r, style, cell))

    for i, (id_a, rect_a, _, cell_a) in enumerate(rects):
        for id_b, rect_b, _, cell_b in rects[i + 1 :]:
            if is_ancestor(id_a, cell_b, by_id) or is_ancestor(id_b, cell_a, by_id):
                continue
            if overlaps(rect_a, rect_b):
                msg = f"overlap: {id_a} / {id_b}"
                if strict_overlap:
                    errors.append(msg)
                else:
                    warnings.append(msg)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drawio", type=Path)
    parser.add_argument("--strict-overlap", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors, warnings = validate(args.drawio, strict_overlap=args.strict_overlap)
    result = {"file": str(args.drawio), "errors": errors, "warnings": warnings, "ok": not errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"file={args.drawio}")
        print(f"errors={len(errors)}")
        for item in errors:
            print(f"ERROR: {item}")
        print(f"warnings={len(warnings)}")
        for item in warnings:
            print(f"WARN: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
