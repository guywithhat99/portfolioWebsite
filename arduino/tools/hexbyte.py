BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; PURPLE="#6d28d9"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
W,H=900,420
BW,BH=68,62
GAP=40
X0=(W-8*BW-GAP)/2
bits="11010000"
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="42" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">One byte is always two hex digits</text>')
for i,b in enumerate(bits):
    col = TEAL if i<4 else ORANGE
    x = X0 + i*BW + (GAP if i>=4 else 0)
    s.append(f'<rect x="{x+4}" y="92" width="{BW-8}" height="{BH}" rx="7" fill="{col}" opacity=".15"/>')
    s.append(f'<rect x="{x+4}" y="92" width="{BW-8}" height="{BH}" rx="7" fill="none" stroke="{col}" stroke-width="2"/>')
    s.append(f'<text x="{x+BW/2}" y="{92+42}" fill="{col}" font-family="{F}" font-size="26" font-weight="700" text-anchor="middle">{b}</text>')
def nib(i0,col,digit,val):
    x1=X0+i0*BW+4+(GAP if i0>=4 else 0); x2=X0+(i0+4)*BW-4+(GAP if i0>=4 else 0)
    y=172
    s.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="2.4"/>')
    for xx in (x1,x2): s.append(f'<line x1="{xx}" y1="{y-7}" x2="{xx}" y2="{y+7}" stroke="{col}" stroke-width="2.4"/>')
    s.append(f'<text x="{(x1+x2)/2}" y="{y+34}" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">four bits, worth {val}</text>')
    s.append(f'<text x="{(x1+x2)/2}" y="{y+82}" fill="{col}" font-family="{F}" font-size="40" font-weight="700" text-anchor="middle">{digit}</text>')
nib(0,TEAL,"D","13")
nib(4,ORANGE,"0","0")
s.append(f'<text x="{W/2}" y="330" fill="{TEXT}" font-family="{F}" font-size="30" font-weight="700" text-anchor="middle">0xD0</text>')
s.append(f'<text x="{W/2}" y="368" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">Four bits have sixteen possible values, so one digit covers them exactly.</text>')
s.append(f'<text x="{W/2}" y="394" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">Decimal cannot do that, which is why datasheets do not use it.</text>')
s.append('</svg>')
open('content/img/hex-byte.svg','w').write("\n".join(s)); print("hex-byte.svg")

# ---------- write vs read transaction, byte level ----------
W,H=1010,430
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">What goes down the wires</text>')
def strip(x0,y,items):
    x=x0
    for label,w,who in items:
        col = GREEN if who=="s" else TEAL
        if label in ("S","P"):
            col = "#b4241f"
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="54" rx="6" fill="{col}" opacity=".15"/>')
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="54" rx="6" fill="none" stroke="{col}" stroke-width="2"/>')
        fs = 17 if len(label)<=5 else 15
        s.append(f'<text x="{x+w/2}" y="{y+34}" fill="{col}" font-family="{F}" font-size="{fs}" font-weight="700" text-anchor="middle">{label}</text>')
        x += w+5
    return x
s.append(f'<text x="40" y="96" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700">Writing a register</text>')
s.append(f'<text x="40" y="118" fill="{DIM}" font-family="{S}" font-size="14">one message</text>')
strip(230,80,[("S",34,"m"),("0x76 W",106,"m"),("A",34,"s"),("0xF4",84,"m"),("A",34,"s"),("0x27",84,"m"),("A",34,"s"),("P",34,"m")])
s.append(f'<text x="40" y="216" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700">Reading a register</text>')
s.append(f'<text x="40" y="238" fill="{DIM}" font-family="{S}" font-size="14">two messages</text>')
endx=strip(230,200,[("S",34,"m"),("0x76 W",106,"m"),("A",34,"s"),("0xD0",84,"m"),("A",34,"s"),("P",34,"m")])
strip(230,272,[("S",34,"m"),("0x76 R",106,"m"),("A",34,"s"),("0x58",84,"s"),("N",34,"m"),("P",34,"m")])
s.append(f'<text x="{endx+18}" y="234" fill="{DIM}" font-family="{S}" font-size="14">then</text>')
# key
kx=230
for col,lab in ((TEAL,"Arduino drives"),(GREEN,"the chip drives"),("#b4241f","start and stop")):
    s.append(f'<rect x="{kx}" y="352" width="14" height="14" rx="3" fill="{col}" opacity=".3"/>')
    s.append(f'<rect x="{kx}" y="352" width="14" height="14" rx="3" fill="none" stroke="{col}" stroke-width="1.6"/>')
    s.append(f'<text x="{kx+21}" y="364" fill="{DIM}" font-family="{S}" font-size="14">{lab}</text>')
    kx += 21+len(lab)*7.2+28
s.append(f'<text x="{W/2}" y="406" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">A write carries the value with it. A read has to turn the bus around.</text>')
s.append('</svg>')
open('content/img/write-vs-read.svg','w').write("\n".join(s)); print("write-vs-read.svg")
