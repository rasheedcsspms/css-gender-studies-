"""Figure templates drawn with matplotlib from short text specs.

Every template takes the lines of a ``::: fig TYPE | caption`` block.
Options are lines starting with ``@key value``; items are the other lines.
Text is wrapped by measuring the real font, so boxes never overflow.
"""
import hashlib
import math
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from matplotlib import font_manager                   # noqa: E402
from matplotlib.font_manager import FontProperties    # noqa: E402
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch  # noqa: E402
from matplotlib.path import Path as MPath             # noqa: E402
from matplotlib.patches import PathPatch              # noqa: E402
from matplotlib.textpath import TextToPath            # noqa: E402

from . import style as S                               # noqa: E402

for _f in S.FONT_DIR.glob("*.ttf"):
    font_manager.fontManager.addfont(str(_f))
plt.rcParams["font.family"] = "Lato"
plt.rcParams["svg.fonttype"] = "none"

PALETTE = [S.PLUM, S.TEAL, S.GOLD, S.BLUE, S.ROSE, S.GREEN, S.CORAL, S.NAVY, S.SLATE]
NAMED = {"plum": S.PLUM, "teal": S.TEAL, "navy": S.NAVY, "rose": S.ROSE, "gold": S.GOLD,
         "blue": S.BLUE, "green": S.GREEN, "coral": S.CORAL, "red": S.RED, "slate": S.SLATE}
_TTP = TextToPath()
FS = 1.2   # global figure font scale (figures are shrunk to page width)
_WCACHE = {}


def C(h):
    return "#" + h


def colour(name, default=S.PLUM):
    if not name:
        return default
    name = name.strip().lower()
    if name in NAMED:
        return NAMED[name]
    if re.fullmatch(r"#?[0-9a-fA-F]{6}", name):
        return name.lstrip("#").upper()
    m = re.fullmatch(r"t(\d)", name)
    if m:
        return S.TOPIC_COLOURS[int(m.group(1))]
    return default


def clean(s):
    return re.sub(r"\*\*(.+?)\*\*|==(.+?)==|\^\^(.+?)\^\^", lambda m: next(g for g in m.groups() if g), s).strip()


# ------------------------------------------------------------ text metrics
def tw(s, size, bold=False, italic=False):
    key = (s, size, bold, italic)
    if key not in _WCACHE:
        fp = FontProperties(family="Lato", weight="bold" if bold else "normal",
                            style="italic" if italic else "normal", size=size * FS)
        w, _, _ = _TTP.get_text_width_height_descent(s, fp, ismath=False)
        _WCACHE[key] = w / 72.0
    return _WCACHE[key]


def wrap(s, width, size, bold=False, italic=False):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(trial, size, bold, italic) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def lh(size):
    return size * FS * 1.34 / 72.0


# ------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, W):
        self.W = W
        self.ops = []

    def rect(self, x, y, w, h, fc="FFFFFF", ec=None, lw=1.6, r=0.09, ls="-", alpha=1.0, z=1):
        self.ops.append(("rect", x, y, w, h, fc, ec, lw, r, ls, alpha, z))

    def text(self, x, y, s, size, col=S.INK, bold=False, italic=False, ha="left", va="top", z=5):
        self.ops.append(("text", x, y, s, size, col, bold, italic, ha, va, z))

    def line(self, pts, col=S.GREY, lw=1.4, arrow=False, ls="-", z=0, curve=False):
        self.ops.append(("line", pts, col, lw, arrow, ls, z, curve))

    def circle(self, x, y, r, fc, ec=None, lw=1.5, alpha=1.0, z=2):
        self.ops.append(("circle", x, y, r, fc, ec, lw, alpha, z))

    def poly(self, pts, fc, ec=None, lw=1.2, alpha=1.0, z=1):
        self.ops.append(("poly", pts, fc, ec, lw, alpha, z))

    def arc_arrow(self, p1, p2, col, rad=0.25, lw=1.6):
        self.ops.append(("arc", p1, p2, col, rad, lw))

    def render(self, H, path):
        fig = plt.figure(figsize=(self.W, H), dpi=200)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, self.W)
        ax.set_ylim(H, 0)
        ax.axis("off")
        for op in self.ops:
            k = op[0]
            if k == "rect":
                _, x, y, w, h, fc, ec, lw, r, ls, alpha, z = op
                ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                            fc=C(fc) if fc else "none", ec=C(ec) if ec else "none",
                                            lw=lw, ls=ls, alpha=alpha, zorder=z))
            elif k == "text":
                _, x, y, s, size, col, bold, italic, ha, va, z = op
                ax.text(x, y, s, fontsize=size * FS, color=C(col), fontweight="bold" if bold else "normal",
                        fontstyle="italic" if italic else "normal", ha=ha, va=va, zorder=z,
                        linespacing=1.25)
            elif k == "line":
                _, pts, col, lw, arrow, ls, z, curve = op
                if curve and len(pts) == 2:
                    (x1, y1), (x2, y2) = pts
                    mx = (x1 + x2) / 2
                    bez = MPath([(x1, y1), (mx, y1), (mx, y2), (x2, y2)],
                                [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
                    ax.add_patch(PathPatch(bez, fc="none", ec=C(col), lw=lw, zorder=z))
                elif arrow:
                    for a, b in zip(pts[:-2], pts[1:-1]):
                        ax.plot([a[0], b[0]], [a[1], b[1]], color=C(col), lw=lw, ls=ls, zorder=z,
                                solid_capstyle="round")
                    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>", mutation_scale=14,
                                                 color=C(col), lw=lw, zorder=z, shrinkA=0, shrinkB=0))
                else:
                    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=C(col), lw=lw, ls=ls,
                            zorder=z, solid_capstyle="round")
            elif k == "circle":
                _, x, y, r, fc, ec, lw, alpha, z = op
                ax.add_patch(Circle((x, y), r, fc=C(fc) if fc else "none", ec=C(ec) if ec else "none",
                                    lw=lw, alpha=alpha, zorder=z))
            elif k == "poly":
                _, pts, fc, ec, lw, alpha, z = op
                ax.add_patch(Polygon(pts, closed=True, fc=C(fc), ec=C(ec) if ec else "none", lw=lw,
                                     alpha=alpha, zorder=z))
            elif k == "arc":
                _, p1, p2, col, rad, lw = op
                ax.add_patch(FancyArrowPatch(p1, p2, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                             mutation_scale=14, color=C(col), lw=lw, zorder=3))
        fig.savefig(path, dpi=200, facecolor="white")
        plt.close(fig)


# ------------------------------------------------------------ text blocks
def measure_block(w, title, items, tsize=12, bsize=10.5, pad=0.13, bullets=True, text=None, tcentre=False):
    inner = w - 2 * pad
    tl = wrap(title, inner, tsize, bold=True) if title else []
    ind = 0.16 if bullets else 0.0
    body = [wrap(it, inner - ind, bsize) for it in items]
    tx = wrap(text, inner, bsize) if text else []
    h = pad + len(tl) * lh(tsize)
    if tl and (body or tx):
        h += 0.06
    h += len(tx) * lh(bsize) + sum(len(b) for b in body) * lh(bsize) + max(0, len(body) - 1) * 0.025
    return h + pad, (tl, tx, body)


def draw_block(cv, x, y, w, h, parts, col, fill="FFFFFF", edge=True, tsize=12, bsize=10.5, pad=0.13,
               bullets=True, tcol=None, bcol=S.INK, lw=1.8, centre=False, title_band=False):
    tl, tx, body = parts
    if title_band and tl:
        band_h = pad + len(tl) * lh(tsize) + 0.05
        cv.rect(x, y, w, h, fc=fill, ec=col if edge else None, lw=lw)
        cv.rect(x, y, w, band_h, fc=col, ec=col, lw=lw, z=2)
        cy = y + pad * 0.8
        for ln in tl:
            cv.text(x + w / 2 if centre else x + pad, cy, ln, tsize, "FFFFFF", bold=True,
                    ha="center" if centre else "left")
            cy += lh(tsize)
        cy = y + band_h + 0.08
    else:
        cv.rect(x, y, w, h, fc=fill, ec=col if edge else None, lw=lw)
        cy = y + pad
        for ln in tl:
            cv.text(x + w / 2 if centre else x + pad, cy, ln, tsize, tcol or col, bold=True,
                    ha="center" if centre else "left")
            cy += lh(tsize)
        if tl and (body or tx):
            cy += 0.06
    for ln in tx:
        cv.text(x + w / 2 if centre else x + pad, cy, ln, bsize, bcol, ha="center" if centre else "left")
        cy += lh(bsize)
    ind = 0.16 if bullets else 0.0
    for b in body:
        for i, ln in enumerate(b):
            if i == 0 and bullets:
                cv.text(x + pad, cy, "•", bsize, col, bold=True)
            cv.text(x + pad + ind, cy, ln, bsize, bcol)
            cy += lh(bsize)
        cy += 0.025


def split_items(lines):
    opts, items = {}, []
    for raw in lines:
        s = raw.rstrip()
        if not s.strip():
            continue
        if s.lstrip().startswith("@"):
            k, _, v = s.strip()[1:].partition(" ")
            if k in opts and k in ("ask", "note"):
                opts[k] += "\n" + v.strip()
            else:
                opts[k] = v.strip()
        else:
            items.append(s)
    return opts, items


def title_text(item):
    """'Title: a; b; c' -> ('Title', ['a','b','c'])."""
    t, sep, rest = clean(item).partition(":")
    if not sep:
        return t.strip(), []
    pts = [p.strip() for p in rest.split(";") if p.strip()]
    return t.strip(), [p[0].upper() + p[1:] for p in pts]


# ============================================================ templates
def fig_mindmap(lines, path):
    opts, items = split_items(lines)
    br = [title_text(i) for i in items]
    W, colw, cw = 11.0, 3.55, 2.75
    lx, cx, rx = 0.2, (11.0 - 2.75) / 2, 11.0 - 0.2 - 3.55
    nl = math.ceil(len(br) / 2)
    left, right = br[:nl], br[nl:]
    note_lines = wrap(clean(opts["note"]), W - 0.6, 11, italic=True) if opts.get("note") else []
    top = 0.2 + len(note_lines) * lh(11) + 0.18 if note_lines else 0.15
    cv = Canvas(W)
    for i, ln in enumerate(note_lines):
        cv.text(W / 2, 0.12 + i * lh(11), ln, 11, S.SLATE, italic=True, ha="center")

    def stack(col_items, start_idx):
        out, y = [], top
        for j, (t, pts) in enumerate(col_items):
            h, parts = measure_block(colw, t, pts, 12.5, 10.8)
            out.append((y, h, parts, PALETTE[(start_idx + j) % len(PALETTE)]))
            y += h + 0.17
        return out, y - 0.17

    L, lh_ = stack(left, 0)
    R, rh_ = stack(right, nl)
    body_h = max(lh_, rh_) - top
    asks = [clean(a) for a in opts.get("ask", "").split("\n") if a.strip()]
    head = "THE QUESTION ASKS"
    alines = [wrap(a, cw - 0.3, 11.5, bold=True) for a in asks]
    ch = 0.18 + lh(9) + 0.1 + sum(len(a) for a in alines) * lh(11.5) + 0.06 * len(alines) + 0.16
    total_h = max(top + body_h, top + ch) + 0.2
    cy = top + (max(body_h, ch) - ch) / 2
    # centre left columns if shorter
    for col, colH in ((L, lh_), (R, rh_)):
        off = (max(lh_, rh_) - colH) / 2
        for k in range(len(col)):
            y, h, parts, c = col[k]
            col[k] = (y + off, h, parts, c)
    cv.rect(cx, cy, cw, ch, fc=S.NAVY, ec=S.NAVY, r=0.14)
    yy = cy + 0.18
    cv.text(cx + cw / 2, yy, head, 9, "C7D2FE", bold=True, ha="center")
    yy += lh(9) + 0.1
    for a in alines:
        for ln in a:
            cv.text(cx + cw / 2, yy, ln, 11.5, "FFFFFF", bold=True, ha="center")
            yy += lh(11.5)
        yy += 0.06
    for y, h, parts, c in L:
        draw_block(cv, lx, y, colw, h, parts, c, tsize=12.5, bsize=10.8)
        cv.line([(lx + colw, y + h / 2), (cx, min(max(y + h / 2, cy + 0.2), cy + ch - 0.2))], c, 1.8, curve=True)
    for y, h, parts, c in R:
        draw_block(cv, rx, y, colw, h, parts, c, tsize=12.5, bsize=10.8)
        cv.line([(cx + cw, min(max(y + h / 2, cy + 0.2), cy + ch - 0.2)), (rx, y + h / 2)], c, 1.8, curve=True)
    cv.render(total_h, path)


def fig_flow(lines, path):
    opts, items = split_items(lines)
    br = [title_text(i) for i in items]
    single = colour(opts.get("colour"), None) if opts.get("colour") else None
    direction = opts.get("dir", "across")
    cv = Canvas(10.0 if direction == "across" else 8.0)
    if direction == "down":
        W, bw = 8.0, 6.2
        x = (W - bw) / 2
        y = 0.12
        for i, (t, pts) in enumerate(br):
            c = single or PALETTE[i % len(PALETTE)]
            h, parts = measure_block(bw, t, [], 13, 11.5, text=" ".join(pts) if pts else None)
            draw_block(cv, x, y, bw, h, parts, c, fill=S.tint(c, 0.9), centre=True, tsize=13, bsize=11.5)
            y += h
            if i < len(br) - 1:
                cv.line([(W / 2, y + 0.02), (W / 2, y + 0.33)], S.SLATE, 1.6, arrow=True)
                y += 0.36
        cv.render(y + 0.12, path)
        return
    W = 10.0
    per = int(opts.get("per", min(len(br), 4)))
    gap = 0.42
    bw = (W - 0.2 - (per - 1) * gap) / per
    rows = [br[i:i + per] for i in range(0, len(br), per)]
    y = 0.12
    idx = 0
    prev_end = None
    for r, row in enumerate(rows):
        meas = [measure_block(bw, t, [], 12.5, 11, text=" ".join(p) if p else None) for t, p in row]
        rh = max(m[0] for m in meas)
        for j, ((t, p), (h, parts)) in enumerate(zip(row, meas)):
            c = single or PALETTE[idx % len(PALETTE)]
            x = 0.1 + j * (bw + gap)
            draw_block(cv, x, y, bw, rh, parts, c, fill=S.tint(c, 0.9), tsize=12.5, bsize=11, centre=True)
            if j > 0:
                cv.line([(x - gap + 0.04, y + rh / 2), (x - 0.04, y + rh / 2)], S.SLATE, 1.6, arrow=True)
            elif prev_end is not None:
                px, py = prev_end
                cv.line([(px, py), (px, py + 0.2), (x + bw / 2, py + 0.2), (x + bw / 2, y - 0.02)], S.SLATE, 1.6,
                        arrow=True)
            idx += 1
        prev_end = (0.1 + (len(row) - 1) * (bw + gap) + bw / 2, y + rh + 0.02)
        y += rh + 0.45
    cv.render(y - 0.45 + 0.12, path)


def fig_timeline(lines, path):
    opts, raw = split_items(lines)
    events, groups, g = [], [], -1
    for s in raw:
        if s.startswith("=="):
            g += 1
            groups.append((len(events), clean(s.strip("= "))))
            continue
        yr, _, lab = clean(s).partition(":")
        events.append((yr.strip(), lab.strip(), max(g, 0)))
    layout = opts.get("layout", "horizontal" if len(events) <= 8 and not groups else "vertical")
    gcols = [PALETTE[i % len(PALETTE)] for i in range(max(1, len(groups)))]
    if layout == "vertical":
        W = 9.0
        cv = Canvas(W)
        ax_x, y = 1.75, 0.15
        gstart = {i: name for i, name in groups}
        y0 = y
        for i, (yr, lab, gi) in enumerate(events):
            c = gcols[gi] if groups else PALETTE[i % len(PALETTE)]
            if i in gstart:
                cv.rect(0.1, y, W - 0.2, lh(11) + 0.14, fc=S.tint(c, 0.85), ec=None, r=0.06)
                cv.text(0.25, y + 0.07, gstart[i], 11, c, bold=True)
                y += lh(11) + 0.24
            ll = wrap(lab, W - ax_x - 0.45, 10.5)
            h = max(len(ll) * lh(10.5), lh(11)) + 0.14
            cv.text(ax_x - 0.2, y, yr, 11, c, bold=True, ha="right")
            cv.circle(ax_x, y + lh(11) / 2, 0.07, c, "FFFFFF", 1.2, z=4)
            for k, ln in enumerate(ll):
                cv.text(ax_x + 0.25, y + k * lh(10.5), ln, 10.5, S.INK)
            y += h
        cv.line([(ax_x, y0), (ax_x, y - 0.1)], "CBD5E1", 2.2, z=0)
        cv.render(y + 0.1, path)
        return
    W = 11.0
    n = len(events)
    sp = (W - 0.6) / n
    lw_ = min(2 * sp - 0.2, 2.4)
    meas = []
    for yr, lab, gi in events:
        ll = wrap(lab, lw_, 10)
        meas.append((ll, lh(11.5) + len(ll) * lh(10) + 0.05))
    up = max([m[1] for i, m in enumerate(meas) if i % 2 == 0] or [0])
    dn = max([m[1] for i, m in enumerate(meas) if i % 2 == 1] or [0])
    axis_y = 0.15 + up + 0.35
    cv = Canvas(W)
    cv.line([(0.2, axis_y), (W - 0.2, axis_y)], "CBD5E1", 3, z=0)
    for i, ((yr, lab, gi), (ll, h)) in enumerate(zip(events, meas)):
        c = PALETTE[i % len(PALETTE)]
        x = 0.3 + sp * (i + 0.5)
        cv.circle(x, axis_y, 0.1, c, "FFFFFF", 1.5, z=4)
        if i % 2 == 0:
            ty = axis_y - 0.3 - h
            cv.line([(x, axis_y - 0.1), (x, axis_y - 0.28)], c, 1.4)
        else:
            ty = axis_y + 0.3
            cv.line([(x, axis_y + 0.1), (x, axis_y + 0.28)], c, 1.4)
        cv.text(x, ty, yr, 11.5, c, bold=True, ha="center")
        for k, ln in enumerate(ll):
            cv.text(x, ty + lh(11.5) + k * lh(10), ln, 10, S.INK, ha="center")
    cv.render(axis_y + 0.35 + dn + 0.15, path)


def fig_bars(lines, path):
    opts, items = split_items(lines)
    labels, vals, hi = [], [], []
    for s in items:
        star = s.rstrip().endswith("*")
        s = s.rstrip(" *")
        lab, _, v = s.rpartition(":")
        labels.append(clean(lab))
        vals.append(float(v.strip().replace("%", "")))
        hi.append(star)
    if "sort" in opts:
        order = sorted(range(len(vals)), key=lambda i: vals[i], reverse=True)
        labels, vals, hi = [labels[i] for i in order], [vals[i] for i in order], [hi[i] for i in order]
    base = colour(opts.get("colour"), S.TEAL)
    unit = opts.get("unit", "")
    n = len(labels)
    fig, ax = plt.subplots(figsize=(9, 0.46 * n + 0.9), dpi=200)
    ys = list(range(n))[::-1]
    ax.barh(ys, vals, color=[C(S.CORAL) if h else C(base) for h in hi], height=0.62, zorder=2)
    vmax = float(opts.get("max", max(vals) * 1.15 if vals else 1))
    ax.set_xlim(0, vmax)
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=10.5 * FS, color=C(S.INK))
    for y, v in zip(ys, vals):
        txt = (f"{v:g}{unit}")
        ax.text(v + vmax * 0.01, y, txt, va="center", fontsize=10 * FS, color=C(S.INK), fontweight="bold")
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", colors=C(S.SLATE), labelsize=9 * FS)
    ax.grid(axis="x", color="#E2E8F0", zorder=0)
    if opts.get("xlabel"):
        ax.set_xlabel(opts["xlabel"], fontsize=10 * FS, color=C(S.SLATE))
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor="white")
    plt.close(fig)


def fig_compare(lines, path):
    opts, items = split_items(lines)
    cols = []
    for s in items:
        if s.startswith("## "):
            cols.append([clean(s[3:]), []])
        elif cols:
            cols[-1][1].append(clean(s.lstrip("- ")))
    W = 10.0
    n = len(cols)
    gap = 0.5 if "vs" in opts and n == 2 else 0.22
    bw = (W - 0.2 - (n - 1) * gap) / n
    meas = [measure_block(bw, t, it, 12.5, 10.5) for t, it in cols]
    h = max(m[0] for m in meas) + 0.1
    cv = Canvas(W)
    for i, ((t, it), (hh, parts)) in enumerate(zip(cols, meas)):
        c = colour(opts.get(f"c{i+1}"), PALETTE[i % len(PALETTE)])
        x = 0.1 + i * (bw + gap)
        draw_block(cv, x, 0.1, bw, h, parts, c, fill=S.tint(c, 0.93), tsize=12.5, bsize=10.5,
                   title_band=True)
    if "vs" in opts and n == 2:
        cv.circle(W / 2, 0.1 + h / 2, 0.24, S.NAVY, "FFFFFF", 2, z=6)
        cv.text(W / 2, 0.1 + h / 2, opts["vs"] or "vs", 10.5, "FFFFFF", bold=True, ha="center", va="center", z=7)
    cv.render(h + 0.2, path)


def fig_tree(lines, path):
    opts, items = split_items(lines)
    root, kids = None, []
    for s in items:
        ind = len(s) - len(s.lstrip())
        t = s.strip()
        if root is None and not t.startswith("-"):
            root = clean(t)
        elif t.startswith("-") and ind == 0:
            tt, _, desc = clean(t[1:]).partition(":")
            kids.append([tt.strip(), desc.strip(), []])
        elif t.startswith("-") and kids:
            kids[-1][2].append(clean(t[1:]))
    W = 11.0
    per = int(opts.get("per", min(len(kids), 4)))
    rows = [kids[i:i + per] for i in range(0, len(kids), per)]
    gap = 0.22
    cv = Canvas(W)
    rw = min(5.5, W - 1)
    rh, rparts = measure_block(rw, root, [], 13.5, 10.5)
    cv.rect((W - rw) / 2, 0.1, rw, rh, fc=S.NAVY, ec=S.NAVY)
    draw_block(cv, (W - rw) / 2, 0.1, rw, rh, rparts, S.NAVY, fill=S.NAVY, tcol="FFFFFF", tsize=13.5, centre=True)
    y = 0.1 + rh + 0.5
    bus_y = 0.1 + rh + 0.25
    idx = 0
    for r, row in enumerate(rows):
        bw = (W - 0.2 - (per - 1) * gap) / per
        offset = (W - 0.2 - (len(row) * bw + (len(row) - 1) * gap)) / 2
        meas = [measure_block(bw, t, it, 11.5, 10, text=d or None) for t, d, it in row]
        hh = max(m[0] for m in meas) + 0.05
        xs = []
        for j, ((t, d, it), (h, parts)) in enumerate(zip(row, meas)):
            c = PALETTE[idx % len(PALETTE)]
            x = 0.1 + offset + j * (bw + gap)
            xs.append(x + bw / 2)
            draw_block(cv, x, y, bw, hh, parts, c, fill=S.tint(c, 0.93), tsize=11.5, bsize=10, title_band=True)
            cv.line([(x + bw / 2, y - 0.25 if r == 0 else y - 0.2), (x + bw / 2, y)], S.GREY, 1.5)
            idx += 1
        if r == 0:
            cv.line([(W / 2, 0.1 + rh), (W / 2, bus_y)], S.GREY, 1.5)
            cv.line([(min(xs), bus_y), (max(xs), bus_y)], S.GREY, 1.5)
        else:
            cv.line([(min(xs), y - 0.2), (max(xs), y - 0.2)], S.GREY, 1.5)
            cv.line([(W / 2, prev_bottom), (W / 2, y - 0.2)], S.GREY, 1.5)  # noqa: F821
        prev_bottom = y + hh  # noqa: F841
        y += hh + 0.45
    cv.render(y - 0.45 + 0.15, path)


def fig_grid(lines, path):
    opts, items = split_items(lines)
    br = [title_text(i) for i in items]
    W = 10.0
    cols = int(opts.get("cols", 3))
    gap = 0.2
    bw = (W - 0.2 - (cols - 1) * gap) / cols
    single = colour(opts.get("colour"), None) if opts.get("colour") else None
    cv = Canvas(W)
    y = 0.1
    for r in range(0, len(br), cols):
        row = br[r:r + cols]
        meas = [measure_block(bw, t, p if len(p) > 1 else [], 11.5, 10, text=p[0] if len(p) == 1 else None,
                              bullets=len(p) > 1) for t, p in row]
        hh = max(m[0] for m in meas)
        for j, ((t, p), (h, parts)) in enumerate(zip(row, meas)):
            c = single or PALETTE[(r + j) % len(PALETTE)]
            x = 0.1 + j * (bw + gap)
            draw_block(cv, x, y, bw, hh, parts, c, fill=S.tint(c, 0.92), tsize=11.5, bsize=10,
                       bullets=len(p) > 1, lw=1.4)
        y += hh + gap
    cv.render(y - gap + 0.1, path)


def fig_cycle(lines, path):
    opts, items = split_items(lines)
    br = [title_text(i) for i in items]
    n = len(br)
    W = 9.5
    R = 2.35 if n <= 5 else 2.6
    bw = 2.35
    meas = [measure_block(bw, t, [], 11, 9.8, text=" ".join(p) if p else None) for t, p in br]
    mh = max(m[0] for m in meas)
    cyc = 0.2 + mh / 2 + R
    cx = W / 2
    cv = Canvas(W)
    pts = []
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        pts.append((cx + R * math.cos(a) * 1.25, cyc + R * math.sin(a)))
    for i in range(n):
        p1, p2 = pts[i], pts[(i + 1) % n]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        d = math.hypot(dx, dy)
        s = 0.62
        a1 = (p1[0] + dx / d * s * 1.6, p1[1] + dy / d * s)
        a2 = (p2[0] - dx / d * s * 1.6, p2[1] - dy / d * s)
        cv.arc_arrow(a1, a2, S.GREY, rad=-0.2)
    for i, ((t, p), (h, parts)) in enumerate(zip(br, meas)):
        c = PALETTE[i % len(PALETTE)]
        x, y = pts[i]
        draw_block(cv, x - bw / 2, y - h / 2, bw, h, parts, c, fill=S.tint(c, 0.9), tsize=11, bsize=9.8, centre=True)
    if opts.get("centre"):
        cl = wrap(clean(opts["centre"]), 2.0, 12, bold=True)
        cv.circle(cx, cyc, 1.0, S.NAVY, None)
        yy = cyc - len(cl) * lh(12) / 2
        for ln in cl:
            cv.text(cx, yy, ln, 12, "FFFFFF", bold=True, ha="center")
            yy += lh(12)
    cv.render(cyc + R + mh / 2 + 0.2, path)


def fig_spectrum(lines, path):
    opts, items = split_items(lines)
    pts = []
    for s in items:
        p, _, lab = clean(s).partition(":")
        pts.append((float(p), lab.strip()))
    W = 10.0
    x0, x1 = 1.2, W - 1.2
    meas = [wrap(lab, 1.9, 10) for _, lab in pts]
    up = max([len(m) for i, m in enumerate(meas) if i % 2 == 0] or [1]) * lh(10) + 0.4
    dn = max([len(m) for i, m in enumerate(meas) if i % 2 == 1] or [1]) * lh(10) + 0.4
    ay = 0.15 + up + 0.1
    cv = Canvas(W)
    lc, rc = colour(opts.get("lc"), S.TEAL), colour(opts.get("rc"), S.PLUM)
    cv.line([(x0, ay), (x1, ay)], S.SLATE, 2.2, arrow=True)
    cv.line([(x1, ay), (x0, ay)], S.SLATE, 2.2, arrow=True)
    for k, (txt, x, c) in enumerate(((opts.get("left", ""), 0.6, lc), (opts.get("right", ""), W - 0.6, rc))):
        ll = wrap(clean(txt), 1.1, 11, bold=True)
        yy = ay - len(ll) * lh(11) / 2
        for ln in ll:
            cv.text(x, yy, ln, 11, c, bold=True, ha="center")
            yy += lh(11)
    for i, ((p, lab), ll) in enumerate(zip(pts, meas)):
        x = x0 + (x1 - x0) * p / 100
        c = PALETTE[i % len(PALETTE)]
        cv.circle(x, ay, 0.09, c, "FFFFFF", 1.4, z=4)
        if i % 2 == 0:
            ty = ay - 0.3 - len(ll) * lh(10)
            cv.line([(x, ay - 0.09), (x, ay - 0.26)], c, 1.2)
        else:
            ty = ay + 0.3
            cv.line([(x, ay + 0.09), (x, ay + 0.26)], c, 1.2)
        for k, ln in enumerate(ll):
            cv.text(x, ty + k * lh(10), ln, 10, S.INK, bold=(k == 0 and False), ha="center")
    cv.render(ay + dn + 0.15, path)


def fig_venn(lines, path):
    opts, items = split_items(lines)
    br = [title_text(i) for i in items]
    W = 9.0
    cv = Canvas(W)
    r = 1.75
    if len(br) == 2:
        centres = [(W / 2 - 1.1, 2.0), (W / 2 + 1.1, 2.0)]
        lab_off = [(-1.0, 0), (1.0, 0)]
        H = 4.1
        mid = (W / 2, 2.0)
    else:
        centres = [(W / 2 - 1.05, 1.95), (W / 2 + 1.05, 1.95), (W / 2, 3.7)]
        lab_off = [(-0.85, -0.45), (0.85, -0.45), (0, 0.8)]
        H = 5.65
        mid = (W / 2, 2.55)
    for i, ((t, p), (x, y), (ox, oy)) in enumerate(zip(br, centres, lab_off)):
        c = PALETTE[i % len(PALETTE)]
        cv.circle(x, y, r, c, None, alpha=0.16)
        cv.circle(x, y, r, None, c, 2.2)
        tl = wrap(t, 1.4, 11.5, bold=True)
        yy = y + oy - (len(tl) * lh(11.5) + len(p) * lh(9.5)) / 2
        for ln in tl:
            cv.text(x + ox, yy, ln, 11.5, c, bold=True, ha="center")
            yy += lh(11.5)
        for q in p:
            for ln in wrap(q, 1.4, 9.5):
                cv.text(x + ox, yy, ln, 9.5, S.INK, ha="center")
                yy += lh(9.5)
    if opts.get("centre"):
        cl = wrap(clean(opts["centre"]), 1.1, 10.5, bold=True)
        yy = mid[1] - len(cl) * lh(10.5) / 2
        for ln in cl:
            cv.text(mid[0], yy, ln, 10.5, S.NAVY, bold=True, ha="center")
            yy += lh(10.5)
    cv.render(H, path)


def fig_pyramid(lines, path):
    opts, items = split_items(lines)
    br = [title_text(i) for i in items]
    W = 9.0
    n = len(br)
    cv = Canvas(W)
    y = 0.1
    topw, botw = 2.6, 8.6
    hs = []
    for i, (t, p) in enumerate(br):
        wmid = topw + (botw - topw) * (i + 0.5) / n
        h, parts = measure_block(wmid * 0.72, t, [], 11.5, 10, text=" ".join(p) if p else None)
        hs.append((max(h, 0.62), parts))
    total = sum(h for h, _ in hs)
    for i, ((t, p), (h, parts)) in enumerate(zip(br, hs)):
        c = PALETTE[i % len(PALETTE)]
        yt = y
        wt = topw + (botw - topw) * (sum(hh for hh, _ in hs[:i]) / total)
        wb = topw + (botw - topw) * (sum(hh for hh, _ in hs[:i + 1]) / total)
        cv.poly([((W - wt) / 2, yt), ((W + wt) / 2, yt), ((W + wb) / 2, yt + h), ((W - wb) / 2, yt + h)],
                S.tint(c, 0.8), "FFFFFF", 2.5)
        tl, tx, _ = parts
        yy = yt + (h - (len(tl) * lh(11.5) + len(tx) * lh(10))) / 2
        for ln in tl:
            cv.text(W / 2, yy, ln, 11.5, c, bold=True, ha="center")
            yy += lh(11.5)
        for ln in tx:
            cv.text(W / 2, yy, ln, 10, S.INK, ha="center")
            yy += lh(10)
        y += h
    cv.render(y + 0.1, path)


def fig_matrix(lines, path):
    opts, items = split_items(lines)
    br = [title_text(i) for i in items][:4]
    W = 9.0
    cv = Canvas(W)
    x0, y0, s = 1.0, 0.2, (W - 1.3) / 2
    meas = [measure_block(s - 0.1, t, [], 11.5, 10, text=" ".join(p)) for t, p in br]
    hq = max(max(m[0] for m in meas) + 0.1, 1.5)
    for i, ((t, p), (h, parts)) in enumerate(zip(br, meas)):
        c = PALETTE[i % len(PALETTE)]
        x = x0 + (i % 2) * s
        y = y0 + (i // 2) * hq
        draw_block(cv, x + 0.05, y + 0.05, s - 0.1, hq - 0.1, parts, c, fill=S.tint(c, 0.9), centre=True)
    cv.line([(x0 - 0.1, y0 + 2 * hq + 0.1), (x0 - 0.1, y0 - 0.05)], S.SLATE, 1.8, arrow=True)
    cv.line([(x0 - 0.1, y0 + 2 * hq + 0.1), (x0 + 2 * s + 0.15, y0 + 2 * hq + 0.1)], S.SLATE, 1.8, arrow=True)
    cv.text(x0 + s, y0 + 2 * hq + 0.2, clean(opts.get("x", "")), 10.5, S.SLATE, bold=True, ha="center")
    yl = wrap(clean(opts.get("y", "")), 0.75, 10.5, bold=True)
    yy = y0 + hq - len(yl) * lh(10.5) / 2
    for ln in yl:
        cv.text(0.45, yy, ln, 10.5, S.SLATE, bold=True, ha="center")
        yy += lh(10.5)
    cv.render(y0 + 2 * hq + 0.55, path)


def fig_mapping(lines, path):
    opts, items = split_items(lines)
    pairs = []
    for s in items:
        l, _, r = s.partition("=>")
        pairs.append((clean(l), clean(r)))
    lefts = [p[0] for p in pairs]
    rights = []
    for _, r in pairs:
        if r not in rights:
            rights.append(r)
    W = 10.5
    lw_, rw_ = 4.0, 4.3
    lx, rx = 0.1, W - 0.1 - rw_
    cv = Canvas(W)
    top = 0.1
    if opts.get("left") or opts.get("right"):
        cv.text(lx + lw_ / 2, 0.1, clean(opts.get("left", "")), 11, S.SLATE, bold=True, ha="center")
        cv.text(rx + rw_ / 2, 0.1, clean(opts.get("right", "")), 11, S.SLATE, bold=True, ha="center")
        top = 0.45
    lm = [measure_block(lw_, l, [], 10.5, 10, pad=0.1) for l in lefts]
    rm = [measure_block(rw_, r, [], 11, 10, pad=0.12) for r in rights]
    gl, gr = 0.12, 0.2
    LH = sum(m[0] for m in lm) + gl * (len(lm) - 1)
    RH = sum(m[0] for m in rm) + gr * (len(rm) - 1)
    H = max(LH, RH)
    ly, ry = top + (H - LH) / 2, top + (H - RH) / 2
    rpos = {}
    for r, (h, parts) in zip(rights, rm):
        c = S.TOPIC_COLOURS[(len(rpos) + 1) % len(S.TOPIC_COLOURS)]
        draw_block(cv, rx, ry, rw_, h, parts, c, fill=c, tcol="FFFFFF", tsize=11, pad=0.12)
        rpos[r] = (ry + h / 2, c)
        ry += h + gr
    for (l, r), (h, parts) in zip(pairs, lm):
        yc, c = rpos[r]
        draw_block(cv, lx, ly, lw_, h, parts, c, fill=S.tint(c, 0.9), tsize=10.5, pad=0.1, lw=1.2)
        cv.line([(lx + lw_, ly + h / 2), (rx, yc)], c, 1.6, curve=True)
        ly += h + gl
    cv.render(top + H + 0.15, path)


def fig_heatmap(rows, cols, values, path, title=None, cmap_hex=S.PLUM, row_colours=None, fmt="{:g}",
                col_totals=True, row_totals=True):
    """Generic annotated heat map. values[r][c] numbers (0 shown blank)."""
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    data = np.array(values, dtype=float)
    nr, nc = data.shape
    cm = LinearSegmentedColormap.from_list("gs", ["#FFFFFF", C(S.tint(cmap_hex, 0.55)), C(cmap_hex)])
    fig_w = 1.9 + 0.62 * (nc + (1 if row_totals else 0))
    fig, ax = plt.subplots(figsize=(max(fig_w, 8.5), 0.5 * (nr + (1 if col_totals else 0)) + 1.0), dpi=200)
    vmax = max(1, data.max())
    ax.imshow(data, cmap=cm, vmin=0, vmax=vmax, aspect="auto", extent=(0, nc, nr, 0))
    for r in range(nr):
        for c in range(nc):
            v = data[r, c]
            if v:
                ax.text(c + 0.5, r + 0.5, fmt.format(v), ha="center", va="center", fontsize=10 * FS,
                        color="white" if v > vmax * 0.6 else C(S.INK), fontweight="bold")
    if row_totals:
        for r in range(nr):
            ax.text(nc + 0.5, r + 0.5, fmt.format(data[r].sum()), ha="center", va="center", fontsize=10.5 * FS,
                    color=C(S.NAVY), fontweight="bold")
        ax.text(nc + 0.5, -0.35, "Total", ha="center", va="center", fontsize=9.5 * FS, color=C(S.SLATE),
                fontweight="bold")
    if col_totals:
        for c in range(nc):
            ax.text(c + 0.5, nr + 0.45, fmt.format(data[:, c].sum()), ha="center", va="center", fontsize=9.5 * FS,
                    color=C(S.SLATE), fontweight="bold")
    ax.set_xlim(0, nc + (1 if row_totals else 0))
    ax.set_ylim(nr + (0.9 if col_totals else 0), 0)
    ax.set_xticks([c + 0.5 for c in range(nc)])
    ax.set_xticklabels(cols, fontsize=9.5 * FS, color=C(S.INK))
    ax.xaxis.tick_top()
    ax.set_yticks([r + 0.5 for r in range(nr)])
    ax.set_yticklabels(rows, fontsize=10 * FS, color=C(S.INK))
    if row_colours:
        for lbl, col in zip(ax.get_yticklabels(), row_colours):
            lbl.set_color(C(col))
            lbl.set_fontweight("bold")
    for x in range(nc + 1):
        ax.axvline(x, color="white", lw=2)
    for y in range(nr + 1):
        ax.axhline(y, color="white", lw=2)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor="white")
    plt.close(fig)


TEMPLATES = {
    "mindmap": fig_mindmap, "flow": fig_flow, "timeline": fig_timeline, "bars": fig_bars,
    "compare": fig_compare, "tree": fig_tree, "grid": fig_grid, "cycle": fig_cycle,
    "spectrum": fig_spectrum, "venn": fig_venn, "pyramid": fig_pyramid, "matrix": fig_matrix,
    "mapping": fig_mapping,
}


def render(kind, lines, doc_code):
    """Render a template figure into the cache; returns the PNG path (cached by content hash)."""
    S.CACHE.mkdir(parents=True, exist_ok=True)
    src = open(__file__, "rb").read()
    h = hashlib.md5((kind + "\n".join(lines)).encode() + hashlib.md5(src).digest()).hexdigest()[:12]
    path = S.CACHE / f"{doc_code}_{kind}_{h}.png"
    if not path.exists():
        TEMPLATES[kind](lines, str(path))
    return path
