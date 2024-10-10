# Les valeurs qui peuvent être changé


taille_case = 30         # Valeur minimale : 1
# Taille des cases en pixels

cases_longueur = 10      # Valeur minimale : 4
# Nombre de cases en longueur (sur l'axe des abscisses)

cases_hauteur = 23       # Valeur minimale : 4
# Nombre de cases en hauteur (sur l'axe des ordonnée)

niveau = 10               # Valeur minimale : 1
# Niveau initiale

COULEUR_BG = "black"     # Valeurs possibles : "black", "white"
# Couleur du fond d'écran

RANDOM_BAGS = False      # Valeurs possibles : True, False
# False donne le système de 7-bag (plus de précisions sur Github)
# True donne des pièces de manière totalement aléatoire

LOCKDELAY = 1            # Valeur minimale : 0
# Temps (en seconde) avant qu'une pièce soit posé après qu'il entre en contact avec un obstacle (en dessous de lui)

SD_SCORE = 1/20          # Valeur minimale : 0
# Nombre de score à chaque fois qu'un déplacement vers le bas est fait (avec la flèche du bas)
# La gravité ne donne pas ce score

HD_SCORE = 1/15          # Valeur minimale : SD_SCORE
# Nombre de score par déplacement vers le bas en utilisant le Hard Drop (avec la flèche du haut)


# -------------------------------------------------------------------------------------------------------------------


from fltk import *
import time
import random
from Piece import Piece
from Interface import Interface


# -------------------------------------------------------------------------------------------------------------------


# Valeurs à ne pas changer


longueurFenetre = taille_case * cases_longueur * 1.7
hauteurFenetre = taille_case * cases_hauteur
# Taille de la fenêtre en pixels

gravite : float
# Temps avant qu'une pièce tombe d'une ligne

SAC = ["I", "T", "L", "J", "S", "Z", "O"]
# Les pièces dans un sac

score = 0
line_clears = 0


# -------------------------------------------------------------------------------------------------------------------


def pose_piece(plateau: list, lst: list) -> bool :
    """Détermine si une pièce doit être placée

    :param list plateau: Le plateau de jeu
    :param list lst: La liste de coordonnées de la pièce
    :return bool: Renvoie True si la pièce doit être placé et False dans le cas contraire.
    """
    if (any(l >= cases_hauteur - 1 for l, c in lst)
     or any(plateau[l + 1][c] != None and (l + 1, c) not in lst for l, c in lst)) :
        return True
    return False


def rafraichir_plateau(plateau) -> int :
    """Modifie le plateau si une ligne est remplie et renvoie le nombre de lignes remplies.

    :param _type_ plateau: Le plateau de jeu
    :return int: Renvoie le nombre de lignes remplies
    """
    line_clears = 0
    for i in range(len(plateau)) :
        if all(e != None for e in plateau[i]) :
            line_clears += 1
            for j in range(len(plateau[i])) :
                plateau[i][j] = None
                if any(plateau[i - k][j] != None for k in range(i)) :
                # S'il y a aucun bloc au dessus de la ligne, ne pas déplacer les lignes au dessus
                    
                    for k in range(i) :
                        plateau[i - k - 1][j], plateau[i - k][j] = plateau[i - k][j], plateau[i - k - 1][j]
    return line_clears


def hard_drop(plateau: list, piece: Piece) -> float :
    """Place la pièce le plus bas possible dans le plateau.

    :param list plateau: Le plateau de jeu
    :param Piece piece: La pièce à poser
    :return float: Le score obtenu avec cette action
    """
    i = 0
    while not pose_piece(plateau, piece.coord_cases) :
        piece.deplacement("Down")
        i += HD_SCORE
    for l, c in piece.coord_cases :
        plateau[l][c] = piece.nom_piece
    return i


def update_gravity(level : int) -> float :
    """Donne la gravité correspondante au niveau donné.

    :param int level: le niveau actuel
    :return float: La gravité en millisecondes
    """
    if level >= 29 :
        x = 1
    elif level >= 19 :
        x = 2
    elif level >= 16 :
        x = 3
    elif level >= 13 :
        x = 4
    elif level >= 10 :
        x = 5
    elif level == 9 :
        x = 6
    else :
        x = (8 - level) * 5 + 8
    return x / 60



if __name__ == "__main__" :


    try :

        assert (COULEUR_BG in ["white", "black"]
            and niveau > 0
            and HD_SCORE >=SD_SCORE
            and LOCKDELAY >= 0
            and type(RANDOM_BAGS) == bool
            and taille_case >= 1
            and cases_hauteur >= 4
            and cases_longueur >= 4)
        
        interface: Interface = Interface(longueurFenetre, hauteurFenetre, taille_case, cases_longueur, cases_hauteur, COULEUR_BG)

        interface.initialiser_interface()

        plateau = [[None for _ in range(cases_longueur)] for __ in range(cases_hauteur)]
        if not RANDOM_BAGS :
            sac_en_cours = list(SAC)
            piece = Piece(random.choice(sac_en_cours), cases_longueur, cases_hauteur, plateau)
            sac_en_cours.remove(piece.nom_piece)
            next_piece = random.choice(sac_en_cours)
            sac_en_cours.remove(next_piece)
        else :
            piece = Piece(random.choice(SAC), cases_longueur, cases_hauteur, plateau)
            next_piece = random.choice(SAC)

        gravite = update_gravity(niveau)
        held_piece = None
        interface.affichage_plateau(plateau, piece)
        interface.update_affichage(score, line_clears, next_piece, held_piece, 0)
        tgrav1 = time.perf_counter()
        active = False
        t2 = time.perf_counter()
        

        while True:
            ev = donne_ev()
            tev = type_ev(ev)
            
            fps = 1 // (time.perf_counter() - t2)
            t2 = time.perf_counter()
            if t2 - tgrav1 >= gravite :
                piece.deplacement("Down")
                interface.affichage_plateau(plateau, piece)
                tgrav1 = t2


            if active :
                if t2 - tlockdelay1 >= LOCKDELAY :
                    if pose_piece(plateau, piece.coord_cases) :
                        for l, c in piece.coord_cases :
                            plateau[l][c] = piece.nom_piece

                        line_clears_at_once = rafraichir_plateau(plateau)
                        if line_clears_at_once == 1 :
                            score += 40
                        elif line_clears_at_once == 2 :
                            score += 100
                        elif line_clears_at_once == 3 :
                            score += 300
                        elif line_clears_at_once == 4 :
                            score += 1200
                        line_clears += line_clears_at_once
                        if line_clears // (niveau * 10) > 0 :
                            niveau += 1
                            gravite = update_gravity(niveau)

                        if not RANDOM_BAGS :
                            piece, next_piece = Piece(next_piece, cases_longueur, cases_hauteur, plateau), random.choice(sac_en_cours)
                            sac_en_cours.remove(next_piece)
                            if len(sac_en_cours) == 0 :
                                sac_en_cours = list(SAC)
                        else :
                            piece, next_piece = Piece(next_piece, cases_longueur, cases_hauteur, plateau), random.choice(SAC)
                        if not piece.coord_cases :
                            break
                        else :
                            interface.affichage_plateau(plateau, piece)
                            interface.update_affichage(score, line_clears, next_piece, held_piece, fps)
                        active = False
            else :
                if pose_piece(plateau, piece.coord_cases) :
                    tlockdelay1 = time.perf_counter()
                    active = True


            if tev == "Touche" :
                nom_touche = touche(ev)

                if nom_touche in ["Left", "Right", "Down"] :
                    piece.deplacement(nom_touche)
                    if nom_touche == "Down" :
                        score += SD_SCORE
                        interface.update_affichage(score, line_clears, next_piece, held_piece, fps)
                    interface.affichage_plateau(plateau, piece)
                
                elif nom_touche == "Up" :
                    score += hard_drop(plateau, piece)

                    line_clears_at_once = rafraichir_plateau(plateau)
                    if line_clears_at_once == 1 :
                        score += 40
                    elif line_clears_at_once == 2 :
                        score += 100
                    elif line_clears_at_once == 3 :
                        score += 300
                    elif line_clears_at_once == 4 :
                        score += 1200
                    line_clears += line_clears_at_once
                    if line_clears // (niveau * 10) > 0 :
                        niveau += 1
                        gravite = update_gravity(niveau)

                    if not RANDOM_BAGS :
                        piece, next_piece = Piece(next_piece, cases_longueur, cases_hauteur, plateau), random.choice(sac_en_cours)
                        sac_en_cours.remove(next_piece)
                        if len(sac_en_cours) == 0 :
                            sac_en_cours = list(SAC)
                    else :
                        piece, next_piece = Piece(next_piece, cases_longueur, cases_hauteur, plateau), random.choice(SAC)
                    if not piece.coord_cases :
                        break
                    else :
                        interface.affichage_plateau(plateau, piece)
                        interface.update_affichage(score, line_clears, next_piece, held_piece, fps)
                    active = False

                elif nom_touche in ["a", "e"] :
                    if nom_touche == "a" :
                        piece.rotation_SRS("AntiClockwise")
                    else :
                        piece.rotation_SRS("Clockwise")
                    interface.affichage_plateau(plateau, piece)

                elif nom_touche == "space" :
                    held_piece, piece = piece.nom_piece, held_piece
                    active = False
                    if piece == None :
                        piece = next_piece
                        if not RANDOM_BAGS :
                            next_piece = random.choice(sac_en_cours)
                            sac_en_cours.remove(next_piece)
                            if len(sac_en_cours) == 0 :
                                sac_en_cours = list(SAC)
                        else :
                            next_piece = random.choice(SAC)
                    piece = Piece(piece, cases_longueur, cases_hauteur, plateau)



            if tev == "Quitte" :
                break
            mise_a_jour()
            interface.affichage_plateau(plateau, piece)
            interface.update_affichage(score, line_clears, next_piece, held_piece, fps)


        ferme_fenetre()
    
    except AssertionError:
        print("""
Des valeurs changeables ont un format incorrecte.\n
        Elles ne respectent pas :
        \t - Les valeurs minimales, ou
        \t - Les valeurs imposées
""")