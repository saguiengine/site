+++
title = "Tidying up before the physics"
date = 2026-11-02
description = "Delivery 1 of stage 3 changes nothing on the screen: it takes care of 16 small items left from stage 2 and gets the engine ready for physics, with a lock against the wrong order of the pieces and the new version."

[extra]
delivery_stage = "3"
deliveries = [1]
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*A short post from stage 3, about delivery 1. The times are provisional,
measured on my PC.*

Stage 3 brings physics, but its first delivery changes nothing on the
screen. It tidies up: 16 small items that the checks of stage 2 left on
a card on GitHub (an *issue*), and the groundwork for physics.

## A lock against the wrong order

The engine keeps the pieces as in a parking lot, which programmers call an
*arena*: a space that is freed goes to the next piece that arrives.

The game moves in the order of the piece tree, the Assembly's (or by
priority, when someone sets one): an order you can see in the editor, and
one that does not change when a piece leaves and another arrives. If physics
received the pieces in the order of the spaces, the result would depend on
an order nobody can see.

Now the automatic code checker (the *linter*) refuses any new use of the
order of the spaces. The six places where that order is right carry
their reason in writing.

{{ <figura src="arena-ordem.png" alt="Drawing: on the left, a row of four spaces: a coin, an empty space, a platform and the little monkey, with a dashed red arrow and an X below; on the right, the piece tree, with a folder at the top and the little monkey, a coin and a platform hanging from it, with a green arrow and a check mark below." lang="en" caption="The order that counts is the piece tree's, not the spaces'." has_text={false} /> }}

## The square goes, the version goes up

Stage 1's test square, which only the tests and a measurement use, lived in
the engine's core. Now it sits behind a switch that only they turn on (a
*feature*), out of the program that reaches players. Stage
1's reference *hashes*, the game's fingerprints, stayed the same, at 60 and
120 steps per second, on the computer and in *WebAssembly*, the program
format of browsers.

The internal version is now 0.3.0-dev ("dev" for development). A state
saved by 0.2 (a snapshot of the game at a step) is
refused, and a game recorded by 0.2 (a *replay*) still runs, with a warning
that the result may change.

## Clearer errors

A level with a typo, like the extra comma in `format: 1,,`, gave two
warnings: the right one, SE0004, with the line and the column (line 2,
column 15), and a wrong one, SE0007, as if the file could not be read.
Now only SE0004 shows up, in the editor and in the game.

Four of the project's commands did not point out a misspelled option:
`prova 1 --hashes-onyl` ("proof"), for example, ignored the misspelled option
and ran all of proof 1 instead of only its hashes. Now they stop and say
which option they did not understand.

## Faster GIFs

The GIFs in this devlog come from a tool that plays back a replay and
puts its frames together. Putting together the
1,800 frames of a GIF, once the game has taken the pictures, took 203 s and
now takes 63 s, about 3.2 times faster. And a test keeps the hash of two
small GIFs, the same on Windows and on Linux: if a new version of the GIF
library changes a single byte, the test fails.

## The acceptance check that miscounted

Each delivery has an **acceptance check**, a command that checks the
criteria of the specification (the *spec*) by counting each one's tests
by name. In this delivery, two tests with the same name, one in the
editor and one in the game, became one in the count. Now the
acceptance check refuses a repeated name in a criterion; in stages 1 and 2,
it found none.

Of this delivery's 20 criteria, the 14 that the acceptance check covers
passed, with 29 tests. In all, 871 tests pass, and 297 in WebAssembly.

## What comes next

Delivery 2 puts in one place what runs at every step, so the window and
the tests use the same code. Physics starts in delivery 4.
