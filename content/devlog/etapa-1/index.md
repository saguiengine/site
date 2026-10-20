+++
title = "Devlog da etapa 1: a base da engine"
date = 2026-10-16
description = "A etapa 1 construiu o que todas as outras vão usar: o mesmo jogo em todo computador, o desenho, os controles, o som, o jogo na própria janela ligado ao editor, a casca do editor e este site."

[extra]
stage = "1"
thumbnail = "quadrado-miniatura.png"
thumbnail_has_text = false
+++

*Os números são provisórios: medi no meu PC, e os oficiais vão sair de um
notebook modesto que ainda vai chegar.*

A {{ <marca /> }} é uma engine de jogos 2D, ou seja, um programa para criar
jogos, com uma linguagem própria, a {{ <linguagem /> }}, para dizer como cada
coisa do jogo se comporta (uma linguagem de *script*). Na etapa 0, cinco
provas pequenas (as provas de conceito, ou *PoC*) atacaram os maiores riscos,
e o código delas não entrou na engine. A etapa 1 começou do zero e construiu a
base: as partes que todas as etapas seguintes vão usar. Esse código fica.

*Uma correção: no [post da etapa 0](@/devlog/etapa-0/index.md), eu disse que o
código das provas ia para o lixo. Ele não entrou na engine, mas continua
guardado, sem mudanças, até o notebook medir os números oficiais da etapa 0.
Depois disso, pode sair.*

Faço a {{ <marca /> }} com a ajuda do Claude, uma inteligência artificial: ele
escreve o código e faz as medições, e eu reviso, jogo e decido o que entra. A
etapa 1 teve nove entregas. Cada uma começou por um texto que diz o que ela
precisa fazer (a especificação, ou *spec*) e só terminou com os testes
passando.

Para quem não leu o post da etapa 0, duas palavras aparecem bastante:

- **Passo:** o jogo recalcula o mundo (quem se mexeu, quem bateu em quem) 60
  vezes por segundo, sempre no mesmo ritmo. Cada recálculo é um passo (um
  *tick*).
- **Quadro:** cada imagem desenhada na tela (um *frame*). A 60 imagens por
  segundo (60 *FPS*), cada uma precisa ficar pronta em cerca de 16 milésimos
  de segundo (ms).

## O que a etapa 1 entregou

### O mesmo jogo em qualquer computador

O coração da engine avança o jogo em passos fixos, 60 ou 120 por segundo, e
nunca usa o relógio do computador para decidir o que acontece. Uma partida
gravada de 60 segundos, com os botões apertados em cada passo, termina
exatamente igual (o jogo é *determinístico*) no Windows, no Linux, no Mac e em
*WebAssembly*, o formato dos programas que rodam no navegador. É isso que vai
permitir assistir de novo a uma partida (o *replay*), achar erros repetindo a
mesma jogada e, um dia, jogar online. Um passo com 5.000 quadrados leva
0,068 ms, e o limite no PC é 0,5 ms.

### O desenho

Os *sprites*, que são as imagens de personagens e objetos, são desenhados pela
placa de vídeo (a *GPU*, a parte do computador feita para os gráficos), em
grupo (o *batching*): com 2.000 deles, 99% dos quadros ficam prontos em
2,6 ms, e a meta no notebook é 8,3 ms. Para jogos com pixels grandes, como os
antigos (a *pixel art*), a imagem cresce sempre por um número inteiro (2
vezes, 3 vezes: o *integer scaling*), com faixas nas bordas quando a tela não
tem a mesma proporção (o *letterbox*), para nenhum pixel sair torto. E o
movimento fica suave entre um passo e outro (a *interpolação*), mesmo quando a
tela desenha mais quadros por segundo do que o jogo calcula passos.

### Teclado, mouse e controle

O jogo não pergunta "a tecla Espaço está apertada?". Ele pergunta pelo
comando: pular, atacar, andar, pausar. Um arquivo diz quais teclas, botões do
mouse e botões do controle disparam cada comando (o *input map*), então trocar
os botões não mexe no jogo. Controles de videogame (os *gamepads*) também
valem. Cada aperto entra numa fila com a hora em que aconteceu, e por isso
dois toques rápidos dentro do mesmo passo contam como dois. Se um controle
desconecta no meio do jogo, aparece um aviso, e os botões dele passam a
contar como soltos.

### O som do pulo

A engine toca sons, e o primeiro é o do pulo. O som é gerado pelo próprio
programa, sem arquivo de áudio, e quem decide quando ele toca é o passo do
jogo, e não o relógio do som. Assim, a partida gravada continua igual. Do
pedido até o som chegar à mistura de sons do computador (o atraso, ou
*latência*), levou 25 ms.

### O jogo na própria janela

O jogo abre numa janela própria, que pode mudar de tamanho. Por enquanto, o
jogo de teste é um quadrado que anda e toca o som do pulo. A primeira imagem
aparece em até 0,53 segundo depois de o jogo abrir, e o limite no PC é 0,75
segundo. Na partida gravada de 60 segundos, 99% dos quadros ficaram prontos
em menos de 2,4 ms.

{{ <figura src="quadrado.png" alt="O jogo de teste: um quadrado laranja sobre um fundo escuro" lang="pt" has_text={false} /> }}

### Ligado ao editor

Quando a pessoa aperta Jogar no editor, o jogo abre como um programa
separado (outro *processo*), que conversa com o editor. A etapa 0 provou que
isso funcionava, e agora é para valer:

- **Jogo travado:** o editor percebe em menos de 2 segundos e fecha só o jogo.
- **Jogo que quebra (o *crash*):** o editor percebe em menos de um décimo de
  segundo e mostra uma mensagem com o motivo (no Windows, um tipo de quebra
  demora mais; veja abaixo).
- **Reabrir:** o jogo volta em 10 ms.
- **Mensagens e fotos da tela:** uma mensagem do jogo chega ao editor em
  menos de um décimo de milésimo de segundo, e uma foto da tela do jogo (um
  *screenshot*), em 6 ms.

### A casca do editor

O editor ganhou a casca: a barra de cima, com o botão Jogar, e os painéis
nos seus lugares, ainda vazios. Eles vão ser preenchidos nas próximas
etapas. Há dois arranjos de painéis (*layouts*). O Padrão serve para telas
grandes:

{{ <figura src="editor-padrao.png" alt="O editor no arranjo Padrão: a barra de cima com o botão Jogar e os painéis Montagem, Fase, Propriedades, Arquivos e Console" lang="pt" /> }}

O Compacto serve para telas pequenas, a partir de 1280 × 720 (a *resolução*:
1280 pixels de largura por 720 de altura), com o painel de mensagens (o
*console*) recolhido numa linha embaixo:

{{ <figura src="editor-compacto.png" alt="O editor no arranjo Compacto, numa tela de 1280 por 720, com o Console recolhido numa linha embaixo" lang="pt" /> }}

Na primeira vez em que abre, o editor pergunta o idioma e o perfil de quem
vai usar. Quem está começando passa por três telas; quem já programa passa
por cinco, porque escolhe também o editor de código (o programa em que se
escreve o código, como o VS Code) e a aparência. Tudo pode ser mudado depois,
nas Preferências, e trocar o idioma vale na hora, sem reabrir o programa.

{{ <figura src="primeira-execucao.png" alt="A primeira execução do editor, no passo 1 de 3: a escolha do idioma, entre Português e English" lang="pt" /> }}

O editor inteiro funciona pelo teclado: Tab e Shift+Tab andam pelos botões, e
F6 pula de painel em painel. Os testes automáticos usam o editor como um
leitor de tela (o programa que lê a tela em voz alta, o *screen reader*) usa,
pelos nomes dos botões, e um deles falha se alguma coisa clicável ficar sem
nome para quem não enxerga a tela. Os números: o editor fica pronto 0,4
segundo depois de abrir, e com 10.000 linhas no painel de mensagens, 99% dos
quadros ficam prontos em 2,6 ms.

### Este site

O site que você está lendo também é da etapa 1: em português e em inglês,
sem nenhum programa rodando na página (nenhum *JavaScript*) e sem *cookies*
(os dados que um site guarda no seu navegador, por exemplo para lembrar quem
você é). O nome da engine e o da linguagem vêm de um arquivo só, o mesmo que
o código usa, para nunca aparecerem escritos de dois jeitos.

## A revisão de fim de etapa

Antes de começar a etapa 2, parei para revisar a etapa 1 inteira. O plano,
os textos de cada entrega e o código foram comparados, um por um, para ver se
dizem a mesma coisa. Um conferente que não tinha feito o código, também uma
inteligência artificial, refez os testes de cada entrega, e as metas foram
medidas outra vez no PC. Saíram dessa revisão:

- correções pequenas no código, cada uma com um teste que mostra o erro
  antes da correção (um *teste de regressão*);
- textos alinhados com o que o código faz;
- os testes noturnos conferindo também o que a etapa 1 construiu;
- os números medidos guardados junto com o código.

## O que deu errado (e como resolvi)

- **Os testes que travavam o Windows.** Os testes de desenho rodam vários ao
  mesmo tempo. Quando dois deles abriam a placa de vídeo de jeitos diferentes
  ao mesmo tempo, o programa da placa de vídeo no Windows (o *driver*)
  travava, e os testes automáticos ficaram mais de 20 minutos parados. Agora
  os testes que usam a placa de vídeo esperam a sua vez, e um teste novo
  garante que nenhum fura a fila.
- **O Windows segurando o jogo que quebra.** Quando o jogo quebra de um certo
  jeito, o Windows o segura por um tempo enquanto escreve um relatório do
  erro: uns 2 segundos, e até 35 quando o Windows põe o relatório numa fila.
  Nesse tempo, o editor vê um jogo parado e acha que ele travou. O editor agora
  trata os dois casos, e no Windows o tempo desse tipo de quebra só é
  anotado, sem contar na meta.
- **O teste que falhava de vez em quando.** Por causa do mesmo relatório do
  Windows, esse tipo de quebra levava meio segundo, um pouco mais ou um pouco
  menos que o limite do teste. O teste passava quase sempre. Um teste que
  falha de vez em quando (um teste instável, ou *flaky*) é um erro, e não
  azar, então corrigi o teste.
- **Arquivos do Windows que não abriam.** Algumas ferramentas do Windows
  salvam textos com uma marca invisível no começo (o *BOM*), ou noutra
  codificação (o jeito de guardar cada letra como números, o *encoding*). A
  engine recusava esses arquivos com uma mensagem que não dizia o motivo.
  Agora eles abrem. Um arquivo numa codificação que a engine não lê diz isso
  com todas as letras.

## O que falta

- **O notebook:** os números oficiais das etapas 0 e 1.
- **Metas folgadas demais:** muitas metas sobraram mais de 80% no PC. Vou
  revê-las depois dos números do notebook.

Com isso, a etapa 1 está fechada, e a base está pronta. A etapa 2 traz as
peças (o jogador, uma moeda, uma plataforma) e as fases: o jeito de montar o
mundo do jogo.
