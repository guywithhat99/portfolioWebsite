# Intro to Microcontrollers, Workshop Plan
**CU InSpace Avionics · self-paced web workshop**
Owner: Jack Miller · Draft 1 · 2026-09-10

---

## The one-sentence version

Take people who have never written code to the point where they can read a real
pressure sensor over I2C, stream it off the board, and then **feel the super loop
break**, so that interrupts and an RTOS arrive as the answer to a problem they
have personally hit rather than as trivia.

---

## Audience and constraints

| | |
|---|---|
| **Attendees** | 6-10, one kit each |
| **Programming experience** | Genuinely none, for most |
| **Microcontroller experience** | None |
| **Session length** | ~2 hours |
| **Number of sessions** | **As many as it takes.** Nothing is cut for time |
| **Toolchain** | Arduino IDE 2.x. Real toolchain (CMake/OpenOCD) comes later, separately |
| **Hardware** | Arduino Uno kit + GY-BMP280 barometer |
| **Pre-work** | **None.** Setup happens in the room, Module 1 |

**Estimated contact time for the full arc: 11-13 hours**:  call it six 2-hour
sessions, now that in-room setup and the debugging module are inside the budget.
The doc is one continuous resource, not chopped into sessions, so the split
floats with how fast the room actually moves.

---

## Slide philosophy

The first two drafts failed the same way: they were written for the person who
already knows the material. These are the rules now.

**1. No preamble.** No agenda, no "what you will build", no "why this matters".
A student does not need the workshop explained to them before they have touched
anything. Title slide, then the first instruction.

**2. Just in time, never just in case.** A concept appears on the slide where it
is first needed, and nowhere earlier. Digital output is explained when the LED
blinks. Analog input is explained when a knob is read. PWM is explained when
something fades. The kit is introduced part by part as each part gets used,
not as an inventory at the front.

**3. Never state the intention behind the design.** Lines like "remember this,
it comes back in Part 4" are notes from the author to themselves. Cut them.
If the workshop is built correctly the payoff lands without being announced.

**4. One idea per slide.** If a slide holds two things, it is two slides. Every
slide must fit on screen with no scrolling. `index.html` logs any slide that
overflows to the browser console, so this is checkable rather than a hope.

**5. Code is built one line at a time.** Never show a finished program and then
annotate it. Each slide adds one line to the same growing program and explains
only the line that just appeared.

**6. Images carry the explanation, not prose.** A list of pins in sentences is
useless. Anything spatial gets a picture.

**7. One image, reused.** The same board photo returns across slides with
different regions highlighted, so the picture accumulates meaning instead of
being replaced each time.

**8. Plain sentences.** No em dashes. No asides, no jokes, no observations about
how learning works, no restating a point in a cleverer way. Say it once and
move on.

**9. A slide is an explainer or an instruction, never both.** Instructions sit
in green "Try it" blocks so they are findable when someone scrolls back.

## What this means for a self-paced deck

Someone working alone will lose their place, get stuck, and scroll backwards to
find the thing they half remember. So:

- Module titles are plain nouns, not clever ones.
- Every "Try it" looks identical and is visually loud.
- Troubleshooting is split by **symptom**, so you can find your own failure
  without reading the others.
- Hints and answers are collapsed, so nobody is spoiled and nobody is stranded.

## Format

Same mechanic as the Tamagotchi page, reveal.js, arrow keys, hosted on the
site, with the content structure rebuilt.

**The 2D layout does real work here:**

- **→ Horizontal = modules.** Sweep across the top for the instructor-led intro.
- **↓ Vertical = steps within a module.** People descend at their own pace.

That maps exactly onto "some intro slides, then self-paced sections." During the
talk you stay on the top row; when people go hands-on they go down.

**Per-module template** (each becomes one vertical stack):

```
## Module N, Title              ← top row, the instructor-led slide
  ↓ Components needed            ← check your kit before wiring
  ↓ The idea                     ← the explainer, plain language, code syntax explainer
  ↓ Wire it                      ← diagram + explicit pin list
  ↓ The code                     ← full worked example, annotated
  ↓ ✋ Your Turn                  ← they write something
  ↓    ↳ hint (collapsed)
  ↓    ↳ answer (collapsed)
  ↓ When it doesn't work         ← troubleshooting: ALWAYS ≥3 possible causes
```

**File layout.** The Tamagotchi deck was a single 1,156-line `presentation.md`,
which was unwieldy to edit. This one splits into one markdown file per part , 
`00-setup.md`, `01-basics.md`, `02-analog.md`, `03-sensor.md`, `04-concurrency.md`
,  loaded as separate reveal.js sections from one `index.html`. Same navigation
for the reader, far easier to edit and to revise a single part without touching
the rest.

---

## The arc

**27 modules, four parts.** No pre-work, Module 1 is setup, in the room.

### Part 1, Getting it running
| # | Module | New C++ arriving here |
|---|---|---|
| 1 | Setup: IDE, driver, board, port, first upload |, |
| 2 | The board and the breadboard |, |
| 3 | `setup()`, `loop()`, and your first blink | statements, function calls, `pinMode`/`digitalWrite`/`delay` |
| 4 | Naming things | variables, `int`, `const` |
| 5 | The Serial Monitor, your debugging window | `Serial.begin`, `println` |
| 6 | **Is it the code or the circuit?** | bisection method · **find-the-bug #1** |
| 7 | Reading a button | `digitalRead`, `if`/`else`, `bool`, `INPUT_PULLUP` |
| 8 | Why your button fires five times | debouncing |

> **Module 6 is the addition the research demanded.** It comes right after the
> first things they build can break, and before the first circuit complex enough
> to break in two places at once.
>
> **Module 7's internal pull-up** is deliberate setup for Module 15's I2C bus
> pull-ups, one concept, two encounters.

### Part 2, Analog and PWM
| # | Module | New C++ |
|---|---|---|
| 9 | PWM, faking analog with a fast switch | `analogWrite`, duty cycle, `for` loops |
| 10 | Reading a knob | `analogRead`, ADC, `map()` |
| 11 | Reading light, the voltage divider | (circuit theory) · **find-the-bug #2** |
| 12 | Driving a servo | `#include`, libraries, objects |
| 13 | Driving a motor, transistor and flyback diode | why a pin can't source enough current |

> Module 13 is the heaviest wiring in the workshop, the one retrospective we
> found specifically ran out of time on the transistor project. Budget for it.

### Part 3, Talking to a real sensor, from the datasheet
**This is the part Jack specifically wants built around reading the datasheet.**
No library until they've earned it.

| # | Module | Notes |
|---|---|---|
| 14 | Why buses exist, I2C, addresses, pull-ups | callback to Module 7's `INPUT_PULLUP` |
| 15 | **Bits, bytes, hex and masks** | prerequisite for register work: `0x`, bit positions, `&` mask, `\|` set, `<<` shift. Taught concretely, "one byte holding three separate settings" |
| 16 | Wiring the GY-BMP280 + I2C scanner | **3.3V only, `0x76`**, disable the AVR's internal pull-ups. Scanner proves something is alive before any driver exists |
| 17 | **First datasheet read, "who are you?"** | Open the real Bosch PDF, find Table 18, read register `0xD0`, expect `0x58` |
| 18 | **Telling the sensor what to do, `ctrl_meas`** | Datasheet §4.3.4. Decode `0xF4` as `osrs_t[7:5] \| osrs_p[4:2] \| mode[1:0]`, build the byte by hand, write it |
| 19 | Reading raw data | burst-read `0xF7…0xF9`; assemble a 20-bit value out of three bytes |
| 20 | **Compensation, and the wall** | 12 factory coefficients at `0x88…0x9F`. Implement the *temperature* formula by hand and get real °C. Then look at the *pressure* one |
| 21 | Altitude and the telemetry stream | sea-level reference; why altitude is derived, not measured. Serial Plotter, CSV |
| 22 | **Your sketch is a mess, split it up** | **`.h` / `.cpp` tabs in the Arduino IDE.** Real headers and includes, no PlatformIO |

**Why Module 17 is the right first step.** One register, one documented expected
value, unambiguous pass/fail. If `0x58` comes back, they have talked to a silicon
device on their own terms with no library in between. That is the single biggest
motivational moment available in this whole workshop.

> The same PCB is used for the BME280, whose ID is `0x60`. So this step **also
> tells them which chip they actually own**:  a genuine diagnostic, not a toy
> exercise.

**Why Module 20 works, and why it is not just a wall.** The datasheet's
temperature compensation is four lines and needs three coefficients:

```c
var1  = ((((adc_T>>3) - ((int32_t)dig_T1<<1))) * ((int32_t)dig_T2)) >> 11;
var2  = (((((adc_T>>4) - ((int32_t)dig_T1)) * ((adc_T>>4) - ((int32_t)dig_T1))) >> 12)
        * ((int32_t)dig_T3)) >> 14;
t_fine = var1 + var2;
T = (t_fine * 5 + 128) >> 8;        // hundredths of °C
```

They type that, and raw bytes become a real temperature. **They succeed at the
hard thing once.**

*Then* they look at `bmp280_compensate_P_int64`, nine more coefficients, 64-bit
fixed-point, ten-plus lines of opaque arithmetic. And the lesson lands as an
informed engineering judgement rather than a failure:

> You could finish this. It would take an hour and teach you nothing you didn't
> just learn. **This is what a driver library is**:  and now you know exactly
> what `Adafruit_BMP280` is doing for you, because you did the first half of it
> yourself.

Only at that point does the library get installed. Same shape as Part 4: do it
the hard way until it hurts, then the tool arrives as earned relief instead of
magic.

### Part 4, Where the super loop breaks ← **the point**
| # | Module | What happens |
|---|---|---|
| 23 | Put it all together | sensor + button + servo + status LED, one loop |
| 24 | **Watch it fail** | button presses missed, `delay()` stalls the data, timing jitters, **measured, not asserted** |
| 25 | `millis()` and non-blocking state machines | the first real fix |
| 26 | Interrupts | `attachInterrupt`, `volatile`, what you must never do in an ISR |
| 27 | Why that's *still* not enough → RTOS, and what it looks like on the H753 | tasks, priorities, preemption; bridge to the real flight computer repo |

### Appendices
Troubleshooting index · glossary · **project ideas tied to real CU InSpace work**
(sensor integration, logging, telemetry), the on-ramp from workshop to real tasks.

---

## Running it, facilitation

Full detail and sources in `research/how-to-run-it.md`. The short version:

| Practice | Why |
|---|---|
| **Recruit 1-2 helpers** | Highest-leverage prep item there is. A 9-student workshop found 1 helper per 2 students "really necessary to stay on time" |
| **Live-code each module's opening** | Slows you to the pace of learning, and lets them watch you make and fix mistakes. Type `digitalRite` on purpose |
| **Name tags** | Reported as a surprisingly large effect on interaction |
| **Check the room every ~15 min** | A quick thumbs or one MCQ. Tells *you* whether to move on |
| **10-minute reflection at the end of each part** | Cheap, and the thing most workshops skip |
| **Attendees download the IDE themselves** | Arduino IDE 2 from arduino.cc. Genuine Unos, so no CH340 driver needed |
| **Pre-sort resistors into labelled bags** | Colour bands are genuinely hard to read, a real, quiet time sink |
| **Say out loud that the hardware is hard to break** | Beginners are visibly afraid of damaging equipment that isn't theirs |

---

## Reused from the Tamagotchi deck

Content worth carrying forward rather than rewriting:

| Asset | Change needed |
|---|---|
| **Breadboard anatomy SVG**:  rails, gap, row connectivity | None. Kit-agnostic and genuinely good |
| **PWM diagram SVG**:  annotated wave, duty cycle → brightness | Change `3.3V` to `5V` for the Uno |
| **Tactile button internals SVG**:  4 pins, 2 electrical sides | None |
| **`setup()` / `loop()` explainer** | Light rewrite for Uno |
| Everything else | Leave it, it was Pico- and project-specific |

## Why this arc and not a project build

The Tamagotchi workshop was a single project with a provided library. This one is
a **capability ladder** that happens to end in something real. Two reasons:

- A provided library hides the layer that matters. Here, nothing is hidden , 
  the only library is the vendor's BMP280 driver, which is exactly the boundary
  they'll meet on the real board.
- The end state isn't a toy; it's a small telemetry loop with the same shape as
  the flight computer's job: sample widely, actuate one thing, stream it off.
  Module 21 makes that connection explicit.

---

## Open items

| Item | Status |
|---|---|
| ~~LEDs and resistors in the kits?~~ | **Resolved 12 Sep.** Both present. Resistors are **330 Ω**, and the instructions now say so |
| **10 kΩ resistors for the photoresistor** | **Open.** 330 Ω is the wrong order of magnitude for a photoresistor divider and gives almost no usable swing. A bag of 10 kΩ is a few dollars. See `research/hardware-notes.md` |
| ~~Genuine Unos or CH340 clones?~~ | **Resolved 12 Sep. Genuine Unos.** No CH340 driver needed, and the setup module no longer mentions it |
| Helpers, how many | Highest-leverage prep item. Aim for two |
| Session dates | Needed before the form goes out |
| Where the form gets hosted | TBD |

## Kit, as confirmed

Arduino Uno · breadboard · USB A-B cable · jumper wires · LEDs · 330 Ω resistors ·
potentiometer · push button · photoresistor · diode · NPN transistor · DC motor ·
servo motor · 9V barrel jack · USB power bank

Anyone on a USB-C only laptop needs an A-to-C adapter. Say so in the invite.
