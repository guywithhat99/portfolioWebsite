<p class="modnum">Module 7</p>

# The button

----

## What you need

<div class="box kit">
<span class="lbl">From your kit</span>
Push button · two jumper wires
</div>

<p class="sub">No resistor. The reason why is most of this module.</p>

----

## A button has four legs and two connections

<img src="content/img/button-legs.svg" alt="Tactile button: legs are joined in pairs, pressing joins the pairs">

----

### What that means when wiring

Take **one leg from the left** and **one from the right**.

Straddle the centre gap of the breadboard so the two sides land in different columns.

<div class="box warn">
<span class="lbl">The classic mistake</span>
Using two legs from the same side. Those are joined permanently, so the circuit behaves as though the button is always pressed.
</div>

----

## Now the real problem

A switch does not produce a voltage. It only connects two things, or does not.

So when the button is **not** pressed, what is the pin connected to?

<p class="big">Nothing.</p>

----

## A pin connected to nothing

<img src="content/img/pullup.svg" alt="A floating pin reads noise; a pull-up resistor holds it high">

----

### This is called floating

An unconnected input pin does not read `LOW`.

It picks up interference from the air, from your hand, from the mains, and reports whatever it finds.

<p class="sub">You saw this already: an unconnected analog pin gives you a number that drifts around on its own.</p>

----

## The fix is a resistor to 5 V

It holds the pin at 5 V whenever nothing else is driving it.

Press the button and the pin is connected straight to ground, which wins.

<p class="sub">This is called a <strong>pull-up resistor</strong>, because it pulls the pin up to 5 V.</p>

----

## The Uno has them built in

You do not need to wire one. The chip has a pull-up resistor on every digital pin, switched off by default.

```cpp
pinMode(2, INPUT_PULLUP);
```

That turns it on.

<p class="sub">This is why the kit list for this module has no resistor in it.</p>

----

## So the logic is backwards

<div class="two">
<div>

<h4>Not pressed</h4>

Pin is held at 5 V by the pull-up

reads <span class="no">HIGH</span>

</div>
<div>

<h4>Pressed</h4>

Pin is connected to ground

reads <span class="yes">LOW</span>

</div>
</div>

----

## Wiring it

<div class="ph" style="height:330px">
<span><b>FRITZING, BREADBOARD VIEW</b>
Button straddling the centre gap. One side to pin 2,
other side to GND. LED and 330 Ω still on pin 6.</span>
</div>

<p class="sub">Two wires. One to pin 2, one to ground.</p>

----

## Reading it

```cpp
void setup() {
    pinMode(2, INPUT_PULLUP);
    Serial.begin(9600);
}

void loop() {
    Serial.println(digitalRead(2));
    delay(100);
}
```

`digitalRead` gives back `1` for HIGH and `0` for LOW.

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Watch it change</h2>

<div class="try">
<span class="lbl">Your turn</span>

Upload that and open the Serial Monitor.

You should see a stream of <code>1</code>s that turns into <code>0</code>s while you hold the button down.
</div>

----

## Acting on it

```cpp
int ledPin = 6;

void setup() {
    pinMode(ledPin, OUTPUT);
    pinMode(2, INPUT_PULLUP);
}

void loop() {
    if (digitalRead(2) == LOW) {
        digitalWrite(ledPin, HIGH);
    } else {
        digitalWrite(ledPin, LOW);
    }
}
```

`LOW` because that is what pressed looks like.

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Light while held</h2>

<div class="try">
<span class="lbl">Your turn</span>

Make the LED come on while the button is held, and go off when released.

Then swap <code>LOW</code> for <code>HIGH</code> and see what happens.
</div>

<details>
<summary>What swapping does</summary>
The LED is on all the time and goes off when you press.

That is exactly the bug you get from forgetting the logic is inverted, and now you know what it looks like.
</details>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Dim while held</h2>

<div class="try">
<span class="lbl">Your turn</span>

You have PWM and you have a button.

Make the LED sit at half brightness normally, and go to full brightness while the button is held.
</div>

<details>
<summary>One way to write it</summary>

```cpp
void loop() {
    if (digitalRead(2) == LOW) {
        analogWrite(ledPin, 255);
    } else {
        analogWrite(ledPin, 128);
    }
}
```
</details>

----

## If it does not work

<div class="box trouble">
<span class="lbl">Check in this order</span>
<ul>
<li><strong>It behaves as if always pressed.</strong> Both wires are on legs from the same side of the button. Those are joined permanently. Move one across the gap.</li>
<li><strong>The reading flickers between 0 and 1 on its own.</strong> <code>INPUT_PULLUP</code> is missing, so the pin is floating.</li>
<li><strong>The LED is on until you press.</strong> The logic is inverted. Pressed is <code>LOW</code>.</li>
<li><strong>Nothing changes at all.</strong> The ground wire is missing, so pressing connects the pin to nothing.</li>
</ul>
</div>

----

## What you now know

| | |
|---|---|
| A button | Two connections, four legs. Same side is joined |
| Floating | An unconnected input reads noise, not zero |
| Pull-up | A resistor holding the pin high until something pulls it down |
| `INPUT_PULLUP` | Uses the one already inside the chip |
| Pressed is `LOW` | Because pressing connects the pin to ground |
