+++
title = "Devlog: a pause to replan"
date = 2026-10-17
description = "Before building the pieces, I stopped to compare the engine with Godot, Unity and GameMaker. A bigger plan came out of it: what gets better, what stays out of 1.0 and what the architecture leaves ready for later."
+++

*The numbers are provisional: I measured them on my PC, and the official ones
will come from a modest laptop that has not arrived yet.*

Stage 2 started on October 16. It is the stage of pieces and levels: the
things that exist in the game (the player, a coin, a platform) and the
levels of the game, saved to files. It is the first stage in which the game
stops being a lone square. The next day, before writing the first piece, I
stopped everything.

The reason was a simple question: what can Godot, an open-source engine
widely used for 2D games, do that {{ <marca /> }} cannot? I downloaded Godot,
started comparing, and the list grew fast. Several answers depended on
decisions that get expensive to change later. For example: how each piece
keeps its data, how the game saves its own state, how {{ <linguagem /> }}
talks to the engine. Changing that in stage 2 costs days. Changing it in
stage 8, with the editor, the sound and the lighting built on top, costs
redoing half of what already exists.

So the rule became this: everything Godot does in 2D has to be possible in
{{ <marca /> }}. "Possible" can mean one of four things:

- **ready-made:** it already comes with the engine, and you just turn it on
  (a camera that follows the player);
- **by script:** you write a few lines of {{ <linguagem /> }} (an enemy that
  runs away when its health is low);
- **by package:** someone bundles ready-made pieces, scripts and images, and
  you install it in your project (a dialogue system);
- **by module:** a chunk of fast code, written in another language, for the
  heavy math (a simulation of thousands of grains of sand).

Whatever needs a new part of the engine goes into the roadmap, with a date.
What stays out stays out on purpose, with the reason written down.

## How the review went

I make {{ <marca /> }} with the help of Claude, an artificial intelligence.
During the review, it worked on several fronts at once: comparing, measuring
and checking. I read the reports and decided.

### Three engines, item by item

I compared Godot, the 2D side of Unity and GameMaker with the plan for
{{ <marca /> }}. Each line of the comparison is a feature, that is, something
the engine does: "the camera follows the player", "import art from another
program", "a joint that holds two pieces together". After merging what the
three said about the same thing, there were about 340 features. For each
one, the table says what {{ <marca /> }} already has, what is missing and in
which stage it comes.

### Measure before deciding

When the doubt was about speed, Claude wrote small test programs, only to
measure, and threw them away afterwards. There were six questions:

- **How many times per second the game should recompute the world.** Today
  it is 60 steps per second. More steps make the controls quicker, but they
  cost more. The measurements still depend on a test of mine: playing
  without knowing which rate is on, and giving it a score.
- **How much a noise effect written in script costs.** Noise, here, is not
  sound: it is smooth randomness. Instead of numbers that jump around at
  random, it gives values that change little by little, like the outline of
  hills. It is used to create things automatically. In a game with caves
  that change on every run, the noise decides where there is rock and where
  there is a passage. It also works for clouds, terrain and the natural shake
  of a camera.
- **How much it costs to draw thousands of images.** The game's images are
  packed into big sheets, the pages, so the graphics card can draw many of
  them at once. The measurement showed a way to draw everything in one go,
  even when the images come from different pages.
- **How much it costs to save and restore the whole game.** That is what
  allows saving at any moment, going back in time and, one day, playing
  online.
- **How much it costs for {{ <linguagem /> }} to read and change 5,000
  pieces** on every step, as in a game full of enemies, coins and
  projectiles.
- **The same result everywhere.** A recorded match, with the buttons pressed
  on each step, gave exactly the same numbers on Windows, on Linux, in the
  browser and on a Mac. That is what makes it possible to watch a match again
  and to find a bug by repeating the same moves.

### Decisions in rounds

There were three rounds of questions, with about 150 decisions. The ones
only I could make came one by one. The technical ones came in blocks, after
I read the reason for each. Then, three checks looked for contradictions
between the plan, the code and the screen designs.

## What gets better

### In physics

- **Joints:** a pin, a spring or a rope holding two pieces together. With
  them, you can make a plank bridge that sways when the player walks across,
  a ball on a chain, or a little cart with wheels that turn. Before, joints
  were planned for after 1.0, because I thought they needed their own editor.
  Godot showed they do not: a joint is a piece that connects two others, and
  the spot where it sits is the pivot.
- **More than one shape per piece.** For example, the player's body to bump
  into walls and a small sensor at the feet to know whether the player is on
  the ground.
- **Zones that push:** a gust of wind that throws the player sideways, water
  that pulls upward, a conveyor belt that carries the boxes.
- **Paths:** a platform that goes back and forth along a route drawn in the
  level, with no script.
- **Questions about space:** "what is inside this circle?" (an explosion that
  hits everything around it) or "what does this line hit first?" (can the
  enemy see the player, or is there a wall in between?).

### In drawing

- **Ready-made effects, without writing a shader.** A shader is a tiny
  program that runs on the graphics card and decides the color of each pixel.
  In other engines, almost every effect means writing one. In
  {{ <marca /> }} 1.0, the most common ones come ready:
  - the player flashes red when taking damage;
  - the defeated enemy vanishes, crumbling into bits;
  - the chosen piece gets an outline;
  - the game turns gray while paused;
  - lights add up, instead of covering what is behind them.
- **A better camera.** It gets a dead zone: the character walks a little
  without the camera moving, and the screen stays calmer. And it gets
  look-ahead: when the character runs, the camera looks a little ahead, so
  the player sees the hole before falling into it.
- **Aseprite art.** Aseprite is a program widely used to draw pixel art. Its
  files go straight in, with their layers and animations, without exporting
  image by image.

### In the editor

- **Select by clicking in the running game, pause and move forward one step
  at a time.** If an enemy falls through the floor once in a while, you can
  pause at that moment, move forward step by step, click it and see its
  values.
- **A command palette:** a shortcut opens a box, you type "duplicate" and
  pick "Duplicate piece". It works for any action in the editor, and it helps
  a lot if you prefer the keyboard.
- **A floating panel:** you can take a panel out of its place, like the one
  with the messages, and leave it floating over the level.
- **Undo for everything,** even for the pixel brush and the tile brush (tiles
  are the square bits that build the scenery).
- **"If" in Reactions.** Reactions are ready-made sentences for people who do
  not program yet, like "when the player touches the coin, remove the coin and
  add 1 point". Now they accept a simple condition: "if the player has the
  key, open the door" or "if the coins reach 10, play the victory music".

### In {{ <linguagem /> }}

- **Functions as values.** You can hand over an action to be done later:
  `after(1, explode)` means "1 second from now, explode". And `lambda`
  arrives: a short function written on the spot, with no name, like the one
  in Python. `sort(enemies, key=lambda e: e.hp)` sorts the enemies by health.
  People who already program miss this right away.
- **More access to the game:** the mouse; asking whether the piece is on the
  ground or touching a wall; rays (the line that asks what it hits); and
  force and impulse on loose pieces, like a steady push of wind or the blow of
  an explosion.
- **An enemy that already patrols and chases,** without writing anything: it
  walks back and forth, turns around at the edge and runs after the player
  when it sees them.
- **The shortest path,** ready and fast: on a tile map, the enemy finds its
  way to the player around the walls, as in a maze. The method has a name,
  A*.

### In the game you export

- **The full interface kit,** the pieces of menu screens: besides buttons and
  bars, a switch (music, on or off), a selector (the language), a text field
  (the player's name) and a scrolling list (the controller buttons, one below
  the other). Without them, the example game's options menu could not be
  done. A prototype of the menu also showed how the interface adapts to any
  screen size.
- **Full screen** with Alt+Enter, and **sound in the browser**, which is
  still silent today.

### Under the hood

This is the part that shows the least and the one that changed the most.
Three measurements, to give a sense of scale (all on the PC, provisional):

- **Save in the middle of anything.** The game now saves everything, even a
  script paused in the middle of a wait. Imagine a chest that opens slowly,
  over three seconds: if you save halfway, when you load, it keeps opening
  from the same point. With 1,500 pieces and 500 paused waits, saving takes
  0.2 ms and restoring, 0.5 ms. One ms is a thousandth of a second.
- **Many pieces with scripts.** With 5,000 pieces, each with its own script,
  a step takes 0.64 ms. At 60 steps per second, each frame has 16.7 ms, so
  that is less than a twentieth of the time.
- **Noise comes ready-made.** Written in {{ <linguagem /> }}, it was 37 to 87
  times slower than inside the engine. That is why noise and the shortest
  path come ready-made, and the script just calls them:
  `noise.perlin(x, y)`.

## What stays out of 1.0

Each item has a reason, and almost all of them come later.

- **Screen readers in games.** A screen reader is the program that reads the
  screen aloud for people who cannot see. In 1.0, every button and every
  text in the game already keeps a name for it to read, but the reading
  itself comes later. Godot's is still experimental.
- **An animation timeline,** for scenes with several pieces moving together:
  the door opens, the camera glides across the room, the character speaks. In
  1.0, you can do it with animations in sequence and waits in the script.
- **Two players on the same computer.** The engine already keeps each
  player's commands separate, so this comes later without redoing anything.
- **Exporting to Mac and to phones.** In 1.0, games export to Windows, Linux
  and the browser, and people who play on a Mac use the browser version.
- **Consoles.** They are not in the plan. The Nintendo, Sony and Microsoft
  kits are closed by contract, and bringing the engine to them is a project of
  its own. I will think about it again after 1.0.
- **One processor core for the game.** The processor has several cores, like
  several people working at the same time. The game uses one core to compute
  each step; the editor, the sound and reading files use the others. Splitting
  the game's computation across cores would make the result change from one
  computer to another, because nobody guarantees who finishes first. The
  numbers show that one core is enough for 1.0. In the browser, also just
  one, so the game runs on any website, with no special setup.
- **Only one language.** I compared {{ <linguagem /> }} with four existing
  languages that other games use: Lua, Luau, Wren and Rhai. None of them can,
  at the same time, save a script paused halfway, like the chest's, run in
  the browser and show its errors in Portuguese.

## What the architecture leaves ready for later

- **Several cores, with the same result.** The rule is now written down for a
  system to use several cores without losing the same result on every
  computer: split the work into fixed chunks and always join them in the same
  order. It exists so that falling-sand games and games with per-pixel
  materials become possible after 1.0. In them, each pixel is a grain that
  falls, flows or catches fire, and there are hundreds of thousands of them
  every second.
- **Modules.** Fast parts written in other languages and called from
  {{ <linguagem /> }}, as if they were functions of the engine.
- **Stores.** Steam achievements ("finished the level without taking
  damage") and leaderboards, through an official module. Steam Cloud saves
  already work with no code.
- **Editor extensions,** made by the community. For example, a tool to draw
  roads, using the same commands the editor uses inside.
- **Online play,** with the requirement that everyone runs the same version
  of the same game.

## The price

The plan got bigger, and 1.0 got further away. The new date comes after I
measure the real hours of stage 2. Stages 0 and 1 went faster than I
expected, but they were infrastructure. The next ones depend more on me
playing and looking, and that cannot be rushed.

I prefer it this way. The foundation mistakes the review caught now would
cost much more in stage 8.

## What comes now

Stage 2 is back: the pieces, the levels and the first game put together in
the editor, now on the new foundation.
