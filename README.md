# Site da Sagui

O site público da Sagui, uma engine de jogos 2D: a página inicial e o devlog,
em português e inglês. A engine fica em outro repositório, privado.

O site está em prévia: as páginas pedem aos buscadores que não as indexem
(`noindex`) até o lançamento.

## Montar o site

Com o [Zola](https://www.getzola.org/) 0.23.6 (D380) e o Python 3.11 ou mais
novo:

```
python build.py        # gera public/, com o endereço do identity.toml
zola serve             # para ver ao vivo em http://127.0.0.1:1111
python scripts/check_brand.py
```

O `build.py` passa o endereço ao `zola build`. No Cloudflare Pages, cada
prévia usa o próprio endereço; a `main` também, até o domínio ser ligado.

## A marca (D276, D379)

O nome da engine, o da linguagem, o handle e o endereço do site vêm só do
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
  `main` usar o endereço do `identity.toml`.

A `main` vira o site, e cada pull request ganha um endereço de prévia. O CI
roda só em runners da nuvem do GitHub.
