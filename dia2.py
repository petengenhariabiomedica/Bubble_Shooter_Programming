import pygame
import random

LARGURA, ALTURA, RAIO, COLUNAS, LINHAS = 600, 700, 20, 14, 15

# Lista simples de cores
LISTA_CORES = [
    (240, 196, 203),
    (251, 234, 214),
    (107, 117, 86)
]

def buscar_grupo(mapa, r, c, cor_alvo, grupo):
    """
    Busca recursivamente todas as bolinhas conectadas da mesma cor.
    
    - mapa: matriz do jogo
    - r, c: posição atual
    - cor_alvo: cor que estamos procurando
    - grupo: conjunto que armazena posições já visitadas
    """

    # Casos de parada (condições para NÃO continuar)
    if (
        r < 0 or r >= LINHAS or   # fora da matriz
        c < 0 or c >= COLUNAS or
        mapa[r][c] != cor_alvo or # cor diferente
        (r, c) in grupo           # já visitado
    ):
        return

    # Marca a posição atual como parte do grupo
    grupo.add((r, c))

    # Vizinhos básicos (cima, baixo, esquerda, direita)
    vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Ajuste para grade "hexagonal"
    if r % 2 == 0:
        vizinhos += [(-1, -1), (1, -1)]
    else:
        vizinhos += [(-1, 1), (1, 1)]

    # Explora todos os vizinhos
    for dr, dc in vizinhos:
        buscar_grupo(mapa, r + dr, c + dc, cor_alvo, grupo)

if __name__ == "__main__":
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))

    # Cria o mapa inicial
    mapa = [
        [random.choice(LISTA_CORES) if r < 5 else None for c in range(COLUNAS)]
        for r in range(LINHAS)
    ]
    
    while True:
        tela.fill((255, 255, 255))

        # Desenha o mapa (igual dia 1)
        for r in range(LINHAS):
            for c in range(COLUNAS):
                if mapa[r][c]:
                    px = c * (RAIO * 2) + RAIO + (RAIO if r % 2 == 1 else 0)
                    py = r * (RAIO * 1.75) + RAIO
                    pygame.draw.circle(tela, mapa[r][c], (int(px), int(py)), RAIO)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Clique do mouse
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # Posição do clique
                mx, my = pygame.mouse.get_pos()

                # Converte coordenadas da tela → matriz
                r_c = int(my // (RAIO * 1.75))
                c_c = int((mx - (RAIO if r_c % 2 == 1 else 0)) // (RAIO * 2))

                # Verifica se está dentro da matriz e se há bolinha
                if 0 <= r_c < LINHAS and 0 <= c_c < COLUNAS and mapa[r_c][c_c]:

                    grupo = set()

                    # Busca todas as bolinhas conectadas
                    buscar_grupo(mapa, r_c, c_c, mapa[r_c][c_c], grupo)

                    # Remove todas (coloca None)
                    for rg, cg in grupo:
                        mapa[rg][cg] = None

        pygame.display.flip()
