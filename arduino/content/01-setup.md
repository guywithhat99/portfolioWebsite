<p class="modnum">Module 1</p>

# Setup

----

## Install the IDE

<span class="step">1.</span> Copy the installer off one of the USB sticks.

<span class="step">2.</span> Run it. Accept the defaults.

<span class="step">3.</span> On Windows, say yes if it asks to install a driver.

----

### When it opens

<div class="ph" style="height:400px">
<span><b>SCREENSHOT</b>
Arduino IDE 2.x just opened, empty sketch visible.
Full window.</span>
</div>

----

## Plug in the board

<div class="two img-l">
<div>
<div class="ph" style="height:330px">
<span><b>PHOTO</b>
Uno powered on, green ON LED clearly lit,
USB cable attached.</span>
</div>
</div>
<div>

Connect the USB cable to the Uno, then to your laptop.

A green light marked <code>ON</code> should come on.

<p class="sub">An orange light may also blink. Boards often arrive with a test program on them.</p>

</div>
</div>

----

## Choose the board

**Tools → Board → Arduino AVR Boards → Arduino Uno**

<div class="ph" style="height:330px">
<span><b>SCREENSHOT</b>
Tools → Board menu open, Arduino Uno highlighted.
Cropped to the menu.</span>
</div>

----

## Choose the port

**Tools → Port**

Pick the one that appeared when you plugged the board in.

| Your system | Looks like |
|---|---|
| Windows | `COM3`, `COM4`, usually the highest number |
| macOS | `/dev/cu.usbmodem...` |
| Linux | `/dev/ttyACM0` |

----

### Why there are two settings

<div class="two">
<div>

<h4>Board</h4>

What chip to compile for.

</div>
<div>

<h4>Port</h4>

Which cable to send it down.

</div>
</div>

----

## Upload something

<span class="step">1.</span> **File → Examples → 01.Basics → Blink**

<span class="step">2.</span> Click the arrow button, top left.

<div class="ph" style="height:230px">
<span><b>SCREENSHOT</b>
IDE toolbar, cropped tight, Upload arrow clearly visible.</span>
</div>

----

### It worked if

<span class="yes">✓</span> The bottom of the window says **Done uploading**

<span class="yes">✓</span> The orange light marked `L` blinks once a second

----

<p class="modnum">Try it</p>
<h2 class="tryhead">Change the speed</h2>

<div class="try">
<span class="lbl">Your turn</span>

Find the two lines that say <code>delay(1000);</code>

Change both to <code>delay(100);</code> and upload again.
</div>

----

### What that number is

Milliseconds.

`1000` is one second. `100` is a tenth of a second.

----

## If it did not work

<p class="sub">Find the one that matches what you are seeing.</p>

----

### No green light

<div class="box trouble">
<span class="lbl">Try in this order</span>
<ul>
<li><strong>A different USB cable.</strong> Some carry power but no data.</li>
<li><strong>A different USB port.</strong> Avoid hubs and docks.</li>
<li><strong>A different board.</strong> Grab a spare rather than debugging it.</li>
</ul>
</div>

----

### The Port menu is empty

<div class="box trouble">
<span class="lbl">Try in this order</span>
<ul>
<li><strong>A different USB cable.</strong> Power-only cables light the board but your laptop never sees a device.</li>
<li><strong>Close and reopen the IDE.</strong> The port list is built at startup and does not always notice a board plugged in afterwards.</li>
<li><strong>Try another USB port.</strong> Costs five seconds and fixes it more often than it should.</li>
</ul>
</div>

----

### The upload fails

<div class="box trouble">
<span class="lbl">Match the message</span>
<ul>
<li><code>programmer is not responding</code><br>Wrong port, or a cable with no data wires.</li>
<li><code>Board at ... is not available</code><br>Unplug, wait five seconds, plug back in, reselect the port.</li>
<li><strong>Compiles but never finishes</strong><br>Another program is holding the port. Close other IDE windows.</li>
<li><strong>Uploads but nothing blinks</strong><br>Check the board is set to Uno, not Nano.</li>
</ul>
</div>
