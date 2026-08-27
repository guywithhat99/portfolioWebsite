# IoT Sensor Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A XIAO ESP32C6 on the lab bench posts a 10 minute average of six environmental metrics to ThingSpeak, and `https://guywithhat.me/sensors` graphs the last 24 hours in the site's own styling.

**Architecture:** ThingSpeak is used as a database only, never as a dashboard. Firmware does an unauthenticated-read/keyed-write HTTP GET to `api.thingspeak.com/update` every 600 s. The static `/sensors` page fetches the channel's public JSON feed directly from the browser. The two repos share exactly one contract: the field number to metric mapping.

**Tech Stack:** PlatformIO + Arduino (pioarduino fork) on `seeed_xiao_esp32c6`; Unity for host-side firmware tests; vanilla ES modules + Chart.js (vendored) on Cloudflare Pages; Node's built-in `node --test`.

**Spec:** `docs/superpowers/specs/2026-08-27-iot-sensor-dashboard-design.md`

## Global Constraints

- **Two repos.** Web: `~/Documents/Projects/portfolioWebsite`. Firmware: `~/Desktop/ECEN 4610 - Capstone 1/IOT Sensor`. Never import across them.
- **Commit style is per-repo.** `portfolioWebsite` uses conventional prefixes (`feat:`, `chore:`). The firmware repo uses plain lowercase imperative (`add platformio scaffold for xiao esp32c6`). Match the repo you are in. Never add a `Co-Authored-By` trailer.
- **No em dashes** in any prose, comment, or commit message.
- **Never push.** Commit locally only. Jack pushes.
- **`pio` is not on PATH.** Every firmware command must be preceded by `export PATH="$HOME/.platformio/penv/bin:$PATH"`.
- **Do not "fix" the `platform =` URL** in `platformio.ini` back to `espressif32`. The pioarduino fork is required for ESP32-C6 Arduino support.
- **`include/secrets.h` is gitignored and must stay that way.** Never commit a real API key. Never print `TS_WRITE_KEY` to stdout.
- **I2C stays at 100 kHz.** The SCD30 caps there and clock-stretches up to 150 ms.
- **Plain HTTP to ThingSpeak, not HTTPS.** Verified working. Using `WiFiClientSecure` wastes heap for no benefit here.
- **ADC1 only.** The C6 has no ADC2. The rail divider lands on A0, A1 or A2.

### Field contract (locked, both repos depend on this)

| Field | Metric | Unit | Source |
|-------|--------|------|--------|
| field1 | temperature | degF | BME688 @0x77 |
| field2 | humidity | %RH | BME688 |
| field3 | altitude | ft | BME688 pressure, 1013.25 hPa ref |
| field4 | rail voltage | V | 2:1 divider into ADC1 |
| field5 | particle count | count / 0.1 L | PMSA003I @0x12 |
| field6 | CO2 | ppm | SCD30 @0x61 |
| field7 | gas resistance | ohm | BME688 |

---

### Task 1: Provision the ThingSpeak channel and verify the contract end to end

No code. This unblocks every other task, because both repos hardcode the field numbers and the web page needs a real channel ID.

**Files:**
- Modify: `~/Desktop/ECEN 4610 - Capstone 1/IOT Sensor/include/secrets.h` (gitignored, not committed)
- Modify: `~/Desktop/ECEN 4610 - Capstone 1/IOT Sensor/README.md`

- [ ] **Step 1: Create the channel**

At https://thingspeak.com, sign in with a MathWorks account, then Channels > My Channels > New Channel.

Name: `guywithhat IoT sensor node`. Enable fields 1 through 7 and name each one exactly as the field contract table above specifies. Save.

- [ ] **Step 2: Make the channel public**

Channel Settings > check **Make Public**. Save.

This is required. The browser reads the feed with no API key, so a private channel would force the read key into client-side JavaScript where anyone can take it.

- [ ] **Step 3: Record the credentials**

From the **API Keys** tab, copy the Channel ID and the Write API Key into `include/secrets.h`:

```c
#define TS_CHANNEL_ID 1234567
#define TS_WRITE_KEY  "YOURWRITEKEYHERE"
```

Confirm `git status` in the firmware repo does **not** list `include/secrets.h`. If it does, stop and fix `.gitignore` before continuing.

- [ ] **Step 4: Smoke test the write path with curl**

Substitute your real write key. This proves the channel accepts the exact request shape the firmware will send.

```bash
curl -sS "http://api.thingspeak.com/update?api_key=YOURWRITEKEY&field1=72.5&field2=41.2&field3=5280&field4=5.02&field5=120&field6=680&field7=98000"
```

Expected: a single integer greater than `0` (the new entry ID). A response of `0` means the write was rejected, usually a bad key or posting faster than the 15 s minimum interval.

- [ ] **Step 5: Smoke test the read path**

Substitute your real channel ID.

```bash
curl -sS "https://api.thingspeak.com/channels/YOURCHANNELID/feeds.json?results=2"
```

Expected: JSON containing a `feeds` array whose newest entry has `field1` of `"72.5"`. Note that ThingSpeak returns every field as a **string**, not a number. The web code must parse them.

- [ ] **Step 6: Record the channel ID in the firmware README**

The channel ID is not a secret, only the write key is. Replace the `Who's doing what` table's empty dashboard row and add a line under it:

```markdown
ThingSpeak channel: <YOUR_ID> (public)
Dashboard: https://guywithhat.me/sensors
```

- [ ] **Step 7: Commit**

```bash
cd "$HOME/Desktop/ECEN 4610 - Capstone 1/IOT Sensor"
git add README.md
git commit -m "record thingspeak channel id and dashboard url"
```

---

### Task 2: Web, pure feed-parsing module with host tests

Build the logic that has no DOM in it first, so it can be tested without a browser or a running sensor.

**Files:**
- Create: `sensors/lib.js`
- Test: `tests/sensors.test.mjs`

**Interfaces:**
- Produces: `METRICS` (array of `{field, key, label, unit}`), `parseFeed(json) -> {points: Array<{t: Date, values: Object<string, number|null>}>, channel: object}`, `isStale(newest, now, maxAgeMs) -> boolean`, `seriesFor(points, key) -> Array<{x: Date, y: number|null}>`

- [ ] **Step 1: Write the failing test**

Create `tests/sensors.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { METRICS, parseFeed, isStale, seriesFor } from '../sensors/lib.js';

const sample = {
  channel: { id: 123, name: 'test' },
  feeds: [
    { created_at: '2026-08-27T10:00:00Z', entry_id: 1,
      field1: '72.5', field2: '41.2', field3: '5280', field4: '5.02',
      field5: '120', field6: '680', field7: '98000' },
    { created_at: '2026-08-27T10:10:00Z', entry_id: 2,
      field1: '73.0', field2: null, field3: '5281', field4: '5.01',
      field5: '118', field6: '690', field7: '97000' }
  ]
};

test('METRICS covers all seven contract fields in order', () => {
  assert.equal(METRICS.length, 7);
  assert.deepEqual(METRICS.map(m => m.field), [1, 2, 3, 4, 5, 6, 7]);
  assert.equal(METRICS[0].key, 'temp_f');
  assert.equal(METRICS[0].unit, 'degF');
});

test('parseFeed converts ThingSpeak strings to numbers', () => {
  const { points } = parseFeed(sample);
  assert.equal(points.length, 2);
  assert.equal(points[0].values.temp_f, 72.5);
  assert.equal(typeof points[0].values.temp_f, 'number');
});

test('parseFeed maps a null field to null, not NaN or zero', () => {
  const { points } = parseFeed(sample);
  assert.equal(points[1].values.humidity, null);
});

test('parseFeed produces Date objects in chronological order', () => {
  const { points } = parseFeed(sample);
  assert.ok(points[0].t instanceof Date);
  assert.ok(points[0].t < points[1].t);
});

test('parseFeed tolerates an empty feed', () => {
  const { points } = parseFeed({ channel: {}, feeds: [] });
  assert.deepEqual(points, []);
});

test('isStale is false for a fresh point and true past the threshold', () => {
  const now = new Date('2026-08-27T10:20:00Z');
  assert.equal(isStale(new Date('2026-08-27T10:12:00Z'), now, 25 * 60000), false);
  assert.equal(isStale(new Date('2026-08-27T09:40:00Z'), now, 25 * 60000), true);
});

test('isStale treats a missing newest point as stale', () => {
  assert.equal(isStale(null, new Date(), 25 * 60000), true);
});

test('seriesFor extracts x/y pairs for one metric', () => {
  const { points } = parseFeed(sample);
  const s = seriesFor(points, 'co2');
  assert.deepEqual(s.map(p => p.y), [680, 690]);
});
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd "$HOME/Documents/Projects/portfolioWebsite" && node --test "tests/*.test.mjs"
```

Expected: FAIL, cannot find module `../sensors/lib.js`.

- [ ] **Step 3: Write the implementation**

Create `sensors/lib.js`:

```javascript
// Field numbers are the contract with the firmware. Changing one here means
// changing it in net.cpp too.
export const METRICS = [
  { field: 1, key: 'temp_f',   label: 'Temperature',   unit: 'degF' },
  { field: 2, key: 'humidity', label: 'Humidity',      unit: '%RH' },
  { field: 3, key: 'altitude', label: 'Altitude',      unit: 'ft' },
  { field: 4, key: 'v_rail',   label: 'Rail Voltage',  unit: 'V' },
  { field: 5, key: 'pm_count', label: 'Particles',     unit: 'count / 0.1 L' },
  { field: 6, key: 'co2',      label: 'CO2',           unit: 'ppm' },
  { field: 7, key: 'gas',      label: 'Gas Resistance', unit: 'ohm' }
];

// ThingSpeak hands back every field as a string, and a skipped field as null.
// Number(null) is 0, which would silently plot a real-looking zero, so null
// has to be checked before conversion.
function num(raw) {
  if (raw === null || raw === undefined || raw === '') return null;
  const n = Number(raw);
  return Number.isFinite(n) ? n : null;
}

export function parseFeed(json) {
  const feeds = (json && json.feeds) || [];
  const points = feeds.map(row => {
    const values = {};
    for (const m of METRICS) values[m.key] = num(row['field' + m.field]);
    return { t: new Date(row.created_at), values };
  });
  return { points, channel: (json && json.channel) || {} };
}

export function isStale(newest, now, maxAgeMs) {
  if (!newest) return true;
  return (now.getTime() - newest.getTime()) > maxAgeMs;
}

export function seriesFor(points, key) {
  return points.map(p => ({ x: p.t, y: p.values[key] }));
}
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
node --test "tests/*.test.mjs"
```

Expected: PASS, 8 tests.

- [ ] **Step 5: Commit**

```bash
git add sensors/lib.js tests/sensors.test.mjs
git commit -m "feat: add sensors feed parsing module with tests"
```

---

### Task 3: Web, the /sensors page

**Files:**
- Create: `sensors/index.html`, `sensors/sensors.js`, `sensors/sensors.css`, `sensors/vendor/chart.umd.min.js`
- Modify: `sitemap.xml`

**Interfaces:**
- Consumes: `METRICS`, `parseFeed`, `isStale`, `seriesFor` from `sensors/lib.js`

- [ ] **Step 1: Vendor Chart.js and its date adapter**

Chart.js needs a date adapter for a time axis. Both are vendored so the page keeps the site's zero-external-dependency property.

```bash
cd "$HOME/Documents/Projects/portfolioWebsite" && mkdir -p sensors/vendor
curl -sSL -o sensors/vendor/chart.umd.min.js https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js
curl -sSL -o sensors/vendor/luxon.min.js https://cdn.jsdelivr.net/npm/luxon@3.4.4/build/global/luxon.min.js
curl -sSL -o sensors/vendor/chartjs-adapter-luxon.min.js https://cdn.jsdelivr.net/npm/chartjs-adapter-luxon@1.3.1/dist/chartjs-adapter-luxon.umd.min.js
ls -la sensors/vendor/
```

Expected: three non-empty files. If any is under 1 KB the CDN returned an error page, so check it before continuing.

- [ ] **Step 2: Write the page shell**

Create `sensors/index.html`. Replace `YOUR_CHANNEL_ID` with the real ID from Task 1.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sensor Node | Jack Miller</title>
    <meta name="description" content="Live environmental sensor data from an ESP32C6 node, updated every 10 minutes." />
    <meta name="theme-color" content="#000000" />
    <link rel="canonical" href="https://guywithhat.me/sensors" />
    <link rel="stylesheet" href="../styles.css" />
    <link rel="stylesheet" href="sensors.css" />
</head>
<body>
    <div class="container">
        <header>
            <h1>Sensor Node</h1>
            <p class="tagline">ECEN 4610 capstone. XIAO ESP32C6 on the bench, one averaged point every 10 minutes.</p>
        </header>

        <div id="status" class="status" role="status">Loading...</div>

        <main id="charts" class="charts"></main>

        <footer class="sensors-footer">
            <p>Data stored on ThingSpeak channel
               <a id="channel-link" href="https://thingspeak.com/channels/YOUR_CHANNEL_ID">YOUR_CHANNEL_ID</a>.
               Graphs rendered here.</p>
            <p><a href="/">back to guywithhat.me</a></p>
        </footer>
    </div>

    <script src="vendor/luxon.min.js"></script>
    <script src="vendor/chart.umd.min.js"></script>
    <script src="vendor/chartjs-adapter-luxon.min.js"></script>
    <script type="module" src="sensors.js"></script>
</body>
</html>
```

- [ ] **Step 3: Write the styles**

Create `sensors/sensors.css`. This reuses the custom properties already declared in `styles.css`, so the page inherits the site's palette.

```css
.status {
    padding: 12px 16px;
    border: 1px solid var(--color-border);
    border-radius: 6px;
    background: var(--color-surface);
    color: var(--color-text-muted);
    font-size: 0.9rem;
    margin-bottom: 24px;
}

.status.stale {
    border-color: #d97706;
    color: #92400e;
    background: #fffbeb;
}

.status.error {
    border-color: #dc2626;
    color: #991b1b;
    background: #fef2f2;
}

.charts {
    display: grid;
    gap: 32px;
    margin-bottom: 48px;
}

.chart-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 6px;
    padding: 16px;
}

.chart-card h2 {
    font-size: 0.875rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-muted);
    margin-bottom: 12px;
}

.chart-wrap { position: relative; height: 220px; }

.sensors-footer {
    padding-bottom: 60px;
    font-size: 0.875rem;
    color: var(--color-text-muted);
}
```

- [ ] **Step 4: Write the page logic**

Create `sensors/sensors.js`. Replace `YOUR_CHANNEL_ID` with the real ID.

```javascript
import { METRICS, parseFeed, isStale, seriesFor } from './lib.js';

const CHANNEL_ID = 'YOUR_CHANNEL_ID';
const RESULTS = 144;             // 144 points at 10 min = 24 hours
const STALE_MS = 25 * 60 * 1000; // one missed window plus slack
const FEED_URL =
  `https://api.thingspeak.com/channels/${CHANNEL_ID}/feeds.json?results=${RESULTS}`;

const statusEl = document.getElementById('status');
const chartsEl = document.getElementById('charts');

function setStatus(text, cls) {
  statusEl.textContent = text;
  statusEl.className = 'status' + (cls ? ' ' + cls : '');
}

function humanAge(ms) {
  const min = Math.round(ms / 60000);
  if (min < 60) return `${min} min`;
  const hr = Math.floor(min / 60);
  return `${hr} hr ${min % 60} min`;
}

function renderChart(metric, points) {
  const card = document.createElement('section');
  card.className = 'chart-card';
  card.innerHTML =
    `<h2>${metric.label} (${metric.unit})</h2><div class="chart-wrap"><canvas></canvas></div>`;
  chartsEl.appendChild(card);

  new Chart(card.querySelector('canvas'), {
    type: 'line',
    data: {
      datasets: [{
        label: `${metric.label} (${metric.unit})`,
        data: seriesFor(points, metric.key),
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37,99,235,0.08)',
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.2,
        spanGaps: false   // a dropped window must read as a gap, not a straight line
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { type: 'time',
             time: { unit: 'hour', displayFormats: { hour: 'HH:mm' } },
             title: { display: true, text: 'Time' } },
        y: { title: { display: true, text: metric.unit } }
      }
    }
  });
}

async function load() {
  let json;
  try {
    const res = await fetch(FEED_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    json = await res.json();
  } catch (err) {
    setStatus(`Could not reach ThingSpeak: ${err.message}`, 'error');
    return;
  }

  const { points } = parseFeed(json);
  if (points.length === 0) {
    setStatus('Channel is live but has no data yet.', 'error');
    return;
  }

  const newest = points[points.length - 1].t;
  const now = new Date();
  if (isStale(newest, now, STALE_MS)) {
    setStatus(
      `Node may be offline. Last reading was ${humanAge(now - newest)} ago ` +
      `(${newest.toLocaleString()}). Showing the most recent data available.`,
      'stale');
  } else {
    setStatus(
      `Live. ${points.length} points over the last 24 hours. ` +
      `Last reading ${humanAge(now - newest)} ago.`, '');
  }

  for (const m of METRICS) renderChart(m, points);
}

const link = document.getElementById('channel-link');
link.href = `https://thingspeak.com/channels/${CHANNEL_ID}`;
link.textContent = CHANNEL_ID;

load();
setInterval(load, 5 * 60 * 1000);
```

- [ ] **Step 5: Verify against the live channel**

```bash
cd "$HOME/Documents/Projects/portfolioWebsite" && python3 -m http.server 8765
```

Open `http://localhost:8765/sensors/`. Expected: the status line reads either "Live" or "Node may be offline", and seven chart cards render with labeled axes. The single test point from Task 1 shows as one dot per chart.

Stop the server with Ctrl-C.

- [ ] **Step 6: Verify the stale banner**

The point posted in Task 1 will be over 25 minutes old by now, so the amber "Node may be offline" banner should already be showing. If it is not, post a fresh point with the Task 1 curl command, reload to confirm the green "Live" state, and trust that the threshold works.

- [ ] **Step 7: Add the page to the sitemap**

In `sitemap.xml`, add a `<url>` entry for `https://guywithhat.me/sensors` following the format of the existing entries.

- [ ] **Step 8: Commit**

```bash
git add sensors/ sitemap.xml
git commit -m "feat: add /sensors dashboard page"
```

---

### Task 4: Firmware, host-testable averaging accumulator

The 10 minute average is pure arithmetic with no Arduino dependency, so it compiles and runs on the Mac. Getting this right matters: it is the one piece where a silent bug produces plausible-looking wrong numbers for nine months.

**Files:**
- Create: `include/accumulator.h`
- Create: `test/test_accumulator/test_accumulator.cpp`
- Modify: `platformio.ini`

**Interfaces:**
- Produces: `struct Accumulator` with `void add(float)`, `void reset()`, `bool valid() const`, `uint32_t count() const`, `float mean() const`, `float min() const`, `float max() const`

- [ ] **Step 1: Add a native test environment**

Append to `platformio.ini`:

```ini
; Host-side tests for pure logic. `build_src_filter = -<*>` keeps src/ out of
; the native build, since main.cpp includes Arduino.h and will never compile here.
[env:native]
platform = native
test_framework = unity
build_src_filter = -<*>
build_flags = -std=gnu++17 -I include
```

- [ ] **Step 2: Write the failing test**

Create `test/test_accumulator/test_accumulator.cpp`:

```cpp
#include <unity.h>
#include "accumulator.h"

void setUp(void) {}
void tearDown(void) {}

void test_empty_is_invalid(void) {
  Accumulator a;
  TEST_ASSERT_FALSE(a.valid());
  TEST_ASSERT_EQUAL_UINT32(0, a.count());
}

void test_mean_of_known_values(void) {
  Accumulator a;
  a.add(10.0f); a.add(20.0f); a.add(30.0f);
  TEST_ASSERT_TRUE(a.valid());
  TEST_ASSERT_EQUAL_UINT32(3, a.count());
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 20.0f, a.mean());
}

void test_tracks_min_and_max(void) {
  Accumulator a;
  a.add(5.0f); a.add(-2.0f); a.add(11.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, -2.0f, a.min());
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 11.0f, a.max());
}

void test_reset_clears_everything(void) {
  Accumulator a;
  a.add(1.0f); a.reset();
  TEST_ASSERT_FALSE(a.valid());
  TEST_ASSERT_EQUAL_UINT32(0, a.count());
}

// A failed sensor read must not drag the average toward zero.
void test_nan_is_rejected(void) {
  Accumulator a;
  a.add(10.0f);
  a.add(NAN);
  TEST_ASSERT_EQUAL_UINT32(1, a.count());
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 10.0f, a.mean());
}

// 600 s of 10 Hz sampling is 6000 adds. Accumulating float into float loses
// resolution once the sum is large; the sum must be double.
void test_no_precision_loss_over_a_full_window(void) {
  Accumulator a;
  for (int i = 0; i < 6000; i++) a.add(1000.125f);
  TEST_ASSERT_EQUAL_UINT32(6000, a.count());
  TEST_ASSERT_FLOAT_WITHIN(0.01f, 1000.125f, a.mean());
}

int main(int, char **) {
  UNITY_BEGIN();
  RUN_TEST(test_empty_is_invalid);
  RUN_TEST(test_mean_of_known_values);
  RUN_TEST(test_tracks_min_and_max);
  RUN_TEST(test_reset_clears_everything);
  RUN_TEST(test_nan_is_rejected);
  RUN_TEST(test_no_precision_loss_over_a_full_window);
  return UNITY_END();
}
```

- [ ] **Step 3: Run the test to verify it fails**

```bash
export PATH="$HOME/.platformio/penv/bin:$PATH"
cd "$HOME/Desktop/ECEN 4610 - Capstone 1/IOT Sensor"
pio test -e native
```

Expected: FAIL, `accumulator.h: No such file or directory`.

- [ ] **Step 4: Write the implementation**

Create `include/accumulator.h`:

```cpp
#pragma once
#include <cmath>
#include <cstdint>

// Running mean/min/max for one metric over one upload window.
// Deliberately free of Arduino types so it builds and tests on the host.
struct Accumulator {
  void add(float v) {
    if (std::isnan(v)) return;   // a failed read is absent, not zero
    if (n_ == 0) { lo_ = v; hi_ = v; }
    else { if (v < lo_) lo_ = v; if (v > hi_) hi_ = v; }
    sum_ += static_cast<double>(v);
    n_++;
  }

  void reset() { sum_ = 0.0; n_ = 0; lo_ = 0.0f; hi_ = 0.0f; }

  bool     valid() const { return n_ > 0; }
  uint32_t count() const { return n_; }
  float    mean()  const { return n_ ? static_cast<float>(sum_ / n_) : NAN; }
  float    min()   const { return n_ ? lo_ : NAN; }
  float    max()   const { return n_ ? hi_ : NAN; }

 private:
  double   sum_ = 0.0;   // double, not float. 6000 adds of a 4-digit value
  uint32_t n_   = 0;     // overflows float's 24-bit mantissa.
  float    lo_  = 0.0f;
  float    hi_  = 0.0f;
};
```

- [ ] **Step 5: Run the tests to verify they pass**

```bash
pio test -e native
```

Expected: PASS, 6 tests.

- [ ] **Step 6: Confirm the device build still works**

```bash
pio run -e seeed_xiao_esp32c6
```

Expected: SUCCESS. The new `[env:native]` section must not disturb the device environment.

- [ ] **Step 7: Commit**

```bash
git add platformio.ini include/accumulator.h test/test_accumulator/
git commit -m "add host-testable averaging accumulator"
```

---

### Task 5: Firmware, sensor bring-up and reads

**Files:**
- Modify: `include/sensors.h`, `src/sensors.cpp`

**Interfaces:**
- Consumes: nothing from earlier tasks
- Produces: `struct SensorSample { float temp_f, humidity, altitude_ft, pm_count, co2, gas_ohm; }`, `bool sensorsBegin()`, `void sensorsPoll(SensorSample& out)`, `SensorStatus sensorsStatus()`

- [ ] **Step 1: Write the header**

Replace `include/sensors.h`:

```cpp
#pragma once
#include <cstdint>

// NAN in any field means "no new reading this poll", not "measured zero".
struct SensorSample {
  float temp_f;
  float humidity;
  float altitude_ft;
  float pm_count;
  float co2;
  float gas_ohm;
};

struct SensorStatus {
  bool bme;
  bool scd;
  bool pm;
};

// Brings up all three I2C sensors. Returns true only if all three answered.
// Partial failure still leaves the working ones usable; check sensorsStatus().
bool sensorsBegin();

// Non-blocking. Fills only the fields whose sensor has fresh data ready,
// leaving the rest NAN. Safe to call in a tight loop.
void sensorsPoll(SensorSample& out);

SensorStatus sensorsStatus();
```

- [ ] **Step 2: Write the implementation**

Replace `src/sensors.cpp`:

```cpp
#include "sensors.h"

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BME680.h>
#include <Adafruit_SCD30.h>
#include <Adafruit_PM25AQI.h>
#include <cmath>

static Adafruit_BME680   bme;
static Adafruit_SCD30    scd;
static Adafruit_PM25AQI  pm;
static SensorStatus      st = {false, false, false};

// BME688 with the gas heater on takes ~200ms per reading, so polling it
// faster than this just wastes the bus.
static const uint32_t BME_PERIOD_MS = 1000;
static uint32_t bmeLast = 0;

static const float SEA_LEVEL_HPA = 1013.25f;

bool sensorsBegin() {
  st.bme = bme.begin(0x77);
  if (st.bme) {
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    bme.setPressureOversampling(BME680_OS_4X);
    bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
    bme.setGasHeater(320, 150);  // 320 C for 150 ms
  }

  st.scd = scd.begin(0x61);
  // SCD30 self-paces at 2 s. Asking for faster costs accuracy for no gain
  // at a 10 minute averaging window.
  if (st.scd) scd.setMeasurementInterval(2);

  st.pm = pm.begin_I2C(&Wire);

  return st.bme && st.scd && st.pm;
}

SensorStatus sensorsStatus() { return st; }

void sensorsPoll(SensorSample& out) {
  out.temp_f = out.humidity = out.altitude_ft = NAN;
  out.pm_count = out.co2 = out.gas_ohm = NAN;

  if (st.bme && (millis() - bmeLast) >= BME_PERIOD_MS) {
    if (bme.performReading()) {
      out.temp_f      = bme.temperature * 9.0f / 5.0f + 32.0f;
      out.humidity    = bme.humidity;
      out.altitude_ft = bme.readAltitude(SEA_LEVEL_HPA) * 3.28084f;
      out.gas_ohm     = static_cast<float>(bme.gas_resistance);
    }
    bmeLast = millis();
  }

  if (st.scd && scd.dataReady()) {
    if (scd.read()) out.co2 = scd.CO2;
  }

  if (st.pm) {
    PM25_AQI_Data d;
    // Sum the 0.3 to 2.5 um bins, which is what the requirement asks for.
    if (pm.read(&d)) {
      out.pm_count = static_cast<float>(d.particles_03um) +
                     static_cast<float>(d.particles_05um) +
                     static_cast<float>(d.particles_10um) +
                     static_cast<float>(d.particles_25um);
    }
  }
}
```

- [ ] **Step 3: Build**

```bash
export PATH="$HOME/.platformio/penv/bin:$PATH"
cd "$HOME/Desktop/ECEN 4610 - Capstone 1/IOT Sensor"
pio run -e seeed_xiao_esp32c6
```

Expected: SUCCESS. If `Adafruit_SCD30.h` is not found, confirm the `lib_deps` block in `platformio.ini` still lists all three libraries.

- [ ] **Step 4: Verify on hardware with a temporary probe**

Temporarily replace the body of `loop()` in `src/main.cpp` with:

```cpp
void loop() {
  SensorSample s;
  sensorsPoll(s);
  Serial.printf("T=%.2fF RH=%.1f%% alt=%.0fft pm=%.0f co2=%.0f gas=%.0f\n",
                s.temp_f, s.humidity, s.altitude_ft, s.pm_count, s.co2, s.gas_ohm);
  delay(1000);
}
```

Add `#include "sensors.h"` at the top and `sensorsBegin();` at the end of `setup()`.

```bash
pio run -t upload && pio device monitor
```

Expected: temperature within a few degrees of room temperature, humidity between 20 and 60 in a normal room, CO2 between 400 and 1200 ppm, and `nan` appearing intermittently for SCD30 and BME688 rows because they pace slower than the loop. Intermittent `nan` here is correct behavior, not a bug.

If every field is `nan`, run an I2C scan to confirm 0x77, 0x61 and 0x12 all respond before debugging the drivers.

- [ ] **Step 5: Commit**

```bash
git add include/sensors.h src/sensors.cpp src/main.cpp
git commit -m "bring up bme688, scd30 and pmsa003i"
```

---

### Task 6: Firmware, rail voltage on ADC1

**Files:**
- Modify: `include/sensors.h`, `src/sensors.cpp`

**Interfaces:**
- Produces: `float readRailVolts()`, and a `v_rail` field added to `SensorSample`

- [ ] **Step 1: Build the divider**

Two equal resistors from the 5 V rail to ground, tap in the middle to **A0 (GPIO0)**. Use 10k and 10k. That halves 5.0 V to 2.5 V, comfortably inside ADC1's roughly 3.3 V full scale at maximum attenuation.

Higher values than 10k start interacting with the ADC's input impedance and read low. Do not use 100k.

- [ ] **Step 2: Add the declaration**

In `include/sensors.h`, add `float v_rail;` to `SensorSample` after `gas_ohm`, and declare:

```cpp
// Reads the 5V rail through a 2:1 divider on A0. Always returns a value;
// there is no "not ready" state for an ADC.
float readRailVolts();
```

- [ ] **Step 3: Implement**

Add to `src/sensors.cpp`:

```cpp
static const int   RAIL_ADC_PIN   = A0;
static const float DIVIDER_RATIO  = 2.0f;  // 10k/10k
static const int   RAIL_OVERSAMPLE = 8;

float readRailVolts() {
  // analogReadMilliVolts, not analogRead. It applies the per-chip factory
  // calibration burned into the eFuse; the raw counts are badly nonlinear
  // near both ends of the range.
  uint32_t acc = 0;
  for (int i = 0; i < RAIL_OVERSAMPLE; i++) acc += analogReadMilliVolts(RAIL_ADC_PIN);
  return (acc / RAIL_OVERSAMPLE) / 1000.0f * DIVIDER_RATIO;
}
```

Then in `sensorsPoll()`, add `out.v_rail = readRailVolts();` alongside the other reads. Note that `v_rail` is deliberately **not** added to the NAN initialization block at the top of that function, because unlike the I2C sensors the ADC always produces a reading and has no "not ready" state.

If the build fails with `'A0' was not declared`, the variant header does not alias the analog pins. Substitute the raw GPIO number and change the constant to `static const int RAIL_ADC_PIN = 0;`, which is the same pad per the pin map in the README.

- [ ] **Step 4: Verify against a DMM**

Flash, monitor, and compare the printed rail voltage against a multimeter on the same 5 V rail.

Expected: within about 100 mV. If it reads consistently low by a fixed percentage, your two resistors are not actually equal; measure them and set `DIVIDER_RATIO` to the real `(R1 + R2) / R2`.

Record the measured DMM value and the reported value. This is evidence for the report.

- [ ] **Step 5: Commit**

```bash
git add include/sensors.h src/sensors.cpp
git commit -m "add rail voltage measurement on adc1"
```

---

### Task 7: Firmware, wifi and the ThingSpeak upload

**Files:**
- Modify: `include/net.h`, `src/net.cpp`

**Interfaces:**
- Consumes: nothing from earlier tasks
- Produces: `bool netBegin(uint32_t timeoutMs)`, `bool netEnsureConnected()`, `bool netPostReading(const float* values, const bool* present, int count)`

- [ ] **Step 1: Write the header**

Replace `include/net.h`:

```cpp
#pragma once
#include <cstdint>

// Connects to the SSID in secrets.h. Returns false on timeout; the caller
// decides whether that is fatal.
bool netBegin(uint32_t timeoutMs);

// Cheap to call. Reconnects if the link dropped. Returns current state.
bool netEnsureConnected();

// Posts one averaged data point. `values[i]` maps to ThingSpeak fieldN where
// N = i + 1, so the array order IS the field contract. A false in `present`
// omits that field from the query string entirely, which ThingSpeak stores as
// null rather than zero.
// Returns true only if ThingSpeak replied with a nonzero entry id.
bool netPostReading(const float* values, const bool* present, int count);
```

- [ ] **Step 2: Write the implementation**

Replace `src/net.cpp`:

```cpp
#include "net.h"

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

#include "secrets.h"

// Plain HTTP on purpose. ThingSpeak accepts it, and WiFiClientSecure is the
// single largest heap consumer available to this firmware.
static const char* TS_HOST = "http://api.thingspeak.com/update";

bool netBegin(uint32_t timeoutMs) {
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);   // modem sleep adds latency and buys nothing on USB power
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  uint32_t start = millis();
  while (WiFi.status() != WL_CONNECTED && (millis() - start) < timeoutMs) {
    delay(250);
  }
  return WiFi.status() == WL_CONNECTED;
}

bool netEnsureConnected() {
  if (WiFi.status() == WL_CONNECTED) return true;
  WiFi.disconnect();
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  uint32_t start = millis();
  while (WiFi.status() != WL_CONNECTED && (millis() - start) < 15000) delay(250);
  return WiFi.status() == WL_CONNECTED;
}

bool netPostReading(const float* values, const bool* present, int count) {
  if (!netEnsureConnected()) return false;

  String url = String(TS_HOST) + "?api_key=" + TS_WRITE_KEY;
  for (int i = 0; i < count; i++) {
    if (!present[i]) continue;   // omitted, not zero
    url += "&field" + String(i + 1) + "=" + String(values[i], 3);
  }

  WiFiClient client;
  HTTPClient http;
  http.setTimeout(10000);
  if (!http.begin(client, url)) return false;

  int code = http.GET();
  String body = http.getString();
  http.end();

  // ThingSpeak answers with the new entry id, or "0" if it rejected the write
  // (bad key, or faster than the 15 s minimum interval). HTTP 200 alone is
  // not success here.
  bool ok = (code == 200) && (body.toInt() > 0);
  Serial.printf("[net] post http=%d body=%s -> %s\n",
                code, body.c_str(), ok ? "ok" : "FAILED");
  return ok;
}
```

- [ ] **Step 3: Verify wifi and one real post**

Temporarily set `setup()` to call `netBegin(30000)` then post a fixed test point:

```cpp
float v[7]  = {70.0f, 40.0f, 5280.0f, 5.0f, 100.0f, 500.0f, 90000.0f};
bool  p[7]  = {true, true, true, true, true, true, true};
netPostReading(v, p, 7);
```

```bash
pio run -t upload && pio device monitor
```

Expected: `[net] post http=200 body=<some number> -> ok`. Then confirm the point arrived:

```bash
curl -sS "https://api.thingspeak.com/channels/YOURCHANNELID/feeds.json?results=1"
```

Expected: `field1` is `"70.000"`.

- [ ] **Step 4: Verify the omission path**

Set `p[5] = false` (CO2 absent), reflash, and check the feed again. Expected: `field6` comes back as `null`, not `"0"`. This is the behavior that keeps a dead sensor from drawing a flat zero line across the graph for a week.

- [ ] **Step 5: Commit**

```bash
git add include/net.h src/net.cpp src/main.cpp
git commit -m "add wifi connect and thingspeak upload"
```

---

### Task 8: Firmware, the sampling loop and resilience

Wires everything together and makes it survive nine months unattended.

**Files:**
- Modify: `src/main.cpp`

**Interfaces:**
- Consumes: `Accumulator`, `SensorSample`, `sensorsBegin()`, `sensorsPoll()`, `readRailVolts()`, `netBegin()`, `netPostReading()`

- [ ] **Step 1: Write main.cpp**

Replace `src/main.cpp`, keeping the existing `initAntenna()` exactly as it is:

```cpp
#include <Arduino.h>
#include <Wire.h>

#include "accumulator.h"
#include "net.h"
#include "secrets.h"
#include "sensors.h"

// XIAO ESP32C6 RF switch. Pins float on boot and wifi range is awful until
// these are driven. WIFI_ANT_CONFIG low = onboard ceramic, high = u.FL.
static void initAntenna() {
  pinMode(WIFI_ENABLE, OUTPUT);
  digitalWrite(WIFI_ENABLE, LOW);
  pinMode(WIFI_ANT_CONFIG, OUTPUT);
  digitalWrite(WIFI_ANT_CONFIG, LOW);
}

static const uint32_t WINDOW_MS = 600000;  // 10 min, requirement 2
static const int      NFIELDS   = 7;

// Index IS the ThingSpeak field number minus one. Do not reorder.
enum { F_TEMP = 0, F_RH, F_ALT, F_VRAIL, F_PM, F_CO2, F_GAS };

static Accumulator acc[NFIELDS];
static uint32_t    windowStart = 0;
static uint32_t    consecutiveFailures = 0;

static void uploadWindow() {
  float values[NFIELDS];
  bool  present[NFIELDS];

  for (int i = 0; i < NFIELDS; i++) {
    present[i] = acc[i].valid();
    values[i]  = present[i] ? acc[i].mean() : 0.0f;
  }

  // Sample counts go to serial only. They are needed for the report table,
  // not for the graphs, and the channel only has seven field slots.
  Serial.printf("[win] n: T=%lu RH=%lu alt=%lu V=%lu pm=%lu co2=%lu gas=%lu\n",
                (unsigned long)acc[F_TEMP].count(), (unsigned long)acc[F_RH].count(),
                (unsigned long)acc[F_ALT].count(),  (unsigned long)acc[F_VRAIL].count(),
                (unsigned long)acc[F_PM].count(),   (unsigned long)acc[F_CO2].count(),
                (unsigned long)acc[F_GAS].count());

  if (netPostReading(values, present, NFIELDS)) {
    consecutiveFailures = 0;
  } else {
    consecutiveFailures++;
    Serial.printf("[win] upload failed, %lu in a row\n",
                  (unsigned long)consecutiveFailures);
  }

  for (int i = 0; i < NFIELDS; i++) acc[i].reset();

  // Three missed windows is half an hour of silence. Something is wedged that
  // a reconnect has not fixed, so restart rather than sit dead until someone
  // walks past the bench in February.
  if (consecutiveFailures >= 3) {
    Serial.println("[win] too many failures, restarting");
    delay(200);
    ESP.restart();
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial && millis() < 3000) {}  // native USB-CDC needs a moment

  initAntenna();

  Wire.begin();          // SDA=D4/GPIO22, SCL=D5/GPIO23
  Wire.setClock(100000); // SCD30 tops out at 100kHz and stretches the clock hard

  if (!sensorsBegin()) {
    SensorStatus s = sensorsStatus();
    Serial.printf("[boot] sensor trouble: bme=%d scd=%d pm=%d\n", s.bme, s.scd, s.pm);
  }

  // A failed first connect is not fatal. The window loop retries every 10 min.
  if (!netBegin(30000)) Serial.println("[boot] wifi failed, will retry");

  windowStart = millis();
  Serial.println("boot ok");
}

void loop() {
  SensorSample s;
  sensorsPoll(s);

  acc[F_TEMP].add(s.temp_f);
  acc[F_RH].add(s.humidity);
  acc[F_ALT].add(s.altitude_ft);
  acc[F_VRAIL].add(s.v_rail);
  acc[F_PM].add(s.pm_count);
  acc[F_CO2].add(s.co2);
  acc[F_GAS].add(s.gas_ohm);

  // millis() rolls over every 49 days and this box runs for nine months.
  // Unsigned subtraction handles the wrap correctly; comparing raw timestamps
  // would not.
  if ((millis() - windowStart) >= WINDOW_MS) {
    windowStart += WINDOW_MS;
    uploadWindow();
  }

  delay(20);  // let the wifi task run
}
```

- [ ] **Step 2: Build and flash**

```bash
export PATH="$HOME/.platformio/penv/bin:$PATH"
cd "$HOME/Desktop/ECEN 4610 - Capstone 1/IOT Sensor"
pio run -e seeed_xiao_esp32c6 -t upload && pio device monitor
```

Expected: `boot ok`, then silence for ten minutes, then a `[win] n: ...` line followed by `[net] post ... -> ok`.

- [ ] **Step 3: Verify the window timing with a temporary short window**

Ten minutes per test iteration is too slow to debug. Temporarily set `WINDOW_MS` to `20000` and reflash.

Expected: a window line every 20 seconds. Confirm the sample counts are plausible: at `delay(20)` the rail voltage should accumulate roughly 900 samples in 20 s, while CO2 should show about 10, because the SCD30 only produces a reading every 2 s.

That divergence is the point. Each sensor has its own achievable rate, and those counts are exactly the numbers the report table asks for. **Record them now.**

- [ ] **Step 4: Restore the real window**

Set `WINDOW_MS` back to `600000`. Reflash. Confirm one upload after ten minutes.

Note that ThingSpeak enforces a 15 s minimum write interval on the free tier, so a short test window below that will produce `body=0` failures. That is expected during testing and not a firmware bug.

- [ ] **Step 5: Verify recovery from a wifi drop**

With the node running, disconnect the access point or move the node out of range for one window. Expected: `[win] upload failed, 1 in a row`, then a successful post once the link returns, with `consecutiveFailures` back to 0.

- [ ] **Step 6: Commit**

```bash
git add src/main.cpp
git commit -m "add 10 minute sampling window with upload and restart on failure"
```

---

### Task 9: QR code, deploy and the report table

**Files:**
- Create: `~/Desktop/ECEN 4610 - Capstone 1/IOT Sensor/docs/qr-sensors.png`
- Modify: `~/Desktop/ECEN 4610 - Capstone 1/IOT Sensor/README.md`

- [ ] **Step 1: Deploy the dashboard**

The web work is committed but not pushed. Ask Jack to confirm before pushing, per his standing rule.

```bash
cd "$HOME/Documents/Projects/portfolioWebsite" && git push origin main
```

Cloudflare Pages builds on push. Wait about a minute, then verify the live URL:

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://guywithhat.me/sensors
```

Expected: `200`.

- [ ] **Step 2: Generate the QR code**

```bash
brew install qrencode
cd "$HOME/Desktop/ECEN 4610 - Capstone 1/IOT Sensor" && mkdir -p docs
qrencode -o docs/qr-sensors.png -s 12 -m 2 "https://guywithhat.me/sensors"
```

- [ ] **Step 3: Verify the QR code actually resolves**

Open `docs/qr-sensors.png` and scan it with a phone camera. Expected: it opens the live dashboard.

Do not skip this. A QR code that encodes a typo is indistinguishable from a working one by eye, and this one gets printed and left on a bench for a semester.

- [ ] **Step 4: Record the sample rate table**

Using the counts captured in Task 8 Step 3, add to the firmware README:

```markdown
## Sample rates

Measured with a 20 s test window, extrapolated to the 600 s production window.

| Sensor | Metric | Limiting factor | Samples per uploaded point |
|---|---|---|---|
| BME688 | temp, RH, altitude, gas | 1 s software poll, ~200 ms conversion with gas heater | ~600 |
| SCD30 | CO2 | 2 s internal measurement interval | ~300 |
| PMSA003I | particle count | ~1 s sensor output rate | ~600 |
| ADC1 | rail voltage | loop rate, 20 ms | ~30000 |

Fill the last column with the counts actually printed by `[win] n:`.
```

- [ ] **Step 5: Commit**

```bash
cd "$HOME/Desktop/ECEN 4610 - Capstone 1/IOT Sensor"
git add README.md docs/qr-sensors.png
git commit -m "add qr code and measured sample rate table"
```

- [ ] **Step 6: Confirm 24 hours of data before submitting**

The deliverable requires the URL to show at least 24 hours of data. Leave the node running a full day, then check the point count:

```bash
curl -sS "https://api.thingspeak.com/channels/YOURCHANNELID/feeds.json?results=144" \
  | python3 -c "import json,sys; f=json.load(sys.stdin)['feeds']; print(len(f), 'points', f[0]['created_at'], '->', f[-1]['created_at'])"
```

Expected: close to 144 points spanning about 24 hours. A count well under 144 means windows are being dropped, so check the serial log for repeated upload failures before submitting.
