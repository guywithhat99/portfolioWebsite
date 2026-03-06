# Build Your Own Virtual Pet

### An Arduino C++ Workshop

<img src="presentationPhotos/slide1.jpeg" style="max-width:85%;max-height:340px;border-radius:12px;margin-top:24px;object-fit:cover;box-shadow:0 8px 40px rgba(0,0,0,0.5);">

---

## What We're Building

A handheld virtual pet that lives on a microcontroller.

- Feed it, water it, play games with it
- Ignore it long enough and it gets hungry and tired
- 3 buttons, an RGB LED, a buzzer, and a screen

**Your pet starts alive but broken — you bring it to life piece by piece.**

---

## What's Inside

<div style="display:flex;gap:28px;align-items:center;margin-top:16px;">
<table style="flex:1;border-collapse:collapse;">
<thead><tr><th style="color:#f0a830;border-bottom:2px solid #f0a830;padding:0.4em 0.8em;font-size:0.75em;text-transform:uppercase;letter-spacing:0.05em;">Component</th><th style="color:#f0a830;border-bottom:2px solid #f0a830;padding:0.4em 0.8em;font-size:0.75em;text-transform:uppercase;letter-spacing:0.05em;">What it does</th></tr></thead>
<tbody>
<tr><td style="padding:0.35em 0.8em;border-bottom:1px solid #2a3545;font-family:'JetBrains Mono',monospace;font-size:0.72em;"><strong>Pico</strong></td><td style="padding:0.35em 0.8em;border-bottom:1px solid #2a3545;font-family:'JetBrains Mono',monospace;font-size:0.72em;">The brain — runs your code</td></tr>
<tr><td style="padding:0.35em 0.8em;border-bottom:1px solid #2a3545;font-family:'JetBrains Mono',monospace;font-size:0.72em;"><strong>LCD Display</strong></td><td style="padding:0.35em 0.8em;border-bottom:1px solid #2a3545;font-family:'JetBrains Mono',monospace;font-size:0.72em;">Shows your pet's face and stats</td></tr>
<tr><td style="padding:0.35em 0.8em;border-bottom:1px solid #2a3545;font-family:'JetBrains Mono',monospace;font-size:0.72em;"><strong>3 Buttons</strong></td><td style="padding:0.35em 0.8em;border-bottom:1px solid #2a3545;font-family:'JetBrains Mono',monospace;font-size:0.72em;">Red, Yellow, Green — your controls</td></tr>
<tr><td style="padding:0.35em 0.8em;border-bottom:1px solid #2a3545;font-family:'JetBrains Mono',monospace;font-size:0.72em;"><strong>RGB LED</strong></td><td style="padding:0.35em 0.8em;border-bottom:1px solid #2a3545;font-family:'JetBrains Mono',monospace;font-size:0.72em;">Mood indicator + game feedback</td></tr>
<tr><td style="padding:0.35em 0.8em;font-family:'JetBrains Mono',monospace;font-size:0.72em;"><strong>Buzzer</strong></td><td style="padding:0.35em 0.8em;font-family:'JetBrains Mono',monospace;font-size:0.72em;">Sound effects and melodies</td></tr>
</tbody>
</table>
<img src="presentationPhotos/slide3.jpeg" style="height:400px;width:auto;flex-shrink:0;border-radius:12px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
</div>

---

## The Pico

<img src="presentationPhotos/Slide%2011.png" style="max-width:90%;max-height:460px;border-radius:12px;margin-top:16px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">

----

### setup() and loop()

Every Arduino program has two functions:

```cpp
void setup() {
    // runs ONCE at power-on
}

void loop() {
    // runs FOREVER, as fast as possible
}
```

This is the heartbeat of every embedded program.

----

### How a Breadboard Works

<div style="display:flex;align-items:center;gap:32px;margin-top:12px;">
<svg viewBox="0 0 400 240" xmlns="http://www.w3.org/2000/svg" style="width:55%;flex-shrink:0;border-radius:8px;">
  <rect width="400" height="240" fill="#111820" rx="8"/>
  <rect x="6" y="6" width="388" height="228" fill="#1a2818" rx="5"/>
  <!-- Left + rail -->
  <rect x="12" y="18" width="16" height="208" fill="#f8717115" rx="3"/>
  <line x1="20" y1="22" x2="20" y2="222" stroke="#f87171" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="20" y="14" fill="#f87171" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">+</text>
  <!-- Left - rail -->
  <rect x="32" y="18" width="16" height="208" fill="#60a5fa15" rx="3"/>
  <line x1="40" y1="22" x2="40" y2="222" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="40" y="14" fill="#60a5fa" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">−</text>
  <!-- Left rail gap: shaded strip + dashed separator line -->
  <rect x="50" y="18" width="13" height="208" fill="#0c101935" rx="0"/>
  <line x1="56" y1="18" x2="56" y2="226" stroke="#2a3545" stroke-width="1" stroke-dasharray="2,5"/>
  <!-- Right rail gap: shaded strip + dashed separator line -->
  <rect x="323" y="18" width="24" height="208" fill="#0c101935" rx="0"/>
  <line x1="336" y1="18" x2="336" y2="226" stroke="#2a3545" stroke-width="1" stroke-dasharray="2,5"/>
  <!-- Right - rail -->
  <rect x="352" y="18" width="16" height="208" fill="#60a5fa15" rx="3"/>
  <line x1="360" y1="22" x2="360" y2="222" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="360" y="14" fill="#60a5fa" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">−</text>
  <!-- Right + rail -->
  <rect x="372" y="18" width="16" height="208" fill="#f8717115" rx="3"/>
  <line x1="380" y1="22" x2="380" y2="222" stroke="#f87171" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="380" y="14" fill="#f87171" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">+</text>
  <!-- Column labels -->
  <text x="72" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">a</text>
  <text x="96" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">b</text>
  <text x="120" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">c</text>
  <text x="144" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">d</text>
  <text x="168" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">e</text>
  <text x="220" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">f</text>
  <text x="244" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">g</text>
  <text x="268" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">h</text>
  <text x="292" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">i</text>
  <text x="316" y="14" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="9" text-anchor="middle">j</text>
  <!-- Center gap label -->
  <text x="196" y="124" fill="#f0a830" font-family="DM Sans,sans-serif" font-size="8" text-anchor="middle" transform="rotate(-90,196,124)">GAP — not connected</text>
  <!-- Row 1 y=36 -->
  <line x1="64" y1="36" x2="176" y2="36" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="72" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="96" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="120" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="144" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="168" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <line x1="212" y1="36" x2="324" y2="36" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="220" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="244" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="268" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="292" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="316" cy="36" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <text x="56" y="39" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">1</text>
  <!-- Row 2 y=60 -->
  <line x1="64" y1="60" x2="176" y2="60" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="72" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="96" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="120" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="144" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="168" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <line x1="212" y1="60" x2="324" y2="60" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="220" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="244" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="268" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="292" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="316" cy="60" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <text x="56" y="63" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">2</text>
  <!-- Row 3 y=84 -->
  <line x1="64" y1="84" x2="176" y2="84" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="72" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="96" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="120" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="144" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="168" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <line x1="212" y1="84" x2="324" y2="84" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="220" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="244" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="268" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="292" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="316" cy="84" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <text x="56" y="87" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">3</text>
  <!-- Row 4 y=108 -->
  <line x1="64" y1="108" x2="176" y2="108" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="72" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="96" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="120" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="144" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="168" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <line x1="212" y1="108" x2="324" y2="108" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="220" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="244" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="268" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="292" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="316" cy="108" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <text x="56" y="111" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">4</text>
  <!-- Row 5 y=132 -->
  <line x1="64" y1="132" x2="176" y2="132" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="72" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="96" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="120" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="144" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="168" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <line x1="212" y1="132" x2="324" y2="132" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="220" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="244" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="268" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="292" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="316" cy="132" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <text x="56" y="135" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">5</text>
  <!-- Row 6 y=156 -->
  <line x1="64" y1="156" x2="176" y2="156" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="72" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="96" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="120" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="144" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="168" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <line x1="212" y1="156" x2="324" y2="156" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="220" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="244" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="268" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="292" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="316" cy="156" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <text x="56" y="159" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">6</text>
  <!-- Row 7 y=180 -->
  <line x1="64" y1="180" x2="176" y2="180" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="72" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="96" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="120" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="144" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="168" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <line x1="212" y1="180" x2="324" y2="180" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="220" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="244" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="268" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="292" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="316" cy="180" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <text x="56" y="183" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">7</text>
  <!-- Row 8 y=204 -->
  <line x1="64" y1="204" x2="176" y2="204" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="72" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="96" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="120" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="144" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="168" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <line x1="212" y1="204" x2="324" y2="204" stroke="#4ade8035" stroke-width="8" stroke-linecap="round"/>
  <circle cx="220" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="244" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="268" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="292" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <circle cx="316" cy="204" r="4" fill="#0c1019" stroke="#4ade80" stroke-width="1.2"/>
  <text x="56" y="207" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">8</text>
</svg>
<div style="flex:1;text-align:left;">
<ul>
<li><strong>Power rails</strong> (red +, blue −) run <em>vertically</em> the full length</li>
<li><strong>Rail gap</strong> — rails are <em>not</em> connected to tie strip rows</li>
<li><strong>Tie strips</strong> — each row (a–e and f–j) is connected <em>horizontally</em></li>
<li><strong>Center gap</strong> — left and right halves are <em>not</em> connected</li>
<li>Place each leg of a component in a different <strong>row</strong></li>
</ul>
</div>
</div>

---

## Wiring — Display

SPI protocol — 6 data wires + power.

<table style="width:70%; margin: 0 auto;">
<thead><tr><th>Signal</th><th>Pico Pin</th><th></th><th>Signal</th><th>Pico Pin</th></tr></thead>
<tbody>
<tr><td>SCK</td><td>GP10</td><td style="border:none;"></td><td>RST</td><td>GP12</td></tr>
<tr><td>MOSI</td><td>GP11</td><td style="border:none;"></td><td>BL</td><td>GP13</td></tr>
<tr><td>DC</td><td>GP8</td><td style="border:none;"></td><td>VCC</td><td>3V3</td></tr>
<tr><td>CS</td><td>GP9</td><td style="border:none;"></td><td>GND</td><td>GND</td></tr>
</tbody>
</table>

<img src="presentationPhotos/Slide%2013.png" style="max-width:90%;max-height:340px;border-radius:12px;margin-top:20px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">

----

### Wiring — Buttons

Each button: one leg to GPIO, other leg to GND.

| Button | Pico Pin |
|--------|----------|
| Red | GP22 |
| Yellow | GP21 |
| Green | GP19 |

<img src="presentationPhotos/Slide%2014.png" style="max-width:90%;max-height:300px;border-radius:12px;margin-top:20px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">

----

### Wiring — LED & Buzzer

**RGB LED:** Red→GP16, Green→GP17, Blue→GP18, GND→GND

**Buzzer:** +→GP6, -→GND

<img src="presentationPhotos/SLide%2015.png" style="max-width:85%;max-height:380px;border-radius:12px;margin-top:20px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">

---

## Setup

Five steps. Then you're coding.

----

### 1 — Install VS Code

<div class="step-num">01</div>

<div style="display:flex;align-items:center;gap:40px;margin-top:16px;">
<div style="flex:1;text-align:left;">
<p>Download from <strong>code.visualstudio.com</strong></p>
<ul>
<li>Choose Windows, Mac, or Linux</li>
<li>Run the installer — accept the defaults</li>
<li>Open VS Code when done</li>
</ul>
</div>
<img src="presentationPhotos/vsdownload.png" style="width:54%;border-radius:12px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
</div>

----

### 2 — Install PlatformIO

<div class="step-num">02</div>

<div style="display:flex;align-items:center;gap:40px;margin-top:16px;">
<div style="flex:1;text-align:left;">
<p>Open the <strong>Extensions</strong> panel:</p>
<ul>
<li><strong>Windows / Linux</strong> — <code>Ctrl+Shift+X</code></li>
<li><strong>Mac</strong> — <code>Cmd+Shift+X</code></li>
<li>Search <strong>PlatformIO IDE</strong>, click <strong>Install</strong></li>
<li>VS Code reloads automatically</li>
</ul>
</div>
<img src="presentationPhotos/Platformio.png" style="width:54%;border-radius:12px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
</div>

----

### 3 — Get the Project

<div class="step-num">03</div>

Go to **github.com/guywithhat99** — **tamagotchi-starter** for the workshop, **tamagotchi-reference** for the finished version. Click **Code → Download ZIP**.

<div style="display:flex;gap:20px;align-items:flex-start;margin-top:14px;">
<img src="presentationPhotos/Pinned%20repos.png" style="max-width:50%;max-height:390px;border-radius:12px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
<img src="presentationPhotos/download%20repo.png" style="max-width:48%;max-height:390px;border-radius:12px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
</div>

----

### 4 — Open the Folder

<div class="step-num">04</div>

<div style="display:flex;align-items:center;gap:40px;margin-top:16px;">
<div style="flex:1;text-align:left;">
<ul>
<li><strong>File → Open Folder</strong> in VS Code</li>
<li>Select the <code>tamagotchi_starter</code> folder</li>
<li>PlatformIO detects <code>platformio.ini</code> automatically</li>
<li><strong>First open downloads the Pico toolchain</strong> — watch the status bar at the bottom</li>
</ul>
</div>
<img src="presentationPhotos/Stater%20vscode.png" style="width:54%;border-radius:12px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
</div>

----

### 5 — Build & Upload

<div class="step-num">05</div>

<div style="display:flex;flex-direction:column;align-items:center;gap:24px;margin-top:16px;">
<div style="text-align:left;width:100%;">
<p>PlatformIO adds its own icons to the <strong>bottom toolbar</strong>:</p>
<ul>
<li>Click <strong>✓</strong> — wait for <strong>SUCCESS</strong> in the terminal</li>
<li>Plug your Pico in via USB</li>
<li>Click <strong>→</strong> to upload</li>
</ul>
</div>
<img src="presentationPhotos/build%20and%20upload%20buttons.png" style="max-width:88%;max-height:160px;border-radius:12px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
</div>

----

### platformio.ini — What's Inside

```ini
[env:rpipico]
platform          = https://github.com/maxgerhardt/platform-raspberrypi.git
board             = rpipico
framework         = arduino
board_build.core  = earlephilhower
upload_protocol   = picotool
extra_scripts     = pre:upload_reset.py

monitor_speed     = 115200

lib_deps =
    adafruit/Adafruit ST7735 and ST7789 Library
    adafruit/Adafruit GFX Library
```

Already in the project — PlatformIO reads this and installs everything.

---

## Step 0 — Hello World

Get the display working.

----

### main.cpp

Create `src/main.cpp`:

```cpp
#include <Arduino.h>
#include "Pet.h"

Pet pet;

void setup() {
    Serial.begin(115200);
    Serial.println("Pet alive!");
    pet.begin();
}

void loop() {
    pet.update();
    delay(50);
}
```

`Pet` is provided — it handles the display, stats, and sprites.

----

### Serial Monitor

Open the Serial Monitor (**PlatformIO sidebar → Serial Monitor**, or the plug icon).

`Serial.begin(115200)` opens a connection at 115200 baud.
`Serial.println()` sends a line of text to your computer.

```
Pet alive!
```

This is your **debugging window** — you'll use it throughout the workshop to see what your code is doing.

----

### Try It

Upload — your pet's face appears and "Pet alive!" shows in the Serial Monitor.

**Nothing in the monitor?** Make sure baud rate is set to **115200** in the Serial Monitor dropdown.

----

### ✓ What You Learned

- Your program has `setup()` — runs once — and `loop()` — runs forever
- `Serial.begin(115200)` opens USB serial at 115200 baud — same cable as upload, no extra wiring
- `Serial.println()` sends text to your computer — your first debugging tool
- `pet.begin()` initialises the display and draws the pet's face
- `pet.update()` redraws the screen each frame

---

## Step 1 — Buttons

Teach your pet to listen.

----

### Inside a Tactile Button

<div style="display:flex;align-items:center;gap:32px;margin-top:12px;">
<div style="flex:1;text-align:left;">
<ul>
<li>4 physical pins — but only <strong>2 electrical sides</strong></li>
<li>Each side's pin pair is <em>always shorted</em> together</li>
<li>Pressing <em>bridges</em> side A to side B</li>
<li><code>INPUT_PULLDOWN</code> — pin held <strong>LOW</strong> until button connects it to 3.3V</li>
</ul>
</div>
<svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" style="width:52%;flex-shrink:0;border-radius:8px;">
  <rect width="360" height="200" fill="#111820" rx="8"/>
  <!-- ── LEFT: Button anatomy ── -->
  <text x="88" y="13" fill="#f5e6c8" font-family="DM Sans,sans-serif" font-size="9" font-weight="700" text-anchor="middle">inside the button</text>
  <!-- Button body -->
  <rect x="53" y="22" width="70" height="114" fill="#1a2818" rx="4" stroke="#2a3545" stroke-width="1.5"/>
  <!-- Cap -->
  <circle cx="88" cy="79" r="24" fill="#243020"/>
  <circle cx="88" cy="79" r="10" fill="#111820" stroke="#4ade8030" stroke-width="1"/>
  <!-- Side A: left pin pair, always shorted -->
  <rect x="30" y="33" width="23" height="8" fill="#f0a830" rx="2"/>
  <rect x="30" y="115" width="23" height="8" fill="#f0a830" rx="2"/>
  <line x1="41" y1="41" x2="41" y2="115" stroke="#f0a830" stroke-width="2.5" stroke-linecap="round"/>
  <text x="22" y="79" fill="#f0a830" font-family="DM Sans,sans-serif" font-size="7" text-anchor="middle" transform="rotate(-90,22,79)">side A · shorted</text>
  <text x="41" y="158" fill="#f0a830" font-family="JetBrains Mono,monospace" font-size="7" text-anchor="middle">3.3V</text>
  <!-- Side B: right pin pair, always shorted -->
  <rect x="123" y="33" width="23" height="8" fill="#60a5fa" rx="2"/>
  <rect x="123" y="115" width="23" height="8" fill="#60a5fa" rx="2"/>
  <line x1="135" y1="41" x2="135" y2="115" stroke="#60a5fa" stroke-width="2.5" stroke-linecap="round"/>
  <text x="154" y="79" fill="#60a5fa" font-family="DM Sans,sans-serif" font-size="7" text-anchor="middle" transform="rotate(90,154,79)">side B · shorted</text>
  <text x="135" y="158" fill="#60a5fa" font-family="JetBrains Mono,monospace" font-size="7" text-anchor="middle">GP22</text>
  <!-- Press bridge (dashed) -->
  <line x1="53" y1="79" x2="123" y2="79" stroke="#4ade80" stroke-width="2" stroke-dasharray="5,4"/>
  <text x="88" y="145" fill="#4ade80" font-family="DM Sans,sans-serif" font-size="8" text-anchor="middle">bridged when pressed</text>
  <!-- Center divider -->
  <line x1="178" y1="8" x2="178" y2="192" stroke="#2a3545" stroke-width="1"/>
  <!-- ── RIGHT: Circuit states ── -->
  <!-- NOT PRESSED -->
  <text x="269" y="13" fill="#8a8272" font-family="DM Sans,sans-serif" font-size="9" font-weight="700" text-anchor="middle">not pressed</text>
  <text x="218" y="28" fill="#f87171" font-family="JetBrains Mono,monospace" font-size="8">3.3V</text>
  <line x1="238" y1="29" x2="238" y2="43" stroke="#f87171" stroke-width="1.5"/>
  <circle cx="238" cy="46" r="2.5" fill="#f87171"/>
  <line x1="241" y1="46" x2="253" y2="41" stroke="#f87171" stroke-width="1.5"/>
  <circle cx="257" cy="46" r="2.5" fill="#60a5fa"/>
  <line x1="257" y1="49" x2="257" y2="60" stroke="#60a5fa" stroke-width="1.5"/>
  <circle cx="257" cy="60" r="3" fill="#60a5fa"/>
  <text x="263" y="63" fill="#60a5fa" font-family="JetBrains Mono,monospace" font-size="7">GP22</text>
  <line x1="305" y1="60" x2="315" y2="60" stroke="#8a8272" stroke-width="0.5" stroke-dasharray="2,3"/>
  <text x="318" y="63" fill="#8a8272" font-family="DM Sans,sans-serif" font-size="9" font-weight="700">LOW</text>
  <line x1="257" y1="63" x2="257" y2="71" stroke="#60a5fa" stroke-width="1.5"/>
  <polyline points="257,71 252,75 262,79 252,83 257,87" fill="none" stroke="#8a8272" stroke-width="1.5"/>
  <line x1="257" y1="87" x2="257" y2="93" stroke="#8a8272" stroke-width="1.5"/>
  <line x1="246" y1="93" x2="268" y2="93" stroke="#8a8272" stroke-width="1.5"/>
  <line x1="250" y1="96" x2="264" y2="96" stroke="#8a8272" stroke-width="1"/>
  <line x1="254" y1="99" x2="260" y2="99" stroke="#8a8272" stroke-width="0.7"/>
  <!-- Horizontal divider -->
  <line x1="185" y1="108" x2="352" y2="108" stroke="#2a3545" stroke-width="1"/>
  <!-- PRESSED -->
  <text x="269" y="122" fill="#4ade80" font-family="DM Sans,sans-serif" font-size="9" font-weight="700" text-anchor="middle">pressed</text>
  <text x="218" y="137" fill="#f87171" font-family="JetBrains Mono,monospace" font-size="8">3.3V</text>
  <line x1="238" y1="138" x2="238" y2="150" stroke="#f87171" stroke-width="1.5"/>
  <circle cx="238" cy="153" r="2.5" fill="#f87171"/>
  <line x1="241" y1="153" x2="254" y2="153" stroke="#4ade80" stroke-width="2"/>
  <circle cx="257" cy="153" r="2.5" fill="#60a5fa"/>
  <line x1="257" y1="156" x2="257" y2="167" stroke="#60a5fa" stroke-width="1.5"/>
  <circle cx="257" cy="167" r="3" fill="#60a5fa"/>
  <text x="263" y="170" fill="#60a5fa" font-family="JetBrains Mono,monospace" font-size="7">GP22</text>
  <line x1="305" y1="167" x2="315" y2="167" stroke="#4ade80" stroke-width="0.5" stroke-dasharray="2,3"/>
  <text x="318" y="170" fill="#4ade80" font-family="DM Sans,sans-serif" font-size="9" font-weight="700">HIGH</text>
  <line x1="257" y1="170" x2="257" y2="178" stroke="#60a5fa" stroke-width="1.5"/>
  <polyline points="257,178 252,182 262,186 252,190 257,194" fill="none" stroke="#8a8272" stroke-width="1.5"/>
  <text x="268" y="197" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="6">↓ GND</text>
</svg>
</div>

----

### How Buttons Work

`digitalRead(pin)` returns `HIGH` or `LOW`.

**Edge detection** — react to a *press*, not a *hold*:

```cpp
static bool lastRed = false;
bool red = digitalRead(22);

if (red && !lastRed) {
    // fresh press — fire once!
}

lastRed = red;
```

`static` keeps `lastRed` alive between calls.

----

### buttons.h

```cpp
#pragma once
#include "Pet.h"

void setupButtons();
void readButtons(Pet& pet);
```

`.h` declares. `.cpp` defines.

----

### buttons.cpp — setup

```cpp
#include <Arduino.h>
#include "buttons.h"

const int PIN_BTN_RED    = 22;
const int PIN_BTN_YELLOW = 21;
const int PIN_BTN_GREEN  = 19;

static bool lastRed    = false;
static bool lastYellow = false;
static bool lastGreen  = false;

void setupButtons() {
    pinMode(PIN_BTN_RED,    INPUT_PULLDOWN);
    pinMode(PIN_BTN_YELLOW, INPUT_PULLDOWN);
    pinMode(PIN_BTN_GREEN,  INPUT_PULLDOWN);
}
```

----

### buttons.cpp — readButtons

```cpp
void readButtons(Pet& pet) {
    bool red    = digitalRead(PIN_BTN_RED);
    bool yellow = digitalRead(PIN_BTN_YELLOW);
    bool green  = digitalRead(PIN_BTN_GREEN);

    if (red && !lastRed) {
        pet.feed();
    }
    if (green && !lastGreen) {
        pet.say(pet.catchphrase());
    }
    // yellow wired in Step 3 → Simon Says

    lastRed    = red;
    lastYellow = yellow;
    lastGreen  = green;
}
```

----

### Update main.cpp

```cpp
#include <Arduino.h>
#include "Pet.h"
#include "buttons.h"

Pet pet;

void setup() {
    Serial.begin(115200);
    pet.begin();
    setupButtons();
}

void loop() {
    readButtons(pet);
    pet.update();
    delay(50);
}
```

----

### Try It

<div style="display:flex;align-items:center;gap:40px;margin-top:16px;">
<div style="flex:1;text-align:left;">
<ul>
<li><strong>Red</strong> — feed your pet ("Yum!", "So full!")</li>
<li><strong>Green</strong> — hear its catchphrase</li>
<li><strong>Yellow</strong> — does nothing yet, wired in Step 3</li>
</ul>
<p style="margin-top:24px;">Buttons firing randomly? You forgot <code>INPUT_PULLDOWN</code>.</p>
</div>
<img src="presentationPhotos/yum.jpeg" style="width:45%;max-height:500px;border-radius:12px;object-fit:contain;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
</div>

----

### ✓ What You Learned

- `digitalRead()` returns HIGH or LOW — the two states of a digital signal
- `INPUT_PULLDOWN` keeps the pin LOW when the button isn't pressed
- Edge detection: compare *current* state to *last* state to fire exactly once per press
- Header/source split: `.h` is the interface, `.cpp` is the implementation

---

## Step 2 — Sound

Give your pet a voice.

----

### PWM — Digital Becomes Sound

<div style="display:flex;align-items:center;gap:32px;margin-top:12px;">
<div style="flex:1;text-align:left;">
<ul>
<li>A digital pin is only <strong>HIGH</strong> (3.3V) or <strong>LOW</strong> (0V)</li>
<li><strong>Frequency</strong> — cycles per second → <em>sound pitch</em></li>
<li><strong>Duty cycle</strong> — % of time HIGH → <em>LED brightness</em></li>
<li>Double the frequency → one octave up</li>
<li><code>analogWrite(pin, 0–255)</code> sets duty cycle</li>
</ul>
</div>
<svg viewBox="0 0 380 265" xmlns="http://www.w3.org/2000/svg" style="width:50%;flex-shrink:0;border-radius:8px;">
  <rect width="380" height="265" fill="#111820" rx="8"/>
  <!-- ═══ SECTION 1: Annotated PWM wave ═══ -->
  <text x="190" y="14" fill="#f5e6c8" font-family="DM Sans,sans-serif" font-size="10" font-weight="700" text-anchor="middle">Pulse Width Modulation (PWM)</text>
  <!-- Voltage reference lines -->
  <line x1="38" y1="27" x2="345" y2="27" stroke="#4ade8020" stroke-width="0.5" stroke-dasharray="3,4"/>
  <line x1="38" y1="65" x2="345" y2="65" stroke="#8a827220" stroke-width="0.5" stroke-dasharray="3,4"/>
  <!-- Y-axis voltage labels -->
  <text x="36" y="31" fill="#4ade80" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">3.3V</text>
  <text x="36" y="68" fill="#8a8272" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="end">0V</text>
  <!-- Shaded ON regions (75% duty cycle) -->
  <rect x="40" y="27" width="113" height="38" fill="#f0a83018" rx="0"/>
  <rect x="190" y="27" width="113" height="38" fill="#f0a83018" rx="0"/>
  <!-- Waveform: 2 cycles, 75% duty cycle, x=40-340 -->
  <polyline points="40,65 40,27 153,27 153,65 190,65 190,27 303,27 303,65 340,65" fill="none" stroke="#f0a830" stroke-width="2.5" stroke-linejoin="miter"/>
  <!-- Duty cycle label inside shaded area -->
  <text x="96" y="49" fill="#f0a830" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="middle">75% duty cycle</text>
  <!-- Period bracket -->
  <line x1="40" y1="77" x2="190" y2="77" stroke="#60a5fa" stroke-width="1"/>
  <line x1="40" y1="73" x2="40" y2="81" stroke="#60a5fa" stroke-width="1"/>
  <line x1="190" y1="73" x2="190" y2="81" stroke="#60a5fa" stroke-width="1"/>
  <text x="115" y="89" fill="#60a5fa" font-family="JetBrains Mono,monospace" font-size="8" text-anchor="middle">period T (= 1 / frequency)</text>
  <!-- Divider -->
  <line x1="10" y1="97" x2="370" y2="97" stroke="#2a3545" stroke-width="1"/>
  <!-- ═══ SECTION 2: Frequency → Pitch ═══ -->
  <text x="190" y="110" fill="#60a5fa" font-family="DM Sans,sans-serif" font-size="10" font-weight="700" text-anchor="middle">frequency → pitch</text>
  <!-- 440 Hz: 3 cycles, 50% duty, cycle=100px -->
  <text x="40" y="119" fill="#60a5fa" font-family="JetBrains Mono,monospace" font-size="8">440 Hz — A4</text>
  <polyline points="40,135 40,121 90,121 90,135 140,135 140,121 190,121 190,135 240,135 240,121 290,121 290,135 340,135" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linejoin="miter"/>
  <!-- 880 Hz: 6 cycles, 50% duty, cycle=50px -->
  <text x="40" y="149" fill="#60a5fa" font-family="JetBrains Mono,monospace" font-size="8">880 Hz — A5</text>
  <polyline points="40,165 40,151 65,151 65,165 90,165 90,151 115,151 115,165 140,165 140,151 165,151 165,165 190,165 190,151 215,151 215,165 240,165 240,151 265,151 265,165 290,165 290,151 315,151 315,165 340,165" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linejoin="miter"/>
  <text x="340" y="129" fill="#8a8272" font-family="DM Sans,sans-serif" font-size="8" text-anchor="end">lower pitch</text>
  <text x="340" y="163" fill="#f5e6c8" font-family="DM Sans,sans-serif" font-size="8" text-anchor="end">higher pitch</text>
  <!-- Divider -->
  <line x1="10" y1="173" x2="370" y2="173" stroke="#2a3545" stroke-width="1"/>
  <!-- ═══ SECTION 3: Duty Cycle → Brightness ═══ -->
  <text x="190" y="187" fill="#f0a830" font-family="DM Sans,sans-serif" font-size="10" font-weight="700" text-anchor="middle">duty cycle → LED brightness</text>
  <!-- 25% duty cycle: 3 cycles, ON=25px, OFF=75px -->
  <text x="40" y="197" fill="#f0a830" font-family="JetBrains Mono,monospace" font-size="8">25% dc</text>
  <polyline points="40,213 40,199 65,199 65,213 140,213 140,199 165,199 165,213 240,213 240,199 265,199 265,213 340,213" fill="none" stroke="#f0a830" stroke-width="2" stroke-linejoin="miter" opacity="0.45"/>
  <text x="342" y="209" fill="#8a8272" font-family="DM Sans,sans-serif" font-size="8">dim</text>
  <!-- 75% duty cycle: 3 cycles, ON=75px, OFF=25px -->
  <text x="40" y="227" fill="#f0a830" font-family="JetBrains Mono,monospace" font-size="8">75% dc</text>
  <polyline points="40,243 40,229 115,229 115,243 140,243 140,229 215,229 215,243 240,243 240,229 315,229 315,243 340,243" fill="none" stroke="#f0a830" stroke-width="2" stroke-linejoin="miter"/>
  <text x="342" y="239" fill="#f5e6c8" font-family="DM Sans,sans-serif" font-size="8">bright</text>
  <!-- Bottom note -->
  <text x="190" y="259" fill="#8a8272" font-family="DM Sans,sans-serif" font-size="8" text-anchor="middle">analogWrite(pin, 0–255) sets duty cycle</text>
</svg>
</div>

----

### tone()

```cpp
tone(pin, frequency, duration);
```

Frequency = pitch. Higher = higher note.

| Note | Hz | Note | Hz |
|------|----|------|----|
| C5 | 523 | G5 | 784 |
| D5 | 587 | A5 | 880 |
| E5 | 659 | B5 | 988 |

A melody is an array of `{freq, duration}` pairs.

----

### sound.h

```cpp
#pragma once
#include "Pet.h"

void setupBuzzer();
void playTone(int freq, int duration);
void playMelody(const int notes[][2], int len);
void chirp(Mood m);
```

----

### sound.cpp — playTone

```cpp
const int PIN_BUZZER = 6;

void setupBuzzer() {
    pinMode(PIN_BUZZER, OUTPUT);
}

void playTone(int freq, int duration) {
    if (freq > 0) {
        tone(PIN_BUZZER, freq, duration);
        delay(duration);
        noTone(PIN_BUZZER);
    } else {
        delay(duration);
    }
}
```

----

### sound.cpp — chirp

```cpp
void chirp(Mood m) {
    switch (m) {
        case Mood::HAPPY:
            playTone(880, 80);
            playTone(988, 80);
            break;
        case Mood::SAD:
            playTone(330, 200);
            playTone(262, 300);
            break;
        default:
            playTone(523, 100);
            break;
    }
}
```

Happy = bright rising chirp. Sad = low falling moan.

----

### Try It

Add `#include "sound.h"` and `setupBuzzer()` to `main.cpp`.

Add `chirp(pet.mood())` after each button action in `buttons.cpp`.

Every press now makes a sound that matches your pet's mood.

**Change the frequencies** — what does 1400 Hz sound like?

----

### ✓ What You Learned

- `tone(pin, freq, ms)` generates a square wave — the simplest form of digital audio
- Frequency maps directly to musical pitch: 440 Hz = A4, double it for the octave above
- A melody is just data: an array of `{frequency, duration}` pairs iterated in a loop
- `switch` on an enum is a clean way to branch on a fixed set of states

---

## Step 3 — LEDs

Light it up.

----

### RGB Color Mixing

One LED, three channels. Mix them digitally:

```
(1, 0, 0) = Red       (1, 1, 0) = Yellow
(0, 1, 0) = Green     (1, 0, 1) = Magenta
(0, 0, 1) = Blue      (1, 1, 1) = White
```

----

### leds.h + leds.cpp

```cpp
// leds.h
#pragma once
void setupLeds();
void setLed(int r, int g, int b);
```

```cpp
void setupLeds() {
    pinMode(PIN_LED_R, OUTPUT);
    pinMode(PIN_LED_G, OUTPUT);
    pinMode(PIN_LED_B, OUTPUT);
}

void setLed(int r, int g, int b) {
    digitalWrite(PIN_LED_R, r);
    digitalWrite(PIN_LED_G, g);
    digitalWrite(PIN_LED_B, b);
}
```

----

### Simon Says

`simon.h` and `simon.cpp` are already in your `src/` folder — no setup needed.

It uses YOUR `setLed()` and `playTone()` to:
1. Flash a color sequence with tones
2. Wait for matching button presses
3. Win = white flash + victory tune. Lose = fail buzz.

Add `#include "simon.h"` to `buttons.cpp`, then add the yellow button action:

```cpp
if (yellow && !lastYellow) {
    int rounds = playSimon();
    if (rounds > 0) {
        for (int i = 0; i < rounds / 2; i++) pet.feed();
        pet.say(String(rounds) + " rounds!");
        playMelody(VICTORY_TUNE, VICTORY_TUNE_LEN);
    } else {
        pet.say("Nope...");
        playTone(200, 300);
    }
}
```

----

### Mood LED Glow

Add to `buttons.cpp` — after any press, glow the pet's mood:

```cpp
switch (pet.mood()) {
    case Mood::HAPPY:
        setLed(0, 1, 0);
        break;
    case Mood::SAD:
        setLed(1, 0, 0);
        break;
    case Mood::DEAD:
        setLed(0, 0, 0);
        break;
    default:
        setLed(1, 1, 0);
        break;
}
```

----

### Try It

- Press any button — LED glows mood colour
- Press yellow — Simon Says starts
- Beat Simon = pet gets fed + victory fanfare

Wrong colours? Check pin wiring — GP16=R, GP17=G, GP18=B.

----

### ✓ What You Learned

- `digitalWrite()` drives an output pin HIGH or LOW — the foundation of hardware control
- An RGB LED is three separate LEDs sharing a common cathode — you control each channel independently
- Reading code you didn't write is a core skill: `playSimon()` uses your `setLed()` and `playTone()` functions
- Physical feedback (light, sound together) makes interactions feel real

---

## Step 4 — Alive!

Your pet has needs now.

----

### millis() — Time Without Blocking

`delay()` freezes everything. `millis()` doesn't:

```cpp
uint32_t start = millis();

while (millis() - start < 3000) {
    // runs for 3 seconds
    // nothing else is frozen
}
```

`uint32_t` because `millis()` returns an unsigned 32-bit value.

----

### game.h + game.cpp

```cpp
// game.h
#pragma once
#include <stdint.h>

int32_t buttonMash(int32_t pin, uint32_t durationMs);
```

```cpp
int32_t buttonMash(int32_t pin, uint32_t durationMs) {
    int32_t  presses = 0;
    bool     lastBtn = digitalRead(pin);
    uint32_t start   = millis();

    while (millis() - start < durationMs) {
        bool btn = digitalRead(pin);
        if (btn && !lastBtn) presses++;
        lastBtn = btn;
        delay(10);
    }
    return presses;
}
```

----

### The Final main.cpp

```cpp
#include <Arduino.h>
#include "Pet.h"
#include "buttons.h"
#include "sound.h"
#include "leds.h"
#include "game.h"

Pet pet;

void setup() {
    Serial.begin(115200);
    Serial.println("Pet alive!");
    pet.begin();
    setupButtons();
    setupBuzzer();
    setupLeds();
    pet.enableDecay();
}
```

`enableDecay()` starts the clock. Stats drop. Your pet is mortal.

----

### loop() — Green Button Mash

```cpp
void loop() {
    static bool lastGreen = false;
    bool green = digitalRead(19);

    if (green && !lastGreen) {
        pet.say("MASH IT!");
        int32_t presses = buttonMash(19, 3000);
        pet.exercise(presses);
    }

    lastGreen = green;
    readButtons(pet);
    pet.update();
    delay(50);
}
```

----

### Try It

- Leave it for 30 seconds — watch the stats drop
- Press green — "MASH IT!" — hit it as fast as you can for 3 seconds
- Feed and water it to keep the stats up

----

### ✓ What You Learned

- `millis()` gives you time without blocking — essential for any responsive embedded program
- `uint32_t` vs `unsigned long`: explicit width types are portable and self-documenting
- `enableDecay()` turns your program into a real-time system — stats change even when you do nothing
- Counting button presses over a time window is a simple but effective game mechanic

---

## Step 5 — Make It Yours

----

### Tune Your Pet

```cpp
PetConfig config;

config.decayRate      = 3;
config.decayInterval  = 5000;
config.feedAmount     = 10;

pet.begin(config);
```

Lower `decayInterval` = harder. Higher `feedAmount` = easier.

----

### Custom Sprites

Give your pet a face. Replace any of the four mood sprites with your own pixel art.

<div style="display:flex;align-items:flex-start;gap:40px;margin-top:12px;">
<div style="flex:1;text-align:left;">

**1.** Install once:
```
pip install pillow
```
**2.** Draw at **piskelapp.com** — free, no sign-in
- Canvas: **120 × 120** pixels
- Black background, bold colors

**3.** Export → PNG → Download

**4.** Run from your project folder:
```
python tools/add_sprite.py ~/Desktop/my_face.png happy
```
Patches `src/sprites.h` automatically — no copy-pasting.

**5.** Upload in VS Code and see it appear.

</div>
<table style="font-size:0.75em;flex-shrink:0;">
<thead><tr><th>Mood</th><th>When it shows</th></tr></thead>
<tbody>
<tr><td>happy</td><td>All stats above 60</td></tr>
<tr><td>okay</td><td>Stats between 40–60</td></tr>
<tr><td>sad</td><td>Any stat below 40</td></tr>
<tr><td>dead</td><td>Any stat hits 0</td></tr>
</tbody>
</table>
</div>

----

### What Now?

You know how to wire hardware, read inputs, drive outputs, and structure C++ across multiple files.

Take what you built and make something new.

A reaction timer. A night light. A noise machine. A door alarm. A two-player game.

**The circuit is yours — you choose what it does next.**

---

## What You Built

- `pinMode` / `digitalRead` / `digitalWrite` — the three verbs of GPIO
- `tone()` — PWM audio: frequency is pitch, duration is rhythm
- RGB colour mixing with `digitalWrite` on three channels
- `millis()` — non-blocking time: the foundation of real-time embedded logic
- Header/source split in C++ — interface vs implementation
- Edge detection — the pattern behind every button in every device

You built a complete interactive embedded device from scratch.

----

### What's Next?

- **WiFi** — Pico W has wireless built in. Connect your pet online.
- **Sensors** — temperature, light, accelerometer — new inputs, same patterns.
- **Multiplayer** — two Picos talking over serial or WiFi.
- **Custom sprites** — draw at piskelapp.com, convert with the included tool.

Take it home.
