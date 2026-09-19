"""Byte level I2C frames with every box explained in words."""
BG="#f5f3ed"; DIM="#5d6670"; TEXT="#1b1e22"; LINE="#d9d3c7"
TEAL="#00767d"; GREEN="#1a7f4b"; RED="#b4241f"
S="DM Sans,sans-serif"; F="JetBrains Mono,monospace"

def strip(s, x0, y, items):
    x = x0
    for label, w, who, c1, c2 in items:
        col = RED if who == "e" else (GREEN if who == "s" else TEAL)
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="56" rx="7" fill="{col}" opacity=".14"/>')
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="56" rx="7" fill="none" stroke="{col}" stroke-width="2"/>')
        fs = 18 if len(label) <= 4 else 16
        s.append(f'<text x="{x+w/2}" y="{y+36}" fill="{col}" font-family="{F}" font-size="{fs}" font-weight="700" text-anchor="middle">{label}</text>')
        if c1: s.append(f'<text x="{x+w/2}" y="{y+78}" fill="{DIM}" font-family="{S}" font-size="13" text-anchor="middle">{c1}</text>')
        if c2: s.append(f'<text x="{x+w/2}" y="{y+95}" fill="{DIM}" font-family="{S}" font-size="13" text-anchor="middle">{c2}</text>')
        x += w + 7
    return x

WRITE = [("S",56,"e","start",""),
         ("0x76 + W",170,"m","chip 0x76,","I am writing"),
         ("ACK",76,"s","chip:","I am here"),
         ("0xF4",118,"m","which","register"),
         ("ACK",76,"s","chip:","got it"),
         ("0x27",118,"m","the value","to put in it"),
         ("ACK",76,"s","chip:","got it"),
         ("P",56,"e","stop","")]

# ---------- writing ----------
W,H=960,300
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="42" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Writing a register is one message</text>')
strip(s, 60, 86, WRITE)
s.append(f'<text x="{W/2}" y="250" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">The register number and the value travel together.</text>')
s.append(f'<text x="{W/2}" y="276" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">Blue is the Arduino talking, green is the sensor answering.</text>')
s.append('</svg>')
open('content/img/write-frame.svg','w').write("\n".join(s)); print("write-frame.svg")

# ---------- reading ----------
M1 = [("S",56,"e","start",""),
      ("0x76 + W",170,"m","chip 0x76,","I am writing"),
      ("ACK",76,"s","chip:","I am here"),
      ("0xD0",118,"m","which","register"),
      ("ACK",76,"s","chip:","got it"),
      ("P",56,"e","stop","")]
M2 = [("S",56,"e","start",""),
      ("0x76 + R",170,"m","chip 0x76,","I am reading"),
      ("ACK",76,"s","chip:","I am here"),
      ("0x58",118,"s","the sensor","sends the byte"),
      ("NACK",84,"m","that is all","I wanted"),
      ("P",56,"e","stop","")]
W,H=960,420
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
s.append(f'<text x="{W/2}" y="40" fill="{TEXT}" font-family="{S}" font-size="20" font-weight="700" text-anchor="middle">Reading one takes two</text>')
s.append(f'<text x="60" y="94" fill="{TEXT}" font-family="{S}" font-size="15" font-weight="700">First</text>')
strip(s, 130, 70, M1)
s.append(f'<text x="60" y="254" fill="{TEXT}" font-family="{S}" font-size="15" font-weight="700">Then</text>')
strip(s, 130, 230, M2)
s.append(f'<text x="{W/2}" y="376" fill="{TEXT}" font-family="{S}" font-size="17" font-weight="700" text-anchor="middle">The first message says which register. The second collects it.</text>')
s.append(f'<text x="{W/2}" y="402" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">In between, the direction on the wire has to reverse.</text>')
s.append('</svg>')
open('content/img/read-frame.svg','w').write("\n".join(s)); print("read-frame.svg")
