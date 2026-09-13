# What Already Exists, Don't Reinvent

Goal: reuse circuits, sequencing, and diagrams that are already proven and
legally reusable; spend our own effort only on the parts nobody else has
(the CU InSpace framing, the super-loop-breaks arc, and the GY-BMP280 gotchas).

## Reusable with attribution

| Source | License | What to take | What to ignore |
|---|---|---|---|
| [SparkFun Inventor's Kit Guide v4.1](https://learn.sparkfun.com/tutorials/sparkfun-inventors-kit-experiment-guide---v41/all) | **CC BY-SA 4.0**, genuinely reusable, share-alike | Best-in-class **circuit diagrams** and breadboard layouts. Their component set overlaps ours almost exactly: button, pot, photoresistor, servo, DC motor, transistor, diode | Their RedBoard-specific bits; the kit-branded narrative |
| [Adafruit Learn Arduino](https://learn.adafruit.com/series/learn-arduino) | CC BY-SA (text), MIT (code) | **Lesson sequencing.** Their order, Blink → LEDs → Serial → Digital Inputs → PWM fade → Analog Inputs → Sensing Light, is well-tested and matches our kit. Also the canonical BMP280 library docs | Shift-register and LCD lessons (not in our kit) |
| [Arduino Docs + built-in examples](https://docs.arduino.cc/) | CC BY-SA 3.0 | `File → Examples` ships **BlinkWithoutDelay**, **Debounce**, **StateChangeDetection**, **Fading**, **AnalogInput**. These are already on every attendee's machine, zero install, canonical, and free to reference |, |
| [Adafruit BMP388/390 guide](https://learn.adafruit.com/adafruit-bmp388-bmp390-bmp3xx) | CC BY-SA | I2C wiring explanation and library patterns; adapt to BMP280 + `0x76` | Their board is 5V-safe; **ours is not**, see `hardware-notes.md` |

**Attribution plan:** a Credits slide at the end listing the above, plus inline
"adapted from SparkFun SIK, CC BY-SA 4.0" on any diagram we derive. Share-alike
means our workshop page should carry a CC BY-SA 4.0 notice too. That is a
one-line footer, not a burden.

## Deliberately NOT reused

- **Paid courses** (Udemy/Coursera Arduino bootcamps), can't redistribute, and
  they're video-first, which is the opposite of a self-paced written doc.
- **Tinkercad Circuits**, the obvious simulator choice, but its library is
  limited and **I2C sensor support is weak**, so the BMP280 module can't be
  simulated. Dead end for the back half of the workshop.
- **Wokwi**, much better I2C support and simulates a BMP280 fine. Worth keeping
  as a **backup path** for anyone whose laptop won't cooperate, or as pre-work
  before kits are handed out. Not the primary path, since the whole point is
  getting hardware into people's hands.

## The gap nobody else fills

Every beginner Arduino course teaches `delay()` and stops. Almost none of them
deliberately **construct the failure**, build a program where polling visibly
misses events and `delay()` visibly stalls a sensor read, and then use that pain
to motivate interrupts and an RTOS.

That arc is the actual value of this workshop and it is the part we write ourselves.
It is also the part that maps onto CU InSpace's real problem: a flight computer
that must sample sensors, service a radio, and run a control loop concurrently,
where a blocking read is a genuine defect.

Supporting reading for that module (concepts, not copy):
- [Non-blocking delays with millis()](https://mechatronicslab.net/courses/arduino-programming-handbook/lessons/16-2-non-blocking-delays-in-arduino-programming/)
- [Timer interrupts for non-blocking execution](https://techexplorations.com/blog/arduino/timer-interrupts-for-non-blocking-code-execution-the-arduino/)
