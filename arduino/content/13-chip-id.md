<p class="modnum">Module 13</p>

# Reading a register

----

## You already know which one

From Table 18: register `0xD0` holds the chip id, and it should read `0x58`.

It is the one register where the answer is known in advance.

<p class="sub">A correct answer means the wiring, the address, the bus and the read are all right.</p>

----

## It takes two messages

<img src="content/img/i2c-read.svg" alt="Write the register number, then request a byte back" style="max-height:420px">

----

## First, a confusing thing about `Wire`

<div class="two">
<div>

```cpp
Wire.beginTransmission(0x76);
Wire.write(0xD0);
Wire.endTransmission();
```

</div>
<div style="font-size:.82em">

<code>beginTransmission</code> does <strong>not</strong> begin a transmission.

<code>write</code> does <strong>not</strong> write anything.

Both just put bytes in a buffer.

<p class="sub"><code>endTransmission</code> is the call that actually puts all of it on the wire.</p>

</div>
</div>

<p class="sub">The names describe what the calls are for, not what they do.</p>

----

## Then ask for the answer

<div class="two">
<div>

```cpp
Wire.requestFrom(0x76, 1);
byte value = Wire.read();
```

</div>
<div style="font-size:.82em">

<code>requestFrom</code> sends the second message and collects the reply.

<code>1</code> is how many bytes you want.

<code>read</code> takes one byte out of what arrived.

</div>
</div>

----

## The same four lines every time

Reading any register is these four steps. Only the register number changes.

<div class="two">
<div>

```cpp
Wire.beginTransmission(0x76);
Wire.write(reg);
Wire.endTransmission();

Wire.requestFrom(0x76, 1);
```

</div>
<div style="font-size:.86em">

There are a dozen registers in this sensor worth reading.

Copying four lines each time means a dozen chances to get one of them wrong.

</div>
</div>

----

## So give it a name

`setup` and `loop` are functions. You have been filling them in since the first module, but the Arduino wrote the outside of them.

<p class="big">You can write your own.</p>

----

### What the parts are

<img src="content/img/fn-define.svg" alt="byte readRegister(byte reg) explained" style="max-height:400px">

----

### That first word

<div class="two">
<div>

| Written | Hands back |
|---|---|
| <code>byte</code> | one byte |
| <code>int</code> | a whole number |
| <code>void</code> | nothing at all |

</div>
<div style="font-size:.88em">

<code>void</code> is the one you have been typing since module 2.

<code>setup</code> and <code>loop</code> do things, but they do not hand a value back to anyone, so their first word is <code>void</code>.

<p class="sub">A function that hands something back says what type it is.</p>

</div>
</div>

----

### And `return`

<div class="two">
<div>

```cpp
byte readRegister(byte reg) {
    ...
    return Wire.read();
}
```

</div>
<div style="font-size:.86em">

<code>return</code> is how the value gets out.

It ends the function there and hands that value back to whoever called it.

<p class="sub">A <code>void</code> function has nothing to return, which is why <code>setup</code> and <code>loop</code> never use it.</p>

</div>
</div>

----

## The finished function

<div class="two">
<div>

```cpp
byte readRegister(byte reg) {
    Wire.beginTransmission(0x76);
    Wire.write(reg);
    Wire.endTransmission();

    Wire.requestFrom(0x76, 1);
    return Wire.read();
}
```

</div>
<div style="font-size:.86em">

The four steps, with <code>reg</code> standing in for whichever register is wanted.

Asking the sensor anything is then one line:

```cpp
byte id = readRegister(0xD0);
```

<p class="sub">Which states the intent, instead of four lines of setup.</p>

</div>
</div>

----

## The whole program

<div class="two">
<div>

```cpp
#include <Wire.h>

byte readRegister(byte reg) {
    Wire.beginTransmission(0x76);
    Wire.write(reg);
    Wire.endTransmission();
    Wire.requestFrom(0x76, 1);
    return Wire.read();
}

void setup() {
    Serial.begin(9600);
    Wire.begin();
    digitalWrite(SDA, LOW);
    digitalWrite(SCL, LOW);

    byte id = readRegister(0xD0);
    Serial.print("Chip ID: 0x");
    Serial.println(id, HEX);
}

void loop() {
}
```

</div>
<div style="font-size:.82em">

The helper sits above <code>setup</code>, like a variable does.

<code>Serial.println(id, HEX)</code> prints in hex, so it matches what the datasheet says.

<div class="box kit">
<span class="lbl">What to expect</span>
<code>Chip ID: 0x58</code>
</div>

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Ask it</h2>

<div class="try">
<span class="lbl">Your turn</span>

Upload it and open the Serial Monitor.

You are looking for <code>Chip ID: 0x58</code>
</div>

----

## What you just did

You sent bytes to a silicon device using nothing but the document describing it, and got back exactly what that document promised.

<p class="sub">Every sensor on the rocket works this way. The registers differ, the method does not.</p>

----

## If a different number came back

<div class="box trouble">
<span class="lbl">Match what you saw</span>
<ul>
<li><strong><code>0x60</code></strong>, you have a BME280, not a BMP280. Same board, slightly different chip, and it also measures humidity. Everything after this still works.</li>
<li><strong><code>0x0</code> or <code>0xFF</code></strong>, nothing is answering. Go back and check the address check from the last module still passes.</li>
<li><strong>Nothing prints.</strong> Serial Monitor is not set to 9600.</li>
<li><strong>The number changes every run.</strong> Loose wire. Press the sensor firmly into the breadboard.</li>
</ul>
</div>

----

<details>
<summary>If you want to know what else is on the bus</summary>

You can try every address in turn and see which ones answer.

```cpp
for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
        Serial.print("Found 0x");
        Serial.println(addr, HEX);
    }
}
```

Useful when a board is not the address you expected. Not needed otherwise.
</details>

----

## What you now know

| | |
|---|---|
| `Wire.beginTransmission` | Fills a buffer. Sends nothing |
| `Wire.endTransmission` | Sends it, and returns whether a chip acknowledged |
| `Wire.requestFrom` | Asks for bytes back |
| Writing a function | Return type, name, then what it takes |
| `void` | Hands nothing back |
| `return` | Hands a value back and ends the function |
| `readRegister(reg)` | Your own helper. One line per register |
| `0x58` | What a BMP280 says when you ask who it is |
