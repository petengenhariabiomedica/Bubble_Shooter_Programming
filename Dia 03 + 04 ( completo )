import pygame
import math
import random

# Configurações gerais
LARGURA, ALTURA = 600, 700
RAIO = 20
COLUNAS = 14
LINHAS = 15

# Cores
LISTA_CORES = [
    (240, 196, 203),
    (251, 234, 214),
    (107, 117, 86)
]

BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)

VELOCIDADE_TIRO = 12


# =========================
# Bolinha
# =========================
class Bolinha:
    def __init__(self, x, y, cor, vx=0, vy=0):
        self.x = x
        self.y = y
        self.cor = cor
        self.vx = vx
        self.vy = vy

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), RAIO)


# =========================
# Funções auxiliares
# =========================
def posicao_bolinha(r, c):
    """
    Converte uma posição da matriz em posição da tela.
    """
    x = c * (RAIO * 2) + RAIO + (RAIO if r % 2 == 1 else 0)
    y = r * (RAIO * 1.75) + RAIO
    return x, y


def posicao_matriz(x, y):
    """
    Converte uma posição da tela em linha e coluna da matriz.
    """
    r = int(y // (RAIO * 1.75))
    c = int((x - (RAIO if r % 2 == 1 else 0)) // (RAIO * 2))

    # Garante que a posição não saia da matriz
    r = max(0, min(LINHAS - 1, r))
    c = max(0, min(COLUNAS - 1, c))

    return r, c


def criar_mapa():
    """
    Cria o mapa inicial com bolinhas nas primeiras 5 linhas.
    """
    mapa = []

    for r in range(LINHAS):
        linha = []

        for c in range(COLUNAS):
            if r < 5:
                x, y = posicao_bolinha(r, c)
                cor = random.choice(LISTA_CORES)
                linha.append(Bolinha(x, y, cor))
            else:
                linha.append(None)

        mapa.append(linha)

    return mapa


def buscar_grupo(mapa, r, c, cor_alvo, grupo):
    """
    Busca bolinhas conectadas da mesma cor.
    É a mesma ideia do Dia 2.
    """
    if r < 0 or r >= LINHAS or c < 0 or c >= COLUNAS:
        return

    bolinha = mapa[r][c]

    if not bolinha:
        return

    if bolinha.cor != cor_alvo:
        return

    if (r, c) in grupo:
        return

    grupo.add((r, c))

    vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    if r % 2 == 0:
        vizinhos += [(-1, -1), (1, -1)]
    else:
        vizinhos += [(-1, 1), (1, 1)]

    for dr, dc in vizinhos:
        buscar_grupo(mapa, r + dr, c + dc, cor_alvo, grupo)


def remover_grupo(mapa, grupo):
    for r, c in grupo:
        mapa[r][c] = None


# =========================
# Canhão e tiro
# =========================
def desenhar_canhao(tela, x_canhao, y_canhao, angulo, cor_atual):
    """
    Desenha a linha do canhão e a bolinha que será disparada.
    """
    x_fim = x_canhao + math.cos(angulo) * 50
    y_fim = y_canhao + math.sin(angulo) * 50

    pygame.draw.line(tela, CINZA, (x_canhao, y_canhao), (x_fim, y_fim), 4)
    pygame.draw.circle(tela, cor_atual, (x_canhao, y_canhao), RAIO)


def criar_tiro(x_canhao, y_canhao, angulo, cor):
    """
    Cria uma bolinha em movimento.
    """
    vx = math.cos(angulo) * VELOCIDADE_TIRO
    vy = math.sin(angulo) * VELOCIDADE_TIRO

    return Bolinha(x_canhao, y_canhao, cor, vx, vy)


def grudar_tiro(mapa, tiro):
    """
    Faz o tiro virar uma bolinha parada dentro do mapa.
    Depois verifica se formou grupo de 3 ou mais.
    """
    r, c = posicao_matriz(tiro.x, tiro.y)

    x, y = posicao_bolinha(r, c)

    mapa[r][c] = Bolinha(x, y, tiro.cor)

    grupo = set()
    buscar_grupo(mapa, r, c, tiro.cor, grupo)

    if len(grupo) >= 3:
        remover_grupo(mapa, grupo)


def atualizar_tiro(mapa, tiro):
    """
    Move o tiro e verifica colisões.
    Retorna None se o tiro grudou.
    Retorna o próprio tiro se ele continua se movendo.
    """
    if tiro is None:
        return None

    tiro.atualizar()

    # Rebater nas paredes
    if tiro.x < RAIO or tiro.x > LARGURA - RAIO:
        tiro.vx *= -1

    # Grudar no teto
    if tiro.y <= RAIO:
        grudar_tiro(mapa, tiro)
        return None

    # Verificar colisão com bolinhas do mapa
    for r in range(LINHAS):
        for c in range(COLUNAS):
            alvo = mapa[r][c]

            if alvo:
                distancia = math.hypot(tiro.x - alvo.x, tiro.y - alvo.y)

                if distancia < RAIO * 1.6:
                    grudar_tiro(mapa, tiro)
                    return None

    return tiro


# =========================
# Desenho do jogo
# =========================
def desenhar_mapa(tela, mapa):
    for linha in mapa:
        for bolinha in linha:
            if bolinha:
                bolinha.desenhar(tela)


def desenhar_jogo(tela, mapa, tiro, x_canhao, y_canhao, angulo, cor_atual):
    tela.fill(BRANCO)

    desenhar_mapa(tela, mapa)

    if tiro:
        tiro.desenhar(tela)

    desenhar_canhao(tela, x_canhao, y_canhao, angulo, cor_atual)


# =========================
# Loop principal
# =========================
if __name__ == "__main__":
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Bubble Shooter")

    relogio = pygame.time.Clock()

    mapa = criar_mapa()

    x_canhao = LARGURA // 2
    y_canhao = 650

    cor_atual = random.choice(LISTA_CORES)
    tiro = None

    while True:
        # Mira do canhão
        mx, my = pygame.mouse.get_pos()
        angulo = math.atan2(my - y_canhao, mx - x_canhao)

        # Eventos
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if tiro is None:
                    tiro = criar_tiro(x_canhao, y_canhao, angulo, cor_atual)
                    cor_atual = random.choice(LISTA_CORES)

        # Atualiza lógica
        tiro = atualizar_tiro(mapa, tiro)

        # Desenha tudo
        desenhar_jogo(tela, mapa, tiro, x_canhao, y_canhao, angulo, cor_atual)

        pygame.display.flip()
        relogio.tick(60)

