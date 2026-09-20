from lib import *

T14 = 'MODULE 14 · WAKING THE SENSOR UP'


def pack_rows(specs, res_bits, res_hex):
    """specs: list of (label, bits8, (start, end) group index range, colors)."""
    out = ''
    for lab, b, (s, e), colr in specs:
        grp = [(s, NEUTRAL), (e - s, colr), (8 - e, NEUTRAL)]
        grp = [g for g in grp if g[0] > 0]
        out += row(M(esc(lab), 30, INK, 500, 'width:400px; flex:none') + bits(b, grp, w=72, size=40, pad=12), gap=24, extra='align-items:center')
    out += div('', f'height:4px; width:1000px; background:{INK}')
    out += row(M('OR together', 30, INK, 700, 'width:400px; flex:none') + bits(res_bits, [(3, FB), (3, FO), (2, FG)], w=72, size=40, pad=12) +
               M('= ' + res_hex, 56, INK, 700, 'padding:0 0 0 16px'), gap=24, extra='align-items:center')
    return col(out, gap=14)


def slides():
    S = []

    S.append(('m14', section_slide('m14', '14', 'Waking the sensor up', 'Bit fields, shifts and masks, and writing a register',
        'About seventeen minutes with one core hands-on stop, plus a stretch stop if we are on time. This module has the most new syntax, so go slowly on the bit slides. The rest of the session leans on it.', T14)))

    # 41 asleep
    idx = idx_row(7, 0, w=96, gap=6, size=28)
    bts = bits('00000000', [(6, NEUTRAL), (2, FG)], w=96, size=48, pad=16)
    lb = row(P('oversampling: skipped', 28, BODY, 500, 'width:606px; text-align:center') + empty(6) + P('mode: sleep', 28, GRN, 700, 'width:198px; text-align:center'), gap=0)
    S.append(('asleep', light('asleep', 'It starts asleep',
        col(col(P('ctrl_meas at 0xF4, reset state 0x00', 40, INK, 600) + col(idx + bts + lb, gap=8), gap=24) +
            P('All eight bits are zero, and the bottom two decide whether the sensor runs. Right now it is asleep.', 36, BODY),
            gap=48, extra='flex:1; justify-content:space-between'),
        'It is not measuring anything. Table 18 gave ctrl_meas a reset state of 0x00. All eight bits are zero, and the bottom two of those decide whether the sensor runs. Right now it is asleep. That is why we could read the chip ID fine but a measurement would just be zeros. The sensor is on, it just has not been told to work.', T14)))

    # 42 ctrl_meas datasheet
    def pr(name, desc, c):
        return row(div('', f'width:28px; height:28px; flex:none; background:{c[0]}; border:3px solid {c[1]}; border-radius:6px') +
                   col(M(name, 32, INK, 700) + P(desc, 28, BODY), gap=2), gap=20, extra='align-items:flex-start')
    S.append(('ctrl-meas-table', light('ctrl-meas-table', 'ctrl_meas in the datasheet',
        row(ph(1000, 540, 'Bosch BMP280 data sheet', 'Table 20, register 0xF4 ctrl_meas') +
            col(pr('osrs_t', 'temperature oversampling', FB) + pr('osrs_p', 'pressure oversampling', FO) + pr('mode', 'sleep, forced or normal', FG), gap=32, extra='flex:1; justify-content:center'),
            gap=48, extra='flex:1'),
        'This is what the datasheet says about that register, Table 20. Three named fields packed into one byte. Two oversampling settings, one for temperature and one for pressure, and the mode. I will color them consistently from here on: blue for temperature, orange for pressure, green for mode.', T14)))

    # 43 byte layout
    W_ = 140
    gw = lambda n: n * W_ + (n - 1) * 6
    idx = idx_row(7, 0, w=W_, gap=6, size=28)
    def merged(t, n, c):
        return P(t, 36, INK, 600, f'font-family:{MONO}; width:{gw(n)}px; text-align:center; background:{c[0]}; border:2px solid {c[1]}; border-radius:8px; padding:24px 0; line-height:1.2')
    mrow = row(merged('osrs_t', 3, FB) + merged('osrs_p', 3, FO) + merged('mode', 2, FG), gap=6)
    dsc = lambda a, b, n: col(P(a, 28, INK, 600) + P(b, 28, BODY), gap=2, extra=f'width:{gw(n)}px')
    drow = row(dsc('bits 7 to 5', 'temperature oversampling', 3) + dsc('bits 4 to 2', 'pressure oversampling', 3) + dsc('bits 1 to 0', 'sleep, forced or normal', 2), gap=6)
    S.append(('byte-layout', light('byte-layout', 'Three settings in eight bits',
        col(P('0xF4 ctrl_meas', 40, INK, 600) + col(idx + mrow + drow, gap=12) +
            P('One register, several separate settings. We have to pack them into a single byte.', 36, BODY),
            gap=40, extra='flex:1; justify-content:space-between'),
        'Here is the byte laid out. Bits seven to five are temperature oversampling. Bits four to two are pressure oversampling. Bits one and zero are the mode. That is three separate settings in eight bits, and to write the register we have to build one byte out of three pieces.', T14)))

    # 44 osrs and mode tables
    def tr(bt, d, hi=False):
        bg, bd = (BLUE_T, BLUE) if hi else (PAPER, LINE)
        return row(M(bt, 36, INK, 700, 'width:200px; flex:none') + P(d, 30, INK, 400, 'flex:1'), gap=16,
                   extra=f'align-items:center; background:{bg}; border:2px solid {bd}; border-radius:10px; padding:12px 24px')
    lt = card(P('Oversampling, osrs_t and osrs_p', 32, INK, 700) + col(tr('000', 'skipped') + tr('001', '×1, measure once', True) + tr('010', '×2') + tr('101', '×16'), gap=8) +
              P('More samples: less noise, more time per reading. Tables 21 and 22.', 28, BODY), gap=16, extra='flex:1')
    rt = card(P('Mode', 32, INK, 700) + col(tr('00', 'sleep: does nothing') + tr('01 or 10', 'forced: one reading, then sleep') + tr('11', 'normal: measures over and over', True), gap=8) +
              P('Table 10. Normal is what we want.', 28, BODY), gap=16, extra='flex:1')
    sel = row(pill('osrs_t = 001', BLUE_T, INK, BLUE, 32, 600, mono=True) + pill('osrs_p = 001', ORG_T, INK, ORG, 32, 600, mono=True) +
              pill('mode = 11', GRN_T, INK, GRN, 32, 600, mono=True), gap=20)
    S.append(('osrs-mode', light('osrs-mode', 'Choosing the three values',
        col(row(lt + rt, gap=32) + col(P('So the three values are', 32, BODY) + sel, gap=14), gap=32, extra='flex:1; justify-content:space-between'),
        'Oversampling is how many times the sensor measures internally before giving you an answer. More samples, less noise, more time per reading. 001 means once, and that is enough to start. Temperature uses the same encoding. Then the mode: sleep does nothing and is where we are now, forced takes one reading and goes back to sleep, and normal measures over and over on its own. Normal is what we want, so 11. Our three values: 001, 001 and 11.', T14)))

    # 45 pack
    pk = pack_rows([('osrs_t  0b001 << 5', '00100000', (0, 3), FB), ('osrs_p  0b001 << 2', '00000100', (3, 6), FO), ('mode  0b11', '00000011', (6, 8), FG)], '00100111', '0x27')
    S.append(('pack-byte', light('pack-byte', 'Packing three fields into one byte',
        col(pk + col(P(esc('<< moves every bit up by that many places and fills zeros in behind.'), 30, BODY) +
                     P(esc('| is bitwise OR: a bit is set wherever either input had it set. Each field sits somewhere different, so nothing overlaps.'), 30, BODY), gap=8),
            gap=32, extra='flex:1; justify-content:space-between'),
        'Two new operators. Left shift, written two less-than signs, moves every bit up by that many places and fills in zeros behind. So 001 shifted five places becomes 00100000. Then bitwise OR, the vertical bar, sets a bit wherever either input has one. Since every field was shifted somewhere different, nothing overlaps. Put together: 00100111, which is 0x27. Also note 0b means a number written in binary, the same way 0x means hex.'.replace('two less-than signs', 'two less than signs'), T14)))

    # 46 code and write
    lc = code(['byte osrs_t = 0b001;', 'byte osrs_p = 0b001;', 'byte mode = 0b11;', '', 'byte value = (osrs_t << 5)', '           | (osrs_p << 2)', '           | mode;', '',
               'writeRegister(0xF4, value);'], size=28, extra='flex:1')
    rc = col(code(['void writeRegister(byte reg, byte value) {', '    Wire.beginTransmission(0x76);', '    Wire.write(reg);', '    Wire.write(value);', '    Wire.endTransmission();', '}'], size=28) +
             P('The partner to readRegister. Register first, then what goes in it.', 30, BODY), gap=20, extra='flex:1')
    S.append(('write-code', light('write-code', 'In code, then onto the wire',
        col(row(lc + rc, gap=32, extra='align-items:flex-start') +
            P('Writing the shifts out says where each field goes. You could write 0x27 directly, but in six months nobody would know what it meant.', 30, BODY),
            gap=32, extra='flex:1; justify-content:space-between'),
        'In code it looks like this. The three fields, then shift each into place and OR them together. The value comes out as 0x27. Writing the shifts out means the code documents itself. Then writeRegister: same message as before with one extra byte after the register number, register first, then what goes in it. A write is one message. A read needs two, because the register number goes out and the answer has to come back, and a message only runs one way.', T14)))

    # 47 your turn wake
    S.append(('turn-wake', dark_turn('turn-wake', 'Wake it up', [
        'Add writeRegister next to readRegister.',
        'Build the byte from the three fields and write it to 0xF4.',
        'Read 0xF4 back with readRegister and print it in hex.'],
        'Five minutes. Reading back confirms the write landed, ctrl_meas is read and write so it gives you its current contents. Common slip: writing to 0xF5 instead of 0xF4.',
        T14, answer='0x27', minutes='5 MIN')))

    # 48 mask and shift
    def blk(title, rows_, note):
        parts = ''
        for lab, b, groups in rows_:
            parts += col(P(esc(lab), 28, INK, 600, 'font-family:%s' % MONO) + bits(b, groups, w=64, size=36, gap=5, pad=10), gap=4)
        return card(P(title, 32, INK, 700) + col(parts, gap=14) + P(note, 28, BODY), gap=16, extra='flex:1')
    v = ('v = 0x27', '00100111', [(3, FB), (3, FO), (2, FG)])
    left = blk('Pull out mode', [v, ('& 0b11', '00000011', [(6, NEUTRAL), (2, FD)]), ('mode = 0b11', '00000011', [(6, NEUTRAL), (2, FG)])], 'AND clears everything above the bottom two bits.')
    right = blk('Pull out osrs_p', [v, ('v >> 2', '00001001', [(8, NEUTRAL)]), ('& 0b111', '00000111', [(5, NEUTRAL), (3, FD)]), ('osrs_p = 0b001', '00000001', [(5, NEUTRAL), (3, FO)])],
                'Shift the field to the bottom first, then mask.')
    S.append(('mask-shift', light('mask-shift', 'Getting a field back out',
        col(row(left + right, gap=32, extra='align-items:flex-start') +
            P(esc('& is bitwise AND: a bit is set only where both inputs had it set. A value used this way is a mask. >> is the opposite of <<, so shift by the same amount you shifted when writing.'), 30, BODY),
            gap=28, extra='flex:1; justify-content:space-between'),
        'Reading goes the other way. Reading 0xF4 gives the whole byte, and pulling one field out takes two operations. AND, the ampersand, keeps a bit only where both inputs have it. Ending with 0b11 keeps just the bottom two bits, so we get the mode. A value used this way is called a mask. For a field that is not at the bottom, shift it down first with right shift, then mask off what is above it. Shift by the same amount you shifted when writing.', T14)))

    # 49 use cases
    S.append(('use-cases', light('use-cases', 'Choosing settings for a job',
        row(ph(1000, 540, 'Bosch BMP280 data sheet', 'Table 7, recommended settings for use cases') +
            col(P('Oversampling costs time and power, and buys less noise.', 32, INK, 600) +
                P('Rather than guess, the makers list settings for jobs people actually do.', 32, BODY) +
                P('Each row gives a mode, an oversampling setting for pressure and temperature, and a filter.', 32, BODY) +
                P('Indoor navigation is the closest to tracking altitude changes.', 32, ORG, 600), gap=28, extra='flex:1; justify-content:center'),
            gap=48, extra='flex:1'),
        'How do we pick numbers other than once? Oversampling costs time and power and buys less noise. Table 7 lists what the makers recommend for real jobs. Each row gives a mode, an oversampling setting for pressure and temperature, and a filter coefficient. For us, indoor navigation is the closest to tracking altitude changes, and it is the stretch exercise. Skip it and the answer slide if we are behind.', T14)))

    # 50 your turn indoor
    S.append(('turn-indoor', dark_turn('turn-indoor', 'Configure it for indoor navigation', [
        'Read the Indoor navigation row of Table 7: the mode and both oversampling settings.',
        'Look each one up in Tables 10, 21 and 22 for its bit pattern.',
        'Build the byte, write it to 0xF4, and read it back.'],
        'Stretch stop, eight minutes, skip it and the next slide if we are behind. The point is to do the table lookup themselves. The hint pinned at the bottom appears with a build in Present mode. Do not reveal the answer until most people have a value on screen.',
        T14, answer='normal mode · pressure ×16 · temperature ×2', minutes='STRETCH · 8 MIN', label='HINT')))

    # 51 answer
    pk = pack_rows([('osrs_t  0b010 << 5', '01000000', (0, 3), FB), ('osrs_p  0b101 << 2', '00010100', (3, 6), FO), ('mode  0b11', '00000011', (6, 8), FG)], '01010111', '0x57')
    S.append(('indoor-answer', light('indoor-answer', 'Indoor navigation packs to 0x57',
        col(pk + P('Table 21 gives 101 for ×16. Table 22 gives 010 for ×2. Table 10 gives 11 for normal. Read 0xF4 back and it should say 0x57.', 32, BODY),
            gap=40, extra='flex:1; justify-content:space-between'),
        'The answer. Temperature times two is 010, shifted up five. Pressure times sixteen is 101, shifted up two. Normal mode is 11. OR them together and you get 01010111, which is 0x57. If your read back says 0x57, you configured it the way the makers recommend for indoor navigation.', T14)))
    return S
