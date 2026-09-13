BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
W,H=900,400
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
   f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="44" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">The value is stored in one byte, which is eight bits</text>')
places=[128,64,32,16,8,4,2,1]
BW,BH=74,64; X0=(W-len(places)*BW)/2
def row(y,bits,label,val,col):
    for i,(p,b) in enumerate(zip(places,bits)):
        x=X0+i*BW
        on = b=='1'
        s.append(f'<rect x="{x+4}" y="{y}" width="{BW-8}" height="{BH}" rx="7" fill="{col if on else "#ffffff"}" opacity="{0.18 if on else 1}" stroke="{col if on else LINE}" stroke-width="{2 if on else 1.5}"/>')
        s.append(f'<text x="{x+BW/2}" y="{y+41}" fill="{col if on else DIM}" font-family="{F}" font-size="26" font-weight="700" text-anchor="middle">{b}</text>')
        if y==110:
            s.append(f'<text x="{x+BW/2}" y="{y-12}" fill="{DIM}" font-family="{F}" font-size="14" text-anchor="middle">{p}</text>')
    s.append(f'<text x="{X0-24}" y="{y+41}" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="end">{label}</text>')
    s.append(f'<text x="{X0+len(places)*BW+24}" y="{y+41}" fill="{col}" font-family="{F}" font-size="24" font-weight="700">{val}</text>')
row(110,"00000000","all off","0",DIM)
row(196,"10000000","just the 128","128",ORANGE)
row(282,"11111111","all on","255",GREEN)
s.append(f'<text x="{W/2}" y="378" fill="{DIM}" font-family="{S}" font-size="17" text-anchor="middle">256 possible values, counting from zero. So the largest is 255.</text>')
s.append('</svg>')
open('content/img/byte.svg','w').write("\n".join(s)); print("byte.svg")

# ---------- floating vs pull-up ----------
W,H=900,470
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
   f'<rect width="{W}" height="{H}" fill="{BG}"/>']
RED="#b4241f"
def panel(cx,title,pullup,verdict,vcol):
    PY=150; GY=370
    s.append(f'<text x="{cx}" y="38" fill="{TEXT}" font-family="{S}" font-size="19" font-weight="700" text-anchor="middle">{title}</text>')
    # the pin
    s.append(f'<rect x="{cx-118}" y="{PY-20}" width="86" height="40" rx="6" fill="#fff" stroke="{TEAL}" stroke-width="2"/>')
    s.append(f'<text x="{cx-75}" y="{PY+7}" fill="{TEAL}" font-family="{F}" font-size="16" text-anchor="middle">pin 2</text>')
    s.append(f'<line x1="{cx-32}" y1="{PY}" x2="{cx}" y2="{PY}" stroke="{TEXT}" stroke-width="2.5"/>')
    s.append(f'<line x1="{cx}" y1="{PY}" x2="{cx}" y2="{PY+70}" stroke="{TEXT}" stroke-width="2.5"/>')
    if pullup:
        s.append(f'<line x1="{cx}" y1="{PY}" x2="{cx}" y2="{PY-62}" stroke="{TEXT}" stroke-width="2.5"/>')
        s.append(f'<rect x="{cx-17}" y="{PY-52}" width="34" height="26" fill="#d9c79a" stroke="#8a7f6a" stroke-width="1.5" rx="4"/>')
        s.append(f'<text x="{cx+26}" y="{PY-34}" fill="{DIM}" font-family="{S}" font-size="14">pull-up</text>')
        s.append(f'<line x1="{cx-22}" y1="{PY-72}" x2="{cx+22}" y2="{PY-72}" stroke="{RED}" stroke-width="3"/>')
        s.append(f'<text x="{cx}" y="{PY-82}" fill="{RED}" font-family="{F}" font-size="15" text-anchor="middle">5 V</text>')
    # switch
    s.append(f'<circle cx="{cx}" cy="{PY+70}" r="4.5" fill="{TEXT}"/>')
    s.append(f'<line x1="{cx}" y1="{PY+70}" x2="{cx+44}" y2="{PY+40}" stroke="{TEXT}" stroke-width="2.5"/>')
    s.append(f'<circle cx="{cx}" cy="{PY+130}" r="4.5" fill="{TEXT}"/>')
    s.append(f'<line x1="{cx}" y1="{PY+130}" x2="{cx}" y2="{GY-40}" stroke="{TEXT}" stroke-width="2.5"/>')
    s.append(f'<text x="{cx+52}" y="{PY+92}" fill="{DIM}" font-family="{S}" font-size="14">button, not pressed</text>')
    for i,w in enumerate((34,24,14)):
        s.append(f'<line x1="{cx-w}" y1="{GY-40+i*7}" x2="{cx+w}" y2="{GY-40+i*7}" stroke="{DIM}" stroke-width="2.5"/>')
    s.append(f'<text x="{cx}" y="{GY+2}" fill="{DIM}" font-family="{F}" font-size="15" text-anchor="middle">GND</text>')
    s.append(f'<text x="{cx}" y="{GY+46}" fill="{vcol}" font-family="{S}" font-size="18" font-weight="700" text-anchor="middle">{verdict}</text>')
panel(250,"Nothing holding the pin","",  "reads anything at all",RED)
panel(660,"A resistor holding it high",1,"reads HIGH, reliably",GREEN)
s.append(f'<line x1="455" y1="64" x2="455" y2="430" stroke="{LINE}" stroke-width="1.5"/>')
s.append('</svg>')
open('content/img/pullup.svg','w').write("\n".join(s)); print("pullup.svg")

# ---------- tactile button legs ----------
W,H=900,360
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
   f'<rect width="{W}" height="{H}" fill="{BG}"/>']
cx,cy=450,175
s.append(f'<text x="{W/2}" y="46" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">A four-legged button only has two connections</text>')
s.append(f'<rect x="{cx-80}" y="{cy-80}" width="160" height="160" rx="10" fill="#e2ddd2" stroke="{LINE}" stroke-width="2"/>')
s.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="#c9c2b3" stroke="{LINE}" stroke-width="2"/>')
legs=[(-120,-56,"A"),(-120,56,"B"),(120,-56,"C"),(120,56,"D")]
for dx,dy,n in legs:
    x,y=cx+dx,cy+dy
    s.append(f'<line x1="{cx+(-80 if dx<0 else 80)}" y1="{y}" x2="{x}" y2="{y}" stroke="#9aa0a6" stroke-width="4"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="{DIM}" stroke-width="2"/>')
    s.append(f'<text x="{x+(-24 if dx<0 else 24)}" y="{y+6}" fill="{DIM}" font-family="{F}" font-size="16" text-anchor="{"end" if dx<0 else "start"}">{n}</text>')
for sx,col,lab in ((-120,TEAL,"always joined"),(120,TEAL,"always joined")):
    s.append(f'<line x1="{cx+sx}" y1="{cy-56}" x2="{cx+sx}" y2="{cy+56}" stroke="{col}" stroke-width="5" opacity=".8"/>')
s.append(f'<text x="{cx-120}" y="{cy+92}" fill="{TEAL}" font-family="{S}" font-size="15" font-weight="700" text-anchor="middle">always joined</text>')
s.append(f'<text x="{cx+120}" y="{cy+92}" fill="{TEAL}" font-family="{S}" font-size="15" font-weight="700" text-anchor="middle">always joined</text>')
s.append(f'<line x1="{cx-120}" y1="{cy}" x2="{cx+120}" y2="{cy}" stroke="{ORANGE}" stroke-width="4" stroke-dasharray="9,7"/>')
s.append(f'<text x="{cx}" y="{cy-52}" fill="{ORANGE}" font-family="{S}" font-size="16" font-weight="700" text-anchor="middle">joined only while pressed</text>')
s.append(f'<text x="{W/2}" y="{H-18}" fill="{DIM}" font-family="{S}" font-size="17" text-anchor="middle">Use one leg from the left and one from the right, straddling the centre gap.</text>')
s.append('</svg>')
open('content/img/button-legs.svg','w').write("\n".join(s)); print("button-legs.svg")
