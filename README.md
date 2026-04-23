# Minicurso: Introdução à Programação com Python (Abordagem Baseada em Projeto)

---

## Dia 1 — Fazendo algo aparecer na tela

### Objetivo

O primeiro encontro tem como objetivo levar o aluno do absoluto zero até a construção de uma tela onde múltiplas bolinhas são desenhadas de forma organizada. Mais do que o resultado visual, o foco está em fazer o aluno perceber que tudo o que aparece na tela é resultado direto de instruções simples executadas pelo computador.

### Introdução (5–10 min)

A aula deve começar com a demonstração do resultado final já pronto: uma tela com várias bolinhas organizadas em uma grade. Esse momento é importante para gerar curiosidade e dar um objetivo concreto ao aluno.

A partir disso, levanta-se a pergunta guia: "Como fazemos algo aparecer na tela usando código?". Essa pergunta orienta toda a construção da aula.

### Desenvolvimento (30–40 min)

O desenvolvimento começa com a inicialização do Pygame e a criação da janela. Aqui, é importante explicar que o computador não “sabe” que queremos desenhar; precisamos primeiro abrir um espaço onde isso será possível. A janela funciona como uma tela em branco.

Em seguida, introduz-se o loop principal (`while True`). Em vez de apresentar como um conceito formal, ele deve ser explicado como algo necessário para que o programa continue rodando e atualizando a tela constantemente. Uma boa analogia é a de um filme: a tela precisa ser redesenhada várias vezes por segundo.

Depois disso, mostra-se como limpar a tela a cada ciclo, reforçando que tudo será redesenhado repetidamente.

O próximo passo é desenhar uma única bolinha na tela. Esse momento é importante porque estabelece a primeira relação direta entre código e resultado visual.

Com isso funcionando, evolui-se para a criação de múltiplas bolinhas usando estruturas de repetição (`for`). Aqui, o professor pode explorar a ideia de organizar elementos em linhas e colunas, construindo uma grade.

Por fim, introduz-se a função que gera o mapa com cores aleatórias. Esse é o primeiro contato do aluno com a ideia de encapsular lógica em funções e também com a noção de dados estruturados (listas e listas de listas).

### Conceitos introduzidos

Durante essa aula, diversos conceitos fundamentais são apresentados de forma contextualizada: variáveis (para guardar posições e tamanhos), tipos básicos (como números e tuplas para cores), estruturas de repetição, funções, listas e listas de listas, além da noção de coordenadas (x, y).

### Atividades práticas

Os alunos podem experimentar modificando cores, tamanhos das bolinhas, quantidade de linhas e colunas. Essas pequenas mudanças ajudam a consolidar a relação entre código e comportamento visual.

### Fechamento (10 min)

No encerramento, reforça-se a ideia central da aula: tudo o que aparece na tela é resultado de coordenadas e repetição. O objetivo é que o aluno saia entendendo que não há “mágica”, apenas instruções sendo executadas.

---

## Dia 2 — Interação e lógica de grupos

### Objetivo

O segundo encontro tem como objetivo tornar o programa interativo, permitindo que o usuário clique nas bolinhas e que o sistema responda a essa ação removendo grupos conectados.

### Introdução

A aula começa com a demonstração do jogo respondendo ao clique do mouse. Isso cria um contraste com o dia anterior, onde o programa era apenas visual.

A pergunta guia é: "Como o programa entende o que o usuário fez?".

### Desenvolvimento

O primeiro passo é capturar eventos de mouse. Aqui, introduz-se a ideia de que o programa está constantemente “observando” o que acontece.

Em seguida, trabalha-se a conversão da posição do mouse (coordenadas da tela) para a posição dentro da grade (linha e coluna). Esse é um momento importante para reforçar a relação entre representação visual e estrutura de dados.

Depois, verifica-se se há uma bolinha na posição clicada. Isso introduz o uso de condicionais de forma natural.

A partir daí, implementa-se a função de busca de grupo. Em vez de apresentar formalmente como recursão, o ideal é explicar como um processo de explorar vizinhos: uma bolinha chama suas vizinhas, que chamam outras, e assim por diante.

Por fim, remove-se o grupo encontrado, alterando o mapa.

### Conceitos introduzidos

Nesta aula, surgem conceitos como eventos, condicionais, recursão (de forma intuitiva), conjuntos (`set`) para evitar repetição, e a ideia de algoritmo de busca.

### Atividades práticas

Os alunos podem implementar regras adicionais, como remover apenas grupos com três ou mais bolinhas, contar o tamanho do grupo ou exibir informações no terminal.

### Fechamento

A aula se encerra com a reflexão de que o programa agora toma decisões com base em regras, não apenas desenha elementos.

---

## Dia 3 — Transformando em jogo

### Objetivo

O terceiro encontro tem como objetivo transformar o sistema construído em um jogo, introduzindo mecânicas como canhão, tiro e colisão.

### Introdução

A aula começa com a demonstração do jogo com mecânica de tiro. Isso mostra uma evolução significativa do projeto.

A pergunta guia é: "Como damos comportamento independente para cada elemento?".

### Desenvolvimento

O ponto de partida é um problema: agora cada bolinha precisa armazenar mais informações (posição, cor, velocidade). Isso motiva a introdução de classes.

Cria-se então a classe `Bolinha`, explicando que ela representa um “tipo de objeto” com dados e comportamentos próprios.

Em seguida, cria-se o `Canhao`, responsável por mirar e disparar.

Depois, implementa-se o movimento do tiro, introduzindo a ideia de velocidade (vx, vy) e atualização contínua.

A lógica de atualização por frame é reforçada, mostrando que o jogo está sempre sendo recalculado.

Em seguida, introduz-se a detecção de colisões, tanto com paredes quanto com outras bolinhas.

Por fim, integra-se essa nova mecânica com a lógica de remoção de grupos já construída anteriormente.

### Conceitos introduzidos

Nesta etapa, surgem conceitos como classes e objetos, métodos, encapsulamento, movimento baseado em velocidade e colisão.

### Atividades práticas

Os alunos podem modificar a velocidade do tiro, limitar o ângulo do canhão ou exibir a próxima cor da bolinha.

### Fechamento

O fechamento reforça que o jogo é composto por objetos que possuem regras e comportamentos próprios, e que esses objetos interagem entre si.

---

## Dia 4 — Organização e finalização

### Objetivo

O último encontro tem como objetivo organizar melhor o código e transformar o protótipo em um jogo mais estruturado, com menu e estados.

### Introdução

A aula começa com a demonstração de uma versão com menu inicial, mostrando uma experiência mais completa.

A pergunta guia é: "Como organizamos melhor um programa maior?".

### Desenvolvimento

Primeiramente, cria-se uma classe principal que gerencia o funcionamento geral do programa.

Em seguida, introduz-se o conceito de estados (como MENU e JOGANDO), explicando que o programa pode se comportar de maneiras diferentes dependendo do contexto.

Depois, constrói-se a tela inicial e a lógica de transição entre estados.

Integra-se então o jogo já desenvolvido, agora dentro dessa nova estrutura.

Por fim, melhora-se o controle de entrada e a fluidez da interação.

### Conceitos introduzidos

Nesta etapa final, são trabalhados conceitos como estados, modularização, organização de código e importação entre arquivos.

### Atividades práticas

Os alunos podem implementar tela de game over, reinício do jogo e sistema de pontuação.

### Fechamento

A aula se encerra com uma reflexão sobre a evolução do projeto: de uma tela vazia até um jogo funcional. Reforça-se que os conceitos de programação foram aprendidos como ferramentas para resolver problemas reais.

---

