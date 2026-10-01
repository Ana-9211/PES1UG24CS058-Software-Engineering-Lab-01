"""Generates the four UML diagrams (SVG + PNG). Run: python make_diagrams.py"""
import os
from svglib import SVG, ellipse_edge, rect_edge, save_drawio
import pymupdf

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
UCFILL = {"core": "#dbe8fb", "inc": "#dcefd8", "ext": "#fde5c4"}


# ----------------------------------------------------------------- use case
def use_case():
    s = SVG(1240, 980)
    s.fscale = 1.12
    s.rect(170, 40, 830, 780, stroke="#222")
    s.text(585, 66, "Smart Lab Equipment & Slot Reservation Portal", fs=16, weight="bold")
    RX, RY = 105, 32
    ucs = {  # id: (x, y, name, kind)
        "UC-01": (560, 120, "Login / Authenticate", "core"),
        "UC-02": (290, 200, "View Equipment\nAvailability", "core"),
        "UC-03": (560, 270, "Reserve Equipment Slot", "core"),
        "UC-09": (860, 225, "Verify Calibration\nStatus", "inc"),
        "UC-10": (860, 345, "Generate Reservation\nToken", "inc"),
        "UC-11": (560, 410, "Send Confirmation\nNotification", "inc"),
        "UC-04": (290, 450, "Cancel Reservation", "core"),
        "UC-05": (290, 600, "View Reservation\nHistory", "core"),
        "UC-07": (860, 480, "Update Calibration\nStatus", "core"),
        "UC-06": (860, 590, "Return Equipment", "core"),
        "UC-12": (560, 640, "Apply Late-Return\nPenalty", "ext"),
        "UC-08": (860, 700, "Manage Equipment\nInventory", "core"),
    }
    stu, tech, notif = (90, 430), (1130, 520), (330, 870)
    for u in ["UC-01", "UC-02", "UC-03", "UC-04", "UC-05"]:
        x, y = ucs[u][:2]
        ex, ey = ellipse_edge(x, y, RX, RY, *stu)
        s.line(stu[0] + 20, stu[1] + 31, ex, ey)
    s.polyline([(1130, 500), (1130, 120), (665, 120)])
    for u in ["UC-06", "UC-07", "UC-08"]:
        x, y = ucs[u][:2]
        ex, ey = ellipse_edge(x, y, RX, RY, *tech)
        s.line(tech[0] - 20, tech[1] + 31, ex, ey)
    x, y = ucs["UC-11"][:2]
    ex, ey = ellipse_edge(x, y, RX, RY, notif[0], notif[1])
    s.line(notif[0], notif[1] + 8, ex, ey)
    for u, (x, y, name, kind) in ucs.items():
        s.ellipse(x, y, RX, RY, fill=UCFILL[kind])
        lines = name.split("\n")
        off = -12 if len(lines) == 1 else -17
        s.text(x, y + off - 2, u, fs=10, fill="#444", weight="bold")
        for i, ln in enumerate(lines):
            s.text(x, y + off + 14 + i * 14, ln, fs=12.5)

    def rel(a, b):
        ax, ay = ucs[a][:2]
        bx, by = ucs[b][:2]
        p1 = ellipse_edge(ax, ay, RX, RY, bx, by)
        p2 = ellipse_edge(bx, by, RX, RY, ax, ay)
        s.arrow(*p1, *p2, dash="6,4")
        return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

    mx, my = rel("UC-03", "UC-09")
    s.text(mx, my - 14, "«include»", fs=11, italic=True)
    mx, my = rel("UC-03", "UC-10")
    s.text(mx + 36, my - 2, "«include»", fs=11, italic=True)
    mx, my = rel("UC-03", "UC-11")
    s.text(mx + 42, my + 2, "«include»", fs=11, italic=True)
    mx, my = rel("UC-12", "UC-06")
    s.text(mx, my - 12, "«extend»", fs=11, italic=True)
    s.text(mx + 14, my + 24, "[return time > slot end]", fs=10, italic=True, anchor="start")
    s.actor(stu[0], stu[1] - 10, "Student")
    s.actor(tech[0], tech[1] - 10, "Lab Technician")
    s.text(notif[0], notif[1] + 60, "Notification System", fs=13, weight="bold")
    s.text(notif[0], notif[1] + 76, "«external system»", fs=10.5, italic=True)
        # secondary actor stick figure
    nx, ny = notif[0], notif[1] + 8
    s.line(nx, ny + 1, nx, ny + 24)
    s.line(nx - 15, ny + 9, nx + 15, ny + 9)
    s.line(nx, ny + 24, nx - 12, ny + 40)
    s.line(nx, ny + 24, nx + 12, ny + 40)
    # legend
    s.rect(1010, 830, 215, 125, stroke="#999", sw=1)
    s.text(1020, 850, "Legend", fs=12, anchor="start", weight="bold")
    for i, (k, t) in enumerate([("core", "Primary use case"), ("inc", "Included use case"), ("ext", "Extending use case")]):
        s.rect(1022, 862 + i * 22, 24, 14, fill=UCFILL[k], stroke="#555", sw=1)
        s.text(1054, 874 + i * 22, t, fs=11, anchor="start")
    s.text(1020, 940, "Dashed arrow = UML dependency", fs=10.5, anchor="start", italic=True)
    s.save(os.path.join(OUT, "use-case.svg")); save_drawio(s, os.path.join(OUT, "use-case.drawio"), "use-case")


# ----------------------------------------------------------------- component
def component():
    s = SVG(1420, 900)
    s.fscale = 1.1
    s.text(710, 28, "Component Diagram - Smart Lab Equipment & Slot Reservation Portal", fs=16, weight="bold")
    for x, w, t in [(20, 190, "«tier» Client"), (230, 700, "«tier» Application Server"),
                    (950, 190, "«tier» Data"), (1160, 240, "«external»")]:
        s.rect(x, 50, w, 810, fill="#f6f6f6", stroke="#888", sw=1, dash="6,4")
        s.text(x + w / 2, 72, t, fs=12, weight="bold", fill="#555")
    s.rect(560, 270, 340, 480, fill="#fafafa", stroke="#555", sw=1.2)
    s.rect(560, 270, 130, 20, fill="#eee", stroke="#555", sw=1.2)
    s.text(625, 285, "Business Services", fs=11, weight="bold")

    W, H = 190, 64
    comps = {
        "C-01": (105, 160, "Web Client", 140, "«component»"),
        "C-02": (360, 160, "API Layer\ninput validation, security filter", 230, "«component»"),
        "C-03": (350, 330, "Authentication &\nSession Service", 150, "«component»"),
        "C-04": (350, 450, "Access Control\nGuard (RBAC)", 150, "«component»"),
        "C-05": (730, 345, "Reservation Service", W, "«component»"),
        "C-06": (730, 460, "Calibration Service", W, "«component»"),
        "C-07": (730, 575, "Inventory Service", W, "«component»"),
        "C-08": (730, 690, "Return & Penalty\nService", W, "«component»"),
        "C-09": (730, 175, "Notification Adapter", 190, "«component»"),
        "C-10": (730, 800, "Audit Logger", 170, "«component»"),
        "C-11": (1045, 460, "Data Access\nLayer", 150, "«component»"),
        "C-12": (1045, 700, "Relational\nDatabase", 140, "«database»"),
        "EXT": (1280, 175, "Notification\nSystem", 140, "«external system»"),
    }
    boxes = {}
    for cid, (cx, cy, name, w, st) in comps.items():
        h = H
        x, y = cx - w / 2, cy - h / 2
        fill = "#fff2cc" if cid == "EXT" else ("#e6e6e6" if cid == "C-12" else "#dbe8fb")
        s.rect(x, y, w, h, fill=fill, stroke="#222", sw=1.5)
        if cid not in ("C-12", "EXT"):
            ix, iy = x + w - 24, y + 7
            s.rect(ix, iy, 16, 11, fill=fill, stroke="#222", sw=1)
            s.rect(ix - 4, iy + 2, 8, 3, fill=fill, stroke="#222", sw=1)
            s.rect(ix - 4, iy + 6, 8, 3, fill=fill, stroke="#222", sw=1)
        s.text(cx - (6 if cid not in ("C-12", "EXT") else 0), y + 15, st, fs=9.5, italic=True, fill="#444")
        for i, ln in enumerate(name.split("\n")):
            s.text(cx, y + 31 + i * 14, ln, fs=12 if i == 0 else 10.5, weight="bold" if i == 0 else "normal")
        if cid != "EXT":
            s.text(x + 6, y + h - 5, cid, fs=9.5, anchor="start", fill="#444", weight="bold")
        boxes[cid] = (cx, cy, w, h)

    def dep(path, label=None, lpos=None, anchor="middle"):
        s.polyline(path, dash="6,4")
        s.arrowhead(*path[-2], *path[-1])
        if label:
            s.text(lpos[0], lpos[1], label, fs=10.5, italic=True, anchor=anchor)

    def edge(a, b, label=None, lpos=None, anchor="middle"):
        ax, ay, aw, ah = boxes[a]
        bx, by, bw, bh = boxes[b]
        p1 = rect_edge(ax, ay, aw, ah, bx, by)
        p2 = rect_edge(bx, by, bw, bh, ax, ay)
        dep([p1, p2], label, lpos, anchor)

    edge("C-01", "C-02", "HTTP / JSON", (210, 150))
    edge("C-02", "C-03", "IAuthenticate", (352, 258), "end")
    dep([(260, 192), (260, 450), (275, 450)], "IAuthorize", (236, 505), "start")
    edge("C-04", "C-03", "ISession", (358, 394), "start")
    # API -> services bus
    s.line(475, 160, 520, 160, dash="6,4")
    s.line(520, 160, 520, 690, dash="6,4")
    for y in (345, 460, 575, 690):
        s.line(520, y, 635, y, dash="6,4")
        s.arrowhead(520, y, 635, y)
    for i, ln in enumerate(["IReservation,", "ICalibration,", "IInventory,", "IReturn"]):
        s.text(528, 200 + i * 12, ln, fs=10, italic=True, anchor="start")
    s.text(500, 118, "IInventory, IReturn", fs=10, italic=True, anchor="start") if False else None
    s.text(485, 134, "IInventory, IReturn", fs=10, italic=True, anchor="start") if False else None
    # Reservation -> Calibration
    dep([(730, 377), (730, 428)], "verifyCalibration", (740, 408), "start")
    # Reservation -> Notification adapter (up)
    dep([(730, 313), (730, 207)], "INotify", (740, 300), "start")
    # Notification adapter -> external
    dep([(825, 175), (1210, 175)], "email / notification request", (1015, 166))
    # package -> Audit Logger
    dep([(730, 750), (730, 768)])
    s.text(740, 762, "ILog", fs=10.5, italic=True, anchor="start")
    # package -> Data Access Layer
    dep([(900, 445), (970, 445)], "IData", (935, 464))
    # Auth -> DAL over the top
    dep([(425, 316), (480, 316), (480, 245), (940, 245), (940, 430), (970, 430)], "IData (credentials, sessions)", (850, 238))
    # Audit -> DAL
    dep([(815, 800), (940, 800), (940, 480), (970, 480)], "IData (audit records)", (960, 790), "start")
    # DAL -> DB
    dep([(1045, 492), (1045, 668)], "SQL / transactions", (1055, 585), "start")
    s.save(os.path.join(OUT, "component.svg")); save_drawio(s, os.path.join(OUT, "component.drawio"), "component")


# ----------------------------------------------------------------- sequence
def sequence(name, title, parts, items, spacing=190, fs=12.5):
    n = len(parts)
    left = 40
    W = left * 2 + spacing * n
    xs = [left + spacing * i + spacing / 2 for i in range(n)]
    pidx = {p[0]: i for i, p in enumerate(parts)}
    ops, y, stack, frames = [], 160, [], []
    for it in items:
        k = it[0]
        if k == "msg":
            _, a, b, t, *r = it
            y += 38
            ops.append(("msg", pidx[a], pidx[b], t, y, bool(r and r[0] == "ret")))
        elif k == "self":
            _, a, t = it
            y += 36
            ops.append(("self", pidx[a], t, y))
            y += 14
        elif k == "note":
            _, a, t = it
            h = 18 + 15 * len(t.split("\n"))
            y += 14
            ops.append(("note", pidx[a], t, y, h))
            y += h + 4
        elif k == "begin":
            _, kind, cond = it
            y += 26
            stack.append({"kind": kind, "y0": y, "elses": [], "depth": len(stack)})
            ops.append(("cond", len(stack) - 1, cond, y))
            y += 6
        elif k == "else":
            _, cond = it
            y += 22
            stack[-1]["elses"].append(y)
            ops.append(("cond2", len(stack) - 1, cond, y))
            y += 4
        elif k == "end":
            y += 14
            f = stack.pop()
            f["y1"] = y
            frames.append(f)
    H = y + 50
    s = SVG(W, H)
    s.fscale = 1.12
    s.text(W / 2, 28, title, fs=16, weight="bold")
    top = 52
    for i, (pid, label, kind) in enumerate(parts):
        s.line(xs[i], top + (96 if kind == "actor" else 54), xs[i], H - 24, dash="5,4", stroke="#777")
    for i, (pid, label, kind) in enumerate(parts):
        if kind == "actor":
            s.actor(xs[i], top, label, fs=12.5)
        else:
            bw = spacing - 30
            s.rect(xs[i] - bw / 2, top, bw, 50, fill="#fff2cc" if kind == "ext" else "#dbe8fb", stroke="#222", sw=1.5)
            s.text(xs[i], top + 14, "«external»" if kind == "ext" else "«component»", fs=9.5, italic=True, fill="#444")
            for j, ln in enumerate(label.split("\n")):
                s.text(xs[i], top + 29 + j * 13, ln, fs=12, weight="bold")
    for f in sorted(frames, key=lambda f: f["depth"]):
        inset = 22 * f["depth"]
        x0, x1 = 22 + inset, W - 22 - inset
        s.rect(x0, f["y0"], x1 - x0, f["y1"] - f["y0"], stroke="#444", sw=1.2)
        tw = 12 + 8 * len(f["kind"])
        s.poly([(x0, f["y0"]), (x0 + tw, f["y0"]), (x0 + tw, f["y0"] + 12), (x0 + tw - 7, f["y0"] + 20), (x0, f["y0"] + 20)],
               fill="#eee", stroke="#444", sw=1.2)
        s.text(x0 + 7, f["y0"] + 14, f["kind"], fs=11.5, anchor="start", weight="bold")
        for ey in f["elses"]:
            s.line(x0, ey - 14, x1, ey - 14, dash="8,5", stroke="#444", sw=1.2)
    for op in ops:
        if op[0] == "cond":
            f = [fr for fr in frames if fr["depth"] == op[1] and abs(fr["y0"] - op[3]) < 1][0]
            x0 = 22 + 22 * f["depth"] + 12 + 8 * len(f["kind"]) + 8
            s.text(x0, op[3] + 14, "[" + op[2] + "]", fs=11.5, anchor="start", italic=True)
        elif op[0] == "cond2":
            s.text(22 + 22 * op[1] + 12, op[3], "[" + op[2] + "]", fs=11.5, anchor="start", italic=True)
        elif op[0] == "msg":
            _, a, b, t, yy, ret = op
            x1, x2 = xs[a], xs[b]
            s.line(x1, yy, x2, yy, dash="7,4" if ret else None)
            s.arrowhead(x1, yy, x2, yy, kind="open" if ret else "filled")
            s.text((x1 + x2) / 2, yy - 6, t, fs=fs)
        elif op[0] == "self":
            _, a, t, yy = op
            x = xs[a]
            s.polyline([(x, yy - 8), (x + 34, yy - 8), (x + 34, yy + 10), (x, yy + 10)])
            s.arrowhead(x + 34, yy + 10, x, yy + 10, kind="filled")
            s.text(x + 42, yy + 3, t, fs=fs, anchor="start")
        elif op[0] == "note":
            _, a, t, yy, h = op
            lines = t.split("\n")
            wmax = max(len(l) for l in lines) * 6.4 + 22
            x0 = min(xs[a] - 20, W - 34 - wmax)
            s.poly([(x0, yy), (x0 + wmax - 10, yy), (x0 + wmax, yy + 10), (x0 + wmax, yy + h), (x0, yy + h)],
                   fill="#fffbd6", stroke="#999", sw=1)
            for j, ln in enumerate(lines):
                s.text(x0 + 8, yy + 16 + j * 15, ln, fs=11, anchor="start")
    s.save(os.path.join(OUT, name + ".svg")); save_drawio(s, os.path.join(OUT, name + ".drawio"), name)


def sd01a():
    parts = [("stu", "Student", "actor"), ("web", "Web Client\n(C-01)", "c"), ("api", "API Layer\n(C-02)", "c"),
             ("res", "Reservation Service\n(C-05)", "c"), ("cal", "Calibration Service\n(C-06)", "c"),
             ("dal", "Data Access Layer\n(C-11)", "c")]
    it = [
        ("msg", "stu", "web", "select equipment, start, duration (<= 2 h)"),
        ("msg", "web", "api", "POST /api/v1/reservations"),
        ("self", "api", "validate session, role, inputs (C-03, C-04)"),
        ("begin", "alt", "session / role / input invalid - alternate flow A3"),
        ("msg", "api", "web", "401 / 403 / 422 error response", "ret"),
        ("else", "session, role and inputs valid"),
        ("msg", "api", "res", "reserve(studentId, equipmentId, start, duration)"),
        ("msg", "res", "cal", "verifyCalibration(equipmentId)  \u00abinclude\u00bb UC-09"),
        ("msg", "cal", "dal", "getCalibrationStatus(equipmentId)"),
        ("msg", "dal", "cal", "status", "ret"),
        ("msg", "cal", "res", "status", "ret"),
        ("begin", "alt", "status != Valid (Expired / Pending) - alternate flow A1"),
        ("msg", "res", "api", "CalibrationInvalid + alternative instruments", "ret"),
        ("msg", "api", "web", "409 CALIBRATION_INVALID", "ret"),
        ("msg", "web", "stu", "message: calibration required + alternatives", "ret"),
        ("else", "status = Valid"),
        ("note", "res", "continues in part 2: overlap check,\nreservation, notification"),
        ("end",), ("end",),
    ]
    sequence("sequence-01a", "Sequence Diagram 1 (part 1 of 2) - UC-03 Reserve Equipment Slot: request validation and calibration check",
             parts, it, spacing=200)


def sd01b():
    parts = [("stu", "Student", "actor"), ("web", "Web Client\n(C-01)", "c"), ("api", "API Layer\n(C-02)", "c"),
             ("res", "Reservation Service\n(C-05)", "c"), ("dal", "Data Access Layer\n(C-11)", "c"),
             ("nad", "Notification Adapter\n(C-09)", "c"), ("ext", "Notification System", "ext")]
    it = [
        ("note", "res", "starts from part 1: session valid, calibration status = Valid"),
        ("msg", "res", "dal", "beginTransaction; lock equipment time slots"),
        ("msg", "res", "dal", "findOverlaps(equipment window, student window)"),
        ("msg", "dal", "res", "overlap result", "ret"),
        ("begin", "alt", "overlap found - alternate flow A2 (or A4 for the student's own overlap)"),
        ("msg", "res", "dal", "rollback"),
        ("msg", "res", "api", "SlotConflict + next available slots", "ret"),
        ("msg", "api", "web", "409 SLOT_CONFLICT / STUDENT_SLOT_CONFLICT", "ret"),
        ("msg", "web", "stu", "message: choose another slot", "ret"),
        ("else", "no overlap"),
        ("self", "res", "generate unique token  \u00abinclude\u00bb UC-10"),
        ("msg", "res", "dal", "insertReservation(Confirmed, token); commit"),
        ("msg", "dal", "res", "reservation saved; slot locked", "ret"),
        ("msg", "res", "nad", "sendConfirmation(reservation)  \u00abinclude\u00bb UC-11"),
        ("msg", "nad", "ext", "deliver email / notification"),
        ("note", "nad", "delivery failure is logged; reservation is kept (A-06)"),
        ("msg", "res", "api", "reservation (token, slot)", "ret"),
        ("msg", "api", "web", "201 Created {token, slot details}", "ret"),
        ("msg", "web", "stu", "confirmation screen (token, slot)", "ret"),
        ("end",),
    ]
    sequence("sequence-01b", "Sequence Diagram 1 (part 2 of 2) - UC-03 Reserve Equipment Slot: reservation, token and notification",
             parts, it, spacing=190)


def sd02():
    parts = [("tec", "Lab Technician", "actor"), ("web", "Web Client\n(C-01)", "c"), ("api", "API Layer\n(C-02)", "c"),
             ("ret", "Return & Penalty Service\n(C-08)", "c"), ("dal", "Data Access Layer\n(C-11)", "c"),
             ("aud", "Audit Logger\n(C-10)", "c")]
    it = [
        ("msg", "tec", "web", "select reserved item, choose 'Mark Returned'"),
        ("msg", "web", "api", "POST /api/v1/reservations/{id}/return"),
        ("self", "api", "validate session (30 min idle), role = Technician"),
        ("begin", "alt", "session expired / role != Lab Technician / malformed id"),
        ("msg", "api", "web", "401 / 403 / 400 error response", "ret"),
        ("else", "authorized and valid"),
        ("msg", "api", "ret", "recordReturn(reservationId, technicianId)"),
        ("msg", "ret", "dal", "getReservation(reservationId)"),
        ("msg", "dal", "ret", "reservation (status, slotEnd) or none", "ret"),
        ("begin", "alt", "not found"),
        ("msg", "ret", "api", "ReservationNotFound  (API Layer returns 404)", "ret"),
        ("else", "status != Confirmed (already returned / cancelled)"),
        ("msg", "ret", "api", "InvalidState  (API Layer returns 409)", "ret"),
        ("else", "status = Confirmed"),
        ("self", "ret", "returnTime = now(); late = returnTime > slotEnd"),
        ("begin", "opt", "late = true   «extend» UC-12 Apply Late-Return Penalty"),
        ("self", "ret", "penaltyFlag = true"),
        ("end",),
        ("msg", "ret", "dal", "saveReturn(id, returnTime, penaltyFlag, Returned)"),
        ("msg", "dal", "ret", "saved", "ret"),
        ("msg", "ret", "aud", "log(technicianId, RETURN, id, returnTime, penaltyFlag)"),
        ("msg", "ret", "api", "return result", "ret"),
        ("msg", "api", "web", "200 OK {returnTimestamp, penaltyFlag}", "ret"),
        ("end",), ("end",),
        ("msg", "web", "tec", "return confirmation (penalty flag shown)", "ret"),
    ]
    sequence("sequence-02", "Sequence Diagram 2 - UC-06 Return Equipment", parts, it, spacing=195)


def to_png(name, dpi=170):
    doc = pymupdf.open(os.path.join(OUT, name + ".svg"))
    pix = doc[0].get_pixmap(dpi=dpi)
    pix.save(os.path.join(OUT, name + ".png"))
    print(name, pix.width, pix.height)


if __name__ == "__main__":
    use_case(); component(); sd01a(); sd01b(); sd02()
    for n in ["use-case", "component", "sequence-01a", "sequence-01b", "sequence-02"]:
        to_png(n)
