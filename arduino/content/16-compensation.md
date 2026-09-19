<p class="modnum">Module 16</p>

# Turning it into a temperature

----

## The factory measured your sensor

Every BMP280 comes out of manufacturing slightly different.

Each one was tested, and the numbers describing how it differs were burned into it.

<p class="sub">Those numbers are the only way to turn a raw reading into a real one.</p>

----

## Where they live

<div class="two">
<div>

<img src="content/img/ds-calib.png" alt="Table 17, compensation parameter storage" style="max-height:440px">

</div>
<div style="font-size:.86em">

Twelve values in twenty-four registers, <code>0x88</code> to <code>0x9F</code>.

Three for temperature, nine for pressure.

<p class="sub">Bosch Sensortec, BMP280 data sheet, Table 17.</p>

</div>
</div>

----

### Two things that column header is telling you

<div class="two">
<div>

<strong><code>LSB / MSB</code></strong>

Each value is two registers, and the <strong>first</strong> one holds the low half.

</div>
<div>

<strong><code>signed short</code> / <code>unsigned short</code></strong>

Some of these can be negative. <code>dig_T1</code> cannot, the other two can.

</div>
</div>

----

## The byte order

<img src="content/img/little-endian.svg" alt="The first byte is the low half of the 16-bit value" style="max-height:400px">

----

### Which in code is

<div class="two">
<div>

```cpp
uint16_t dig_T1 = (c[1] << 8) | c[0];
 int16_t dig_T2 = (c[3] << 8) | c[2];
 int16_t dig_T3 = (c[5] << 8) | c[4];
```

</div>
<div style="font-size:.86em">

The <strong>second</strong> byte gets shifted up, because it is the high half.

<code>uint16_t</code> for the one the table calls unsigned, <code>int16_t</code> for the ones it calls signed.

<p class="sub">Get that wrong and a negative coefficient reads as a large positive one.</p>

</div>
</div>

----

## Fetching them

<div class="two">
<div>

```cpp
byte c[24];

Wire.beginTransmission(0x76);
Wire.write(0x88);
Wire.endTransmission();

Wire.requestFrom(0x76, 24);
for (int i = 0; i < 24; i++) {
    c[i] = Wire.read();
}
```

</div>
<div style="font-size:.86em">

One burst, same as the measurement.

Twenty-four bytes, comfortably under the thirty-two <code>Wire</code> allows.

<div class="box kit">
<span class="lbl">Do this once</span>
These never change. Read them in <code>setup</code> and keep them.
</div>

</div>
</div>

----

## The formula

The datasheet gives it, in section 3.11.3.

<div class="two">
<div>

```cpp
int32_t t_fine;

int32_t compensateT(int32_t adc_T) {
  int32_t var1, var2;

  var1 = ((((adc_T >> 3) - ((int32_t)dig_T1 << 1)))
          * ((int32_t)dig_T2)) >> 11;

  var2 = (((((adc_T >> 4) - ((int32_t)dig_T1))
          * ((adc_T >> 4) - ((int32_t)dig_T1))) >> 12)
          * ((int32_t)dig_T3)) >> 14;

  t_fine = var1 + var2;
  return (t_fine * 5 + 128) >> 8;
}
```

</div>
<div style="font-size:.86em">

Copy it exactly. There is nothing to work out here.

It is arithmetic chosen to fit a small processor, not something to read.

<p class="sub">The answer comes back in hundredths of a degree, so 2534 means 25.34 °C.</p>

</div>
</div>

----

### Why it looks like that

<div class="two">
<div>

An 8-bit chip has no floating point hardware. Doing this in <code>float</code> would be far slower.

</div>
<div style="font-size:.9em">

So the maths is done in whole numbers, with shifts standing in for multiplying and dividing by powers of two.

<p class="sub">Section 3.11.1 puts the 32-bit integer version at about 46 clock cycles, against roughly 2400 for floating point.</p>

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Get a real temperature</h2>

<div class="try">
<span class="lbl">Your turn</span>

Read the calibration in <code>setup</code>, pull out <code>dig_T1</code> to <code>dig_T3</code>, and run your raw temperature through the formula.

Print it as degrees, so divide by 100.
</div>

<details>
<summary>What you should see</summary>
Room temperature, somewhere around 20 to 25 degrees.

Hold a finger on the sensor and it should climb within a few seconds.
</details>

----

## That worked

Raw bytes off a wire became a number you can check against a thermometer.

<p class="big">Now do the same for pressure.</p>

----

## The pressure formula

<div class="two">
<div>

```cpp
int64_t var1, var2, p;
var1 = ((int64_t)t_fine) - 128000;
var2 = var1 * var1 * (int64_t)dig_P6;
var2 = var2 + ((var1 * (int64_t)dig_P5) << 17);
var2 = var2 + (((int64_t)dig_P4) << 35);
var1 = ((var1 * var1 * (int64_t)dig_P3) >> 8)
     + ((var1 * (int64_t)dig_P2) << 12);
var1 = (((((int64_t)1) << 47) + var1))
     * ((int64_t)dig_P1) >> 33;
if (var1 == 0) return 0;
...
```

</div>
<div style="font-size:.86em">

Nine more coefficients.

64-bit arithmetic, on a chip whose registers are 8 bits wide.

And that is about half of it.

</div>
</div>

----

## You could finish this

It would take an hour of careful typing, and you would learn nothing you did not learn from the temperature one.

<p class="big">This is what a driver library is.</p>

----

### So use one

<div class="two">
<div>

<strong>Sketch → Include Library → Manage Libraries</strong>

Search for <code>Adafruit BMP280</code> and install it.

It will ask to install <code>Adafruit Unified Sensor</code> and <code>Adafruit BusIO</code> as well. Say yes.

</div>
<div style="font-size:.88em">

<div class="box kit">
<span class="lbl">What you know now that you did not before</span>
Exactly what it is doing. It reads the same registers you read, applies the same formula from the same datasheet, and hands back a number.

Nothing in it is hidden from you any more.
</div>

</div>
</div>

----

### Using it

<div class="two">
<div>

```cpp
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

void setup() {
    Serial.begin(9600);
    bmp.begin(0x76);
}

void loop() {
    Serial.print(bmp.readTemperature());
    Serial.print("  ");
    Serial.println(bmp.readPressure());
    delay(500);
}
```

</div>
<div style="font-size:.86em">

<code>0x76</code>, because that is your address and the library defaults to <code>0x77</code>.

Temperature comes back in degrees, pressure in pascals.

<p class="sub">Both already compensated.</p>

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Check it against your own</h2>

<div class="try">
<span class="lbl">Your turn</span>

Print the library's temperature next to the one your own code worked out.

They should agree.
</div>

----

## What you now know

| | |
|---|---|
| Calibration | Twelve per-sensor values at `0x88` to `0x9F` |
| `LSB / MSB` | First byte is the low half |
| signed or unsigned | The table says which, and it matters |
| `t_fine` | Temperature result the pressure formula also needs |
| Integer maths | Shifts instead of floating point, because the chip is 8-bit |
| A driver library | The same registers and the same formula, already typed |
