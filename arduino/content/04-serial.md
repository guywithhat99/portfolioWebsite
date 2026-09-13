<p class="modnum">Module 4</p>

# Talking back

----

## Right now the board cannot tell you anything

The only thing it can say is "the light is on" or "the light is off".

If a number in your program is wrong, you have no way to see it.

----

## The cable works both ways

The same USB cable that uploads your code can carry **text back**.

That text appears in a window on your laptop called the **Serial Monitor**.

<p class="sub">This is the tool you will use to find every problem from here on.</p>

----

## Switching it on

```cpp
void setup() {
    Serial.begin(9600);
}
```

`9600` is the speed. The monitor has to be set to the same number.

The baud rate is how many bits per second. `9600` means 9600.

No wire carries the timing, so both ends agree on the speed in advance.

<p class="sub">Opened once, in <code>setup</code>.</p>


----

## Sending a line of text

```cpp
void setup() {
    Serial.begin(9600);
    delay(1000);
    Serial.println("Hello");
}

void loop() {

}
```

Open the connection, give your laptop a second to connect, then send one line.

<p class="sub">Nothing in <code>loop</code>, so it sends once and then sits there.</p>

----

## Opening the monitor

<img src="content/img/openmonitor.png" alt="Arduino IDE with the Serial Monitor open, showing Hello, and the baud rate dropdown" style="max-height:600px">

----

## The two numbers must match

<div class="two">
<div>

<h4>In your code</h4>

```cpp
Serial.begin(9600);
```

</div>
<div>

<h4>In the monitor</h4>

The dropdown in the corner must also say <strong>9600</strong>.

</div>
</div>

<div class="box warn">
<span class="lbl">If they do not match</span>
You get a line of nonsense characters instead of your text. Nothing is broken. Change the dropdown to match the code.
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Say hello</h2>

<div class="try">
<span class="lbl">Your turn</span>

<span class="step">1.</span> Type the program above and upload it.

<span class="step">2.</span> Open the Serial Monitor.

<span class="step">3.</span> Set the dropdown to <strong>9600</strong>.

<span class="step">4.</span> Press the reset button on the board to see it again.
</div>

----

## Printing a number instead

```cpp
int ledPin = 6;

void setup() {
    Serial.begin(9600);
    Serial.println(ledPin);
}
```

No quotes this time.

<div class="two">
<div>

<h4>With quotes</h4>

<code>Serial.println("ledPin")</code>

prints the word <code>ledPin</code>

</div>
<div>

<h4>Without quotes</h4>

<code>Serial.println(ledPin)</code>

prints <code>6</code>

</div>
</div>

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Print your pin number</h2>

<div class="try">
<span class="lbl">Your turn</span>

Print your <code>ledPin</code> variable to the monitor.

Then change the variable and check the printed number changes too.
</div>

----

## Watching the blink happen

```cpp
int ledPin = 6;

void setup() {
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    Serial.println("on");
    digitalWrite(ledPin, HIGH);
    delay(1000);
    Serial.println("off");
    digitalWrite(ledPin, LOW);
    delay(1000);
}
```

Now you can see what the program is doing, not just what the light is doing.

----

## Counting the blinks

```cpp
count = count + 1;
```

Take whatever `count` is, add one, put it back.

----

### Counting in the program

```cpp
int ledPin = 6;
int count = 0;

void setup() {
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    count = count + 1;
    Serial.println(count);
    digitalWrite(ledPin, HIGH);
    delay(1000);
    digitalWrite(ledPin, LOW);
    delay(1000);
}
```

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Count your blinks</h2>

<div class="try">
<span class="lbl">Your turn</span>

Add a counter to your blink program and print it every time round.

The monitor should count up, one line per blink.
</div>

<details>
<summary>What happens if you press reset</summary>
It starts again from 1.

The variable lives in memory, and resetting the board clears it. Nothing on an Arduino is remembered between runs unless you deliberately save it.
</details>

----

## If nothing appears

<div class="box trouble">
<span class="lbl">Check in this order</span>
<ul>
<li><strong>Nonsense characters.</strong> The dropdown does not match <code>Serial.begin</code>. Set it to 9600.</li>
<li><strong>Completely empty.</strong> The <code>Serial.begin</code> line is missing, or it is in <code>loop</code> instead of <code>setup</code>.</li>
<li><strong>It printed once and stopped.</strong> That is correct if the print is in <code>setup</code>. Press reset to see it again, or move it into <code>loop</code>.</li>
<li><strong>Upload now fails.</strong> The monitor can hold the port. Close it, upload, reopen it.</li>
</ul>
</div>

----

## What you now know

| | |
|---|---|
| `Serial.begin(9600)` | Opens the connection, once, in `setup` |
| `Serial.println(...)` | Sends one line to your laptop |
| Quotes | Text as written. No quotes, the value of a variable |
| Matching baud | The dropdown must equal the number in the code |
| `count = count + 1` | Work out the right side, store it on the left |
