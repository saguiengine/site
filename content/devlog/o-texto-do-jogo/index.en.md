+++
title = "Note: the game's text, in the player's language"
date = 2026-10-22T21:00:00Z
description = "Delivery 8 brings the Text piece and the game's languages: signs and phrases that show up in the player's language, with the same letters on any computer."

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*A short note from stage 2, about delivery 8.*

Until now, the game's pieces only showed images. Delivery 8 brings the
**Text** piece: a sign, a score, a message on the screen. And it brings the
game's languages, so each phrase shows up in the player's language.

## A key for each phrase

The Text piece does not keep the phrase, but a **key**: a name that stays
the same in every language, like `level1.sign.text`. Each language's phrase lives in a
separate file, one per language, in *Fluent*, a file format for
translations. In the file, the key's dot becomes a hyphen:

```
# pt-BR.ftl
level1-sign-text = Use as setas para andar

# en.ftl
level1-sign-text = Use the arrow keys to walk
```

For a text that is the same in every language, like the game's name, the
piece has the **Do not translate** box, and the phrase stays in the piece
itself.

## Which language shows up

The first time, the language of the player's system (in the browser, the
browser's). If the game does not have that language, it follows a **chain of
fallbacks** (each *fallback* is a language to fall back on) that the project
sets, for example from pt-PT (Portugal) to pt-BR (Brazil), until it
reaches the language the game was written in. A phrase never shows up blank: what is missing in one
language comes from the next.

A key that exists in no language shows up on the screen in brackets, like
`[level1.sign.text]`, and the game warns once in its record of events (the
*log*). A typo in a language's file is reported with the line and the
column, and the other phrases still work.

## The same letters on every computer

The game never uses the fonts installed on the computer. The engine draws
TTF and OTF fonts, the common font files, and *bitmap* fonts: a PNG with the
letters in a grid, common in *pixel art* (art made of visible little
squares). The letters the processor builds come out identical, down to the
last byte, on Windows, Linux and macOS. The project's own fonts reach the
game in delivery 10.

In pixel art, the edges of the letters are not smoothed (no *antialiasing*):
each pixel is either on or off. In HD, the high-resolution style, TTF and
OTF letters come out smooth.

{{ <figura src="texto-pixel.png" alt="A delivery 8 test in pixel art, with a bitmap font and text in Portuguese: at the top, the phrase Ação, você e à toa: 1.516!; in the middle, the words ação, você and à, one under the other, aligned on the same point by their start, center and end; at the bottom, the phrase Use as setas para andar e o espaço para pular à vontade, twice, wrapped into four lines: on the left, aligned at the start; on the right, at the end." lang="en" caption="A real delivery 8 test: accents, line wrapping and alignments (the text in the image is in Portuguese)." has_text={true} /> }}

## The font that comes from the style

A Text with no font chosen uses the font of the project's style: IBM Plex
Sans in HD and monogram in pixel art. The monogram font is by datagoblin
(Vinícius Menézio) and has a CC0 license, free to use.

The monogram font came in because of something the tester, the checker who
took no part in the work, found: in the first review, Plex, small and
unsmoothed, came out broken in pixel art.

{{ <figura src="texto-antes-depois.png" alt="The phrase Vidas: 3 (Lives: 3, in Portuguese), in red over the green floor of a test, enlarged, side by side: on the left, in small Plex, with broken, crooked letters; on the right, in monogram, with straight, crisp letters." lang="en" caption="The same score in Plex (left) and in monogram (right); the text in the image is in Portuguese." has_text={true} /> }}

The monogram font lacks 20 letters of the Cyrillic alphabet used in Serbian,
Macedonian and Belarusian. In the default font, those letters come from
Plex, at the same size and unsmoothed, and none of them shows up as an empty
box.

## What the tester found

The tester also saw that the automatic tests used the computer's language,
so a test run could come out differently on my PC and in the cloud. Now
the tests use the language the game was written in, unless a test asks for
another. And the tester found that, with the language written `pt-br` in the
project, Linux, which treats capital and lowercase letters as different, did
not find the file `pt-BR.ftl`, and nothing warned about it. Both were fixed,
each with a test.

## What comes next

Delivery 9: the editor opening the project, only to view the level's pieces
and the files.
