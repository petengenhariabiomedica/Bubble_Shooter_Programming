import pygame  # Biblioteca multimídia do código
import math    # Funções matemáticas (Seno, Cosseno, Arcotangente)
import random  # Função para randomizar a aparição das bolinhas

# Chamando o módulo da pygame --- controle de multimídia
pygame.init() 

################## MÓDULOS DA PYGAME ##################

# pygame.display: Cria a janela do jogo e controla os pixels que aparecem nela
# pygame.surface: Gerencia as imagens e áreas de desenho, como se fossem "folhas de papel" digitais
# pygame.mixer: Carrega e toca arquivos de som e música
# pygame.event: Captura tudo o que o usuário faz (clicar no mouse, apertar uma tecla, fechar a janela)
# pygame.mouse: Lê a posição exata (x,y) do cursor e quais botões estão pressionados
# pygame.key: Identifica exatamente qual tecla do teclado foi apertada
# pygame.joystick: Reconhece e lê dados de controles de videogame conectados
# pygame.draw: Contém as fórmulas matemáticas para desenhar formas (círculos, retângulos, linhas)
# pygame.font: Traduz arquivos de texto em imagens para que você consiga ler pontuação e menus
# pygame.time: Controla a velocidade do jogo (FPS) para que ele não rode rápido demais
# pygame.image: Permite abrir arquivos de imagem externos 

# Imprimir as tuplas conferindo se nenhum módulo deu problema.
# Tem que aparecer algo tipo (5,0) - 5 sucessos e 0 falhas.
print(pygame.init()) 

####### CRIANDO A TELA INICIAL 

# 1. Definição de constantes de tamanho da janela (aba inicial)
LARGURA, ALTURA = 600, 760 

# Na linha abaixo criei duas variáveis para guardar o tamanho da janela.
# 600 é a largura (horizontal) e 760 é a altura (vertical), medidos em pixels.
# Utilizei os nomes em MAIÚSCULO por convenção de que esses valores não devem ser mudados.

# 2. Criação da superfície principal (a janela)
# O 'set_mode' pede para o sistema operacional abrir uma janela.
# O uso de parênteses duplos ((LARGURA, ALTURA)) ocorre porque a função espera uma 'tupla'.
# A variável 'tela' guarda a referência dessa janela para desenhar nela depois.
tela = pygame.display.set_mode((LARGURA, ALTURA))

# 3. Identificação do programa
# O 'set_caption' define o texto que aparece na barra de título da janela.
pygame.display.set_caption("Bubble Shooter Pro")

# 4. Controle de fluxo temporal
# 'Clock()' cria um objeto gerenciador de tempo para o jogo não rodar na velocidade máxima do processador.
relogio = pygame.time.Clock() # Alvo: 60 FPS

# 5. '.font.SysFont' busca uma fonte instalada no sistema para colocar textos na tela.
fonte = pygame.font.SysFont("arial", 24) 
fonte_grande = pygame.font.SysFont("arial", 36)

####### CRIANDO A INTERFACE DO GAME - GEOMETRIA E GRADE

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

# Cores fixas para a identidade visual do jogo (Interface e Cenário)
BRANCO = (245, 245, 245)        # Cor do fundo 
PRETO = (20, 20, 20)            # Cor dos textos
CINZA = (180, 180, 180)         # Usado para a linha da mira e instruções
AZUL_DETALHE = (70, 120, 220)   # Cor das bordas das caixas de texto
VERMELHO_CHAO = (180, 60, 60)   # Cor da linha de limite (indica perigo)


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
# LÓGICA DO JOGO
# =========================

def criar_grade():
    # Cria a matriz inicial: 5 primeiras linhas coloridas, o resto vazio (None).
    return [[random.choice(LISTA_CORES) if r < 5 else None for c in range(COLUNAS)] for r in range(LINHAS)]

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
# TELAS E INTERFACE
# =========================

def desenhar_grade(tela, grade): 
    # Varre a matriz e desenha os círculos coloridos na tela.
    for r in range(LINHAS):
        for c in range(COLUNAS): 
            if grade[r][c]: # Se a gaveta não estiver vazia (None).
                px, py = obter_pos_pixel(r, c) # Traduz grid para pixel.
                pygame.draw.circle(tela, grade[r][c], (int(px), int(py)), RAIO)

def tela_nome_jogador(): 
    # Loop da tela de boas-vindas para capturar o nome.
    nome = ""
    while True: 
        tela.fill(BRANCO) 
        titulo = fonte_grande.render("Bubble Shooter Pro", True, PRETO) 
        caixa = pygame.Rect(120, 300, 360, 50)
        pygame.draw.rect(tela, AZUL_DETALHE, caixa, 3)
        texto_nome = fonte.render(nome + "|", True, PRETO) # Cursor piscante improvisado
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 180))
        tela.blit(texto_nome, (caixa.x + 10, caixa.y + 12))
        pygame.display.flip()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: return None
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN: return nome if nome else "Jogador"
                elif ev.key == pygame.K_BACKSPACE: nome = nome[:-1]
                else: 
                    # Limite de 12 caracteres para não explodir a caixa.
                    if len(nome) < 12 and ev.unicode.isprintable(): nome += ev.unicode

def tela_final(tela, jogador):
    # Mostra pontuação final e pergunta se quer jogar de novo.
    while True:
        tela.fill(BRANCO)
        msg = fonte_grande.render(f"Fim de Jogo, {jogador['nome']}!", True, PRETO)
        pts = fonte.render(f"Pontos: {jogador['pontos']}", True, PRETO)
        inst = fonte.render("ENTER para Reiniciar - ESC para Sair", True, CINZA)
        tela.blit(msg, (LARGURA//2 - msg.get_width()//2, 300))
        tela.blit(pts, (LARGURA//2 - pts.get_width()//2, 360))
        tela.blit(inst, (LARGURA//2 - inst.get_width()//2, 450))
        pygame.display.flip()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: return False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN: return True # Reinicia.
                if ev.key == pygame.K_ESCAPE: return False # Fecha.

# =========================
# PARTIDA PRINCIPAL
# =========================

def jogar_partida(nome_jogador):
    grade = criar_grade() # Gera o mapa inicial.
    jogador = {"nome": nome_jogador, "pontos": 0} 
    pos_canhao = [LARGURA // 2, ALTURA_JOGO - 50] 
    cor_atual = random.choice(LISTA_CORES) 
    cor_proxima = random.choice(LISTA_CORES) 
    tiro = None # Começa vazio porque né, a gente não atirou nada ainda.
    
    rodando = True 
    while rodando:
        tela.fill(BRANCO)
        mouse_x, mouse_y = pygame.mouse.get_pos() # Onde o mouse está?
        
        # Trigonometria para a mira:
        dx = mouse_x - pos_canhao[0]
        dy = mouse_y - pos_canhao[1]
        angulo = math.atan2(dy, dx) # Arco Tangente para achar o ângulo.
        # Trava o canhão para não atirar para trás ou no próprio pé.
        angulo = max(min(angulo, -0.2), -math.pi + 0.2) 

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return None
            if evento.type == pygame.MOUSEBUTTONDOWN and tiro is None:
                # Trava de segurança para um tiro por vez.
                vel = 15 
                # Cria o tiro: [Pos X, Pos Y, Velocidade X, Velocidade Y, Cor].
                tiro = [pos_canhao[0], pos_canhao[1], math.cos(angulo)*vel, math.sin(angulo)*vel, cor_atual] 
                cor_atual = cor_proxima
                cor_proxima = random.choice(LISTA_CORES)

        # Desenha elementos fixos:
        pygame.draw.line(tela, VERMELHO_CHAO, (0, CHAO_Y), (LARGURA, CHAO_Y), 3)
        desenhar_grade(tela, grade)
        
        # Desenha a linha da mira:
        mira_x = pos_canhao[0] + math.cos(angulo) * 60
        mira_y = pos_canhao[1] + math.sin(angulo) * 60
        pygame.draw.line(tela, CINZA, pos_canhao, (mira_x, mira_y), 2)
        
        # Desenha o canhão e a próxima bolinha:
        pygame.draw.circle(tela, cor_atual, pos_canhao, RAIO)
        pygame.draw.circle(tela, cor_proxima, (pos_canhao[0] + 60, pos_canhao[1] + 10), RAIO // 2)

        ################# MOVIMENTO DO VOO 
        if tiro: 
            tiro[0] += tiro[2] # Incrementa X.
            tiro[1] += tiro[3] # Incrementa Y.
            pygame.draw.circle(tela, tiro[4], (int(tiro[0]), int(tiro[1])), RAIO)
            
        ################## BATE E VOLTA
            # Se bater nas paredes laterais, inverte a velocidade X.
            if tiro[0] <= RAIO or tiro[0] >= LARGURA - RAIO:
                tiro[2] *= -1 
            
            colidiu = False 
            if tiro[1] <= RAIO: # Colidiu no teto?
                colidiu = True
            else: # Colidiu com outra bolinha?
                for r in range(LINHAS):
                    for c in range(COLUNAS):
                        if grade[r][c]:
                            px, py = obter_pos_pixel(r, c)
                            # math.hypot calcula a distância real. Margem de erro 1.6 para parecer natural.
                            if math.hypot(tiro[0] - px, tiro[1] - py) < RAIO * 1.6: 
                                colidiu = True
                                break
            
            #################### FUNÇÃO DE GRUDAR
            if colidiu:
                # Acha a gaveta vazia mais próxima na grade.
                r_fix, c_fix = obter_grid_por_pixel(tiro[0], tiro[1]) 
                if r_fix < LINHAS and grade[r_fix][c_fix] is None:
                    grade[r_fix][c_fix] = tiro[4]
                    grupo = set()
                    buscar_grupo(grade, r_fix, c_fix, tiro[4], grupo)
                    
                    if len(grupo) >= 3: # Estoura se tiver 3 ou mais.
                        for rg, cg in grupo: grade[rg][cg] = None
                        jogador["pontos"] += len(grupo) * 10
                        # Bônus por derrubar bolinhas soltas no ar.
                        jogador["pontos"] += verificar_soltas(grade) * 5 
                tiro = None # Libera o canhão para o próximo tiro.

        # Verificação de fim de jogo (bolinha tocou o chão)
        for r in range(LINHAS):
            for c in range(COLUNAS):
                if grade[r][c]:
                    px, py = obter_pos_pixel(r, c)
                    if py + RAIO >= CHAO_Y: 
                        rodando = False # F de derrota.

        # Mostra HUD de pontos:
        info = fonte.render(f"{jogador['nome']} | Pontos: {jogador['pontos']}", True, PRETO)
        tela.blit(info, (20, ALTURA - 40))
        pygame.display.flip()
        relogio.tick(60) # Crava em 60 frames por segundo.
        
    return jogador 

# =========================
# LOOP PRINCIPAL
# =========================

ativo = True
while ativo:
    nome = tela_nome_jogador()
    if not nome: break
    
    res = jogar_partida(nome) 
    if res is None: break 
    
    # Se a partida acabar, vai para a tela de Game Over.
    if not tela_final(tela, res): 
        ativo = False

pygame.quit() # Encerra a biblioteca e fecha a janela.