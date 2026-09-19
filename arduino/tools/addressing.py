BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; RED="#b4241f"; PURPLE="#6d28d9"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
W,H=900,470
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Two different numbers, both written in hex</text>')
# left: the bus
s.append(f'<text x="175" y="82" fill="{DIM}" font-family="{S}" font-size="15" font-weight="700" text-anchor="middle">on the bus</text>')
for y,col in ((116,TEAL),(140,PURPLE)):
    s.append(f'<line x1="60" y1="{y}" x2="300" y2="{y}" stroke="{col}" stroke-width="3"/>')
def chip(cx,addr,col,hi=False):
    s.append(f'<line x1="{cx}" y1="140" x2="{cx}" y2="196" stroke="{DIM}" stroke-width="2.5"/>')
    s.append(f'<rect x="{cx-58}" y="196" width="116" height="56" rx="8" fill="#fff" stroke="{col}" stroke-width="{3 if hi else 2}"/>')
    s.append(f'<text x="{cx}" y="228" fill="{col}" font-family="{F}" font-size="18" font-weight="700" text-anchor="middle">{addr}</text>')
chip(120,"0x68",DIM); chip(250,"0x76",GREEN,hi=True)
s.append(f'<text x="250" y="276" fill="{GREEN}" font-family="{S}" font-size="15" font-weight="700" text-anchor="middle">which chip</text>')
s.append(f'<text x="120" y="276" fill="{DIM}" font-family="{S}" font-size="14" text-anchor="middle">a different chip</text>')
# zoom lines
s.append(f'<path d="M 308 196 L 470 108" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="6,5"/>')
s.append(f'<path d="M 308 252 L 470 402" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="6,5"/>')
# right: inside the chip
s.append(f'<text x="655" y="82" fill="{DIM}" font-family="{S}" font-size="15" font-weight="700" text-anchor="middle">inside that chip</text>')
s.append(f'<rect x="470" y="98" width="370" height="314" rx="10" fill="#fff" stroke="{GREEN}" stroke-width="2.5"/>')
rows=[("0xD0","chip id",PURPLE),("0xE0","reset",GREEN),("0xF3","status",DIM),
      ("0xF4","ctrl_meas",ORANGE),("0xF5","config",ORANGE),("0xF7","pressure",TEAL),("0xFA","temperature",TEAL)]
y=128
for addr,what,col in rows:
    s.append(f'<rect x="496" y="{y}" width="86" height="30" rx="4" fill="{col}" opacity=".14"/>')
    s.append(f'<rect x="496" y="{y}" width="86" height="30" rx="4" fill="none" stroke="{col}" stroke-width="1.5"/>')
    s.append(f'<text x="539" y="{y+21}" fill="{col}" font-family="{F}" font-size="16" font-weight="700" text-anchor="middle">{addr}</text>')
    s.append(f'<text x="598" y="{y+21}" fill="{DIM}" font-family="{S}" font-size="15">{what}</text>')
    y+=40
s.append(f'<text x="539" y="{y+16}" fill="{DIM}" font-family="{F}" font-size="18" text-anchor="middle">...</text>')
s.append(f'<text x="655" y="440" fill="{ORANGE}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">which box inside it</text>')
s.append('</svg>')
open('content/img/two-addresses.svg','w').write("\n".join(s)); print("two-addresses.svg")
