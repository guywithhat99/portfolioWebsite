from lib import *

T12 = 'MODULE 12 · WIRING THE SENSOR'


def slides():
    S = []

    S.append(('m12', section_slide('m12', '12', 'Wiring the sensor', 'Six pins, one hazard, and a first question to the chip',
        'About twelve minutes including build time, so keep the explanation to about four. Hardware comes out of the bag now. Before anyone plugs anything in, the next slide is the one that saves a board.', T12)))

    # 24 warning
    tile = lambda big, cap, bg, bd, c: card(P(big, 160, c, 700, f'font-family:{MONO}; line-height:1'), bg=bg, border=bd, gap=6, extra='flex:1')
    t1 = card(M('5 V', 160, INK, 700, 'line-height:1') + P('Everything else in the kit', 36, BODY), gap=12, extra='flex:1')
    t2 = card(M('3.3 V', 160, ORG, 700, 'line-height:1') + P('The GY-BMP280 board', 36, INK, 600), bg=ORG_T, border=ORG, gap=12, extra='flex:1')
    warn = row('<x-icon name="Warning" style="color:#B34B0A; width:72px; height:72px"></x-icon>' +
               P('There is no protection on this board. Connect VCC to 5 volts and you can destroy it.', 40, INK, 600, 'flex:1'), gap=28, extra='align-items:center')
    S.append(('warning-3v3', light('warning-3v3', 'This one can be damaged',
        col(row(t1 + t2, gap=32) + warn, gap=48, extra='flex:1; justify-content:space-between'),
        'Stop and read this before anything is plugged in. Everything else in your kit runs on five volts. This sensor board runs on three point three, and there is no protection on it. If VCC goes to the five volt pin the sensor can die instantly. Build it with the USB cable unplugged. VCC goes to the pin marked 3.3V, which sits right next to 5V on the power header, so double check.', T12)))

    # 25 pins
    rows_ = [['Pin', 'Connect to', 'Why'], ['VCC', '3.3V', 'not 5V'], ['GND', 'GND', 'ground'], ['SCL', 'A5', 'the clock'],
             ['SDA', 'A4', 'the data'], ['CSB', 'nothing', 'the board holds it high: I2C mode'],
             ['SDO', 'nothing', 'the board holds it low: address 0x76']]
    tb = table(rows_, [16, 24, 60], size=30, hl={1: ORG_T, 5: PAPER2, 6: PAPER2})
    S.append(('pins', light('pins', 'Six pins, four wires',
        col(row(ph(640, 470, 'GY-BMP280 board', 'Close up, with the six pin labels on the silkscreen readable') + col(tb, extra='flex:1'), gap=48) +
            card(P('Tie SDO high instead and the same chip answers at 0x77. Most examples online assume 0x77, yours is 0x76.', 32, INK, 500), bg=ORG_T, border=ORG, pad=28),
            gap=32, extra='flex:1; justify-content:space-between'),
        'The board has six pins but we use four wires. VCC to 3.3V, ground to ground, SCL to A5, SDA to A4. Why do CSB and SDO go nowhere? The board already has resistors on them. CSB held high selects I2C rather than the other protocol this chip supports. SDO held low picks one of the two possible addresses, and that is why our address is 0x76. On a bare chip leaving them floating would be a bug, here it is correct. If SDO were tied high the chip would answer at 0x77, and most code online assumes 0x77.', T12)))

    # 26 wiring diagram
    def wr(c, t):
        return row(f'<div style="width:28px; height:28px; flex:none; background:{c}; border-radius:50%"></div>' + P(t, 32, INK, 500, 'flex:1'), gap=20, extra='align-items:center')
    right = col(wr(ORG, 'VCC to 3.3V') + wr(INK, 'GND to GND') + wr(MUTED, 'SCL to A5') + wr(BLUE, 'SDA to A4') + wr(LINE, 'CSB and SDO: nothing'), gap=20)
    chk = card(P('BEFORE THE USB CABLE GOES IN', 24, ORG, 600, 'letter-spacing:2px') +
               P('Follow the red wire with your finger. It must land on the pin marked 3.3V, next to 5V.', 32, INK, 500), bg=ORG_T, border=ORG, pad=28, gap=10)
    S.append(('wiring', light('wiring', 'Wiring it',
        row(ph(1000, 560, 'Fritzing, breadboard view', 'VCC to the Uno 3.3V pin, GND to GND, SCL to A5, SDA to A4. CSB and SDO unconnected.') +
            col(right + spacer() + chk, gap=24, extra='flex:1'), gap=48, extra='flex:1'),
        'Wire it as on the diagram, with the cable unplugged. Give people a couple of minutes. Walk the room and look at the red wire on every desk. The classic mistake is a wire in 5V because it is the neighbour of 3.3V.', T12)))

    # 27 pull-ups
    stk = lambda rail, sub, c: col(M(rail, 32, c, 700, 'text-align:center') + vline(30, c) +
                                   P('pull-up', 26, INK, 500, f'text-align:center; width:200px; background:{PAPER}; border:3px solid {c}; border-radius:8px; padding:10px 0') +
                                   P(sub, 24, BODY, 400, 'text-align:center; width:200px') + vline(30, c), gap=4, extra='align-items:center')
    dia = card(row(stk('5 V', 'inside the Arduino', ORG) + stk('3.3 V', 'on the sensor board', BLUE), gap=60, extra='justify-content:center') +
               div('', f'height:8px; background:{BLUE}; border-radius:4px') +
               P('SDA sits between two voltages, higher than the sensor would like.', 28, BODY, 400, 'text-align:center'), gap=14, extra='width:660px')
    rt = col(P('Turning them off', 32, INK, 600) +
             code(['Wire.begin();', 'digitalWrite(SDA, LOW);', 'digitalWrite(SCL, LOW);'], size=30) +
             P('On these chips, writing LOW to a pin that is set as an input switches its pull-up off. Now only the 3.3 volt resistors on the sensor board pull the line high.', 30, BODY),
             gap=20, extra='flex:1')
    S.append(('pullups', light('pullups', 'Two sets of pull-ups',
        row(dia + rt, gap=48, extra='flex:1; align-items:center'),
        'One more thing, in software. The Arduino has its own pull-up resistors on the I2C pins, and they pull toward five volts. Your sensor board already has pull-ups to three point three. Leave both on and the line sits higher than the sensor would like. So right after Wire.begin we write LOW to both pins. On these chips, writing LOW to a pin set as an input switches its internal pull-up off. Now only the sensor board resistors pull the line up.', T12)))

    # 28 is anything there
    cd = code(['Wire.beginTransmission(0x76);', 'byte answer = Wire.endTransmission();', '',
               'Serial.println(answer == 0', '    ? "Something is there"', '    : "Nothing answered");'], size=28, width=760, extra='flex:none')
    res = col(card(M('0', 64, ORG, 700) + P('A chip pulled SDA low: it acknowledged. Something is there.', 30, INK), bg=ORG_T, border=ORG, gap=8) +
              card(P('anything else', 40, INK, 700) + P('Nobody pulled the line low. Nothing answered.', 30, INK), gap=8) +
              P('This is the ACK bit from module 11, surfaced as a number.', 30, BODY, 500), gap=20, extra='flex:1')
    S.append(('ack-check', light('ack-check', 'Is anything there?',
        row(cd + res, gap=48, extra='flex:1; align-items:center'),
        'We do not need to read a register yet. We can just ask whether anything answers at that address. beginTransmission followed by endTransmission sends an address and nothing else. endTransmission returns a status. Zero means a chip pulled the line low to acknowledge. Anything else means nobody did. That is exactly the ACK bit from the last module, turned into a number your code can test. Remember the paper exercise: no ACK means the line stayed high.', T12)))

    # 29 your turn
    S.append(('turn-wire', dark_turn('turn-wire', 'Wire it and ask', [
        'Wire four jumpers: VCC to 3.3V, GND to GND, SCL to A5, SDA to A4.',
        'Follow the red wire with your finger before the USB cable goes in.',
        'Upload the address check and open the Serial Monitor at 9600.'],
        'This is the longest stop. Give it eight minutes and expect to spend most of it walking around. The next slide is the troubleshooting order, keep it ready. If someone gets Nothing answered, ask them to check A4 and A5 first, then the 3.3V wire, then try 0x77.',
        T12, answer='Something is there', minutes='8 MIN')))

    # 30 troubleshooting
    tb = table([['What you see', 'Check, in this order'],
                ['Nothing reported at all', 'SDA and SCL swapped. They are A4 and A5, and it is easy to reverse them.'],
                ['Still nothing', 'The 3.3V wire is really in 3.3V and the ground wire is connected. A sensor with no ground cannot answer.'],
                ['Wiring looks right, nothing answered', 'Try 0x77 instead. Some boards tie SDO the other way.'],
                ['It worked once and now does not', 'If the board ever saw 5 volts on VCC it may be dead. Swap it and check the wiring again.']],
               [38, 62], size=30, hl={2: PAPER2, 4: PAPER2})
    S.append(('nothing-answers', light('nothing-answers', 'If nothing answers', col(tb, extra='flex:1'),
        'Leave this slide up while people debug. Work down the list in order. Almost every failure is one of the first two rows.', T12)))
    return S
