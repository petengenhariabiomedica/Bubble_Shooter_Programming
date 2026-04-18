import pygame  # Biblioteca multimídia do código
import math    # Funções matemáticas (Seno, Cosseno, Arcotangente)
import random  # Função para randomizar a aparição das bolinhas
from dia1 import *

RAIO = 20 # O tamanho (raio) de cada bolinha em pixels 
LARGURA_JOGO = 600
ALTURA_JOGO = 700
CHAO_Y = ALTURA_JOGO - 20          # Limite onde o jogo acaba se a bolinha encostar
COLUNAS = 14                       # Quantas bolinhas cabem na horizontal
LINHAS = int(CHAO_Y // (RAIO*1.75)) # Cálculo dinâmico das linhas baseado na altura do chão

# Um dicionário para organizar as cores das bolinhas.
# A "chave" é o nome (ex: "blush") e o "valor" é a TUPLA (R, G, B).
CORES = {
    "blush": (240, 196, 203),        # Rosa claro
    "antique_rose": (200, 125, 135), # Rosa escuro
    "champagne": (251, 234, 214),    # Bege
    "thyme": (107, 117, 86),         # Verde acinzentado
    "bique": (229, 188, 169)         # Tom de pêssego
}

# Transformamos os valores do dicionário em uma LISTA simples.
# O Python ignora os nomes (chaves) e guarda apenas os números (RGB).
# Isso é necessário para usar 'random.choice' e sortear uma cor para o tiro.
LISTA_CORES = list(CORES.values())

# =========================
# LÓGICA DO JOGO
# =========================
def criar_grade():
    # Cria a matriz inicial: 5 primeiras linhas coloridas, o resto vazio (None).
    return [[random.choice(LISTA_CORES) if r < 5 else None for c in range(COLUNAS)] for r in range(LINHAS)]


# =========================
# FUNÇÕES DE POSICIONAMENTO
# =========================
def obter_pos_pixel(r, c): 
    # Traduzindo de Grid (matriz) para Pixel (tela).
    # r de 'row' (linha) para não confundir 'l' com 'i'. c de 'column' (coluna).
    x = c * (RAIO * 2) + RAIO # +RAIO centraliza a bolinha para não começar no pixel 0.
    
    # Truque do encaixe (deslocamento hexagonal):
    # Se r % 2 for igual a 1, a linha é ímpar (1, 3, 5...).
    if r % 2 == 1:  
        # Empurramos a bolinha meio diâmetro para a direita para criar o zigue-zague.
        # Isso faz com que ela se encaixe no vão das bolinhas de cima.
        x += RAIO
    
    # Altura y: usamos 1.75 em vez de 2 pois as bolinhas entram nos vãos das outras.
    y = r * (RAIO * 1.75) + RAIO
    return x, y

def obter_grid_por_pixel(x, y): 
    # Traduzindo de Pixel para Grid.
    # Essencial para saber onde a bolinha disparada deve "grudar" na grade.

    # r (linha): divisão inteira da altura pelo espaço vertical.
    r = int(y // (RAIO * 1.75))
    
    # Ajustando lateralmente para o encaixe hexagonal:
    # Se a linha (r) for ímpar, subtraímos o RAIO para "desfazer" o empurrão do zigue-zague.
    x_ajustado = x - RAIO if r % 2 == 1 else x

    # c (coluna): divisão do x ajustado pelo diâmetro da bolinha.
    c = int(x_ajustado // (RAIO * 2))

    # Trava de segurança: impede que retorne índices fora da lista (ex: negativo ou maior que o mapa).
    return max(0, min(LINHAS-1, r)), max(0, min(COLUNAS-1, c))

# =========================
# TELAS E INTERFACE
# =========================
def desenhar_grade(tela, grade): 
    # Varre a matriz e desenha os círculos coloridos na tela.
    for r in range(LINHAS):
        for c in range(COLUNAS): 
            if grade[r][c] is not None: # Se a gaveta não estiver vazia (None).
                px, py = obter_pos_pixel(r, c) # Traduz grid para pixel.
                pygame.draw.circle(tela, grade[r][c], (int(px), int(py)), RAIO)


def tela_principal(nome):
    grade = criar_grade() # Gera o mapa inicial

    rodando = True
    while rodando:
        tela.fill(BRANCO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        desenhar_grade(tela, grade)

        texto = fonte.render(f"Jogador: {nome}", True, PRETO)
        tela.blit(texto, (20, 720))

        pygame.display.flip()
        relogio.tick(60)


# =========================
# LÓGICA DO JOGO
# =========================

def buscar_grupo(grade, r, c, cor_alvo, grupo): 
    # Função recursiva responsável por encontrar bolinhas adjacentes da mesma cor.
    # FILTRO: para se estiver fora do mapa, se a cor for diferente ou se já estiver no grupo.
    if r < 0 or r >= LINHAS or c < 0 or c >= COLUNAS or grade[r][c] != cor_alvo or (r, c) in grupo:
        return
    
    # Se passou no filtro, a bolinha é válida e seu endereço é guardado.
    grupo.add((r, c)) 
    
    # Definindo os 6 vizinhos (encaixe de colmeia).
    vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Cima, Baixo, Esquerda, Direita
    if r % 2 == 0:
        vizinhos += [(-1, -1), (1, -1)] # Vizinhos extras para linhas pares
    else:
        vizinhos += [(-1, 1), (1, 1)]   # Vizinhos extras para linhas ímpares

    # Reação em cadeia (Flood Fill): chama a si mesma para cada vizinho.
    # "Ei, eu sou rosa? Você também é? Se for, avise os seus vizinhos também!"
    for dr, dc in vizinhos:
        buscar_grupo(grade, r + dr, c + dc, cor_alvo, grupo)


def verificar_soltas(grade): 
    # Confere a conectividade com o teto para derrubar bolinhas "órfãs".
    conectadas = set() # Guarda o endereço das bolinhas que têm caminho até o topo.

    def buscar_conectadas(r, c): 
        # Filtro: para se sair do mapa, se for vazio (None) ou se já estiver marcada.
        if r < 0 or r >= LINHAS or c < 0 or c >= COLUNAS or grade[r][c] is None or (r, c) in conectadas:
            return
        # Se passou no filtro, recebe o visto de entrada válida.
        conectadas.add((r, c)) 
        
        # Vizinhos hexagonais:
        vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        vizinhos += [(-1, -1), (1, -1)] if r % 2 == 0 else [(-1, 1), (1, 1)]
        
        for dr, dc in vizinhos:
            buscar_conectadas(r + dr, c + dc)

    # Inicia a busca apenas a partir da linha 0 (o teto).
    for c in range(COLUNAS):
        buscar_conectadas(0, c) 

    # Pente fino: quem não está na lista 'conectadas' vai de vasco :)
    removidas = 0
    for r in range(LINHAS):
        for c in range(COLUNAS):
            if grade[r][c] is not None and (r, c) not in conectadas:
                grade[r][c] = None
                removidas += 1
    return removidas 


# =========================
# LOOP PRINCIPAL
# =========================
if __name__ == "__main__":
    nome = tela_nome_jogador()

    if nome:  # se não fechou a janela
        tela_principal(nome)

    pygame.quit()