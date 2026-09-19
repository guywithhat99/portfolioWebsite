<p class="modnum">Module 10</p>

# Inside a chip

----

## A sensor is a block of numbered bytes

Each one holds a single byte and has a number.

They are called **registers**. Some hold readings the chip keeps updating, some hold settings you write.

<p class="big">That is the whole model.</p>

----

## The numbers look strange

Everything in a datasheet is written in **hex**, marked with `0x`.

| Written | Is |
|---|---|
| `0x0A` | 10 |
| `0x76` | 118 |
| `0xD0` | 208 |
| `0xFF` | 255 |

<p class="sub">Digits run 0 to 9, then A to F for 10 to 15.</p>

----

## Why not just decimal

<img src="content/img/hex-byte.svg" alt="One byte splits into two groups of four bits, each written as one hex digit" style="max-height:400px">

----

### The useful part

<div class="two">
<div>

Every byte is <strong>exactly two hex digits</strong>. No more, no less.

<code>0x00</code> is the smallest, <code>0xFF</code> is the largest.

</div>
<div style="font-size:.9em">

Each digit maps to four bits, so you can read a bit pattern straight off the number once you know the sixteen.

<p class="sub">In decimal, 255 is three digits and 10 is two. Nothing lines up.</p>

</div>
</div>

----

## The makers publish the layout

<a href="datasheets/BMP280-datasheet-rev1.26.pdf">BMP280 datasheet, revision 1.26</a>

Section 4.2, Table 18.

<p class="sub">Opens in a new tab.</p>

----

## This is it

<img src="content/img/ds-memory-map.png" alt="Table 18 from the BMP280 datasheet, the memory map" style="max-height:470px">

<p class="sub">Bosch Sensortec, BMP280 data sheet, Table 18.</p>

----

## How to read it

<div class="board">
<img src="content/img/ds-memory-map.png" alt="Table 18 from the BMP280 datasheet, the memory map" style="max-height:372px">
</div>

<div class="two" style="margin-top:.5em">
<div>

| Column | Means |
|---|---|
| <strong>Register Name</strong> | what the makers call it |
| <strong>Address</strong> | the register number |
| <strong>bit7 to bit0</strong> | what each bit is for |
| <strong>Reset state</strong> | value at power-on |

</div>
<div style="font-size:.86em">

The colours are the datasheet's own key, printed under the table.

They mark each register as <strong>read only</strong>, <strong>read and write</strong>, or one to <strong>not write to at all</strong>.

</div>
</div>

----

## The row called `id`

<div class="board">
<img src="content/img/ds-memory-map.png" alt="Table 18 from the BMP280 datasheet, the memory map" style="max-height:372px">
<div class="hl ring" style="left:0.8%;top:64.3%;width:97.4%;height:4.4%"></div>
</div>

<div class="two" style="margin-top:.6em">
<div>

Address <code>0xD0</code>

Contents <code>chip_id[7:0]</code>

Reset state <code>0x58</code>

</div>
<div style="font-size:.86em">

<div class="box kit">
<span class="lbl">Reading a datasheet</span>
One row gives a register's number, what is in it, and what value to expect.
</div>

</div>
</div>

----

## Where the readings live

<div class="board">
<img src="content/img/ds-memory-map.png" alt="Table 18 from the BMP280 datasheet, the memory map" style="max-height:372px">
<div class="hl ring" style="left:0.8%;top:20.9%;width:97.4%;height:25.9%"></div>
</div>

<div class="two" style="margin-top:.6em">
<div>

| Registers | Holds |
|---|---|
| <code>0xF7</code> to <code>0xF9</code> | latest pressure |
| <code>0xFA</code> to <code>0xFC</code> | latest temperature |

</div>
<div style="font-size:.86em">

Three registers for one reading, because the value is 20 bits and a register only holds 8.

<p class="sub">Look at the <code>xlsb</code> rows on the table: only the top four bits are used, and the rest are zero.</p>

</div>
</div>

----

## Where the settings live

<div class="board">
<img src="content/img/ds-memory-map.png" alt="Table 18 from the BMP280 datasheet, the memory map" style="max-height:372px">
<div class="hl ring" style="left:0.8%;top:46.8%;width:97.4%;height:8.9%"></div>
</div>

<div class="two" style="margin-top:.6em">
<div>

| Register | Controls |
|---|---|
| <code>0xF4</code> | how it measures, and whether it is running |
| <code>0xF5</code> | filtering and timing |

</div>
<div style="font-size:.86em">

These two you write to.

On the table those rows carry several named fields across the bit columns, rather than one value. One register, several separate settings.

</div>
</div>

----

## Two kinds of address

<img src="content/img/two-addresses.svg" alt="0x76 selects the chip on the bus; 0xD0 selects a register inside it">

----

### The difference

<div class="two">
<div>

<h4><code>0x76</code></h4>

Which chip is being spoken to.

Set by the hardware, by that resistor on the board.

</div>
<div>

<h4><code>0xD0</code></h4>

Which register inside that chip.

Set by the chip's designers, listed in Table 18.

</div>
</div>

<p class="sub">Both are hex, both are one byte, and they mean completely different things.</p>

----

## What you now know

| | |
|---|---|
| Register | One numbered byte inside a chip |
| Memory map | The table of all of them |
| Reset state | What a register holds at power-on |
| `0xF7` onwards | Readings, written by the chip |
| `0xF4`, `0xF5` | Settings, written by you |
| Device address | Which chip |
| Register address | Which register inside it |
