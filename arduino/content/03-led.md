<p class="modnum">Module 3</p>

# Wire your own LED

----

## What you need

<div class="box kit">
<span class="lbl">From your kit</span>
Breadboard · one LED · one 330 Ω resistor · two jumper wires
</div>

<p class="sub">The light you have been blinking is soldered to the board. This one you wire yourself.</p>

----

## An LED has a front and a back

<div class="two">
<div>

<img src="content/img/led-diagram.png" alt="LED showing the long leg and the short leg" style="max-height:520px">

</div>
<div>

One leg is <strong>longer</strong>. That is the side current goes <strong>in</strong>.

One leg is <strong>shorter</strong>. That is the side current comes <strong>out</strong>.

Put it in backwards and nothing happens.

</div>
</div>

----

## It also needs a resistor

An LED on its own will draw as much current as the board will give it.

That is more than it can survive.

The resistor limits the current to something the LED is happy with.

<p class="sub">Your kit has 330 Ω resistors. That is the right sort of value for an LED on a 5 volt board.</p>

----

## How the holes connect

<img src="content/img/breadboard-anatomy.svg" alt="Breadboard columns are joined underneath; the centre gap breaks the connection" style="max-height:640px">

----

## The circuit

<div class="two" style="align-items:center">
<div>

<img src="content/img/LEDcircuit.png" alt="LED circuit wiring diagram" style="max-height:600px">

</div>
<div>

<img src="content/img/ledcircuitschematic.png" alt="LED circuit schematic: pin 9, resistor, LED, ground" style="max-height:480px">

</div>
</div>

----

## The same thing, on the breadboard

<img src="content/img/ledcircuitreal.jpeg" alt="The LED circuit built on a breadboard" style="max-height:620px">

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Build it</h2>

<div class="try">
<span class="lbl">Your turn</span>

<span class="step">1.</span> Unplug the USB cable first.

<span class="step">2.</span> Build the circuit from the breadboard picture.

<span class="step">3.</span> Check the long leg is on the resistor side.

<span class="step">4.</span> Plug the USB cable back in.
</div>

----

## Now point the code at it

<div class="two">
<div>

```cpp
void setup() {
    pinMode(9, OUTPUT);
}

void loop() {
    digitalWrite(9, HIGH);
    delay(1000);
    digitalWrite(9, LOW);
    delay(1000);
}
```

</div>
<div style="font-size:.84em">

The same program as Module 2.

Every <code>13</code> is now a <code>9</code>, because that is the pin you wired to.

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Run it</h2>

<div class="try">
<span class="lbl">Your turn</span>

Change the three <code>13</code>s to <code>9</code>s and upload.

Your own LED should blink.
</div>

----

## If it does not light

<div class="box trouble">
<span class="lbl">Check in this order</span>
<ul>
<li><strong>The LED is backwards.</strong> Long leg towards the resistor. This is the most common one, and it does no damage. Turn it around.</li>
<li><strong>Both legs are in the same column.</strong> Then current skips the LED entirely.</li>
<li><strong>A wire is in the wrong column.</strong> Follow the path with your finger: pin 9, resistor, long leg, short leg, ground.</li>
<li><strong>The code still says 13.</strong> Check all three lines.</li>
<li><strong>No ground wire.</strong> Current has to get back to the board.</li>
</ul>
</div>

----
## One number, written once

```cpp
int ledPin = 9;

void setup() {
    pinMode(ledPin, OUTPUT);
}

void loop() {
    digitalWrite(ledPin, HIGH);
    delay(1000);
    digitalWrite(ledPin, LOW);
    delay(1000);
}
```

Wherever the pin number appeared, the name goes instead.

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Move the LED</h2>

<div class="try">
<span class="lbl">Your turn</span>

<span class="step">1.</span> Unplug the USB cable.

<span class="step">2.</span> Move the jumper from pin 9 to pin 6.

<span class="step">3.</span> Plug back in, and change <strong>one line</strong> so it works again.
</div>

<details>
<summary>Which line</summary>

```cpp
int ledPin = 6;
```

Nothing else in the program mentions a pin number.
</details>

----

## What you now know

| | |
|---|---|
| LED | Long leg in, short leg out |
| Resistor | Limits current so the LED survives |
| Breadboard column | Five holes, joined underneath |
| Centre gap | Breaks the connection between halves |
| Pin number | The one in code must match the one you wired |
