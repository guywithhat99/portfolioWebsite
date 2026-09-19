BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; PURPLE="#6d28d9"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
W,H=940,420
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">The low half arrives first</text>')
BW,BH=180,70
X=200
def box(x,y,label,sub,col,w=BW):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="8" fill="{col}" opacity=".16"/>')
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="8" fill="none" stroke="{col}" stroke-width="2.2"/>')
    s.append(f'<text x="{x+w/2}" y="{y+44}" fill="{col}" font-family="{F}" font-size="22" font-weight="700" text-anchor="middle">{label}</text>')
    s.append(f'<text x="{x+w/2}" y="{y+BH+24}" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">{sub}</text>')
s.append(f'<text x="{X-20}" y="{100+44}" fill="{TEXT}" font-family="{S}" font-size="15" font-weight="700" text-anchor="end">what arrives</text>')
box(X,100,"0x88","first byte",ORANGE)
box(X+BW+30,100,"0x89","second byte",TEAL)
# arrows crossing
s.append(f'<path d="M {X+BW/2} 196 C {X+BW/2} 240, {X+BW+30+BW/2+90} 240, {X+BW+30+BW/2+90} 276" fill="none" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="7,5"/>')
s.append(f'<polygon points="{X+BW+30+BW/2+90},282 {X+BW+30+BW/2+82},266 {X+BW+30+BW/2+98},266" fill="{ORANGE}"/>')
s.append(f'<path d="M {X+BW+30+BW/2} 196 C {X+BW+30+BW/2} 240, {X+BW/2-40} 240, {X+BW/2-40} 276" fill="none" stroke="{TEAL}" stroke-width="2.5" stroke-dasharray="7,5"/>')
s.append(f'<polygon points="{X+BW/2-40},282 {X+BW/2-48},266 {X+BW/2-32},266" fill="{TEAL}"/>')
s.append(f'<text x="{X-20}" y="{286+44}" fill="{TEXT}" font-family="{S}" font-size="15" font-weight="700" text-anchor="end">what it means</text>')
box(X,286,"0x89","high half",TEAL)
box(X+BW+30,286,"0x88","low half",ORANGE)
s.append(f'<text x="{X+2*BW+52}" y="{286+44}" fill="{PURPLE}" font-family="{F}" font-size="19" font-weight="700">one 16-bit number</text>')
s.append('</svg>')
open('content/img/little-endian.svg','w').write("\n".join(s)); print("little-endian.svg")
