# Fontes editáveis das imagens

[English](README.md) · [Imagens](../README.pt-br.md)

Estas fontes atualizam as ilustrações existentes da **Alpha-v0.2.0-Alkimim** na própria edição. Preservam a paleta azul/ciano, os painéis arredondados, as funções dos ícones, as posições gerais, as dimensões e os pares bilíngues.

| Ilustração | SVG em inglês | SVG em português | Dimensões do PNG |
| --- | --- | --- | --- |
| Banner | [Inglês](oal-banner-en.svg) | [Português](oal-banner-pt-br.svg) | 1766 × 776 |
| Camadas | [Inglês](oal-layers-en.svg) | [Português](oal-layers-pt-br.svg) | 1284 × 1020 |
| Cardinalidade dos casos | [Inglês](oal-map-en.svg) | [Português](oal-map-pt-br.svg) | 1427 × 1058 |

Os SVGs são autocontidos e mantêm textos, ícones, painéis e conectores editáveis. O banner incorpora a marca OAL original e o fundo decorativo restaurado. A marca original e os dois logotipos PNG permanecem inalterados na pasta superior.

## Atualizar os dois idiomas

Edite as entradas correspondentes em [labels.json](labels.json) e execute [render_images.py](render_images.py). O script controla a geometria compartilhada pelos idiomas. Ele grava os seis SVGs nesta pasta e os seis PNGs na pasta superior.

```sh
python -m pip install cairosvg==2.9.1
python assets/sources/render_images.py
```

Execute o último comando na raiz do repositório. O CairoSVG requer Cairo no ambiente. A tipografia usa Arial/Helvetica/Nimbus Sans, com alternativa sans-serif; os PNGs entregues foram renderizados com Nimbus Sans. Confira ambos os idiomas depois de mudar textos ou geometria, especialmente os rótulos mais longos em português. Os PNGs incluídos podem ser usados diretamente, sem instalar as dependências de renderização.

## Significado dos desenhos

- O diagrama de camadas possui um agrupamento ADMV com ADPM e ADVS e um único motor L1–L2.
- O mapa de cardinalidade preserva uma identidade de caso UCS, uma identidade ADPM, um teste comportamental ADVS diretamente vinculado e uma identidade ADI. Seus dois vínculos inferiores de identidade não são motores de derivação.
- O mapeamento ADI–ADIB é registrado nos dois sentidos e pode ser muitos para muitos.
- A seta tracejada do banner aponta da ADIB para a UCS versionada como fonte adicional opcional durante a derivação; ela não é dependência de execução da aplicação nem motor canônico L1–L4.

## Produção da arte

O fundo decorativo do banner foi restaurado a partir do banner em inglês fornecido, por edição de imagem: foram retirados textos, diagramas, ícones, cartões e logotipos, preservando ondas azul-claras/brancas, gradientes e cantos arredondados. A arte resultante é [banner-background.png](banner-background.png). Nenhuma relação técnica ou legenda está codificada nesse fundo gerado. Todos os rótulos e a geometria dos diagramas estão explícitos nos SVGs e no script de renderização. A marca OAL original é reutilizada diretamente.

A instrução de produção foi: preservar somente o fundo abstrato original branco/azul-gelo/ciano, as ondas translúcidas inferiores, os arcos dos cantos superiores, a composição horizontal e a transparência fora dos cantos; remover todos os textos, logotipos, cartões, ícones, conectores e símbolos. Os seis diagramas finais foram conferidos quanto a rótulos, acentos, setas, agrupamento, legibilidade e equivalência EN/PT.
