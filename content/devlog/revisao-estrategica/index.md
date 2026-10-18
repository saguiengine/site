+++
title = "Devlog: uma pausa para replanejar"
date = 2026-10-17
description = "Antes de construir as peças, parei para comparar a engine com o Godot, a Unity e o GameMaker. Saiu um plano maior: o que melhora, o que fica de fora da 1.0 e o que a arquitetura deixa pronto para depois."
+++

*Os números são provisórios: medi no meu PC, e os oficiais vão sair de um
notebook modesto que ainda vai chegar.*

A etapa 2 começou em 16/10. É a etapa das peças e das fases: das coisas que
existem no jogo (o jogador, uma moeda, uma plataforma) e das fases, os níveis
do jogo, salvos em arquivo. É a primeira etapa em que o jogo deixa de ser um
quadrado sozinho. No dia seguinte, antes de escrever a primeira peça, eu parei
tudo.

O motivo foi uma pergunta simples: o que o Godot, uma engine de código aberto
muito usada para jogos 2D, consegue fazer que a {{ <marca /> }} não consegue?
Baixei o Godot, comecei a comparar, e a lista cresceu rápido. Várias respostas
dependiam de decisões que ficam caras de trocar depois. Por exemplo: como cada
peça guarda os seus dados, como o jogo salva o próprio estado, como a
{{ <linguagem /> }} conversa com a engine. Mudar isso na etapa 2 custa dias.
Mudar na etapa 8, com o editor e os tiles construídos em cima,
custa refazer metade do que já existe.

Então a regra ficou esta: tudo o que o Godot faz em 2D tem que ser possível
na {{ <marca /> }}. "Possível" pode ser de quatro jeitos:

- **pronto:** já vem na engine, e é só ligar (uma câmera que segue o jogador);
- **por script:** você escreve algumas linhas de {{ <linguagem /> }} (um
  inimigo que foge quando a vida está baixa);
- **por pacote:** alguém junta peças prontas, scripts e imagens, e você instala
  no projeto (um sistema de diálogos);
- **por módulo:** um pedaço de código rápido, escrito em outra linguagem, para
  as contas pesadas (uma simulação de milhares de grãos de areia).

O que pedir uma parte nova da engine vai para o roteiro. O que fica
de fora, fica de propósito, com o motivo escrito.

## Como foi a revisão

Faço a {{ <marca /> }} com a ajuda do Claude, uma inteligência artificial. Na
revisão, ele trabalhou em várias frentes ao mesmo tempo: comparando, medindo e
conferindo. Eu li os relatórios e decidi.

### Três engines, item por item

Comparei o Godot, a parte 2D da Unity e o GameMaker com o plano da
{{ <marca /> }}. Cada linha da comparação é um recurso, ou seja, uma coisa que
a engine faz: "a câmera segue o jogador", "importar arte de outro programa",
"uma junta que prende duas peças". Juntando o que as três falavam sobre a mesma
coisa, ficaram cerca de 340 recursos. Para cada um, a tabela diz o que a
{{ <marca /> }} já tem, o que falta e em que etapa entra.

### Medir antes de decidir

Quando a dúvida era de velocidade, o Claude escreveu programas pequenos de
teste, só para medir, e jogou fora depois. Foram seis perguntas:

- **Quantas vezes por segundo o jogo deve recalcular o mundo.** Hoje são 60
  passos por segundo. Mais passos deixam o controle mais rápido, mas custam
  mais. As medições ainda dependem de um teste meu: jogar sem saber qual taxa
  está ligada e dar uma nota.
- **Quanto custa um efeito de ruído escrito em script.** Ruído (*noise*), aqui, não
  é som: é um sorteio suave. Em vez de números que pulam ao acaso, ele dá
  valores que mudam aos poucos, como o desenho de morros. É a ferramenta clássica da geração procedural (*procedural generation*):
  criar conteúdo por regras, em vez de desenhar tudo à mão. Num jogo de cavernas que mudam a cada partida,
  o ruído decide onde tem rocha e onde tem passagem. Também serve para nuvens,
  terrenos e o tremor natural de uma câmera.
- **Quanto custa desenhar milhares de imagens.** As imagens do jogo ficam
  coladas em folhas grandes, as páginas (o *texture atlas*), para a placa de vídeo desenhar muitas
  de uma vez. A medição mostrou um jeito de desenhar tudo de uma vez só, mesmo
  quando as imagens vêm de páginas diferentes.
- **Quanto custa salvar e restaurar o jogo inteiro.** É o que permite salvar a
  qualquer momento (*save state*), voltar no tempo e, um dia, jogar online
  com *rollback*.
- **Quanto custa a {{ <linguagem /> }} ler e mudar 5.000 peças** a cada passo,
  como num jogo cheio de inimigos, moedas e projéteis.
- **O mesmo resultado em todo lugar** (o jogo é *determinístico*). Uma partida gravada, com os botões
  apertados em cada passo, deu exatamente os mesmos números no Windows, no
  Linux, no Mac e em *WebAssembly*, o formato dos programas que rodam no
  navegador. É isso que permite assistir de novo a uma
  partida e achar um erro repetindo a mesma jogada.

### Decisões em rodadas

Foram três rodadas de perguntas, com cerca de 150 decisões. As que só eu
podia tomar vieram uma a uma. As técnicas vieram em bloco, depois de eu ler o
porquê de cada uma. Depois, três conferências procuraram contradições entre o
plano, o código e o desenho das telas.

## O que melhora

### Na física

- **Juntas** (*joints*): um pino, uma mola ou uma corda prendendo duas peças. Com elas,
  dá para fazer uma ponte de tábuas que balança quando o jogador passa, uma
  bola presa numa corrente, ou um carrinho com rodas que giram. Antes, as
  juntas estavam para depois da 1.0, porque eu achava que precisavam de um
  editor próprio. O Godot mostrou que não: a junta é uma peça que liga duas
  outras, e o ponto onde ela fica é o ponto de apoio.
- **Mais de uma forma de colisão por peça** (vários *colliders*). Por exemplo, o corpo do jogador para bater
  nas paredes e um sensor pequeno nos pés para saber se ele está no chão.
- **Zonas que empurram** (os *effectors* da Unity): uma corrente de vento que joga o jogador para o lado,
  água que puxa para cima, uma esteira que leva as caixas.
- **Caminhos** (*paths*): uma plataforma que vai e volta por um trajeto desenhado na
  fase, sem script.
- **Perguntas sobre o espaço** (*overlap queries* e *raycasts*): "o que está dentro deste círculo?" (uma
  explosão que atinge tudo em volta) ou "o que esta linha encontra primeiro?"
  (o inimigo enxerga o jogador, ou tem uma parede no meio?).

### No desenho

- **Efeitos prontos, sem escrever shader.** Um shader é um programinha que
  roda na placa de vídeo e decide a cor de cada pixel. Nas outras engines,
  quase todo efeito pede escrever um. Na 1.0 da {{ <marca /> }}, os mais
  comuns vêm prontos:
  - o jogador pisca em vermelho ao levar dano;
  - o inimigo derrotado some se desfazendo em pedaços;
  - a peça escolhida ganha um contorno;
  - o jogo fica em tons de cinza na pausa;
  - as luzes se somam, em vez de cobrir o que está atrás.
- **Uma câmera melhor.** Ela ganha uma zona morta (*dead zone*): o personagem anda um pouco
  sem a câmera se mexer, e a tela fica mais calma. E ganha antecipação (*look-ahead*): quando
  o personagem corre, a câmera olha um pouco à frente, para o jogador ver o
  buraco antes de cair nele.
- **Arte do Aseprite.** O Aseprite é um programa muito usado para desenhar
  pixel art. O arquivo dele entra direto, com as camadas e as animações, sem
  exportar imagem por imagem.

### No editor

- **Selecionar clicando no jogo rodando, pausar e avançar um passo de cada
  vez.** Se um inimigo atravessa o chão de vez em quando, dá para pausar no
  momento, avançar passo por passo, clicar nele e ver os valores dele.
- **Uma paleta de comandos** (*command palette*, como a do VS Code): um atalho abre uma caixa, você digita
  "duplicar" e escolhe "Duplicar peça". Serve para qualquer ação do editor, e
  ajuda muito quem prefere o teclado.
- **Um painel solto** (*floating panel*): dá para tirar um painel do lugar, como o das mensagens,
  e deixá-lo flutuando por cima da fase.
- **Desfazer em tudo** (*undo*), até no pincel de pixels e no de tiles (os pedaços
  quadrados que montam o cenário, num *tilemap*).
- **"Se" nas Reações.** As Reações são frases prontas para quem ainda não
  programa, como "quando o jogador tocar a moeda, some a moeda e soma 1 ponto".
  Agora elas aceitam uma condição simples: "se tiver a chave, abre a porta" ou
  "se as moedas chegarem a 10, toca a música da vitória".

### Na {{ <linguagem /> }}

- **Funções como valor** (*first-class functions*). Dá para entregar uma ação para ser feita depois:
  `after(1, explode)` quer dizer "daqui a 1 segundo, explode". E chega a
  `lambda`, uma função curtinha escrita na hora, sem nome, como a do Python:
  `sort(enemies, key=lambda e: e.hp)` ordena os inimigos pela vida. Quem já
  programa sente falta disso logo.
- **Mais acesso ao jogo:** o mouse; perguntar se a peça está no chão ou
  encostada na parede; os raios (raycast: a linha que pergunta o que encontra); e a
  força e o impulso nas peças soltas, como um empurrão contínuo de vento ou o
  golpe de uma explosão.
- **Um inimigo que já patrulha e persegue,** sem escrever nada: ele anda de um
  lado para o outro, vira na beirada e corre atrás do jogador quando o vê.
- **O caminho mais curto** (*pathfinding*), pronto e rápido: num mapa de tiles, o inimigo
  acha o caminho até o jogador desviando das paredes, como num labirinto. A
  conta tem um nome, A*.

### No jogo que você exporta

- **O kit de interface completo** (a *UI*), as peças das telas de menu: além de botões e
  barras, um interruptor (*toggle*: a música, ligada ou desligada), um seletor
  (*dropdown*: o idioma), um campo de texto (*text input*: o nome do jogador)
  e uma lista que rola (*scroll list*: os botões do controle, um embaixo do
  outro). Sem eles, o menu de opções do jogo
  de exemplo não fechava. Um protótipo do menu também mostrou como a interface
  se ajusta a qualquer tamanho de tela.
- **Tela cheia** (*fullscreen*) com Alt+Enter, e **som no navegador**, que hoje ainda é mudo.

### Por dentro

É a parte que menos aparece e a que mais mudou. Três medições, para dar a
escala (todas no PC, provisórias):

- **Salvar no meio de qualquer coisa.** O jogo agora salva tudo, até um script
  parado no meio de uma espera. Imagine um baú que abre devagar, em três
  segundos: se você salva no meio, ao carregar ele continua abrindo do mesmo
  ponto. Com 1.500 peças e 500 esperas paradas, salvar leva 0,2 ms e
  restaurar, 0,5 ms. Um ms é um milésimo de segundo.
- **Muitas peças com script.** Com 5.000 peças, cada uma com o seu script, um
  passo leva 0,64 ms. A 60 passos por segundo, cada quadro tem 16,7 ms, então
  isso é menos de um vigésimo do tempo.
- **O ruído vem pronto.** Escrito como script, no protótipo da {{ <linguagem /> }} da
  etapa 0, ele ficou de 37 a 87 vezes mais lento que dentro da engine. Por isso o ruído e o caminho mais
  curto vêm prontos, e o script só chama: `noise.perlin(x, y)`.

## O que fica de fora da 1.0

Cada item tem um motivo, e quase todos entram depois.

- **Leitor de tela nos jogos** (*screen reader*). O leitor de tela é o programa que lê a tela em
  voz alta para quem não enxerga. Na 1.0, cada botão e cada texto do jogo já
  guarda um nome para ele ler, mas a leitura em si vem depois. A do Godot
  ainda é experimental.
- **Linha do tempo de animação** (*timeline*, como o AnimationPlayer do
  Godot), para cenas com várias peças se mexendo
  juntas: a porta abre, a câmera passeia pela sala, o personagem fala. Na 1.0,
  dá para fazer com animações em sequência e esperas no script.
- **Dois jogadores no mesmo computador** (*co-op local*). A engine já guarda os comandos de
  cada jogador separados, então isso entra depois sem refazer nada.
- **Exportar para Mac e para celular.** Na 1.0, o jogo sai para Windows, Linux
  e o navegador, e quem joga no Mac usa a versão do navegador.
- **Consoles.** Não estão no plano. Os kits da Nintendo, da Sony e da Microsoft
  são fechados por contrato, e levar a engine para eles é um projeto à parte.
  Volto a pensar nisso depois da 1.0.
- **Um núcleo do processador para o jogo.** O processador tem vários núcleos,
  como várias pessoas trabalhando ao mesmo tempo. O jogo usa um núcleo para
  calcular cada passo (*single-thread*); o editor, o som e a leitura dos arquivos usam os
  outros. Dividir o cálculo do jogo entre núcleos faria o resultado mudar de
  um computador para outro, porque ninguém garante quem termina primeiro. As
  contas mostram que um núcleo dá conta da 1.0. No navegador, também um só,
  para o jogo rodar em qualquer site, sem configuração especial.
- **Uma linguagem só.** Comparei a {{ <linguagem /> }} com quatro linguagens
  prontas, usadas em outros jogos: Lua, Luau, Wren e Rhai. Nenhuma consegue ao
  mesmo tempo salvar um script parado no meio, como o do baú, rodar no
  navegador e mostrar os erros em português.

## O que a arquitetura deixa pronto para depois

- **Vários núcleos, com o mesmo resultado** (*multithreading*
  determinístico). Fica escrita a regra para um
  sistema usar vários núcleos sem perder o mesmo resultado em todo computador:
  dividir o trabalho em pedaços fixos e juntar sempre na mesma ordem. Ela
  existe para que jogos de simulação de areia e de materiais por pixel sejam
  possíveis depois da 1.0. Neles, cada pixel é um grão que cai, escorre ou
  pega fogo, e são centenas de milhares por segundo.
- **Módulos** (em WebAssembly). Partes rápidas escritas em outras linguagens e chamadas pela
  {{ <linguagem /> }}, como se fossem funções da engine.
- **Lojas.** Conquistas (*achievements*) ("terminou a fase sem levar dano") e placares (*leaderboards*) do
  Steam, por um módulo oficial. Os saves na nuvem do Steam não precisam do
  módulo: o próprio Steam copia a pasta dos saves.
- **Extensões do editor** (*plugins*), feitas pela comunidade. Por exemplo, uma ferramenta
  para desenhar estradas, usando os mesmos comandos que o editor usa por
  dentro.
- **Jogo online** (*multiplayer*), com a exigência de que todos rodem a mesma versão do mesmo
  jogo.

## O preço

O plano ficou maior, e a 1.0 ficou mais longe. Quanto mais longe, só vou saber
depois de medir as horas reais da etapa 2. As etapas 0 e 1 andaram mais rápido do que eu
previa, mas eram de infraestrutura. As próximas dependem mais de eu jogar e
olhar, e isso não se apressa.

Prefiro assim. Os erros de base que a revisão pegou agora custariam muito mais
caro na etapa 8.

## O que vem agora

A etapa 2 volta, agora sobre a base nova: as peças e as fases. No fim dela, a
fase fica salva num arquivo e a câmera segue o jogador.
