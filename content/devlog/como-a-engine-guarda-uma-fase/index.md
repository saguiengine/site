+++
title = "Nota: como a engine guarda uma fase"
date = 2026-10-19
description = "Uma fase do jogo agora vive num arquivo de texto que dá para ler e consertar à mão. Uma nota curta sobre o formato, os moldes, os IDs que não quebram e o leitor que abre uma fase de 5.000 peças em 31 ms."

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*Uma nota curta da etapa 2. Os números são provisórios, medidos no meu PC.*

Uma fase do jogo, com o cenário, o jogador, as moedas e as plataformas,
agora vive num arquivo de texto. Dá para abrir num editor de texto qualquer
e ler:

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
        image: (id: "66401c90be1e26a241e250e87b2fe284", path: "sprites/ground.png"),
    ),
),
```

Cada peça é um bloco: um ID (um código que identifica a peça e nunca muda),
quem é o pai dela, o tipo, o nome que aparece
no editor e só as propriedades que mudam do padrão. O formato se chama RON
(*Rusty Object Notation*), um primo do JSON, o formato de texto mais usado
para guardar dados, feito para o Rust, a linguagem em que a engine é
escrita.

Por que texto, e não um arquivo binário, que só um programa consegue ler?
Porque dá para ver o que mudou de uma versão para outra no Git, o sistema
que guarda o histórico do projeto (o *diff*), juntar o trabalho de duas pessoas
(o *merge*) e consertar à mão quando algo dá errado.

## Moldes

O jogador não está descrito dentro da fase. Ele está num **molde** (o
*prefab* de outras engines), o arquivo `player.mold`. A fase só diz "aqui
vai uma cópia do molde do jogador, nesta posição". Mudou o molde, mudam
todas as cópias. A próxima entrega traz as variantes e os moldes dentro de
moldes.

## IDs que não quebram

Cada imagem e cada som ganha um arquivo `.meta` ao lado, com um ID
permanente e uma impressão digital do conteúdo (um *hash*). Se você
renomeia ou move o `player.png`, a engine reencontra o `.meta` pelo
conteúdo, e as fases continuam apontando para a imagem certa. Se o mesmo
arquivo aparece em dois lugares, o de caminho mais curto fica com o ID, e o
outro ganha um aviso.

## Nada some

Se uma fase tiver uma propriedade que esta versão não conhece, escrita à mão
ou por um script, a engine avisa e guarda a linha como veio. Abrir e salvar
nunca apaga uma propriedade que ela não entende. Só os comentários escritos
à mão (as linhas que começam com `//`) ainda se perdem ao salvar.

## O leitor próprio

A biblioteca de RON que usávamos, o código pronto de outras pessoas que lê
esse formato, ficava lenta com fases grandes. Para ler
valores sem tipo fixo, ela procurava um trecho no resto do arquivo a cada
número: quanto maior o arquivo, mais lenta cada leitura. Com 5.000 peças,
abrir a fase levava 1,1 s. A meta é meio segundo no meu PC e um segundo no
notebook modesto de referência.

Escrevemos então um leitor próprio (um *parser*), só para fases e moldes, que passa pelo
texto uma vez. A mesma fase abre em **31 ms** (um ms é um milésimo de
segundo), cerca de 35 vezes mais rápido. A lentidão já foi corrigida no código da biblioteca, mas ainda não
saiu numa versão. E o nosso leitor continua útil mesmo assim: ele guarda
detalhes que a biblioteca perde, como a diferença entre uma lista e um grupo fixo
de valores, como a posição (x, y).

Um leitor novo é um lugar novo para erros, então ele foi posto à prova
contra a biblioteca: mais de 3 milhões de textos aleatórios e arquivos
estragados de propósito (a técnica se chama *fuzzing*), sem travar nem
quebrar uma vez. Num erro de
digitação, ele aponta o mesmo lugar que a biblioteca em 87% dos casos. E
uma fase com 100.000 grupos, um dentro do outro, abre em 0,3 s.

## O que vem agora

Os moldes com variantes e os moldes dentro de moldes, ainda na etapa 2.
