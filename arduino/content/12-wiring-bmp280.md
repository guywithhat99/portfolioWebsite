<p class="modnum">Module 12</p>

# Wiring the sensor

----

## What you need

<div class="box kit">
<span class="lbl">On your desk</span>
The GY-BMP280 board · four jumper wires
</div>

----

## This one can be damaged

Everything else in the kit runs on 5 volts.

<p class="big">This board runs on 3.3.</p>

There is no protection on it. Connect it to 5 volts and you can destroy it.

----

## The board has six pins

<div class="two">
<div>

<div class="ph" style="height:250px">
<span><b>PHOTO</b>
The GY-BMP280 board, close up, with the six pin
labels on the silkscreen readable.</span>
</div>

</div>
<div>

| Pin | Connect to |
|---|---|
| <code>VCC</code> | <strong>3.3V</strong>, not 5V |
| <code>GND</code> | <code>GND</code> |
| <code>SCL</code> | <code>A5</code> |
| <code>SDA</code> | <code>A4</code> |
| <code>CSB</code> | nothing |
| <code>SDO</code> | nothing |

</div>
</div>

----

### Why two pins go nowhere

The board already has resistors on `CSB` and `SDO` that hold them where they need to be.

`CSB` held high selects I2C rather than the other protocol this chip supports.

`SDO` held low picks one of the two possible addresses.

<p class="sub">Leaving them unconnected is correct here <em>because</em> those resistors exist. On a bare chip it would be a bug.</p>

----

## Wiring it

<div class="ph" style="height:330px">
<span><b>FRITZING, BREADBOARD VIEW</b>
BMP280 VCC to the Uno 3.3V pin, GND to GND,
SCL to A5, SDA to A4. CSB and SDO unconnected.</span>
</div>

<div class="box warn">
<span class="lbl">Check before plugging in the USB cable</span>
Follow the red wire with your finger. It must land on the pin marked <strong>3.3V</strong>, which sits next to 5V on the power header.
</div>

----

## One more thing, in software

The Arduino's I2C pins have pull-up resistors inside the chip, and they pull towards **5 volts**.

Your sensor board already has its own pull-ups, to 3.3 volts.

<p class="sub">Leave both on and the line sits higher than the sensor would like.</p>

----

### Turning them off

```cpp
Wire.begin();
digitalWrite(SDA, LOW);
digitalWrite(SCL, LOW);
```

On these chips, writing `LOW` to a pin that is set as an input switches its pull-up **off**.

<p class="sub">Now the only thing setting the line high is the 3.3 volt resistors on the sensor board.</p>

----

## Is anything there

You do not need to read a register yet. You can just ask whether anything answers at that address.

<div class="two">
<div>

```cpp
Wire.beginTransmission(0x76);
byte answer = Wire.endTransmission();

Serial.println(answer == 0
    ? "Something is there"
    : "Nothing answered");
```

</div>
<div style="font-size:.82em">

<code>endTransmission()</code> hands back a status.

<strong><code>0</code></strong> means a chip pulled the line low to acknowledge.

Anything else means nobody did.

<p class="sub">This is the ACK bit from the last module, surfaced as a number.</p>

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Check your wiring</h2>

<div class="try">
<span class="lbl">Your turn</span>

Wire it up, run that, and open the Serial Monitor at 9600.

You want <code>Something is there</code>
</div>

----

## That address is not arbitrary

`0x76` is the address because the resistor on the board holds `SDO` low.

Tie `SDO` high instead and the same chip answers to `0x77`.

<div class="box warn">
<span class="lbl">Address mismatch</span>
Most examples online assume <code>0x77</code>. Yours is <code>0x76</code>, and code that assumes otherwise will report that no sensor is connected.
</div>

----

## If nothing answers

<div class="box trouble">
<span class="lbl">Check in this order</span>
<ul>
<li><strong>Nothing at all reported.</strong> Usually SDA and SCL swapped. They are A4 and A5, and it is easy to reverse them.</li>
<li><strong>Still nothing.</strong> Check the 3.3V wire is actually in 3.3V and the ground wire is connected. A sensor with no ground cannot answer.</li>
<li><strong>Nothing answered, and the wiring looks right.</strong> Try <code>0x77</code> instead. Some boards tie SDO the other way.</li>
<li><strong>It worked once and now does not.</strong> If the board ever saw 5 volts on VCC, it may be dead. Swap it and check the wiring again.</li>
</ul>
</div>

----

## What you now know

| | |
|---|---|
| 3.3 V only | This board has no protection against 5 V |
| A4 and A5 | Fixed I2C pins on the Uno |
| `CSB` and `SDO` | Left alone, because the board sets them |
| Internal pull-ups | Turned off so the line stays at 3.3 V |
| `0x76` | This sensor's address, because SDO is held low |
| `endTransmission()` | Returns 0 when a chip acknowledged |
