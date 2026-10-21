+++
title = "Note: the Performance panel, and why a frame is not a step"
date = 2026-10-21T21:00:00Z
description = "Delivery 12 shows the game's numbers while it runs: frames per second, 1% low, the graphics card's time and more, in the editor and inside the game window. And it answers a good question: is a step the same thing as FPS?"

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*A short note from stage 2, about delivery 12. The numbers are
provisional, measured on my PC.*

When you press Play, you can now see how the game is doing inside. The
editor got the **Performance** panel, a tab beside the Console, and the game
window got a box with the main numbers, which F3 turns on and off. The
delivery was born from a request in the middle of the stage and went ahead
of delivery 7.

{{ <figura src="desempenho-cena.png" alt="Drawing: on the left, a graph of each frame's time, with a dashed line and four spikes; on the right, a row of blue marks, the frames, over a row of fewer green marks, the steps, with the little monkey below." lang="en" has_text={false} /> }}

## A frame is not a step

The first question on seeing the panel was: "would a step be FPS?". It is
not.

- A **frame** is each image that shows up on the screen. How many frames
  come out per second (the *FPS*, frames per second) depends on the monitor
  and the graphics card: 144 on a 144 Hz monitor, 60 on a 60 Hz one.
- A **step** is each time the game's logic runs: walking, jumping,
  colliding. There are always 60 per second, on any PC, and that is what
  makes the game give the same result everywhere.

Between one step and the next, the drawing only smooths the movement. That
is why the panel shows both, and the steps' column is called **Logic**.

## What the panel shows

- **Frames:** the FPS, the time of each frame and the graph of the last
  10 s. And the *1% low*, the average of the slowest 1% of frames: if the
  average is 144 and the 1% low is 60, the game stutters now and then, even
  when it looks fast.
- **Logic:** how much of a step's time, 16.7 ms, the logic uses (a ms is a
  thousandth of a second).
- **Video:** the card, its time to draw a frame and the video memory.
- **Screen:** the resolution, the pixel art scale, the monitor's refresh
  rate and *VSync*, which makes the game wait for the monitor to show each
  frame, with no tearing in the image.
- **Game:** the CPU, the memory and how many draw requests go to the card
  each frame.

A Copy button takes it all, with the version and the card, to paste into a
bug report.

{{ <figura src="desempenho-painel.en.png" alt="The Performance panel, in the tab beside the Console: the graph of each frame's time over the last 10 s and the Frames (144 fps, 1% low 121 fps), Logic (60 steps per second), Video, Screen and Game blocks. At the top, the Also show in the game (F3) switch, the note that the game is stopped and the Copy button." lang="en" caption="The real panel, drawn by the editor, with sample numbers." /> }}

## What the tester found

Measuring must not get in the way. The game measures all of this outside
the logic, measuring costs about 0.04 ms per frame, and the game's result
stays identical with the panel on or off.

Two curiosities. The panel said 61 FPS on a 60 Hz monitor almost half of
the time: the count caught both ends of the last second, and sometimes one
frame too many got in. Now the FPS comes from the average time of each
frame, and the 61 is gone. And, in a short window, the panel's last line was
cut off. Now, when there is not enough height, the graph goes away and the
numbers stay whole.

{{ <figura src="desempenho-f3.en.png" alt="The F3 box in the corner of the game window: 60 fps and 16.7 ms, the 1% low, the logic at 60 steps per second, the GPU time and the CPU, the 1280×720 window at 60 Hz with VSync, and F3 hides at the bottom." lang="en" caption="The F3 box over the game, drawn by the engine in its automation mode, with sample numbers." /> }}

## What comes next

Delivery 7: the game's style (pixel art or HD), the screen scale and the
camera that follows the player.
