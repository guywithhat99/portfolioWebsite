import math
BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; RED="#b4241f"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
W,H=900,500
X0=210; PXMS=118          # pixels per millisecond
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="42" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">The width of the pulse is the message</text>')
rows=[(1.0,0,"0"),(1.5,90,"90"),(2.0,180,"180")]
y=130
for ms,ang,lab in rows:
    hi,lo=y-30,y+16
    s.append(f'<text x="{X0-22}" y="{y-2}" fill="{ORANGE}" font-family="{F}" font-size="18" font-weight="700" text-anchor="end">{ms} ms</text>')
    w=ms*PXMS
    s.append(f'<rect x="{X0}" y="{hi}" width="{w:.0f}" height="{lo-hi}" fill="{ORANGE}" opacity=".14"/>')
    s.append(f'<polyline points="{X0},{lo} {X0},{hi} {X0+w:.0f},{hi} {X0+w:.0f},{lo} {X0+w+70:.0f},{lo}" fill="none" stroke="{ORANGE}" stroke-width="3"/>')
    s.append(f'<line x1="{X0+w+70:.0f}" y1="{lo}" x2="{X0+300:.0f}" y2="{lo}" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="7,6" opacity=".55"/>')
    # width marker
    s.append(f'<line x1="{X0}" y1="{hi-14}" x2="{X0+w:.0f}" y2="{hi-14}" stroke="{TEAL}" stroke-width="1.6"/>')
    for xx in (X0, X0+w):
        s.append(f'<line x1="{xx:.0f}" y1="{hi-19}" x2="{xx:.0f}" y2="{hi-9}" stroke="{TEAL}" stroke-width="1.6"/>')
    # horn
    hx,hy=700,y-4
    s.append(f'<path d="M {hx-44} {hy} A 44 44 0 0 1 {hx+44} {hy}" fill="none" stroke="{LINE}" stroke-width="8" stroke-linecap="round"/>')
    s.append(f'<circle cx="{hx}" cy="{hy}" r="13" fill="#fff" stroke="{TEXT}" stroke-width="2.5"/>')
    a=math.radians(180-ang)
    s.append(f'<line x1="{hx}" y1="{hy}" x2="{hx+46*math.cos(a):.1f}" y2="{hy-46*math.sin(a):.1f}" stroke="{TEAL}" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<text x="{hx+72}" y="{hy+6}" fill="{TEAL}" font-family="{S}" font-size="17" font-weight="700">{lab} deg</text>')
    y+=120
s.append(f'<text x="{X0+210}" y="{y-72}" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">then nothing, until the next pulse 20 ms later</text>')
s.append(f'<text x="{W/2}" y="{H-40}" fill="{TEXT}" font-family="{S}" font-size="18" font-weight="700" text-anchor="middle">A pulse every 20 ms, and its width says where to go.</text>')
s.append(f'<text x="{W/2}" y="{H-14}" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">The servo holds that position on its own until you tell it another one.</text>')
s.append('</svg>')
open('content/img/servo-pulse.svg','w').write("\n".join(s)); print("servo-pulse.svg")

# ---- open loop vs closed loop ----
W,H=900,380
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
def box(x,y,w,h,label,col,sub=None):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#fff" stroke="{col}" stroke-width="2.5"/>')
    s.append(f'<text x="{x+w/2}" y="{y+h/2+(0 if not sub else -6)}" fill="{col}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">{label}</text>')
    if sub: s.append(f'<text x="{x+w/2}" y="{y+h/2+16}" fill="{DIM}" font-family="{S}" font-size="13" text-anchor="middle">{sub}</text>')
def arrow(x1,y1,x2,y2,col):
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2-10}" y2="{y2}" stroke="{col}" stroke-width="2.5"/>')
    s.append(f'<polygon points="{x2},{y2} {x2-11},{y2-7} {x2-11},{y2+7}" fill="{col}"/>')
s.append(f'<text x="230" y="46" fill="{TEXT}" font-family="{S}" font-size="18" font-weight="700" text-anchor="middle">The DC motor</text>')
box(70,90,150,62,"your code",RED); arrow(220,121,300,121,RED); box(300,90,150,62,"motor spins",RED)
s.append(f'<text x="230" y="196" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">You set how hard to push.</text>')
s.append(f'<text x="230" y="218" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">Nothing knows where it ended up.</text>')
s.append(f'<text x="670" y="46" fill="{TEXT}" font-family="{S}" font-size="18" font-weight="700" text-anchor="middle">The servo</text>')
box(505,90,140,62,"your code",GREEN); arrow(645,121,700,121,GREEN); box(700,90,140,62,"servo",GREEN,"and its own circuit")
s.append(f'<path d="M 770 152 C 770 200, 575 200, 575 156" fill="none" stroke="{GREEN}" stroke-width="2.5"/>')
s.append(f'<polygon points="575,152 568,164 582,164" fill="{GREEN}"/>')
s.append(f'<text x="672" y="222" fill="{GREEN}" font-family="{S}" font-size="15" font-weight="700" text-anchor="middle">it checks where it actually is</text>')
s.append(f'<text x="670" y="250" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">You set where to go, and it gets itself there.</text>')
s.append(f'<line x1="460" y1="70" x2="460" y2="290" stroke="{LINE}" stroke-width="1.5"/>')
s.append(f'<text x="{W/2}" y="330" fill="{TEXT}" font-family="{S}" font-size="18" font-weight="700" text-anchor="middle">The servo has a sensor inside it. The motor does not.</text>')
s.append(f'<text x="{W/2}" y="358" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">That is the whole difference, and it is why one holds position and the other cannot.</text>')
s.append('</svg>')
open('content/img/servo-vs-motor.svg','w').write("\n".join(s)); print("servo-vs-motor.svg")
