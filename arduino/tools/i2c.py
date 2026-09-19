BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; RED="#b4241f"; PURPLE="#6d28d9"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"

# ---------- 1. the shared bus ----------
W,H=900,430
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Everything shares the same two wires</text>')
SDA,SCL=150,196
X0,X1=150,800
# pull-ups
s.append(f'<line x1="180" y1="82" x2="300" y2="82" stroke="{RED}" stroke-width="3"/>')
s.append(f'<text x="312" y="88" fill="{RED}" font-family="{F}" font-size="15">3.3 V</text>')
for x,yline in ((200,SDA),(240,SCL)):
    s.append(f'<line x1="{x}" y1="82" x2="{x}" y2="102" stroke="{TEXT}" stroke-width="2"/>')
    s.append(f'<rect x="{x-13}" y="102" width="26" height="30" fill="#d9c79a" stroke="#8a7f6a" stroke-width="1.5" rx="4"/>')
    s.append(f'<line x1="{x}" y1="132" x2="{x}" y2="{yline}" stroke="{TEXT}" stroke-width="2"/>')
s.append(f'<text x="262" y="126" fill="{DIM}" font-family="{S}" font-size="14">pull-ups</text>')
# the two bus lines
for y,lab,col in ((SDA,"SDA",TEAL),(SCL,"SCL",PURPLE)):
    s.append(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{col}" stroke-width="3.5"/>')
    s.append(f'<text x="{X1+12}" y="{y+6}" fill="{col}" font-family="{F}" font-size="16" font-weight="700">{lab}</text>')
# devices
def dev(cx,title,addr,col,dim=False):
    op=".45" if dim else "1"
    s.append(f'<g opacity="{op}">')
    s.append(f'<line x1="{cx-16}" y1="{SDA}" x2="{cx-16}" y2="300" stroke="{TEAL}" stroke-width="2.5"/>')
    s.append(f'<line x1="{cx+16}" y1="{SCL}" x2="{cx+16}" y2="300" stroke="{PURPLE}" stroke-width="2.5"/>')
    s.append(f'<circle cx="{cx-16}" cy="{SDA}" r="5" fill="{TEAL}"/>')
    s.append(f'<circle cx="{cx+16}" cy="{SCL}" r="5" fill="{PURPLE}"/>')
    s.append(f'<rect x="{cx-90}" y="300" width="180" height="66" rx="8" fill="#fff" stroke="{col}" stroke-width="2.5"/>')
    s.append(f'<text x="{cx}" y="{326}" fill="{col}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">{title}</text>')
    s.append(f'<text x="{cx}" y="{350}" fill="{DIM}" font-family="{F}" font-size="15" text-anchor="middle">{addr}</text>')
    s.append('</g>')
dev(250,"Arduino","in charge",TEXT)
dev(520,"BMP280","0x76",GREEN)
dev(770,"something else","0x68",DIM,dim=True)
s.append(f'<text x="{W/2}" y="{H-14}" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">Each chip has its own address, so the Arduino can say which one it is talking to.</text>')
s.append('</svg>')
open('content/img/i2c-bus.svg','w').write("\n".join(s)); print("i2c-bus.svg")

# ---------- 2. open drain ----------
W,H=900,470
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Nobody pushes the line up. Chips can only pull it down.</text>')
RED="#b4241f"
def panel(cx,title,closed,verdict,vcol):
    RAIL,NODE,SW_T,SW_B,GND = 120, 250, 296, 352, 392
    s.append(f'<text x="{cx}" y="82" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">{title}</text>')
    # supply rail + pull-up
    s.append(f'<line x1="{cx-56}" y1="{RAIL}" x2="{cx+56}" y2="{RAIL}" stroke="{RED}" stroke-width="3"/>')
    s.append(f'<text x="{cx+66}" y="{RAIL+5}" fill="{RED}" font-family="{F}" font-size="14">3.3 V</text>')
    s.append(f'<line x1="{cx}" y1="{RAIL}" x2="{cx}" y2="{RAIL+34}" stroke="{TEXT}" stroke-width="2.5"/>')
    s.append(f'<rect x="{cx-15}" y="{RAIL+34}" width="30" height="34" fill="#d9c79a" stroke="#8a7f6a" stroke-width="1.5" rx="4"/>')
    s.append(f'<text x="{cx-24}" y="{RAIL+56}" fill="{DIM}" font-family="{S}" font-size="13" text-anchor="end">pull-up</text>')
    s.append(f'<line x1="{cx}" y1="{RAIL+68}" x2="{cx}" y2="{NODE}" stroke="{TEXT}" stroke-width="2.5"/>')
    # bus tap
    busc = GREEN if not closed else TEAL
    s.append(f'<circle cx="{cx}" cy="{NODE}" r="5" fill="{TEXT}"/>')
    s.append(f'<line x1="{cx}" y1="{NODE}" x2="{cx+130}" y2="{NODE}" stroke="{busc}" stroke-width="3.5"/>')
    s.append(f'<text x="{cx+138}" y="{NODE+5}" fill="{busc}" font-family="{F}" font-size="15" font-weight="700">the bus</text>')
    # down into the chip's switch
    s.append(f'<line x1="{cx}" y1="{NODE}" x2="{cx}" y2="{SW_T}" stroke="{TEXT}" stroke-width="2.5"/>')
    s.append(f'<circle cx="{cx}" cy="{SW_T}" r="4.5" fill="{TEXT}"/>')
    s.append(f'<circle cx="{cx}" cy="{SW_B}" r="4.5" fill="{TEXT}"/>')
    if closed:
        s.append(f'<line x1="{cx}" y1="{SW_T}" x2="{cx}" y2="{SW_B}" stroke="{TEAL}" stroke-width="3.5"/>')
    else:
        s.append(f'<line x1="{cx}" y1="{SW_T}" x2="{cx+34}" y2="{SW_B-24}" stroke="{TEXT}" stroke-width="2.5"/>')
    s.append(f'<line x1="{cx}" y1="{SW_B}" x2="{cx}" y2="{GND}" stroke="{TEXT}" stroke-width="2.5"/>')
    for i,w in enumerate((24,15,7)):
        s.append(f'<line x1="{cx-w}" y1="{GND+i*7}" x2="{cx+w}" y2="{GND+i*7}" stroke="{DIM}" stroke-width="2.5"/>')

    # chip bracket
    s.append(f'<rect x="{cx-92}" y="{SW_T-22}" width="176" height="{SW_B-SW_T+44}" rx="8" fill="none" stroke="{DIM}" stroke-width="1.6" stroke-dasharray="6,5"/>')
    s.append(f'<text x="{cx-98}" y="{(SW_T+SW_B)/2+5}" fill="{DIM}" font-family="{S}" font-size="14" text-anchor="end">inside</text>')
    s.append(f'<text x="{cx-98}" y="{(SW_T+SW_B)/2+22}" fill="{DIM}" font-family="{S}" font-size="14" text-anchor="end">the chip</text>')
    s.append(f'<text x="{cx}" y="{H-36}" fill="{vcol}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">{verdict}</text>')
panel(250,"Switch open",False,"the resistor wins, line is HIGH",GREEN)
panel(660,"Switch closed",True,"the chip wins, line is LOW",TEAL)
s.append(f'<line x1="455" y1="66" x2="455" y2="430" stroke="{LINE}" stroke-width="1.5"/>')
s.append('</svg>')
open('content/img/open-drain.svg','w').write("\n".join(s)); print("open-drain.svg redrawn")
