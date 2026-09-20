from lib import *

T13 = 'MODULE 13 · READING A REGISTER'


def slides():
    S = []

    S.append(('m13', section_slide('m13', '13', 'Reading a register', 'Two messages, one helper function, and a known answer',
        'About ten minutes. We already know one register whose answer is known in advance. That makes it the perfect first read.', T13)))

    # 32 chip id
    t1 = card(M('0xD0', 140, BLUE, 700, 'line-height:1') + P('the register we ask', 36, BODY), bg=BLUE_T, border=BLUE, gap=12, extra='flex:1')
    t2 = card(M('0x58', 140, ORG, 700, 'line-height:1') + P('the answer the chip should give', 36, BODY), bg=ORG_T, border=ORG, gap=12, extra='flex:1')
    ar = div('<x-shape kind="arrow-right" style="width:120px; height:60px; background:#66707D"></x-shape>', 'flex:none')
    S.append(('chip-id', light('chip-id', 'A register with a known answer',
        col(row(t1 + ar + t2, gap=32, extra='align-items:center') +
            P('It is the one register where the answer is known in advance. A correct answer means the wiring, the address, the bus and the read are all right.', 36, INK, 500),
            gap=48, extra='flex:1; justify-content:space-between'),
        'From Table 18 we know register 0xD0 is the chip ID and it should read 0x58. It is the one register where we know the answer before we ask. So if we get 0x58 back, everything works: the wiring, the address, the bus, and the read. That makes it a perfect first test.', T13)))

    # 33 sequence diagram
    hdr = lambda left, name: pin(P(name, 32, INK, 700, 'text-align:center'), left, 0, 280, 70, f'background:{PAPER2}; border:3px solid {INK}; border-radius:14px; display:flex; flex-direction:column; justify-content:center')
    lab = lambda t, top, c: pinp(t, 380, top, 900, 30, c, 600, 'center')
    parts = [
        conn(340, 76, 340, 590, MUTED, 4, dash=True), conn(1324, 76, 1324, 590, MUTED, 4, dash=True),
        hdr(200, 'Arduino'), hdr(1184, 'BMP280'),
        conn(350, 170, 1314, 170, BLUE, 5, 'end'), lab('0xEC : address, write', 124, BLUE),
        conn(350, 250, 1314, 250, BLUE, 5, 'end'), lab('0xD0 : the register number', 204, BLUE),
        conn(60, 330, 1604, 330, LINE, 3, dash=True),
        conn(350, 420, 1314, 420, BLUE, 5, 'end'), lab('0xED : address, read', 374, BLUE),
        conn(1314, 510, 350, 510, ORG, 5, 'end'), lab('0x58 : the data comes back', 464, ORG),
        pinp('Message one', 0, 186, 190, 26, INK, 700), pinp('Message two', 0, 440, 190, 26, INK, 700),
        pinp('The chip remembers 0xD0', 1380, 176, 280, 26, BODY),
    ]
    S.append(('read-two-messages', light('read-two-messages', 'It takes two messages', host(''.join(parts), 1664, 600),
        'Here is the read as a sequence. Message one: the Arduino addresses the chip with the write bit, 0xEC on the wire, then sends the register number 0xD0. The chip stores it. Message two: the Arduino addresses the chip with the read bit, 0xED, and this time the chip sends the byte back. Blue is the Arduino talking, orange is the chip talking. ACKs are in there too, they are just left out to keep the picture clean.', T13)))

    # 34 wire calls
    calls = [('Wire.beginTransmission(0x76)', 'buffer', 'Starts a buffer. Nothing is sent yet.'),
             ('Wire.write(0xD0)', 'buffer', 'Adds a byte to the buffer. Still nothing on the wire.'),
             ('Wire.endTransmission()', 'wire', 'Puts the whole buffer on the wire. Returns 0 if a chip acknowledged.'),
             ('Wire.requestFrom(0x76, 1)', 'wire', 'Sends the read message and collects the reply. 1 is the byte count.'),
             ('Wire.read()', 'buffer', 'Takes one byte out of what arrived.')]
    rr = ''
    for c, k, d in calls:
        tag = pill('fills a buffer', PAPER2, INK, LINE, 26, 500, extra='width:220px; text-align:center') if k == 'buffer' else \
              pill('on the wire', BLUE_T, INK, BLUE, 26, 600, extra='width:220px; text-align:center')
        rr += row(M(c, 28, INK, 500, 'width:610px; flex:none') + div(tag, 'flex:none') + P(d, 28, BODY, 400, 'flex:1'), gap=24,
                  extra=f'align-items:center; background:{PAPER2}; border:2px solid {LINE}; border-radius:14px; padding:16px 28px')
    S.append(('wire-calls', light('wire-calls', 'What each Wire call really does',
        col(col(rr, gap=12) + P('The names describe what the calls are for, not what they do.', 36, INK, 600), gap=32, extra='flex:1; justify-content:space-between'),
        'Here is a confusing thing about the Wire library. beginTransmission does not begin a transmission, and write does not write anything. Both just put bytes in a buffer. endTransmission is the call that actually puts all of it on the wire. requestFrom sends the read message and collects the reply, and read pulls a byte out of what arrived. The names describe what the calls are for, not what they do. If you remember one thing: nothing moves until endTransmission or requestFrom.', T13)))

    # 35 function anatomy
    def span(t, c, b=False):
        w = ' font-weight:700;' if b else ''
        return f'<span style="color:{c};{w}">{esc(t)}</span>'
    def L(inner, ind=0, size=32):
        return f'<p style="font-family:{MONO}; font-size:{size}px; line-height:1.45; white-space:nowrap; color:{INK}; padding:0 12px 0 {int(ind * size * 0.6) + 12}px">{inner}</p>'
    lines = [L(span('byte', BLUE) + ' ' + span('readRegister', INK, True) + '(' + span('byte reg', ORG) + ') {')]
    for t in ['Wire.beginTransmission(0x76);', 'Wire.write(reg);', 'Wire.endTransmission();', 'Wire.requestFrom(0x76, 1);']:
        lines.append(L(esc(t), 4))
    lines.append(L(span('return', GRN, True) + ' Wire.read();', 4))
    lines.append(L('}'))
    cpanel = div(''.join(lines), f'background:#ECEAE0; border:2px solid {LINE}; border-radius:16px; padding:22px 16px; display:flex; flex-direction:column')
    use = row(code(['byte id = readRegister(0xD0);'], size=32, pad=24, extra='flex:none') + P('One line instead of four.', 32, INK, 600), gap=28, extra='align-items:center')
    leg = lambda w_, c, t, b=False: col(M(w_, 32, c, 700), gap=2) + P(t, 28, BODY)
    legend = col(
        col(M('byte', 32, BLUE, 700) + P('What it hands back. void means nothing, int means a whole number.', 28, BODY), gap=2) +
        col(M('readRegister', 32, INK, 700) + P('Your name for it.', 28, BODY), gap=2) +
        col(M('byte reg', 32, ORG, 700) + P('What you give it. reg stands in for whichever register is wanted.', 28, BODY), gap=2) +
        col(M('return', 32, GRN, 700) + P('Hands a value back and ends the function.', 28, BODY), gap=2),
        gap=22, extra='flex:1')
    S.append(('function-anatomy', light('function-anatomy', 'Writing your own function',
        row(col(cpanel + use, gap=28, extra='width:900px; flex:none') + legend, gap=56, extra='flex:1; align-items:center'),
        'Reading any register is the same four steps, only the register number changes. There are a dozen registers worth reading in this sensor, and copying four lines a dozen times is a dozen chances to typo. So we give it a name. You have been filling in setup and loop since day one, both are functions, the Arduino just wrote the outside for you. The first word is what it hands back. void, which you have typed since module 2, means nothing. Our function hands back a byte. Then the name, then what it takes in, then the body. return hands the value back and ends the function.', T13)))

    # 36 whole program
    left = code(['#include <Wire.h>', '', 'byte readRegister(byte reg) {', '    Wire.beginTransmission(0x76);', '    Wire.write(reg);',
                 '    Wire.endTransmission();', '    Wire.requestFrom(0x76, 1);', '    return Wire.read();', '}'], size=26, extra='flex:1')
    right = code(['void setup() {', '    Serial.begin(9600);', '    Wire.begin();', '    digitalWrite(SDA, LOW);', '    digitalWrite(SCL, LOW);', '',
                  '    byte id = readRegister(0xD0);', '    Serial.print("Chip ID: 0x");', '    Serial.println(id, HEX);', '}', '', 'void loop() {', '}'], size=26, extra='flex:1')
    S.append(('whole-program', light('whole-program', 'The whole program',
        col(row(left + right, gap=32, extra='align-items:flex-start') +
            P('The helper sits above setup, like a variable does. println(id, HEX) prints in hex, so it matches the datasheet. Expect: Chip ID: 0x58', 30, BODY),
            gap=28, extra='flex:1; justify-content:space-between'),
        'Here is everything together. The helper goes above setup. In setup we start Serial, start Wire, switch the pull-ups off like before, read register 0xD0, and print it in hex so it matches what the datasheet says. Loop is empty, we only need to do this once. What you expect to see is Chip ID: 0x58.', T13)))

    # 37 your turn
    S.append(('turn-chipid', dark_turn('turn-chipid', 'Ask it who it is', [
        'Add readRegister above setup.',
        'In setup, read register 0xD0 and print it in hex.',
        'Upload it and open the Serial Monitor at 9600.'],
        'Five minutes. Most people just retype the slide, which is fine. The reward is seeing 0x58 appear. If someone gets 0x60 they have a BME280, see the next slide, and everything else still works for them.',
        T13, answer='Chip ID: 0x58', minutes='5 MIN')))

    # 38 wrong id
    tb = table([['You see', 'It means'],
                ['0x60', 'You have a BME280, not a BMP280. Same board, slightly different chip that also measures humidity. Everything after this still works.'],
                ['0x0 or 0xFF', 'Nothing is answering. Go back and check that the address check still passes.'],
                ['Nothing prints', 'The Serial Monitor is not set to 9600.'],
                ['A different number every run', 'A loose wire. Press the sensor firmly into the breadboard.']],
               [30, 70], size=30, hl={2: PAPER2, 4: PAPER2})
    S.append(('wrong-id', light('wrong-id', 'If a different number came back', col(tb, extra='flex:1'),
        'Match what you see to a row. 0x60 is not a failure, it is a BME280 that shipped on a board labelled BMP280. Same registers for everything we do today.', T13)))

    # 39 statement
    S.append(('same-method', f'''<section id="same-method" data-transition="fade" style="background:{BLUE}; color:{PAPER}; font-family:{SANS}; padding:128px; display:flex; flex-direction:column; justify-content:center; gap:48px">
<p style="font-size:64px; font-weight:600; line-height:1.2; color:{PAPER}; width:1500px">You sent bytes to a silicon device using nothing but the document describing it, and got back exactly what that document promised.</p>
<p style="font-size:40px; line-height:1.35; color:#DCE6F8; width:1200px">Every sensor on the rocket works this way. The registers differ, the method does not.</p>
<aside>{esc("Pause here. This is the moment the whole session has been building toward. You used a PDF to talk to a piece of silicon. Every IMU, barometer and magnetometer on the flight computer is this exact conversation with a different register table. Let that land before moving on.")}</aside></section>'''))
    return S
