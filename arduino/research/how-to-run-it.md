# How to Actually Run This, Evidence from People Who've Done It

Not curriculum. This is about facilitation: what makes hands-on hardware
workshops succeed or fail, from workshop retrospectives, CS-education research,
and The Carpentries' instructor training.

---

## 1. Findings from real workshop retrospectives

### Bonnie Eisenman, [Lessons Learned from Teaching an Arduino Workshop](https://medium.com/@brindelle/lessons-learned-from-teaching-an-arduino-workshop-f8d1282e0985)
*9 students, 2 instructors, 3 hours, almost exactly our shape.*

| Finding | What we do about it |
|---|---|
| **"Follow the book" produced silences.** Pointing people at written material without engaging them felt like the *opposite* of a guided workshop | The doc is the **safety net, not the lesson**. Each module opens live, out loud. People go self-paced *after* the idea has been introduced by a human |
| **No name tags hurt interaction badly**, an oddly large effect for such a small thing | Name tags. Costs nothing |
| **1 helper per 2 students was "really necessary to stay on time"** | For 6-10 people, recruit **at least one helper**, ideally two. This is the single highest-leverage prep item |
| **3 hours was tight; the transistor project didn't finish** | Confirms the motor/transistor module is the heaviest in Part 2. Budget accordingly |
| Focus on **why**, not just how, what an Arduino is *for* | Every module leads with the idea before the wiring |
| Pre-made kits with everything in one package worked well | Ours are pre-made. **Pre-sort and label them** anyway, see §4 |

### Murray Varey, [Lessons Learned After An Hour of Arduino](https://www.murrayvarey.com/lessons-learned-after-an-hour-of-arduino/)
*Written from the **beginner's** side, which is rarer and more useful.*

- **Resistor colour bands are genuinely hard to read.** He describes it as "spot the
  difference", brown and purple on beige. This is a real time sink and a real
  source of quiet frustration. → **Pre-sort resistors into labelled bags.**
- **Physical intimidation is real.** Small components, fear of breaking equipment
  that isn't yours. → Say out loud, early: *this hardware is hard to damage,
  it's cheap, and breaking one is fine.*
- **The breakthrough was learning *why*:** "this LED needs a 220Ω resistor,
  otherwise it takes in too much energy and burns out." Suddenly resistors made
  sense instead of being arbitrary. → Never introduce a component without its
  reason.
- **A basic LED circuit took about an hour** for a true beginner. Calibrate
  expectations to that, not to how long it takes us.

### [DanSpicyTaco university Arduino workshop](https://github.com/DanSpicyTaco/arduino_workshop)
Per-module rhythm that they found worked:
**10-15 min presentation → 20-30 min follow-along → 10 min reflection.**
Numbered sketch files handed out, with solutions kept separate.
3-4 volunteers for 30 students.

> The **10 min reflection** is the part most workshops skip and it's cheap. Adopted.

---

## 2. What CS-education research says about hardware debugging

This is the most important section, and it changes the plan.

**Source:** [Failure Artifact Scenarios (arXiv 2311.17212)](https://arxiv.org/html/2311.17212) ·
[Toward a debugging pedagogy](https://www.emerald.com/ils/article-abstract/124/1-2/1/170008/Toward-a-debugging-pedagogy-helping-students-learn) ·
[Scaffolding debugging with Circuit Check](https://par.nsf.gov/servlets/purl/10386912)

### Finding 1, Novices are *domain blind*
> Before instruction, **only 44% of students examined both the circuit and the
> code.** Most fixated on one domain and never looked at the other. After
> explicit instruction, **72%** did.

This is *the* defining difficulty of physical computing. A beginner whose LED
doesn't light will read their code twenty times and never touch the wire, or
reseat the wire twenty times and never read the code.

**→ Action: teach an explicit bisection method as its own module, early.**
"Is it the code or the circuit?" with a repeatable procedure for deciding.
This is not a troubleshooting appendix; it is a skill with its own lesson.

### Finding 2, Novices generate only one hypothesis
> Only **12%** initially recognised that one failure could have multiple causes;
> **50%** did after instruction.

**→ Action:** every troubleshooting section lists **multiple** plausible causes,
never one. Model the habit of "here are three things this could be."

### Finding 3, "Failure artifact scenarios" work
Handing students a **deliberately broken** project and asking them to diagnose it
measurably improves troubleshooting, and costs less time than free debugging.

**→ Action: seed deliberately broken sketches through the workshop.** A "Find the
bug" step with a known-wrong sketch, wrong pin, missing `pinMode`, `==` vs `=`,
baud mismatch, floating input. High learning per minute, and it's *fun* in a way
that copying working code is not.

### Finding 4, Frustration from debugging is where people quit
> "If the challenge of debugging becomes too great, frustration can lead to
> quitting."

**→ Action:** collapsible hints *before* collapsible answers, and a hard rule for
helpers, nobody sits stuck and silent for more than a few minutes. This is what
the red/green flags in §3 are for.

### Finding 5, Working prototypes ≠ understanding
Research on LilyPad/Circuit Playground notes students can build working things
**without grasping the underlying principles**. This is exactly the trap the
Tamagotchi workshop's provided library fell into.

**→ Action:** already handled, the only library is the vendor BMP280 driver.

---

## 3. The Carpentries, the best-documented practice for hands-on technical teaching

**Source:** [Live Coding is a Skill](https://carpentries.github.io/instructor-training/17-live) ·
[Key Points](https://carpentries.github.io/instructor-training/key-points.html)

### Live coding, type it in front of them, don't present finished slides
Their core practice, and the evidence behind it is strong:

- It **forces the instructor down to the pace of learning**
- It keeps examples small enough for working memory
- **Learners see mistakes being made and recovered from.** This is the part that
  matters most here, beginners think errors mean they're failing. Watching you
  hit a compiler error, read it, and fix it teaches more than any slide about
  debugging.

> **Deliberately make a mistake or two and fix them out loud.** Type `digitalRite`.
> Forget a semicolon. This is a teaching technique, not an accident.

### Sticky notes as status flags  
> **REJECTED for this workshop.** Jack does not want them. Kept here only as a record of what the source material recommended.
Every learner gets two sticky notes on their laptop lid:
**red = I'm stuck**, **green = I'm done**.

- No hand-raising, no waiting passively, no one too shy to ask
- You read the whole room's state in one glance from anywhere
- A field of green = move on. Three reds = stop and address it collectively

Cheap, and repeatedly reported as one of the highest-impact practices they have.
**Directly solves the self-paced problem of knowing when to move on.**

### Formative assessment every ~15 minutes
A quick multiple-choice or thumbs check. Not graded, it exists to tell *you*
whether to move on, and to tell *them* whether they actually understood.

### Faded examples
Scaffolding that is progressively removed: full worked example → same thing with
blanks → blank page. This is precisely the structure Jack described wanting
("now that you know `digitalWrite` and `delay`, make it blink 1s on 1s off"),
and it has a literature behind it. Good instinct; keep it.

---

## 4. Practical logistics that will otherwise eat the session

Now that setup happens **in the room**, these stop being nice-to-haves.

| Risk | Mitigation |
|---|---|
| **10 people downloading the Arduino IDE on campus wifi at once**, ~300 MB each. This alone can cost 30+ minutes | **Put offline installers on 2-3 USB sticks** (Windows + macOS) and pass them around. Also stage the **Adafruit BMP280 + Unified Sensor + BusIO** libraries as `.zip` for offline install |
| **CH340 clone boards need a driver**; genuine ones don't | Check one kit *now*. If clone, put the CH340 driver on the same USB sticks |
| **Power-only USB cables** silently fail to enumerate | Have 2 known-good spare A-B cables. Test the kit cables beforehand if possible |
| **Wrong COM port / board selection**, the #1 first-session failure | Screenshot of the exact Tools menu state in the doc. Both OSes |
| **Baud mismatch → garbled serial.** Beginners read gibberish as "broken" | Standardise on **9600** everywhere and say why. Show the garbled output deliberately so they recognise it |
| **Resistor bands unreadable** | Pre-sort into labelled bags per value |
| **Locked-down laptops (no admin rights)** | Ask on the signup form. Fix beforehand or pair them with someone who can install |
| **Someone's laptop just dies** | Have one loaner ready, or plan pairs |

**Room setup:** name tags · sticky notes at every seat · power strips (laptops
*and* boards) · the workshop URL written large somewhere visible.

---

## 5. What this changes in the plan

1. **Add Module 2, "Is it the code or the circuit?"** A dedicated debugging
   module, early, teaching bisection. Evidence-driven, and currently missing.
2. **Seed "find the bug" broken sketches** through every part.
3. **Every troubleshooting box lists multiple causes,** never one.
4. **Setup becomes Module 1, in-room**, with offline installers as the mitigation
   for its biggest risk.
5. **Recruit one or two helpers.** Highest-leverage prep item there is.
6. **Walk the room continuously.** Do not wait to be asked for help.
7. **Live-code each module's opening** rather than pointing at the doc.
8. **10-minute reflection** at the end of each part.
