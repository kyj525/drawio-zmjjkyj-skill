# Draw.io XML Patterns

## Minimal File

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="diagram-1" name="Page-1">
    <mxGraphModel page="1" pageWidth="1200" pageHeight="800">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        ...
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Cells

Vertex:

```xml
<mxCell id="node1" value="Label" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e5eefb;strokeColor=#a9bedc;fontColor=#17355f;fontFamily=SimHei;fontSize=16;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="80" y="100" width="260" height="64" as="geometry"/>
</mxCell>
```

Edge:

```xml
<mxCell id="edge1" style="endArrow=block;html=1;rounded=0;strokeColor=#7a7a7a;strokeWidth=2;" edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

Edge with waypoints:

```xml
<mxCell id="skip" style="endArrow=block;html=1;rounded=0;strokeColor=#3f8f55;strokeWidth=2.4;" edge="1" parent="1" source="in" target="add">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="560" y="200"/>
      <mxPoint x="560" y="500"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## Style Recipes

- Text title: `text;html=1;align=center;verticalAlign=middle;fontFamily=SimHei;fontSize=30;fontColor=#172033;fontStyle=1;`
- Panel: `rounded=1;arcSize=7;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#dbe1ea;strokeWidth=1;shadow=0;`
- Input/output: `rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#e8eef6;strokeColor=#aebbd0;strokeWidth=1.2;fontColor=#1d2b3a;fontFamily=SimHei;fontSize=18;fontStyle=1;spacing=8;shadow=1;`
- Process: `rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#e5eefb;strokeColor=#a9bedc;strokeWidth=1.2;fontColor=#17355f;fontFamily=SimHei;fontSize=16;fontStyle=1;spacing=8;shadow=1;`
- Warning/first layer: `rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#f7dcdc;strokeColor=#dca8a8;strokeWidth=1.2;fontColor=#642525;fontFamily=SimHei;fontSize=15;fontStyle=1;spacing=8;shadow=1;`
- Add node: `ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#5f6b7a;strokeWidth=1.4;fontColor=#172033;fontFamily=SimHei;fontSize=28;fontStyle=1;shadow=1;`

## Validation Heuristics

- Check XML parsing before opening in draw.io.
- Reject duplicate IDs and edge source/target IDs that do not exist.
- Scan for mojibake markers: `鐢`, `鍥`, `脳`, `鈯`, `�`.
- Treat rectangle overlaps as warnings unless the cell is a known container panel.
- Keep all text boxes inside page bounds. For figure legends, prefer two-column or two-row layouts instead of one crowded row.

## Browser/MCP Notes

- The safest automation path is generate `.drawio` XML locally, import/open it in diagrams.net, then visually inspect.
- Live canvas editing through Browser is possible only when the app exposes usable DOM controls or a configured draw.io MCP/bridge exists.
- If file-picker automation fails, save the file and give the user the path for `File -> Open From -> Device`.
