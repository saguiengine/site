+++
title = "Stage 2 devlog: pieces and levels"
date = 2026-10-27
description = "Stage 2 gave the engine its pieces, its levels and the files that keep a game, and ended with the first example game: the little monkey walking through a pixel art level, with the camera following."

[extra]
stage = "2"
thumbnail = "meu-jogo-miniatura.png"
thumbnail_has_text = false
+++

*The numbers are provisional: I measured them on my PC, and the official ones
will come from a modest laptop that has not arrived yet. The ones on this
page are from the measurement at the end of the stage and may differ a little
from the posts of each delivery.*

Stage 1 built the foundation of {{ <marca /> }}: the same game on every
computer, drawing, controls, sound, the game in its own window and the
editor's shell. What goes on top of it was still missing. Stage 2 brought the
**pieces**, each thing that exists in a game (the player, a platform, a text),
and the **levels**, the place where the pieces live. It ended with the first
example game.

I make {{ <marca /> }} with the help of Claude, an artificial intelligence: it
writes the code and takes the measurements, and I review, play and decide
what goes in. There were twelve deliveries, told in eight short posts: the
first one covered the first four, and only delivery 11 had no post. This one
puts it all together and tells the review at the end of the stage and what
went wrong.

Three words show up a lot:

- **Step:** the game recomputes the world 60 times per second, always at the
  same pace. Each recomputation is a step (a *tick*).
- **Frame:** each picture drawn on the screen.
- **ms:** a thousandth of a second. At 60 pictures per second, each frame has
  about 16.7 ms to be ready.

## What stage 2 delivered

### The pieces and the tree

The pieces of a level live in a tree: a piece can have pieces inside it (its
*children*), like a car that takes its wheels along when it moves. This tree
shows in the editor in a panel called the **Assembly** (the *scene tree* of
other engines). And the game can be frozen at any step, saved to a file and
carried on from there later, with the same result as if it had never
stopped. For now, that is a testing tool; the game's save comes in stage 11a.
With 5,000 pieces moving, a step takes 0.133 ms, and the limit on the PC is
0.5 ms. [The piece tree](@/devlog/a-arvore-de-pecas/index.en.md) tells more.

### The files

A project is now a folder. The project, each level and each mold are text
files, and each picture, sound and font gets a small card next to it (the
*.meta*). Each piece and each file gets an identity number (an *ID*) that does
not change when the name changes, so nothing gets lost when renaming. A level
of 5,000 pieces opens in 36 ms, and the limit on the PC is half a second.
[How the engine stores a level](@/devlog/como-a-engine-guarda-uma-fase/index.en.md)
explains.

### The molds

A **mold** is a model piece that repeats across the level (a *prefab*): a coin
drawn once becomes a hundred coins, and changing the mold changes all hundred.
A copy can change only what it needs, and a mold can have another one inside
it. The pieces also got the **Active** switch, which turns a piece off
without deleting it.
[Molds, copies and the Active switch](@/devlog/moldes-e-o-interruptor-ativa/index.en.md).

### The image, the camera and the text

The project picks its style, *pixel art* (drawing made of visible little
squares) or HD (high resolution, with smooth drawing), and a way for the
image to fit any screen. The **Camera** follows the player and stops at the
edges of the level.
[The image that fits any screen](@/devlog/a-escala-e-a-camera/index.en.md).
The game also got the **Text** piece, which shows phrases in the player's
language, with a pixel art font kept in the project itself.
[The game's text](@/devlog/o-texto-do-jogo/index.en.md).

### The Performance panel

The editor got a panel that shows, while the game runs, how many pictures per
second the game shows, how long each frame takes and how much of it goes to
the logic and to the graphics card; and the game got a summary in its own
window, with the F3 key. Measuring costs 0.018 ms per frame, and the limit on
the PC is 0.05 ms.
[The Performance panel](@/devlog/o-painel-desempenho/index.en.md).

### The editor opens the project

The editor opens a project and shows the Assembly and the files. For now, it
is only for looking: editing comes in stage 5. From the start of the program
until the Assembly shows up takes half a second, and the limit on the PC is
1.5 seconds.
[The editor opens the project](@/devlog/o-editor-abre-o-projeto/index.en.md).

{{ <figura src="editor-projeto.en.png" alt="The editor in English with the test project open. The project's own names (Câmera, Jogador, Chão, Moedas, Nuvem, Placa) are in Portuguese, because the project was written in Portuguese; the editor's words are in English. The tree of the level level1 in the Assembly, with the camera, the player, the floor, three coins, a cloud turned off and the sign, and the Files with the six categories and how many files each one has" lang="en" has_text={true} /> }}

### The first example game

**Meu Jogo** ("My Game", in Portuguese) is a pixel art level three screens
wide. The little monkey walks through the level, between the grass floor and
the plank platforms (for now in any direction, even through the air, because
there is no gravity yet), and the camera follows it to the end of the level.
The sign at the start speaks the player's language. The game shows its first
frame 0.6 seconds after opening, and the limit on the PC is 0.75 seconds; 99%
of the frames are ready in under 3 ms.
[The first example game](@/devlog/o-primeiro-jogo-de-exemplo/index.en.md).

{{ <figura src="meu-jogo-600.en.png" alt="The start of Meu Jogo: the little monkey on the grass floor, under a wooden sign that says Use the arrow keys to walk, with plank platforms, clouds and the background of mountains and hills" lang="en" has_text={true} /> }}

### And the tidying up

Three deliveries were tidying up. The first made the editor match the drawing
of its screens (the *mockup*), with the fixes the review of stages 0 and 1
asked for, and the logo became the little monkey's face in pixel art. The
second made the report of each delivery say, for each criterion, the measured
value, the limit and the margin, and not just "passed".
[The piece tree](@/devlog/a-arvore-de-pecas/index.en.md) tells both. The third
tidied up the automatic tests and brought to my PC the part of the robot that
runs the tests on every change (the *continuous integration*, or *CI*) that
still ran in the cloud. The reason is in "What went wrong", further down.

## The review at the end of the stage

Before starting stage 3, I stopped to review the whole of stage 2. An
auditor, an artificial intelligence like Claude, compared the plan with
itself and then with the code and with the mockup. It found things like a
decision I had made that was not written in the plan, and texts that still
described the old way. Out of the review came:

- the plan, the texts and the code lined up;
- the measured numbers of the twelve deliveries kept together with the code;
- two new working rules: every change to the code goes through the tester,
  the checker who took no part in the work (text-only changes do not), and a
  decision of mine goes into the plan on the same day;
- the plan redone with the real time of stage 2, which was much faster than I
  expected, because almost all of it was the foundation on the inside, which
  does not need to be played to be approved. The next stages depend on me
  playing and adjusting, and that does not speed up the same way.

## What went wrong (and how I fixed it)

- **The cloud minutes ran out.** Part of the automatic tests, the Linux ones
  and the browser ones, ran on GitHub's computers, in the cloud, with a quota
  of minutes per month, and October's quota ran out on the 25th. Instead of
  paying more, that part came to my PC, which already ran the Windows ones, in
  a Linux that runs inside Windows (*WSL*), kept apart from it: the code
  of the tests cannot reach Windows' files, graphics card or programs. Now the
  tests cost nothing and take 7 to 10 minutes.
- **The PC froze during the tests.** With the Linux tests and the Windows
  tests running at the same time, the memory ran out: 0.1 GB was left. I put a
  ceiling on Linux's memory and fewer tasks at the same time, and at the
  worst moment almost 8 GB are left now.
- **The power went out.** It went out in the middle of a test and damaged a
  few files of the version history (*Git*) in the folder where Linux runs
  the tests. I deleted only the damaged ones, without losing the rest, and the
  step by step is written down for next time.

## What is left

- **The laptop:** the official numbers of stages 0, 1 and 2.
- **The list of what to draw:** with 5,000 pieces, building on each frame the
  list of what goes to the screen takes 0.78 ms, above the limit on the PC
  (0.5 ms). That number is only noted, without failing, but stage 3 will take
  care of it, right in its spec.
- **Targets too loose:** three targets had more than 80% to spare. In the next
  stages, the limits will be closer to what was measured, with a margin, so
  that a slowdown shows up.

With that, stage 2 is closed. Stage 3 brings physics: gravity, collisions and
the real jump. The little monkey, which so far only walks, is going to jump.
