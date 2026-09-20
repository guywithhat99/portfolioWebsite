import html, re

INK = '#14202E'
BODY = '#435063'
MUTED = '#66707D'
PAPER = '#FAF9F5'
PAPER2 = '#F0EEE6'
LINE = '#D9D6CA'
BLUE = '#1D5FD1'
BLUE_T = '#E1EBFA'
ORG = '#B34B0A'
ORG_T = '#FBE8D9'
GRN = '#1E6B45'
GRN_T = '#DDF0E3'
DBLUE = '#8DB4F5'
DAMB = '#F2A65A'
DPANEL = '#1E2E42'
DMUTED = '#9AA6B6'
SANS = "'IBM Plex Sans', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Courier New', monospace"


def esc(s):
    return html.escape(s, quote=False)


def P(text, size=32, color=BODY, weight=400, extra='', lh=1.4):
    return (f'<p style="font-size:{size}px; color:{color}; font-weight:{weight}; '
            f'line-height:{lh}; {extra}">{text}</p>')


def M(text, size=32, color=INK, weight=500, extra=''):
    return (f'<p style="font-family:{MONO}; font-size:{size}px; color:{color}; '
            f'font-weight:{weight}; line-height:1.3; {extra}">{text}</p>')


def div(inner, style=''):
    return f'<div style="{style}">{inner}</div>'


def row(inner, gap=24, extra=''):
    return div(inner, f'display:flex; gap:{gap}px; {extra}')


def col(inner, gap=16, extra=''):
    return div(inner, f'display:flex; flex-direction:column; gap:{gap}px; {extra}')


def card(inner, bg=PAPER2, border=LINE, pad=36, gap=14, extra=''):
    return div(inner, f'display:flex; flex-direction:column; gap:{gap}px; background:{bg}; '
                      f'border:2px solid {border}; border-radius:18px; padding:{pad}px; {extra}')


def spacer():
    return '<div style="flex:1"></div>'


def vline(h=40, c=INK, w=4):
    return f'<div style="width:{w}px; height:{h}px; background:{c}; align-self:center"></div>'


def hline(w=100, c=INK, h=4):
    return f'<div style="width:{w}px; height:{h}px; background:{c}"></div>'


def conn(x1, y1, x2, y2, color=INK, w=4, head='none', route=None, dash=False):
    r = f' route="{route}"' if route else ''
    d = ' border-style:dashed;' if dash else ''
    return (f'<x-connector x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" head="{head}"{r} '
            f'style="color:{color}; border-width:{w}px;{d}"></x-connector>')


def pin(inner, left, top, width=None, height=None, extra=''):
    w = f' width:{width}px;' if width is not None else ''
    h = f' height:{height}px;' if height is not None else ''
    return f'<div style="position:absolute; left:{left}px; top:{top}px;{w}{h} {extra}">{inner}</div>'


def pinp(text, left, top, width, size=28, color=BODY, weight=400, align='left', mono=False, extra=''):
    ff = f'font-family:{MONO}; ' if mono else ''
    return (f'<p style="position:absolute; left:{left}px; top:{top}px; width:{width}px; {ff}'
            f'font-size:{size}px; color:{color}; font-weight:{weight}; text-align:{align}; '
            f'line-height:1.3; {extra}">{text}</p>')


def host(inner, w=1664, h=640):
    return f'<div style="position:relative; width:{w}px; height:{h}px">{inner}</div>'


def pill(text, bg=PAPER2, color=INK, border=LINE, size=28, weight=500, pad='8px 20px', mono=False, extra=''):
    ff = f'font-family:{MONO}; ' if mono else ''
    return (f'<p style="{ff}font-size:{size}px; font-weight:{weight}; color:{color}; background:{bg}; '
            f'border:2px solid {border}; border-radius:999px; padding:{pad}; line-height:1.2; {extra}">{text}</p>')


def cell(txt, w=64, bg=PAPER2, color=INK, border=LINE, size=36, weight=500, pad=12, mono=True):
    ff = f'font-family:{MONO}; ' if mono else ''
    return (f'<p style="{ff}width:{w}px; padding:{pad}px 0; text-align:center; background:{bg}; '
            f'color:{color}; border:2px solid {border}; border-radius:8px; font-size:{size}px; '
            f'font-weight:{weight}; line-height:1.2">{txt}</p>')


def empty(w):
    return f'<div style="width:{w}px; flex:none"></div>'


NEUTRAL = (PAPER2, LINE, INK)
FB = (BLUE_T, BLUE, INK)
FO = (ORG_T, ORG, INK)
FG = (GRN_T, GRN, INK)
FD = (INK, INK, PAPER)


def bits(s, groups=None, w=64, size=36, gap=6, pad=12):
    """s: string of 0/1. groups: list of (count, (bg, border, color)); default neutral."""
    if groups is None:
        groups = [(len(s), NEUTRAL)]
    out = []
    i = 0
    for n, (bg, br, fg) in groups:
        for _ in range(n):
            out.append(cell(s[i], w=w, bg=bg, border=br, color=fg, size=size, pad=pad))
            i += 1
    return row(''.join(out), gap=gap)


def idx_row(hi, lo, w=64, gap=6, color=MUTED, size=24):
    out = []
    for k in range(hi, lo - 1, -1):
        out.append(f'<p style="width:{w}px; text-align:center; font-family:{MONO}; font-size:{size}px; '
                   f'color:{color}; line-height:1.2">{k}</p>')
    return row(''.join(out), gap=gap)


# ---------- code ----------
KW = r'\b(?:byte|void|return|int|uint32_t|uint16_t|int16_t|int32_t|int64_t|if|for)\b'
TOK = re.compile(r'(?P<c>//.*$)|(?P<s>"[^"]*")|(?P<n>0x[0-9A-Fa-f]+|0b[01]+|\b\d+\b)|(?P<k>' + KW + r')|(?P<i>#include)')


def colorize(line, dark=False):
    cols = {'c': DMUTED if dark else MUTED, 's': DAMB if dark else ORG,
            'n': DAMB if dark else ORG, 'k': DBLUE if dark else BLUE, 'i': DBLUE if dark else BLUE}
    out = []
    pos = 0
    for m in TOK.finditer(line):
        out.append(esc(line[pos:m.start()]))
        out.append(f'<span style="color:{cols[m.lastgroup]}">{esc(m.group(0))}</span>')
        pos = m.end()
    out.append(esc(line[pos:]))
    return ''.join(out)


def code(lines, size=28, hl=None, dark=False, bg=None, width=None, pad=28, hlbg=None, extra=''):
    """lines: list of str. hl: dict {line index: bg color}.

    Rendered as a real <pre>: the line break between rows is a literal newline
    and the indentation is real spaces, so selecting the block and pasting it
    into the Arduino IDE gives back exactly these lines. Highlighted rows use an
    inline-block so the tint still fills the width.
    """
    hl = hl or {}
    fg = PAPER if dark else INK
    pbg = bg or ('#0E1722' if dark else '#ECEAE0')
    bd = '#2C3E55' if dark else LINE
    rows = []
    for i, ln in enumerate(lines):
        body = colorize(ln, dark) if ln.strip() else ''
        if i in hl:
            body = (f'<span style="display:inline-block; min-width:100%; background:{hl[i]}; '
                    f'border-radius:6px">{body or "&#160;"}</span>')
        rows.append(body)
    w = f' width:{width}px;' if width else ''
    return ('<pre style="font-family:%s; font-size:%dpx; line-height:1.45; color:%s; background:%s; '
            'border:2px solid %s; border-radius:16px; padding:%dpx %dpx; margin:0; white-space:pre; '
            'overflow:auto;%s %s">%s</pre>' % (MONO, size, fg, pbg, bd, pad - 6, pad - 12, w, extra,
                                               '\n'.join(rows)))


# ---------- tables ----------
def table(rows, widths, size=32, color=BODY, head_color=INK, hl=None, extra=''):
    hl = hl or {}
    out = []
    for r, cells in enumerate(rows):
        tag = 'th' if r == 0 else 'td'
        tds = []
        for c, txt in enumerate(cells):
            style = 'text-align:left;'
            if r == 0:
                style += f' font-weight:600; color:{head_color};'
            if r == 0:
                style += f' width:{widths[c]}%;'
            tds.append(f'<{tag} style="{style}">{txt}</{tag}>')
        bgs = f' style="background:{hl[r]}"' if r in hl else ''
        out.append(f'<tr{bgs}>' + ''.join(tds) + '</tr>')
    return (f'<table style="font-family:{SANS}; font-size:{size}px; color:{color}; {extra}">'
            + ''.join(out) + '</table>')


# ---------- placeholder for screenshots ----------
def ph(w, h, what, where, dark=False):
    bg = DPANEL if dark else PAPER2
    fg = PAPER if dark else INK
    sub = DMUTED if dark else BODY
    ac = DAMB if dark else ORG
    return div(
        P('SCREENSHOT TO ADD', 24, ac, 600, 'letter-spacing:3px') +
        P(what, 40, fg, 600, 'text-align:center; line-height:1.2') +
        P(where, 28, sub, 400, 'text-align:center'),
        f'width:{w}px; height:{h}px; flex:none; display:flex; flex-direction:column; align-items:center; '
        f'justify-content:center; gap:16px; background:{bg}; border:4px dashed {ac}; border-radius:20px; padding:40px')


# ---------- waveform ----------
def wave(slots, P_, start=False, stop=False, ack=(), bands=False, dark=False, labels=True, gutter=128):
    hiS, loS, hiD, loD = 34, 94, 176, 236
    H = 270
    scl_c = DMUTED if dark else MUTED
    sda_c = DBLUE if dark else BLUE
    n = len(slots)
    x0 = P_ if start else 0
    xe = x0 + n * P_
    W = xe + (P_ if stop else 0)
    r = 6
    yD = lambda v: hiD if v else loD

    def ramp(pts, x, y1, y2):
        pts.append((round(x), y1))
        pts.append((round(x + r), y2))

    # SCL
    sp = [(0, hiS if start else loS)]
    if start:
        ramp(sp, x0 - 0.2 * P_, hiS, loS)
    for k in range(n):
        s = x0 + k * P_
        ramp(sp, s + 0.25 * P_, loS, hiS)
        ramp(sp, s + 0.75 * P_, hiS, loS)
    if stop:
        ramp(sp, xe + 0.3 * P_, loS, hiS)
        sp.append((W, hiS))
    else:
        sp.append((xe, loS))
    # SDA
    if start:
        dp = [(0, hiD)]
        ramp(dp, 0.45 * P_, hiD, loD)
        cur = 0
    else:
        cur = slots[0]
        dp = [(0, yD(cur))]
    for k, v in enumerate(slots):
        s = x0 + k * P_
        if v != cur:
            ramp(dp, s + 0.05 * P_, yD(cur), yD(v))
            cur = v
    if stop:
        assert cur == 0
        ramp(dp, xe + 0.6 * P_, loD, hiD)
        dp.append((W, hiD))
    else:
        dp.append((xe, yD(cur)))
    path = lambda pts: 'M ' + ' L '.join(f'{x},{y}' for x, y in pts)
    parts = []
    if bands:
        for k in range(n):
            s = x0 + k * P_
            parts.append(f'<rect x="{round(s + 0.25 * P_)}" y="0" width="{round(0.5 * P_)}" height="{H}" fill="{BLUE_T}"/>')
    for k in ack:
        s = x0 + k * P_
        parts.append(f'<rect x="{s}" y="0" width="{P_}" height="{H}" fill="{ORG_T}"/>')
    parts.append(f'<path d="{path(sp)}" fill="none" stroke="{scl_c}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
    parts.append(f'<path d="{path(dp)}" fill="none" stroke="{sda_c}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
    for k in ack:
        s = x0 + k * P_
        parts.append(f'<path d="M {round(s + 0.05 * P_ + r)},{loD} L {s + P_},{loD}" fill="none" stroke="{ORG if not dark else DAMB}" stroke-width="7" stroke-linecap="round"/>')
    svg = (f'<svg aria-label="Waveform of the SCL clock and the SDA data line" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">' + ''.join(parts) + '</svg>')
    lab = ''
    if labels:
        lab = (pinp('SCL', 0, (hiS + loS) // 2 - 14, 110, 28, scl_c, 700, mono=True) +
               pinp('SDA', 0, (hiD + loD) // 2 - 14, 110, 28, sda_c, 700, mono=True))
    hst = (f'<div style="position:relative; display:flex; width:{gutter + W}px">'
           f'{empty(gutter)}{svg}{lab}</div>')
    return hst, W, x0


def mini_edge(kind, dark=False):
    """START or STOP snippet, 700 x 230."""
    scl_c = DMUTED if dark else MUTED
    sda_c = DBLUE if dark else BLUE
    if kind == 'start':
        scl = 'M 0,40 L 450,40 L 456,100 L 620,100'
        sda = 'M 0,140 L 290,140 L 296,200 L 620,200'
    else:
        scl = 'M 0,100 L 180,100 L 186,40 L 620,40'
        sda = 'M 0,200 L 320,200 L 326,140 L 620,140'
    svg = (f'<svg aria-label="{kind.upper()} condition: SDA changes while SCL is high" width="620" height="230" viewBox="0 0 620 230">'
           f'<path d="{scl}" fill="none" stroke="{scl_c}" stroke-width="5" stroke-linejoin="round"/>'
           f'<path d="{sda}" fill="none" stroke="{sda_c}" stroke-width="5" stroke-linejoin="round"/></svg>')
    lab = (pinp('SCL', 0, 56, 100, 28, scl_c, 700, mono=True) + pinp('SDA', 0, 156, 100, 28, sda_c, 700, mono=True))
    return f'<div style="position:relative; display:flex; width:730px">{empty(110)}{svg}{lab}</div>'


# ---------- slide builders ----------
def footer(tag, dark=False):
    c = DMUTED if dark else MUTED
    return (f'<p style="position:absolute; left:128px; bottom:64px; width:1200px; font-size:24px; color:{c}; '
            f'letter-spacing:1px; line-height:1.2">{esc(tag)}</p>'
            f'<p style="position:absolute; right:128px; bottom:64px; width:200px; text-align:right; font-size:24px; '
            f'color:{c}; line-height:1.2">@@N@@</p>')


def light(id, title, body, notes, tag, bg=PAPER, gap=40):
    return (f'<section id="{id}" data-transition="fade" style="background:{bg}; color:{BODY}; font-family:{SANS}; '
            f'padding:128px 128px 160px; display:flex; flex-direction:column; gap:{gap}px">'
            f'<h2 style="font-family:{SANS}; font-size:64px; font-weight:600; line-height:1.1; color:{INK}">{esc(title)}</h2>'
            f'{body}{footer(tag)}<aside>{esc(notes)}</aside></section>')


def dark_turn(id, title, steps, notes, tag, answer=None, minutes='', label='YOU SHOULD SEE'):
    st = []
    for i, s in enumerate(steps, 1):
        st.append(row(
            f'<p style="width:56px; flex:none; text-align:center; background:{DAMB}; color:{INK}; font-size:32px; '
            f'font-weight:700; border-radius:50%; padding:6px 0; line-height:1.2">{i}</p>'
            + P(s, 36, PAPER, 400, 'flex:1; line-height:1.35'), gap=28, extra='align-items:flex-start'))
    ans = ''
    if answer:
        ans = (f'<div data-build-in="fade" style="position:absolute; left:128px; top:800px; width:1664px; padding:22px 32px; '
               f'background:{DPANEL}; border:2px solid {DAMB}; border-radius:16px; display:flex; gap:28px; align-items:center">'
               f'<p style="width:280px; flex:none; font-size:24px; color:{DAMB}; font-weight:600; letter-spacing:3px; '
               f'line-height:1.3">{label}</p>'
               f'<p style="flex:1; font-size:36px; color:{PAPER}; line-height:1.3">{answer}</p></div>')
    head = row(P('YOUR TURN', 24, DAMB, 600, 'letter-spacing:4px') +
               (P(minutes, 24, DMUTED, 500, 'letter-spacing:2px') if minutes else ''), gap=28, extra='align-items:baseline')
    return (f'<section id="{id}" data-transition="fade" style="background:{INK}; color:{PAPER}; font-family:{SANS}; '
            f'padding:128px 128px 160px; display:flex; flex-direction:column; gap:36px">'
            f'{head}'
            f'<h2 style="font-family:{SANS}; font-size:64px; font-weight:600; line-height:1.1; color:{PAPER}">{esc(title)}</h2>'
            f'{col("".join(st), gap=22, extra="")}'
            f'{ans}{footer(tag, True)}<aside>{esc(notes)}</aside></section>')


def section_slide(id, num, title, blurb, notes, tag):
    return (f'<section id="{id}" data-transition="push" style="background:{PAPER2}; color:{BODY}; font-family:{SANS}; '
            f'padding:128px 128px 160px; display:flex; flex-direction:column; justify-content:center; gap:24px">'
            f'<p style="font-family:{MONO}; font-size:24px; font-weight:700; letter-spacing:6px; color:{BLUE}">MODULE</p>'
            f'<p style="font-family:{MONO}; font-size:240px; font-weight:700; line-height:1; color:{INK}">{num}</p>'
            f'<h1 style="font-family:{SANS}; font-size:96px; font-weight:600; line-height:1.1; color:{INK}">{esc(title)}</h1>'
            f'<p style="font-size:40px; color:{BODY}; line-height:1.35; width:1200px">{esc(blurb)}</p>'
            f'<aside>{esc(notes)}</aside></section>')
