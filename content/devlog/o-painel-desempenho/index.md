+++
title = "Nota: o painel Desempenho, e por que quadro não é passo"
date = 2026-10-21T21:00:00Z
description = "A entrega 12 mostra os números do jogo enquanto ele roda: quadros por segundo, 1% low, o tempo da placa de vídeo e mais, no editor e dentro da janela do jogo. E responde a uma boa pergunta: passo é a mesma coisa que FPS?"

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*Uma nota curta da etapa 2, sobre a entrega 12. Os números são
provisórios, medidos no meu PC.*

Ao dar Jogar, agora dá para ver como o jogo está indo por dentro. O editor
ganhou o painel **Desempenho**, uma aba ao lado do Console, e a janela do
jogo ganhou um quadro com os números principais, que liga e desliga com F3.
A entrega nasceu de um pedido no meio da etapa e passou na frente da 7.

{{ <figura src="desempenho-cena.png" alt="Desenho: à esquerda, um gráfico do tempo de cada quadro, com uma linha tracejada e quatro picos; à direita, uma fileira de traços azuis, os quadros, sobre uma fileira com menos traços verdes, os passos, e o macaquinho embaixo." lang="pt" has_text={false} /> }}

## Quadro não é passo

A primeira pergunta ao ver o painel foi: "passo seria FPS?". Não é.

- O **quadro** é cada imagem que aparece na tela. Quantos quadros saem por
  segundo (o *FPS*) depende do monitor e da placa de vídeo: 144 num
  monitor de 144 Hz, 60 num de 60.
- O **passo** é cada vez que a lógica do jogo roda: andar, pular, colidir.
  São sempre 60 por segundo, em qualquer PC, e é isso que faz o jogo dar o
  mesmo resultado em todo lugar.

Entre um passo e outro, o desenho só suaviza o movimento. Por isso o
painel mostra os dois, e a coluna dos passos se chama **Lógica**.

## O que o painel mostra

- **Quadros:** o FPS, o tempo de cada quadro e o gráfico dos últimos 10 s.
  E o *1% low*, a média do 1% de quadros mais lentos: se a média é 144 e o
  1% low é 60, o jogo engasga de vez em quando, mesmo parecendo rápido.
- **Lógica:** quanto do tempo de um passo, 16,7 ms, a lógica usa (um ms é
  um milésimo de segundo).
- **Vídeo:** a placa, o tempo dela para desenhar um quadro e a memória de
  vídeo.
- **Tela:** a resolução, a escala do pixel art, a frequência do monitor e o
  *VSync*, que faz o jogo esperar o monitor para mostrar cada quadro, sem
  cortes na imagem.
- **Jogo:** a CPU, a memória e quantos pedidos de desenho vão para a placa
  a cada quadro.

Um botão Copiar leva tudo, com a versão e a placa, para colar num relato de
problema.

{{ <figura src="desempenho-painel.png" alt="O painel Desempenho, na aba ao lado do Console: o gráfico do tempo de cada quadro nos últimos 10 s e os blocos Quadros (144 fps, 1% low 121 fps), Lógica (60 passos por segundo), Vídeo, Tela e Jogo. Em cima, o interruptor Mostrar também no jogo (F3), o aviso de jogo parado e o botão Copiar." lang="pt" caption="O painel de verdade, desenhado pelo editor, com números de exemplo." /> }}

## O que o testador achou

Medir não pode atrapalhar. O jogo mede tudo isso fora da lógica, a
medição custa cerca de 0,04 ms por quadro, e o resultado do jogo continua
idêntico com o painel ligado ou desligado.

Duas curiosidades. O painel chegou a dizer 61 FPS a 60 quadros por segundo
em quase metade das vezes: a conta pegava as duas pontas do último segundo, e às
vezes entrava um quadro a mais. Agora o FPS vem do tempo médio de cada
quadro, e o 61 sumiu. E, numa janela baixa, a última linha do painel ficava
cortada. Agora, quando falta altura, o gráfico some e os números ficam
inteiros.

{{ <figura src="desempenho-f3.png" alt="O quadro F3 no canto da janela do jogo: 60 fps e 16,7 ms, o 1% low, a lógica a 60 passos por segundo, o tempo da GPU e a CPU, a janela de 1920×1080 a 59 Hz com VSync, e embaixo F3 esconde." lang="pt" caption="O quadro F3 na janela do jogo, capturado da tela do meu PC." /> }}

## O que vem agora

A entrega 7: o estilo do jogo (pixel art ou HD), a escala da tela e a
câmera que segue o jogador.
