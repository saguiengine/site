+++
title = "O nome Sagui e a marca registrada"
date = 2026-10-21
description = "Gostar de um nome não basta: é preciso ver se ele pode virar marca. Uma busca no INPI achou um SAGUI de software, e o nome da engine pode mudar antes da etapa 4. Por que isso não assusta: o nome mora num arquivo só."

[extra]
thumbnail = "nome-miniatura.png"
thumbnail_has_text = false
+++

*Um post especial, fora das entregas.*

O nome Sagui veio no começo do projeto. Ele esconde o "Gui" de Guilherme,
é brasileiro, é fácil de falar em inglês (sa-GWEE) e já vem com mascote: o
macaquinho que aparece no logo e nos exemplos. Mas gostar de um nome não
basta. Antes de lançar, é preciso saber se ele pode virar **marca**.

{{ <figura src="nome-cena.png" alt="Desenho: no meio, um arquivo com o macaquinho do logo e linhas coloridas; quatro setas saem dele para uma janela do editor, uma página do site, um arquivo de script e um balão de mensagem de erro." lang="pt" has_text={false} /> }}

## O que é uma marca

Uma marca registrada dá o direito de usar um nome com exclusividade num
tipo de produto. No Brasil, quem registra é o INPI, o Instituto Nacional
da Propriedade Industrial. O registro vale por **classes**, grupos de
produtos e serviços: um programa para baixar fica na classe 9, um serviço
de software pela internet na 42, e cursos e entretenimento na 41. Por isso
podem existir um "Sagui" de óculos e outro de software sem briga: as
classes são diferentes.

## O que a busca achou

Fiz a primeira busca no INPI em 16/10, e a classe 9 parecia livre. Só que
o campo da classe pede dois dígitos, "09", e eu tinha digitado "9". Refeita
em 18/10, a busca mostrou outra coisa:

- na classe 9, a marca SAGUI (Sistema de Apoio à Gestão e Uso da
  Inovação), da Unicamp, para programas de computador, em vigor até 2036;
- na classe 42, duas marcas ligadas a software, sagui.ai e Saguitech;
- e um pedido de "Sagui Studio" que o INPI já recusou, por parecer demais
  com marcas mais antigas.

O INPI compara os nomes pelo som e pela ideia, e acrescentar uma palavra,
como "Engine" ou "Studio", não resolve: a lei fala em reproduzir uma marca
"ainda que com acréscimo". Isso não quer dizer que existe um conflito.
Quem avalia isso é um especialista, e nada aqui é parecer jurídico. Quer
dizer que a dúvida é séria o bastante para ser resolvida antes de lançar, e
não depois.

## O nome mora num arquivo só

Desde o começo, a engine foi feita para essa hora. A marca, o nome da
linguagem, a extensão dos scripts (`.sagui`) e as letras dos códigos de
erro moram num arquivo só, o `identity.toml`. O código usa nomes neutros, e
um teste automático falha se a marca aparecer escrita em qualquer outro
lugar. O editor, as mensagens e o próprio site leem o nome desse arquivo.

{{ <figura src="nome-editor-logo.png" alt="O canto da barra de cima do editor: o logo, com o macaquinho num quadrado azul, o nome Sagui ao lado e o menu Arquivo." lang="pt" caption="O editor de verdade: o nome ao lado do logo vem do identity.toml." /> }}

Trocar o nome hoje é mudar esse arquivo, o logo e alguns desenhos. O que
fica caro é trocar depois: quando a extensão estiver nos projetos das
pessoas, os instaladores tiverem saído e o nome estiver em vídeos e
tutoriais. Por isso a decisão tem data.

## O que vem agora

Antes da etapa 4, quando a linguagem de script ganha a forma final, vou
consultar um agente de propriedade industrial, o profissional que cuida de
registros de marca no INPI, e decidir: manter Sagui ou trocar. Já existem
alguns nomes reserva conferidos, que ficam guardados por enquanto, para
ninguém registrá-los antes. Quando a decisão sair, ela vira um post aqui.
