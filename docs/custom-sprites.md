# Custom Sprites

Give your Tamagotchi a face! You can replace any of the four mood sprites with your own pixel art in four steps.

---

## Step 1 — Install the converter (once only)

```bash
pip install pillow
```

---

## Step 2 — Draw your sprite

Go to **[piskelapp.com](https://www.piskelapp.com)** (free, browser-based, no sign-in needed).

1. Click **Create Sprite**
2. Set the canvas to **120 × 120** pixels
   *(Resize panel: top-right → enter 120 / 120)*
3. Draw your character

**Tips:**
- Use a black background — the screen background is black
- Bold, simple shapes look best at 120px
- You can use as many colours as you like
- Don't worry about being perfect — you can re-run the script as many times as you want

---

## Step 3 — Export as PNG

In Piskel: **Export → PNG → Download**

Save the file somewhere easy to find, e.g. your Desktop.

---

## Step 4 — Add it to your project

Open a terminal in the **project root folder** and run:

```bash
python tools/add_sprite.py ~/Desktop/my_face.png happy
```

Replace `happy` with whichever mood you want to change:

| Mood | When it shows |
|------|--------------|
| `happy` | All stats above 60 |
| `okay` | Stats between 40–60 |
| `sad` | Any stat below 40 |
| `dead` | Any stat hits 0 |

The script patches `src/sprites.h` automatically — no copy-pasting.

---

## Step 5 — Upload and see it

Hit **Upload** in VS Code (or run `pio run -t upload`) and your sprite appears on screen.

If you want to replace more moods, repeat steps 2–5 for each one.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: PIL` | Run `pip install pillow` |
| `sprites.h not found` | Make sure you're running the command from the project root folder (the one containing `platformio.ini`) |
| Sprite looks stretched | Your canvas wasn't 120×120 in Piskel — the script resizes automatically but odd aspect ratios look squashed |
| Colours look wrong on screen | RGB565 has lower colour depth than a normal screen. Bright, saturated colours work best |
