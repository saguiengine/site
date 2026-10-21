# Site da Sagui

O site público da Sagui, uma engine de jogos 2D: a página inicial e o devlog,
em português e inglês. A engine fica em outro repositório, privado.

O site está em prévia. No endereço provisório (`*.pages.dev`) e nas prévias
de pull request, as páginas pedem aos buscadores que não as indexem
(`noindex`); com o domínio ligado, o site e o devlog ficam visíveis na busca
(D383).

## Montar o site

Com o [Zola](https://www.getzola.org/) 0.23.6 (D380) e o Python 3.11 ou mais
novo:

```
python build.py        # gera public/, com o endereço do identity.toml
zola serve             # para ver ao vivo em http://127.0.0.1:1111
python scripts/check_brand.py
python scripts/check_site.py      # endereço, E9.4, imagens, milhar e 404
python scripts/check_touch.py     # alvos de toque no celular (precisa do Chrome)
python -m unittest discover -s scripts -p "test_*.py"
```

O `build.py` passa o endereço ao `zola build`. No Cloudflare Pages, a
`main` usa o endereço fixo do projeto (`https://<projeto>.pages.dev`) até o
domínio ser ligado; cada prévia usa o endereço da sua branch
(`https://<branch>.<projeto>.pages.dev`). O endereço nunca depende do
deployment, que muda a cada deploy. O `build.py` também escreve o `_headers`
do `noindex` (D383) e move a 404 em inglês para `en/404.html`.

## A marca (D276, D379)

O nome da engine, o da linguagem, o handle, o endereço do site e a frase do
rodapé (a pronúncia e o sentido do nome, em pt e en) vêm só do
`identity.toml`. Esse arquivo é uma cópia do repositório da engine, feita lá
pelo `cargo xtask copy-site-identity` e trazida para cá num PR. **Não edite o
`identity.toml` aqui.** Uma checagem semanal no repositório da engine avisa se
a cópia ficar para trás.

- Os templates leem a marca com `load_data(path="identity.toml")`.
- Os textos, posts inclusive, usam os componentes `{{ <marca /> }}`,
  `{{ <linguagem /> }}` e `{{ <repositorio /> }}` (em
  `templates/components.html`).
- O `scripts/check_brand.py` falha se a marca aparecer escrita fora do
  `identity.toml`. Ele também faz o teste da E9.2: monta uma cópia do site
  com outra marca no `identity.toml` e confere que nenhuma página mostra a
  marca de verdade. O texto desenhado em imagens fica de fora.
- A única exceção são os dois arquivos do post sobre o nome e a marca
  registrada (`content/devlog/o-nome-e-a-marca/index.md` e `index.en.md`,
  aprovada em 21/10/2026): ele escreve o nome de verdade e marcas de
  terceiros de propósito, e precisa dizer o mesmo se o nome mudar. A
  checagem pula só esses dois caminhos, e a cópia da E9.2 os deixa de fora;
  o `scripts/test_check_brand.py` confere que a exceção não vale para outro
  arquivo.

## Imagens (D388)

As imagens dos posts entram pelo componente `{{ <figura src="..." alt="..."
lang="pt" /> }}` (em `templates/components.html`): ela abre no tamanho cheio
numa aba nova, avisa leitores de tela que abre em nova aba, no idioma da
página, e aceita uma legenda (`caption`). Nada disso usa script.

Imagens com interface (o editor, o jogo, mensagens) têm uma versão em pt e
outra em en, com `.en.` no nome da inglesa. As do post da etapa 0 são o
registro da etapa e ficam só em pt; no post em en, o texto alternativo e a
legenda dizem que estão em português. Uma imagem sem texto leva
`has_text={false}`. O `scripts/check_site.py` confere tudo isso.

## Licenças (D378)

- **Código do site** (templates, estilo e scripts): [MIT](LICENSE).
- **Conteúdo** (textos, devlog e imagens feitas pelo projeto):
  [CC BY 4.0](LICENSE-CC-BY-4.0.txt).
- **Exemplos de código em SaguiScript**: [CC0 1.0](LICENSE-CC0-1.0.txt).
- **O nome e o logo da Sagui** ficam fora de qualquer licença.
- **Material de terceiros**, como as fontes: a licença de cada um, nos
  [créditos](CREDITOS.md).

Contribuições são aceitas sob as mesmas licenças: quem manda um pull request
concorda que ele entra sob a licença da parte que muda.

## Autoria (D381)

Os commits levam o nome "Guilherme Cruz" com o e-mail noreply do GitHub,
nunca um e-mail pessoal. O rodapé do site diz "feito por Guilherme e
comunidade".

## Publicação

O Cloudflare Pages monta o site a cada push:

- **Build command:** `python3 build.py`
- **Build output directory:** `public`
- **Variável:** `ZOLA_VERSION` = `0.23.6`, a mesma do CI
  (`.github/workflows/ci.yml`)
- **Variável `DOMAIN_LIVE` = `1`:** só depois de ligar o domínio, para a
  `main` usar o endereço do `identity.toml` e ficar visível na busca (D383).

A `main` vira o site, e cada pull request ganha um endereço de prévia. O CI
roda só em runners da nuvem do GitHub.
