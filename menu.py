import pygame
from pygame import mixer

import main_soduku

from pygame.locals import *

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.init(22050,-16,2,1024)
# dimension de la fenêtre adaptée à l'image de fond

class Application:
    # Classe maîtresse gérant les différentes interfaces du jeu
    def __init__(self):
        size = (700, 700)
        pygame.init()
        pygame.display.set_caption("Menu SUDOKU ECE")

        ## Creation de la fenêtre au dimension souhaitée
        self.fenetre = pygame.display.set_mode((size))

        ## Chargement et insertion de l'image de fond sur la fenêtre principale
        self.fond = pygame.image.load("assets/images/menu.png")
        self.fenetre.blit(self.fond, (0, 0))  # mise de l'image en arrière-plan
        pygame.display.flip()

        # Groupe de sprites utilisé pour l'affichage
        # Les sprites permettent d'organiser les différents objets du code
        # Group fait aussi partie du module spirite qui est fait pour la réalisation des jeux en pygame
        self.groupeGlobal = pygame.sprite.Group()
        self.statut = True

    def _initialiser(self):
        try:
            self.ecran.detruire()
            # Suppression de tous les sprites(classe pour organiser les objets) du groupe
            self.groupeGlobal.empty()
        except AttributeError:
            pass

    def menu(self):
        # Affichage du menu
        self._initialiser()
        self.ecran = Menu(self, self.groupeGlobal)

    def jeu(self):
        # Affichage du jeu
        main_soduku.chooseLevel()

    def informations(self):
        ## Affichage de la fenetre A propos pour avoir les règles du jeu
        # Ouverture d'une fenêtre avec les règles du jeu
        self._initialiser()
        size = (700, 700)
        self.ecran = Regle(self, self.groupeGlobal)
        pygame.init()
        pygame.display.set_caption("SUDOKU")

        # Création de la fenêtre aux dimensions souhaitées
        self.fenetre = pygame.display.set_mode((size))

        ## Chargement et insertion de l'image de fond sur la fenêtre principale
        self.fond = pygame.image.load("assets/images/objectif.png")
        self.fenetre.blit(self.fond, (0, 0))  # Mise de l'image en arrière-plan

        pygame.display.flip()

    def quitter(self):
        ## Fermeture de la fenêtre
        self.statut = False


    def update(self):
        ## Mise à jour de la fenêtre après chaque action effectuée
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.quitter()
                return

        self.ecran.update(events)
        self.groupeGlobal.update()
        self.groupeGlobal.draw(self.fenetre)
        pygame.display.update()


class Menu:
    # Création et gestion des boutons d'un menu
    def __init__(self, application, *groupes):
        # Couleur prise par les boutons en fonction des commandes
        self.couleurs = dict(
            normal=(240, 253, 113),
            survol=(200, 0, 0),
        )
        font = pygame.font.SysFont('Helvetica', 15, bold=True)

        ## Noms des boutons et commandes associées
        items = (
            ('JOUER', application.jeu),
            ('RÈGLES', application.informations),
            ('QUITTER', application.quitter)
        )

        ## Coordonnées du premier bouton sur la fenêtre
        x = 350
        y = 450

        self._boutons = []
        for texte, cmd in items:
            # Caractéristique appliquée à l'ensemble des boutons
            mb = MenuBouton(
                texte,
                self.couleurs['normal'],
                font,
                x,
                y,
                100,
                50,
                cmd
            )
            self._boutons.append(mb)
            # Augmentation de la valeur de y pour créer les boutons à la suite
            y += 100
            for groupe in groupes:
                groupe.add(mb)

    def update(self, events):
        # Détecte si le clique gauche a été utilisé
        clicGauche, *_ = pygame.mouse.get_pressed()
        posPointeur = pygame.mouse.get_pos()
        for bouton in self._boutons:
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur):
                # Changement du curseur de base
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                # Changement de la couleur du bouton
                bouton.dessiner(self.couleurs['survol'])
                # Si le clic gauche a été pressé
                if clicGauche:
                    # Appel de la fonction du bouton
                    bouton.executerCommande()
                break
            else:
                # Le pointeur n'est pas au-dessus du bouton
                bouton.dessiner(self.couleurs['normal'])
        else:
            # Le pointeur n'est pas au-dessus d'un des boutons
            ## Initialisation du pointeur par défaut
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    def detruire(self):
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)  # Initialisation du pointeur


class MenuBouton(pygame.sprite.Sprite):
    # Création d'un simple bouton rectangulaire
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande):
        super().__init__()
        self._commande = commande
        # Création des dimensions des boutons
        self.image = pygame.Surface((largeur, hauteur))
        # Positionnement sur la fenêtre
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Caractéristique du texte dans les boutons
        self.texte = font.render(texte, True, (0, 0, 0))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (largeur / 2, hauteur / 2)

    def dessiner(self, couleur):
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)

    def executerCommande(self):
        # Appel de la commande du bouton
        self._commande()


class Regle:
    # Ouvre une nouvelle interface quand on clique sur un bonton
    def __init__(self, jeu, application, surfaceH=20, *groupes):
        self._fenetre = jeu.fenetre
        # Itertools est un module qui permet de créer différentes itérations
        # Ici, cycle permet de répeter une boucle à l'infini
        from itertools import cycle
        couleurs = [(0, 0, i) for i in range(0, 256, 15)]
        couleurs.extend(sorted(couleurs[1:-2], reverse=True))
        self._couleurTexte = cycle(couleurs)

        # Création d'un texte sur la nouvelle interface
        # Caractéristique du texte et position
        self._font = pygame.font.SysFont('Helvetica', 20, bold=True)
        self.creerTexte()
        self.position = (
            surfaceH / 2 - 350, surfaceH / 2 + 500)  ## Ajout pour le positionnement du texte sur la surface de jeu
        # Création d'un event
        #self._CLIGNOTER = pygame.USEREVENT + 1
        #pygame.time.set_timer(self._CLIGNOTER, 80)

    def creerTexte(self):
        size = (700,600)
        self.img = pygame.image.load("assets/images/objectif.png")
        self.fenetre = pygame.display.set_mode((size))
        ## str: méthode string pour le formatage des chaines
        self.fenetre.blit(self.img, (0, 0))  # Mise de l'image en arrière plan


    def update(self, events):
        # Mise à jour la fenêtre selon certaines conditions
        self._fenetre.blit(self.img, self.position)

        for event in events:
            #if event.type == self._CLIGNOTER:
                self.creerTexte()
                break

    def detruire(self):
        pygame.time.set_timer(self._CLIGNOTER, 0)  # Désactivation du timer"""


##----------------------------------FONCTION PRINCIPALE-------------------------------------------------------
app = Application()
app.menu()
mixer.music.load("assets/sounds/background.wav")
mixer.music.play()

## Départ avec un timer permettant de maintenir la fenêtre ouverte
clock = pygame.time.Clock()

while app.statut == True:
     app.update()
     clock.tick(30)


if app.statut == False:
    pygame.quit()  # Fermeture de pygame
