import pygame,sys
from constantes import *
from play import *
#Botões
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)



# Menu:
def menu():
    pygame.init()

    SCREEN = pygame.display.set_mode((TELA_MENU_LARGURA, TELA_MENU_ALTURA))
    pygame.display.set_caption(NOME_JOGO)

    pygame.mixer.music.load(MUSICA_MENU)
    pygame.mixer.music.play(-1)

    def get_font(size):
        return pygame.font.Font(FONTE_PADRAO, size)

    def play():
        iniciar_jogo(SCREEN)



    def main_menu():

        while True:

            SCREEN.blit(BACKGROUND, (CENTRALIZACAO_X, CENTRALIZACAO_Y))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(FONTE_MAIN_MENU).render(MENU, True, LARANJA)
            MENU_RECT = MENU_TEXT.get_rect(center=(OPTIONS_X, OPTION_Y_1))

            PLAY_BUTTON = Button(image=pygame.image.load(RETANGULO_PLAY), pos=(OPTIONS_X, OPTION_Y_2),
                                       text_input=JOGAR, font=get_font(FONTE_BOTOES), base_color=VERDE_CLARO,
                                       hovering_color=BRANCO)

            QUIT_BUTTON = Button(image=pygame.image.load(RETANGULO_QUIT), pos=(OPTIONS_X, OPTION_Y_3),
                                       text_input=SAIR, font=get_font(FONTE_BOTOES), base_color=VERDE_CLARO,
                                       hovering_color=BRANCO)

            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        play()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    main_menu()