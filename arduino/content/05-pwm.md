<p class="modnum">Module 5</p>

# Half on

----

## The problem

`digitalWrite` gives you 5 volts or 0 volts.

So how do you get an LED that is **half** as bright?

----

## You cannot

A digital pin is a switch, not a dial.

There is no setting between on and off. The hardware does not have one.

<p class="sub">So we cheat.</p>

----

## Switch it faster than the eye

Turn the pin on and off hundreds of times a second.

Spend more of each cycle on, and the LED looks brighter. Less, and it looks dimmer.

<p class="sub">This is called <strong>PWM</strong>, for pulse width modulation.</p>

----

## One cycle

<img src="content/img/pwm-wave.svg" alt="A PWM cycle showing on time and off time">

----

## Changing the duty cycle

<img src="content/img/pwm-duty.svg" alt="Duty cycle against LED brightness" style="max-height:600px">

----

## Setting it in code

<img src="content/img/fn-analogwrite.svg" alt="analogWrite(9, 128); explained">

----

### Why 255 and not 100

<img src="content/img/byte.svg" alt="One byte is eight bits, so 256 values from 0 to 255">

<p class="sub">Not a percentage. <code>128</code> is roughly half, <code>64</code> is roughly a quarter.</p>

----

## Only six pins can do it

<div class="board">
<div class="ph" style="height:300px">
<span><b>IMAGE</b>
Same board image, with the six pins marked ~
highlighted along the digital header.</span>
</div>
<div class="hl" style="left:30%;top:5%;width:5%;height:12%"></div>
<div class="hl" style="left:38%;top:5%;width:5%;height:12%"></div>
<div class="hl" style="left:46%;top:5%;width:5%;height:12%"></div>
<div class="hltag" style="left:57%;top:6%">3 5 6 9 10 11</div>
</div>

<p class="sub">Look for the tilde. <code>analogWrite</code> on any other pin does nothing useful.</p>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Dim your LED</h2>

<div class="try">
<span class="lbl">Your turn</span>

Your LED is on pin 6, which has a tilde.

```
analogWrite(6, 128);
```

Put that in <code>setup</code>, with nothing in <code>loop</code>, and upload.

Then try 20, then 200.
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Make it fade</h2>

<div class="try">
<span class="lbl">Your turn</span>

Use a loop to walk the value from 0 up to 255 and back down.

You will need a small <code>delay</code> inside the loop, or it happens too fast to see.
</div>

<details>
<summary>One way to write it</summary>

```cpp
int ledPin = 6;

void setup() {
    pinMode(ledPin, OUTPUT);
}

void loop() {
    for (int v = 0; v <= 255; v++) {
        analogWrite(ledPin, v);
        delay(4);
    }
    for (int v = 255; v >= 0; v--) {
        analogWrite(ledPin, v);
        delay(4);
    }
}
```
</details>

----

## It is not an analog voltage

This matters, and it catches people out.

<div class="two">
<div>

<h4>What it is not</h4>

The pin sitting at 2.5 volts.

</div>
<div>

<h4>What it is</h4>

The pin slamming between 5 and 0, hundreds of times a second.

</div>
</div>

<p class="sub">Put a meter on it and you will read an average. Put a scope on it and you will see the square wave.</p>

----

## Why that distinction matters

<div class="box note">
<span class="lbl">It depends what you connect</span>
An <strong>LED</strong> averages it out, because your eye is slow.

A <strong>motor</strong> averages it out, because it is heavy and cannot react that fast.

A <strong>radio</strong> or an <strong>audio circuit</strong> will not average it out. It will hear the switching.
</div>

----

## The same trick drives a motor

`analogWrite` on a motor sets its **speed**, for exactly the same reason.

<p class="sub">Wiring a motor needs a transistor, which is the next module.</p>

----

## If nothing changes

<div class="box trouble">
<span class="lbl">Check in this order</span>
<ul>
<li><strong>The pin has no tilde.</strong> On any other pin, <code>analogWrite</code> just switches fully on above 128 and fully off below. Move the wire to 3, 5, 6, 9, 10 or 11.</li>
<li><strong>The value is above 255.</strong> Anything higher wraps around and behaves oddly.</li>
<li><strong>It is in <code>loop</code> with no delay.</strong> Fine, but it will look the same as a fixed value.</li>
<li><strong>Still blinking.</strong> An old <code>digitalWrite</code> is probably still in <code>loop</code> fighting it.</li>
</ul>
</div>

----

## What you now know

| | |
|---|---|
| PWM | Fast switching that imitates a level |
| Duty cycle | The fraction of each cycle spent on |
| `analogWrite(pin, 0-255)` | Sets the duty cycle |
| The six ~ pins | The only ones that can do it |
| Not analog | Still only ever 5 V or 0 V |
