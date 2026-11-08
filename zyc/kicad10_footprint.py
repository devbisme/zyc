"""Adapt the KiCad 10 footprint constructs needed by the Zyc renderer."""

import re
from types import SimpleNamespace


_TOKEN_RE = re.compile(r'\s*(\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+)')


def _parse_sexpr(text):
    root = []
    stack = [root]
    for match in _TOKEN_RE.finditer(text):
        token = match.group(1)
        if token == "(":
            node = []
            stack[-1].append(node)
            stack.append(node)
        elif token == ")":
            if len(stack) == 1:
                raise ValueError("Unexpected closing parenthesis in footprint.")
            stack.pop()
        else:
            stack[-1].append(token[1:-1] if token.startswith('"') else token)

    if len(stack) != 1 or len(root) != 1 or not isinstance(root[0], list):
        raise ValueError("Invalid KiCad footprint expression.")
    return root[0]


def _children(node, name):
    return [child for child in node[1:] if isinstance(child, list) and child[0] == name]


def _child(node, name):
    children = _children(node, name)
    return children[0] if children else None


def _numbers(node):
    values = []
    for value in node[1:]:
        if not isinstance(value, str):
            continue
        try:
            values.append(float(value))
        except ValueError:
            continue
    return values


def _layer(node):
    layer = _child(node, "layer")
    return layer[1] if layer and len(layer) > 1 else None


def _width(node):
    stroke = _child(node, "stroke")
    width = _child(stroke, "width") if stroke else _child(node, "width")
    return _numbers(width)[0] if width else 0.0


def _at(node):
    at = _child(node, "at")
    values = _numbers(at) if at else []
    return (values + [0.0, 0.0, 0.0])[:3]


def _point(node, name):
    point = _child(node, name)
    if not point:
        raise ValueError(f"Missing {name} in footprint graphic.")
    values = _numbers(point)
    if len(values) < 2:
        raise ValueError(f"Invalid {name} in footprint graphic.")
    return values[:2]


def _pad(node):
    if len(node) < 4:
        raise ValueError("Invalid pad in footprint.")

    size = _numbers(_child(node, "size"))
    layers = _child(node, "layers")
    shape = node[3]
    attributes = {
        "size": size[:2],
        "at": _at(node),
        "layers": layers[1:] if layers else [],
        "shape": shape if shape != "custom" else "rect",
    }

    rratio = _child(node, "roundrect_rratio")
    if rratio:
        attributes["roundrect_rratio"] = _numbers(rratio)[0]

    drill = _child(node, "drill")
    if drill:
        drill_size = _numbers(drill)
        drill_attributes = {"size": drill_size[:2] if len(drill_size) > 1 else drill_size[0]}
        offset = _child(drill, "offset")
        if offset:
            drill_attributes["offset"] = _numbers(offset)[:2]
        attributes["drill"] = SimpleNamespace(attributes=drill_attributes)

    return SimpleNamespace(attributes=attributes)


def _line(node):
    return SimpleNamespace(
        attributes={
            "width": _width(node),
            "start": _point(node, "start"),
            "end": _point(node, "end"),
            "layer": _layer(node),
        }
    )


def _circle(node):
    return SimpleNamespace(
        attributes={
            "width": _width(node),
            "center": _point(node, "center"),
            "end": _point(node, "end"),
            "layer": _layer(node),
        }
    )


def _rectangle(node):
    start = _point(node, "start")
    end = _point(node, "end")
    width = _width(node)
    layer = _layer(node)
    points = (
        start,
        (end[0], start[1]),
        end,
        (start[0], end[1]),
    )
    return [
        SimpleNamespace(
            attributes={
                "width": width,
                "start": points[index],
                "end": points[(index + 1) % len(points)],
                "layer": layer,
            }
        )
        for index in range(len(points))
    ]


def parse_kicad10_footprint(text):
    """Return a renderer-compatible view of a KiCad 10 footprint."""

    footprint = _parse_sexpr(text)
    if not footprint or footprint[0] != "footprint":
        raise ValueError("Expected a KiCad 10 footprint.")

    pads = []
    lines = []
    circles = []
    for node in footprint[1:]:
        if not isinstance(node, list) or not node:
            continue
        if node[0] == "pad":
            pads.append(_pad(node))
        elif node[0] == "fp_line":
            lines.append(_line(node))
        elif node[0] == "fp_circle":
            circles.append(_circle(node))
        elif node[0] == "fp_rect":
            lines.extend(_rectangle(node))

    return SimpleNamespace(pads=pads, lines=lines, circles=circles)
