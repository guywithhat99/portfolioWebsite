<p class="modnum">Module 9</p>

# The servo

----

## What you need

<div class="box kit">
<span class="lbl">From your kit</span>
Servo motor · three jumper wires
</div>

<p class="sub">No transistor and no diode this time. A servo has its own driver circuit built in.</p>

----

## Not the same as the motor

<img src="content/img/servo-vs-motor.svg" alt="The DC motor is told how hard to push; the servo is told where to go">

----

### What is in the box

A small motor, a gearbox, and a sensor that measures the output shaft.

You give it an angle. Its own circuit compares that to where the shaft actually is, and drives the motor until they match.

<p class="sub">Then it keeps checking, so it holds position even if something pushes against it.</p>

----

## Three wires

| Wire | Usually | Goes to |
|---|---|---|
| Power | red | `5V` |
| Ground | brown or black | `GND` |
| Signal | orange or yellow | any digital pin |

<p class="sub">Colours vary between makes. The order on the plug is the reliable part.</p>

----

## How you tell it an angle

<img src="content/img/servo-pulse.svg" alt="1 ms means 0 degrees, 1.5 ms means 90, 2 ms means 180">

----

### This is not `analogWrite`

`analogWrite` changes how much of each cycle is on, at a fixed frequency near 490 Hz.

A servo wants one short pulse every 20 ms, and reads its **width** in microseconds.

<p class="sub">Different meaning, different timing. <code>analogWrite</code> on a servo does not work.</p>

----

## So somebody wrote a library

```cpp
#include <Servo.h>
```

Code somebody else wrote, that does the pulse timing for you.

<p class="sub">The angle goes in, correctly shaped pulses come out.</p>

----

### Using it

```cpp
#include <Servo.h>

Servo arm;

void setup() {
    arm.attach(9);
    arm.write(90);
}
```

<span class="step">1.</span> `Servo arm;` makes one to work with, named `arm`

<span class="step">2.</span> `arm.attach(9)` tells it which pin

<span class="step">3.</span> `arm.write(90)` sends it to 90 degrees

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Point it somewhere</h2>

<div class="try">
<span class="lbl">Your turn</span>

Wire the servo to pin 9, upload that program, and watch it move to the middle.

Then change the angle to 0, and to 180.
</div>

----

## Sweeping

```cpp
#include <Servo.h>

Servo arm;

void setup() {
    arm.attach(9);
}

void loop() {
    for (int a = 0; a <= 180; a++) {
        arm.write(a);
        delay(15);
    }
    for (int a = 180; a >= 0; a--) {
        arm.write(a);
        delay(15);
    }
}
```

The `delay(15)` gives it time to actually get there before you ask for the next angle.

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Sweep it</h2>

<div class="try">
<span class="lbl">Your turn</span>

Run the sweep.

Then try <code>delay(1)</code> instead of <code>delay(15)</code> and watch what happens.
</div>

<details>
<summary>What you should see</summary>
It moves less far, and less smoothly.

You are asking for new angles faster than the servo can physically reach them, so it is always chasing a target that has already moved.
</details>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">A position dial</h2>

<div class="try">
<span class="lbl">Your turn</span>

Use the potentiometer to set the servo angle.

The knob gives you 0 to 1023. The servo wants 0 to 180.
</div>

<details>
<summary>Hint</summary>
Same problem as the LED dial, different numbers. There is a built-in function called <code>map</code> that does this, or you can work out the division yourself.
</details>

<details>
<summary>One way to write it</summary>

```cpp
#include <Servo.h>

Servo arm;

void setup() {
    arm.attach(9);
}

void loop() {
    int knob = analogRead(A0);
    arm.write(map(knob, 0, 1023, 0, 180));
}
```

`map` takes a value, the range it is in now, and the range you want it in.
</details>

----

## Two things that catch people

<div class="box warn">
<span class="lbl">PWM stops working on pins 9 and 10</span>
The Servo library takes over the timer those two pins use.

If your motor from the last module was on pin 9, <code>analogWrite</code> to it will stop doing anything the moment you include this library.
</div>

----

<div class="box warn">
<span class="lbl">Servos pull a lot of current</span>
Especially when they start moving or when something resists them.

If the board resets or the servo twitches oddly, power it from the barrel jack or the power bank rather than USB.
</div>

----

## If it does not work

<div class="box trouble">
<span class="lbl">Check in this order</span>
<ul>
<li><strong>It buzzes and does not move.</strong> It is being asked for an angle it cannot reach, and straining against its own end stop. Stay between 0 and 180.</li>
<li><strong>It jitters constantly.</strong> Usually power. Try the barrel jack or power bank.</li>
<li><strong>Nothing at all.</strong> Check the plug orientation. Signal is the wire on the end nearest the pin number, not the middle one.</li>
<li><strong>The board resets when it moves.</strong> Too much current for USB.</li>
<li><strong>Your LED or motor on pin 9 or 10 stopped working.</strong> The Servo library owns that timer now.</li>
</ul>
</div>

----

## What you now know

| | |
|---|---|
| Servo | A motor that knows where it is and holds position |
| Pulse width | 1 ms to 2 ms, repeated every 20 ms, is the angle |
| A library | Someone else's code, brought in with `#include` |
| `map` | Rescales a value from one range to another |
| Timer conflicts | The Servo library costs you PWM on pins 9 and 10 |
