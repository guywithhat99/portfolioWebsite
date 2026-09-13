<p class="modnum">Module 6</p>

# A brightness dial

----

## What you need

<div class="box kit">
<span class="lbl">From your kit</span>
Everything from the last module, plus the potentiometer
</div>

----

## The potentiometer

<div class="two" style="align-items:center">
<div>

<img src="content/img/potentiometer-pinout.webp" alt="Potentiometer internals: resistive track, sliding arm, and three pins" style="max-height:500px">

</div>
<div>

<img src="content/img/potentiometer.webp" alt="A potentiometer" style="max-height:180px;margin:0 0 .6em 0">

Three legs, and a knob.

Inside is a strip of resistive material with a contact that slides along it.

</div>
</div>

----

## What is actually inside

<img src="content/img/pot-inside.svg" alt="A resistor track split into two resistances by a sliding contact">

----

### The part that matters

The two outer legs are the **ends of the track**. The resistance between them never changes.

The middle leg is the **sliding contact**.

Turning the knob moves the contact, so one side of the track gets longer and the other gets shorter.

<p class="sub">Two resistances that always add up to the same total.</p>

----

## That gives you two different parts

<div class="two">
<div>

<h4>Use all three legs</h4>

You get a <strong>voltage divider</strong>. The middle leg sits somewhere between whatever the two ends are connected to.

</div>
<div>

<h4>Use two legs</h4>

One end and the middle. You get a plain <strong>variable resistor</strong>, and the knob changes its value.

</div>
</div>

<p class="sub">Same component. Which one it is depends on how you wire it.</p>

----

## We want the divider

<img src="content/img/pot-divider.svg" alt="With 5V and 0V across the ends, the middle leg gives a voltage set by the wiper position">

----

### Why this is the useful one

The Arduino can measure a **voltage**. It cannot measure a resistance directly.

So we put 5 V across the track and read the middle leg.

<p class="sub">Note the voltage follows the <em>ratio</em> of the two sides. A 10 k pot and a 1 k pot both give 2.5 V at the halfway point.</p>

----

## Wiring it

<img src="content/img/potentiometerdiagram.png" alt="Potentiometer wired to 5V, GND and A0" style="max-height:540px">

<p class="sub">Which outer leg goes to 5 V and which to ground only decides which way the knob counts.</p>

----

## Reading it

```cpp
int value = analogRead(A0);
```

This one **gives you a number back**, which is why it goes on the right of an `=`.

<p class="sub">Turned fully down you get <code>0</code>. Fully up you get <code>1023</code>.</p>

----

### Why 1023

The chip measures the voltage and reports it as one of **1024 steps**, counting from zero.

<p class="sub">That is 10 bits. It is a property of the hardware, not a choice you make.</p>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">See the numbers</h2>

<div class="try">
<span class="lbl">Your turn</span>

Print <code>analogRead(A0)</code> to the Serial Monitor in a loop, with a short delay.

Turn the knob slowly from one end to the other and watch the number move.
</div>

<details>
<summary>One way to write it</summary>

```cpp
void setup() {
    Serial.begin(9600);
}

void loop() {
    Serial.println(analogRead(A0));
    delay(100);
}
```
</details>

----

## Now drive the LED with it

You have a number from the knob. You have `analogWrite` for brightness.

But the two do not use the same range.

----

## The ranges do not match

<img src="content/img/adc-to-pwm.svg" alt="analogRead gives 0 to 1023, analogWrite takes 0 to 255">

----

### So divide by four

```cpp
int knob = analogRead(A0);
analogWrite(ledPin, knob / 4);
```

<div class="box warn">
<span class="lbl">If you skip this</span>
Anything above 255 wraps around, so the LED gets brighter, snaps back to dark, and gets brighter again, four times per turn of the knob.
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Build the dial</h2>

<div class="try">
<span class="lbl">Your turn</span>

Make the knob control the brightness of your LED.

Read the knob, scale it, write it, repeat.
</div>

<details>
<summary>One way to write it</summary>

```cpp
int ledPin = 6;

void setup() {
    pinMode(ledPin, OUTPUT);
}

void loop() {
    int knob = analogRead(A0);
    analogWrite(ledPin, knob / 4);
}
```

No `delay` needed. The loop runs thousands of times a second and the LED simply
tracks the knob.
</details>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Invert it</h2>

<div class="try">
<span class="lbl">Your turn</span>

Change one line so turning the knob <strong>up</strong> makes the LED <strong>dimmer</strong>.
</div>

<details>
<summary>Hint</summary>
You want the value to run the other way. The largest value <code>analogWrite</code> takes is 255.
</details>

<details>
<summary>Answer</summary>

```cpp
analogWrite(ledPin, 255 - (knob / 4));
```
</details>

----

## What you just built

A sensor reading turned into an actuator output, continuously, in a loop.

<p class="sub">Read something, scale it, drive something. Almost every embedded program is this shape.</p>

----

## If it does not work

<div class="box trouble">
<span class="lbl">Check in this order</span>
<ul>
<li><strong>The LED flickers between bright and dark as you turn.</strong> The <code>/ 4</code> is missing.</li>
<li><strong>The reading jumps around on its own.</strong> The middle leg is not connected, or an outer leg is missing 5 V or ground. A floating analog pin reads noise.</li>
<li><strong>It only works at one end of the travel.</strong> The outer legs may be swapped. Harmless, just turn the knob the other way or swap them back.</li>
<li><strong>Nothing at all.</strong> Check the LED is still on a pin with a tilde.</li>
</ul>
</div>

----

## What you now know

| | |
|---|---|
| Potentiometer | A knob that taps off a voltage between 5 V and 0 V |
| `analogRead(pin)` | Returns 0 to 1023 |
| 10 bits in, 8 bits out | The ADC is finer than the PWM, so scale between them |
| A floating input | Reads noise, not zero |
