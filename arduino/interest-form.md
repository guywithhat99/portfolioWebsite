# Arduino Workshop, Interest & Signup Form (draft)

Platform-agnostic. Paste into Google Forms, Microsoft Forms, or a page on the site.
**Target completion time: 2-3 minutes.** Anything longer and response rate drops.

Questions marked ⚑ are the ones that actually change how the workshop is run , 
if you need to cut for length, cut everything else first.

---

## Intro blurb (top of form)

> **Intro to Microcontrollers, CU InSpace Avionics**
>
> A hands-on workshop that takes you from "I have never written code" to reading a
> real pressure sensor and streaming data off a microcontroller, the same job the
> flight computer does on the rocket.
>
> **No experience needed.** Genuinely none. Kits are provided.
>
> This form is mostly so we know how many kits to bring and where to pitch the
> material. Takes about two minutes.

---

## Section 1, Who you are

1. **Name** *(short text, required)*
2. **Email** *(short text, required)*, use the one you actually check
3. **Program and year** *(short text)*
4. **Are you currently on CU InSpace?** *(single choice)*
   - Yes, on the avionics/electronics team
   - Yes, on another subteam
   - No, interested in joining
   - No, just here for the workshop

---

## Section 2, Experience ⚑

> *Form text: There are no wrong answers here and nobody sees this but the
> organiser. It exists so the workshop isn't too fast or too slow. "None" is a
> completely normal answer and the workshop is built for it.*

5. ⚑ **How much programming have you done?** *(single choice)*
   - None at all
   - A little, an intro course, or followed a tutorial once
   - I can write a small program on my own
   - I'm comfortable programming
6. **Which of these have you written any code in?** *(checkboxes, "none" allowed)*
   - None · Python · C · C++ · Java · MATLAB · JavaScript · Other
7. ⚑ **Have you used a microcontroller before?** *(single choice)*
   - Never heard of one before this form
   - Heard of Arduino, never used one
   - Used an Arduino once or twice
   - Used Arduino / ESP32 / STM32 on a real project
8. **Have you built a circuit on a breadboard?** *(single choice)*
   - Never · Once or twice · I'm comfortable
9. ⚑ **Tick anything you've heard of, even if you couldn't explain it.**
   *(checkboxes, this is the single most useful question on the form)*
   - Variable, loop, function
   - Compiling code
   - Resistor / Ohm's law
   - Breadboard power rails
   - Digital vs analog signal
   - PWM
   - I2C or SPI
   - Interrupt
   - RTOS / task scheduling
   - Soldering
   - Multimeter or oscilloscope
   - Git / GitHub
   - *None of these* ← include this option explicitly so it's not an empty row

---

## Section 3, Logistics ⚑

> *These are boring but they are the difference between starting on time and
> spending the first hour on installers.*

10. ⚑ **Will you bring a laptop?** *(single choice)*
    - Yes
    - No, I'd need to borrow one
    - I have one but it's unreliable
11. ⚑ **What OS?** *(single choice)*, Windows · macOS · Linux · Chromebook · Not sure
    > **Why this matters:** a Chromebook cannot run the Arduino IDE normally.
    > If anyone picks Chromebook you need to know *before* the session, that
    > person goes on the browser-based path or borrows a machine.
12. ⚑ **Can you install software on it yourself (admin rights)?**
    - Yes · No · Not sure
    > **Why this matters:** this was the failure mode last time. A locked-down
    > machine can't install the IDE or USB drivers, and you find out at minute five.
13. **Which sessions can you make?** *(checkboxes, fill in real dates)*
    - Session 1, `[date/time]`
    - Session 2, `[date/time]`
    - Neither of those, but I'm interested if it runs again

---

## Section 4, Interest

14. **What sounds most interesting?** *(checkboxes, pick any)*
    - Sensors and data collection
    - Radio / telemetry / getting data off the rocket
    - PCB design
    - Control systems (airbrakes, GNC)
    - Ground station and software
    - Power systems and batteries
    - Testing and validation
    - Not sure yet, show me the options
15. **Anything specific you're hoping to get out of this?** *(long text, optional)*
16. **Any accessibility needs or anything we should know?** *(long text, optional)*

---

## Notes on running it

- **Turn on "collect email" / one response per person** so the responses double as
  a headcount you can trust.
- **Q9 is your pacing instrument.** If most people tick 0-2 boxes, Module 0 needs
  its full length. If most tick 6+, you can compress the front half and spend the
  saved time on interrupts.
- **Q11 + Q12 are your setup risk register.** Any "Chromebook", "No", or "Not sure"
  is a person to contact individually before the session. Fixing three laptops by
  email beforehand is far cheaper than fixing them in the room.
- **Close the form ~3 days before** so there's time to act on the answers and
  count kits.
