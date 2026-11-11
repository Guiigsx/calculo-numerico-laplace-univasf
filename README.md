# Equação de Laplace — Cálculo Numérico · UNIVASF

Aplicação acadêmica para calcular e visualizar a distribuição estacionária de temperatura em uma placa retangular. A solução utiliza diferenças finitas e o método de sobrerrelaxação sucessiva (SOR), implementados em JavaScript sem bibliotecas externas.

## Como abrir

1. Baixe o projeto pelo botão **Code → Download ZIP** do GitHub e extraia os arquivos.
2. Abra `index.html` em um navegador.
3. Clique em **Executar cálculo**.

A página funciona localmente, sem instalação de pacotes, servidor ou conexão com a internet.

## Recursos

- Indicadores da malha, convergência, erros e tempo de execução.
- Superfície tridimensional e mapa de temperatura.
- Animação das varreduras SOR.
- Planta interativa com os 6.399 pontos da malha: seleção por clique ou pelas setas do teclado.
- Caixa junto ao ponto selecionado com coordenadas, temperatura numérica, temperatura analítica e erro absoluto.
- Lista dos 6.083 pontos internos e exportação em CSV.
- Código do método disponível na própria página.

## Problema e método

Resolve-se a equação de Laplace no domínio $1<x<40$, $0<y<40$:

$$
\frac{\partial^2 T}{\partial x^2}+\frac{\partial^2 T}{\partial y^2}=0.
$$

As condições de contorno utilizadas são:

$$
T(1,y)=\ln(1+y^2),\qquad T(40,y)=\ln(1600+y^2),
$$

$$
T(x,0)=2\ln x,\qquad T(x,40)=\ln(x^2+1600).
$$

Com $h=k=0{,}5$, o esquema de cinco pontos resulta em:

$$
4T_{i,j}-T_{i-1,j}-T_{i+1,j}-T_{i,j-1}-T_{i,j+1}=0.
$$

O sistema tem 6.083 incógnitas internas. Os 316 pontos de borda recebem os valores prescritos. As estimativas internas começam em zero e são atualizadas por SOR com ordenação em duas cores, fator $\omega=1{,}92$ e tolerância de $10^{-12}$ para a maior alteração por varredura. O limite de execução é de 20.000 varreduras.

A referência analítica é $T(x,y)=\ln(x^2+y^2)$. Os erros são calculados sobre os pontos internos. A animação acompanha as iterações numéricas; a equação modela o estado estacionário.

## Resultados de referência

| Medida | Valor |
| --- | ---: |
| Pontos da malha | 79 × 81 = 6.399 |
| Pontos internos calculados | 6.083 |
| Varreduras SOR | 479 |
| Erro absoluto máximo | 0,004402389 |
| Ponto de erro máximo | (1,5; 1,5) |
| Erro absoluto médio | 0,000135291 |
| RMSE | 0,000318676 |

O tempo de execução é medido a cada cálculo e depende do computador e do navegador.

## Código e atualização da página

O algoritmo também pode ser executado no terminal, com Node.js instalado:

```sh
node solve_laplace.js
```

Para atualizar a página após editar o algoritmo ou o modelo HTML, use Python 3:

```sh
python build.py
```

No Windows, também é possível usar `py build.py`. O gerador utiliza apenas a biblioteca padrão do Python e incorpora o algoritmo, os estilos e a imagem institucional em `index.html`.

```text
index.html          Página pronta para abrir
solve_laplace.js     Algoritmo numérico
build.py            Modelo da página e gerador
univasf.png         Marca institucional
```

## Discentes

- Cecília Moura Reis Frota
- Guilherme Hilário Schmitz da Silva
- Guilherme Torres de Miranda
- Luiz Felipe Monte de Oliveira

Disciplina: **MATM0048 — Cálculo Numérico**. Professor: **Sergio Floquet**. Universidade Federal do Vale do São Francisco — **UNIVASF**.

A identidade visual utiliza a marca institucional e o [manual de identidade visual da UNIVASF](https://portais.univasf.edu.br/comunicacao/ManualdeIdentidadeVisualUniversidadeFederaldoValedoSoFranciscoUnivasf.pdf).
