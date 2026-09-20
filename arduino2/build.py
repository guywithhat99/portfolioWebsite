#!/usr/bin/env python3
"""Build arduino-new/index.html.

Default content is the generated deck in src/. Anything listed in overrides.py
replaces the generated slide with the same id.

    python3 build.py
"""
import os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))
import s1, s2, s3, s4, s5, s6, s7
from overrides import OVERRIDES

slides = []
for m in (s1, s2, s3, s4, s5, s6, s7):
    slides += m.slides()

ids = [i for i, _ in slides]
assert len(ids) == len(set(ids)), 'duplicate slide ids'
missing = set(OVERRIDES) - set(ids)
assert not missing, f'override for unknown slide: {missing}'

swapped = []
body = []
for n, (i, h) in enumerate(slides, 1):
    if i in OVERRIDES:
        h = OVERRIDES[i]()
        swapped.append(i)
    h = h.replace('@@N@@', str(n))
    h = h.replace('<aside>', '<aside class="notes">')
    h = h.replace('data-build-in="fade"', 'class="fragment"')
    h = h.replace('data-transition="push"', 'data-transition="slide"')
    assert h.count('<section') == 1 and h.startswith(f'<section id="{i}"'), i
    for ch in ('—', '–'):
        if ch in h:
            print('  dash in', i)
    body.append(h)

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>I2C from zero to hero</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">

<style>
  html, body { background:#FAF9F5; }
  .reveal { font-family:'IBM Plex Sans', Arial, sans-serif; }
  .reveal .slides { text-align:left; }
  .reveal .slides section { width:1920px; height:1080px; box-sizing:border-box; overflow:hidden; }
  .reveal .slides section > * { box-sizing:border-box; }
  .reveal p, .reveal h1, .reveal h2, .reveal h3 { margin:0; }
  .reveal img { border:0; box-shadow:none; }
  .reveal table { border-collapse:collapse; width:100%; }
  .reveal th, .reveal td { padding:10px 16px; border-bottom:2px solid #D9D6CA; vertical-align:top; }
  .reveal .progress { color:#1D5FD1; height:4px; }
  .reveal .controls { color:#1D5FD1; }
  @page { size:1920px 1080px; margin:0; }
</style>
</head>
<body>
<div class="reveal"><div class="slides">
'''

TAIL = '''
</div></div>

<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/notes/notes.js"></script>
<script>
/* <x-connector> and <x-shape> are Claude Design elements. Render them in a browser. */
class XConnector extends HTMLElement {
  connectedCallback() {
    if (this._done) return; this._done = true;
    const a = n => parseFloat(this.getAttribute(n));
    const x1 = a('x1'), y1 = a('y1'), x2 = a('x2'), y2 = a('y2');
    const cs = getComputedStyle(this);
    const col = cs.color || '#14202E';
    const w = parseFloat(cs.borderTopWidth) || 4;
    const dashed = cs.borderTopStyle === 'dashed';
    const head = (this.getAttribute('head') || 'none') !== 'none';
    const pad = Math.max(w * 4, 14);
    const minX = Math.min(x1, x2) - pad, minY = Math.min(y1, y2) - pad;
    const W = Math.abs(x2 - x1) + pad * 2, H = Math.abs(y2 - y1) + pad * 2;
    const sx = x1 - minX, sy = y1 - minY;
    let ex = x2 - minX, ey = y2 - minY;
    const ang = Math.atan2(ey - sy, ex - sx);
    if (head) { ex -= Math.cos(ang) * w * 2.2; ey -= Math.sin(ang) * w * 2.2; }
    const NS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', W); svg.setAttribute('height', H);
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`); svg.setAttribute('aria-hidden', 'true');
    const ln = document.createElementNS(NS, 'line');
    ln.setAttribute('x1', sx); ln.setAttribute('y1', sy);
    ln.setAttribute('x2', ex); ln.setAttribute('y2', ey);
    ln.setAttribute('stroke', col); ln.setAttribute('stroke-width', w);
    ln.setAttribute('stroke-linecap', 'round');
    if (dashed) ln.setAttribute('stroke-dasharray', `${w * 2.5} ${w * 2.5}`);
    svg.appendChild(ln);
    if (head) {
      const s = w * 3.2, tip = document.createElementNS(NS, 'polygon');
      const bx = x2 - minX - Math.cos(ang) * s, by = y2 - minY - Math.sin(ang) * s;
      const nx = -Math.sin(ang) * s * 0.55, ny = Math.cos(ang) * s * 0.55;
      tip.setAttribute('points', `${x2 - minX},${y2 - minY} ${bx + nx},${by + ny} ${bx - nx},${by - ny}`);
      tip.setAttribute('fill', col); svg.appendChild(tip);
    }
    Object.assign(this.style, { position:'absolute', left:minX+'px', top:minY+'px',
      width:W+'px', height:H+'px', border:'0', pointerEvents:'none' });
    this.appendChild(svg);
  }
}
customElements.define('x-connector', XConnector);

class XShape extends HTMLElement {
  connectedCallback() {
    if (this._done) return; this._done = true;
    if ((this.getAttribute('kind') || '') !== 'arrow-right') return;
    const cs = getComputedStyle(this);
    const col = cs.backgroundColor;
    const w = parseFloat(cs.width) || 80, h = parseFloat(cs.height) || 40;
    const shaft = h * 0.34, headW = Math.min(h * 0.9, w * 0.45);
    this.style.background = 'transparent';
    const NS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', w); svg.setAttribute('height', h);
    svg.setAttribute('viewBox', `0 0 ${w} ${h}`); svg.setAttribute('aria-hidden', 'true');
    const p = document.createElementNS(NS, 'path');
    const m = (h - shaft) / 2;
    p.setAttribute('d', `M0,${m} H${w - headW} V0 L${w},${h / 2} L${w - headW},${h} V${m + shaft} H0 Z`);
    p.setAttribute('fill', col); svg.appendChild(p);
    this.appendChild(svg);
  }
}
customElements.define('x-shape', XShape);

Reveal.initialize({
  hash:true, controls:true, controlsLayout:'edges', progress:true,
  slideNumber:false, transition:'fade', transitionSpeed:'fast',
  center:false, margin:0, width:1920, height:1080,
  plugins:[ RevealNotes ]
});
</script>
</body>
</html>
'''

out = os.path.join(HERE, 'index.html')
open(out, 'w').write(HEAD + '\n'.join(body) + TAIL)
print(f'{len(body)} slides, {os.path.getsize(out)//1024} KB')
print(f'overridden: {", ".join(swapped)}')
