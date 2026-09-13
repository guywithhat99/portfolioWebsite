<p class="modnum">Module 2</p>

# Your first program

----

## Every program has two parts

<div class="two">
<div>

```cpp
void setup() {

}

void loop() {

}
```

</div>
<div>

<img src="content/img/setup-loop.svg" alt="setup runs once, loop runs forever" style="max-height:430px">

</div>
</div>

----

## What we are making

The small orange light on the board, marked `L`.

<div class="board">
<div class="ph" style="height:310px">
<span><b>IMAGE</b>
Top-down Arduino Uno, whole board, filling the frame.
Reused across the next few slides.</span>
</div>
<div class="hl" style="left:56%;top:32%;width:9%;height:15%"></div>
<div class="hltag" style="left:66%;top:34%">the L light</div>
</div>

----

## It is wired to pin 13

<div class="board">
<div class="ph" style="height:310px">
<span><b>IMAGE</b>
Same board image.</span>
</div>
<div class="hl t" style="left:41%;top:5%;width:7%;height:12%"></div>
<div class="hltag t" style="left:49%;top:7%">pin 13</div>
<div class="hl" style="left:56%;top:32%;width:9%;height:15%"></div>
</div>

<p class="sub">Whatever you do to pin 13, that light does.</p>

----

## A pin is on or off

<div class="two">
<div>

<h4>On</h4>

<p class="big">5 volts</p>

Written as <code>HIGH</code>

</div>
<div>

<h4>Off</h4>

<p class="big">0 volts</p>

Written as <code>LOW</code>

</div>
</div>

<p class="sub">There is nothing in between.</p>

----

## pinMode

<img src="content/img/fn-pinmode.svg" alt="pinMode(13, OUTPUT); explained">

----

### Put it in setup

```cpp
void setup() {
    pinMode(13, OUTPUT);
}

void loop() {

}
```

Pin 13 only needs telling once.

<p class="sub">Things that happen once go in <code>setup</code>. Things that repeat go in <code>loop</code>.</p>

----

## digitalWrite

<img src="content/img/fn-digitalwrite.svg" alt="digitalWrite(13, HIGH); explained">

----

### Turn the light on

```cpp
void setup() {
    pinMode(13, OUTPUT);
}

void loop() {
    digitalWrite(13, HIGH);
}
```

----

### If you ran this now

The light would come on and stay on.

`loop` would keep setting the pin high, millions of times a second.

Nothing would ever turn it off.

----

## Wait a second

```cpp
void setup() {
    pinMode(13, OUTPUT);
}

void loop() {
    digitalWrite(13, HIGH);
    delay(1000);
}
```

----

### Turn it off

```cpp
void setup() {
    pinMode(13, OUTPUT);
}

void loop() {
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13, LOW);
}
```

Same function, different value.

----

### Wait again

```cpp
void setup() {
    pinMode(13, OUTPUT);
}

void loop() {
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13, LOW);
    delay(1000);
}
```

Without this, the light would switch off and straight back on.

<p class="sub">Too fast to see. It would just look dim.</p>

----

## The finished program

<div class="two">
<div>

```cpp
void setup() {
    pinMode(13, OUTPUT);
}

void loop() {
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13, LOW);
    delay(1000);
}
```

</div>
<div style="font-size:.82em">

<span class="step">1.</span> Claim the pin. Once.

<span class="step">2.</span> On.

<span class="step">3.</span> Wait.

<span class="step">4.</span> Off.

<span class="step">5.</span> Wait.

<span class="step">↻</span> Back to 2.

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Type it in</h2>

<div class="try">
<span class="lbl">Your turn</span>

<span class="step">1.</span> <strong>File → New Sketch</strong>

<span class="step">2.</span> Delete what is already in the window.

<span class="step">3.</span> Type the program above.

<span class="step">4.</span> Upload.
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Break it</h2>

<div class="try">
<span class="lbl">Your turn</span>

Delete the semicolon at the end of the first <code>delay(1000)</code> line.

Upload, and read the red text at the bottom.
</div>

----

### What it says

```
expected ';' before 'digitalWrite'
```

----

### Look where it points

You broke the `delay` line.

It names the `digitalWrite` line, which is the next one down.

<div class="box note">
<span class="lbl">Worth knowing</span>
When an error points at a line that looks fine, check the line above it.
</div>

Put the semicolon back.

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Make a heartbeat</h2>

<div class="try">
<span class="lbl">Your turn</span>

Make the light pulse: <strong>on, off, on, off, then a long pause.</strong>

Try 100, 100, 100, then 700 milliseconds.
</div>

<details>
<summary>Hint</summary>
Four <code>digitalWrite</code> lines and four <code>delay</code> lines, alternating, inside <code>loop</code>. Only the numbers change.
</details>

<details>
<summary>One way to write it</summary>

```cpp
void loop() {
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(700);
}
```
</details>

----

## What you now know

| | |
|---|---|
| `setup()` | Runs once |
| `loop()` | Runs forever |
| `pinMode(pin, OUTPUT)` | Claims a pin for driving |
| `digitalWrite(pin, HIGH)` | 5 volts |
| `digitalWrite(pin, LOW)` | 0 volts |
| `delay(ms)` | Stops everything for that long |
