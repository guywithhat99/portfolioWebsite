"""Potentiometer: a resistor track split in two by a sliding wiper."""
BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; RED="#b4241f"; GREEN="#1a7f4b"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
TOP,BOT=110,330
POS=[(0.2,"8","2"),(0.5,"5","5"),(0.8,"2","8")]   # fraction from bottom, R_upper, R_lower

def track(s,cx,frac,rup,rlo,supply):
    wy=BOT-(BOT-TOP)*frac
    # upper section
    s.append(f'<rect x="{cx-27}" y="{TOP}" width="54" height="{wy-TOP:.0f}" fill="#d9c79a" stroke="#8a7f6a" stroke-width="1.5" rx="4"/>')
    # lower section
    s.append(f'<rect x="{cx-27}" y="{wy:.0f}" width="54" height="{BOT-wy:.0f}" fill="#c0a970" stroke="#8a7f6a" stroke-width="1.5" rx="4"/>')
    s.append(f'<text x="{cx-40}" y="{(TOP+wy)/2+6:.0f}" fill="{TEXT}" font-family="{F}" font-size="16" text-anchor="end">{rup} k</text>')
    s.append(f'<text x="{cx-40}" y="{(wy+BOT)/2+6:.0f}" fill="{TEXT}" font-family="{F}" font-size="16" text-anchor="end">{rlo} k</text>')
    # wiper
    s.append(f'<polygon points="{cx+27},{wy:.0f} {cx+45},{wy-10:.0f} {cx+45},{wy+10:.0f}" fill="{TEAL}"/>')
    s.append(f'<line x1="{cx+45}" y1="{wy:.0f}" x2="{cx+78}" y2="{wy:.0f}" stroke="{TEAL}" stroke-width="3"/>')
    return wy

# ---------- 1. what is inside ----------
W,H=900,460
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="44" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Inside is one resistor track with a sliding contact on it</text>')
for i,(frac,rup,rlo) in enumerate(POS):
    cx=190+i*260
    wy=track(s,cx,frac,rup,rlo,False)
    s.append(f'<line x1="{cx-27}" y1="{TOP}" x2="{cx-52}" y2="{TOP}" stroke="{DIM}" stroke-width="2.5"/>')
    s.append(f'<line x1="{cx-27}" y1="{BOT}" x2="{cx-52}" y2="{BOT}" stroke="{DIM}" stroke-width="2.5"/>')
    s.append(f'<text x="{cx}" y="{BOT+40}" fill="{TEXT}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">{rup} k + {rlo} k</text>')
s.append(f'<text x="{190}" y="{TOP-14}" fill="{DIM}" font-family="{S}" font-size="14" text-anchor="middle">outer leg</text>')
s.append(f'<text x="{190+78}" y="{BOT-(BOT-TOP)*0.2-18:.0f}" fill="{TEAL}" font-family="{S}" font-size="14" text-anchor="middle">middle leg</text>')
s.append(f'<text x="{W/2}" y="{H-42}" fill="{TEXT}" font-family="{S}" font-size="18" font-weight="700" text-anchor="middle">The contact splits the track into two resistances.</text>')
s.append(f'<text x="{W/2}" y="{H-16}" fill="{DIM}" font-family="{S}" font-size="17" text-anchor="middle">Turn the knob and one grows as the other shrinks. They always add up to 10 k.</text>')
s.append('</svg>')
open('content/img/pot-inside.svg','w').write("\n".join(s)); print("pot-inside.svg")

# ---------- 2. used as a divider ----------
W,H=900,470
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="44" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Put a voltage across the ends and the contact taps off part of it</text>')
for i,(frac,rup,rlo) in enumerate(POS):
    cx=190+i*260
    wy=track(s,cx,frac,rup,rlo,True)
    s.append(f'<line x1="{cx-27}" y1="{TOP}" x2="{cx-62}" y2="{TOP}" stroke="{RED}" stroke-width="3"/>')
    s.append(f'<text x="{cx-68}" y="{TOP+6}" fill="{RED}" font-family="{F}" font-size="15" text-anchor="end">5 V</text>')
    s.append(f'<line x1="{cx-27}" y1="{BOT}" x2="{cx-62}" y2="{BOT}" stroke="{DIM}" stroke-width="3"/>')
    s.append(f'<text x="{cx-68}" y="{BOT+6}" fill="{DIM}" font-family="{F}" font-size="15" text-anchor="end">0 V</text>')
    v=5*frac; adc=int(1023*frac)
    s.append(f'<text x="{cx+84}" y="{wy-5:.0f}" fill="{TEAL}" font-family="{F}" font-size="17" font-weight="700">{v:.1f} V</text>')
    s.append(f'<text x="{cx+84}" y="{wy+16:.0f}" fill="{DIM}" font-family="{F}" font-size="14">reads {adc}</text>')
    s.append(f'<text x="{cx}" y="{BOT+42}" fill="{DIM}" font-family="{F}" font-size="15" text-anchor="middle">{rlo} of 10</text>')
s.append(f'<text x="{W/2}" y="{H-42}" fill="{TEXT}" font-family="{S}" font-size="18" font-weight="700" text-anchor="middle">The voltage on the middle leg follows the ratio, not the resistance.</text>')
s.append(f'<text x="{W/2}" y="{H-16}" fill="{DIM}" font-family="{S}" font-size="17" text-anchor="middle">Two thirds of the way up the track means two thirds of the voltage.</text>')
s.append('</svg>')
open('content/img/pot-divider.svg','w').write("\n".join(s)); print("pot-divider.svg")
