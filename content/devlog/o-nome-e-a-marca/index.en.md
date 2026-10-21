+++
title = "The name Sagui and the trademark"
date = 2026-10-21
description = "Liking a name is not enough: you have to check whether it can become a trademark. A search at the INPI found a software SAGUI, and the engine's name may change before stage 4. Why that is not scary: the name lives in a single file."

[extra]
thumbnail = "nome-miniatura.png"
thumbnail_has_text = false
+++

*A special post, outside the deliveries.*

The name Sagui came at the start of the project. It hides the "Gui" of
Guilherme, it is Brazilian, it is easy to say in English (sah-GWEE) and it
already comes with a mascot: the little monkey that shows up in the logo and
in the examples. But liking a name is not enough. Before launching, you need
to know whether it can become a **trademark**.

{{ <figura src="nome-cena.png" alt="Drawing: in the middle, a file with the little monkey from the logo and colored lines; four arrows go out of it to an editor window, a page of the site, a script file and an error message bubble." lang="en" has_text={false} /> }}

## What a trademark is

A registered trademark gives you the right to use a name exclusively for a
kind of product. In Brazil, trademarks are registered by the INPI, the
National Institute of Industrial Property (*Instituto Nacional da
Propriedade Industrial*). A registration holds per **class**, a group of
products and services: a program you download goes in class 9, a software
service over the internet in 42, and courses and entertainment in 41. But
the class alone does not decide: the INPI looks at whether the products are
alike. In class 9, for example, a SAGUI for eyeglass frames and another one
for computer programs live side by side, because nobody mistakes eyeglasses
for software.

## What the search found

I did the first search at the INPI on October 16, and class 9 looked free.
But the class field asks for two digits, "09", and I had typed "9". Redone
on October 18, the search showed something else:

- in class 9, the trademark SAGUI (*Sistema de Apoio à Gestão e Uso da
  Inovação*, a system that supports managing and using innovation), from
  Unicamp, a Brazilian university, for computer programs, in force until
  2036;
- in class 42, two trademarks tied to software, sagui.ai and Saguitech;
- and an application for "Sagui Studio" that the INPI has already turned
  down, for looking too much like older trademarks.

The INPI compares names by sound and by idea, and adding a word, like
"Engine" or "Studio", does not solve it: the law speaks of reproducing a
trademark "even with an addition" (*ainda que com acréscimo*). That does not
mean there is a conflict. That is for a specialist to judge, and nothing
here is legal advice. It means the question is serious enough to be settled
before launching, not after.

## The name lives in a single file

From the start, the engine was made for this moment. The brand, the name of
the language, the extension of the scripts (`.sagui`) and the letters of the
error codes live in a single file, `identity.toml`. The code uses neutral
names, and an automated test fails if the brand shows up written anywhere
else. The editor, the messages and the site itself read the name from that
file.

{{ <figura src="nome-editor-logo.en.png" alt="The corner of the editor's top bar: the logo, with the little monkey on a blue square, the name Sagui beside it and the File menu." lang="en" caption="The real editor: the name beside the logo comes from identity.toml." /> }}

Changing the name today means changing that file, the logo and a few
drawings. What gets expensive is changing it later: once the extension is in
people's projects, the installers are out and the name is in videos and
tutorials. That is why the decision has a date.

## What comes next

Before stage 4, when the scripting language takes its final shape, I will
consult a trademark attorney (in Brazil, an *agente da propriedade
industrial*), the professional who handles trademark registrations at the
INPI, and decide: keep Sagui or change it. There are already a few backup
names, checked, that I am keeping to myself for now, so nobody registers
them first. When the decision comes, it becomes a post here.
