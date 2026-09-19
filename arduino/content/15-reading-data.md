<p class="modnum">Module 15</p>

# Reading the measurement

----

## The sensor is running now

It is measuring on its own and writing the answers into six registers.

| Registers | Holds |
|---|---|
| `0xF7` `0xF8` `0xF9` | pressure |
| `0xFA` `0xFB` `0xFC` | temperature |

<p class="sub">Three each, because one register is eight bits and a reading is twenty.</p>

----

## What the datasheet says

<img src="content/img/ds-press.png" alt="Table 24 from the datasheet, the press registers" style="max-height:300px">

<p class="sub">Bosch Sensortec, BMP280 data sheet, Table 24.</p>

----

### Reading that closely

| Register | Holds | Which bits |
|---|---|---|
| `0xF7` | `press_msb` | the top eight, `up[19:12]` |
| `0xF8` | `press_lsb` | the middle eight, `up[11:4]` |
| `0xF9` | `press_xlsb` | the bottom four, `up[3:0]`, in **bits 7 to 4** |

<p class="sub">The last one only uses half its register. The bottom four bits are always zero.</p>

----

## Putting them back together

<img src="content/img/assemble-20bit.svg" alt="0xF7 shifted 12, 0xF8 shifted 4, 0xF9 shifted right 4, merged into one 20-bit value" style="max-height:420px">

----

### In code

<div class="two">
<div>

```cpp
uint32_t raw =
      ((uint32_t)msb  << 12)
    | ((uint32_t)lsb  <<  4)
    | ( xlsb >> 4);
```

</div>
<div style="font-size:.86em">

Same two operations as <code>ctrl_meas</code>, in the other direction.

<code>xlsb</code> shifts <strong>right</strong>, because its useful bits sit at the top of the register and belong at the bottom of the result.

<p class="sub"><code>uint32_t</code> because 20 bits will not fit in a <code>byte</code>.</p>

</div>
</div>

----

## Now, how to fetch six registers

Six separate calls to `readRegister` would work.

<p class="big">The datasheet says not to do that.</p>

----

## Why

Section 3.10. The sensor measures on its own schedule, which has nothing to do with when you read.

<div class="two">
<div>

A new measurement can land <strong>while you are partway through</strong> reading the last one.

</div>
<div style="font-size:.9em">

You would get a pressure from one measurement and a temperature from the next, silently.

<p class="sub">The datasheet calls the result inconsistent data.</p>

</div>
</div>

----

### What the chip does about it

<div class="box kit">
<span class="lbl">Shadowing</span>
If a new measurement finishes while you are reading, the chip parks it in shadow registers and keeps showing you the old set.

It swaps them in when it sees the <strong>stop condition</strong> that ends your read.
</div>

<p class="sub">Which only works if all six registers come out in one go.</p>

----

### So it has to be one request

<div class="two">
<div>

Six reads means six stop conditions, so six chances for the values to change underneath you.

</div>
<div style="font-size:.9em">

One read means one stop condition, at the end, and all six bytes come from the same measurement.

<p class="sub">This is what the datasheet means by a burst read.</p>

</div>
</div>

----

## Asking for several bytes

<div class="two">
<div>

```cpp
Wire.beginTransmission(0x76);
Wire.write(0xF7);
Wire.endTransmission();

Wire.requestFrom(0x76, 6);

byte data[6];
for (int i = 0; i < 6; i++) {
    data[i] = Wire.read();
}
```

</div>
<div style="font-size:.86em">

Name the <strong>first</strong> register, then ask for six.

The sensor sends <code>0xF7</code> onwards without being asked for each one.

<p class="sub">An array holds them, because six separate variables would be tedious.</p>

</div>
</div>

----

### One limit worth knowing

`Wire` can carry **32 bytes** in one request on an Uno.

Six is fine. So is the calibration data, which is 24.

<p class="sub">Past 32 it silently gives you fewer bytes than you asked for.</p>

----

## The whole read

<div class="two">
<div>

```cpp
void readMeasurement() {
    Wire.beginTransmission(0x76);
    Wire.write(0xF7);
    Wire.endTransmission();
    Wire.requestFrom(0x76, 6);

    byte d[6];
    for (int i = 0; i < 6; i++) {
        d[i] = Wire.read();
    }

    uint32_t p = ((uint32_t)d[0] << 12)
               | ((uint32_t)d[1] <<  4)
               | ( d[2] >> 4);

    uint32_t t = ((uint32_t)d[3] << 12)
               | ((uint32_t)d[4] <<  4)
               | ( d[5] >> 4);

    Serial.print(p);
    Serial.print("  ");
    Serial.println(t);
}
```

</div>
<div style="font-size:.86em">

<code>d[0]</code> to <code>d[2]</code> are pressure, <code>d[3]</code> to <code>d[5]</code> are temperature.

They arrive in register order, which is the order Table 18 lists them.

<div class="box kit">
<span class="lbl">Roughly what to expect</span>
Two large numbers, around 300000 to 500000.
</div>

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Read it</h2>

<div class="try">
<span class="lbl">Your turn</span>

Call <code>readMeasurement</code> from <code>loop</code> with a short delay, and watch the numbers.

Breathe on the sensor and watch the second one move.
</div>

----

## Those are not pressure and temperature

They are what the sensor's converter produced, and nothing more.

<p class="big">Two identical sensors give different numbers in the same room.</p>

----

### Why

Each one is physically slightly different, and the factory measured how.

Turning these numbers into pascals and degrees needs those per-sensor figures, which live in the calibration registers.

<p class="sub">That is the next module.</p>

----

## If the numbers look wrong

<div class="box trouble">
<span class="lbl">Check what you are seeing</span>
<ul>
<li><strong>Both read 0 or 524288.</strong> The sensor is still asleep, or oversampling is set to skipped. Check <code>ctrl_meas</code> reads back what you wrote.</li>
<li><strong>They never change.</strong> Mode may be set to forced, which takes one reading and stops. Normal mode is <code>11</code>.</li>
<li><strong>Wild jumps between readings.</strong> You are probably reading each register separately rather than in one request.</li>
<li><strong>Everything reads 255.</strong> Nothing is answering. Go back to the chip id check.</li>
</ul>
</div>

----

## What you now know

| | |
|---|---|
| `0xF7` to `0xFC` | Six registers holding two readings |
| 20 bits | Spread over three registers each |
| `>>` on the xlsb | Its bits sit at the top and belong at the bottom |
| Burst read | One request, one stop, one consistent set |
| Shadowing | How the chip keeps a set consistent while you read it |
| 32 bytes | What `Wire` can carry in one request |
| Raw values | Not yet pressure or temperature |
