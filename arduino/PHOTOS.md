# Images needed

You are sourcing these. Every one has a placeholder already sized and positioned
in the deck, so dropping a file in is the only work.

## How to drop one in

Put the file in `content/img/`, then replace the placeholder block with:

```html
<img src="content/img/your-file.jpg" alt="...">
```

## The board image

One top-down photo of an Uno is reused across several slides, with different
parts highlighted each time. Source it once and it serves all of them.

The highlight boxes are positioned in percentages of the image, so they follow
the image whatever size it is. After dropping the real image in, the percentages
will need nudging to line up with the actual pin headers. They are inline on each
slide and look like this:

```html
<div class="hl t" style="left:41%;top:4%;width:7%;height:13%"></div>
<div class="hltag t" style="left:38%;top:-7%">pin 13</div>
```

`hl` is the box, `hltag` is the label. Add `t` for teal, `g` for green, `r` for
red, or leave it off for orange.

A flat top-down shot works best. Angled photos make the highlight boxes sit wrong.

## Full list


### 01-setup.md

- **SCREENSHOT**: Arduino IDE 2.x just opened, empty sketch visible. Full window.
- **PHOTO**: Uno powered on, green ON LED clearly lit, USB cable attached.
- **SCREENSHOT**: Tools → Board menu open, Arduino Uno highlighted. Cropped to the menu.
- **SCREENSHOT**: IDE toolbar, cropped tight, Upload arrow clearly visible.

### 02-blink.md

- **IMAGE**: Top-down Arduino Uno, whole board, filling the frame. Reused on later slides with different parts highlighted.
- **IMAGE**: Same board image.

## Still to come

Later modules will need wiring diagrams for the breadboard circuits. Those are
schematic, so I will draw them rather than adding them to this list.