BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; ORANGE="#c4551a"; GREEN="#1a7f4b"; RED="#b4241f"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"
W,H=900,460
AX,BX=200,700
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Reading one register takes two messages</text>')
for x,lab,col in ((AX,"Arduino",TEAL),(BX,"BMP280",GREEN)):
    s.append(f'<rect x="{x-76}" y="66" width="152" height="46" rx="8" fill="#fff" stroke="{col}" stroke-width="2.5"/>')
    s.append(f'<text x="{x}" y="96" fill="{col}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">{lab}</text>')
    s.append(f'<line x1="{x}" y1="112" x2="{x}" y2="410" stroke="{LINE}" stroke-width="2" stroke-dasharray="6,6"/>')
def msg(y,text,sub,rtl=False,col=TEAL):
    x1,x2 = (BX,AX) if rtl else (AX,BX)
    d = -1 if rtl else 1
    s.append(f'<line x1="{x1}" y1="{y}" x2="{x2-14*d}" y2="{y}" stroke="{col}" stroke-width="2.5"/>')
    s.append(f'<polygon points="{x2},{y} {x2-14*d},{y-7} {x2-14*d},{y+7}" fill="{col}"/>')
    s.append(f'<text x="{(AX+BX)/2}" y="{y-12}" fill="{col}" font-family="{F}" font-size="16" font-weight="700" text-anchor="middle">{text}</text>')
    if sub:
        s.append(f'<text x="{(AX+BX)/2}" y="{y+22}" fill="{DIM}" font-family="{S}" font-size="14" text-anchor="middle">{sub}</text>')
s.append(f'<text x="70" y="168" fill="{ORANGE}" font-family="{S}" font-size="15" font-weight="700">first</text>')
msg(168,"0x76, listen up","")
msg(228,"0xD0","the register I want")
s.append(f'<text x="70" y="316" fill="{ORANGE}" font-family="{S}" font-size="15" font-weight="700">then</text>')
msg(316,"0x76, send me one byte","")
msg(376,"0x58",None,rtl=True,col=GREEN)
s.append(f'<text x="{(AX+BX)/2}" y="398" fill="{DIM}" font-family="{S}" font-size="14" text-anchor="middle">whatever was in that register</text>')
s.append(f'<text x="{W/2}" y="{H-14}" fill="{DIM}" font-family="{S}" font-size="16" text-anchor="middle">Say which register, then ask for the contents. Two separate messages.</text>')
s.append('</svg>')
open('content/img/i2c-read.svg','w').write("\n".join(s)); print("i2c-read.svg")
