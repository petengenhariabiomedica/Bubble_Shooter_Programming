import pygame
import random

# Dimensões da janela
LARGURA, ALTURA = 600, 700

# Tamanho de cada bolinha
RAIO = 20

# Quantidade de colunas e linhas da "grade"
COLUNAS = 14
LINHAS = 15

# Dicionário de cores (nome -> valor RGB)
CORES = {
    "rosa": (240, 196, 203),
    "bege": (251, 234, 214),
    "verde": (107, 117, 86)
}

# Pegamos apenas os valores (tuplas RGB) para usar no jogo
LISTA_CORES = list(CORES.values())

def criar_mapa():
    """
    Cria uma matriz (lista de listas) representando o jogo.
    
    - Cada posição pode ter uma cor (bolinha) ou None (vazio)
    - Apenas as primeiras 5 linhas começam preenchidas
    """
    return [
        [random.choice(LISTA_CORES) if r < 5 else None for c in range(COLUNAS)]
        for r in range(LINHAS)
    ]

if __name__ == "__main__":
    pygame.init()  # Inicializa o pygame
    
    # Cria a janela do jogo
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    
    # Cria o "mapa" inicial do jogo
    mapa = criar_mapa()
    
    # Loop principal (o jogo roda infinitamente)
    while True:
        # Limpa a tela com branco
        tela.fill((255, 255, 255))

        # Percorre todas as posições da matriz
        for r in range(LINHAS):
            for c in range(COLUNAS):

                # Só desenha se houver uma bolinha ali
                if mapa[r][c]:

                    # Calcula posição X
                    # O (RAIO * 2) é o "diâmetro" da bolinha
                    # O offset cria o efeito "hexagonal" (linhas alternadas)
                    px = c * (RAIO * 2) + RAIO + (RAIO if r % 2 == 1 else 0)

                    # Calcula posição Y
                    py = r * (RAIO * 1.75) + RAIO

                    # Desenha a bolinha na tela
                    pygame.draw.circle(
                        tela,
                        mapa[r][c],        # cor
                        (int(px), int(py)), # posição
                        RAIO               # tamanho
                    )

        # Processa eventos (ex: fechar janela)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Atualiza a tela
        pygame.display.flip()
