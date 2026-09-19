"""The address and the R/W bit are one byte on the wire."""
BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; RED="#b4241f"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
W,H=900,470
BW,BH=62,58
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">The address and the R/W bit travel as one byte</text>')
addr="1110110"
def row(y,bits,rw,label,result,col):
    X0=(W-8*BW)/2
    for i in range(7):
        x=X0+i*BW
        s.append(f'<rect x="{x+3}" y="{y}" width="{BW-6}" height="{BH}" rx="6" fill="{TEAL}" opacity=".13"/>')
        s.append(f'<rect x="{x+3}" y="{y}" width="{BW-6}" height="{BH}" rx="6" fill="none" stroke="{TEAL}" stroke-width="1.8"/>')
        s.append(f'<text x="{x+BW/2}" y="{y+39}" fill="{TEAL}" font-family="{F}" font-size="25" font-weight="700" text-anchor="middle">{bits[i]}</text>')
    x=X0+7*BW
    s.append(f'<rect x="{x+3}" y="{y}" width="{BW-6}" height="{BH}" rx="6" fill="{col}" opacity=".16"/>')
    s.append(f'<rect x="{x+3}" y="{y}" width="{BW-6}" height="{BH}" rx="6" fill="none" stroke="{col}" stroke-width="2.4"/>')
    s.append(f'<text x="{x+BW/2}" y="{y+39}" fill="{col}" font-family="{F}" font-size="25" font-weight="700" text-anchor="middle">{rw}</text>')
    s.append(f'<text x="{X0-18}" y="{y+37}" fill="{DIM}" font-family="{S}" font-size="16" font-weight="700" text-anchor="end">{label}</text>')
    s.append(f'<text x="{X0+8*BW+18}" y="{y+37}" fill="{col}" font-family="{F}" font-size="20" font-weight="700">{result}</text>')
X0=(W-8*BW)/2
# brackets
s.append(f'<line x1="{X0+3}" y1="118" x2="{X0+7*BW-3}" y2="118" stroke="{TEAL}" stroke-width="2"/>')
for xx in (X0+3, X0+7*BW-3): s.append(f'<line x1="{xx}" y1="112" x2="{xx}" y2="124" stroke="{TEAL}" stroke-width="2"/>')
s.append(f'<text x="{X0+3.5*BW}" y="106" fill="{TEAL}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">the 7 address bits, 0x76</text>')
s.append(f'<text x="{X0+7.5*BW}" y="106" fill="{ORANGE}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">R/W</text>')
row(132,addr,"0","writing","0xEC",ORANGE)
row(238,addr,"1","reading","0xED",GREEN)
s.append(f'<text x="{W/2}" y="344" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">Same seven bits both times. Only the last one changes.</text>')
s.append(f'<rect x="150" y="372" width="600" height="72" rx="8" fill="#fff" stroke="{LINE}" stroke-width="1.6"/>')
s.append(f'<text x="{W/2}" y="399" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">You write <tspan font-family="{F}" fill="{TEXT}">0x76</tspan> in your code. The library shifts it up one place</text>')
s.append(f'<text x="{W/2}" y="424" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">and fills in the last bit, depending on which call you made.</text>')
s.append('</svg>')
open('content/img/address-byte.svg','w').write("\n".join(s)); print("address-byte.svg")
