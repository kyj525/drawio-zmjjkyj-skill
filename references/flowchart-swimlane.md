# Flowchart Swimlane Rules

Use these rules when the user asks for a flowchart, workflow, algorithm, process map, decision tree, review pipeline, or staged operational flow.

## Canvas

- For tall process charts, keep `pageWidth <= 800`; diagrams.net may auto-scale wide canvases and make text look tiny.
- Suggested sizes:
  - Simple: `600 x 1200`
  - Medium: `800 x 2800`
  - Complex: `800 x 3800`
- Set `dx` and `dy` close to the page size.

## Stage Containers

Use `swimlane` containers for stages:

```xml
<mxCell id="g1" parent="1" connectable="0"
  style="swimlane;startSize=32;fillColor=#EBF5FF;strokeColor=#2563EB;strokeWidth=2;fontSize=16;fontStyle=1;fontColor=#1e40af;rounded=0;collapsible=0;"
  value="① Stage Name" vertex="1">
  <mxGeometry x="20" y="60" width="720" height="200" as="geometry"/>
</mxCell>
```

Rules:

- `connectable="0"` belongs on the cell tag.
- `rounded=0;collapsible=0` belongs in the style.
- Put child nodes inside the stage with `parent="g1"`.

## Text

- Stage title: `fontSize=14-16`, bold.
- Node title/body: prefer centered text; use short labels.
- Use HTML labels only when useful, e.g. `&lt;b style=&quot;font-size:13px&quot;&gt;Title&lt;/b&gt;&lt;br&gt;&lt;br&gt;Body`.

## Connectors

- Main inter-stage flow: orthogonal, `strokeWidth=3`, blue `#2563EB`.
- Internal flow: orthogonal, `strokeWidth=2`, color matching the stage.
- Fan-out: use explicit `entryX` / `exitX` anchors.
- Return/loop arrows: dashed orange `#d97706`, routed through left-margin waypoints to avoid crossing content.

## Palette

Use this stage palette:

| Stage | fillColor | strokeColor | fontColor |
|---|---|---|---|
| 1 | `#EBF5FF` | `#2563EB` | `#1e40af` |
| 2 | `#F0FDF4` | `#16a34a` | `#047857` |
| 3 | `#FAF5FF` | `#7c3aed` | `#6d28d9` |
| 4 | `#F0FDF4` | `#059669` | `#047857` |
| 5 | `#FFF7ED` | `#ea580c` | `#c2410c` |

Node fill should usually be white with the parent stage border color. Use yellow rhombus for decisions.

## Patterns

- Use a centered `或` label between two parallel options.
- Use small gray italic note bars for status annotations.
- Never leave diagonal or crossing connectors when an orthogonal route is possible.
