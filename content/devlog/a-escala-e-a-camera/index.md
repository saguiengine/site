+++
title = "A imagem que cabe em qualquer tela, e a câmera que segue"
date = 2026-10-22
description = "A entrega 7 decide como o jogo aparece numa janela de qualquer tamanho, do notebook ao monitor ultralargo, e traz a câmera que acompanha o jogador. Tudo sem mudar o resultado do jogo."

[extra]
delivery_stage = "2"
deliveries = [7]
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*Um post curto da etapa 2, sobre a entrega 7.*

Um jogo em *pixel art* (feito de quadradinhos visíveis) é desenhado pequeno: na {{ <marca /> }}, 640 × 360 pixels, a
**resolução base**. Só que ninguém joga numa janela desse tamanho. A tela
pode ter 1366 × 768, 1920 × 1080 ou ser um monitor ultralargo de 2560 ×
1080. A entrega 7 decide como a imagem aumenta em cada caso, e traz a câmera
que acompanha o jogador.

## Dois estilos

O projeto escolhe um **estilo**. No **pixel art**, a base é 640 × 360 e as
imagens, por padrão, não são suavizadas: cada pixel continua um quadradinho
nítido. No **HD**, a base é 1920 × 1080 e as imagens são suavizadas ao
aumentar ou diminuir. O estilo dá esses valores iniciais, e também os da
câmera e da escala; o projeto pode mudar cada um.

## Quatro jeitos de caber na tela

- **Pixel perfeito** (*pixel perfect*): só aumenta por números inteiros,
  ×2 ou ×3, e completa o resto com barras pretas (o *letterbox*). Os pixels
  ficam perfeitos. É o padrão do pixel art.
- **Ajustar:** aumenta o máximo que cabe sem deformar, com barras só onde
  sobra espaço (em cima e embaixo, ou dos lados). É o padrão do HD.
- **Expandir:** sem barras: a janela mais larga mostra mais do mundo dos
  lados.
- **Esticar:** preenche tudo, mesmo deformando.

{{ <figura src="escala-modos.png" alt="Duas capturas de um teste da entrega 7 numa janela de 1366 × 768, com um chão xadrez e um quadrado branco: à esquerda, o pixel perfeito, com o jogo em ×2 e uma moldura preta em volta; à direita, o ajustar, com o jogo em ×2,13 ocupando quase toda a janela." lang="pt" caption="Um teste real da entrega 7, desenhado pela engine: pixel perfeito e ajustar." has_text={false} /> }}

No pixel art em ajustar, 1366 × 768 dá uma escala quebrada: ×2,13. Aumentar um pixel
2,13 vezes o deixaria torto, com uns pixels mais largos que outros. O
truque é aumentar ×3, ainda nítido, e depois reduzir para o tamanho da
janela com um filtro suave. De perto, a borda continua reta, só com uma
linha fina de transição.

{{ <figura src="escala-borda.png" alt="O canto do quadrado branco no ajustar em ×2,13, ampliado: as bordas são retas, com só uma linha fina de verde mais claro entre o quadrado e o chão." lang="pt" caption="O canto do quadrado em ×2,13, ampliado." has_text={false} /> }}

## A câmera que segue

A **Câmera** é uma peça que acompanha o jogador. Dá para ajustar:

- a **suavização**: 0 deixa a câmera presa ao jogador; 0,9 faz ela chegar
  aos poucos, e depois de meio segundo falta 4% do caminho;
- os **limites**, um retângulo que a câmera não passa, para ninguém ver
  além da borda da fase;
- o ***zoom***, que aproxima ou afasta a imagem: só inteiro onde a escala
  também é inteira (no pixel perfeito, o padrão do pixel art), para não
  entortar os pixels, ou suave, como opção.

A zona morta (*dead zone*), uma área em que o jogador anda sem a câmera
mexer, e a antecipação (*look-ahead*), a câmera olhando um pouco à frente,
já estão no formato do arquivo. Elas passam a funcionar na etapa 3, com o
movimento de verdade.

Por dentro, a lógica do jogo usa sempre a resolução base. O desenho muda
com a janela, e o jogo não. Um *replay*, a partida gravada, desenhado nos
quatro modos e em quatro tamanhos de janela, deu o mesmo *hash*, a
"impressão digital" do estado do jogo, em todos.

## O que o testador achou

O testador, o conferente que não participou da obra, passou três vezes pela
entrega. Achou um céu fixo que sumia quando o zoom suave estava ligado, e
um caso raro de arredondamento que fechava o jogo. Também viu que, no
expandir, o monitor largo mostrava um pedaço além do limite da câmera.
Os três foram corrigidos, cada um com um teste que falhava antes.

## O que vem agora

A entrega 8: o texto dentro do jogo e os idiomas.
