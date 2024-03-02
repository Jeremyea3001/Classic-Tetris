

# Les valeurs qui peuvent être changé


taille_case = 30         # Valeur minimale : 1
# Taille des cases en pixels

cases_longueur = 10      # Valeur minimale : 4
# Nombre de cases en longueur (sur l'axe des abscisses)

cases_hauteur = 23       # Valeur minimale : 4
# Nombre de cases en hauteur (sur l'axe des ordonnée)

niveau = 1               # Valeur minimale : 1
# Niveau initiale

COULEUR_BG = "black"     # Valeurs possibles : "black", "white"
# Couleur du fond d'écran

RANDOM_BAGS = False      # Valeurs possibles : True, False
# False donne le système de 7-bag (plus de précisions sur Github)
# True donne des pièces de manière totalement aléatoire

LOCKDELAY = 1            # Valeur minimale : 0
# Temps (en seconde) avant qu'une pièce est posé après qu'il entre en contact avec un obstacles (en dessous de lui)

SD_SCORE = 1/20          # Valeur minimale : 0
# Nombre de score à chaque fois qu'un déplacement vers le bas est fait (avec la flèche du bas)
# La gravité ne donne pas ce score

HD_SCORE = 1/15          # Valeur minimale : SD_SCORE
# Nombre de score par déplacement vers le bas en utilisant le Hard Drop (avec la flèche du haut)


# -------------------------------------------------------------------------------------------------------------------


from fltk import *
import time
import random
import math
from Rotation import rotation


# -------------------------------------------------------------------------------------------------------------------


# Valeurs à ne pas changer


longueur_fenetre = taille_case * cases_longueur * 1.7
hauteur_fenetre = taille_case * cases_hauteur
# Taille de la fenêtre en pixels

gravite = 43/60
# Temps avant qu'une pièce tombe d'une ligne

SAC = ["I", "T", "L", "J", "S", "Z", "O"]
# Les pièces dans un sac

COULEUR_INVERSE_BG = "black" if COULEUR_BG == "white" else "white"
# Couleur inverse du fond d'écran

COULEURS = ["pink", "#00CCFF", "yellow", "lime", "red", "orange", "dark blue"]
        #     T   ,     I    ,    O    ,   S   ,   Z  ,     L   ,      J
# Liste des couleurs des pièces avec leur pièce respective en dessous

score = 0
line_clears = 0


# -------------------------------------------------------------------------------------------------------------------


class Piece :

    def __init__(self, nom_piece: str):
        """Initialisation de la pièce"""
        self.nom_piece = nom_piece
        # Nom de la pièce

        self.coord_cases = nouvelle_piece(self.nom_piece)
        # Coordonnées des cases de la pièce

        self.etat = 0
        # Etat de la pièce (orientation)

    
    def rotation(self, dir: str) -> None :
        """Modifie les coordonnées de piece avec la rotation normale dir s'il n'y a aucun obstacles."""

        if self.nom_piece == "O" :      # Si la pièce est le O, ne pas faire de rotation
            return None

        lst = rotation(self.coord_cases, self.nom_piece, dir)
        # Algorithme pour appliquer une rotation dans un sens

        if all(0 <= e[1] <= cases_longueur - 1 and 0 <= e[0] <= cases_hauteur - 1 for e in lst) :
        # Si une coordonnée n'est pas dans la matrice, ne pas exécuter la prochaine condition
            
            if all(plateau[i][j] == None for i, j in lst) :
            # Si un couple coordonnées a un obstacle dans le plateau, ne pas changer les coordonnées de la pièce
                self.coord_cases = lst


    def rotation_SRS(self, dir: str) -> None :
        """Modifie les coordonnées de piece avec la rotation SRS dans la direction dir."""

        if self.nom_piece == "O" :      # Même condition que pour rotation
            return None

        tests = [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]        # N.B. : Les coordonnées y de ces couples sont le contraire car 
        # Liste de tests, pour savoir si une de ces positions sont possibles
        # Pour plus d'informations sur ces tests, voir Github

        # En fonction de l'état de la pièce et de la direction de la rotation, le signe des tests diffèrent
        if self.etat == 0 :
            if dir == "Clockwise" :
                x = 1
            else :
                x = -1
            y = 1
        elif self.etat == 1 :
            x = -1
            y = -1
        elif self.etat == 2 :
            if dir == "Clockwise" :
                x = -1
            else :
                x = 1
            y = 1
        elif self.etat == 3 :
            x = 1
            y = -1


        lst = rotation(self.coord_cases, self.nom_piece, dir)
        # Même algorithme utilisé que dans la précédente méthode

        for test in tests :
            if all(0 <= e[1] + test[1] * y <= cases_longueur - 1 and 0 <= e[0] + test[0] * x <= cases_hauteur - 1 for e in lst) :
                if all(plateau[e[0] + test[0] * x][e[1] + test[1] * y] == None for e in lst) :
                # Mêmes tests que la précédente méthode
                    
                    for e in lst :
                        e[0] += test[0] * x
                        e[1] += test[1] * y
                    # Modification des coordonnées dans lst
                        
                    self.coord_cases = lst
                    break


        # En fonction de la direction de la rotation, l'état change :
        # Si la rotation est dans le sens de l'aiguille d'une montre, ajouter 1 à l'état
        # Sinon, soustraire 1
        if dir == "Clockwise" :
            if self.etat == 3 :
                self.etat = 0
            else :
                self.etat += 1
        
        else :
            if self.etat == 0 :
                self.etat = 3
            else :
                self.etat -= 1
        

# -------------------------------------------------------------------------------------------------------------------


    def deplacement(self, dir: str) -> None :
        """Effectue le déplacement dans la direction indiquée."""
        if all(e[1] > 0 for e in self.coord_cases) and dir == "Left" :
        # Si une coordonnée est déjà à l'extrémité et que le déplacement est vers la gauche,
        # Ne pas effectuer le déplacement
            
            if all(plateau[e[0]][e[1] - 1] == None for e in self.coord_cases) :
            # S'il y a un obstacle aux coordonnées après le déplacement,
            # Ne pas effectuer le déplacement

                for e in self.coord_cases :
                    e[1] -= 1

        elif all(e[1] < cases_longueur - 1 for e in self.coord_cases) and dir == "Right" :
        # Idem que pour le premier bloc
            
            if all(plateau[e[0]][e[1] + 1] == None for e in self.coord_cases) :

                for e in self.coord_cases :
                    e[1] += 1

        elif all(e[0] < cases_hauteur - 1 for e in self.coord_cases) and dir == "Down" :
        # Idem que pour les 2 premiers blocs
            
            if all(plateau[e[0] + 1][e[1]] == None or [e[0] + 1, e[1]] in self.coord_cases for e in self.coord_cases) :
            
                for e in self.coord_cases :
                    e[0] += 1


def nouvelle_piece(piece: str) -> list :
    """Renvoie une liste de 4 couples de coordonnées s'il n'y a pas d'obstacles."""
    lst = []

    if piece == "I" :
        for i in range(-2, 2) :
            if plateau[0][i + cases_longueur // 2] != None :
                return False
            lst.append([0, i + cases_longueur // 2])
    

    elif piece == "O" :
        for i in range(2) :
            for j in range(-1, 1) :
                if plateau[i][cases_longueur // 2 + j] != None :
                    return False
                lst.append([i, j + cases_longueur // 2])


    elif piece in ["T", "L", "J"] :
        for i in range(-1, 2) :
            if ((piece == "L" and i == 1)
            or  (piece == "T" and i == 0)
            or  (piece == "J" and i == -1)) :
                for j in range(2) :
                    if plateau[j][cases_longueur // 2 + i] != None :
                        return False
                    lst.append([j, i + cases_longueur // 2])

            else :
                if plateau[1][cases_longueur // 2 + i] != None :
                    return False
                lst.append([1, i + cases_longueur // 2])
            

    else :
        for i in range(-1, 2) :
            if ((i == -1 and piece == "S")
            or  (i == 1 and piece == "Z")) :
                if plateau[1][cases_longueur // 2 + i] != None :
                    return False
                lst.append([1, i + cases_longueur // 2])

            elif i == 0 :
                for j in range(2) :
                    if plateau[j][i] != None :
                        return False
                    lst.append([j, i + cases_longueur // 2])
            
            else :
                if plateau[0][i + cases_longueur // 2] != None :
                    return False
                lst.append([0, i + cases_longueur // 2])
    
    return lst


def initialiser_interface() -> None :
    """Initialise l'interface."""

    cree_fenetre(longueur_fenetre, hauteur_fenetre)


    # Background
    rectangle(0, 0, longueur_fenetre, hauteur_fenetre, COULEUR_BG, COULEUR_BG, tag="bg")


    # Encadré SCORE et le texte
    rectangle(taille_case * cases_longueur * 1.1, 
              taille_case * 1, 
              taille_case * cases_longueur * 1.1 + taille_case * 5, 
              taille_case * 4, 
              COULEUR_INVERSE_BG, 
              epaisseur=2, 
              tag="encadre"
              )
    texte(13.5 * taille_case, 9/5 * taille_case, "SCORE", COULEUR_INVERSE_BG, "center", tag="SCORE")


    # Encadré NEXT et le texte
    rectangle(taille_case * cases_longueur * 1.1, 
              taille_case * 5, 
              taille_case * cases_longueur * 1.1 + taille_case * 5, 
              taille_case * 9, 
              COULEUR_INVERSE_BG, 
              epaisseur=2, 
              tag="encadre"
              )
    texte(13.5 * taille_case, 29/5 * taille_case, "NEXT", COULEUR_INVERSE_BG, "center", tag="NEXT")


    # Texte lignes remplis
    texte(13.5 * taille_case, hauteur_fenetre - 13/5 * taille_case, "Lines cleared :", COULEUR_INVERSE_BG, "center", taille=18, tag="LIGNES")
        

    # Zone de jeu
    for i in range(cases_longueur + 1) :
        ligne(i * taille_case, 0, i * taille_case, hauteur_fenetre, COULEUR_INVERSE_BG, tag="bordure")
    for i in range(cases_hauteur) :
        ligne(0, i * taille_case, longueur_fenetre / 1.7, i * taille_case, COULEUR_INVERSE_BG, tag="bordure")


def remplir_case(i: int, j: int, piece: str) -> None :
    """Colorie la case plateau[i][j] avec la couleur de la pièce correspondante."""
    if piece == "T" :
        couleur = COULEURS[0]
    elif piece == "I" :
        couleur = COULEURS[1]
    elif piece == "O" :
        couleur = COULEURS[2]
    elif piece == "S" :
        couleur = COULEURS[3]
    elif piece == "Z" :
        couleur = COULEURS[4]
    elif piece == "L" :
        couleur = COULEURS[5]
    elif piece == "J" :
        couleur = COULEURS[6]
    rectangle(j * taille_case, i * taille_case, (j + 1) * taille_case, (i + 1) * taille_case, COULEUR_INVERSE_BG, couleur, tag="piece")


def affichage_plateau(plateau: list, piece: Piece) -> None :
    """Rafraichis l'affichage du plateau."""
    efface("piece")
    for l, c in piece.coord_cases :
        remplir_case(l, c, piece.nom_piece)
    for i in range(len(plateau)) :
        for j in range(len(plateau[0])) :
            if plateau[i][j] != None :
                remplir_case(i, j, plateau[i][j])


def update_affichage(score: int, lines: int, piece: str) -> None :
    """Rafraichis l'affichage du score, des lignes et de la pièce suivante."""
    efface("next")
    efface("score")
    efface("lines")

    # Rafraichissage de la prochaine pièce
    if piece == "I" :
        for j in range(11, 15) :
            rectangle((j + 0.5) * taille_case, 7 * taille_case, (j + 1.5) * taille_case, 8 * taille_case, COULEUR_INVERSE_BG, COULEURS[1], tag="next")

    elif piece == "O":
        for j in range(12, 14) :
            for i in range(6, 8) :
                    rectangle((j + 0.5) * taille_case, (i + 0.5) * taille_case, (j + 1.5) * taille_case, (i + 1.5) * taille_case, COULEUR_INVERSE_BG, COULEURS[2], tag="next")

    else :
        for j in range(12, 15) :
            if piece == "T" :
                rectangle(j * taille_case, 7.5 * taille_case, (j + 1) * taille_case, 8.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[0], tag="next")
                if j == 13 :
                    rectangle(j * taille_case, 6.5 * taille_case, (j + 1) * taille_case, 7.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[0], tag="next")
            
            elif piece == "S" :
                if j <= 13 :
                    rectangle(j * taille_case, 7.5 * taille_case, (j + 1) * taille_case, 8.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[3], tag="next")
                if j >= 13 :
                    rectangle(j * taille_case, 6.5 * taille_case, (j + 1) * taille_case, 7.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[3], tag="next")
            
            elif piece == "Z" :
                if j <= 13 :
                    rectangle(j * taille_case, 6.5 * taille_case, (j + 1) * taille_case, 7.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[4], tag="next")
                if j >= 13 :
                    rectangle(j * taille_case, 7.5 * taille_case, (j + 1) * taille_case, 8.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[4], tag="next")
            
            elif piece == "L" :
                rectangle(j * taille_case, 7.5 * taille_case, (j + 1) * taille_case, 8.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[5], tag="next")
                if j == 14 :
                    rectangle(j * taille_case, 6.5 * taille_case, (j + 1) * taille_case, 7.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[5], tag="next")
            
            elif piece == "J" :
                rectangle(j * taille_case, 7.5 * taille_case, (j + 1) * taille_case, 8.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[6], tag="next")
                if j == 12 :
                    rectangle(j * taille_case, 6.5 * taille_case, (j + 1) * taille_case, 7.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[6], tag="next")

    # Rafraichissage du score
    if score > 0 :
        nb_zeros = 7 - round((math.log10(score))) if 7 - round((math.log10(score))) >= 0 else 0
        texte(13.5 * taille_case, 16/5 * taille_case, "0" * nb_zeros + str(round(score)), COULEUR_INVERSE_BG, "center", tag="score")
    else :
        texte(13.5 * taille_case, 16/5 * taille_case, "0000000", COULEUR_INVERSE_BG, "center", tag="score")

    # Rafraichissage des lignes remplies
    texte(13.5 * taille_case, hauteur_fenetre - 7/5 * taille_case, str(lines), COULEUR_INVERSE_BG, "center", taille=18, tag="lines")


def pose_piece(plateau: list, lst: list) -> bool :
    """Renvoie True si la pièce doit être placé et False dans le cas contraire."""
    if (any(l >= cases_hauteur - 1 for l, c in lst)
     or any(plateau[l + 1][c] != None and (l + 1, c) not in lst for l, c in lst)) :
        return True
    return False


def rafraichir_plateau(plateau) -> int :
    """Modifie le plateau si une ligne est remplie et renvoie le nombre de lignes remplies."""
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
    """Place la pièce le plus bas possible dans le plateau."""
    i = 0
    while not pose_piece(plateau, piece.coord_cases) :
        piece.deplacement("Down")
        i += HD_SCORE
    for l, c in piece.coord_cases :
        plateau[l][c] = piece.nom_piece
    return i


def update_gravity(level : int) -> float :
    """Donne la gravité correspondante au niveau donné."""
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
        
        initialiser_interface()

        plateau = [[None for _ in range(cases_longueur)] for __ in range(cases_hauteur)]
        if not RANDOM_BAGS :
            sac_en_cours = list(SAC)
            piece = Piece(random.choice(sac_en_cours))
            sac_en_cours.remove(piece.nom_piece)
            next_piece = random.choice(sac_en_cours)
            sac_en_cours.remove(next_piece)
        else :
            piece = Piece(random.choice(SAC))
            next_piece = random.choice(SAC)
        affichage_plateau(plateau, piece)
        update_affichage(score, line_clears, next_piece)
        tgrav1 = time.perf_counter()
        active = False
        

        while True:
            ev = donne_ev()
            tev = type_ev(ev)

            t2 = time.perf_counter()
            if t2 - tgrav1 >= gravite :
                piece.deplacement("Down")
                affichage_plateau(plateau, piece)
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
                            piece, next_piece = Piece(next_piece), random.choice(sac_en_cours)
                            sac_en_cours.remove(next_piece)
                            if len(sac_en_cours) == 0 :
                                sac_en_cours = list(SAC)
                        else :
                            piece, next_piece = Piece(next_piece), random.choice(SAC)
                        if not piece.coord_cases :
                            break
                        else :
                            affichage_plateau(plateau, piece)
                            update_affichage(score, line_clears, next_piece)
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
                        update_affichage(score, line_clears, next_piece)
                    affichage_plateau(plateau, piece)
                
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
                        piece, next_piece = Piece(next_piece), random.choice(sac_en_cours)
                        sac_en_cours.remove(next_piece)
                        if len(sac_en_cours) == 0 :
                            sac_en_cours = list(SAC)
                    else :
                        piece, next_piece = Piece(next_piece), random.choice(SAC)
                    if not piece.coord_cases :
                        break
                    else :
                        affichage_plateau(plateau, piece)
                        update_affichage(score, line_clears, next_piece)
                    active = False

                
                elif nom_touche in ["a", "e"] :
                    if nom_touche == "a" :
                        piece.rotation_SRS("AntiClockwise")
                    else :
                        piece.rotation_SRS("Clockwise")
                    affichage_plateau(plateau, piece)


            if tev == "Quitte" :
                break
            mise_a_jour()

        ferme_fenetre()
    
    except AssertionError:
        print("""
Des valeurs changeables ont un format incorrecte.\n
        Elles ne respectent pas :
        \t - Les valeurs minimales, ou
        \t - Les valeurs imposées
""")
