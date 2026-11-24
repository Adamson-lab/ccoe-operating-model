"""Tiny SVG architecture-diagram toolkit with built-in text-overflow checks."""
import math
import textwrap
from xml.sax.saxutils import escape as esc

FONT = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
PAL = {  # fill, stroke, text
    "navy": ("#0B1F3A", "#0B1F3A", "#FFFFFF"), "blue": ("#E8F1FF", "#2563EB", "#0B1F3A"),
    "teal": ("#E3F8F5", "#0D9488", "#0B2F2B"), "green": ("#E8F8EE", "#16A34A", "#0B2E17"),
    "amber": ("#FFF4DC", "#D97706", "#3D2300"), "red": ("#FDECEC", "#DC2626", "#450A0A"),
    "purple": ("#F2EBFF", "#7C3AED", "#2E1065"), "gray": ("#F1F5F9", "#64748B", "#0F172A"),
}
CB, CR = 0.64, 0.59  # conservative char widths (bold / regular) in em


def tw(s, fs, bold=False):
    return len(s) * fs * (CB if bold else CR)


def cols(x0, total, n, gap):
    w = (total - gap * (n - 1)) / n
    return [x0 + i * (w + gap) for i in range(n)], w


def B(x, y, w, h):
    return {"x": x, "y": y, "w": w, "h": h}


def anchor(b, side, f=0.5):
    return {"r": (b["x"] + b["w"], b["y"] + b["h"] * f), "l": (b["x"], b["y"] + b["h"] * f),
            "t": (b["x"] + b["w"] * f, b["y"]), "b": (b["x"] + b["w"] * f, b["y"] + b["h"])}[side]


def route(p, q, sa, sb, m=None):
    (x1, y1), (x2, y2) = p, q
    if sa in "rl" and sb in "rl":
        if sa != sb:
            if abs(y1 - y2) < .5:
                return [p, q]
            mx = m if m is not None else (x1 + x2) / 2
            return [p, (mx, y1), (mx, y2), q]
        ex = (max(x1, x2) + 34) if sa == "r" else (min(x1, x2) - 34)
        return [p, (ex, y1), (ex, y2), q]
    if sa in "tb" and sb in "tb":
        if sa != sb:
            if abs(x1 - x2) < .5:
                return [p, q]
            my = m if m is not None else (y1 + y2) / 2
            return [p, (x1, my), (x2, my), q]
        ey = (max(y1, y2) + 34) if sa == "b" else (min(y1, y2) - 34)
        return [p, (x1, ey), (x2, ey), q]
    if sa in "rl":
        return [p, (x2, y1), q]
    return [p, (x1, y2), q]


class Dia:
    def __init__(s, num, title, sub, w=1600, h=900, domain="Architecture"):
        s.num, s.title, s.sub, s.w, s.h, s.domain = num, title, sub, w, h, domain
        s.o, s.warn, s.legend = [], [], []
        s.shapes, s.labels, s.paths = [], [], []
        if tw(title, 22, True) > w - 330:
            s.warn.append(f"title too long: {title}")

    # ---- primitives
    def add(s, x):
        s.o.append(x)

    def text(s, x, y, t, fs=12, bold=False, fill="#0F172A", anchor="start", ls=None, halo=False):
        extra = f' letter-spacing="{ls}"' if ls else ""
        if halo:
            extra += ' stroke="#F8FAFC" stroke-width="4" paint-order="stroke" stroke-linejoin="round"'
        s.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="{700 if bold else 400}" fill="{fill}" text-anchor="{anchor}"{extra}>{esc(t)}</text>')

    def _wrap(s, t, width, fs, bold):
        cpl = max(int(width / (fs * (CB if bold else CR))), 4)
        out = []
        for para in str(t).split("\n"):
            out += textwrap.wrap(para, cpl, break_long_words=False) or [""]
        return out

    def _label(s, b, title, sub, kind, fs, accent=True, name=""):
        f, st, tx = PAL[kind]
        inner = b["w"] - (34 if accent else 20)
        tl = s._wrap(title, inner, fs, True) if title else []
        sl = s._wrap(sub, inner, fs - 1.5, False) if sub else []
        lh, slh = fs + 4, fs + 2.5
        total = len(tl) * lh + len(sl) * slh + (5 if sl and tl else 0)
        if total > b["h"] - 8:
            s.warn.append(f"[{s.num:02d}] vertical overflow in '{title}' ({total:.0f}>{b['h']-8:.0f})")
        for l in tl:
            if tw(l, fs, True) > inner + 4:
                s.warn.append(f"[{s.num:02d}] horizontal overflow '{l}'")
        for l in sl:
            if tw(l, fs - 1.5) > inner + 4:
                s.warn.append(f"[{s.num:02d}] horizontal overflow '{l}'")
        cx = b["x"] + b["w"] / 2 + (4 if accent else 0)
        y = b["y"] + (b["h"] - total) / 2 + fs
        tc = tx
        sc = "#CBD5E1" if kind == "navy" else "#475569"
        for l in tl:
            s.text(cx, y, l, fs, True, tc, "middle")
            y += lh
        if sl and tl:
            y += 5
        for l in sl:
            s.text(cx, y - 1, l, fs - 1.5, False, sc, "middle")
            y += slh

    # ---- shapes
    def box(s, x, y, w, h, title, sub=None, kind="blue", fs=12):
        f, st, tx = PAL[kind]
        s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="9" fill="{f}" stroke="{st}" stroke-width="1.5" filter="url(#sh)"/>')
        if kind != "navy":
            s.add(f'<path d="M{x+9:.1f},{y+12:.1f} V{y+h-12:.1f}" stroke="{st}" stroke-width="4" stroke-linecap="round"/>')
        b = B(x, y, w, h)
        s.shapes.append((x, y, w, h, title))
        s._label(b, title, sub, kind, fs, accent=(kind != "navy"))
        return b

    def pill(s, x, y, w, h, title, sub=None, kind="gray", fs=12):
        f, st, tx = PAL[kind]
        s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" fill="{f}" stroke="{st}" stroke-width="1.8" filter="url(#sh)"/>')
        b = B(x, y, w, h)
        s.shapes.append((x, y, w, h, title))
        s._label(b, title, sub, kind, fs, accent=False)
        return b

    def group(s, x, y, w, h, label, kind="gray", dash=True):
        st = PAL[kind][1]
        d = ' stroke-dasharray="7 5"' if dash else ""
        s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="14" fill="{st}" fill-opacity="0.055" stroke="{st}" stroke-width="1.3"{d}/>')
        if tw(label.upper(), 11, True) > w - 30:
            s.warn.append(f"[{s.num:02d}] group label too long: {label}")
        s.text(x + 16, y + 22, label.upper(), 11, True, st, ls="0.8")
        return B(x, y, w, h)

    def cyl(s, x, y, w, h, title, sub=None, kind="teal", fs=12):
        f, st, tx = PAL[kind]
        ry = 9
        s.add(f'<path d="M{x:.1f},{y+ry:.1f} L{x:.1f},{y+h-ry:.1f} A{w/2:.1f},{ry} 0 0 0 {x+w:.1f},{y+h-ry:.1f} L{x+w:.1f},{y+ry:.1f} Z" fill="{f}" stroke="{st}" stroke-width="1.5" filter="url(#sh)"/>')
        s.add(f'<ellipse cx="{x+w/2:.1f}" cy="{y+ry:.1f}" rx="{w/2:.1f}" ry="{ry}" fill="{f}" stroke="{st}" stroke-width="1.5"/>')
        s.shapes.append((x, y, w, h, title))
        b = B(x, y + 2 * ry - 4, w, h - 2 * ry - 4)
        s._label(b, title, sub, kind, fs, accent=False)
        return B(x, y, w, h)

    def diamond(s, cx, cy, w, h, title, kind="amber", fs=11):
        f, st, tx = PAL[kind]
        pts = f"{cx:.1f},{cy-h/2:.1f} {cx+w/2:.1f},{cy:.1f} {cx:.1f},{cy+h/2:.1f} {cx-w/2:.1f},{cy:.1f}"
        s.add(f'<polygon points="{pts}" fill="{f}" stroke="{st}" stroke-width="1.8" filter="url(#sh)"/>')
        s.shapes.append((cx - w / 2, cy - h / 2, w, h, title))
        b = B(cx - w * 0.3, cy - h * 0.3, w * 0.6, h * 0.6)
        s._label(b, title, None, kind, fs, accent=False)
        return B(cx - w / 2, cy - h / 2, w, h)

    def chevron(s, x, y, w, h, title, kind="blue", first=False, fs=12):
        st = PAL[kind][1]
        n = 0 if first else 18
        pts = f"{x:.1f},{y:.1f} {x+w-18:.1f},{y:.1f} {x+w:.1f},{y+h/2:.1f} {x+w-18:.1f},{y+h:.1f} {x:.1f},{y+h:.1f} {x+n:.1f},{y+h/2:.1f}"
        s.add(f'<polygon points="{pts}" fill="{st}" stroke="#FFFFFF" stroke-width="2"/>')
        s.shapes.append((x, y, w, h, title))
        b = B(x + 22, y, w - 44, h)
        s._label(b, title, None, "navy", fs, accent=False)
        return B(x, y, w, h)

    def badge(s, x, y, n, kind="navy"):
        st = PAL[kind][1]
        s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{st}" stroke="#fff" stroke-width="2"/>')
        s.text(x, y + 4, str(n), 11, True, "#FFFFFF", "middle")

    def chip(s, x, y, t, kind="gray", fs=10.5):
        f, st, tx = PAL[kind]
        w = tw(t, fs, True) + 16
        s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="20" rx="10" fill="{f}" stroke="{st}" stroke-width="1"/>')
        s.text(x + w / 2, y + 14, t, fs, True, tx, "middle")
        return w

    # ---- connectors
    def _lab(s, x, y, label, st):
        w = tw(label, 10.5, True) + 14
        s.labels.append((x - w / 2, y - 9, w, 18, label))
        s.add(f'<rect x="{x-w/2:.1f}" y="{y-9:.1f}" width="{w:.1f}" height="18" rx="9" fill="#FFFFFF" stroke="{st}" stroke-width="1"/>')
        s.text(x, y + 4, label, 10.5, True, st, "middle")

    def arrow(s, pts, kind="gray", dash=False, label=None, lp=None, w=1.8, both=False):
        st = PAL[kind][1]
        s.paths.append(pts)
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        da = ' stroke-dasharray="6 4"' if dash else ""
        ms = ' marker-start="url(#ar-%s)"' % kind if both else ""
        s.add(f'<path d="{d}" fill="none" stroke="{st}" stroke-width="{w}"{da} stroke-linejoin="round" marker-end="url(#ar-{kind})"{ms}/>')
        if label:
            if lp is None:
                best = max(range(len(pts) - 1), key=lambda i: abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]))
                lp = ((pts[best][0] + pts[best + 1][0]) / 2, (pts[best][1] + pts[best + 1][1]) / 2)
            s._lab(lp[0], lp[1], label, st) if False else s._lab(lp[0], lp[1], label, st)

    def conn(s, a, b, sa, sb, fa=.5, fb=.5, m=None, **kw):
        s.arrow(route(anchor(a, sa, fa), anchor(b, sb, fb), sa, sb, m), **kw)

    def curve(s, p1, p2, kind="gray", w=1.4, op=1.0, c1=None, c2=None, head=True, dash=False):
        st = PAL[kind][1]
        dx = (p2[0] - p1[0]) * .5
        c1 = c1 or (p1[0] + dx, p1[1])
        c2 = c2 or (p2[0] - dx, p2[1])
        da = ' stroke-dasharray="6 4"' if dash else ""
        mk = f' marker-end="url(#ar-{kind})"' if head else ""
        s.add(f'<path d="M{p1[0]:.1f},{p1[1]:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="{st}" stroke-width="{w}" stroke-opacity="{op}"{da}{mk}/>')
        return ((p1[0] + 3 * c1[0] + 3 * c2[0] + p2[0]) / 8, (p1[1] + 3 * c1[1] + 3 * c2[1] + p2[1]) / 8)

    def check(s):
        W, H = s.w, s.h
        sh = s.shapes
        for i, a in enumerate(sh):
            if a[0] < 0 or a[1] < 64 or a[0] + a[2] > W or a[1] + a[3] > H - 30:
                s.warn.append(f"[{s.num:02d}] '{a[4]}' outside canvas")
            for b in sh[i + 1:]:
                if a[0] < b[0] + b[2] - 1 and b[0] < a[0] + a[2] - 1 and a[1] < b[1] + b[3] - 1 and b[1] < a[1] + a[3] - 1:
                    s.warn.append(f"[{s.num:02d}] overlap: '{a[4]}' x '{b[4]}'")
        for pts in s.paths:
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                lo_x, hi_x, lo_y, hi_y = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
                for b in sh:
                    if lo_x < b[0] + b[2] - 3 and hi_x > b[0] + 3 and lo_y < b[1] + b[3] - 3 and hi_y > b[1] + 3:
                        s.warn.append(f"[{s.num:02d}] arrow crosses '{b[4]}'")
        for l in s.labels:
            for b in sh:
                if l[0] < b[0] + b[2] and b[0] < l[0] + l[2] and l[1] < b[1] + b[3] and b[1] < l[1] + l[3]:
                    s.warn.append(f"[{s.num:02d}] label '{l[4]}' overlaps '{b[4]}'")
            if l[0] < 4 or l[0] + l[2] > W - 4:
                s.warn.append(f"[{s.num:02d}] label '{l[4]}' off canvas")

    # ---- output
    def svg(s):
        W, H = s.w, s.h
        s.check()
        mk = "".join(f'<marker id="ar-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{v[1]}"/></marker>' for k, v in PAL.items())
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">'
                f'<defs>{mk}<filter id="sh" x="-5%" y="-5%" width="110%" height="120%"><feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-color="#0F172A" flood-opacity="0.13"/></filter>'
                '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#CBD5E1" fill-opacity="0.55"/></pattern>'
                '<linearGradient id="hd" x1="0" x2="1"><stop offset="0" stop-color="#0B1F3A"/><stop offset="1" stop-color="#1E3A8A"/></linearGradient></defs>'
                f'<rect width="{W}" height="{H}" fill="#F8FAFC"/><rect width="{W}" height="{H}" fill="url(#dots)"/>')
        hdr = (f'<rect width="{W}" height="62" fill="url(#hd)"/>'
               f'<text x="28" y="30" font-size="22" font-weight="700" fill="#FFFFFF">{esc(s.title)}</text>'
               f'<text x="28" y="50" font-size="12.5" fill="#B6C4DB">{esc(s.sub)}</text>'
               f'<rect x="{W-168}" y="17" width="140" height="28" rx="14" fill="#FFFFFF" fill-opacity="0.12" stroke="#FFFFFF" stroke-opacity="0.35"/>'
               f'<text x="{W-98}" y="36" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">DIAGRAM {s.num:02d} / 20</text>')
        if tw(s.sub, 12.5) > W - 220:
            s.warn.append(f"[{s.num:02d}] subtitle too long")
        foot = [f'<line x1="25" y1="{H-30}" x2="{W-25}" y2="{H-30}" stroke="#CBD5E1"/>',
                f'<text x="25" y="{H-12}" font-size="11" fill="#64748B">Cloud Center of Excellence · Operating Model Repository · github.com/Adamson-lab</text>']
        lx = W - 25
        for kind, lab in reversed(s.legend):
            lw = tw(lab, 11) + 28
            lx -= lw
            foot.append(f'<rect x="{lx:.1f}" y="{H-24}" width="12" height="12" rx="3" fill="{PAL[kind][0]}" stroke="{PAL[kind][1]}" stroke-width="1.5"/>')
            foot.append(f'<text x="{lx+18:.1f}" y="{H-13}" font-size="11" fill="#334155">{esc(lab)}</text>')
        return head + "".join(s.o) + hdr + "".join(foot) + "</svg>"
