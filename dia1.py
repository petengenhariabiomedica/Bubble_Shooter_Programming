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

# Cores fixas para a identidade visual do jogo (Interface e Cenário)
BRANCO = (245, 245, 245)        # Cor do fundo 
PRETO = (20, 20, 20)            # Cor dos textos
CINZA = (180, 180, 180)         # Usado para a linha da mira e instruções
AZUL_DETALHE = (70, 120, 220)   # Cor das bordas das caixas de texto
VERMELHO_CHAO = (180, 60, 60)   # Cor da linha de limite (indica perigo)


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

# =========================
# LOOP PRINCIPAL
# =========================
if __name__ == "__main__":
    nome = tela_nome_jogador()
    print("Nome digitado:", nome)
    pygame.quit()