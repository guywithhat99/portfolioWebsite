# IoT Sensor Dashboard Design

Date: 2026-08-27
Status: approved for planning
Scope: cloud + web side of the ECEN capstone IoT sensor node workshop

## Goal

A Seeed XIAO ESP32C6 sensor node on the ECEE lab bench posts environmental readings
every 10 minutes. Anyone scanning a QR code at the bench lands on
`https://guywithhat.me/sensors` and sees the last 24 hours graphed, properly
labeled, with units. Runs unattended for the rest of the school year.

## Requirements traceability

Mapped from the workshop handout (section 28.3.1):

| Req | Requirement | Where satisfied |
|-----|-------------|-----------------|
| 1a-f | Six metrics: temp F, RH%, altitude ft, rail volts, particle count, CO2 ppm | ThingSpeak fields 1-6 |
| 2 | Sample fast, average over 10 min, one point per metric per window | ESP32 firmware, aggregation before post |
| 3 | Graph 144 points (24h), labeled axes and units, time on x | `/sensors` page |
| 4 | Available via URL and printed QR code | `guywithhat.me/sensors` |
| 5 | Free cloud account permitted | ThingSpeak |
| 6 | ESP32 pushes to cloud | HTTP GET to `api.thingspeak.com/update` |
| 7 | CapstoneWifi only | firmware credentials |
| 28.8 | Report table of sample rate and samples per point | measured on bench, static table |

## Repositories

Two, deliberately separate:

- `~/Documents/Projects/portfolioWebsite` : the `/sensors` page. Cloudflare
  Pages, push to main deploys.
- `~/Desktop/ECEN 4610 - Capstone 1/IOT Sensor` : firmware. PlatformIO,
  `seeed_xiao_esp32c6` on the pioarduino fork. Already scaffolded with a
  file split by owner (`sensors.cpp`, `net.cpp`, `main.cpp`).

The ThingSpeak channel is the only contract between them: six field slots and a
10 minute cadence. Neither repo imports anything from the other.

## Hardware as built

Deviates from the handout, which mandates the ESP32 QT Py. Actual bench build:

| Part | Bus | Addr | Provides |
|---|---|---|---|
| Seeed XIAO ESP32C6 | - | - | MCU, wifi |
| BME688 | I2C | 0x77 | temp, RH, pressure, gas |
| SCD30 | I2C | 0x61 | CO2 ppm |
| PMSA003I | I2C | 0x12 | particle count / 0.1 L |
| resistor divider | ADC1 | - | rail voltage |

Consequences that matter for this design: temperature, humidity and pressure all
come from one chip, so three of the six metrics share a single failure mode. The
BME688's gas channel is free once that read is happening, which is why field7 is
spoken for. The C6 has no ADC2, so the divider must land on A0, A1 or A2.

The I2C bus runs at 100 kHz because the SCD30 caps there and clock-stretches for
up to 150 ms. That stretch is the binding constraint on the sample loop.

## Architecture

Three parts, deliberately decoupled:

```
ESP32 on CapstoneWifi
   |  HTTP GET /update?api_key=...&field1=..&field6=..    every 600 s
   v
ThingSpeak channel            <- storage. not ours, not maintained by us.
   |  HTTPS GET /channels/<id>/feeds.json?results=144
   v
guywithhat.me/sensors         <- static page in portfolioWebsite, our styling
```

The key decision is using ThingSpeak as a **database only**, not as the
dashboard. Their charts stay unused. We own the URL, the styling, and the
presentation; they own uptime, storage, and ingest.

### Why not a self-hosted backend

Considered and rejected: Cloudflare Pages Functions + D1, and a Raspberry Pi
collector. Both were rejected for the same reason. This system has a nine month
unattended uptime requirement and no on-call. A third party with a decade of
operational history is the correct dependency here. The Pi was additionally
impossible once the node landed on CapstoneWifi, since `10.0.0.185` is an
RFC1918 address with no route from campus.

The migration path is preserved: swapping storage later touches exactly two
places, the ESP32 post function and the fetch call in `sensors.js`.

## Component: ThingSpeak channel

One public channel. Field assignment is fixed and must match the firmware:

| Field | Metric | Unit | Notes |
|-------|--------|------|-------|
| field1 | temperature | degF | |
| field2 | humidity | %RH | |
| field3 | altitude | ft | derived from BME688 pressure, sea-level ref assumed |
| field4 | rail voltage | V | 2:1 divider into ADC1 (A0/A1/A2 only on C6) |
| field5 | particle count | count / 0.1 L | 0.3 to 2.5 um range |
| field6 | CO2 | ppm | |
| field7 | gas resistance | ohm | BME688 VOC proxy, free with the temp/RH read |
| field8 | reserved | | stretch sensors |

Channel set to **public** so the browser reads it with no API key. The write key
lives only in firmware and is never shipped to the page.

Constraint: 8 fields per channel is a hard cap. Adding min/max bands per metric
would need a second channel (free tier allows 4).

## Component: /sensors page

New directory in `portfolioWebsite`, deployed by the existing Cloudflare Pages
push-to-main flow. No build step, matching the rest of the site.

```
sensors/
  index.html
  sensors.js
  sensors.css
  vendor/chart.umd.min.js
```

Chart.js is vendored locally rather than pulled from a CDN. The rest of the site
has zero external dependencies and this keeps that property, and it means the
page cannot break because someone else's CDN changed.

Six stacked line charts, one per metric, each with a labeled y-axis carrying its
unit and a shared time x-axis. Styling reuses the existing CSS custom properties
in `styles.css` so the page reads as part of the site.

Above the charts: a status line showing the newest reading's age.

## Data flow

1. ESP32 samples each sensor as fast as it practically can for 600 s, keeping a
   running mean and a sample count per metric.
2. At the window boundary it issues one HTTP GET to `api.thingspeak.com/update`
   with all six fields, then resets the accumulators.
3. Browser loads `/sensors`, fetches
   `https://api.thingspeak.com/channels/<id>/feeds.json?results=144`, and renders.

144 results is exactly 24 hours at a 10 minute cadence.

## Error handling

**ESP32 side.** Wifi reconnect with backoff, non-blocking. Task watchdog
enabled. After repeated consecutive post failures, `ESP.restart()`. A dropped
window is an acceptable gap in the graph; correctness of the running system
matters more than completeness of the series.

**Page side.** Three states, all explicit:
- Fetch fails or returns non-200: render an error message, not an empty chart.
- Feed is empty: "no data yet" rather than blank axes.
- Newest point older than 25 minutes: a visible stale banner with the actual
  age. For a device that must run nine months unattended, silent staleness is
  the worst failure mode, because the page looks fine while the data is dead.

## Testing

**Page, without hardware.** Post synthetic points to the channel with `curl` and
confirm each chart renders, axes label correctly, and the stale banner appears
when posting stops. This decouples web work from the bench entirely.

**Sensor validation.** Cross-check temperature and RH against a second
instrument. CO2 sanity check: outdoor air reads near 420 ppm, an occupied room
climbs well above it and falls when the room empties. That diurnal shape is
better evidence the sensor works than a single spot reading.

**Rail voltage.** Compare the reported value against a DMM on the same rail.
Use `analogReadMilliVolts()`, not `analogRead()`. It applies the per-chip
factory calibration from the eFuse; the raw ADC is badly nonlinear near both
ends of its range.

**Sample rate table (deliverable 28.8).** Bracket each sensor read with
`micros()` on the bench, record the fastest achievable rate per sensor, and
compute samples-per-point as window duration divided by cycle time. This is a
one-time measurement for the report, not a runtime metric.

## Verified assumptions

Checked empirically on 2026-08-27 rather than taken from documentation:

- **Plain HTTP works** against `api.thingspeak.com`. Returns 200 with valid
  JSON. This matters because it lets the firmware skip `WiFiClientSecure`
  entirely, which is the largest heap consumer in a project like this.
- **CORS is open** on the read API: `access-control-allow-origin: *`. The
  browser can fetch directly with no proxy.
- **Retention is effectively indefinite.** Channel 9, created 2010-12-14, still
  returns its full 2012 data when queried by date range in 2026. Adafruit IO's
  ~30 day free retention would have violated requirement 6 silently, months in.
- **`results` caps at 8000** per request. Irrelevant at 144, relevant if the
  page later offers a multi-week view.

## Out of scope

- Alerting on sensor failure.
- Views longer than 24 hours. The requirement is 24h; a range selector is a
  later addition and the API supports it via `start`/`end`.
- Sensor driver bring-up beyond what the upload path needs. Owned by teammates
  per the split in the firmware README.

## Open items

- Confirm `bulk_update.json` accepts timestamped backfill arrays before relying
  on it for outage recovery. Not needed for MVP, since a dropped window is an
  acceptable gap.
- Channel ID and write key are created at setup time.
