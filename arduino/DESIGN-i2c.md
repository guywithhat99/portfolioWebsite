# Part 2 rework: how to introduce I2C

Design proposal. Nothing built yet.

---

## What is wrong with the current draft

1. "What a message looks like" is three bullet points in English. It says a
   message happens without showing one.
2. `0x76` and `0xD0` both appear as hex numbers with no explanation of what kind
   of thing either one is.
3. The bus scanner is the first thing they run. It is a loop over 127 addresses
   and a lot of machinery before they understand a single byte of it.
4. Every code slide is code alone, with the explanation on the slide after it.

---

## Finding from looking at how others do it

The widely used beginner I2C tutorials cover start conditions, ACK bits and
pull-ups reasonably well. **What they consistently skip is the difference
between a device address and a register address.** SparkFun's does not
distinguish them at all.

That is exactly the gap. It is also the cheapest one to fix, and fixing it makes
every later slide readable.

---

## Proposal

### 1. A module on what is inside a chip, before any protocol

The sensor is a small block of numbered bytes. Nothing more exotic than that.

**Diagram: the real BMP280 memory map**, drawn as a column of numbered boxes
from `0x88` to `0xFC`, colour coded by region:

| Region | What lives there |
|---|---|
| `0x88` to `0xA1` | factory calibration numbers |
| `0xD0` | chip id |
| `0xE0` | reset |
| `0xF3` | status |
| `0xF4` | `ctrl_meas`, settings |
| `0xF5` | `config`, settings |
| `0xF7` to `0xF9` | pressure, most recent reading |
| `0xFA` to `0xFC` | temperature, most recent reading |

One picture, and it previews everything they will touch for the rest of Part 2.
Readings are not "fetched from the sensor", they are **sat in a numbered box that
the sensor keeps updating**. That reframing is worth the whole module.

**Then the distinction, stated plainly and drawn:**

- `0x76` says **which chip on the bus**
- `0xD0` says **which box inside that chip**

Two different kinds of number that look identical on the page.

### 2. Then a module on how two wires actually carry that

**Diagram: a real frame, at bit level.** SDA and SCL drawn as two traces, with:

`START` · 7 address bits · `R/W` · `ACK` · 8 data bits · `ACK` · `STOP`

Annotated with the two rules that explain the whole protocol:

- SDA is only allowed to change while SCL is low
- so a change while SCL is **high** is not data, it is a START or a STOP

That is genuinely technical, fits on one slide, and is the thing the current
draft is missing.

**Second diagram:** the same frame with brackets underneath showing which
`Wire` call produced which part. That is the bridge from protocol to code, and
it is where the opacity complaint gets answered.

### 3. Deal with `Wire.h` being opaque by saying so

I looked for a better teaching library. The realistic options:

| Option | Verdict |
|---|---|
| **`Wire.h`** | Standard, already installed, what they will meet in every example and on the flight computer. Keep it |
| Bit-banged I2C libraries | Good for reading, bad for using. You would be teaching someone else's GPIO code, not the protocol |
| Write our own full driver | Start conditions, ACK handling and clock stretching. Half a session, and fragile |

`Wire` is confusing for one specific and fixable reason:

> `beginTransmission()` does not begin a transmission. `write()` does not write
> anything. Both just fill a buffer. `endTransmission()` is the call that
> actually puts everything on the wire.

Say that out loud on a slide. It stops being opaque the moment somebody admits it.

**Then have them write two functions:**

```cpp
byte readRegister(byte reg);
void writeRegister(byte reg, byte value);
```

Short, written once, and after that every sensor interaction reads as what it
means instead of four lines of `Wire` ceremony. They are also the natural first
thing to move into a `.h` and `.cpp` pair in the later module.

### 4. Drop the scanner from first contact

Reading the chip id is the better first test. One register, one documented
answer, and if `0x58` comes back then wiring, address, bus and read are all
proven at once.

The scanner moves to a troubleshooting slide, for when the id read fails.

### 5. Config registers, set up by hand

Unchanged from the plan and worth restating, since it is the point of the
section:

- `ctrl_meas` at `0xF4` is three settings packed into one byte,
  `osrs_t[7:5]`, `osrs_p[4:2]`, `mode[1:0]`
- They read section 4.3.4, decode the bit layout, build the byte themselves, and
  write it with their own `writeRegister`
- A short module on masks and shifts goes immediately before this, not earlier

**Addition:** do `config` at `0xF5` straight afterwards, for the IIR filter and
standby time. Same skill, second repetition, much less guidance. That is where
it actually sticks.

### 6. Code and explanation side by side

All code slides in Part 2 become two columns: code on the left, the explanation
of that code on the right. The layout already exists in the deck.

---

## Things considered and rejected

**Wokwi's logic analyzer.** It captures SDA and SCL, but it does not decode
anything itself. It writes a `.vcd` file that needs PulseView or GTKWave
installed to read. Given how Part 1's setup went, putting a second desktop
install in front of the room is not worth it.

Still worth doing as **your** demo on the projector, set up in advance, if you
want them to see a live capture rather than a drawing.

**Bit-banging a START condition by hand.** Toggling SDA and SCL with
`digitalWrite` to produce one START and one byte is a real option and fits the
"do it the hard way first" shape of the workshop. It is also fiddly, and the
payoff overlaps heavily with just showing an accurate waveform diagram.

Left out of the main line. Could be a stretch goal for whoever finishes early.

---

## Proposed module list for Part 2

| # | Module | New idea |
|---|---|---|
| 10 | Inside a chip | registers, the memory map, the two kinds of address |
| 11 | How two wires carry a message | frames, START, ACK, STOP, at bit level |
| 12 | Wiring the sensor | 3.3 V, the pins, why two go nowhere |
| 13 | Asking the chip who it is | `0xD0`, and writing `readRegister` |
| 14 | Bits, masks and shifts | just in time, immediately before it is needed |
| 15 | Telling the sensor what to do | `ctrl_meas`, then `config`, both by hand |
| 16 | Reading the raw numbers | burst read, 20 bits out of three bytes |
| 17 | Compensation, and the wall | temperature by hand, then the pressure formula |
| 18 | Altitude and the stream | sea level reference, plotting it |

Modules 10 and 11 replace the current single module 10. Modules 12 and 13 are
rewrites of what is already there.

---

## Open questions

1. **How deep on the waveform?** One annotated frame is what I would do. Going
   further, clock stretching, repeated start, arbitration, is real protocol
   detail that nothing in this workshop needs.
2. **Bit-banging as a stretch goal, or leave it out entirely?**
3. **Do you want the Wokwi capture as a projector demo?** If so it needs
   PulseView on your machine only, and about twenty minutes of setup beforehand.
