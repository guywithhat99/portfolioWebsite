<p class="modnum">Module 1</p>

# Setup

----

## Download the IDE

Go to **[arduino.cc/en/software](https://www.arduino.cc/en/software)**

Download **Arduino IDE 2** for your operating system.

<p class="sub">Not the Legacy IDE (1.8). Version 2 is the current one.</p>

----

## Install it

| Your system | What to do |
|---|---|
| **Windows** | Run the `.exe`. Accept the defaults. Say yes when it asks to install drivers |
| **macOS** | Open the `.dmg` and drag Arduino IDE into Applications |
| **Linux** | Use the AppImage. Make it executable, then run it |

<p class="sub">The first time it opens it may download a few extra parts. Let it finish.</p>

----

### When it opens

<img src="content/img/arduinoideopen.png" alt="Arduino IDE 2 just opened, showing an empty sketch" style="max-height:620px">

----

## Plug in the board

<div class="two img-l">
<div>
<img src="content/img/uno-powered-on.jpeg" alt="Arduino Uno powered on with the green ON light lit" style="max-height:380px">
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

<img src="content/img/choosetheboard.png" alt="Tools, Board menu with Arduino Uno selected" style="max-height:480px">

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

<img src="content/img/UploadArrow.png" alt="The Upload arrow button in the IDE toolbar" style="max-height:260px">

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
