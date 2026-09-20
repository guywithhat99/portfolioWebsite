from lib import *

T15 = 'MODULE 15 · READING THE MEASUREMENT'


def slots(start, n, colr, w=60, gap=4):
    """One row of 20 bit slots: n coloured cells starting at slot index start."""
    parts = ''
    if start > 0:
        parts += empty(start * (w + gap) - gap)
    for _ in range(n):
        parts += cell('&#160;', w=w, bg=colr[0], border=colr[1], pad=16, size=32)
    return row(parts, gap=gap)


def slides():
    S = []

    S.append(('m15', section_slide('m15', '15', 'Reading the measurement', 'Twenty bits, six registers, and why one request matters',
        'About eleven minutes. The sensor is running now and writing answers into six registers. Two ideas here: how to reassemble a twenty bit number, and why we must read all six in one go.', T15)))

    # 53 six registers
    tb = table([['Register', 'Holds', 'Which bits'], ['0xF7', 'press_msb', 'the top eight, up[19:12]'], ['0xF8', 'press_lsb', 'the middle eight, up[11:4]'],
                ['0xF9', 'press_xlsb', 'the bottom four, up[3:0], in bits 7 to 4']], [18, 28, 54], size=28)
    S.append(('six-registers', light('six-registers', 'Six registers, two readings',
        row(ph(860, 560, 'Bosch BMP280 data sheet', 'Table 24, press_msb, press_lsb and press_xlsb') +
            col(tb + P('The last one only uses half its register. The bottom four bits are always zero.', 30, INK, 500) +
                P('Temperature, 0xFA to 0xFC, works the same way.', 30, BODY), gap=28, extra='flex:1'), gap=48, extra='flex:1'),
        'Three registers per reading, because one register is eight bits and a reading is twenty. Look at the datasheet closely. F7 is the top eight bits, F8 the middle eight, and F9 holds the bottom four, but in its upper half. The lower four bits of F9 are always zero. Temperature at FA to FC follows the identical pattern.', T15)))

    # 54 assemble
    hdr = row(empty(304) + idx_row(19, 0, w=60, gap=4, size=24), gap=0)
    def lab(t):
        return M(esc(t), 28, INK, 600, 'width:280px; flex:none')
    r1 = row(lab('msb << 12') + slots(0, 8, FB), gap=24, extra='align-items:center')
    r2 = row(lab('lsb << 4') + slots(8, 8, FO), gap=24, extra='align-items:center')
    r3 = row(lab('xlsb >> 4') + slots(16, 4, FG), gap=24, extra='align-items:center')
    r4 = row(lab('raw, 20 bits') + slots(0, 8, FB) + slots(0, 0, FB) if False else lab('raw, 20 bits') +
             row(''.join(cell('&#160;', 60, c[0], c[1], pad=16, size=32) for c in [FB] * 8 + [FO] * 8 + [FG] * 4), gap=4), gap=24, extra='align-items:center')
    cd = code(['uint32_t raw =', '    ((uint32_t)msb << 12)', '  | ((uint32_t)lsb << 4)', '  | (xlsb >> 4);'], size=28, extra='flex:none')
    nt = col(P('xlsb shifts right: its useful bits sit at the top of the register and belong at the bottom of the result.', 28, BODY) +
             P('uint32_t, because 20 bits will not fit in a byte.', 28, BODY), gap=14, extra='flex:1; justify-content:center')
    S.append(('assemble', light('assemble', 'Putting the 20 bits back together',
        col(col(hdr + r1 + r2 + r3 + div('', f'height:4px; width:1580px; background:{INK}') + r4, gap=12) + row(cd + nt, gap=40, extra='align-items:center'),
            gap=28, extra='flex:1; justify-content:space-between'),
        'To get the twenty bit number back, shift each piece to where it belongs and combine. The msb goes up twelve places. The lsb goes up four. The xlsb goes the other way: its useful bits sit at the top of the register, so shift right by four to drop them to the bottom. OR them together. It is the same two operations as ctrl_meas, in the other direction. We use a 32 bit integer because twenty bits will not fit in a byte.', T15)))

    # 55 inconsistent data
    boxA = lambda t, c: P(t, 32, INK, 600, f'flex:1; text-align:center; background:{c[0]}; border:2px solid {c[1]}; border-radius:12px; padding:22px 0')
    chip = row(boxA('Measurement A', FB) + boxA('Measurement B', FO), gap=8)
    rd = lambda t, c: P(t, 30, INK, 600, f'flex:1; text-align:center; font-family:{MONO}; background:{c[0]}; border:2px solid {c[1]}; border-radius:10px; padding:16px 0')
    reads = row(rd('0xF7', FB) + rd('0xF8', FB) + rd('0xF9', FB) + rd('0xFA', FO) + rd('0xFB', FO) + rd('0xFC', FO), gap=8)
    mark = div('<x-shape kind="arrow-up" style="width:40px; height:64px; background:#B34B0A"></x-shape>' + P('a new measurement lands here', 30, ORG, 600), 'display:flex; align-items:center; justify-content:center; gap:20px')
    S.append(('inconsistent', light('inconsistent', 'Why not read six registers one at a time?',
        col(col(P('THE CHIP KEEPS MEASURING', 24, MUTED, 600, 'letter-spacing:3px') + chip + mark + P('YOU READ ONE REGISTER AT A TIME', 24, MUTED, 600, 'letter-spacing:3px') + reads, gap=14) +
            card(P('You would get a pressure from one measurement and a temperature from the next, silently. The datasheet calls that inconsistent data.', 32, INK, 500), bg=ORG_T, border=ORG, pad=28),
            gap=32, extra='flex:1; justify-content:space-between'),
        'Six separate readRegister calls would work, and the datasheet says not to. Section 3.10. The sensor measures on its own schedule, which has nothing to do with when you read. A new measurement can land while you are partway through reading the last one. You would get a pressure from one measurement and a temperature from the next, and nothing would tell you. The datasheet calls that inconsistent data.', T15)))

    # 56 shadowing and burst
    bx = lambda t, s, c, w_: card(P(t, 32, INK, 700, 'text-align:center') + P(s, 26, BODY, 400, 'text-align:center'), bg=c[0], border=c[1], pad=24, gap=6, extra=f'width:{w_}px; align-items:center')
    ar = div('<x-shape kind="arrow-right" style="width:72px; height:36px; background:#66707D"></x-shape>', 'flex:none')
    top = row(bx('New measurement', 'finishes while you read', FO, 400) + ar + bx('Shadow registers', 'the chip parks it here', NEUTRAL, 400) + ar +
              bx('Registers you read', 'swapped at the STOP that ends your read', FB, 460), gap=20, extra='align-items:center; justify-content:space-between')
    stop = lambda: pill('STOP', INK, PAPER, INK, 26, 600, '6px 14px')
    six = row(''.join(pill('read', PAPER2, INK, LINE, 26, 500, '6px 14px') + stop() for _ in range(6)), gap=10)
    one = row(pill('one request: START, 0xF7, six bytes', BLUE_T, INK, BLUE, 26, 500, '6px 20px') + stop(), gap=10)
    cmp_ = col(
        col(P('Six reads: six STOPs, six chances for the values to change underneath you', 28, BODY, 500) + six, gap=10) +
        col(P('One burst read: one STOP at the end, all six bytes from the same measurement', 28, BODY, 500) + one, gap=10), gap=28)
    S.append(('shadow-burst', light('shadow-burst', 'How the chip keeps a read consistent',
        col(top + cmp_, gap=40, extra='flex:1; justify-content:space-between'),
        'Here is what the chip does about it. Shadowing. If a new measurement finishes while you are reading, the chip parks it in shadow registers and keeps showing you the old set. It swaps them in when it sees the STOP condition that ends your read. That only works if all six registers come out in one go. Six reads means six STOPs and six chances for the values to change. One read means one STOP at the end, and all six bytes come from the same measurement. The datasheet calls that a burst read.', T15)))

    # 57 burst code
    cd = code(['Wire.beginTransmission(0x76);', 'Wire.write(0xF7);', 'Wire.endTransmission();', '', 'Wire.requestFrom(0x76, 6);', '', 'byte data[6];',
               'for (int i = 0; i < 6; i++) {', '    data[i] = Wire.read();', '}'], size=28, extra='flex:none')
    rt = col(P('Name the first register, then ask for six. The sensor sends 0xF7 onwards without being asked for each one.', 30, BODY) +
             card(row(M('32', 96, ORG, 700, 'line-height:1') + P('bytes: the most Wire carries in one request on an Uno.', 28, INK, 500, 'flex:1'), gap=24, extra='align-items:center') +
                  P('Six is fine. So is the calibration data, which is 24. Past 32 it silently gives you fewer bytes than you asked for.', 28, BODY), bg=ORG_T, border=ORG, pad=28, gap=12),
             gap=28, extra='flex:1')
    S.append(('burst-code', light('burst-code', 'One request for all six', row(cd + rt, gap=48, extra='flex:1; align-items:center'),
        'The code for a burst read. Point at register 0xF7, then ask for six bytes in one request. The sensor sends 0xF7 onwards on its own. An array holds them because six separate variables would be tedious. One limit worth knowing: Wire carries 32 bytes in one request on an Uno. Six is fine. So is the calibration data, which is 24. Past 32 it silently gives you fewer bytes than you asked for.', T15)))

    # 58 your turn
    S.append(('turn-read', dark_turn('turn-read', 'Read the measurement', [
        'Read all six registers from 0xF7 in one request.',
        'Assemble the two 20-bit values.',
        'Print them from loop with a short delay, then breathe on the sensor.'],
        'Five minutes. These are raw converter values, not pressure and temperature yet, and I will say that out loud. If it goes wrong: both 0 or 524288 means still asleep or oversampling skipped, so check that ctrl_meas reads back what you wrote. Numbers that never change means forced mode, normal is 11. Wild jumps mean reading each register separately. All 255 means nothing is answering, go back to the chip ID check.',
        T15, answer='Two numbers near 300000 to 500000; breathe and one moves', minutes='5 MIN')))
    return S
