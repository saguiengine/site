+++
title = "Nota: moldes, cópias e o interruptor Ativa"
date = 2026-10-20T19:26:00Z
description = "Um molde vira muitas cópias, cada uma com as suas diferenças, e toda peça ganhou um interruptor Ativa para sair do jogo e voltar. Como a Unity e o Godot fazem, e o que escolhemos."

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*Uma nota curta da etapa 2, sobre a entrega 6.*

Na nota sobre o formato das fases, o jogador vivia num **molde** (o
*prefab* de outras engines): um arquivo com uma peça pronta, que a fase
repete quantas vezes quiser. Nesta entrega, os moldes ficaram completos.

## Cópias com diferenças

Cada cópia guarda só o que muda em relação ao molde. Três morcegos do mesmo
molde podem ter cores diferentes. Se você muda a velocidade no molde, os
três mudam, e cada um continua com a sua cor. A cópia passa por cima de um
valor do molde (o *override*).

Também dá para fazer uma **variante**: um molde que parte de outro e muda
algumas coisas, como um morcego de fogo, que é o morcego com outra cor e
mais rápido. E um molde pode ter outros dentro: uma sala com dois morcegos,
e a fase com três salas.

## Nomes que não quebram

Cada peça dentro de uma cópia ganha um ID (um código que identifica a peça
e nunca muda), calculado a partir do ID da cópia e do ID da peça no molde.
Por isso, renomear uma peça no molde não quebra as diferenças das cópias. O
Godot passou a fazer parecido na versão 4.6, com um ID guardado em cada nó.

E, se você desmancha uma cópia, transformando as peças dela em peças comuns
da fase, elas ficam com os mesmos IDs. Nada que apontava para elas se perde.

## O interruptor Ativa

Às vezes uma parte do jogo precisa sumir de vez e voltar depois: a porta
que só aparece quando a chave é pega, o inimigo que só entra na segunda
onda. Toda peça agora tem uma caixinha **Ativa**, ao lado do nome.

Desligada, a peça e as filhas saem do jogo: não aparecem e não rodam. Quando
a física e o script chegarem, ela também não vai colidir nem receber
eventos, e um script vai poder ligá-la de novo.

As outras engines resolvem isso de jeitos diferentes (conferido na Unity
6.6 e no Godot 4.7):

- Na Unity, é um interruptor só (`SetActive`): desligar um objeto desliga
  os filhos, para os scripts dele e o tira do desenho e das colisões.
- No Godot, são dois. O `visible` esconde a peça, mas ela continua rodando
  e colidindo. O `process_mode` a faz parar e, por padrão, a tira das
  colisões. Para tirar de vez, mexe-se nos dois. É de propósito: lá,
  esconder e parar são coisas separadas.

Ficamos com o jeito da Unity: um interruptor só, que faz o que se espera. O
Visível continua, para esconder sem parar, como um fantasma invisível que
ainda anda.

Numa cópia, desligar uma peça do molde é só mais uma diferença: o morcego da
terceira sala pode vir sem uma asa.

## O que vem agora

A entrega 7: o estilo do jogo (pixel art ou HD), a escala da tela e a
câmera que segue o jogador.
