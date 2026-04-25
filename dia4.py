from dia3 import BubbleShooterGame
import pygame

class BubbleShooterPro:
    def __init__(self):
        pygame.init()

        # Cria janela
        self.tela = pygame.display.set_mode((600, 700))

        # Fonte para textos
        self.fonte = pygame.font.SysFont("Arial", 24)

        # Jogo principal
        self.jogo = BubbleShooterGame()

        # Estado inicial
        self.estado = "MENU"

    def rodar(self):
        while True:
            self.tela.fill((0, 0, 0))

            # Eventos
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Pressionar ENTER inicia o jogo
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                    self.estado = "JOGANDO"

            # Se estiver no menu
            if self.estado == "MENU":

                # Desenha mensagem
                msg = self.fonte.render(
                    "APERTE ENTER PARA INICIAR",
                    True,
                    (255, 255, 255)
                )

                self.tela.blit(msg, (150, 300))

            else:
                # Atualiza jogo normal
                self.jogo.canhao.mirar(pygame.mouse.get_pos())
                self.jogo.atualizar()
                self.jogo.desenhar(self.tela)

                # Clique contínuo dispara
                if pygame.mouse.get_pressed()[0]:
                    self.jogo.atirar()

            pygame.display.flip()

            # Limita FPS
            pygame.time.Clock().tick(60)


if __name__ == "__main__":
    BubbleShooterPro().rodar()