from lib import *

T0 = 'I2C WORKSHOP · CU IN SPACE AVIONICS'
T10 = 'MODULE 10 · INSIDE A CHIP'


def slides():
    S = []

    # 1 cover
    w, W, x0 = wave([1, 1, 0, 1, 0, 0, 1, 0], 100, start=True, stop=True, dark=True, labels=False, gutter=0)
    S.append(('cover', f'''<section id="cover" data-transition="fade" style="background:{INK}; color:{PAPER}; font-family:{SANS}; padding:128px; display:flex; flex-direction:column; gap:32px">
<p style="font-size:24px; font-weight:600; letter-spacing:5px; color:{DAMB}">CU IN SPACE · AVIONICS WORKSHOP</p>
<h1 style="font-family:{SANS}; font-size:120px; font-weight:600; line-height:1.05; color:{PAPER}; width:1500px">I2C from zero to hero</h1>
<p style="font-size:40px; color:{DMUTED}; line-height:1.35; width:1200px">Registers, memory maps, two wires, and a real sensor on your desk</p>
<div style="flex:1"></div>
{w}
<aside>{esc("Welcome. This is a lab, so I will explain a piece, you will do a piece, and we will keep looping. By the end nobody needs to be scared of a datasheet or of I2C. Quick housekeeping: you need your Arduino Uno, the GY-BMP280 board, and four jumper wires. Dark slides are your turn.")}</aside></section>'''))

    # 2 goals
    def goal(n, title, text, graphic):
        return card(
            P(n, 24, BLUE, 700, f'font-family:{MONO}; letter-spacing:4px') +
            P(title, 44, INK, 600, 'line-height:1.15') +
            P(text, 32, BODY) + spacer() + graphic, gap=16, extra='flex:1')
    g1 = row(pill('0xD0', BLUE_T, INK, BLUE, 32, 500, mono=True) + pill('id', PAPER, INK, LINE, 32, 500, mono=True) +
             pill('0x58', ORG_T, INK, ORG, 32, 500, mono=True), gap=12)
    g2 = row(pill('SDA', BLUE_T, INK, BLUE, 28, 600, mono=True) + pill('SCL', PAPER, INK, LINE, 28, 600, mono=True) +
             pill('ACK', ORG_T, INK, ORG, 28, 600, mono=True) + pill('STOP', PAPER, INK, LINE, 28, 600, mono=True), gap=12,
             extra='flex-wrap:wrap')
    g3 = code(['byte id =', '  readRegister(0xD0);'], size=28, pad=24)
    body = col(
        row(goal('01', 'Read a datasheet', 'Find a register, its address, its bits and what to expect, without being told where to look.', g1) +
            goal('02', 'See it on the wires', 'Know electrically and logically what I2C is doing, from START to STOP.', g2) +
            goal('03', 'Drive it from code', 'Send bytes to a chip, read a real value back, and know why each line is there.', g3),
            gap=32, extra='flex:1') +
        P('Lab kit: Arduino Uno · GY-BMP280 sensor · four jumper wires', 32, BODY, 500),
        gap=32, extra='flex:1')
    S.append(('goals', light('goals', 'Where you will be in 90 minutes', body,
        'Three outcomes. First, you can look at a datasheet and find what you need. Second, you know what is physically happening on the two wires, so a logic analyzer trace will make sense. Third, you can write code that talks to a chip and you understand every line of it. Nobody needs to be an expert at the end, but nothing should feel like magic.', T0)))

    # 3 loop and timeline
    def step(t, sub, bg, fg, sfg):
        return div(P(t, 44, fg, 600, 'text-align:center') + P(sub, 28, sfg, 400, 'text-align:center'),
                   f'flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; border-radius:18px; padding:28px 24px; border:2px solid {LINE}')
    arrow = '<x-shape kind="arrow-right" style="width:64px; height:32px; background:#66707D"></x-shape>'
    loop = row(step('I explain', 'a few slides, one idea each', BLUE_T, INK, BODY) + arrow +
               step('You do', 'dark slides, hands on', INK, DAMB, PAPER) + arrow +
               step('We check', 'compare what you see', PAPER2, INK, BODY),
               gap=24, extra='align-items:center')
    mods = [('10', 'Chips', 10, 1, 0), ('11', 'Wires', 15, 1, 0), ('12', 'Wiring', 12, 1, 0), ('13', 'Read', 10, 1, 0),
            ('14', 'Write', 17, 1, 1), ('15', 'Measure', 11, 1, 0), ('16', 'Convert', 14, 1, 1)]
    blocks = ''
    for n, nm, mins, stops, stretch in mods:
        blocks += div(P(n, 44, BLUE, 700, f'font-family:{MONO}; line-height:1.1') + P(nm, 28, INK, 600) +
                      P(f'{mins} min', 24, BODY) + P('1 stop' + (' + stretch' if stretch else ''), 24, ORG, 600),
                      f'flex:{mins}; display:flex; flex-direction:column; gap:4px; background:{PAPER2}; border:2px solid {LINE}; border-radius:14px; padding:20px 16px')
    tl = col(P('NINETY MINUTES, SEVEN MODULES', 24, MUTED, 600, 'letter-spacing:3px') + row(blocks, gap=8), gap=16)
    S.append(('loop', light('loop', 'How this session runs',
        col(loop + tl + P('Seven core hands-on stops, plus two stretch stops if time allows.', 32, BODY), gap=48, extra='flex:1; justify-content:space-between'),
        'The rhythm is always the same. I explain a small idea with a picture, then a dark slide appears and it is your turn to do it on your desk, then we check what everyone got. There are seven core stops and two stretch stops that we skip if we are behind. The timeline is a plan, not a promise. If hardware fights us in module 12 I will trim explanation later, and the follow-along page lets fast people run ahead.', T0)))

    # 4 section
    S.append(('m10', section_slide('m10', '10', 'Inside a chip', 'Registers, hex, and the memory map',
        'About ten minutes. No hardware yet. The goal is one mental model: a chip is a table of numbered bytes, and the datasheet is the table of contents.', T10)))

    # 5 registers
    rows_ = [('00110101', 'o'), ('10100110', 'o'), ('00100111', 'b'), ('01010111', 'b'), ('01011000', 'n'), ('00000000', 'n')]
    tint = {'o': FO, 'b': FB, 'n': NEUTRAL}
    rr = ''
    for i, (b, k) in enumerate(rows_):
        rr += row(M(f'register {i}', 28, MUTED, 500, 'width:250px; padding:10px 0 0 0') + bits(b, [(8, tint[k])], w=56, size=32, pad=8), gap=20)
    left = col(P('Each one holds a single byte and has a number.', 40, INK, 500) +
               P('They are called registers. Some hold readings the chip keeps updating. Some hold settings you write.', 40, BODY) +
               P('That is the whole model.', 40, BLUE, 600), gap=32, extra='width:720px')
    right = col(col(rr, gap=10) +
                row(pill('the chip writes these', ORG_T, INK, ORG, 26) + pill('you write these', BLUE_T, INK, BLUE, 26) + pill('fixed', PAPER2, INK, LINE, 26), gap=12, extra='flex-wrap:wrap'),
                gap=28, extra='flex:1')
    S.append(('registers', light('registers', 'A sensor is a block of numbered bytes', row(left + right, gap=64, extra='flex:1; align-items:center'),
        'Forget everything you think you know about sensors being complicated. A sensor chip is a small block of memory. Each cell holds one byte, eight bits, and each cell has a number. We call them registers. The orange ones the chip fills in for you, like the latest measurement. The blue ones are settings, and you write those. Everything in the next hour is reading those or writing those.', T10)))

    # 6 hex
    hx = ''
    for a, b in [('0x0A', '10'), ('0x76', '118'), ('0xD0', '208'), ('0xFF', '255')]:
        hx += row(cell(a, 190, BLUE_T, INK, BLUE, 40) + P('=', 40, MUTED, 400, 'padding:6px 0 0 0') + cell(b, 130, PAPER2, INK, LINE, 40), gap=20)
    nib = lambda d, b, t: col(cell(d, 200, t[0], t[2], t[1], 80, pad=16) + vline(28, MUTED) + bits(b, [(4, t)], w=72, size=40), gap=0, extra='align-items:center')
    diag = col(P('0xD0 is one byte: two hex digits, four bits each', 32, INK, 600) +
               row(nib('D', '1101', FB) + nib('0', '0000', FO), gap=48) +
               P('Digits run 0 to 9, then A to F for 10 to 15.', 32, BODY), gap=24)
    S.append(('hex', light('hex', 'Datasheets speak hexadecimal',
        row(col(hx, gap=20) + diag, gap=96, extra='flex:1; align-items:center'),
        'Every number in a datasheet is hex, marked with 0x. Digits go zero to nine, then A through F for ten through fifteen. Why bother? Because a byte is always exactly two hex digits, and each digit is exactly four bits. So D is 1101 and zero is 0000, and 0xD0 is 1101 0000. You can read the bits straight off the number once you know the sixteen. In decimal, 255 has three digits and 10 has two and nothing lines up.', T10)))

    # 7 memory map
    def pair(a, b):
        return col(P(a, 32, INK, 600) + P(b, 28, BODY), gap=2)
    right = col(pair('Register Name', 'what the makers call it') + pair('Address', 'the register number') +
                pair('bit7 to bit0', 'what each bit is for') + pair('Reset state', 'value at power-on') +
                P('Colours are the datasheet\'s own key, printed under the table: read only, read and write, or do not write.', 26, MUTED),
                gap=24, extra='flex:1')
    S.append(('memory-map', light('memory-map', 'The makers publish the layout',
        row(ph(1000, 560, 'Bosch BMP280 data sheet', 'Section 4.2, Table 18, the memory map') + right, gap=48, extra='flex:1'),
        'Open the BMP280 datasheet to section 4.2, Table 18. This one table is the entire chip from your point of view. Walk the columns: name, address, the eight bits, and the reset state, which is what the register holds at power-on. The colours are the datasheet key at the bottom of the page. Keep this open on your laptop for the rest of the session.', T10)))

    # 8 id row
    hdr = lambda t, w_: P(t, 24, MUTED, 600, f'width:{w_}px; letter-spacing:1px')
    hdrs = row(hdr('REGISTER NAME', 220) + hdr('ADDRESS', 200) + hdr('BIT 7 TO BIT 0', 720) + hdr('RESET STATE', 220), gap=8)
    def big(t, w_, bg, bd):
        return P(t, 40, INK, 500, f'font-family:{MONO}; width:{w_}px; text-align:center; background:{bg}; border:2px solid {bd}; border-radius:10px; padding:28px 0; line-height:1.2')
    rw = row(big('id', 220, PAPER2, LINE) + big('0xD0', 200, BLUE_T, BLUE) + big('chip_id[7:0]', 720, PAPER2, LINE) + big('0x58', 220, ORG_T, ORG), gap=8)
    lbl = lambda t, w_: P(t, 28, BODY, 400, f'width:{w_}px; text-align:center')
    lbls = row(lbl('what it is called', 220) + lbl('which register', 200) + lbl('all eight bits hold the ID', 720) + lbl('the value to expect', 220), gap=8)
    S.append(('id-row', light('id-row', 'One row: the chip\'s own ID',
        col(col(hdrs + rw + lbls, gap=14) +
            card(P('Reading a datasheet: one row gives a register\'s number, what is in it, and what value to expect.', 40, INK, 500), bg=BLUE_T, border=BLUE, pad=40),
            gap=48, extra='flex:1; justify-content:space-between'),
        'Here is one row of Table 18, rebuilt so it is readable from the back. The register called id lives at address 0xD0. Its eight bits together are the chip ID. And the reset state is 0x58, which is the value we should get back when we ask. That is a check we can use in about twenty minutes: if the chip says 0x58, everything between us and the chip works.', T10)))

    # 9 readings and settings
    def mrow(addr, name, kind, w_=760):
        bg, bd, _ = {'o': FO, 'b': FB, 'n': NEUTRAL}[kind]
        return row(M(addr, 28, INK, 600, f'width:210px') + M(name, 28, INK, 500, 'flex:1'), gap=12,
                   extra=f'background:{bg}; border:2px solid {bd}; padding:11px 24px; width:{w_}px')
    reg = ''.join([mrow('0xFC', 'temp_xlsb', 'o'), mrow('0xFB', 'temp_lsb', 'o'), mrow('0xFA', 'temp_msb', 'o'),
                   mrow('0xF9', 'press_xlsb', 'o'), mrow('0xF8', 'press_lsb', 'o'), mrow('0xF7', 'press_msb', 'o'),
                   mrow('0xF5', 'config', 'b'), mrow('0xF4', 'ctrl_meas', 'b'), mrow('0xD0', 'id', 'n'),
                   mrow('0x88 to 0x9F', 'calibration', 'n')])
    key = col(
        card(P('Readings', 40, INK, 600) + P('The chip writes these. 0xF7 to 0xFC, three registers per reading, because a reading is 20 bits and a register holds 8.', 28, BODY), bg=ORG_T, border=ORG, pad=28, gap=8) +
        card(P('Settings', 40, INK, 600) + P('You write these. 0xF4 says how to measure and whether to run. 0xF5 sets filtering and timing.', 28, BODY), bg=BLUE_T, border=BLUE, pad=28, gap=8) +
        card(P('Fixed', 40, INK, 600) + P('The ID, and the factory calibration numbers we will need at the very end.', 28, BODY), pad=28, gap=8),
        gap=20, extra='flex:1')
    S.append(('readings-settings', light('readings-settings', 'The registers we will use',
        row(col(reg, gap=0) + key, gap=48, extra='flex:1'),
        'Here are the registers this workshop touches, in the datasheet order, highest address at the top. Orange are readings: pressure at 0xF7 to 0xF9, temperature at 0xFA to 0xFC. Blue are the two we write. F4 says how to measure and whether to run at all, F5 is filtering and timing. The gray ones are the ID and the calibration block we will meet in module 16. Notice each reading is three registers. Twenty bits do not fit in eight.', T10)))

    # 10 two addresses
    chip_rows = ''.join([
        row(M('0xD0', 28, INK, 700, 'width:150px') + M('id', 28, INK, 500), gap=8, extra=f'background:{ORG_T}; border:2px solid {ORG}; padding:10px 20px'),
        row(M('0xF4', 28, INK, 500, 'width:150px') + M('ctrl_meas', 28, BODY, 400), gap=8, extra=f'background:{PAPER}; border:2px solid {LINE}; padding:10px 20px'),
        row(M('0xF7', 28, INK, 500, 'width:150px') + M('press_msb', 28, BODY, 400), gap=8, extra=f'background:{PAPER}; border:2px solid {LINE}; padding:10px 20px')])
    chip = card(P('BMP280', 32, INK, 700) + col(chip_rows, gap=8), pad=28, gap=12, extra='width:540px')
    ard = card(P('Arduino', 32, INK, 700) + P('the controller', 28, BODY), pad=28, gap=8, extra='width:300px; align-items:center')
    mid = col(M('0x76', 64, BLUE, 700, 'text-align:center') + P('which chip', 28, BODY, 400, 'text-align:center') +
              div('<x-shape kind="arrow-right" style="width:160px; height:56px; background:#1D5FD1"></x-shape>', 'display:flex; justify-content:center') +
              P('then 0xD0: which register', 28, ORG, 600, 'text-align:center'), gap=8, extra='flex:1; align-items:stretch')
    top = row(ard + mid + chip, gap=32, extra='align-items:center')
    two = row(card(M('0x76', 48, BLUE, 700) + P('Which chip is being spoken to. Set by the hardware, by a resistor on the board.', 30, BODY), gap=8, extra='flex:1') +
              card(M('0xD0', 48, ORG, 700) + P('Which register inside that chip. Set by the chip\'s designers, listed in Table 18.', 30, BODY), gap=8, extra='flex:1'), gap=32)
    S.append(('two-addresses', light('two-addresses', 'Two kinds of address',
        col(top + two + P('Both are hex, both are one byte, and they mean completely different things.', 32, INK, 600), gap=36, extra='flex:1; justify-content:space-between'),
        'One trap before we leave this module. There are two addresses in play and they look identical. 0x76 is the device address, which chip on the wires. It is set by hardware, in this case a resistor on the sensor board. 0xD0 is a register address, which byte inside that chip, and it comes from Table 18. Both are one byte in hex. Keep them apart in your head. Every I2C conversation is: pick the chip, then pick the register.', T10)))

    # 11 your turn
    S.append(('turn-datasheet', dark_turn('turn-datasheet', 'Find it in the datasheet', [
        'Open the BMP280 datasheet to section 4.2, Table 18.',
        'Find the row called id. What are its address and its reset state?',
        'Find ctrl_meas at 0xF4. What is its reset state?',
        'Which register holds the first byte of the pressure reading?'],
        'Three minutes, laptops only. Circulate and check that everyone actually found Table 18 rather than a summary elsewhere. Answers: id is 0xD0 with reset state 0x58, ctrl_meas resets to 0x00, and pressure starts at 0xF7, press_msb. That reset state of 0x00 matters later: it is why the sensor starts asleep.',
        T10, answer='id: 0xD0, reset 0x58 · ctrl_meas resets to 0x00 · pressure starts at 0xF7', minutes='3 MIN')))
    return S
