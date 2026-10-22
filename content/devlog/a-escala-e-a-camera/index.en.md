+++
title = "Note: the image that fits any screen, and the camera that follows"
date = 2026-10-22
description = "Delivery 7 decides how the game shows up in a window of any size, from a laptop to an ultrawide monitor, and brings the camera that follows the player. All without changing the game's result."

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*A short note from stage 2, about delivery 7. The numbers are provisional,
measured on my PC.*

A pixel art game is drawn small: in {{ <marca /> }}, 640 × 360 pixels, the
**base resolution**. But nobody plays in a window that size. The screen can
be 1366 × 768, 1920 × 1080 or an ultrawide monitor of 2560 × 1080. Delivery
7 decides how the image grows in each case, and brings the camera that
follows the player.

## Two styles

The project picks a **style**. In **pixel art**, the base is 640 × 360 and
the images are never smoothed: each pixel stays a crisp little square. In
**HD**, the base is 1920 × 1080 and the images are smoothed when they grow or
shrink. The style also gives the starting values of the camera and the
scale.

## Four ways to fit the screen

- **Pixel perfect:** it only grows by whole numbers, ×2 or ×3, and fills the
  rest with black bars (the *letterbox*). The pixels stay perfect. It is
  pixel art's default.
- **Fit:** it grows as much as fits without distorting, with bars on one
  side only. It is HD's default.
- **Expand:** no bars: a wider window shows more of the world at the sides.
- **Stretch:** it fills everything, even if it distorts.

{{ <figura src="escala-modos.png" alt="Two captures of a delivery 7 test in a 1366 × 768 window, with a checkered floor and a white square: on the left, pixel perfect, with the game at ×2 and a black frame around it; on the right, fit, with the game at ×2.13 filling almost the whole window." lang="en" caption="A real delivery 7 test, drawn by the engine: pixel perfect and fit." has_text={false} /> }}

In fit, 1366 × 768 gives a broken scale: ×2.13. Growing a pixel 2.13 times
would make it crooked, with some pixels wider than others. The trick is to
grow it ×3, still crisp, and then shrink it to the window's size with a
smooth filter. Up close, the edge stays straight, with just a thin
transition line.

{{ <figura src="escala-borda.png" alt="The corner of the white square in fit at ×2.13, enlarged: the edges are straight, with just a thin line of lighter green between the square and the floor." lang="en" caption="The square's corner at ×2.13, enlarged." has_text={false} /> }}

## The camera that follows

The **Camera** is a piece that follows the player. You can set:

- the **smoothing**: 0 keeps the camera stuck to the player; 0.9 makes it
  arrive little by little, and after half a second 4% of the way is left;
- the **limits**, a rectangle the camera does not pass, so nobody sees past
  the edge of the level;
- the ***zoom***, whole in pixel art, so the pixels do not get crooked, or
  smooth, as an option.

The *dead zone*, an area where the player walks without the camera moving,
and the *look-ahead*, the camera looking a little ahead, are already in the
file format. They start working in stage 3, with real movement.

Inside, the game's logic always uses the base resolution. The drawing
changes with the window, and the game does not. A *replay*, the recorded
match, drawn in the four modes and in four window sizes, gave the same
*hash*, the "fingerprint" of the game's state, in all of them.

## What the tester found

The tester, the checker who took no part in the work, went through the
delivery three times. The tester found a fixed sky that vanished when the
smooth zoom was on, and a rare rounding case that closed the game, and also
saw that, in expand, the wide monitor showed a piece beyond the camera's
limit. All three were fixed, each with a test that failed before.

## What comes next

Delivery 8: the text inside the game, and the languages.
