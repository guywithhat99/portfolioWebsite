from lib import *

T16 = 'MODULE 16 · TURNING IT INTO A TEMPERATURE'


def slides():
    S = []

    S.append(('m16', section_slide('m16', '16', 'Turning it into a temperature', 'Calibration, one formula, and then a library',
        'About fourteen minutes. This is the payoff module. The temperature formula is copy and paste, and the point is to see a real number you can check against a thermometer.', T16)))

    # 60 calibration
    names = ['dig_T1', 'dig_T2', 'dig_T3'] + [f'dig_P{i}' for i in range(1, 10)]
    pills = row(''.join(pill(n, BLUE_T if n.startswith('dig_T') else ORG_T, INK, BLUE if n.startswith('dig_T') else ORG, 24, 500, '8px 10px', mono=True) for n in names), gap=8)
    S.append(('calibration', light('calibration', 'Raw numbers need calibration',
        col(row(ph(860, 400, 'Bosch BMP280 data sheet', 'Table 17, calibration parameters at 0x88 to 0x9F') +
                col(P('The raw values are what the converter produced, and nothing more. Two identical sensors give different numbers in the same room.', 32, BODY) +
                    P('The factory measured yours and burned the differences into it: twelve values in twenty-four registers, 0x88 to 0x9F.', 32, INK, 600), gap=24, extra='flex:1; justify-content:center'),
                gap=48) +
            col(P('THREE FOR TEMPERATURE, NINE FOR PRESSURE', 24, MUTED, 600, 'letter-spacing:3px') + pills, gap=14),
            gap=36, extra='flex:1; justify-content:space-between'),
        'The numbers we just read are not pressure and temperature. They are what the converter produced and nothing more. Two identical sensors give different numbers in the same room. Every BMP280 comes out of manufacturing slightly different, each one was tested, and the numbers describing how it differs were burned into it. Those are the only way to turn a raw reading into a real one. Twelve values in twenty-four registers, three for temperature and nine for pressure.', T16)))

    # 61 byte order and sign
    def reg(addr, val, half, c):
        return col(M(addr, 28, MUTED, 500) + cell(val, w=180, bg=c[0], border=c[1], size=44, pad=16) + P(half, 28, BODY), gap=6, extra='align-items:center')
    ar = div('<x-shape kind="arrow-right" style="width:96px; height:48px; background:#66707D"></x-shape>', 'flex:none')
    res = col(M('dig_T1', 28, MUTED, 500) + cell('0x6B70', w=300, bg=PAPER2, border=INK, size=44, pad=16) + P('high half first, as a number', 28, BODY), gap=6, extra='align-items:center')
    dia = row(reg('0x88', '0x70', 'low half, read first', FO) + reg('0x89', '0x6B', 'high half, read second', FB) + ar + res, gap=40, extra='align-items:flex-end; justify-content:center')
    cd = code(['uint16_t dig_T1 = (c[1] << 8) | c[0];', ' int16_t dig_T2 = (c[3] << 8) | c[2];', ' int16_t dig_T3 = (c[5] << 8) | c[4];'], size=28, extra='flex:none')
    sg = card(P('Signed or unsigned', 32, INK, 700) + P('The table says which. Get it wrong and a negative coefficient reads as a large positive one: 0xFC18 is -1000 signed and 64536 unsigned.', 28, BODY), pad=28, gap=8, extra='flex:1')
    S.append(('little-endian', light('little-endian', 'Byte order and sign',
        col(col(P('EXAMPLE VALUES', 24, MUTED, 600, 'letter-spacing:3px') + dia, gap=14) + row(cd + sg, gap=32, extra='align-items:center'), gap=32, extra='flex:1; justify-content:space-between'),
        'Two things the column header is telling you. LSB slash MSB: each value is two registers, and the first one holds the low half. So we shift the second byte up by eight and OR in the first. The numbers on the slide are just an example. And signed short or unsigned short: some of these can be negative. dig_T1 cannot, the other two can. Use uint16 for the one the table calls unsigned and int16 for the signed ones. Get that wrong and a negative coefficient reads as a large positive one.', T16)))

    # 62 formula
    fl = code(['int32_t t_fine;', '', 'int32_t compensateT(int32_t adc_T) {', '  int32_t var1, var2;', '',
               '  var1 = ((((adc_T >> 3) - ((int32_t)dig_T1 << 1)))', '          * ((int32_t)dig_T2)) >> 11;', '',
               '  var2 = (((((adc_T >> 4) - ((int32_t)dig_T1))', '          * ((adc_T >> 4) - ((int32_t)dig_T1))) >> 12)', '          * ((int32_t)dig_T3)) >> 14;', '',
               '  t_fine = var1 + var2;', '  return (t_fine * 5 + 128) >> 8;', '}'], size=24, extra='flex:none')
    side = col(card(P('Copy it exactly', 36, INK, 700) + P('Section 3.11.3. There is nothing to work out here. It is arithmetic chosen to fit a small processor.', 28, BODY), pad=28, gap=8) +
               card(P('2534 means 25.34 °C', 36, INK, 700) + P('The answer comes back in hundredths of a degree.', 28, BODY), bg=BLUE_T, border=BLUE, pad=28, gap=8) +
               card(row(col(M('46', 80, BLUE, 700, 'line-height:1') + P('clock cycles, integer', 26, BODY), gap=4, extra='flex:1') +
                        col(M('2400', 80, ORG, 700, 'line-height:1') + P('roughly, floating point', 26, BODY), gap=4, extra='flex:1'), gap=16) +
                    P('An 8-bit chip has no floating point hardware. Section 3.11.1.', 26, BODY), pad=28, gap=10),
               gap=20, extra='flex:1')
    S.append(('formula', light('formula', 'The compensation formula', row(fl + side, gap=40, extra='flex:1; align-items:flex-start'),
        'The datasheet gives the formula in section 3.11.3, and the honest advice is copy it exactly. There is nothing to work out. It looks strange because it is arithmetic chosen to fit a small processor. An eight bit chip has no floating point hardware, so the maths is whole numbers with shifts standing in for multiplying and dividing by powers of two. Section 3.11.1 puts the integer version at about 46 clock cycles against roughly 2400 for floating point. The answer is in hundredths of a degree, so 2534 means 25.34 degrees. Keep t_fine, the pressure formula needs it too.', T16)))

    # 63 your turn
    S.append(('turn-temp', dark_turn('turn-temp', 'Get a real temperature', [
        'Read the 24 calibration bytes from 0x88 in setup.',
        'Pull out dig_T1, dig_T2 and dig_T3.',
        'Run your raw temperature through the formula and divide by 100.'],
        'Six minutes. Common slips: shifting the wrong byte in the calibration, and forgetting that dig_T2 and dig_T3 are signed. A number that is wildly wrong usually points to signedness. Hold a finger on the sensor and it should climb within a few seconds.',
        T16, answer='20 to 25 degrees at room temperature; a finger makes it climb', minutes='6 MIN')))

    # 64 library
    lib = code(['#include <Adafruit_BMP280.h>', '', 'Adafruit_BMP280 bmp;', '', 'void setup() {', '    Serial.begin(9600);', '    bmp.begin(0x76);', '}', '',
                'void loop() {', '    Serial.print(bmp.readTemperature());', '    Serial.print("  ");', '    Serial.println(bmp.readPressure());', '    delay(500);', '}'],
               size=24, extra='flex:none')
    lt = col(P('Pressure is nine more coefficients and 64-bit arithmetic on an 8-bit chip. An hour of typing that teaches nothing new. This is what a driver library is.', 30, BODY) +
             card(P('Sketch, Include Library, Manage Libraries', 28, INK, 600) + P('Search Adafruit BMP280 and install it. Say yes to Adafruit Unified Sensor and Adafruit BusIO.', 28, BODY), pad=24, gap=6) +
             card(P('Nothing in it is hidden from you any more. It reads the same registers and applies the same formula from the same datasheet.', 28, INK, 500), bg=BLUE_T, border=BLUE, pad=24, gap=6) +
             P('0x76, because that is your address and the library defaults to 0x77. Temperature comes back in degrees, pressure in pascals.', 28, BODY),
             gap=20, extra='flex:1')
    S.append(('library', light('library', 'You could finish this, or use a library', row(lt + lib, gap=48, extra='flex:1; align-items:flex-start'),
        'Pressure is the same idea with nine more coefficients, 64 bit arithmetic on a chip whose registers are eight bits wide, and about half of it is still to type. It would take an hour of careful typing and you would learn nothing you did not learn from temperature. This is what a driver library is. Install Adafruit BMP280 from the Library Manager, and say yes to its two dependencies. What you know now that you did not before is exactly what it is doing. Pass 0x76 because the library defaults to 0x77.', T16)))

    # 65 your turn compare
    S.append(('turn-compare', dark_turn('turn-compare', 'Check it against your own', [
        'Install the Adafruit BMP280 library and its two dependencies.',
        'Upload the library sketch with bmp.begin(0x76).',
        'Print the library temperature next to the one your own code worked out.'],
        'Stretch stop, three minutes, skip it if we are behind. If they disagree by a lot, the usual culprit is the signedness of dig_T2 or dig_T3 in the hand written version. This is the moment that shows the library is no magic.',
        T16, answer='The two temperatures agree', minutes='STRETCH · 3 MIN')))

    # 66 closing
    def item(t):
        return row('<x-icon name="Check" style="color:#F2A65A; width:56px; height:56px"></x-icon>' + P(t, 44, PAPER, 500, 'flex:1'), gap=28, extra='align-items:center')
    S.append(('closing', f'''<section id="closing" data-transition="fade" style="background:{INK}; color:{PAPER}; font-family:{SANS}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:48px">
<p style="font-size:24px; font-weight:600; letter-spacing:5px; color:{DAMB}">WHAT YOU CAN DO NOW</p>
<h2 style="font-family:{SANS}; font-size:72px; font-weight:600; line-height:1.1; color:{PAPER}; width:1400px">Read the table, watch the wires, drive the chip</h2>
{col(item('Find a register, its bits and its reset state in a datasheet.') + item('Explain what SDA and SCL are doing, from START to STOP.') + item('Read, write and convert data from a real sensor.'), gap=28)}
<div style="flex:1"></div>
<p style="font-size:36px; color:{DMUTED}; line-height:1.35">The follow-along page has every step again, at your own pace. Questions?</p>
{footer(T16, True)}
<aside>{esc("Wrap up. Recap the three outcomes from the start: reading a datasheet, seeing it on the wires, driving it from code. Point people to the follow-along page for anything they want to redo at their own pace. Then questions.")}</aside></section>'''))
    return S
