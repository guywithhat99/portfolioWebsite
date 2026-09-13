<p class="modnum">Module 8</p>

# Driving a motor

----

## What you need

<div class="box kit">
<span class="lbl">From your kit</span>
DC motor · NPN transistor · diode · one 330 Ω resistor · jumper wires
</div>

----

## The obvious thing to try

You have driven an LED from a pin. A motor has two wires.

So connect the motor to a pin and call `digitalWrite`.

<p class="big">Do not do this.</p>

----

## Why not

<img src="content/img/current-budget.svg" alt="An LED wants 10 mA, a pin can give 20 mA, a motor wants 250 mA">

----

### What would actually happen

The motor would barely twitch, because the pin cannot supply what it needs.

Then the pin would overheat, and that part of the chip would stop working. Permanently.

<p class="sub">The rest of the board usually keeps running, which makes it a confusing fault to find later.</p>

----

## The pin is a signal, not a supply

This is the idea worth taking away from this module.

A microcontroller pin exists to **say something**, not to **power something**.

Anything that needs real current gets its power from the supply, and the pin only decides when.

----

## A transistor does that job

<img src="content/img/transistor-switch.svg" alt="Transistor circuit: pin 9 through a resistor into the base, motor from 5 V to the collector, emitter to ground" style="max-height:600px">

----

### Three legs

| Leg | Goes to |
|---|---|
| **Base** | Your pin, through a resistor |
| **Collector** | The motor |
| **Emitter** | Ground |

Current from the pin into the base allows a much larger current to flow from collector to emitter.

----

### Why the base gets a resistor

Without one, the pin sees almost a short circuit to ground through the base.

<p class="sub">The 330 Ω limits it to a few milliamps, which is plenty to switch the transistor on.</p>

----

## One more part

A motor is a coil of wire. Coils do not like being switched off suddenly.

----

## What the coil does

<img src="content/img/flyback.svg" alt="Without a diode the collapsing field has nowhere to go">

----

### In words

While the motor runs, energy is stored in its magnetic field.

Switch it off and that field collapses, pushing current that has nowhere to go. The voltage rises until something gives, and the something is usually your transistor.

The diode gives that current a loop to die away in.

----

## Telling which end is which

<img src="content/img/diode-band.svg" alt="The band on the physical diode is the bar in the schematic symbol">

----

### Which way round it goes

The diode sits **across the motor**, with the **band towards 5 V**.

That is deliberately the wrong way for current to flow, so it does nothing at all while the motor is running.

<p class="sub">It only conducts when the coil collapses and pushes the voltage the other way.</p>

<div class="box warn">
<span class="lbl">Backwards is not harmless here</span>
Fitted the wrong way it is a direct short across your supply. Check the band before you plug the board in.
</div>

----

## Wiring it

<img src="content/img/motordiagram.png" alt="Motor driver wiring: pin 9 through a resistor to the transistor base, motor to 5V, diode across the motor" style="max-height:600px">

----

## The code is the same as the LED

```cpp
int motorPin = 9;

void setup() {
    pinMode(motorPin, OUTPUT);
}

void loop() {
    digitalWrite(motorPin, HIGH);
    delay(2000);
    digitalWrite(motorPin, LOW);
    delay(2000);
}
```

Nothing new. The transistor does the hard part.

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Spin it</h2>

<div class="try">
<span class="lbl">Your turn</span>

Build the circuit, check the diode band, then upload.

Two seconds on, two seconds off.
</div>

----

## Now vary the speed

Pin 9 has a tilde, so `analogWrite` works here too.

```cpp
analogWrite(motorPin, 150);
```

The transistor switches on and off hundreds of times a second, and the motor is too heavy to follow. It just runs slower.

----

<p class="modnum">Try it</p>
<h2 class="tryhead">A speed dial</h2>

<div class="try">
<span class="lbl">Your turn</span>

Put the potentiometer back in and use it to control the motor speed.

You already wrote this program for the LED. It is the same one.
</div>

<details>
<summary>One way to write it</summary>

```cpp
int motorPin = 9;

void setup() {
    pinMode(motorPin, OUTPUT);
}

void loop() {
    int knob = analogRead(A0);
    analogWrite(motorPin, knob / 4);
}
```

The motor will not turn at the low end. It needs a minimum current to overcome friction before it moves at all.
</details>

----

## If it does not work

<div class="box trouble">
<span class="lbl">Check in this order</span>
<ul>
<li><strong>Nothing happens.</strong> The transistor legs are probably in the wrong order. Base, collector and emitter are not interchangeable, and the order depends on the part. Check the flat face.</li>
<li><strong>The board resets when the motor starts.</strong> The motor is pulling more than USB will give. Use the power bank or the barrel jack.</li>
<li><strong>It runs constantly, whatever the code does.</strong> Collector and emitter are swapped.</li>
<li><strong>It runs but the board behaves strangely.</strong> The diode is missing, or fitted the wrong way round.</li>
<li><strong>It will not start at low speeds.</strong> Normal. A motor needs a minimum to break friction.</li>
</ul>
</div>

----

## What you now know

| | |
|---|---|
| A pin is a signal | Roughly 20 mA. It is not a power supply |
| Transistor | A small current controlling a big one |
| Base resistor | Stops the pin being shorted to ground |
| Flyback diode | Gives the collapsing magnetic field somewhere to go |
| PWM on a motor | Same trick as the LED, and it sets speed |
