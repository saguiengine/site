+++
title = "Devlog da etapa 2: as peças e as fases"
date = 2026-10-27
description = "A etapa 2 deu à engine as peças, as fases e os arquivos que guardam um jogo, e terminou com o primeiro jogo de exemplo: o macaquinho andando por uma fase em pixel art, com a câmera seguindo."

[extra]
stage = "2"
thumbnail = "meu-jogo-miniatura.png"
thumbnail_has_text = false
+++

*Os números são provisórios: medi no meu PC, e os oficiais vão sair de um
notebook modesto que ainda vai chegar. Os desta página são da medição do fim
da etapa e podem diferir um pouco dos posts de cada entrega.*

A etapa 1 construiu a base da {{ <marca /> }}: o mesmo jogo em todo
computador, o desenho, os controles, o som, o jogo na própria janela e a casca
do editor. Faltava o que vai em cima dela. A etapa 2 trouxe as **peças**, cada
coisa que existe num jogo (o jogador, uma plataforma, um texto), e as
**fases**, o lugar onde as peças ficam. Ela terminou com o primeiro jogo de
exemplo.

Faço a {{ <marca /> }} com a ajuda do Claude, uma inteligência artificial: ele
escreve o código e faz as medições, e eu reviso, jogo e decido o que entra.
Foram doze entregas, contadas em oito posts curtos: o primeiro juntou as
quatro primeiras, e só a 11 ficou sem post. Este junta tudo, conta a revisão
do fim da etapa e o que deu errado.

Três palavras aparecem bastante:

- **Passo:** o jogo recalcula o mundo 60 vezes por segundo, sempre no mesmo
  ritmo. Cada recálculo é um passo (um *tick*).
- **Quadro:** cada imagem desenhada na tela (um *frame*).
- **ms:** um milésimo de segundo. A 60 imagens por segundo, cada quadro tem
  uns 16,7 ms para ficar pronto.

## O que a etapa 2 entregou

### As peças e a árvore

As peças de uma fase ficam numa árvore: uma peça pode ter peças dentro dela
(as *filhas*), como um carro que leva as rodas junto quando anda. Essa árvore
aparece no editor num painel chamado **Montagem** (a *scene tree* de outras
engines). E o jogo pode ser congelado em qualquer passo, gravado num arquivo
e continuar dali depois, com o mesmo resultado de quem nunca parou. Por
enquanto, isso é uma ferramenta de teste; o save do jogo chega na etapa 11a.
Com 5.000 peças se mexendo, um passo leva 0,133 ms, e o limite no PC é
0,5 ms. [A árvore de peças](@/devlog/a-arvore-de-pecas/index.md) conta mais.

### Os arquivos

Um projeto agora é uma pasta. O projeto, cada fase e cada molde são arquivos
de texto, e cada imagem, som e fonte ganha ao lado uma ficha (o *.meta*). Cada
peça e cada arquivo ganham um número de identidade (um *ID*) que não muda
quando o nome muda, para nada se perder ao renomear. Uma fase de 5.000 peças
abre em 36 ms, e o limite no PC é meio segundo.
[Como a engine guarda uma fase](@/devlog/como-a-engine-guarda-uma-fase/index.md)
explica.

### Os moldes

Um **molde** é uma peça-modelo que se repete pela fase (um *prefab*): uma
moeda desenhada uma vez vira cem moedas, e mudar o molde muda as cem. Uma
cópia pode mudar só o que precisa, e um molde pode ter outro dentro dele. As
peças também ganharam o interruptor **Ativa**, que desliga uma peça sem
apagá-la. [Moldes, cópias e o interruptor Ativa](@/devlog/moldes-e-o-interruptor-ativa/index.md).

### A imagem, a câmera e o texto

O projeto escolhe o estilo, *pixel art* (o desenho feito de quadradinhos
visíveis) ou HD (alta resolução, com o desenho liso), e um jeito de a imagem
caber em qualquer tela. A **Câmera** segue o jogador e para nas bordas da
fase. [A imagem que cabe em qualquer tela](@/devlog/a-escala-e-a-camera/index.md).
O jogo também ganhou a peça **Texto**, que mostra as frases no idioma de quem
joga, com uma fonte de pixel art guardada no próprio projeto.
[O texto do jogo](@/devlog/o-texto-do-jogo/index.md).

### O painel Desempenho

O editor ganhou um painel que mostra, enquanto o jogo roda, quantas imagens
por segundo o jogo mostra, quanto tempo cada quadro leva e quanto vai para a
lógica e para a placa de vídeo; e o jogo ganhou um resumo na própria janela,
com a tecla F3. Medir custa 0,018 ms por quadro, e o limite no PC é 0,05 ms.
[O painel Desempenho](@/devlog/o-painel-desempenho/index.md).

### O editor abre o projeto

O editor abre um projeto e mostra a Montagem e os arquivos. Por enquanto, é só
para ver: editar chega na etapa 5. Do início do programa até a Montagem
aparecer, leva meio segundo, e o limite no PC é 1,5 segundo.
[O editor abre o projeto](@/devlog/o-editor-abre-o-projeto/index.md).

{{ <figura src="editor-projeto.png" alt="O editor com o projeto de teste aberto: a árvore da fase level1 na Montagem, com a Câmera, o Jogador, o Chão, três moedas, uma nuvem desligada e a placa, e os Arquivos com as seis categorias e quantos arquivos cada uma tem" lang="pt" /> }}

### O primeiro jogo de exemplo

O **Meu Jogo** é uma fase de três telas em pixel art. O macaquinho anda pela
fase, entre o chão de grama e as plataformas de tábua (por enquanto para
qualquer lado, até pelo ar, porque ainda não há gravidade), e a câmera o
acompanha até o fim da fase. A placa no começo fala o idioma de quem joga. O
jogo mostra o primeiro quadro 0,6 segundo depois de abrir, e o limite no PC é
0,75 segundo; 99% dos quadros ficam prontos em menos de 3 ms.
[O primeiro jogo de exemplo](@/devlog/o-primeiro-jogo-de-exemplo/index.md).

{{ <figura src="meu-jogo-600.png" alt="O começo do Meu Jogo: o macaquinho no chão de grama, embaixo de uma placa de madeira que diz Use as setas para andar, com plataformas de tábua, nuvens e o fundo de montanhas e morros" lang="pt" has_text={true} /> }}

### E as arrumações

Três entregas foram de arrumação. A primeira deixou o editor igual ao desenho
das telas (o *mockup*), com os acertos que a revisão das etapas 0 e 1 pediu, e
o logo virou o rostinho do macaquinho em pixel art. A segunda fez o relatório
de cada entrega dizer, para cada critério, o valor medido, o limite e a folga,
e não só "passou". [A árvore de peças](@/devlog/a-arvore-de-pecas/index.md)
conta as duas. A terceira arrumou os testes automáticos e trouxe para o meu PC
a parte do robô que roda os testes a cada mudança (a *integração contínua*, ou
*CI*) que ainda rodava na nuvem. O porquê está em "O que deu errado", mais
abaixo.

## A revisão de fim de etapa

Antes de começar a etapa 3, parei para revisar a etapa 2 inteira. Um auditor,
uma inteligência artificial como o Claude, comparou o plano com ele mesmo e
depois com o código e com o mockup. Achou coisas como uma decisão que eu tinha
tomado e não estava escrita no plano, e textos que ainda descreviam o jeito
antigo. Saíram da revisão:

- o plano, os textos e o código alinhados;
- os números medidos das doze entregas guardados junto com o código;
- duas regras novas de trabalho: toda mudança no código passa pelo testador,
  o conferente que não participou da obra (as só de texto, não), e uma decisão
  minha entra no plano no mesmo dia;
- o plano refeito com o tempo real da etapa 2, que foi bem mais rápida do que
  eu esperava, porque quase tudo nela era a base por dentro, que não precisa
  ser jogada para ser aprovada. As próximas etapas dependem de eu jogar e
  ajustar, e isso não acelera do mesmo jeito.

## O que deu errado (e como resolvi)

- **Os minutos da nuvem acabaram.** Parte dos testes automáticos, os do Linux
  e os do navegador, rodava em computadores do GitHub, na nuvem, com uma cota
  de minutos por mês, e a cota de outubro acabou no dia 25. Em vez de pagar
  mais, essa parte veio para o meu PC, que já rodava os do Windows, num Linux
  que roda dentro do Windows (o *WSL*), separado dele: o código dos testes não
  alcança os arquivos, a placa de vídeo nem os programas do Windows. Agora os
  testes não custam nada e levam de 7 a 10 minutos.
- **O PC travava durante os testes.** Com os testes do Linux e os do Windows
  rodando ao mesmo tempo, a memória acabou: sobrou 0,1 GB. Pus um teto na
  memória do Linux e menos tarefas ao mesmo tempo, e no pior momento agora
  sobram quase 8 GB.
- **A luz caiu.** Caiu no meio de um teste e estragou alguns arquivos do
  registro de versões (o *Git*) na pasta onde o Linux roda os testes. Apaguei
  só os estragados, sem perder o resto, e o passo a passo ficou escrito para a
  próxima vez.

## O que falta

- **O notebook:** os números oficiais das etapas 0, 1 e 2.
- **A lista do que desenhar:** com 5.000 peças, montar a cada quadro a lista
  do que vai para a tela leva 0,78 ms, acima do limite do PC (0,5 ms). Esse
  número só é anotado, sem reprovar, mas a etapa 3 vai cuidar dele, já na
  spec.
- **Metas folgadas demais:** três metas sobraram mais de 80%. Nas próximas
  etapas, os limites ficam mais perto do medido, com uma margem, para uma
  piora aparecer.

Com isso, a etapa 2 está fechada. A etapa 3 traz a física: a gravidade, as
colisões e o pulo de verdade. O macaquinho, que até agora só anda, vai pular.
