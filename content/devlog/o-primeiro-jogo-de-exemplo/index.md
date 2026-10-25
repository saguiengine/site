+++
title = "Nota: o primeiro jogo de exemplo, com a câmera seguindo"
date = 2026-10-25T15:30:00Z
description = "A entrega 10 traz o Meu Jogo, o primeiro exemplo de jogo de plataforma: uma fase de três telas em pixel art, com a câmera seguindo o macaquinho e a placa no idioma de quem joga."

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*Uma nota curta da etapa 2, sobre a entrega 10. Os tempos são provisórios,
medidos no meu PC.*

Até agora, o jogo de teste era um quadrado num fundo liso. A entrega 10
traz o **Meu Jogo**, o primeiro exemplo de jogo de plataforma (um
*platformer*): uma fase de três telas de largura, em *pixel art* (o desenho
feito de quadradinhos visíveis). É ele que a engine roda quando ninguém
escolhe outro projeto.

{{ <figura src="meu-jogo.gif" alt="Animação do Meu Jogo: o macaquinho anda pela fase em pixel art, sobre o chão de grama e terra, passando por arbustos, flores e plataformas de tábua; perto do fim, ele sobe pelo ar e desce de novo, porque ainda não há gravidade; a câmera o acompanha e para no fim da fase, com o céu, as montanhas com neve, as colinas e os morros com árvores ao fundo." lang="pt" caption="A câmera seguindo o macaquinho até o fim da fase." has_text={false} /> }}

## O que tem na fase

- O jogador é o macaquinho dos desenhos do site e do editor. Ele anda com
  as setas, as teclas W, A, S e D ou o controle. Por enquanto ele só anda,
  para qualquer lado, até para cima, pelo ar; o pulo só toca o som. A
  gravidade e o pulo de verdade chegam na etapa 3.
- O chão, as plataformas de tábua e as nuvens vêm da **Mata**, o conjunto
  de ladrilhos de 16 × 16 pixels (os *tiles*) que já aparecia nos desenhos
  do editor; a placa é a da Mata, redesenhada maior para caber a frase.
  Arbustos e flores, também da Mata, enfeitam o chão.
- As nuvens são cópias de um molde, a peça-modelo que se repete pela fase
  (o *prefab*); uma delas vem de uma variante maior do molde.
- O fundo tem quatro planos: o céu em faixas, montanhas com neve, colinas e
  morros com árvores. Um programa desenha esse fundo (é um fundo
  *procedural*, gerado por código) e sabe fazer também a versão de noite,
  que aparece nos desenhos do editor.

## A câmera e a placa

A **Câmera**, que chegou na entrega 7, agora segue o jogador numa fase de
verdade e para nas bordas, sem mostrar o vazio além delas.

A placa diz "Use as setas para andar" em português e "Use the arrow keys to
walk" em inglês, no idioma de quem joga. É a primeira vez que o jogo usa
uma fonte guardada no próprio projeto: a monogram, numa grade de letras de
6 × 12 pixels.

{{ <figura src="meu-jogo-600.png" alt="O começo do Meu Jogo: o macaquinho no chão, embaixo de uma placa de madeira que diz Use as setas para andar, com arbustos, flores, duas plataformas de tábua, duas nuvens e o fundo de céu, montanhas com neve, colinas e morros." lang="pt" caption="A placa, no idioma de quem joga, com a fonte do projeto." has_text={true} /> }}

## O mesmo jogo em todo lugar

Um *replay* (a gravação dos comandos, que o jogo repete sozinho) de 60
segundos vai até o fim da fase e volta. Ele termina
com o mesmo *hash*, uma impressão digital do estado do jogo que muda se
qualquer coisa mudar, no Windows, no Linux, no macOS e em *WebAssembly* (o
*wasm*), o formato de programa que os navegadores usam; por enquanto, esse
teste roda fora do navegador. Salvar no meio e continuar em outra execução
também dá o mesmo resultado.

No meu PC, o jogo abre e mostra o primeiro quadro (cada imagem que aparece
na tela) em 0,6 s (o limite oficial é 1,5 s), e 99% dos quadros levam menos
de 3 ms (um ms é um milésimo de segundo).

## O que o testador e eu achamos

O testador, o conferente que não participou da obra, viu que as letras da
placa saíam quebradas: o texto estava num tamanho diferente daquele para o
qual a fonte de pixel art foi desenhada, e faltavam pixels. Agora a placa
usa a fonte do projeto no tamanho certo, e um teste compara a placa pixel a
pixel. E, jogando, eu vi que a arte não era a dos desenhos do editor: ela
foi trocada pela Mata, e o fundo ganhou o pixel art de agora.

## O que vem agora

A entrega 11 arruma os testes e a integração contínua (a *CI*, o robô que
roda os testes a cada mudança). Depois vem a revisão do fim da etapa 2.
