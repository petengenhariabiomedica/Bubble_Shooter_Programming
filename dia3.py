import pygame  # Biblioteca multimídia do código
import math    # Funções matemáticas (Seno, Cosseno, Arcotangente)
import random  # Função para randomizar a aparição das bolinhas

from dia1 import *
from dia2 import *

CHAO_Y = ALTURA - 150          # Limite onde o jogo acaba se a bolinha encostar

# =========================
# JOGO - PARTIDA PRINCIPAL:
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
# TELAS E INTERFACE
# =========================

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
            if ev.type == pygame.QUIT:
                return False

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    return True   # Reinicia
                if ev.key == pygame.K_ESCAPE:
                    return False  # Fecha o jogo

# =========================
# LOOP PRINCIPAL
# =========================

if __name__ == "__main__":
    ativo = True

    while ativo:
        nome = tela_nome_jogador()
        if not nome:
            break

        resultado = jogar_partida(nome)

        if resultado is None:
            break

        # Se a partida acabar, vai para a tela de Game Over:
        if not tela_final(tela, resultado):
            ativo = False

    pygame.quit() # Encerra a biblioteca e fecha a janela.