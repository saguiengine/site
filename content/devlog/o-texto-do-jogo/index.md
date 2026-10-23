+++
title = "Nota: o texto do jogo, no idioma de quem joga"
date = 2026-10-22
description = "A entrega 8 traz a peça Texto e os idiomas do jogo: placas e frases que aparecem no idioma de quem joga, com letras iguais em qualquer computador."

[extra]
note_stage = "2"
thumbnail = "nota-miniatura.png"
thumbnail_has_text = false
+++

*Uma nota curta da etapa 2, sobre a entrega 8.*

Até agora, as peças do jogo só mostravam imagens. A entrega 8 traz a peça
**Texto**: uma placa, um placar, um aviso na tela. E traz os idiomas do
jogo, para cada frase aparecer na língua de quem joga.

## Uma chave para cada frase

A peça Texto não guarda a frase, e sim uma **chave**, um nome que vale em
todos os idiomas, como `level1.sign.text`. A frase de cada idioma fica num
arquivo à parte, um por idioma, no *Fluent*, um formato de arquivo de
traduções. No arquivo, o ponto da chave vira hífen:

```
# pt-BR.ftl
level1-sign-text = Use as setas para andar

# en.ftl
level1-sign-text = Use the arrow keys to walk
```

Para um texto igual em todos os idiomas, como o nome do jogo, a peça tem a
caixa **Não traduzir**, e a frase fica nela mesma.

## Qual idioma aparece

Na primeira vez, o do sistema de quem joga (no navegador, o do navegador).
Se o jogo não tem esse idioma, ele segue uma **cadeia de reservas** (o
*fallback*) que o projeto define, por exemplo de pt-PT para pt-BR, até
chegar ao idioma em que o jogo foi escrito. Uma frase
nunca aparece em branco: o que falta num idioma vem do seguinte.

Uma chave que não existe em idioma nenhum aparece na tela entre colchetes,
como `[level1.sign.text]`, e o jogo avisa uma vez no registro (o *log*).
Um erro de digitação no arquivo de um idioma é avisado com a linha e a
coluna, e o resto das frases continua valendo.

## Letras iguais em todo computador

O jogo nunca usa as fontes instaladas no computador. A engine desenha
fontes TTF e OTF, os arquivos de fonte comuns, e fontes *bitmap*: um PNG
com as letras em grade, comum no *pixel art* (o
desenho feito de quadradinhos visíveis). As letras que o processador monta
saem idênticas, até o último byte, no Windows, no Linux e no macOS. As
fontes do próprio projeto chegam ao jogo na entrega 10.

No pixel art, as bordas das letras não são suavizadas (o *antialiasing*):
cada pixel liga ou desliga. No HD, o estilo de alta resolução, as letras
TTF e OTF saem suaves.

{{ <figura src="texto-pixel.png" alt="Um teste da entrega 8 em pixel art, com uma fonte bitmap: no alto, a frase Ação, você e à toa: 1.516!; no meio, as palavras ação, você e à, uma embaixo da outra, alinhadas no mesmo ponto pelo início, pelo centro e pelo fim; embaixo, a frase Use as setas para andar e o espaço para pular à vontade, duas vezes, quebrada em quatro linhas: à esquerda, alinhada pelo início; à direita, pelo fim." lang="pt" caption="Um teste real da entrega 8: acentos, quebra de linha e alinhamentos." has_text={true} /> }}

## A fonte que vem do estilo

Um Texto sem fonte escolhida usa a fonte do estilo do projeto: a IBM Plex
Sans no HD e a monogram no pixel art. A monogram é de datagoblin (Vinícius
Menézio) e tem licença CC0, de uso livre.

A monogram entrou por um achado do testador, o conferente que não
participou da obra: na primeira conferência, a Plex pequena e sem suavizar
saía falhada no pixel art.

{{ <figura src="texto-antes-depois.png" alt="A frase Vidas: 3, em vermelho sobre o chão verde de um teste, ampliada, lado a lado: à esquerda, na Plex pequena, com letras falhadas e tortas; à direita, na monogram, com letras retas e nítidas." lang="pt" caption="O mesmo placar na Plex (à esquerda) e na monogram (à direita)." has_text={true} /> }}

A monogram não tem 20 letras do alfabeto cirílico usadas no sérvio, no
macedônio e no bielorrusso. Na fonte padrão, essas letras saem da Plex, no
mesmo tamanho e sem suavizar, e nenhuma aparece como uma caixa vazia.

## O que o testador achou

Ele também viu que os testes automáticos usavam o idioma do
computador, e uma rodada de teste podia sair diferente no meu PC e na
nuvem. Agora, nos testes, vale o idioma em que o jogo foi escrito, a não
ser que o teste peça outro. E achou que, com o idioma escrito
`pt-br` no projeto, o Linux, que diferencia maiúsculas, não achava o
arquivo `pt-BR.ftl`, e nada avisava. Os dois foram corrigidos, cada um com
um teste.

## O que vem agora

A entrega 9: o editor abrindo o projeto, só para ver as peças da fase e os
arquivos.
