import pygame

# Définir des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
L_GREEN = (150, 255, 150)
RED = (255, 0, 0)
L_RED = (255, 204, 203)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 0)
L_YELLOW = (255, 255, 150)

#
pygame.init()
X = 450
Y = 200
size = (X, Y)
window = pygame.display.set_mode(size)
font = pygame.font.Font('freesansbold.ttf', 25)



def drawButton(left, top, color, textInButton):
    rectSize = pygame.Rect(left, top, 60, 30)
    pygame.draw.rect(window, color, rectSize)  # gauche, haut, largeur, hauteur
    pygame.draw.rect(window, BLACK, rectSize, 3)
    fontButton = pygame.font.Font('freesansbold.ttf', 20)
    textButton = fontButton.render(textInButton, True, BLACK, )
    textRectButton = textButton.get_rect()
    textRectButton.center = (left + 30, top + 15)
    window.blit(textButton, textRectButton)

# séléction du niveau de difficulté
def chooseLevel():
    # initialisation niveau 0
    level = 0
    text = font.render('Choisir le niveau de difficulté', True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2 - 40)

    pygame.display.set_caption("Sudoku ECE")

    done = True
    while done:
        window.fill(WHITE)
        window.blit(text, textRect)
        # création des boutons
        drawButton(70, 100, L_GREEN, "1")
        drawButton(190, 100, L_YELLOW, "2")
        drawButton(310, 100, L_RED, "3")
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # désactive la bibliothèque pygame
                pygame.quit()
                # quitter le programme.
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (70 <= pos[0] <= 130) and (100 <= pos[1] <= 130):
                    level = 1
                if (190 <= pos[0] <= 250) and (100 <= pos[1] <= 130):
                    level = 2
                if (310 <= pos[0] <= 370) and (100 <= pos[1] <= 130):
                    level = 3
                if level != 0:
                    pygame.quit()
                    return level

            # Dessine l'objet de surface à l'écran.
            pygame.display.update()
