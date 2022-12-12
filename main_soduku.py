
import pygame
from pygame import mixer
from sudokuSolverAlgo import *
from chooseLevel import *
import time
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.init(22050,-16,2,1024)

# Définir des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
L_GREEN = (150, 255, 150)
RED = (255, 0, 0)
L_RED = (255, 204, 203)
BLEU = (152, 180, 229)
PURPLE = (228, 152, 229)
YELLOW = (255, 255, 0)
L_GRAY=(217, 221, 220)

# Définir la LARGEUR et la HAUTEUR de chaque emplacement de la grille
WIDTH = HEIGHT = 50

# Définir la marge entre chaque cellule
MARGIN = 5
numbers_1to9 = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                pygame.K_9]

# Définir la largeur et la hauteur de l'écran [largeur, hauteur]
size = (500, 520)
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)

# Boucle jusqu'à ce que l'utilisateur clique sur le bouton de fermeture.
done = False


def cheatingAllTheWay():
    for row in range(len(Board)):
        for column in range(len(Board[row])):
            Board[row][column] = solvedBoard[row][column]
            addNumToBoard(Board[row][column], row, column, L_GREEN)
            time.sleep(0.05)
            pygame.display.flip()
    finish()


def addNumToBoard(number, row, column, color):
    addNewRect(row, column, WHITE, 5)
    addNewRect(row, column, color, None)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(number), True, BLACK, )
    textRect = text.get_rect() # get_rect() -> Renvoie un nouveau rectangle couvrant toute la surface.
    textRect.center = ((MARGIN + WIDTH) * column + MARGIN + WIDTH / 2, (MARGIN + HEIGHT) * row + MARGIN + WIDTH / 2)
    screen.blit(text, textRect)
    drawTheBorder()

# fin de la partie
# affichage
def finish():
    if solvedBoard == Board:
        print("Bravo ! Vous avez gagné")
    else:
        print("Fin de la partie :( \n"
              "Vous avez perdu")


def addNewRect(row, col, color, width):
    rectSize = pygame.Rect((MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                           HEIGHT)
    if width is not None:
        pygame.draw.rect(screen, color, rectSize, width)  # colorier uniquement la bordure
    else:
        pygame.draw.rect(screen, color, rectSize)  # colorier tout le rectangle


def flickering(timeFlickering, color):  # clignotement avec couleur 
    addNewRect(row, column, color, 5)
    pygame.display.flip()
    time.sleep(timeFlickering)
    addNewRect(row, column, WHITE, 5)
    pygame.display.flip()
    time.sleep(timeFlickering)
    addNewRect(row, column, color, 5)
    pygame.display.flip()
    time.sleep(timeFlickering)
    addNewRect(row, column, WHITE, 5)
    pygame.display.flip()


def drawTheBorder():
    dif = 500 // 9
    for i in range(10):
        thick = 5
        pygame.draw.line(screen, PURPLE, (0, i * dif + 2), (500, i * dif + 2), thick)
        pygame.draw.line(screen, PURPLE, (i * dif + 2, 0), (i * dif + 2, 500), thick)
    for i in range(10):
        if i % 3 == 0:
            thick = 8
            pygame.draw.line(screen, BLEU, (0, i * dif), (500, i * dif), thick)
            pygame.draw.line(screen, BLEU, (i * dif, 0), (i * dif, 500), thick)


def drawInitBoard():

    for row in range(len(Board)):
        for column in range(len(Board[row])):
            color = L_GRAY
            if Board[row][column] == 0: # si nous voulons passer à l'arrière-plan des cellules vides
                color = WHITE
                
            # ----- dessiner le rectangle ------
            pygame.draw.rect(screen, color,
                             [(MARGIN + WIDTH) * column + MARGIN, 
                             (MARGIN + HEIGHT) * row + MARGIN, 
                             WIDTH, HEIGHT])
            # n'affiche rien si le nombre est 0
            font = pygame.font.Font('freesansbold.ttf', 32)
            if Board[row][column] == 0:
                text = font.render(" ", True, BLACK, )  
            else:
                text = font.render(str(Board[row][column]), True, BLACK, )

            textRect = text.get_rect()  # get_rect() -> Returns a new rectangle covering the entire surface.
            textRect.center = (
                (MARGIN + WIDTH) * column + MARGIN + WIDTH / 2, (MARGIN + HEIGHT) * row + MARGIN + WIDTH / 2)
            screen.blit(text, textRect)
            drawTheBorder()


# -------- Boucle du programme principal -----------
if __name__ == "__main__":
    flag1 = True
    # lancer une musique en continu
    while flag1:
        # lancer une musique en continu
        mixer.music.load("assets/sounds/background.wav")
        mixer.music.play()
        level = chooseLevel()
        if level == 1 or level == 2 or level == 3:
            print("\n"
                  "Le niveau choisi est le numéro ",level)
            flag1 = False
    pygame.display.set_caption("Sudoku ECE")
    screen = pygame.display.set_mode(size)

    sol = mainSolver(level)  # d'abord le script résout le sudoku tout seul

    print("La solution du SUDOKU généré est la suivante :")
    printBoard(sol)

    # ------ dessiner le tableau ------
    pygame.init()
    screen.fill(BLACK)
    drawInitBoard()
    readyForInput = False
    key = None

    # mettre un timer sur le tableau
    font_clock = pygame.font.SysFont(None, 32)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while not done:
        # --- Boucle d'événement principale

        for event in pygame.event.get():
            #musique en boucle lors de la partie
            mixer.music.load("assets/sounds/Babydoll.mp3")
            mixer.music.play(-1)
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in numbers_1to9:
                    key = chr(event.key)
                if event.key == pygame.K_RETURN:
                    finish()
                if event.key == pygame.K_c:
                    cheatingAllTheWay()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ------ si cliqué sur une cellule obtenir sa ligne et sa colonne ------
                if readyForInput is True:
                    addNewRect(row, column, WHITE, None)
                    drawTheBorder()
                    readyForInput = False

                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (WIDTH + MARGIN)
                # ------ vérifier s'il est vide (0 à l'intérieur) ------
                if Board[row][column] == 0:
                    # ------ colorier la bordure de la cellule cliquée ----- #TODO JAUNE
                   
                    addNewRect(row, column, YELLOW, 5)
                    readyForInput = True
                    # ------ maintenant attendre l'entrée de l'utilisateur -----

        # initialisation du timer
        counting_time = pygame.time.get_ticks() - start_time

        # change milliseconds into minutes, seconds, milliseconds
        counting_minutes = str(counting_time // 60000).zfill(2)
        counting_seconds = str((counting_time % 60000) // 1000).zfill(2)
        counting_millisecond = str(counting_time % 1000).zfill(3)

        counting_string = "%s:%s:%s" % (counting_minutes, counting_seconds, counting_millisecond)
        # print(counting_string)

        counting_text = font_clock.render(str(counting_string), True, (0, 0, 0), (255, 255, 255))
        counting_rect = counting_text.get_rect(width=110, bottomright=screen.get_rect().bottomright)

        screen.blit(counting_text, counting_rect)

        # vérification du nombre saisie
        if readyForInput and key is not None:
            # ------ vérifier si la clé est bonne à sa place ------
            if int(key) == sol[row][column]:
                Board[row][column] = key
                flickering(0.1, GREEN)  # clignoter 0.2 seconde avec la couleur verte
                addNumToBoard(key, row, column, L_GREEN)
                # son de réussite si bon numéro
                errorSound = mixer.Sound("assets/sounds/bonneReponse.wav")
                errorSound.play()
            else:
                flickering(0.1, RED)  # clignoter 0,2 seconde avec la couleur rouge
                addNumToBoard(key, row, column, L_RED)
                # son d'erreur si mauvais numéro
                errorSound = mixer.Sound("assets/sounds/explosion.wav")
                errorSound.play()

            # -----------------------------------------------
            drawTheBorder()
            readyForInput = False

        key = None
        pygame.display.flip()
        pygame.display.update()
        clock.tick(25)

# Fermez la fenêtre et quittez.
pygame.quit()
