"""PWM diagrams: the wave itself, and duty cycle against brightness."""
BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; BLUE="#1d4ed8"; GREEN="#1a7f4b"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"

def wave(pts,col,w=3):
    return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="miter"/>'

# ---------- 1. one annotated cycle ----------
W,H=900,400
X0,X1=110,800; HI,LO=110,250
duty=0.72
c1=X0+(X1-X0)/2
on1=X0+(c1-X0)*duty; on2=c1+(X1-c1)*duty
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
   f'<rect width="{W}" height="{H}" fill="{BG}"/>']
for y,lab,col in ((HI,"5 V",GREEN),(LO,"0 V",DIM)):
    s.append(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{col}" stroke-width="1" stroke-dasharray="4,5" opacity=".5"/>')
    s.append(f'<text x="{X0-14}" y="{y+6}" fill="{col}" font-family="{F}" font-size="17" text-anchor="end">{lab}</text>')
s.append(f'<rect x="{X0}" y="{HI}" width="{on1-X0:.0f}" height="{LO-HI}" fill="{ORANGE}" opacity=".13"/>')
s.append(f'<rect x="{c1}" y="{HI}" width="{on2-c1:.0f}" height="{LO-HI}" fill="{ORANGE}" opacity=".13"/>')
s.append(wave(f"{X0},{LO} {X0},{HI} {on1:.0f},{HI} {on1:.0f},{LO} {c1:.0f},{LO} {c1:.0f},{HI} {on2:.0f},{HI} {on2:.0f},{LO} {X1},{LO}",ORANGE))
mid=(X0+on1)/2
s.append(f'<text x="{mid:.0f}" y="{(HI+LO)/2+7:.0f}" fill="{ORANGE}" font-family="{S}" font-size="19" font-weight="700" text-anchor="middle">on</text>')
s.append(f'<text x="{(on1+c1)/2:.0f}" y="{(HI+LO)/2+7:.0f}" fill="{DIM}" font-family="{S}" font-size="19" font-weight="700" text-anchor="middle">off</text>')
s.append(f'<line x1="{X0}" y1="292" x2="{c1}" y2="292" stroke="{BLUE}" stroke-width="1.6"/>')
for x in (X0,c1): s.append(f'<line x1="{x}" y1="286" x2="{x}" y2="298" stroke="{BLUE}" stroke-width="1.6"/>')
s.append(f'<text x="{(X0+c1)/2:.0f}" y="315" fill="{BLUE}" font-family="{S}" font-size="17" text-anchor="middle">one cycle</text>')
s.append(f'<text x="{W/2:.0f}" y="360" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">On for 72% of every cycle. That is a duty cycle of 72%.</text>')
s.append(f'<text x="{W/2:.0f}" y="386" fill="{DIM}" font-family="{S}" font-size="17" text-anchor="middle">The pin is still only ever at 5 V or 0 V.</text>')
s.append('</svg>')
open('content/img/pwm-wave.svg','w').write("\n".join(s))

# ---------- 2. duty cycle against brightness ----------
W,H=900,450
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
   f'<rect width="{W}" height="{H}" fill="{BG}"/>']
rows=[(0,"0","always off"),(64,"64","dim"),(128,"128","half"),(191,"191","brighter"),(255,"255","always on")]
X0,X1=250,690; y=72; STEP=76; AMP=26
s.append(f'<text x="{X0-22}" y="34" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="end">analogWrite</text>')
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
    s.append(f'<circle cx="{X1+72}" cy="{y}" r="19" fill="{ORANGE}" opacity="{max(d,0.05):.2f}"/>')
    s.append(f'<circle cx="{X1+72}" cy="{y}" r="19" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    s.append(f'<text x="{X1+100}" y="{y+6}" fill="{DIM}" font-family="{S}" font-size="15">{desc}</text>')
    y+=STEP
s.append(f'<text x="{W/2:.0f}" y="{H-16}" fill="{DIM}" font-family="{S}" font-size="17" text-anchor="middle">More time on means a brighter light. The voltage never changes.</text>')
s.append('</svg>')
open('content/img/pwm-duty.svg','w').write("\n".join(s))
print("wrote pwm-wave.svg and pwm-duty.svg")
