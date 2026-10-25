+++
title = "O editor abre o projeto"
date = 2026-10-24T02:15:00Z
description = "A entrega 9 faz o editor abrir um projeto de verdade: a árvore da fase na Montagem, os arquivos por tipo e o Jogar rodando o projeto aberto. Por enquanto, só para ver."

[extra]
delivery_stage = "2"
deliveries = [9]
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*Um post curto da etapa 2, sobre a entrega 9. O tempo é provisório,
medido no meu PC.*

Até agora, o editor abria vazio. Com a entrega 9, ele abre um projeto: o
nome do jogo e da fase aparecem no alto ("Meu Jogo · level1"), as peças da
fase, na Montagem, e os arquivos, nos Arquivos. Por enquanto é só
para ver: mexer nas peças chega na etapa 5.

{{ <figura src="editor-projeto.png" alt="O editor com o projeto de teste Meu Jogo aberto. No alto, o nome do projeto e da fase, os menus e o botão Jogar. À esquerda, a Montagem com a árvore da fase level1: Câmera, Jogador com um Sprite dentro, Chão, Moedas com três moedas, Nuvem apagada e Placa, cada uma com o ícone e o tipo na cor dele; embaixo, os Arquivos com as seis categorias e a contagem de cada uma. No meio, a aba level1, ainda vazia, e embaixo o Console." lang="pt" caption="O editor com o projeto de teste aberto: um print real da entrega 9." has_text={true} /> }}

## A Montagem

A **Montagem** mostra a fase como uma árvore: cada peça com o ícone e a cor
do seu tipo (a cópia de um molde, com os do molde), e as peças de dentro
(as filhas) mais à direita, ligadas por linhas pontilhadas. O Jogador, por
exemplo, é um Grupo com um Sprite (uma imagem) dentro.

- O selo **molde** marca a peça que é cópia de um molde, a peça-modelo que
  se repete pela fase (o *prefab*), como o Jogador e as três moedas.
- Uma peça com o interruptor **Ativa** desligado aparece apagada, como a
  Nuvem.
- Um clique seleciona a peça e acende o ramo dela (as linhas até as
  filhas), a setinha ▾ fecha e abre o ramo, e as setas do teclado andam
  pela árvore.

A árvore também funciona com **leitor de tela**, o programa que lê a tela
em voz alta para quem não enxerga (o *screen reader*). No Narrador do
Windows, descer até o Jogador faz ele dizer "Jogador, Grupo, molde".

## Os Arquivos

Os **Arquivos** mostram as seis categorias da etapa 2 (fases, moldes,
sprites, sons, fontes e traduções), cada uma com a cor do tipo e quantos
arquivos tem. Uma categoria vazia aparece apagada.

## Abrir sem estragar

Abrir um projeto não muda nada nele, com uma exceção. Cada imagem, som e
fonte do jogo tem ao lado uma ficha `.meta`, com o número que identifica o
arquivo e o jeito de ele entrar no jogo. É por esse número que a fase acha
a imagem da moeda, mesmo que você mude o nome ou a pasta dela. Se faltar
uma ficha, o editor cria e avisa qual criou no Console, o painel de
mensagens. Um projeto num formato antigo não é regravado: o editor mostra
o comando que o converte, guardando uma cópia do antigo.

O editor reabre o último projeto. Do início do programa até a Montagem na
tela, levou 473 ms (menos de meio segundo) no meu PC, no pior de cinco
aberturas; o limite oficial é 3 s.

E o **Jogar** roda o projeto aberto. O jogo ainda é o quadrado de teste,
que anda com as setas; o exemplo de jogo de plataforma chega na entrega 10.

## O que o testador e eu achamos

Foram seis conferências do testador, o conferente que não participou da
obra, e duas rodadas minhas. A mais curiosa: o × da aba da
fase passava em todos os testes, mas não fechava a aba com o mouse. Os
testes clicavam pelo caminho que o leitor de tela usa, não pelo mouse.
Agora, um teste clica como o mouse.

Algumas das outras: depois de clicar numa peça, as setas paravam de
andar; o realce da linha sob o mouse escondia as linhas pontilhadas; o
ponteiro não virava a mãozinha sobre os botões; e o projeto de teste não
tinha comandos, então o quadrado não andava. Cada correção ganhou um teste.

## O que vem agora

A entrega 10: o primeiro exemplo de jogo de plataforma, com uma fase de
três telas e a câmera seguindo o jogador. Por enquanto ele só anda; a
gravidade e o pulo de verdade chegam na etapa 3.
