from lib import *

T11 = 'MODULE 11 · HOW TWO WIRES CARRY THAT'


def slides():
    S = []

    S.append(('m11', section_slide('m11', '11', 'How two wires carry that', 'The bus, the one rule, and one whole message',
        'About fifteen minutes, and this is the heart of the session. Take it slowly. The payoff is that by the end you can read a logic analyzer trace and know exactly which bit you are looking at.', T11)))

    # 13 bus
    def dev(left, name, sub, dashed=False):
        st = f'background:{PAPER2}; border:3px {"dashed" if dashed else "solid"} {INK}; border-radius:16px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:4px'
        return pin(P(name, 32, INK, 700, 'text-align:center') + P(sub, 26, BODY, 400, 'text-align:center'), left, 250, 300, 140, st)
    parts = [
        conn(100, 150, 1430, 150, MUTED, 6), conn(100, 520, 1590, 520, BLUE, 6),
        dev(40, 'Arduino', 'the controller'), dev(520, 'BMP280', 'address 0x76'), dev(1000, 'Another chip', 'its own address', True),
    ]
    for c in (190, 670, 1150):
        parts.append(conn(c, 250, c, 150, MUTED, 6))
        parts.append(conn(c, 390, c, 520, BLUE, 6))
    parts += [
        conn(1430, 30, 1590, 30, INK, 6), pinp('3.3 V', 1290, 10, 120, 28, INK, 700, 'right', True),
        conn(1430, 30, 1430, 64, INK, 6),
        pin(P('pull-up', 26, INK, 500, 'text-align:center'), 1365, 64, 130, 56, f'background:{PAPER2}; border:3px solid {INK}; border-radius:8px; display:flex; flex-direction:column; justify-content:center'),
        conn(1430, 120, 1430, 150, INK, 6),
        conn(1590, 30, 1590, 290, INK, 6),
        pin(P('pull-up', 26, INK, 500, 'text-align:center'), 1525, 290, 130, 56, f'background:{PAPER2}; border:3px solid {INK}; border-radius:8px; display:flex; flex-direction:column; justify-content:center'),
        conn(1590, 346, 1590, 520, INK, 6),
        pinp('SCL: the clock', 240, 96, 500, 30, MUTED, 600), pinp('SDA: the data', 240, 545, 500, 30, BLUE, 600),
        pinp('Resistors hold both wires high until a chip pulls one low.', 1000, 585, 660, 26, BODY),
    ]
    S.append(('bus', light('bus', 'One bus, many chips', host(''.join(parts), 1664, 640),
        'Here is the whole physical picture. Every chip on the bus shares the same two wires. One is the clock, SCL. One is the data, SDA. The controller, our Arduino, runs the clock and starts every conversation. Other chips listen for their own address. Notice the two resistors on the right: they connect each wire to the supply. Hold that thought, because it explains why I2C is safe to wire up in parallel.', T11)))

    # 14 two wires
    wcard = lambda nm, pin_, c, txt, bg, bd: card(row(M(nm, 64, c, 700) + pill(pin_, PAPER, INK, bd, 28, 600), gap=20, extra='align-items:center') + P(txt, 32, BODY), bg=bg, border=bd, gap=12, extra='flex:1')
    top = row(wcard('SDA', 'A4 on the Uno', BLUE, 'The data, one bit at a time.', BLUE_T, BLUE) +
              wcard('SCL', 'A5 on the Uno', MUTED, 'A clock, so both ends agree when each bit counts.', PAPER2, LINE), gap=32)
    box = lambda t, s, bg, bd, w_: card(P(t, 36, INK, 600, 'text-align:center') + P(s, 28, BODY, 400, 'text-align:center'), bg=bg, border=bd, pad=28, gap=8, extra=f'width:{w_}px; align-items:center')
    arr = div('<x-shape kind="arrow-right" style="width:72px; height:36px; background:#66707D"></x-shape>', 'flex:none')
    chain = row(box('Your code', 'hands over a byte', PAPER2, LINE, 380) + arr +
                box('I2C hardware block', 'makes the clock, shifts the bits, watches for the ACK', BLUE_T, BLUE, 620) + arr +
                box('Pads A4 and A5', 'wired to the silicon', PAPER2, LINE, 380), gap=24, extra='align-items:center; justify-content:space-between')
    S.append(('two-wires', light('two-wires', 'Two wires, two fixed pins',
        col(top + chain + P('digitalWrite is an instruction, so any pin will do. I2C is not your code: it is a separate circuit wired to two pads, so pinMode or digitalWrite on A4 or A5 will fight it.', 30, BODY), gap=40, extra='flex:1; justify-content:space-between'),
        'Two wires: SDA carries the data one bit at a time, SCL is the clock so both ends agree when a bit counts. On the Uno they are fixed at A4 and A5. Why fixed? Every pin so far was driven by your code, digitalWrite is an instruction so any pin works. I2C is different. There is a separate circuit inside the chip that generates the clock, shifts the bits, and watches for the ACK. That circuit is wired to two specific pads. Your code hands over a byte and gets on with its life. It also means those two pins are spoken for.', T11)))

    # 15 open drain
    def panel(title, node, node_bg, node_bd, sw_txt, sw_bg, sw_bd, sw_dash, top_c, bot_c, note):
        return card(
            P(title, 32, INK, 600, 'text-align:center') +
            col(M('3.3 V', 28, INK, 700, 'text-align:center') + vline(28, INK) +
                P('pull-up resistor', 26, INK, 500, f'text-align:center; width:280px; background:{PAPER}; border:3px solid {INK}; border-radius:8px; padding:10px 0') +
                vline(32, top_c) +
                P(node, 32, INK, 700, f'text-align:center; width:280px; background:{node_bg}; border:3px solid {node_bd}; border-radius:999px; padding:10px 0; font-family:{MONO}') +
                vline(32, bot_c) +
                P(sw_txt, 26, INK, 500, f'text-align:center; width:280px; background:{sw_bg}; border:3px {"dashed" if sw_dash else "solid"} {sw_bd}; border-radius:8px; padding:12px 0') +
                vline(28, bot_c) + M('GND', 28, INK, 700, 'text-align:center'),
                gap=0, extra='align-items:center') +
            P(note, 28, BODY, 400, 'text-align:center'),
            gap=20, extra='flex:1; align-items:stretch')
    a = panel('No chip pulling', 'SDA = 1', BLUE_T, BLUE, 'chip switch: open', PAPER2, MUTED, True, BLUE, LINE, 'The resistor pulls the line up to 3.3 V.')
    b = panel('A chip pulls low', 'SDA = 0', ORG_T, ORG, 'chip switch: closed', ORG_T, ORG, False, LINE, ORG, 'The chip connects the line to ground.')
    S.append(('open-drain', light('open-drain', 'Nobody drives the line high',
        col(row(a + b, gap=32, extra='flex:1') + P('Chips only pull the line low, or let go. If two talk at once the worst case is a garbled message, not a burnt chip.', 32, INK, 600), gap=32, extra='flex:1'),
        'This is the electrical trick. No chip ever pushes the line high. A chip can only do two things: connect the line to ground, or let go. Letting go means the pull-up resistor drags the line high. So a one is really nobody doing anything. If two chips talk at once, one pulling low and another pushing high, they would fight and something would burn out. Since nothing ever pushes, the worst case is a garbled message. That is why you can hang many chips on one bus without thinking hard.', T11)))

    # 16 the rule
    slots = [1, 0, 0, 1, 1]
    wv, W, x0 = wave(slots, 220, bands=True)
    digs = row(empty(128) + ''.join(P(str(v), 40, BLUE, 700, f'font-family:{MONO}; width:220px; text-align:center') for v in slots), gap=0)
    sw = lambda bg, bd: f'<div style="width:44px; height:44px; flex:none; background:{bg}; border:3px solid {bd}; border-radius:8px"></div>'
    legend = row(row(sw(BLUE_T, BLUE) + P('SCL high: SDA holds still. This is when each bit counts.', 30, INK, 500, 'flex:1'), gap=20, extra='flex:1; align-items:center') +
                 row(sw(PAPER, LINE) + P('SCL low: SDA is free to change.', 30, INK, 500, 'flex:1'), gap=20, extra='flex:1; align-items:center'), gap=48)
    S.append(('rule', light('rule', 'SDA may only change while SCL is low',
        col(col(wv + digs, gap=8) + legend, gap=40, extra='flex:1; justify-content:space-between'),
        'One rule makes the whole protocol work. SDA is only allowed to change while SCL is low. Each bit is set up during the low half of the clock and read during the high half. So the blue bands are when the receiver looks at the line, and the line must sit still. Look at the trace: SDA moves only in the gaps between blue bands. If SDA ever changes while SCL is high, that cannot be data, and that is exactly what we use to mark the start and the end of a message.', T11)))

    # 17 start stop
    def ss(kind, name, txt):
        return card(mini_edge(kind) + P(name, 44, INK, 700) + P(txt, 32, BODY) + P('Reserved: it can never be data.', 28, MUTED), gap=10, extra='flex:1')
    S.append(('start-stop', light('start-stop', 'START and STOP break the rule on purpose',
        col(row(ss('start', 'START', 'SDA falls while SCL is high.') + ss('stop', 'STOP', 'SDA rises while SCL is high.'), gap=32) +
            P('Two signals, and that one rule, is the whole protocol.', 40, INK, 600), gap=40, extra='flex:1; justify-content:space-between'),
        'START and STOP are the two exceptions. Falling on SDA while SCL is high means START, a message begins. Rising on SDA while SCL is high means STOP, the message is over. Because data never changes while the clock is high, these cannot be mistaken for data. That is the trick. Two signals and one rule is genuinely the whole protocol.', T11)))

    # 18 frame blocks
    segs = [('1', 'START', 170, FD, 'SDA falls while SCL is high'),
            ('2', 'Address', 380, FB, 'Seven bits: 0x76, most significant first'),
            ('3', 'R/W', 150, FB, '0 means write'),
            ('4', 'ACK', 150, FO, 'The chip pulls SDA low: I am here'),
            ('5', 'Data', 380, FB, 'Eight bits: 0xD0, the register wanted'),
            ('6', 'ACK', 150, FO, 'The chip acknowledges again'),
            ('7', 'STOP', 170, FD, 'SDA rises while SCL is high')]
    bl = ''.join(P(f'{n}', 24, fg if bg == INK else BODY, 600, f'width:{w_}px; text-align:center; font-family:{MONO}') for n, _, w_, (bg, bd, fg), _ in segs)
    bl = row(''.join(col(P(n, 24, MUTED, 600, f'text-align:center; font-family:{MONO}') +
                         P(t, 32, fg, 600, f'text-align:center; background:{bg}; border:2px solid {bd}; border-radius:10px; padding:26px 0; line-height:1.2') +
                         P(d, 24, BODY, 400, 'text-align:center; line-height:1.3'), gap=10, extra=f'width:{w_}px; flex:none')
                     for n, t, w_, (bg, bd, fg), d in segs), gap=8)
    leg = row(row(sw(BLUE_T, BLUE) + P('sent by the Arduino', 28, BODY), gap=14, extra='align-items:center') +
              row(sw(ORG_T, ORG) + P('sent by the chip', 28, BODY), gap=14, extra='align-items:center'), gap=48)
    S.append(('frame', light('frame', 'One whole message',
        col(bl + leg + card(P('No ACK at step 4 means nothing is at that address.', 40, INK, 600), bg=BLUE_T, border=BLUE, pad=32), gap=36, extra='flex:1; justify-content:space-between'),
        'Now the full sequence, in the order it happens. One: START. Two: seven address bits, 0x76, most significant bit first. Three: one read or write bit, zero for write. Four: the ACK. The chip pulls SDA low to say it is there. Five: eight data bits. In this message that is 0xD0, the register we want. Six: another ACK. Seven: STOP. The orange blocks are the only ones the chip sends. If step four never happens, nobody is home at that address, which we will use for a very handy test.', T11)))

    # 19 frame bits on the wire
    fs = [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
    wv, W, x0 = wave(fs, 72, start=True, stop=True, ack=(8, 17))
    hd = lambda t, w_, bg, fg: P(t, 24, fg, 600, f'width:{w_}px; text-align:center; background:{bg}; padding:12px 0; line-height:1.3')
    strip = row(empty(128) + hd('Start', 72, INK, PAPER) + hd('Address 0x76', 504, BLUE_T, INK) + hd('R/W', 72, BLUE, PAPER) +
                hd('ACK', 72, ORG_T, ORG) + hd('Data 0xD0', 576, BLUE_T, INK) + hd('ACK', 72, ORG_T, ORG) + hd('Stop', 72, INK, PAPER), gap=0)
    dg = row(empty(128 + 72) + ''.join(P(str(v), 32, ORG if i in (8, 17) else BLUE, 700, f'font-family:{MONO}; width:72px; text-align:center') for i, v in enumerate(fs)), gap=0)
    S.append(('frame-bits', light('frame-bits', 'The same message on the wire',
        col(col(strip + wv + dg, gap=8) + P('The Arduino sends 0x76 and 0xD0. The chip only ever answers with ACKs, the orange dips.', 32, BODY), gap=32, extra='flex:1; justify-content:space-between'),
        'Here is the same message as a real trace. SDA is blue, SCL is gray. START: SDA drops while the clock is high. Then seven address bits, 1110110, which is 0x76. Then a zero for write. Then the ninth clock: the chip pulls SDA low, that orange dip is the ACK. Then eight bits, 11010000, which is 0xD0. Another ACK. Then SDA rises while the clock is high, and that is STOP. If you ever put a logic analyzer on a real bus, this is what you will see.', T11)))

    # 20 address byte
    ab = lambda rw, lab, val: row(P(lab, 32, INK, 600, 'width:120px; padding:14px 0 0 0') +
                                   bits('1110110' + rw, [(7, FB), (1, FD)], w=72, size=40, pad=14) +
                                   M('= ' + val, 56, INK, 700, 'padding:0 0 0 24px'), gap=24, extra='align-items:center')
    cap = row(empty(144) + P('7 address bits: 0x76', 28, BLUE, 600, 'width:540px; text-align:center') + P('R/W', 28, INK, 600, 'width:72px; text-align:center; padding:0 0 0 6px'), gap=6)
    S.append(('address-byte', light('address-byte', 'The address and R/W are one byte',
        col(col(cap + ab('0', 'write', '0xEC') + ab('1', 'read', '0xED'), gap=20) +
            P('0x76 shifted up one place, with the R/W bit added below it.', 32, BODY) +
            card(P('Some datasheets quote 0x76, some quote the shifted byte. If an address looks twice what you expected, that is why.', 32, INK, 500), bg=ORG_T, border=ORG, pad=32),
            gap=32, extra='flex:1; justify-content:space-between'),
        'One subtlety that bites people. The seven address bits and the read or write bit are not two separate things on the wire, they are one byte sent together. 0x76 with write is 0xEC. The same address with read is 0xED. Some datasheets quote the seven bit address, some quote the shifted byte. If an address looks about twice what you expected, this is why. Arduino Wire wants the seven bit form, so we use 0x76.', T11)))

    # 21 two messages
    def msg(title, lines, pills, note):
        return row(col(P(title, 24, MUTED, 600, 'letter-spacing:3px') + code(lines, size=28, pad=24), gap=10, extra='width:720px; flex:none') +
                   col(P(note, 28, BODY) + row(pills, gap=10, extra='flex-wrap:wrap'), gap=14, extra='flex:1; justify-content:center'), gap=40, extra='align-items:center')
    pb = lambda t: pill(t, BLUE_T, INK, BLUE, 28, 500)
    po = lambda t: pill(t, ORG_T, INK, ORG, 28, 500)
    m1 = msg('MESSAGE ONE', ['Wire.beginTransmission(0x76);', 'Wire.write(0xD0);', 'Wire.endTransmission();'],
             pb('START') + pb('0xEC') + po('ACK') + pb('0xD0') + po('ACK') + pb('STOP'), 'Tell the chip which register. It remembers.')
    m2 = msg('MESSAGE TWO', ['Wire.requestFrom(0x76, 1);', 'byte value = Wire.read();'],
             pb('START') + pb('0xED') + po('ACK') + po('8 data bits'), 'The direction flips. Same wires, the chip talks.')
    S.append(('two-messages', light('two-messages', 'Reading takes two messages',
        col(m1 + m2 + P('You never set the R/W bit yourself. The call you choose sets it.', 32, INK, 600), gap=36, extra='flex:1; justify-content:space-between'),
        'Why does reading a register take two messages? The first message ended in STOP and only told the chip which register we want. The chip remembers it. The second message starts again with the read bit set, and now the chip drives the eight data bits while the Arduino clocks them. The direction flips on the same wires. That is exactly why the code has two halves. beginTransmission and write set the write bit. requestFrom sets the read bit. You never touch the R/W bit yourself.', T11)))

    # 22 your turn
    S.append(('turn-paper', dark_turn('turn-paper', 'Decode it on paper', [
        'Turn 0x76 into its seven address bits.',
        'Write the address byte for a write, and for a read.',
        'Sketch SDA and SCL for the frame that asks for register 0xD0.',
        'What does SDA do at the ACK slot if nothing is at 0x76?'],
        'Pen and paper, three minutes, work in pairs. Answers: 0x76 is 1110110. The bytes are 0xEC and 0xED. For the last one, nobody pulls the line low, so the pull-up resistor holds it high and there is no ACK. Point out that this is how the address check in the next module works.',
        T11, answer='1110110 · 0xEC and 0xED · SDA stays high, so no ACK', minutes='3 MIN')))
    return S
