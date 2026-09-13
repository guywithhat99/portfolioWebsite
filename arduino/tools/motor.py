BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; RED="#b4241f"; GREEN="#1a7f4b"; PURPLE="#6d28d9"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"

# ---------- 1. current budget ----------
W,H=900,390
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="44" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">How much current things want</text>')
X0=260; SCALE=1.7; y=100
items=[("an LED",10,GREEN,"about 10 mA"),
       ("what a pin can give",20,TEAL,"20 mA, comfortably"),
       ("absolute maximum",40,ORANGE,"40 mA, and not for long"),
       ("a small DC motor",250,RED,"250 mA or more when starting")]
for lab,ma,col,note in items:
    w=ma*SCALE
    s.append(f'<text x="{X0-18}" y="{y+22}" fill="{TEXT}" font-family="{S}" font-size="17" text-anchor="end">{lab}</text>')
    s.append(f'<rect x="{X0}" y="{y}" width="{w:.0f}" height="32" fill="{col}" opacity=".75" rx="5"/>')
    s.append(f'<text x="{X0+w+12:.0f}" y="{y+22}" fill="{col}" font-family="{S}" font-size="15" font-weight="700">{note}</text>')
    y+=64
s.append(f'<line x1="{X0+40*SCALE:.0f}" y1="92" x2="{X0+40*SCALE:.0f}" y2="{y-18}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6,5"/>')
s.append(f'<text x="{W/2}" y="{H-18}" fill="{TEXT}" font-family="{S}" font-size="18" font-weight="700" text-anchor="middle">The motor wants roughly ten times what the pin can survive.</text>')
s.append('</svg>')
open('content/img/current-budget.svg','w').write("\n".join(s)); print("current-budget.svg")

# ---------- 2. transistor as a switch ----------
W,H=900,450
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="42" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">A transistor lets a small current control a big one</text>')
BARX,cy=560,250
BT,BB=cy-46,cy+46
# symbol
s.append(f'<line x1="{BARX}" y1="{BT}" x2="{BARX}" y2="{BB}" stroke="{TEXT}" stroke-width="5"/>')
s.append(f'<line x1="{BARX-72}" y1="{cy}" x2="{BARX}" y2="{cy}" stroke="{TEXT}" stroke-width="2.5"/>')
s.append(f'<line x1="{BARX}" y1="{BT+14}" x2="{BARX+56}" y2="{BT-34}" stroke="{TEXT}" stroke-width="2.5"/>')
s.append(f'<line x1="{BARX+56}" y1="{BT-34}" x2="{BARX+56}" y2="{BT-92}" stroke="{TEXT}" stroke-width="2.5"/>')
s.append(f'<line x1="{BARX}" y1="{BB-14}" x2="{BARX+56}" y2="{BB+34}" stroke="{TEXT}" stroke-width="2.5"/>')
s.append(f'<line x1="{BARX+56}" y1="{BB+34}" x2="{BARX+56}" y2="{BB+92}" stroke="{TEXT}" stroke-width="2.5"/>')
s.append(f'<polygon points="{BARX+41},{BB+19} {BARX+30},{BB+8} {BARX+47},{BB+6}" fill="{TEXT}"/>')
# terminal labels, all clear of the wires
s.append(f'<text x="{BARX-8}" y="{cy+30}" fill="{TEAL}" font-family="{S}" font-size="16" font-weight="700" text-anchor="end">base</text>')
s.append(f'<text x="{BARX+78}" y="{BT-84}" fill="{RED}" font-family="{S}" font-size="16" font-weight="700">collector</text>')
s.append(f'<text x="{BARX+78}" y="{BT-64}" fill="{DIM}" font-family="{S}" font-size="14">up to the motor</text>')
s.append(f'<text x="{BARX+78}" y="{BB+86}" fill="{DIM}" font-family="{S}" font-size="16" font-weight="700">emitter</text>')
s.append(f'<text x="{BARX+78}" y="{BB+106}" fill="{DIM}" font-family="{S}" font-size="14">down to ground</text>')
# drive side
s.append(f'<rect x="{BARX-330}" y="{cy-26}" width="116" height="52" rx="7" fill="#fff" stroke="{TEAL}" stroke-width="2"/>')
s.append(f'<text x="{BARX-272}" y="{cy+7}" fill="{TEAL}" font-family="{F}" font-size="17" text-anchor="middle">pin 9</text>')
s.append(f'<line x1="{BARX-214}" y1="{cy}" x2="{BARX-168}" y2="{cy}" stroke="{TEXT}" stroke-width="2.5"/>')
s.append(f'<rect x="{BARX-168}" y="{cy-14}" width="38" height="28" fill="#d9c79a" stroke="#8a7f6a" stroke-width="1.5" rx="4"/>')
s.append(f'<text x="{BARX-149}" y="{cy-26}" fill="{DIM}" font-family="{S}" font-size="14" text-anchor="middle">330 Ohm</text>')
s.append(f'<line x1="{BARX-130}" y1="{cy}" x2="{BARX-72}" y2="{cy}" stroke="{TEXT}" stroke-width="2.5"/>')
s.append(f'<text x="{BARX-150}" y="{cy+42}" fill="{TEAL}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">a few mA</text>')
s.append(f'<text x="{BARX+160}" y="{BT-30}" fill="{RED}" font-family="{S}" font-size="16" font-weight="700">hundreds of mA</text>')
s.append(f'<text x="{W/2}" y="{H-16}" fill="{DIM}" font-family="{S}" font-size="17" text-anchor="middle">The pin never carries the motor current. It only opens and closes the valve.</text>')
s.append('</svg>')
open('content/img/transistor-switch.svg','w').write("\n".join(s)); print("transistor-switch.svg")

# ---------- 3. flyback ----------
W,H=900,430
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Switching a motor off makes a voltage spike</text>')
def motorpanel(cx,title,withdiode,verdict,vcol):
    TOPY,BOTY=110,300
    s.append(f'<text x="{cx}" y="80" fill="{TEXT}" font-family="{S}" font-size="18" font-weight="700" text-anchor="middle">{title}</text>')
    s.append(f'<line x1="{cx-60}" y1="{TOPY}" x2="{cx+60}" y2="{TOPY}" stroke="{RED}" stroke-width="3"/>')
    s.append(f'<text x="{cx+70}" y="{TOPY+5}" fill="{RED}" font-family="{F}" font-size="15">5 V</text>')
    s.append(f'<line x1="{cx}" y1="{TOPY}" x2="{cx}" y2="{TOPY+30}" stroke="{TEXT}" stroke-width="2.5"/>')
    s.append(f'<circle cx="{cx}" cy="{TOPY+62}" r="32" fill="#fff" stroke="{TEXT}" stroke-width="2.5"/>')
    s.append(f'<text x="{cx}" y="{TOPY+69}" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">M</text>')
    s.append(f'<line x1="{cx}" y1="{TOPY+94}" x2="{cx}" y2="{BOTY}" stroke="{TEXT}" stroke-width="2.5"/>')
    if withdiode:
        dx=cx+86
        s.append(f'<line x1="{cx}" y1="{TOPY+30}" x2="{dx}" y2="{TOPY+30}" stroke="{GREEN}" stroke-width="2.5"/>')
        s.append(f'<line x1="{dx}" y1="{TOPY+30}" x2="{dx}" y2="{TOPY+94}" stroke="{GREEN}" stroke-width="2.5"/>')
        s.append(f'<line x1="{cx}" y1="{TOPY+94}" x2="{dx}" y2="{TOPY+94}" stroke="{GREEN}" stroke-width="2.5"/>')
        my=TOPY+62
        s.append(f'<polygon points="{dx-13},{my+13} {dx+13},{my+13} {dx},{my-11}" fill="{GREEN}"/>')
        s.append(f'<line x1="{dx-14}" y1="{my-13}" x2="{dx+14}" y2="{my-13}" stroke="{GREEN}" stroke-width="3"/>')
        s.append(f'<text x="{dx+24}" y="{my+5}" fill="{GREEN}" font-family="{S}" font-size="14" font-weight="700">diode</text>')
    s.append(f'<line x1="{cx-16}" y1="{BOTY}" x2="{cx+16}" y2="{BOTY}" stroke="{TEXT}" stroke-width="3"/>')
    s.append(f'<line x1="{cx+16}" y1="{BOTY}" x2="{cx+46}" y2="{BOTY-26}" stroke="{TEXT}" stroke-width="2.5"/>')
    s.append(f'<text x="{cx+56}" y="{BOTY-14}" fill="{DIM}" font-family="{S}" font-size="13">just switched off</text>')
    s.append(f'<line x1="{cx}" y1="{BOTY}" x2="{cx}" y2="{BOTY+30}" stroke="{TEXT}" stroke-width="2.5"/>')
    for i,w in enumerate((26,17,9)):
        s.append(f'<line x1="{cx-w}" y1="{BOTY+30+i*7}" x2="{cx+w}" y2="{BOTY+30+i*7}" stroke="{DIM}" stroke-width="2.5"/>')
    s.append(f'<text x="{cx}" y="{BOTY+96}" fill="{vcol}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">{verdict}</text>')
motorpanel(260,"No diode",False,"the spike has nowhere to go",RED)
motorpanel(660,"With a diode",True,"the spike loops round harmlessly",GREEN)
s.append(f'<line x1="460" y1="70" x2="460" y2="400" stroke="{LINE}" stroke-width="1.5"/>')
s.append('</svg>')
open('content/img/flyback.svg','w').write("\n".join(s)); print("flyback.svg")
