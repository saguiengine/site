+++
title = "A árvore de peças e o jogo que congela em qualquer passo"
date = 2026-10-20T19:25:00Z
description = "As quatro primeiras entregas da etapa 2: o editor igual ao desenho, a régua de cada entrega, as peças dentro de peças e o estado do jogo que se grava e continua igualzinho, em qualquer sistema."

[extra]
delivery_stage = "2"
deliveries = [1, 4]
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*Um post curto da etapa 2, sobre as entregas 1 a 4. Os números são
provisórios, medidos no meu PC.*

Daqui para a frente, cada entrega da etapa ganha um post. Este junta as
quatro primeiras, que vieram antes do formato das fases.

{{ <figura src="arvore-cena.png" alt="Desenho: à esquerda, uma árvore de peças, com uma pasta no alto e o personagem, uma moeda e uma plataforma como filhas; à direita, os passos do jogo numa linha de pontos, com uma foto guardada num deles e uma seta que volta a ela." lang="pt" has_text={false} /> }}

## O editor igual ao desenho (entrega 1)

Pequenos acertos para o editor ficar igual ao mockup, o desenho de como ele
vai ficar. O menu de *layouts* (os jeitos de arrumar os painéis na tela)
marca o que está em uso, os filtros do Console (a lista de mensagens do
jogo) subiram para o cabeçalho, e o logo virou o rostinho do {{ <marca /> }} em
*pixel art*, o desenho feito de quadradinhos visíveis, como nos jogos
antigos.
O desenho do logo fica no mesmo arquivo que guarda o nome da engine: trocar
a marca troca o desenho.

{{ <figura src="arvore-editor-padrao.png" alt="O editor depois da entrega 1, no arranjo Padrão: a barra de cima com o logo, o botão Jogar e o menu de layouts, e os painéis Montagem, Fase, Propriedades, Arquivos e Console, ainda vazios." lang="pt" caption="O editor depois da entrega 1." /> }}

## A régua da etapa (entrega 2)

Cada entrega agora gera um relatório automático. Para cada critério, ele
diz o valor medido, o limite e a folga, e não só "passou". Por exemplo, o
passo de teste da etapa 1, com 5.000 quadrados, levou 0,066 ms, contra um
limite de 0,5 ms no meu PC (um ms é um milésimo de segundo).

## A árvore de peças (entrega 3)

Cada coisa do jogo é uma **peça**: o jogador, a moeda, o chão. Agora uma
peça pode ter filhas, como pastas dentro de pastas: a espada presa ao
jogador anda, gira e some junto com ele. Essa árvore se chama **Montagem**
(a *scene tree* de outras engines).

Toda fase nova vem com quatro **camadas**, como folhas transparentes empilhadas:
Fundo, Mundo, Frente e Interface. Dentro de uma camada, dá para ordenar
pela altura na tela, como numa foto de grupo: quem está mais embaixo fica
na frente.

{{ <figura src="arvore-ordem.png" alt="Um teste da entrega 3, desenhado pela engine: retângulos coloridos em camadas e ordens diferentes, uns na frente dos outros, sobre um retângulo verde." lang="pt" caption="Um teste real da entrega 3, desenhado pela engine." has_text={false} /> }}

Com 5.000 peças, umas dentro das outras em 8 níveis, um passo do jogo leva
no máximo 0,134 ms em 95% das vezes (o *p95*). E 2.000 imagens saem num pedido só à
placa de vídeo (uma *draw call*).

O testador, um conferente que não participou da obra, achou um caso
curioso: criar 2.000 peças com o mesmo nome levava 3 s, porque cada nome
novo ("Inimigo 2", "Inimigo 3"…) era comparado com todos os irmãos. Hoje
leva 0,7 ms.

## Congelar o jogo em qualquer passo (entrega 4)

O jogo anda em **passos** fixos, 60 por segundo (ou 120, se o projeto
escolher). Agora dá para tirar uma
foto de tudo o que o jogo lembra num passo (o *estado*), gravar num arquivo
e continuar dali depois, com exatamente o mesmo resultado de quem nunca
parou. Com 5.000 peças, a foto leva 0,234 ms, e o arquivo tem 822 kB.

Para saber se duas execuções deram igual, a engine compara um *hash*: um
resumo curto de todos os dados, que muda se um único *bit* mudar (a menor
unidade de dado, um 0 ou um 1), como o dígito verificador do CPF. Os
hashes saem iguais no Windows, no Linux, no macOS e no *wasm*, o formato de
programa que os navegadores usam. Isso é o
*determinismo*: as mesmas entradas dão sempre o mesmo resultado.

O testador trocou um bit no meio de um arquivo de estado, e a engine o
carregou sem reclamar. Agora o arquivo guarda o próprio hash, e um arquivo
danificado é recusado.

Isso ainda não é "salvar o jogo": por enquanto, é uma ferramenta de teste,
pela linha de comando (comandos digitados num terminal, sem janela). O save do jogo chega na etapa 11a.

## O que vem agora

O próximo post conta a entrega 6: moldes, cópias e o interruptor Ativa.
