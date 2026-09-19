"""One complete I2C frame: START, address, R/W, ACK, one data byte, ACK, STOP."""
BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; RED="#b4241f"; PURPLE="#6d28d9"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"

SLOT=50; PRE=70; POST=70; X0=96
ADDR=[1,1,1,0,1,1,0]      # 0x76
RW=[0]                    # writing
ACK1=[0]
DATA=[1,1,0,1,0,0,0,0]    # 0xD0
ACK2=[0]
bits = ADDR+RW+ACK1+DATA+ACK2
owner = ["m"]*7+["m"]+["s"]+["m"]*8+["s"]   # who drives each slot
N=len(bits)
W = X0 + PRE + N*SLOT + POST + 30
H = 440
SDA_H, SDA_L = 136, 196
SCL_H, SCL_L = 268, 328

def poly(pts,col,w=3,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in pts)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="miter"{d}/>'

s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="34" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">One message: telling chip 0x76 that you want register 0xD0</text>')

bus_start = X0+PRE
# ---- SDA ----
sda=[(X0, SDA_H)]
sda.append((bus_start-24, SDA_H))                 # idle high
sda.append((bus_start-24, SDA_L))                 # START: falls while SCL high
lvl=SDA_L
for i,b in enumerate(bits):
    x=bus_start+i*SLOT
    y=SDA_H if b else SDA_L
    sda.append((x,lvl)); sda.append((x,y)); lvl=y
endx=bus_start+N*SLOT
sda.append((endx,lvl)); sda.append((endx,SDA_L))  # hold low into STOP
sda.append((endx+26,SDA_L)); sda.append((endx+26,SDA_H))  # STOP: rises while SCL high
sda.append((W-30,SDA_H))
s.append(poly(sda,TEAL))

# ---- SCL ----
scl=[(X0,SCL_H),(bus_start-24,SCL_H)]             # high during START
for i in range(N):
    x=bus_start+i*SLOT
    scl += [(x,SCL_H),(x,SCL_L),(x+SLOT*0.5,SCL_L),(x+SLOT*0.5,SCL_H),(x+SLOT,SCL_H)]
scl += [(endx,SCL_L),(endx+14,SCL_L),(endx+14,SCL_H),(W-30,SCL_H)]
s.append(poly(scl,PURPLE))

for y,lab,col in ((SDA_H,"SDA",TEAL),(SCL_H,"SCL",PURPLE)):
    s.append(f'<text x="{X0-10}" y="{y+22}" fill="{col}" font-family="{F}" font-size="17" font-weight="700" text-anchor="end">{lab}</text>')

# ---- guides: SDA only changes while SCL is low ----
for i in range(N+1):
    x=bus_start+i*SLOT
    s.append(f'<line x1="{x}" y1="{SDA_H-14}" x2="{x}" y2="{SCL_L+14}" stroke="{DIM}" stroke-width="1" stroke-dasharray="3,4" opacity=".55"/>')
# shade the half of each slot where SCL is high and the bit is being read
for i in range(N):
    x=bus_start+i*SLOT+SLOT*0.5
    s.append(f'<rect x="{x:.0f}" y="{SDA_H-14}" width="{SLOT*0.5:.0f}" height="{SCL_L-SDA_H+28}" fill="{PURPLE}" opacity=".055"/>')

# ---- bit values ----
for i,b in enumerate(bits):
    x=bus_start+i*SLOT+SLOT/2
    col = GREEN if owner[i]=="s" else TEAL
    s.append(f'<text x="{x:.0f}" y="{SDA_L+34}" fill="{col}" font-family="{F}" font-size="15" font-weight="700" text-anchor="middle">{b}</text>')

# ---- group brackets ----
def bracket(i0,n,label,sub,col,row=0):
    x1=bus_start+i0*SLOT; x2=x1+n*SLOT
    y=92
    s.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="2"/>')
    for xx in (x1,x2): s.append(f'<line x1="{xx}" y1="{y-6}" x2="{xx}" y2="{y+6}" stroke="{col}" stroke-width="2"/>')
    s.append(f'<text x="{(x1+x2)/2:.0f}" y="{y-10}" fill="{col}" font-family="{S}" font-size="15" font-weight="700" text-anchor="middle">{label}</text>')
    if sub:
        s.append(f'<text x="{(x1+x2)/2:.0f}" y="{y+22+row*17}" fill="{DIM}" font-family="{S}" font-size="13" text-anchor="middle">{sub}</text>')
bracket(0,7,"address 0x76","which chip",TEAL)
bracket(7,1,"R/W","0 = writing",ORANGE,row=0)
bracket(8,1,"ACK","chip answers",GREEN,row=1)
bracket(9,8,"data 0xD0","which register",TEAL)
bracket(17,1,"ACK","chip answers",GREEN,row=1)

# ---- START / STOP callouts ----
def cond(x,label,col):
    s.append(f'<line x1="{x}" y1="{SDA_H-16}" x2="{x}" y2="{SCL_L+18}" stroke="{col}" stroke-width="2" stroke-dasharray="5,4"/>')
    s.append(f'<text x="{x}" y="{SCL_L+38}" fill="{col}" font-family="{S}" font-size="15" font-weight="700" text-anchor="middle">{label}</text>')
cond(bus_start-24,"START",RED)
cond(endx+26,"STOP",RED)

s.append(f'<text x="{W/2}" y="{H-44}" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">Every dotted line is an SDA change, and SCL is low at all of them.</text>')
s.append(f'<text x="{W/2}" y="{H-18}" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">The shaded half of each slot is where SCL is high and the bit is read.</text>')
s.append('</svg>')
open('content/img/i2c-frame.svg','w').write("\n".join(s))
print(f"i2c-frame.svg  {W}x{H}")
