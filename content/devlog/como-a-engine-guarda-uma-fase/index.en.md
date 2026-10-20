+++
title = "Note: how the engine stores a level"
date = 2026-10-19
description = "A level of the game now lives in a text file you can read and fix by hand. A short note on the format, the molds, the IDs that do not break and the reader that opens a level of 5,000 pieces in 31 ms."

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*A short note from stage 2. The numbers are provisional, measured on my PC.*

A level of the game, with the scenery, the player, the coins and the
platforms, now lives in a text file. You can open it in any text editor and
read it:

```
(
    id: "c7570ac327c0a56d",
    parent: "1609cf0f2a5575bc",
    type: "sprite",
    name: "Chão",
    props: (
        position: (0.0, 320.0),
        scale: (20.0, 1.0),
        tags: ["ground"],
    ),
),
```

Each piece is a block: an ID (a code that identifies the piece and never
changes), its parent, its type, the name shown in the editor and only the
properties that differ from the default. The format is called RON (*Rusty
Object Notation*), a cousin of JSON, the most used text format for storing
data, made for Rust, the language the engine is written in.

Why text, and not a binary file that only a program can read? Because you
can see what changed from one version to the next in Git, the system that
keeps the project's history (the *diff*), put together the work of two
people (the *merge*) and fix things by hand when something goes wrong.

## Molds

The player is not described inside the level. It is in a **mold** (the
*prefab* of other engines), the file `player.mold`. The level only says
"a copy of the player's mold goes here, at this position". Change the mold,
and every copy changes. The next delivery brings variants and molds inside
molds.

## IDs that do not break

Each image and each sound gets a `.meta` file next to it, with a permanent ID
and a fingerprint of its content (a *hash*). If you rename or move
`player.png`, the engine finds the `.meta` again by the content, and the
levels keep pointing to the right image. If the same file shows up in two
places, the one with the shortest path keeps the ID, and the other gets a
warning.

## Nothing disappears

If a level has a property this version does not know, written by hand or
coming from a newer version, the engine warns and keeps the line as it came.
Opening and saving never deletes what it does not understand.

## Our own reader

The RON library we used, ready-made code by other people that reads this
format, got slow with large levels. To read values with no fixed type, it
searched for a piece of text in the rest of the file at every number: the
larger the file, the slower each read. With 5,000 pieces, opening the level
took 1.1 s. The goal is half a second on my PC and one second on the modest
reference laptop.

So we wrote our own reader (a *parser*), only for levels and molds, that
goes through the text once. The same level opens in **31 ms** (a ms is a
thousandth of a second), about 35 times faster. The slowness has already
been fixed in the library's code, but the fix has not come out in a release
yet. And our reader stays useful anyway: it keeps details the library loses,
like the difference between a list and a pair of values.

A new reader is a new place for bugs, so it was put to the test against the
library: more than 3 million random texts and files broken on purpose (the
technique is called *fuzzing*), without hanging or crashing once. In a typo,
it points to the same place as the library in 87% of the cases. And a level
with 100,000 groups, one inside the other, opens in 0.3 s.

## What comes next

Molds with variants and molds inside molds, still in stage 2.
