"""Slides taken from the older deck instead of the generated default.

Each entry is  id -> function(lib) -> html string.
build.py swaps these in by id, so the rest of the deck regenerates normally.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from lib import *

T10 = 'MODULE 10 · INSIDE A CHIP'
T11 = 'MODULE 11 · HOW TWO WIRES CARRY THAT'
T12 = 'MODULE 12 · WIRING THE SENSOR'
T14 = 'MODULE 14 · WRITING A REGISTER'
T15 = 'MODULE 15 · READING THE MEASUREMENT'
T16 = 'MODULE 16 · TURNING IT INTO A TEMPERATURE'


def img(src, h, alt):
    return (f'<img src="{src}" alt="{alt}" style="display:block; margin:0 auto; '
            f'max-height:{h}px; max-width:100%; height:auto">')


def two_addresses():
    """Old deck's drawing, new deck's two cards and closing line."""
    two = row(card(M('0x76', 48, BLUE, 700) +
                   P('Which chip is being spoken to. Set by the hardware, by a resistor on the board.', 30, BODY),
                   gap=8, extra='flex:1') +
              card(M('0xD0', 48, ORG, 700) +
                   P("Which register inside that chip. Set by the chip's designers, listed in Table 18.", 30, BODY),
                   gap=8, extra='flex:1'), gap=32)
    return light('two-addresses', 'Two kinds of address',
        col(img('img/two-addresses.svg', 430, 'The bus address picks the chip, the register address picks a byte inside it')
            + two
            + P('Both are hex, both are one byte, and they mean completely different things.', 32, INK, 600),
            gap=28, extra='flex:1; justify-content:center'),
        'One trap before we leave this module. There are two addresses in play and they look identical. 0x76 is the device address, which chip on the wires. It is set by hardware, in this case a resistor on the sensor board. 0xD0 is a register address, which byte inside that chip, and it comes from Table 18. Both are one byte in hex. Keep them apart in your head. Every I2C conversation is: pick the chip, then pick the register.',
        T10)


def bus():
    return light('bus', 'One bus, many chips',
        col(img('img/i2c-bus.svg', 520, 'Arduino and two sensors sharing SDA and SCL, with pull-up resistors')
            + P('Resistors hold both wires high until a chip pulls one low.', 32, INK, 600, 'text-align:center'),
            gap=24, extra='flex:1; justify-content:center'),
        'Here is the whole physical picture. Every chip on the bus shares the same two wires. One is the clock, SCL. One is the data, SDA. The controller, our Arduino, runs the clock and starts every conversation. Other chips listen for their own address. Notice the two resistors: they connect each wire to the supply. Hold that thought, because it explains why I2C is safe to wire up in parallel.',
        T11)


def open_drain():
    return light('open-drain', 'Nobody drives the line high',
        col(img('img/open-drain.svg', 620, 'With the switch open the resistor holds the line high; closed, the chip pulls it low')
            + P('Chips only pull the line low, or let go. If two talk at once the worst case is a garbled message, not a burnt chip.', 32, INK, 600),
            gap=28, extra='flex:1; justify-content:center'),
        'This is the electrical trick. No chip ever pushes the line high. A chip can only do two things: connect the line to ground, or let go. Letting go means the pull-up resistor drags the line high. So a one is really nobody doing anything. If two chips talk at once, one pulling low and another pushing high, they would fight and something would burn out. Since nothing ever pushes, the worst case is a garbled message. That is why you can hang many chips on one bus without thinking hard.',
        T11)


def wiring():
    """Real Fritzing diagram in place of the placeholder."""
    def wr(c, t):
        return row(f'<div style="width:28px; height:28px; flex:none; background:{c}; border-radius:50%"></div>'
                   + P(t, 32, INK, 500, 'flex:1'), gap=20, extra='align-items:center')
    right = col(wr(ORG, 'VCC to 3.3V') + wr(INK, 'GND to GND') + wr(MUTED, 'SCL to A5') +
                wr(BLUE, 'SDA to A4') + wr(LINE, 'CSB and SDO: nothing'), gap=20)
    chk = card(P('BEFORE THE USB CABLE GOES IN', 24, ORG, 600, 'letter-spacing:2px') +
               P('Follow the red wire with your finger. It must land on the pin marked 3.3V, next to 5V.',
                 32, INK, 500), bg=ORG_T, border=ORG, pad=28, gap=10)
    pic = div(img('img/bmp280-wiring.png', 600, 'Breadboard view: the BMP280 wired to the Uno'),
              'flex:1.85; display:flex; align-items:center')
    return light('wiring', 'Wiring it',
        row(pic + col(right + spacer() + chk, gap=24, extra='flex:1'), gap=48, extra='flex:1; align-items:stretch'),
        'Wire it as on the diagram, with the cable unplugged. Give people a couple of minutes. Walk the room and look at the red wire on every desk. The classic mistake is a wire in 5V because it is the neighbour of 3.3V.',
        T12)


def pins():
    """Real photo of the board in place of the placeholder."""
    rows_ = [['Pin', 'Connect to', 'Why'], ['VCC', '3.3V', 'not 5V'], ['GND', 'GND', 'ground'],
             ['SCL', 'A5', 'the clock'], ['SDA', 'A4', 'the data'],
             ['CSB', 'nothing', 'the board holds it high: I2C mode'],
             ['SDO', 'nothing', 'the board holds it low: address 0x76']]
    tb = table(rows_, [16, 24, 60], size=30, hl={1: ORG_T, 5: PAPER2, 6: PAPER2})
    pic = div(img('img/bmp280-board.jpeg', 520, 'Both sides of the GY-BMP280 board: the pin labels, and the pull-up resistors'),
              'flex:none; display:flex; align-items:center')
    return light('pins', 'Six pins, four wires',
        col(row(pic + col(tb, extra='flex:1'), gap=48, extra='flex:1; align-items:center') +
            card(P('Tie SDO high instead and the same chip answers at 0x77. Most examples online assume 0x77, yours is 0x76.', 32, INK, 500), bg=ORG_T, border=ORG, pad=28),
            gap=28, extra='flex:1; justify-content:space-between'),
        'The board has six pins but we use four wires. VCC to 3.3V, ground to ground, SCL to A5, SDA to A4. Why do CSB and SDO go nowhere? The board already has resistors on them, the little 103 parts you can see on the back. CSB held high selects I2C rather than the other protocol this chip supports. SDO held low picks one of the two possible addresses, and that is why our address is 0x76. On a bare chip leaving them floating would be a bug, here it is correct. If SDO were tied high the chip would answer at 0x77, and most code online assumes 0x77.',
        T12)


def pullups():
    """Same slide, but the code sits inside setup() where it really goes."""
    stk = lambda rail, sub, c: col(M(rail, 32, c, 700, 'text-align:center') + vline(30, c) +
                                   P('pull-up', 26, INK, 500, f'text-align:center; width:200px; background:{PAPER}; border:3px solid {c}; border-radius:8px; padding:10px 0') +
                                   P(sub, 24, BODY, 400, 'text-align:center; width:200px') + vline(30, c),
                                   gap=4, extra='align-items:center')
    dia = card(row(stk('5 V', 'inside the Arduino', ORG) + stk('3.3 V', 'on the sensor board', BLUE), gap=60, extra='justify-content:center') +
               div('', f'height:8px; background:{BLUE}; border-radius:4px') +
               P('SDA sits between two voltages, higher than the sensor would like.', 28, BODY, 400, 'text-align:center'),
               gap=14, extra='width:660px')
    rt = col(P('Turning them off', 32, INK, 600) +
             code(['void setup() {', '    Serial.begin(9600);', '    Wire.begin();', '',
                   '    digitalWrite(SDA, LOW);', '    digitalWrite(SCL, LOW);', '}'], size=28,
                  hl={4: ORG_T, 5: ORG_T}) +
             P('On these chips, writing LOW to a pin that is set as an input switches its pull-up off. Now only the 3.3 volt resistors on the sensor board pull the line high.', 30, BODY),
             gap=20, extra='flex:1')
    return light('pullups', 'Two sets of pull-ups',
        row(dia + rt, gap=48, extra='flex:1; align-items:center'),
        'One more thing, in software. The Arduino has its own pull-up resistors on the I2C pins, and they pull toward five volts. Your sensor board already has pull-ups to three point three. Leave both on and the line sits higher than the sensor would like. So right after Wire.begin, inside setup, we write LOW to both pins. On these chips, writing LOW to a pin set as an input switches its internal pull-up off. Now only the sensor board resistors pull the line up.',
        T12)


def ack_check():
    """Same slide, but the check runs in loop() with a delay so it repeats."""
    cd = code(['void loop() {', '    Wire.beginTransmission(0x76);', '    byte answer = Wire.endTransmission();', '',
               '    Serial.println(answer == 0', '        ? "Something is there"', '        : "Nothing answered");', '',
               '    delay(1000);', '}'], size=26, width=780, extra='flex:none')
    res = col(card(M('0', 64, ORG, 700) + P('A chip pulled SDA low: it acknowledged. Something is there.', 30, INK), bg=ORG_T, border=ORG, gap=8) +
              card(P('anything else', 40, INK, 700) + P('Nobody pulled the line low. Nothing answered.', 30, INK), gap=8) +
              P('It repeats once a second, so you can move a wire and watch the answer change.', 30, BODY, 500),
              gap=20, extra='flex:1')
    return light('ack-check', 'Is anything there?',
        row(cd + res, gap=48, extra='flex:1; align-items:center'),
        'We do not need to read a register yet. We can just ask whether anything answers at that address. beginTransmission followed by endTransmission sends an address and nothing else. endTransmission returns a status. Zero means a chip pulled the line low to acknowledge. Anything else means nobody did. That is exactly the ACK bit from the last module, turned into a number your code can test. It runs in loop with a one second delay, so people can wiggle a jumper and watch the message change while they debug.',
        T12)


def turn_with_code(id, title, steps, code_lines, expect, notes, tag, minutes, size=22):
    """A your-turn slide with the worked answer beside it, hidden until pressed."""
    st = []
    for i, t in enumerate(steps, 1):
        st.append(row(
            f'<p style="width:56px; flex:none; text-align:center; background:{DAMB}; color:{INK}; '
            f'font-size:32px; font-weight:700; border-radius:50%; padding:6px 0; line-height:1.2">{i}</p>'
            + P(t, 34, PAPER, 400, 'flex:1; line-height:1.35'), gap=24, extra='align-items:flex-start'))
    exp = (f'<div style="background:{DPANEL}; border:2px solid {DAMB}; border-radius:16px; '
           f'padding:22px 28px; display:flex; flex-direction:column; gap:8px">'
           f'{P("YOU SHOULD SEE", 22, DAMB, 600, "letter-spacing:3px")}'
           f'{P(expect, 30, PAPER, 400, "line-height:1.3")}</div>')
    cd = (f'<div class="fragment" style="flex:none">'
          f'{code(code_lines, size=size, dark=True, extra="flex:none")}</div>')
    head = row(P('YOUR TURN', 24, DAMB, 600, 'letter-spacing:4px') +
               P(minutes, 24, DMUTED, 500, 'letter-spacing:2px'), gap=28, extra='align-items:baseline')
    left = col(''.join(st) + spacer() + exp, gap=20, extra='flex:1')
    return (f'<section id="{id}" data-transition="fade" style="background:{INK}; color:{PAPER}; '
            f'font-family:{SANS}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:28px">'
            f'{head}'
            f'<h2 style="font-family:{SANS}; font-size:64px; font-weight:600; line-height:1.1; color:{PAPER}">{esc(title)}</h2>'
            f'{row(left + cd, gap=48, extra="flex:1; align-items:flex-start")}'
            f'{footer(tag, True)}<aside>{esc(notes)}</aside></section>')


def turn_read():
    return turn_with_code('turn-read', 'Read the measurement',
        ['Read all six registers from 0xF7 in one request.',
         'Assemble the two 20-bit values.',
         'Print them from loop with a short delay, then breathe on the sensor.'],
        ['void readMeasurement() {',
         '  Wire.beginTransmission(0x76);',
         '  Wire.write(0xF7);',
         '  Wire.endTransmission();',
         '  Wire.requestFrom(0x76, 6);',
         '',
         '  byte d[6];',
         '  for (int i = 0; i < 6; i++) d[i] = Wire.read();',
         '',
         '  uint32_t p = ((uint32_t)d[0] << 12)',
         '             | ((uint32_t)d[1] << 4) | (d[2] >> 4);',
         '',
         '  uint32_t t = ((uint32_t)d[3] << 12)',
         '             | ((uint32_t)d[4] << 4) | (d[5] >> 4);',
         '',
         '  Serial.print(p);   Serial.print("  ");',
         '  Serial.println(t);',
         '}'],
        'Two numbers near 300000 to 500000; breathe and one moves',
        'Five minutes. Let them try first, the answer is one press away on the right. These are raw converter values, not pressure and temperature yet, and I will say that out loud. If it goes wrong: both 0 or 524288 means still asleep or oversampling skipped, so check that ctrl_meas reads back what you wrote. Numbers that never change means forced mode, normal is 11. Wild jumps mean reading each register separately. All 255 means nothing is answering, go back to the chip ID check.',
        T15, '5 MIN')


def turn_temp():
    return turn_with_code('turn-temp', 'Get a real temperature',
        ['Read the 24 calibration bytes from 0x88 in setup.',
         'Pull out dig_T1, dig_T2 and dig_T3.',
         'Run your raw temperature through the formula and divide by 100.'],
        ['uint16_t dig_T1;  int16_t dig_T2, dig_T3;',
         '',
         'void readCalibration() {',
         '  byte c[24];',
         '  Wire.beginTransmission(0x76);',
         '  Wire.write(0x88);',
         '  Wire.endTransmission();',
         '  Wire.requestFrom(0x76, 24);',
         '  for (int i = 0; i < 24; i++) c[i] = Wire.read();',
         '',
         '  dig_T1 = (c[1] << 8) | c[0];',
         '  dig_T2 = (c[3] << 8) | c[2];',
         '  dig_T3 = (c[5] << 8) | c[4];',
         '}',
         '',
         'void loop() {',
         '  int32_t t = compensateT(rawT);   // rawT from module 15',
         '  Serial.println(t / 100.0);',
         '}'],
        '20 to 25 degrees at room temperature; a finger makes it climb',
        'Six minutes. Let them try first, the answer is one press away on the right. Common slips: shifting the wrong byte in the calibration, and forgetting that dig_T2 and dig_T3 are signed. A number that is wildly wrong usually points to signedness. Hold a finger on the sensor and it should climb within a few seconds.',
        T16, '6 MIN')


def little_endian():
    """Old deck's byte-order drawing, with the new slide's code and sign card."""
    cd = code(['uint16_t dig_T1 = (c[1] << 8) | c[0];',
               ' int16_t dig_T2 = (c[3] << 8) | c[2];',
               ' int16_t dig_T3 = (c[5] << 8) | c[4];'], size=28, extra='flex:none')
    sg = card(P('Signed or unsigned', 32, INK, 700) +
              P('The table says which. Get it wrong and a negative coefficient reads as a large positive one: 0xFC18 is -1000 signed and 64536 unsigned.', 28, BODY),
              pad=28, gap=8, extra='flex:1')
    return light('little-endian', 'Byte order and sign',
        col(img('img/little-endian.svg', 400, 'The first byte read is the low half of the 16-bit value')
            + row(cd + sg, gap=32, extra='align-items:center'),
            gap=28, extra='flex:1; justify-content:center'),
        'Two things the column header is telling you. LSB slash MSB: each value is two registers, and the first one holds the low half. So we shift the second byte up by eight and OR in the first. And signed short or unsigned short: some of these can be negative. dig_T1 cannot, the other two can. Use uint16 for the one the table calls unsigned and int16 for the signed ones. Get that wrong and a negative coefficient reads as a large positive one.',
        T16)


CREDIT = 'Bosch Sensortec, BMP280 data sheet'


def sheet(src, h, alt):
    """A datasheet crop with its attribution underneath."""
    return col(img(f'img/{src}', h, alt) + P(CREDIT, 24, MUTED, 400, 'text-align:center'),
               gap=12, extra='flex:none; align-items:center')


def memory_map():
    def pair(a, b):
        return col(P(a, 32, INK, 600) + P(b, 28, BODY), gap=2)
    right = col(pair('Register Name', 'what the makers call it') + pair('Address', 'the register number') +
                pair('bit7 to bit0', 'what each bit is for') + pair('Reset state', 'value at power-on') +
                P("Colours are the datasheet's own key, printed under the table: read only, read and write, or do not write.", 26, MUTED),
                gap=24, extra='flex:1')
    return light('memory-map', 'The makers publish the layout',
        row(sheet('ds-memory-map.png', 470, 'Table 18, the BMP280 memory map') + right,
            gap=48, extra='flex:1; align-items:center'),
        'Open the BMP280 datasheet to section 4.2, Table 18. This one table is the entire chip from your point of view. Walk the columns: name, address, the eight bits, and the reset state, which is what the register holds at power-on. The colours are the datasheet key at the bottom of the page. Keep this open on your laptop for the rest of the session.',
        T10)


def ctrl_meas_table():
    def pr(name, desc, c):
        return row(div('', f'width:28px; height:28px; flex:none; background:{c[0]}; border:3px solid {c[1]}; border-radius:6px') +
                   col(M(name, 32, INK, 700) + P(desc, 28, BODY), gap=2), gap=20, extra='align-items:flex-start')
    return light('ctrl-meas-table', 'ctrl_meas in the datasheet',
        row(sheet('ds-ctrl-meas.png', 300, 'Table 20, register 0xF4 ctrl_meas') +
            col(pr('osrs_t', 'temperature oversampling', FB) + pr('osrs_p', 'pressure oversampling', FO) +
                pr('mode', 'sleep, forced or normal', FG), gap=32, extra='flex:1; justify-content:center'),
            gap=48, extra='flex:1; align-items:center'),
        'This is what the datasheet says about that register, Table 20. Three named fields packed into one byte. Two oversampling settings, one for temperature and one for pressure, and the mode. I will color them consistently from here on: blue for temperature, orange for pressure, green for mode.',
        T14)


def use_cases():
    return light('use-cases', 'Choosing settings for a job',
        row(sheet('ds-usecases.png', 470, 'Table 7, recommended settings for common use cases') +
            col(P('Oversampling costs time and power, and buys less noise.', 32, INK, 600) +
                P('Rather than guess, the makers list settings for jobs people actually do.', 32, BODY) +
                P('Each row gives a mode, an oversampling setting for pressure and temperature, and a filter.', 32, BODY) +
                P('Indoor navigation is the closest to tracking altitude changes.', 32, ORG, 600),
                gap=28, extra='flex:1; justify-content:center'),
            gap=48, extra='flex:1; align-items:center'),
        'How do we pick numbers other than once? Oversampling costs time and power and buys less noise. Table 7 lists what the makers recommend for real jobs. Each row gives a mode, an oversampling setting for pressure and temperature, and a filter coefficient. For us, indoor navigation is the closest to tracking altitude changes, and it is the stretch exercise. Skip it and the answer slide if we are behind.',
        T14)


def six_registers():
    tb = table([['Register', 'Holds', 'Which bits'], ['0xF7', 'press_msb', 'the top eight, up[19:12]'],
                ['0xF8', 'press_lsb', 'the middle eight, up[11:4]'],
                ['0xF9', 'press_xlsb', 'the bottom four, up[3:0], in bits 7 to 4']], [18, 28, 54], size=28)
    return light('six-registers', 'Six registers, two readings',
        row(sheet('ds-press.png', 300, 'Table 24, press_msb, press_lsb and press_xlsb') +
            col(tb + P('The last one only uses half its register. The bottom four bits are always zero.', 30, INK, 500) +
                P('Temperature, 0xFA to 0xFC, works the same way.', 30, BODY), gap=28, extra='flex:1'),
            gap=48, extra='flex:1; align-items:center'),
        'Three registers per reading, because one register is eight bits and a reading is twenty. Look at the datasheet closely. F7 is the top eight bits, F8 the middle eight, and F9 holds the bottom four, but in its upper half. The lower four bits of F9 are always zero. Temperature at FA to FC follows the identical pattern.',
        T15)


def calibration():
    names = ['dig_T1', 'dig_T2', 'dig_T3'] + [f'dig_P{i}' for i in range(1, 10)]
    pills = row(''.join(pill(n, BLUE_T if n.startswith('dig_T') else ORG_T, INK,
                             BLUE if n.startswith('dig_T') else ORG, 24, 500, '8px 10px', mono=True)
                        for n in names), gap=8)
    return light('calibration', 'Raw numbers need calibration',
        col(row(sheet('ds-calib.png', 400, 'Table 17, calibration parameters at 0x88 to 0x9F') +
                col(P('The raw values are what the converter produced, and nothing more. Two identical sensors give different numbers in the same room.', 32, BODY) +
                    P('The factory measured yours and burned the differences into it: twelve values in twenty-four registers, 0x88 to 0x9F.', 32, INK, 600),
                    gap=24, extra='flex:1; justify-content:center'),
                gap=48, extra='align-items:center') +
            col(P('THREE FOR TEMPERATURE, NINE FOR PRESSURE', 24, MUTED, 600, 'letter-spacing:3px') + pills, gap=14),
            gap=32, extra='flex:1; justify-content:space-between'),
        'The numbers we just read are not pressure and temperature. They are what the converter produced and nothing more. Two identical sensors give different numbers in the same room. Every BMP280 comes out of manufacturing slightly different, each one was tested, and the numbers describing how it differs were burned into it. Those are the only way to turn a raw reading into a real one. Twelve values in twenty-four registers, three for temperature and nine for pressure.',
        T16)


OVERRIDES = {
    'two-addresses': two_addresses,
    'bus': bus,
    'open-drain': open_drain,
    'wiring': wiring,
    'pins': pins,
    'pullups': pullups,
    'ack-check': ack_check,
    'turn-read': turn_read,
    'memory-map': memory_map,
    'ctrl-meas-table': ctrl_meas_table,
    'use-cases': use_cases,
    'six-registers': six_registers,
    'calibration': calibration,
    'little-endian': little_endian,
    'turn-temp': turn_temp,
}
