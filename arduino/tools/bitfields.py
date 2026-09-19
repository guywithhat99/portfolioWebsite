BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; RED="#b4241f"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
BW,BH=72,62

def byterow(s,X0,y,bits,cols,fade=None):
    for i in range(8):
        x=X0+i*BW; c=cols[i]
        dim = fade and fade[i]=='0'
        s.append(f'<rect x="{x+4}" y="{y}" width="{BW-8}" height="{BH}" rx="7" fill="{c}" opacity="{0.07 if dim else 0.16}"/>')
        s.append(f'<rect x="{x+4}" y="{y}" width="{BW-8}" height="{BH}" rx="7" fill="none" stroke="{c}" stroke-width="{1.4 if dim else 2.2}" opacity="{0.4 if dim else 1}"/>')
        s.append(f'<text x="{x+BW/2}" y="{y+42}" fill="{c}" font-family="{F}" font-size="27" font-weight="700" text-anchor="middle" opacity="{0.42 if dim else 1}">{bits[i]}</text>')

# ---------- 1. the layout of ctrl_meas ----------
W,H=900,400
X0=(W-8*BW)/2
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="42" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">One register, three separate settings</text>')
for i in range(8):
    s.append(f'<text x="{X0+i*BW+BW/2}" y="92" fill="{DIM}" font-family="{F}" font-size="15" text-anchor="middle">bit {7-i}</text>')
cols=[TEAL]*3+[ORANGE]*3+[GREEN]*2
byterow(s,X0,106,["?"]*8,cols)
def grp(i0,n,label,sub,col):
    x1=X0+i0*BW+4; x2=X0+(i0+n)*BW-4; y=192
    s.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="2.4"/>')
    for xx in (x1,x2): s.append(f'<line x1="{xx}" y1="{y-7}" x2="{xx}" y2="{y+7}" stroke="{col}" stroke-width="2.4"/>')
    s.append(f'<text x="{(x1+x2)/2}" y="{y+30}" fill="{col}" font-family="{F}" font-size="18" font-weight="700" text-anchor="middle">{label}</text>')
    s.append(f'<text x="{(x1+x2)/2}" y="{y+53}" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">{sub}</text>')
grp(0,3,"osrs_t","temperature",TEAL)
grp(3,3,"osrs_p","pressure",ORANGE)
grp(6,2,"mode","running or not",GREEN)
s.append(f'<text x="{W/2}" y="326" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">Writing to 0xF4 sets all three at once.</text>')
s.append(f'<text x="{W/2}" y="356" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">There is no way to change one without writing the whole byte.</text>')
s.append('</svg>')
open('content/img/ctrl-meas-layout.svg','w').write("\n".join(s)); print("ctrl-meas-layout.svg")

# ---------- 2. assembling the byte ----------
W,H=980,520
X0=(W-8*BW)/2+40
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Shift each setting into place, then merge them</text>')
rows=[("001 &lt;&lt; 5","00100000",TEAL),("001 &lt;&lt; 2","00000100",ORANGE),("11","00000011",GREEN)]
y=72
for expr,bits,col in rows:
    byterow(s,X0,y,list(bits),[col]*8,fade=bits)
    s.append(f'<text x="{X0-22}" y="{y+42}" fill="{col}" font-family="{F}" font-size="18" font-weight="700" text-anchor="end">{expr}</text>')
    y+=82
s.append(f'<line x1="{X0-10}" y1="{y+4}" x2="{X0+8*BW+10}" y2="{y+4}" stroke="{TEXT}" stroke-width="2.4"/>')
s.append(f'<text x="{X0-22}" y="{y+10}" fill="{TEXT}" font-family="{F}" font-size="20" font-weight="700" text-anchor="end">|</text>')
res="00100111"
rescols=[TEAL]*3+[ORANGE]*3+[GREEN]*2
byterow(s,X0,y+22,list(res),rescols)
s.append(f'<text x="{X0+8*BW+22}" y="{y+64}" fill="{TEXT}" font-family="{F}" font-size="24" font-weight="700">0x27</text>')
s.append(f'<text x="{W/2}" y="{H-42}" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">Each setting lands on its own bits, so none of them collide.</text>')
s.append(f'<text x="{W/2}" y="{H-16}" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">Temperature x1, pressure x1, normal mode.</text>')
s.append('</svg>')
open('content/img/ctrl-meas-build.svg','w').write("\n".join(s)); print("ctrl-meas-build.svg")
