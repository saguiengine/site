+++
title = "Note: the editor opens the project"
date = 2026-10-24T02:15:00Z
description = "Delivery 9 makes the editor open a real project: the level's tree in the Assembly, the files by type and Play running the open project. For now, only to look at."

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*A short note from stage 2, about delivery 9. The time is provisional,
measured on my PC.*

Until now, the editor opened empty. With delivery 9, it opens a project:
the names of the game and of the level show at the top ("Meu Jogo ·
level1"), the level's pieces in the Assembly, and the files in Files. For
now it is only to look at: changing the pieces comes in stage 5.

{{ <figura src="editor-projeto.en.png" alt="The editor in English with the test project Meu Jogo open. The project's own names (Meu Jogo, Câmera, Jogador, Chão, Moedas, Nuvem, Placa) are in Portuguese, because the project was written in Portuguese; the editor's words are in English. At the top, the project and level names, the menus and the Play button. On the left, the Assembly with the tree of the level level1: Câmera, Jogador with a Sprite inside, Chão, Moedas with three coins, Nuvem dimmed and Placa, each with its icon and its type in its color; below, Files with the six categories and the count of each. In the middle, the level1 tab, still empty, and the Console below it." lang="en" caption="The editor with the test project open: a real print of delivery 9. The names inside the project are in Portuguese, as the project was written." has_text={true} /> }}

## The Assembly

The **Assembly** shows the level as a tree: each piece with the icon and
color of its type (a copy of a mold, with the mold's), and the pieces
inside (the children) further to the right, joined by dotted lines. The
player (Jogador), for example, is a Group with a Sprite (an image) inside.

- The **mold** seal marks a piece that is a copy of a mold, the model piece
  that repeats across the level (the *prefab*), like the player and the
  three coins.
- A piece with the **Active** switch off shows dimmed, like the cloud
  (Nuvem).
- A click selects the piece and lights its branch (the lines down to its
  children), the little ▾ arrow closes and opens the branch, and the
  keyboard's arrows walk the tree.

The tree also works with a *screen reader*, the program that reads the
screen aloud for people who cannot see it. In
Windows' Narrator, going down to the player makes it say "Jogador, Group,
mold".

## Files

**Files** shows the six categories of stage 2 (levels, molds, sprites,
sounds, fonts and translations), each with the color of its type and how
many files it has. An empty category shows dimmed.

## Opening without harm

Opening a project changes nothing in it, with one exception. Each image,
sound and font of the game has a `.meta` card beside it, with the number
that identifies the file and the way it goes into the game. That number is
how the level finds the coin's image, even if you change its name or its
folder. If a card is missing, the editor creates it and says which one in
the Console, the messages panel. A project in an old format is not written
again: the editor shows the command that converts it, keeping a copy of
the old one.

The editor reopens the last project. From the program's start to the
Assembly on the screen, it took 473 ms (less than half a second) on my PC,
in the worst of five openings; the official limit is 3 s.

And **Play** runs the open project. The game is still the test square,
which walks with the arrows; the platform game example comes in delivery
10.

## What the tester and I found

There were six checks by the tester, the checker who took no part in the
work, and two rounds of my own. The most curious: the × on the level's tab
passed every test, but did not close the tab with the mouse. The tests
clicked by the path the screen reader uses, not by the mouse. Now, a test
clicks as the mouse does.

Some of the others: after clicking a piece, the arrows stopped walking;
the highlight of the row under the mouse hid the dotted lines; the pointer
did not turn into the little hand over the buttons; and the test project
had no commands, so the square did not walk. Each fix got a test.

## What comes now

Delivery 10: the first platform game example, with a level three screens
wide and the camera following the player. For now it only walks; gravity
and the real jump come in stage 3.
