BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; RED="#b4241f"; PURPLE="#6d28d9"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
W,H=1000,470
BW,BH=44,50
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="38" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">One reading, spread across three registers</text>')

def row(y,x0,n,col,label,sub,used=None,shift=None):
    for i in range(n):
        x=x0+i*BW
        on = used is None or used[i]
        s.append(f'<rect x="{x+3}" y="{y}" width="{BW-6}" height="{BH}" rx="5" fill="{col}" opacity="{0.18 if on else 0.05}"/>')
        s.append(f'<rect x="{x+3}" y="{y}" width="{BW-6}" height="{BH}" rx="5" fill="none" stroke="{col}" stroke-width="{1.8 if on else 1}" opacity="{1 if on else 0.35}"/>')
        if not on:
            s.append(f'<text x="{x+BW/2}" y="{y+33}" fill="{col}" font-family="{F}" font-size="16" text-anchor="middle" opacity=".4">0</text>')
    s.append(f'<text x="{x0-16}" y="{y+32}" fill="{col}" font-family="{F}" font-size="16" font-weight="700" text-anchor="end">{label}</text>')
    s.append(f'<text x="{x0+n*BW+14}" y="{y+22}" fill="{DIM}" font-family="{S}" font-size="14">{sub}</text>')
    if shift: s.append(f'<text x="{x0+n*BW+14}" y="{y+42}" fill="{TEXT}" font-family="{F}" font-size="15" font-weight="700">{shift}</text>')

X=250
row(74, X, 8, TEAL,   "0xF7", "the top 8 bits",    shift="&lt;&lt; 12")
row(148, X, 8, ORANGE, "0xF8", "the middle 8 bits", shift="&lt;&lt; 4")
row(222, X, 8, GREEN,  "0xF9", "only the top 4 count", used=[1,1,1,1,0,0,0,0], shift="&gt;&gt; 4")

s.append(f'<line x1="{X-26}" y1="292" x2="{X+8*BW+150}" y2="292" stroke="{TEXT}" stroke-width="2.4"/>')
s.append(f'<text x="{X-36}" y="298" fill="{TEXT}" font-family="{F}" font-size="19" font-weight="700" text-anchor="end">|</text>')
# 20 bit result
RB=34
X2=250
for i in range(20):
    x=X2+i*RB
    s.append(f'<rect x="{x+2}" y="312" width="{RB-4}" height="{BH}" rx="5" fill="{PURPLE}" opacity=".16"/>')
    s.append(f'<rect x="{x+2}" y="312" width="{RB-4}" height="{BH}" rx="5" fill="none" stroke="{PURPLE}" stroke-width="1.8"/>')
s.append(f'<text x="{X2-16}" y="344" fill="{PURPLE}" font-family="{S}" font-size="15" font-weight="700" text-anchor="end">result</text>')
s.append(f'<line x1="{X2}" y1="380" x2="{X2+20*RB}" y2="380" stroke="{PURPLE}" stroke-width="2"/>')
for xx in (X2, X2+20*RB): s.append(f'<line x1="{xx}" y1="374" x2="{xx}" y2="386" stroke="{PURPLE}" stroke-width="2"/>')
s.append(f'<text x="{X2+10*RB}" y="404" fill="{PURPLE}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">20 bits</text>')
s.append(f'<text x="{W/2}" y="444" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">Each register is shifted to where its bits belong, then the three are merged.</text>')
s.append('</svg>')
open('content/img/assemble-20bit.svg','w').write("\n".join(s)); print("assemble-20bit.svg")
