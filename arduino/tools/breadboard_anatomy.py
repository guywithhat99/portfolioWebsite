"""Diagram: how breadboard holes connect.

Standard orientation. Landscape board, gap running left to right through the
middle, each column of five holes joined underneath, power rails top and bottom.
"""
BG="#f5f3ed"; BOARD="#e9e5da"; EDGE="#cfc8b8"; HOLE="#fff"; RIM="#b9b1a0"
TEXT="#1b1e22"; DIM="#5d6670"; TEAL="#00767d"; ORANGE="#c4551a"
RED="#b4241f"; BLUE="#1d4ed8"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"

COLS=20; P=30; X0=95; Y0=150; GAP=P*1.7
ROWS_T="abcde"; ROWS_B="fghij"
ry={}
for i,r in enumerate(ROWS_T): ry[r]=Y0+i*P
base=Y0+4*P+GAP
for i,r in enumerate(ROWS_B): ry[r]=base+i*P
rail_tp=Y0-P*1.9; rail_tn=Y0-P*1.0
rail_bn=base+4*P+P*1.0; rail_bp=base+4*P+P*1.9
W=X0+COLS*P+265; H=rail_bp+P*2.6
cx=lambda c: X0+(c-0.5)*P
hole=lambda x,y,rim=RIM: f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{HOLE}" stroke="{rim}" stroke-width="1.2"/>'

s=[f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg">',
   f'<rect width="{W:.0f}" height="{H:.0f}" fill="{BG}"/>']
bx=X0-P*0.7; bw=COLS*P+P*1.4; by=rail_tp-P*0.8; bh=rail_bp-rail_tp+P*1.6
s.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{BOARD}" stroke="{EDGE}" stroke-width="2" rx="9"/>')

HL=7  # highlighted column
# rails
for yy,col,sym in ((rail_tp,RED,"+"),(rail_tn,BLUE,"−"),(rail_bn,BLUE,"−"),(rail_bp,RED,"+")):
    s.append(f'<line x1="{cx(1)-9:.1f}" y1="{yy:.1f}" x2="{cx(COLS)+9:.1f}" y2="{yy:.1f}" stroke="{col}" stroke-width="11" opacity=".16" stroke-linecap="round"/>')
    s.append(f'<text x="{bx-12:.0f}" y="{yy+6:.0f}" fill="{col}" font-family="{S}" font-size="19" font-weight="700" text-anchor="end">{sym}</text>')
    for c in range(1,COLS+1): s.append(hole(cx(c),yy,col))
# columns
for c in range(1,COLS+1):
    for grp in (ROWS_T,ROWS_B):
        y1=ry[grp[0]]; y2=ry[grp[-1]]
        strong = (c==HL)
        s.append(f'<line x1="{cx(c):.1f}" y1="{y1:.1f}" x2="{cx(c):.1f}" y2="{y2:.1f}" stroke="{TEAL}" '
                 f'stroke-width="{13 if strong else 11}" opacity="{0.85 if strong else 0.12}" stroke-linecap="round"/>')
        for r in grp: s.append(hole(cx(c),ry[r], "#fff" if strong else RIM))
# row letters
for r in ROWS_T+ROWS_B:
    s.append(f'<text x="{bx-12:.0f}" y="{ry[r]+6:.0f}" fill="{DIM}" font-family="{F}" font-size="15" text-anchor="end">{r}</text>')
# gap marker
gy=(ry['e']+ry['f'])/2
s.append(f'<line x1="{bx+8:.0f}" y1="{gy:.1f}" x2="{bx+bw-8:.0f}" y2="{gy:.1f}" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="9,6"/>')

def note(x,y,text,col,anchor="start",weight=700,size=18):
    s.append(f'<text x="{x:.0f}" y="{y:.0f}" fill="{col}" font-family="{S}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{text}</text>')

# callout: column  (aligned to row c, well clear of the gap)
LBLX = cx(COLS)+42
s.append(f'<line x1="{bx+bw-6:.0f}" y1="{ry["c"]:.1f}" x2="{LBLX-12:.1f}" y2="{ry["c"]:.1f}" stroke="{TEAL}" stroke-width="2"/>')
note(LBLX, ry["c"]-4, "these five holes", TEAL)
note(LBLX, ry["c"]+20, "are joined underneath", DIM, weight=400, size=16)

# callout: gap
s.append(f'<line x1="{bx+bw-6:.0f}" y1="{gy:.1f}" x2="{LBLX-12:.1f}" y2="{gy:.1f}" stroke="{ORANGE}" stroke-width="2"/>')
note(LBLX, gy-4, "the gap breaks", ORANGE)
note(LBLX, gy+20, "the connection", DIM, weight=400, size=16)

# callout: rails
s.append(f'<line x1="{bx+bw-6:.0f}" y1="{rail_tp:.1f}" x2="{LBLX-12:.1f}" y2="{rail_tp:.1f}" stroke="{RED}" stroke-width="2"/>')
note(LBLX, rail_tp-4, "rails run the", RED)
note(LBLX, rail_tp+20, "whole length", DIM, weight=400, size=16)

# bottom caption
note((X0+COLS*P)/2+X0/2, H-16, "Same column, connected. Different column, not connected.", DIM, anchor="middle", weight=400, size=17)
s.append('</svg>')
open('content/img/breadboard-anatomy.svg','w').write("\n".join(s))
print("wrote content/img/breadboard-anatomy.svg", f"{W:.0f}x{H:.0f}")
