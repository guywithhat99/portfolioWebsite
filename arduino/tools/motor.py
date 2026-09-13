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
import math
W,H=900,540
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
BX,CY=430,300                 # transistor bar x, base height
CX=BX+56                      # x of collector/emitter verticals
RAIL,GND=70,450
def ln(x1,y1,x2,y2,col=TEXT,w=2.8): s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
def txt(x,y,t,col=TEXT,size=16,weight=400,anchor="start",fam=S): s.append(f'<text x="{x}" y="{y}" fill="{col}" font-family="{fam}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{t}</text>')

# big current path, drawn first so wires sit on top
PATHX=CX+120
s.append(f'<line x1="{PATHX}" y1="{RAIL+30}" x2="{PATHX}" y2="{GND-18}" stroke="{RED}" stroke-width="16" opacity=".16" stroke-linecap="round"/>')
for yy in (150,300,410):
    s.append(f'<polygon points="{PATHX-11},{yy-9} {PATHX+11},{yy-9} {PATHX},{yy+9}" fill="{RED}" opacity=".75"/>')
txt(PATHX+24,280,"hundreds of mA",RED,17,700)
txt(PATHX+24,302,"5 V, through the motor,",DIM,15)
txt(PATHX+24,322,"through the transistor,",DIM,15)
txt(PATHX+24,342,"to ground",DIM,15)

# 5 V rail and motor
ln(CX-60,RAIL,CX+60,RAIL,RED,3.5); txt(CX-70,RAIL+6,"5 V",RED,16,700,"end",F)
ln(CX,RAIL,CX,118)
s.append(f'<circle cx="{CX}" cy="150" r="32" fill="#fff" stroke="{TEXT}" stroke-width="2.8"/>')
txt(CX,157,"M",TEXT,19,700,"middle")
txt(CX-44,156,"motor",DIM,15,400,"end")
ln(CX,182,CX,232)

# NPN symbol
ln(BX,CY-44,BX,CY+44,TEXT,6)
ln(BX,CY-18,CX,CY-58); ln(CX,CY-58,CX,232)          # collector
ln(BX,CY+18,CX,CY+58); ln(CX,CY+58,CX,GND)          # emitter
ang=math.atan2(40,56)                                  # arrow on emitter, pointing away from base
ax,ay=BX+0.78*(CX-BX), CY+18+0.78*40
L=15; Wd=8
p1=(ax,ay); p2=(ax-L*math.cos(ang)+Wd*math.sin(ang), ay-L*math.sin(ang)-Wd*math.cos(ang)); p3=(ax-L*math.cos(ang)-Wd*math.sin(ang), ay-L*math.sin(ang)+Wd*math.cos(ang))
s.append(f'<polygon points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}" fill="{TEXT}"/>')
txt(CX+14,CY-62,"collector",RED,16,700)
txt(CX+14,CY+74,"emitter",DIM,16,700)
txt(BX-14,CY+62,"base",TEAL,16,700,"end")

# ground
for i,w in enumerate((30,20,10)): ln(CX-w,GND+i*8,CX+w,GND+i*8,DIM,2.8)
txt(CX-40,GND+14,"ground",DIM,15,400,"end")

# base drive
ln(BX-90,CY,BX,CY)
s.append(f'<rect x="{BX-140}" y="{CY-14}" width="50" height="28" fill="#d9c79a" stroke="#8a7f6a" stroke-width="1.5" rx="4"/>')
txt(BX-115,CY+38,"330 Ω",DIM,14,400,"middle")
ln(BX-200,CY,BX-140,CY)
s.append(f'<rect x="{BX-320}" y="{CY-26}" width="120" height="52" rx="7" fill="#fff" stroke="{TEAL}" stroke-width="2"/>')
txt(BX-260,CY+7,"pin 9",TEAL,17,400,"middle",F)
# small current arrow
ln(BX-190,CY-34,BX-30,CY-34,TEAL,2.2)
s.append(f'<polygon points="{BX-22},{CY-34} {BX-34},{CY-41} {BX-34},{CY-27}" fill="{TEAL}"/>')
txt(BX-110,CY-44,"a few mA",TEAL,16,700,"middle")

txt(W/2,H-40,"A small current into the base lets a big current flow through the motor.",TEXT,18,700,"middle")
txt(W/2,H-14,"The pin never carries the motor current. It only opens and closes the valve.",DIM,16,400,"middle")
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
