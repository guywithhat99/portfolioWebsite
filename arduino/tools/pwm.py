"""PWM diagrams: the wave itself, and duty cycle against brightness."""
BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; BLUE="#1d4ed8"; GREEN="#1a7f4b"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"

def wave(pts,col,w=3):
    return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="miter"/>'

# ---------- 1. PWM wave with a real time axis ----------
W,H=900,470
X0,X1=120,840          # plot area
MS=3                    # show three 1 ms cycles
PX=(X1-X0)/MS           # pixels per millisecond
DUTY=0.75
HI,LO=120,270           # y of 5 V and 0 V
AX=310                  # y of the time axis
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
t=lambda ms: X0+ms*PX

# voltage axis
s.append(f'<line x1="{X0}" y1="{HI-30}" x2="{X0}" y2="{AX}" stroke="{DIM}" stroke-width="1.5"/>')
for y,lab,col in ((HI,"5 V",GREEN),(LO,"0 V",DIM)):
    s.append(f'<line x1="{X0-6}" y1="{y}" x2="{X0}" y2="{y}" stroke="{DIM}" stroke-width="1.5"/>')
    s.append(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{col}" stroke-width="1" stroke-dasharray="4,6" opacity=".45"/>')
    s.append(f'<text x="{X0-14}" y="{y+6}" fill="{col}" font-family="{F}" font-size="17" text-anchor="end">{lab}</text>')
s.append(f'<text x="{X0-70}" y="{(HI+LO)/2}" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle" transform="rotate(-90,{X0-70},{(HI+LO)/2})">voltage</text>')

# time axis
s.append(f'<line x1="{X0}" y1="{AX}" x2="{X1+18}" y2="{AX}" stroke="{DIM}" stroke-width="1.5"/>')
s.append(f'<polygon points="{X1+26},{AX} {X1+14},{AX-6} {X1+14},{AX+6}" fill="{DIM}"/>')
for i in range(MS*4+1):
    ms=i/4; x=t(ms); major=(i%4==0)
    s.append(f'<line x1="{x:.1f}" y1="{AX}" x2="{x:.1f}" y2="{AX+(10 if major else 5)}" stroke="{DIM}" stroke-width="{1.5 if major else 1}"/>')
    if major:
        s.append(f'<text x="{x:.1f}" y="{AX+30}" fill="{TEXT}" font-family="{F}" font-size="16" text-anchor="middle">{int(ms)} ms</text>')
        s.append(f'<line x1="{x:.1f}" y1="{HI-20}" x2="{x:.1f}" y2="{AX}" stroke="{LINE}" stroke-width="1"/>')
s.append(f'<text x="{(X0+X1)/2}" y="{AX+58}" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">time</text>')

# shaded on-time and the wave
pts=[]
for c in range(MS):
    a0=t(c); a1=t(c+DUTY); a2=t(c+1)
    s.append(f'<rect x="{a0:.1f}" y="{HI}" width="{a1-a0:.1f}" height="{LO-HI}" fill="{ORANGE}" opacity=".13"/>')
    pts += [(a0,LO),(a0,HI),(a1,HI),(a1,LO),(a2,LO)]
s.append(wave(" ".join(f"{x:.1f},{y}" for x,y in pts),ORANGE,3.5))

# on / off brackets over the first cycle
def bracket(x1,x2,y,label,col):
    s.append(f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="{col}" stroke-width="1.8"/>')
    for x in (x1,x2): s.append(f'<line x1="{x:.1f}" y1="{y-6}" x2="{x:.1f}" y2="{y+6}" stroke="{col}" stroke-width="1.8"/>')
    s.append(f'<text x="{(x1+x2)/2:.1f}" y="{y-12}" fill="{col}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">{label}</text>')
bracket(t(0),t(DUTY),HI-28,"on 0.75 ms",ORANGE)
bracket(t(DUTY),t(1),HI-28,"off 0.25 ms",DIM)
bracket(t(1),t(2),HI-70,"one cycle: 1 ms",TEAL)

s.append(f'<text x="{W/2}" y="{H-50}" fill="{TEXT}" font-family="{S}" font-size="19" font-weight="700" text-anchor="middle">On for 75% of every cycle. That is a 75% duty cycle.</text>')
AVG=LO-(LO-HI)*DUTY
s.append(f'<line x1="{X0}" y1="{AVG:.1f}" x2="{X1}" y2="{AVG:.1f}" stroke="{TEAL}" stroke-width="3" stroke-dasharray="10,7"/>')
s.append(f'<line x1="{X0-6}" y1="{AVG:.1f}" x2="{X0}" y2="{AVG:.1f}" stroke="{TEAL}" stroke-width="1.5"/>')
s.append(f'<text x="{X0-14}" y="{AVG+6:.1f}" fill="{TEAL}" font-family="{F}" font-size="17" font-weight="700" text-anchor="end">3.75 V</text>')
s.append(f'<rect x="{t(1.375)-44:.1f}" y="{AVG-30:.1f}" width="88" height="22" rx="4" fill="{BG}" opacity=".9"/>')
s.append(f'<text x="{t(1.375):.1f}" y="{AVG-13:.1f}" fill="{TEAL}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">average</text>')
s.append(f'<text x="{W/2}" y="{H-22}" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">The pin is only ever at 5 V or 0 V, but averaged over time it acts like 3.75 V.</text>')
s.append('</svg>')
open('content/img/pwm-wave.svg','w').write("\n".join(s))

# ---------- 2. duty cycle against brightness ----------
W,H=900,450
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
   f'<rect width="{W}" height="{H}" fill="{BG}"/>']
rows=[(0,"0","always off"),(64,"64","dim"),(128,"128","half"),(191,"191","brighter"),(255,"255","always on")]
X0,X1=250,690; y=72; STEP=76; AMP=26
s.append(f'<text x="{X0-22}" y="34" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="end">analogWrite</text>')
s.append(f'<text x="{X0-22}" y="52" fill="{TEAL}" font-family="{S}" font-size="14" text-anchor="end">average</text>')
s.append(f'<text x="{X0}" y="34" fill="{DIM}" font-family="{S}" font-size="16">what the pin does</text>')
s.append(f'<text x="{X1+48}" y="34" fill="{DIM}" font-family="{S}" font-size="16">the LED</text>')
for v,lab,desc in rows:
    d=v/255.0
    hi, lo = y-AMP, y+AMP
    s.append(f'<rect x="{X0}" y="{hi-9}" width="{X1-X0}" height="{2*AMP+18}" fill="#ffffff" opacity=".55" rx="5"/>')
    s.append(f'<line x1="{X0}" y1="{lo}" x2="{X1}" y2="{lo}" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<text x="{X0-22}" y="{y+7}" fill="{ORANGE}" font-family="{F}" font-size="19" font-weight="700" text-anchor="end">{lab}</text>')
    n=4; seg=(X1-X0)/n; pts=[]
    for i in range(n):
        a=X0+i*seg; b=a+seg*d
        if d<=0:
            pts += [(a,lo),(a+seg,lo)]
        elif d>=1:
            pts += [(a,hi),(a+seg,hi)]
        else:
            pts += [(a,lo),(a,hi),(b,hi),(b,lo),(a+seg,lo)]
    s.append(wave(" ".join(f"{x:.0f},{yy:.0f}" for x,yy in pts),ORANGE,2.5))
    avg_y = lo-(lo-hi)*d
    s.append(f'<line x1="{X0}" y1="{avg_y:.1f}" x2="{X1}" y2="{avg_y:.1f}" stroke="{TEAL}" stroke-width="2.5" stroke-dasharray="8,6"/>')
    volts = 5*d
    r = round(volts/0.05)*0.05
    vtxt = f"{r:.0f} V" if abs(r-round(r))<1e-9 else "≈ " + f"{r:.2f}".rstrip('0').rstrip('.') + " V"
    s.append(f'<text x="{X0-22}" y="{y+29}" fill="{TEAL}" font-family="{F}" font-size="15" font-weight="700" text-anchor="end">{vtxt}</text>')
    s.append(f'<circle cx="{X1+72}" cy="{y}" r="19" fill="{ORANGE}" opacity="{max(d,0.05):.2f}"/>')
    s.append(f'<circle cx="{X1+72}" cy="{y}" r="19" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    s.append(f'<text x="{X1+100}" y="{y+6}" fill="{DIM}" font-family="{S}" font-size="15">{desc}</text>')
    y+=STEP
s.append(f'<text x="{W/2:.0f}" y="{H-16}" fill="{DIM}" font-family="{S}" font-size="17" text-anchor="middle">More time on means a higher average, and a brighter light.</text>')
s.append('</svg>')
open('content/img/pwm-duty.svg','w').write("\n".join(s))
print("wrote pwm-wave.svg and pwm-duty.svg")
