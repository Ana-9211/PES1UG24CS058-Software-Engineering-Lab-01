"""Build PDF and DOCX versions of the Markdown deliverables.

Usage (from the docs/ folder):  python build_docs.py
Requires: markdown, markdown-it-py, python-docx, pymupdf and Microsoft Edge (headless) for PDF output.
Output goes to docs/output/.
"""
import os, re, subprocess, sys, tempfile, html
import markdown
from markdown_it import MarkdownIt
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
DOCS = ["SRS", "Test_Plan", "Software_Architecture_and_Design", "Gap_Analysis", "traceability/Requirements_Traceability"]
EDGE = [p for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe") if os.path.exists(p)]

CSS = """
@page { size: A4; margin: 18mm 16mm; }
@page land { size: A4 landscape; margin: 12mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; line-height: 1.4; color: #111; }
h1 { font-size: 20pt; border-bottom: 2px solid #1f3a6e; padding-bottom: 4px; color: #1f3a6e; }
h2 { font-size: 14pt; color: #1f3a6e; margin-top: 18px; border-bottom: 1px solid #ccd; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #1f3a6e; page-break-after: avoid; }
h4 { font-size: 10.5pt; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 8.8pt; page-break-inside: avoid; }
p:has(+ table) { page-break-after: avoid; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #99a; padding: 3px 5px; vertical-align: top; text-align: left; }
th { background: #e4eaf6; }
code { font-family: Consolas, monospace; font-size: 8.8pt; background: #f1f1f4; padding: 0 2px; }
pre { background: #f1f1f4; padding: 6px; font-size: 8.8pt; white-space: pre-wrap; }
blockquote { border-left: 3px solid #c9a227; margin: 8px 0; padding: 2px 10px; background: #fff8e0; }
img { max-width: 100%; display: block; margin: 8px auto; }
.fig { page-break-inside: avoid; }
.land { page: land; }
.land img { max-height: 172mm; width: auto; }
.portrait-img img { max-height: 235mm; width: auto; }
"""


def strip_front_matter(text):
    return re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)


def build_pdf(name, text):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    body = md.convert(text)

    def wrap(m):
        src = m.group(2)
        cls = "land" if "component" in src else "portrait-img"
        return f'<div class="fig {cls}"><img alt="{m.group(1)}" src="{src}"/><p style="text-align:center"><em>{m.group(1)}</em></p></div>'
    body = re.sub(r'<p><img alt="([^"]*)" src="([^"]*)" ?/></p>', wrap, body)
    base = os.path.dirname(os.path.join(HERE, name + ".md")).replace("\\", "/")
    page = f'<html><head><meta charset="utf-8"><base href="file:///{base}/"><style>{CSS}</style></head><body>{body}</body></html>'
    tmp = os.path.join(tempfile.gettempdir(), os.path.basename(name) + ".html")
    open(tmp, "w", encoding="utf-8").write(page)
    out = os.path.join(OUT, os.path.basename(name) + ".pdf")
    if not EDGE:
        print("  (no Edge/Chrome found, skipping PDF)")
        return
    subprocess.run([EDGE[0], "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out}",
                    "file:///" + tmp.replace("\\", "/")], check=True, capture_output=True, timeout=180)
    print("  pdf ->", out)


# ------------------------------------------------------------------ DOCX
def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def add_inline(par, children, size=None):
    bold = ital = code = False
    for t in children or []:
        if t.type == "text":
            run = par.add_run(t.content)
        elif t.type == "code_inline":
            run = par.add_run(t.content); run.font.name = "Consolas"
        elif t.type in ("softbreak", "hardbreak"):
            par.add_run("\n"); continue
        elif t.type == "strong_open":
            bold = True; continue
        elif t.type == "strong_close":
            bold = False; continue
        elif t.type == "em_open":
            ital = True; continue
        elif t.type == "em_close":
            ital = False; continue
        elif t.type == "html_inline":
            continue
        else:
            continue
        run.bold = bold or None
        run.italic = ital or None
        if size:
            run.font.size = Pt(size)


def build_docx(name, text):
    md = MarkdownIt("commonmark").enable("table")
    toks = md.parse(text)
    d = docx.Document()
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Inches(0.8)
    sec.top_margin = sec.bottom_margin = Inches(0.8)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    base = os.path.dirname(os.path.join(HERE, name + ".md"))
    i = 0
    list_stack = []

    def inline_of(idx):
        return toks[idx].children

    while i < len(toks):
        t = toks[i]
        if t.type == "heading_open":
            lvl = int(t.tag[1]); inl = toks[i + 1]
            h = d.add_heading(level=min(lvl, 4))
            add_inline(h, inl.children)
            i += 3; continue
        if t.type == "paragraph_open":
            inl = toks[i + 1]
            kids = inl.children or []
            imgs = [k for k in kids if k.type == "image"]
            if imgs:
                im = imgs[0]
                path = os.path.normpath(os.path.join(base, im.attrs["src"]))
                w, h = Image.open(path).size
                wide = "component" in path
                if wide:
                    ns = d.add_section(); ns.orientation = WD_ORIENT.LANDSCAPE
                    ns.page_width, ns.page_height = ns.page_height, ns.page_width
                    maxw, maxh = 9.4, 6.2
                else:
                    maxw, maxh = 6.7, 8.6
                sc = min(maxw / w, maxh / h)
                d.add_picture(path, width=Inches(w * sc))
                d.paragraphs[-1].alignment = 1
                cap = d.add_paragraph(); cap.alignment = 1
                r = cap.add_run(im.content or ""); r.italic = True; r.font.size = Pt(9)
                if wide:
                    ns = d.add_section(); ns.orientation = WD_ORIENT.PORTRAIT
                    ns.page_width, ns.page_height = ns.page_height, ns.page_width
            else:
                p = d.add_paragraph(style="List Bullet" if list_stack else None)
                add_inline(p, kids)
            i += 3; continue
        if t.type in ("bullet_list_open", "ordered_list_open"):
            list_stack.append(t.type); i += 1; continue
        if t.type in ("bullet_list_close", "ordered_list_close"):
            list_stack.pop(); i += 1; continue
        if t.type == "list_item_open" or t.type == "list_item_close":
            i += 1; continue
        if t.type == "fence" or t.type == "code_block":
            p = d.add_paragraph(); r = p.add_run(t.content.rstrip()); r.font.name = "Consolas"; r.font.size = Pt(9)
            i += 1; continue
        if t.type == "blockquote_open":
            i += 1; continue
        if t.type == "blockquote_close":
            i += 1; continue
        if t.type == "hr":
            i += 1; continue
        if t.type == "table_open":
            rows = []; j = i + 1; head_n = 0
            cur = None
            while toks[j].type != "table_close":
                tk = toks[j]
                if tk.type == "tr_open":
                    cur = []
                elif tk.type in ("th_open", "td_open"):
                    cur.append((tk.type == "th_open", toks[j + 1].children))
                elif tk.type == "tr_close":
                    rows.append(cur)
                j += 1
            ncol = max(len(r) for r in rows)
            tb = d.add_table(rows=len(rows), cols=ncol)
            tb.style = "Table Grid"; tb.alignment = WD_TABLE_ALIGNMENT.CENTER
            for ri, r in enumerate(rows):
                for ci, (is_h, kids) in enumerate(r):
                    c = tb.cell(ri, ci); c.text = ""
                    p = c.paragraphs[0]
                    add_inline(p, kids, size=8.5)
                    if is_h:
                        for run in p.runs:
                            run.bold = True
                        shade(c, "E4EAF6")
            d.add_paragraph()
            i = j + 1; continue
        i += 1
    out = os.path.join(OUT, os.path.basename(name) + ".docx")
    d.save(out)
    print("  docx ->", out)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in DOCS:
        print(name)
        text = strip_front_matter(open(os.path.join(HERE, name + ".md"), encoding="utf-8").read())
        build_pdf(name, text)
        build_docx(name, text)
