import pygame
import math
import random

# Configurações gerais do jogo
LARGURA, ALTURA, RAIO, COLUNAS, LINHAS = 600, 700, 20, 14, 15

# Cores disponíveis para as bolinhas
LISTA_CORES = [
    (240, 196, 203),
    (251, 234, 214),
    (107, 117, 86)
]

# =========================
# Classe que representa uma bolinha
# =========================
class Bolinha:
    def __init__(self, x, y, cor, vx=0, vy=0):
        # Posição da bolinha na tela
        self.x = x
        self.y = y

        # Cor da bolinha
        self.cor = cor

        # Velocidade (usada quando a bolinha está em movimento)
        self.vx = vx
        self.vy = vy

    def atualizar(self):
        # Atualiza posição com base na velocidade
        # Isso faz a bolinha "andar"
        self.x += self.vx
        self.y += self.vy

    def desenhar(self, tela):
        # Desenha a bolinha na tela
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), RAIO)


# =========================
# Classe do canhão (de onde saem os tiros)
# =========================
class Canhao:
    def __init__(self, x, y, cor_inicial):
        # Posição fixa do canhão
        self.x = x
        self.y = y

        # Ângulo de direção (para onde ele está apontando)
        self.angulo = 0

        # Cor da próxima bolinha a ser disparada
        self.cor_atual = cor_inicial

    def mirar(self, pos):
        # Calcula o ângulo entre o canhão e o mouse
        # atan2 retorna o ângulo correto considerando direção
        self.angulo = math.atan2(pos[1] - self.y, pos[0] - self.x)

    def desenhar(self, tela):
        # Calcula a ponta do canhão (linha de direção)
        fim = (
            self.x + math.cos(self.angulo) * 50,
            self.y + math.sin(self.angulo) * 50
        )

        # Desenha a linha do canhão
        pygame.draw.line(tela, (100, 100, 100), (self.x, self.y), fim, 4)

        # Desenha a bolinha atual no canhão
        pygame.draw.circle(tela, self.cor_atual, (self.x, self.y), 20)


# =========================
# Classe principal do jogo
# =========================
class BubbleShooterGame:
    def __init__(self):
        # Escolhe cor inicial do canhão
        cor_ini = random.choice(LISTA_CORES)

        # Cria o canhão
        self.canhao = Canhao(300, 650, cor_ini)

        # Tiro atual (None significa que não há tiro)
        self.tiro = None

        # Cria o mapa do jogo (matriz de bolinhas)
        self.mapa = [
            [
                # Se estiver nas primeiras linhas, cria bolinha
                Bolinha(
                    c * (RAIO * 2) + RAIO + (RAIO if r % 2 == 1 else 0),
                    r * (RAIO * 1.75) + RAIO,
                    random.choice(LISTA_CORES)
                ) if r < 5 else None
                for c in range(COLUNAS)
            ]
            for r in range(LINHAS)
        ]

    # =========================
    # Busca grupo de bolinhas conectadas (recursão)
    # =========================
    def buscar_grupo(self, r, c, cor_alvo, grupo):
        # Verificações de segurança
        if r < 0 or r >= LINHAS or c < 0 or c >= COLUNAS:
            return

        bolinha = self.mapa[r][c]

        # Para se não tiver bolinha, cor diferente ou já visitado
        if not bolinha or bolinha.cor != cor_alvo or (r, c) in grupo:
            return
        
        # Marca como visitado
        grupo.add((r, c))

        # Vizinhos principais
        vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Ajuste para grid hexagonal
        if r % 2 == 0:
            vizinhos += [(-1, -1), (1, -1)]
        else:
            vizinhos += [(-1, 1), (1, 1)]

        # Explora todos os vizinhos
        for dr, dc in vizinhos:
            self.buscar_grupo(r + dr, c + dc, cor_alvo, grupo)

    # =========================
    # Disparo da bolinha
    # =========================
    def atirar(self):
        # Só atira se não houver tiro em andamento
        if not self.tiro:
            # Calcula velocidade com base no ângulo
            vx = math.cos(self.canhao.angulo) * 12
            vy = math.sin(self.canhao.angulo) * 12

            # Cria a bolinha em movimento
            self.tiro = Bolinha(
                self.canhao.x,
                self.canhao.y,
                self.canhao.cor_atual,
                vx,
                vy
            )

            # Sorteia próxima cor do canhão
            self.canhao.cor_atual = random.choice(LISTA_CORES)

    # =========================
    # Faz a bolinha "grudar" no mapa
    # =========================
    def grudar(self):
        # Converte posição do tiro em posição da matriz
        r = max(0, min(LINHAS - 1, int(self.tiro.y // (RAIO * 1.75))))
        c = max(0, min(COLUNAS - 1, int((self.tiro.x - (RAIO if r % 2 == 1 else 0)) // (RAIO * 2))))
        
        # Calcula posição exata para alinhar na grade
        px = c * (RAIO * 2) + RAIO + (RAIO if r % 2 == 1 else 0)
        py = r * (RAIO * 1.75) + RAIO

        # Coloca nova bolinha no mapa
        self.mapa[r][c] = Bolinha(px, py, self.tiro.cor)
        
        # Busca grupo conectado
        grupo = set()
        self.buscar_grupo(r, c, self.mapa[r][c].cor, grupo)

        # Remove grupo se tiver 3 ou mais
        if len(grupo) >= 3:
            for rg, cg in grupo:
                self.mapa[rg][cg] = None  # BOOM!
        
        # Remove o tiro
        self.tiro = None

    # =========================
    # Atualiza o jogo (movimento, colisão)
    # =========================
    def atualizar(self):
        if self.tiro:
            # Move o tiro
            self.tiro.atualizar()

            # Rebater nas paredes laterais
            if self.tiro.x < RAIO or self.tiro.x > LARGURA - RAIO:
                self.tiro.vx *= -1
            
            # Se encostar no topo
            if self.tiro.y <= RAIO:
                self.grudar()
                return

            # Verifica colisão com outras bolinhas
            for r in range(LINHAS):
                for c in range(COLUNAS):
                    alvo = self.mapa[r][c]

                    # Se houver bolinha e estiver próximo o suficiente
                    if alvo and math.hypot(
                        self.tiro.x - alvo.x,
                        self.tiro.y - alvo.y
                    ) < RAIO * 1.6:

                        self.grudar()
                        return

    # =========================
    # Desenha tudo na tela
    # =========================
    def desenhar(self, tela):
        # Limpa a tela
        tela.fill((255, 255, 255))

        # Desenha o canhão
        self.canhao.desenhar(tela)

        # Desenha o tiro (se existir)
        if self.tiro:
            self.tiro.desenhar(tela)

        # Desenha todas as bolinhas do mapa
        for linha in self.mapa:
            for b in linha:
                if b:
                    b.desenhar(tela)


# =========================
# Loop principal do jogo
# =========================
if __name__ == "__main__":
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))

    jogo = BubbleShooterGame()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Clique do mouse dispara
            if ev.type == pygame.MOUSEBUTTONDOWN:
                jogo.atirar()

        # Atualiza direção do canhão
        jogo.canhao.mirar(pygame.mouse.get_pos())

        # Atualiza lógica do jogo
        jogo.atualizar()

        # Desenha tudo
        jogo.desenhar(tela)

        pygame.display.flip()

        # Limita FPS (fluidez do jogo)
        pygame.time.Clock().tick(60)
