"""Tiny SVG helper used to draw the UML diagrams (no external tools required)."""
import math
from xml.sax.saxutils import escape

FONT = "Arial, Helvetica, sans-serif"


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.el = w, h, []
        self.prims = []   # structured copy of everything drawn (used for the draw.io export)
        self._rec = True

    def rect(self, x, y, w, h, fill="none", stroke="#222", sw=1.4, rx=0, dash=None):
        self._p("rect", x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, sw=sw, dash=dash)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def ellipse(self, cx, cy, rx, ry, fill="#fff", stroke="#222", sw=1.4):
        self._p("ellipse", cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, stroke=stroke, sw=sw)
        self.el.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}" fill="{fill}" '
                       f'stroke="{stroke}" stroke-width="{sw}"/>')

    def line(self, x1, y1, x2, y2, stroke="#222", sw=1.4, dash=None):
        self._p("edge", pts=[(x1, y1), (x2, y2)], stroke=stroke, sw=sw, dash=dash)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def poly(self, pts, fill="none", stroke="#222", sw=1.4, dash=None):
        self._p("poly", pts=list(pts), fill=fill, stroke=stroke, sw=sw, dash=dash)
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def polyline(self, pts, stroke="#222", sw=1.4, dash=None):
        self._p("edge", pts=list(pts), stroke=stroke, sw=sw, dash=dash)
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, fs=13, anchor="middle", weight="normal", fill="#111", italic=False):
        self._p("text", x=x, y=y, s=s, fs=fs, anchor=anchor, weight=weight, fill=fill, italic=italic)
        st = ' font-style="italic"' if italic else ""
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{fs}" '
                       f'text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}>{escape(s)}</text>')

    def mtext(self, x, y, s, fs=13, lh=None, **kw):
        lh = lh or fs * 1.3
        for i, ln in enumerate(s.split("\n")):
            self.text(x, y + i * lh, ln, fs=fs, **kw)

    def _p(self, kind, **kw):
        if self._rec:
            self.prims.append(dict(kind=kind, **kw))

    def arrowhead(self, x1, y1, x2, y2, kind="open", size=11, stroke="#222"):
        self._p("arrowhead", tip=(x2, y2), style=kind)
        self._rec = False
        try:
            self._arrowhead(x1, y1, x2, y2, kind, size, stroke)
        finally:
            self._rec = True

    def _arrowhead(self, x1, y1, x2, y2, kind="open", size=11, stroke="#222"):
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - size * math.cos(a - 0.4), y2 - size * math.sin(a - 0.4))
        p2 = (x2 - size * math.cos(a + 0.4), y2 - size * math.sin(a + 0.4))
        if kind == "open":
            self.polyline([p1, (x2, y2), p2], stroke=stroke)
        else:
            self.poly([p1, (x2, y2), p2], fill=stroke, stroke=stroke)

    def arrow(self, x1, y1, x2, y2, dash=None, kind="open", stroke="#222"):
        self.line(x1, y1, x2, y2, stroke=stroke, dash=dash)
        self.arrowhead(x1, y1, x2, y2, kind=kind, stroke=stroke)

    def actor(self, x, y, label, fs=13):
        """Stick figure; (x, y) = top of head."""
        self.ellipse(x, y + 10, 10, 10, fill="#fff")
        self.line(x, y + 20, x, y + 52)
        self.line(x - 17, y + 31, x + 17, y + 31)
        self.line(x, y + 52, x - 15, y + 76)
        self.line(x, y + 52, x + 15, y + 76)
        self.mtext(x, y + 94, label, fs=fs, weight="bold")

    def save(self, path):
        body = "\n".join(self.el)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}"><rect width="100%" height="100%" fill="#fff"/>\n{body}\n</svg>')
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)


def ellipse_edge(cx, cy, rx, ry, tx, ty):
    """Point on ellipse boundary in the direction of (tx, ty)."""
    dx, dy = tx - cx, ty - cy
    d = math.hypot(dx / rx, dy / ry) or 1
    return cx + dx / d, cy + dy / d


def rect_edge(cx, cy, w, h, tx, ty):
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (w / 2) / abs(dx) if dx else 1e9
    sy = (h / 2) / abs(dy) if dy else 1e9
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


# ---------------------------------------------------------------- draw.io export
def _esc(s):
    return escape(s, {'"': "&quot;"})


def save_drawio(svg, path, name):
    """Write the recorded primitives as an editable draw.io (mxGraph) diagram."""
    cells, nid = [], [2]

    def new_id():
        nid[0] += 1
        return f"c{nid[0]}"

    prims = svg.prims
    last_edge = None
    for p in prims:  # attach each arrowhead to the edge that ends at its tip
        if p["kind"] == "edge":
            last_edge = p
        elif p["kind"] == "arrowhead":
            e = last_edge
            if e and abs(e["pts"][-1][0] - p["tip"][0]) < 1.5 and abs(e["pts"][-1][1] - p["tip"][1]) < 1.5:
                e["end"] = "open" if p["style"] == "open" else "block"
                e["endFill"] = 0 if p["style"] == "open" else 1
    for p in prims:
        k = p["kind"]
        if k == "rect":
            st = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={p['fill']};strokeColor={p['stroke']};"
                  f"strokeWidth={p['sw']};")
            if p["dash"]:
                st += "dashed=1;dashPattern=6 4;"
            cells.append(f'<mxCell id="{new_id()}" value="" style="{st}" vertex="1" parent="1">'
                         f'<mxGeometry x="{p["x"]:.1f}" y="{p["y"]:.1f}" width="{p["w"]:.1f}" height="{p["h"]:.1f}" as="geometry"/></mxCell>')
        elif k == "ellipse":
            if p["rx"] < 1:
                continue
            st = f"ellipse;whiteSpace=wrap;html=1;fillColor={p['fill']};strokeColor={p['stroke']};strokeWidth={p['sw']};"
            cells.append(f'<mxCell id="{new_id()}" value="" style="{st}" vertex="1" parent="1">'
                         f'<mxGeometry x="{p["cx"]-p["rx"]:.1f}" y="{p["cy"]-p["ry"]:.1f}" width="{2*p["rx"]:.1f}" height="{2*p["ry"]:.1f}" as="geometry"/></mxCell>')
        elif k == "poly":
            xs = [q[0] for q in p["pts"]]
            ys = [q[1] for q in p["pts"]]
            x0, y0, w, h = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
            shape = "shape=note;size=10;" if p["fill"] == "#fffbd6" else "shape=card;size=8;flipH=1;flipV=1;"
            st = f"{shape}whiteSpace=wrap;html=1;fillColor={p['fill']};strokeColor={p['stroke']};strokeWidth={p['sw']};"
            cells.append(f'<mxCell id="{new_id()}" value="" style="{st}" vertex="1" parent="1">'
                         f'<mxGeometry x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>')
        elif k == "edge":
            pts = p["pts"]
            end = p.get("end", "none")
            st = (f"endArrow={end};endFill={p.get('endFill', 0)};startArrow=none;html=1;rounded=0;"
                  f"strokeColor={p['stroke']};strokeWidth={p['sw']};endSize=8;")
            if p["dash"]:
                st += "dashed=1;dashPattern=6 4;"
            mid = "".join(f'<mxPoint x="{x:.1f}" y="{y:.1f}"/>' for x, y in pts[1:-1])
            arr = f'<Array as="points">{mid}</Array>' if mid else ""
            cells.append(f'<mxCell id="{new_id()}" value="" style="{st}" edge="1" parent="1">'
                         f'<mxGeometry relative="1" as="geometry"><mxPoint x="{pts[0][0]:.1f}" y="{pts[0][1]:.1f}" as="sourcePoint"/>'
                         f'<mxPoint x="{pts[-1][0]:.1f}" y="{pts[-1][1]:.1f}" as="targetPoint"/>{arr}</mxGeometry></mxCell>')
        elif k == "text":
            fs = p["fs"]
            w = len(p["s"]) * fs * 0.56 + 12
            h = fs * 1.6
            x = p["x"] - w / 2 if p["anchor"] == "middle" else (p["x"] if p["anchor"] == "start" else p["x"] - w)
            y = p["y"] - fs * 1.15
            fstyle = (1 if p["weight"] == "bold" else 0) + (2 if p["italic"] else 0)
            al = {"middle": "center", "start": "left", "end": "right"}[p["anchor"]]
            st = (f"text;html=1;strokeColor=none;fillColor=none;align={al};verticalAlign=middle;whiteSpace=nowrap;"
                  f"fontSize={fs:g};fontStyle={fstyle};fontColor={p['fill']};fontFamily=Helvetica;spacing=0;")
            cells.append(f'<mxCell id="{new_id()}" value="{_esc(p["s"])}" style="{st}" vertex="1" parent="1">'
                         f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>')
    xml = (f'<mxfile host="app.diagrams.net"><diagram id="{name}" name="{name}">'
           f'<mxGraphModel dx="{svg.w}" dy="{svg.h}" grid="0" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" '
           f'pageScale="1" pageWidth="{svg.w}" pageHeight="{svg.h}" math="0" shadow="0"><root><mxCell id="0"/>'
           f'<mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
