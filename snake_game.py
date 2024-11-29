import pygame
import random
import sys

# Initialisation de pygame
pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (213, 50, 80)  # Nourriture
GRIS = (169, 169, 169)  # Obstacles
VERT = (0, 255, 0)  # Serpent
BLEU = (50, 153, 213)
JAUNE = (255, 255, 0)  # Bonus
VIOLET = (128, 0, 128)  # Malus

# Dimensions de l'écran
LARGEUR = 800
HAUTEUR = 600

# Initialiser la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu du Serpent Multilingue")

horloge = pygame.time.Clock()
taille_bloc = 20
vitesse = 10  # Vitesse initiale du jeu

# Police pour les scores et les messages
police = pygame.font.SysFont("bahnschrift", 25)
police_score = pygame.font.SysFont("comicsansms", 35)
police_menu = pygame.font.SysFont("comicsansms", 30)

# Traductions
translations = {
    "fr": {
        "title": "Jeu du Serpent",
        "high_score": "Meilleur Score :",
        "play": "Appuyez sur J pour jouer",
        "quit": "Appuyez sur Q pour quitter",
        "tutorial": "Contrôles : Flèches pour bouger, P pour pause.",
        "food": "Nourriture (rouge) : +10 points.",
        "bonus": "Bonus (jaune) : +50 points.",
        "malus": "Malus (violet) : Rétrécit le serpent.",
        "game_over": "Perdu ! Appuyez sur C pour rejouer ou Q pour quitter.",
        "start_message": "Appuyez sur les flèches pour commencer."
    },
    "en": {
        "title": "Snake Game",
        "high_score": "High Score:",
        "play": "Press J to Play",
        "quit": "Press Q to Quit",
        "tutorial": "Controls: Arrows to move, P to pause.",
        "food": "Food (red): +10 points.",
        "bonus": "Bonus (yellow): +50 points.",
        "malus": "Malus (purple): Shrinks the snake.",
        "game_over": "Game Over! Press C to retry or Q to quit.",
        "start_message": "Press arrow keys to start."
    }
}

# Charger le meilleur score
def charger_highscore():
    try:
        with open("highscore.txt", "r") as fichier:
            return int(fichier.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

# Sauvegarder un nouveau meilleur score
def sauvegarder_highscore(highscore):
    with open("highscore.txt", "w") as fichier:
        fichier.write(str(highscore))

# Générer une position pour la nourriture ou les bonus/malus
def generer_nourriture(obstacles):
    while True:
        nourriture_x = round(random.randrange(0, LARGEUR - taille_bloc) / taille_bloc) * taille_bloc
        nourriture_y = round(random.randrange(0, HAUTEUR - taille_bloc) / taille_bloc) * taille_bloc
        if (nourriture_x, nourriture_y) not in obstacles:
            return nourriture_x, nourriture_y

# Affichage du score
def affichage_score(score, highscore, lang="en"):
    t = translations[lang]
    texte = police_score.render(f"{t['high_score']} {highscore} | Score: {score}", True, BLEU)
    fenetre.blit(texte, [10, 10])

# Dessiner le serpent segmenté
def notre_serpent(taille_bloc, liste_corps):
    for i, segment in enumerate(liste_corps):
        if i == len(liste_corps) - 1:  # Tête du serpent
            pygame.draw.rect(fenetre, VERT, [segment[0], segment[1], taille_bloc, taille_bloc])
        else:
            pygame.draw.rect(fenetre, VERT, [segment[0], segment[1], taille_bloc, taille_bloc])
            pygame.draw.rect(fenetre, NOIR, [segment[0] + 2, segment[1] + 2, taille_bloc - 4, taille_bloc - 4])

# Gestion de la pause
def gerer_pause(lang="en"):
    t = translations[lang]  # Obtenir les textes traduits
    pause = True
    while pause:
        texte_pause = police_menu.render(t["tutorial"], True, BLANC)
        fenetre.fill(NOIR)
        fenetre.blit(texte_pause, [LARGEUR // 6, HAUTEUR // 3])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Reprendre le jeu
                    pause = False

# Affichage du menu principal multilingue
def afficher_menu():
    menu = True
    lang = "en"  # Par défaut, le menu est en anglais

    while menu:
        fenetre.fill(NOIR)
        selection_langue = police.render("Press F for French / Press E for English", True, BLANC)
        fenetre.blit(selection_langue, [LARGEUR // 10, HAUTEUR // 3])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    lang = "fr"
                    menu = False
                elif event.key == pygame.K_e:
                    lang = "en"
                    menu = False

    afficher_menu_jeu(lang)

# Affichage du menu principal en fonction de la langue
def afficher_menu_jeu(lang="en"):
    menu = True
    highscore = charger_highscore()
    t = translations[lang]  # Obtenir les textes traduits
    while menu:
        fenetre.fill(NOIR)

        # Titres et instructions traduits
        fenetre.blit(police_menu.render(t["title"], True, VERT), [LARGEUR // 4, HAUTEUR // 6])
        fenetre.blit(police.render(f"{t['high_score']} {highscore}", True, BLEU), [LARGEUR // 4, HAUTEUR // 6 + 50])
        fenetre.blit(police.render(t["play"], True, BLANC), [LARGEUR // 4, HAUTEUR // 6 + 100])
        fenetre.blit(police.render(t["quit"], True, BLANC), [LARGEUR // 4, HAUTEUR // 6 + 140])
        fenetre.blit(police.render(t["tutorial"], True, BLANC), [LARGEUR // 4, HAUTEUR // 6 + 180])
        fenetre.blit(police.render(t["food"], True, ROUGE), [LARGEUR // 4, HAUTEUR // 6 + 240])
        fenetre.blit(police.render(t["bonus"], True, JAUNE), [LARGEUR // 4, HAUTEUR // 6 + 280])
        fenetre.blit(police.render(t["malus"], True, VIOLET), [LARGEUR // 4, HAUTEUR // 6 + 320])

        # Mise à jour de l'écran
        pygame.display.update()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    menu = False
                    boucle_jeu(lang)
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Boucle principale du jeu
def boucle_jeu(lang="en"):
    global vitesse

    game_over = False
    game_close = False

    x1 = LARGEUR / 2
    y1 = HAUTEUR / 2
    x1_changement = 0
    y1_changement = 0

    liste_corps = []
    longueur_serpent = 1
    score = 0

    obstacles = [(random.randint(0, LARGEUR // taille_bloc) * taille_bloc,
                  random.randint(0, HAUTEUR // taille_bloc) * taille_bloc) for _ in range(5)]

    nourriture_x, nourriture_y = generer_nourriture(obstacles)
    bonus_x, bonus_y = generer_nourriture(obstacles)
    malus_x, malus_y = generer_nourriture(obstacles)
    highscore = charger_highscore()

    # Message de début
    t = translations[lang]
    debut_message = True
    while debut_message:
        fenetre.fill(NOIR)
        start_message = police_menu.render(t["start_message"], True, BLANC)
        fenetre.blit(start_message, [LARGEUR // 6, HAUTEUR // 3])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    debut_message = False

    while not game_over:

        while game_close:
            fenetre.fill(NOIR)
            message = police.render(t["game_over"], True, ROUGE)
            fenetre.blit(message, [LARGEUR // 6, HAUTEUR // 3])
            affichage_score(score, highscore, lang)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        boucle_jeu(lang)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_changement == 0:
                    x1_changement = -taille_bloc
                    y1_changement = 0
                elif event.key == pygame.K_RIGHT and x1_changement == 0:
                    x1_changement = taille_bloc
                    y1_changement = 0
                elif event.key == pygame.K_UP and y1_changement == 0:
                    y1_changement = -taille_bloc
                    x1_changement = 0
                elif event.key == pygame.K_DOWN and y1_changement == 0:
                    y1_changement = taille_bloc
                    x1_changement = 0
                elif event.key == pygame.K_p:
                    gerer_pause(lang)

        if x1 >= LARGEUR or x1 < 0 or y1 >= HAUTEUR or y1 < 0:
            game_close = True

        x1 += x1_changement
        y1 += y1_changement
        fenetre.fill((score % 255, score * 2 % 255, score * 3 % 255))

        pygame.draw.rect(fenetre, ROUGE, [nourriture_x, nourriture_y, taille_bloc, taille_bloc])
        pygame.draw.rect(fenetre, JAUNE, [bonus_x, bonus_y, taille_bloc, taille_bloc])
        pygame.draw.rect(fenetre, VIOLET, [malus_x, malus_y, taille_bloc, taille_bloc])

        for obstacle in obstacles:
            pygame.draw.circle(fenetre, GRIS, (obstacle[0] + taille_bloc // 2, obstacle[1] + taille_bloc // 2), taille_bloc // 2)

        tete = [x1, y1]
        liste_corps.append(tete)
        if len(liste_corps) > longueur_serpent:
            del liste_corps[0]

        for bloc in liste_corps[:-1]:
            if bloc == tete:
                game_close = True

        for obstacle in obstacles:
            if x1 == obstacle[0] and y1 == obstacle[1]:
                game_close = True

        notre_serpent(taille_bloc, liste_corps)
        affichage_score(score, highscore, lang)
        pygame.display.update()

        if x1 == nourriture_x and y1 == nourriture_y:
            nourriture_x, nourriture_y = generer_nourriture(obstacles)
            longueur_serpent += 1
            score += 10

        if x1 == bonus_x and y1 == bonus_y:
            score += 50
            bonus_x, bonus_y = generer_nourriture(obstacles)

        if x1 == malus_x and y1 == malus_y:
            longueur_serpent = max(1, longueur_serpent - 2)
            malus_x, malus_y = generer_nourriture(obstacles)

        if score > highscore:
            highscore = score
            sauvegarder_highscore(highscore)

        horloge.tick(vitesse)

    sauvegarder_highscore(highscore)
    pygame.quit()
    sys.exit()

# Lancer le menu en fonction de la langue
afficher_menu()
