<p class="modnum">Module 14</p>

# Waking the sensor up

----

## It is not measuring anything

Table 18 gave `ctrl_meas` a reset state of `0x00`.

All eight bits are zero, and the bottom two of those decide whether the sensor runs.

<p class="big">Right now it is asleep.</p>

----

## What the datasheet says about it

<img src="content/img/ds-ctrl-meas.png" alt="Table 20 from the datasheet, the ctrl_meas register" style="max-height:300px">

<p class="sub">Bosch Sensortec, BMP280 data sheet, Table 20.</p>

----

### Three settings in eight bits

<img src="content/img/ctrl-meas-layout.svg" alt="Bits 7 to 5 are osrs_t, bits 4 to 2 are osrs_p, bits 1 and 0 are mode" style="max-height:400px">

----

## What the three do

<div class="two">
<div>

<img src="content/img/ds-osrs.png" alt="Table 21, oversampling settings" style="max-height:340px">

</div>
<div style="font-size:.88em">

<strong>Oversampling</strong> is how many times the sensor measures internally before giving you an answer.

More samples, less noise, more time per reading.

<code>001</code> means once. That is enough to start.

<p class="sub">Temperature uses the same encoding, in Table 22.</p>

</div>
</div>

----

## And the mode

<div class="two">
<div>

<img src="content/img/ds-mode.png" alt="Table 10, mode settings" style="max-height:300px">

</div>
<div style="font-size:.88em">

<strong>Sleep</strong> does nothing. This is where it is now.

<strong>Forced</strong> takes one reading and goes back to sleep.

<strong>Normal</strong> measures over and over on its own.

<p class="sub">Normal is what we want, so <code>11</code>.</p>

</div>
</div>

----

## So the three values are

| Field | Bits | Value | Meaning |
|---|---|---|---|
| `osrs_t` | 7, 6, 5 | `001` | temperature once |
| `osrs_p` | 4, 3, 2 | `001` | pressure once |
| `mode` | 1, 0 | `11` | keep measuring |

Now they have to be packed into one byte.

----

## Left bit shift

<div class="two">
<div>

```cpp
0b001 << 5
```

</div>
<div style="font-size:.86em">

<code><<</code> is a <strong>left bit shift</strong>. It moves every bit up by that many places and fills in zeros behind.

<code>001</code> shifted five places becomes <code>00100000</code>.

<p class="sub"><code>0b</code> means the number is written in binary, the same way <code>0x</code> means hex.</p>

</div>
</div>

----

### Bitwise OR

<div class="two">
<div>

```cpp
0b00100000
| 0b00000100
| 0b00000011
```

</div>
<div style="font-size:.86em">

<code>|</code> is <strong>bitwise OR</strong>. The result has a bit set wherever <strong>either</strong> input had it set.

Since each field was shifted somewhere different, nothing overlaps.

</div>
</div>

----

## All together

<img src="content/img/ctrl-meas-build.svg" alt="001 shifted 5, 001 shifted 2, and 11, merged into 0x27" style="max-height:430px">

----

### In code

<div class="two">
<div>

```cpp
byte osrs_t = 0b001;
byte osrs_p = 0b001;
byte mode   = 0b11;

byte value = (osrs_t << 5)
           | (osrs_p << 2)
           |  mode;
```

</div>
<div style="font-size:.86em">

Which comes out as <code>0x27</code>.

Writing the shifts out like this says where each field goes.

<p class="sub">You could write <code>0x27</code> directly. In six months nobody would know what it meant.</p>

</div>
</div>

----

## Sending it

<div class="two">
<div>

```cpp
void writeRegister(byte reg, byte value) {
    Wire.beginTransmission(0x76);
    Wire.write(reg);
    Wire.write(value);
    Wire.endTransmission();
}
```

</div>
<div style="font-size:.86em">

The partner to <code>readRegister</code>.

Same message as before, with one extra byte after the register number.

<p class="sub">Register first, then what goes in it.</p>

</div>
</div>

----

### What that looks like on the wires

<img src="content/img/write-frame.svg" alt="A write: start, address with the write bit, then the register number and the value, each acknowledged" style="max-height:340px">

----

### A read, for comparison

<img src="content/img/read-frame.svg" alt="A read: one message naming the register, then a second message collecting the byte" style="max-height:400px">

----

### Why the write is shorter

<div class="two">
<div>

A write sends the register number and the value in the <strong>same message</strong>. Both travel in the direction the bus is already going.

</div>
<div style="font-size:.9em">

A read cannot. The register number goes out, the answer has to come back, and a message only runs one way.

<p class="sub">So the first message ends, and a second one starts with the read bit set.</p>

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Wake it up</h2>

<div class="try">
<span class="lbl">Your turn</span>

Add <code>writeRegister</code>, build the byte, and send it to <code>0xF4</code>.

Then read <code>0xF4</code> back with <code>readRegister</code> and print it.
</div>

<details>
<summary>What you should see</summary>

```
0x27
```

Reading back what you wrote confirms the write landed. `ctrl_meas` is read and
write, so it gives you its current contents.
</details>

----

## Getting a field back out

Reading `0xF4` gives the whole byte. Pulling one field out of it takes two more operations.

<div class="two">
<div>

```cpp
byte v = readRegister(0xF4);
byte mode = v & 0b11;
```

</div>
<div style="font-size:.86em">

<code>&amp;</code> is <strong>bitwise AND</strong>. The result has a bit set only where <strong>both</strong> inputs had it set.

<code>0b11</code> has only the bottom two bits set, so everything above them is cleared.

<p class="sub">A value used this way is called a <strong>mask</strong>.</p>

</div>
</div>

----

### Fields that are not at the bottom

<div class="two">
<div>

```cpp
byte v = readRegister(0xF4);
byte osrs_p = (v >> 2) & 0b111;
```

</div>
<div style="font-size:.86em">

<code>&gt;&gt;</code> is a <strong>right bit shift</strong>. It is the opposite of <code><<</code>.

Shift the field down to the bottom first, then mask off what is above it.

<p class="sub">Shift by the same amount you shifted when writing.</p>

</div>
</div>

----

## Choosing settings for a job

<img src="content/img/ds-usecases.png" alt="Table 7, recommended settings for common use cases" style="max-height:400px">

<p class="sub">Bosch Sensortec, BMP280 data sheet, Table 7.</p>

----

### What that table is for

<div class="two">
<div>

Oversampling costs time and power, and buys less noise.

Rather than guess, the makers list settings for jobs people actually do.

</div>
<div style="font-size:.88em">

Each row gives a mode, an oversampling setting for each of pressure and temperature, and a filter coefficient.

<p class="sub">Indoor navigation is the closest to tracking altitude changes.</p>

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Configure it for indoor navigation</h2>

<div class="try">
<span class="lbl">Your turn</span>

Read the <strong>Indoor navigation</strong> row of Table 7 for the mode and the two oversampling settings.

Look each one up in Tables 10, 21 and 22 to get its bit pattern.

Build the byte and write it to <code>0xF4</code>.
</div>

<details>
<summary>Hint</summary>
The row says normal mode, pressure oversampling ×16, temperature oversampling ×2.

Table 21 gives <code>101</code> for ×16. Table 22 gives <code>010</code> for ×2. Table 10 gives <code>11</code> for normal.
</details>

<details>
<summary>One way to write it</summary>

```cpp
byte osrs_t = 0b010;   // x2
byte osrs_p = 0b101;   // x16
byte mode   = 0b11;    // normal

writeRegister(0xF4, (osrs_t << 5) | (osrs_p << 2) | mode);
```

Which is `0x57`. Read `0xF4` back to confirm.
</details>

----

## The other settings register

`0xF5` is `config`. Same shape, three fields in one byte: standby time in bits 7 to 5, IIR filter in bits 4 to 2, and an SPI option in bit 0.

<p class="sub">Section 4.3.5. The defaults are usable, so it can be left alone for now.</p>

----

## What you now know

| | |
|---|---|
| Reset state `0x00` | The sensor starts asleep |
| `<<` left bit shift | Moves a field up into position |
| `>>` right bit shift | Moves a field back down |
| <code>&#124;</code> bitwise OR | Set where either input was set |
| `&` bitwise AND | Set where both inputs were set, used to mask |
| `0b` | The number is written in binary |
| `writeRegister` | Register number, then the value |
| `0xF4` | Oversampling and mode, in one byte |
| Table 7 | Settings the makers recommend per use case |
