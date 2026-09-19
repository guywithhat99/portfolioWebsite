"""Generate a 'function call anatomy' diagram.

Each new function in the workshop gets one of these before it appears in code.

    python3 tools/anatomy.py

Edit CALLS at the bottom to add more.
"""
BG="#f5f3ed"; DIM="#5d6670"
C={"name":"#00767d","arg1":"#c4551a","arg2":"#1a7f4b","punct":"#5d6670",
   "semi":"#b4241f","arg3":"#6d28d9"}
F="JetBrains Mono,monospace"; S="DM Sans,sans-serif"

def anatomy(segments, callouts, out, fs=44):
    """segments: [(text, colorkey)]
       callouts: [(text, label, sub, up)] or [(text, label, sub, up, row)]

    row 0 sits nearest the code; higher rows stack further away, so adjacent
    callouts with long labels can be staggered instead of colliding.
    """
    def row_of(c): return c[4] if len(c) > 4 else 0
    up_rows   = [row_of(c) for c in callouts if c[3]]
    down_rows = [row_of(c) for c in callouts if not c[3]]
    max_up    = max(up_rows)   if up_rows   else 0
    max_down  = max(down_rows) if down_rows else 0

    LANE = 46          # vertical space per stacked row
    HEAD = 150         # space above the code for row-0 callouts
    FOOT = 150         # space below

    cw = fs*0.6
    total = sum(len(t) for t,_ in segments)*cw
    W = max(900, int(total+280))
    y = HEAD + LANE*max_up
    H = y + FOOT + LANE*max_down

    x0 = (W-total)/2
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
       f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    x=x0; pos={}
    for t,k in segments:
        esc = t.replace('&','&amp;').replace('<','&lt;')
        s.append(f'<text x="{x:.1f}" y="{y}" fill="{C[k]}" font-family="{F}" '
                 f'font-size="{fs}" font-weight="700" xml:space="preserve">{esc}</text>')
        pos[t]=(x, x+len(t)*cw, C[k]); x += len(t)*cw

    for c in callouts:
        key,label,sub,up = c[0],c[1],c[2],c[3]
        row = row_of(c)
        x1,x2,col = pos[key]
        mx=(x1+x2)/2
        if up:
            ay = y - 52 - LANE*row              # bracket
            ty = 56 + LANE*(max_up-row)         # label baseline
            stem_to = ty+14
        else:
            ay = y + 16 + LANE*row
            ty = y + 94 + LANE*row
            stem_to = ty-30
        s.append(f'<line x1="{mx:.1f}" y1="{ay:.1f}" x2="{mx:.1f}" y2="{stem_to:.1f}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<line x1="{x1+2:.1f}" y1="{ay:.1f}" x2="{x2-2:.1f}" y2="{ay:.1f}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<text x="{mx:.1f}" y="{ty:.1f}" fill="{col}" font-family="{S}" font-size="19" font-weight="700" text-anchor="middle">{label}</text>')
        s.append(f'<text x="{mx:.1f}" y="{ty+23:.1f}" fill="{DIM}" font-family="{S}" font-size="15" text-anchor="middle">{sub}</text>')
    s.append('</svg>')
    open(out,'w').write("\n".join(s))
    return out

CALLS = [
  (  # pinMode
    [("pinMode","name"),("(","punct"),("13","arg1"),(", ","punct"),("OUTPUT","arg2"),(")","punct"),(";","semi")],
    [("pinMode","the name","what you want done",True),
     ("13","which pin","the number on the board",False),
     ("OUTPUT","which direction","OUTPUT drives, INPUT reads",False,1),
     (";","semicolon","ends the line",True)],
    "content/img/fn-pinmode.svg"),
  (  # digitalWrite
    [("digitalWrite","name"),("(","punct"),("13","arg1"),(", ","punct"),("HIGH","arg2"),(")","punct"),(";","semi")],
    [("digitalWrite","the name","set a pin's voltage",True),
     ("13","which pin","the number on the board",False),
     ("HIGH","what voltage","HIGH is 5V, LOW is 0V",False,1),
     (";","semicolon","ends the line",True)],
    "content/img/fn-digitalwrite.svg"),
  (  # analogWrite
    [("analogWrite","name"),("(","punct"),("9","arg1"),(", ","punct"),("128","arg2"),(")","punct"),(";","semi")],
    [("analogWrite","sets a duty cycle","not a real voltage",True),
     ("9","which pin","must be one of the six ~ pins",False),
     ("128","how much","0 is always off, 255 is always on",False,1)],
    "content/img/fn-analogwrite.svg"),
  (  # defining a function
    [("byte","name"),(" ","punct"),("readRegister","arg1"),("(","punct"),
     ("byte reg","arg2"),(")","punct"),(" {","punct")],
    [("byte","hands back","the type of the answer",True),
     ("readRegister","the name","you choose this one",False),
     ("byte reg","what it needs","a type, then a name for it",False,1)],
    "content/img/fn-define.svg"),
]

if __name__ == "__main__":
    for segs, cos, out in CALLS:
        print("wrote", anatomy(segs, cos, out))
