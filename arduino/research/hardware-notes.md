# Hardware Notes, Kit + Barometer

## GY-BMP280 (6-pin module), READ THIS BEFORE WIRING

From the schematic Jack supplied. This is the **6-pin GY-BMP280 / "GY-BMP280-3.3"**
variant, not the 4-pin one.

### What the schematic actually shows

| Element | Value | Consequence |
|---|---|---|
| `IC2` silkscreen | `BME280/BMP280` | Same PCB is used for both parts. **You do not know which chip you have until you read the chip ID.** BMP280 = `0x58`, BME280 = `0x60` |
| Supply rail | `3.3V` direct to both `VDD` and `VIO` | **No onboard LDO. No level shifter.** This board is 3.3V, full stop |
| `R1` | 10k, `CSB` → 3.3V | CSB idles high → **I2C mode by default**. Leave CSB unconnected |
| `R2`, `R3` | 10k, `SDI`/`SCK` → 3.3V | Bus pull-ups already on board. Do not add your own |
| `R4` | 10k, `SDO` → GND | SDO idles low → **I2C address is `0x76`**, not `0x77` |
| `C1`, `C2` | 1µF, 0.1µF | Decoupling. Nothing to do |

### CON6 pinout

| Pin | Name | Connect to Uno |
|---|---|---|
| 1 | VCC | **3.3V pin**, NOT 5V |
| 2 | GND | GND |
| 3 | SCK / SCL | A5 |
| 4 | SDI / SDA | A4 |
| 5 | CSB | leave unconnected, **R1 pulls it high on the module**, selecting I2C |
| 6 | SDO | leave unconnected, **R4 pulls it low on the module**, selecting `0x76` |

### The two failure modes that will eat a whole session if unaddressed

**1. Address is 0x76, and most tutorials say 0x77.**
`R4` pulls SDO low, which selects the low address. Every copy-pasted
`bmp.begin()` (which defaults to `0x77` in Adafruit_BMP280) fails with
"Could not find a valid BMP280 sensor". Must be `bmp.begin(0x76)`.
This is the single most likely thing to go wrong.

**2. The Uno is a 5V part and this board is not 5V tolerant.**
`VIO` is tied to the 3.3V rail. Bosch's absolute max on `VDDIO` is 4.3V.

The fix is cheap and is itself a good lesson:

- Power `VCC` from the Uno's **3.3V** pin. The BMP280 draws microamps; the
  Uno's 3.3V rail (~50 mA budget) is far more than enough.
- I2C is **open-drain**: the master only ever pulls the line LOW. It never
  drives HIGH. The line is pulled high by resistors, and `R2`/`R3` on this
  board already pull to 3.3V.
- But `Wire.begin()` on AVR **enables the ATmega328P's internal pull-ups to 5V**,
  which fights R2/R3 and puts ~3.7V plus ESD-diode current into the sensor.
  Disable them immediately after:

```cpp
Wire.begin();
digitalWrite(SDA, LOW);   // on AVR, LOW on an input pin = pull-up OFF
digitalWrite(SCL, LOW);
```

  With the internal pull-ups off, the bus idles at 3.3V and never exceeds it.

- The Uno reads 3.3V as logic HIGH: `VIH` is `0.6 × Vcc` = 3.0V, and 3.3V clears
  it, but only by 300 mV. **Say this out loud in the workshop.** It works, it is
  marginal by design, and "this is why real boards use a level shifter" is a
  one-sentence lesson that lands directly on the avionics work.

> ⚠ **Do not describe CSB/SDO as "floating."** The datasheet is explicit: *"The
> SDO pin cannot be left floating; if left floating, the I²C address will be
> undefined."* On this module they are not floating, R1 and R4 define them.
> Leaving them unconnected is correct *because of those resistors*, and that
> distinction is worth saying out loud, since on a bare chip it would be a bug.

---

## Register map, verified against the datasheet

Extracted from [BMP280 datasheet rev 1.26, Table 18](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf).
These are the registers the workshop actually uses.

| Register | Address | Contents | Reset |
|---|---|---|---|
| `id` | `0xD0` | `chip_id[7:0]`, **`0x58`** for BMP280 (`0x60` = BME280) | `0x58` |
| `reset` | `0xE0` | write `0xB6` for a soft reset | `0x00` |
| `status` | `0xF3` | `measuring[3]`, `im_update[0]` | `0x00` |
| `ctrl_meas` | `0xF4` | `osrs_t[7:5]` · `osrs_p[4:2]` · `mode[1:0]` | `0x00` |
| `config` | `0xF5` | `t_sb[7:5]` · `filter[4:2]` · `spi3w_en[0]` | `0x00` |
| `press` | `0xF7…0xF9` | msb, lsb, xlsb`[7:4]` → 20-bit value | `0x80,0,0` |
| `temp` | `0xFA…0xFC` | msb, lsb, xlsb`[7:4]` → 20-bit value | `0x80,0,0` |
| calibration | `0x88…0xA1` | `dig_T1…T3`, `dig_P1…P9` | per-part |

**`mode[1:0]`:** `00` sleep · `01`/`10` forced · `11` normal.
**`osrs_x[2:0]`:** `000` skip · `001` ×1 · `010` ×2 · `011` ×4 · `100` ×8 · `101+` ×16.

So a sensible starting value for `ctrl_meas` is temperature ×1, pressure ×1,
normal mode → `001 001 11` = **`0x27`**. Deriving that byte from the datasheet is
exactly the Module 18 exercise.

> **Register types matter and catch people out:** calibration and data registers
> are **read-only**, `reset` is **write-only**, and reserved registers must not be
> written at all.

### Library

`Adafruit_BMP280` (pulls in `Adafruit_Unified_Sensor` + `Adafruit_BusIO`).
Available in Arduino IDE Library Manager, so no manual install.

### Free bonus

CON6 exposes CSB and SDO, so the same board runs **SPI** as well as I2C. If there
is ever a "why are there two buses" module, it can be demonstrated on hardware
already in hand rather than in the abstract.

---

## Kit contents (confirmed 12 Sep 2026)

Arduino Uno · breadboard · USB A-B cable · jumper wires · **LEDs** ·
**330 Ω resistors** · potentiometer · push button · photoresistor · diode ·
NPN transistor · DC motor · servo motor · 9V barrel jack · USB power bank

The earlier worry about missing LEDs and resistors is resolved. Both are in the
kit. Every module through PWM is buildable as written.

> **USB-C only laptops need an A-to-C adapter.** Worth saying in the invite, not
> discovering in the room.

### One real problem: the photoresistor

The kit has **330 Ω** resistors and nothing larger. That is a good value for an
LED and a poor one for a photoresistor.

A photoresistor works as one half of a **voltage divider**, and the fixed half
should be roughly the geometric mean of the light and dark resistances. A typical
photoresistor runs about 1 kΩ in bright light and 10 kΩ or more in the dark, so
the fixed resistor wants to be around **10 kΩ**.

With 330 Ω instead, almost the whole supply is dropped across the photoresistor
and `analogRead` sees a tiny swing near the top of its range. It technically
responds to light, but the reading barely moves, which is a bad first experience
of an analog sensor.

**Three ways out, in order of preference:**

| Option | Cost | Notes |
|---|---|---|
| **Buy 10 kΩ resistors** | A few dollars for a bag of 100 | Cleanest. One small order fixes the module permanently |
| **Use the potentiometer as the fixed leg** | Free | Wire the pot as a variable resistor in the divider and tune it until the reading swings well. Genuinely instructive, since it shows *why* the value matters, but fiddly with a room of beginners |
| **Drop the photoresistor, use the potentiometer** | Free | The potentiometer already teaches `analogRead` perfectly. The photoresistor adds the divider concept, which could move to a later module |

**Recommendation:** buy the 10 kΩ resistors. The divider is a genuinely useful
concept for the sensor work later, and it is the cheapest fix on this list.

### Notes on the other parts

**The button needs no resistor.** `pinMode(pin, INPUT_PULLUP)` uses the chip's
internal pull-up. Worth teaching explicitly, because the same pull-up idea
returns on the I2C bus in Part 3.

**The diode, transistor and DC motor are one set.** That is the low-side
transistor motor driver with a flyback diode across the motor. The "diode" is
almost certainly a 1N4001-class rectifier for flyback duty, not an LED.

