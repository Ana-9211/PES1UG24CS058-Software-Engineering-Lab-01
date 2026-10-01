"""Tiny SVG helper used to draw the UML diagrams (no external tools required)."""
import math
from xml.sax.saxutils import escape

FONT = "Arial, Helvetica, sans-serif"


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.el = w, h, []

    def rect(self, x, y, w, h, fill="none", stroke="#222", sw=1.4, rx=0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def ellipse(self, cx, cy, rx, ry, fill="#fff", stroke="#222", sw=1.4):
        self.el.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}" fill="{fill}" '
                       f'stroke="{stroke}" stroke-width="{sw}"/>')

    def line(self, x1, y1, x2, y2, stroke="#222", sw=1.4, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def poly(self, pts, fill="none", stroke="#222", sw=1.4, dash=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def polyline(self, pts, stroke="#222", sw=1.4, dash=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, fs=13, anchor="middle", weight="normal", fill="#111", italic=False):
        st = ' font-style="italic"' if italic else ""
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{fs}" '
                       f'text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}>{escape(s)}</text>')

    def mtext(self, x, y, s, fs=13, lh=None, **kw):
        lh = lh or fs * 1.3
        for i, ln in enumerate(s.split("\n")):
            self.text(x, y + i * lh, ln, fs=fs, **kw)

    def arrowhead(self, x1, y1, x2, y2, kind="open", size=11, stroke="#222"):
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
