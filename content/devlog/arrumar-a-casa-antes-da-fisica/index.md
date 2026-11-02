+++
title = "Arrumar a casa antes da física"
date = 2026-11-02
description = "A entrega 1 da etapa 3 não muda nada na tela: cuida de 16 itens pequenos que ficaram da etapa 2 e prepara a engine para a física, com uma trava contra a ordem errada das peças e a versão nova."

[extra]
delivery_stage = "3"
deliveries = [1]
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*Um post curto da etapa 3, sobre a entrega 1. Os tempos são provisórios,
medidos no meu PC.*

A etapa 3 traz a física, mas a primeira entrega não muda nada na tela. Ela
arruma a casa: 16 itens pequenos que as conferências da etapa 2 deixaram
numa ficha no GitHub (uma *issue*), e os preparos para a física.

## Uma trava contra a ordem errada

A engine guarda as peças como num estacionamento, que os programadores
chamam de *arena*: a vaga que fica livre vai para a próxima peça que chegar.

O jogo anda na ordem da árvore de peças, a da Montagem (ou pela
prioridade, quando alguém escolhe uma): uma ordem que se vê no editor e que
não muda quando uma peça sai e outra entra. Se a física recebesse as peças
na ordem das vagas, o resultado passaria a depender de uma ordem que ninguém
vê.

Agora o corretor automático do código (o *linter*) recusa qualquer uso novo da
ordem das vagas. Os seis lugares em que ela é a certa levam o motivo escrito.

{{ <figura src="arena-ordem.png" alt="Desenho: à esquerda, uma fileira de quatro vagas: uma moeda, uma vaga vazia, uma plataforma e o macaquinho, e embaixo uma seta vermelha tracejada e um X; à direita, a árvore de peças, com uma pasta no alto e o macaquinho, uma moeda e uma plataforma penduradas nela, e embaixo uma seta verde e um sinal de certo." lang="pt" caption="A ordem que vale é a da árvore de peças, e não a das vagas." has_text={false} /> }}

## O quadrado sai, a versão sobe

O quadrado de teste da etapa 1, que só os testes e uma medição usam, morava
no núcleo da engine. Agora fica atrás de um interruptor que só eles ligam
(uma *feature*), fora do programa que vai para quem joga. Os *hashes*
de referência da etapa 1, as impressões digitais do jogo, continuaram os
mesmos, a 60 e a 120 passos por segundo, no computador e no *WebAssembly*, o
formato de programa dos navegadores.

A versão interna passou a 0.3.0-dev (o "dev" é de desenvolvimento). Um estado
salvo pela 0.2 (a foto do jogo num passo) é recusado, e
uma partida gravada pela 0.2 (um *replay*) ainda roda, com um aviso de que o
resultado pode mudar.

## Erros mais claros

Uma fase com um erro de digitação, como a vírgula a mais em `format: 1,,`,
dava dois avisos: o certo, a SE0004, com a linha e a coluna (linha 2,
coluna 15), e um errado, a SE0007, como se o arquivo não pudesse ser lido.
Agora sai só a SE0004, no editor e no jogo.

Quatro comandos do projeto não apontavam uma opção escrita errado: o
`prova 1 --hashes-onyl`, por exemplo, ignorava a opção errada e rodava a prova
1 inteira, em vez de só os hashes. Agora eles param e dizem qual opção não
entenderam.

## GIFs mais rápidos

Os GIFs deste devlog saem de uma ferramenta que repete um replay e junta
os quadros. Juntar os 1.800 quadros de um GIF, depois que
o jogo tira as imagens, levava 203 s e agora leva 63 s, umas 3,2 vezes mais
rápido. E um teste guarda o hash de dois GIFs pequenos, o mesmo no Windows
e no Linux: se uma versão nova da biblioteca de GIFs mudar um único byte, ele
falha.

## O aceite que contava errado

Cada entrega tem um **aceite**, um comando que confere os critérios da
especificação (a *spec*) contando os testes de cada um pelo nome.
Nesta entrega, dois testes de mesmo nome, um no editor e outro no jogo,
viravam um só na conta. Agora o aceite recusa um nome repetido num
critério; nas etapas 1 e 2, não achou nenhum.

Dos 20 critérios desta entrega, os 14 que o aceite confere passaram, com 29
testes. Ao todo, passam 871 testes, e 297 no WebAssembly.

## O que vem agora

A entrega 2 põe num lugar só o que roda a cada passo, para a janela e os
testes usarem o mesmo código. A física começa na entrega 4.
