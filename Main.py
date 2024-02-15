from fltk import *
import time
import random
import math

# Changeable values

taille_case = 30
cases_longueur = 10
cases_hauteur = 24
COULEUR_BG = "white"    # Can change this value to "black" instead for a black background
gravite = 1     # Intervalle de temps pour que la pièce tombe en secondes
RANDOM_BAGS = False         # This variable can take the values : True, False
# It can either have the value False to have 7-bags or True for random bags.
lockdelay = 1


# Values to not change

longueur_plateau = taille_case * cases_longueur * 1.7
hauteur_plateau = taille_case * cases_hauteur

SAC = ["I", "T", "L", "J", "S", "Z", "O"]
COULEUR_INVERSE_BG = "black" if COULEUR_BG == "white" else "white"
COULEURS = ["pink", "#00CCFF", "yellow", "lime", "red", "orange", "dark blue"]      # List of colors for the respective pieces below them
        #     T   ,     I    ,    O    ,   S   ,   Z  ,     L   ,      J
score = 0
line_clears = 0


def initialiser_interface() -> None :
    """Initialise l'interface."""
    cree_fenetre(longueur_plateau, hauteur_plateau)


    # Background
    rectangle(0, 0, longueur_plateau, hauteur_plateau, COULEUR_BG, COULEUR_BG, tag="bg")


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
    texte(13.5 * taille_case, hauteur_plateau - 13/5 * taille_case, "Lines cleared :", COULEUR_INVERSE_BG, "center", taille=18, tag="LIGNES")
        

    # Zone de jeu
    for i in range(cases_longueur + 1) :
        ligne(i * taille_case, 0, i * taille_case, hauteur_plateau, COULEUR_INVERSE_BG, tag="bordure")
    for i in range(cases_hauteur) :
        ligne(0, i * taille_case, longueur_plateau / 1.7, i * taille_case, COULEUR_INVERSE_BG, tag="bordure")


def remplir_case(i: int, j: int, piece: str) -> None :
    """Colorie la case plateau[i][j] avec la couleur indiqué."""
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


def affichage_plateau(plateau: list, lst: list, piece: str) -> None :
    """Rafraichis l'affichage du plateau."""
    efface("piece")
    for l, c in lst :
        remplir_case(l, c, piece)
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
                rectangle(j * taille_case, 6.5 * taille_case, (j + 1) * taille_case, 7.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[0], tag="next")
                if j == 13 :
                    rectangle(j * taille_case, 7.5 * taille_case, (j + 1) * taille_case, 8.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[0], tag="next")
            
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
                rectangle(j * taille_case, 6.5 * taille_case, (j + 1) * taille_case, 7.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[5], tag="next")
                if j == 12 :
                    rectangle(j * taille_case, 7.5 * taille_case, (j + 1) * taille_case, 8.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[5], tag="next")
            
            elif piece == "J" :
                rectangle(j * taille_case, 6.5 * taille_case, (j + 1) * taille_case, 7.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[6], tag="next")
                if j == 14 :
                    rectangle(j * taille_case, 7.5 * taille_case, (j + 1) * taille_case, 8.5 * taille_case, COULEUR_INVERSE_BG, COULEURS[6], tag="next")

    # Rafraichissage du score
    if score > 0 :
        nb_zeros = 7 - round((math.log10(score))) if 7 - round((math.log10(score))) >= 0 else 0
        texte(13.5 * taille_case, 16/5 * taille_case, "0" * nb_zeros + str(round(score)), COULEUR_INVERSE_BG, "center", tag="score")
    else :
        texte(13.5 * taille_case, 16/5 * taille_case, "0000000", COULEUR_INVERSE_BG, "center", tag="score")

    # Rafraichissage des lignes remplies
    texte(13.5 * taille_case, hauteur_plateau - 7/5 * taille_case, str(lines), COULEUR_INVERSE_BG, "center", taille=18, tag="lines")


def initialiser_matrice(n: int, p: int) -> list :
    """Crée et renvoie une matrice de taille n * p."""
    return [[None for i in range(p)] for j in range(n)]


def nouvelle_piece(plateau: list, piece: list) -> list :
    """Renvoie une liste de 4 couples de coordonnées s'il n'y a pas d'obstacles."""
    lst = []
    if piece == "I" :
        for i in range(-2, 2) :
            if plateau[0][i + cases_longueur // 2] != None :
                return lst
            lst.append((0, i + cases_longueur // 2))
    
    elif piece == "O" :
        for i in range(2) :
            for j in range(-1, 1) :
                if plateau[i][cases_longueur // 2 + j] != None :
                    return lst
                lst.append((i, j + cases_longueur // 2))

    elif piece in ["T", "L", "J"] :
        for i in range(-1, 2) :
            if ((piece == "L" and i == -1)
            or  (piece == "T" and i == 0)
            or  (piece == "J" and i == 1)) :
                for j in range(2) :
                    if plateau[j][cases_longueur // 2 + i] != None :
                        return lst
                    lst.append((j, i + cases_longueur // 2))

            else :
                if plateau[0][cases_longueur // 2 + i] != None :
                    return lst
                lst.append((0, i + cases_longueur // 2))
            

    else :
        for i in range(-1, 2) :
            if ((i == -1 and piece == "S")
            or  (i == 1 and piece == "Z")) :
                if plateau[1][cases_longueur // 2 + i] != None :
                    return lst
                lst.append((1, i + cases_longueur // 2))

            elif i == 0 :
                for j in range(2) :
                    if plateau[j][i] != None :
                        return lst
                    lst.append((j, i + cases_longueur // 2))
            
            else :
                if plateau[0][i + cases_longueur // 2] != None :
                    return lst
                lst.append((0, i + cases_longueur // 2))
    
    return lst


def deplacement_piece(plateau: list, lst: list, dir: str) -> list :
    """Effectue le déplacement dans la direction indiquée."""
    lst_deplace = list()
    if any(c <= 0 or plateau[l][c - 1] != None for l, c in lst) and dir == "Left" :
        return lst
    elif any(c >= cases_longueur - 1 or plateau[l][c + 1] != None for l, c in lst) and dir == "Right" :
        return lst
    elif dir == "Down" :
        if (any(l >= cases_hauteur - 1 for l, c in lst)
         or any(plateau[l + 1][c] != None and (l + 1, c) not in lst for l, c in lst)) :
            return lst
    
    for l, c in lst :
        if dir == "Left" :
            lst_deplace.append((l, c - 1))
        elif dir == "Right" :
            lst_deplace.append((l, c + 1))
        elif dir == "Down" :
            lst_deplace.append((l + 1, c))
    return lst_deplace


def pose_piece(plateau: list, lst: list) -> bool :
    """Renvoie True si la pièce doit être placé et False dans le cas contraire."""
    if (any(l >= cases_hauteur - 1 for l, c in lst)
     or any(plateau[l + 1][c] != None and (l + 1, c) not in lst for l, c in lst)) :
        return True
    return False


def creation_lst_modifie(lst_coords: list, piece: str) -> tuple :
    """Renvoie la liste modifié avec comme origine le deuxième ou troisième point de la liste."""
    lst_modifie = list()

    if piece in ["T", "S", "J"] :
        for x, y in lst_coords :
            lst_modifie.append((x - lst_coords[1][0], y - lst_coords[1][1]))
            origine = lst_coords[1]

    elif piece in ["I", "Z", "L"] :
        for x, y in lst_coords :
            lst_modifie.append((x - lst_coords[2][0], y - lst_coords[2][1]))
            origine = lst_coords[2]
        
    return lst_modifie, origine


def rotation(lst_coords: list, piece: str, dir: str) -> list :
    """Renvoie la liste des coordonnées modifié avec la rotation dans le sens dir."""

    lst_modifie, origine = creation_lst_modifie(lst_coords, piece)
    lst_coords_modifie = list()
    lst_resultat = list()

    for x, y in lst_modifie :
        if dir == "Clockwise" :
            lst_coords_modifie.append((y, -x))
        else :
            lst_coords_modifie.append((-y, x))
    
    for x, y in lst_coords_modifie :
        lst_resultat.append((x + origine[0], y + origine[1]))

    return lst_resultat



def rotation_piece(coord_piece: list, piece: str, dir: str) -> list :
    """Modifie les coordonnées de piece avec la rotation dir s'il n'y a aucun obstacles."""
    lst = list()

    if piece == "O" :
        return coord_piece

    lst = rotation(coord_piece, piece, dir)

    if all(0 <= j <= cases_longueur - 1 and 0 <= i <= cases_hauteur - 1 for i, j in lst) :
        if all(plateau[i][j] == None for i, j in lst) :
            return lst
    return coord_piece


def rafraichir_plateau(plateau) -> int :
    """Modifie le plateau si une ligne est remplie et renvoie le nombre de lignes remplies."""
    line_clears = 0
    for i in range(len(plateau)) :
        if all(_ != None for _ in plateau[i]) :
            line_clears += 1
            for j in range(len(plateau[i])) :
                plateau[i][j] = None
                if any(plateau[i - k][j] != None for k in range(i)) :        # S'il y a aucun bloc au dessus de la ligne, ne pas déplacer les lignes au dessus
                    for k in range(i) :
                        plateau[i - k - 1][j], plateau[i - k][j] = plateau[i - k][j], plateau[i - k - 1][j]
    return line_clears


def hard_drop(plateau: list, coord_cases: list, piece: str) -> float :
    """Place la pièce le plus bas possible dans le plateau."""
    i = 0
    while not pose_piece(plateau, coord_cases) :
        coord_cases = deplacement_piece(plateau, coord_cases, "Down")
        i += 1/15
    for l, c in coord_cases :
        plateau[l][c] = piece
    return i


if __name__ == "__main__" :


    initialiser_interface()

    plateau = initialiser_matrice(cases_hauteur, cases_longueur)
    if not RANDOM_BAGS :
        sac_en_cours = list(SAC)
        piece = random.choice(sac_en_cours)
        sac_en_cours.remove(piece)
        next_piece = random.choice(sac_en_cours)
        sac_en_cours.remove(next_piece)
    else :
        piece = random.choice(SAC)
        next_piece = random.choice(SAC)
    coord_cases = nouvelle_piece(plateau, piece)
    affichage_plateau(plateau, coord_cases, piece)
    update_affichage(score, line_clears, next_piece)
    tgrav1 = time.perf_counter()
    active = False
    

    while True:
        ev = donne_ev()
        tev = type_ev(ev)

        t2 = time.perf_counter()
        if t2 - tgrav1 >= gravite :
            coord_cases = deplacement_piece(plateau, coord_cases, "Down")
            affichage_plateau(plateau, coord_cases, piece)
            tgrav1 = t2


        if active :
            if t2 - tlockdelay1 >= lockdelay :
                if pose_piece(plateau, coord_cases) :
                    for l, c in coord_cases :
                        plateau[l][c] = piece
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
                    if not RANDOM_BAGS :
                        piece, next_piece = next_piece, random.choice(sac_en_cours)
                        sac_en_cours.remove(next_piece)
                        if len(sac_en_cours) == 0 :
                            sac_en_cours = list(SAC)
                    else :
                        piece, next_piece = next_piece, random.choice(SAC)
                    coord_cases = nouvelle_piece(plateau, piece)
                    if len(coord_cases) != 4 :
                        break
                    else :
                        affichage_plateau(plateau, coord_cases, piece)
                        update_affichage(score, line_clears, next_piece)
                    active = False
        else :
            if pose_piece(plateau, coord_cases) :
                tlockdelay1 = time.perf_counter()
                active = True


        if tev == "Touche" :
            nom_touche = touche(ev)

            if nom_touche in ["Left", "Right", "Down"] :
                coord_cases = deplacement_piece(plateau, coord_cases, nom_touche)
                if nom_touche == "Down" :
                    score += 1/20
                    update_affichage(score, line_clears, next_piece)
                affichage_plateau(plateau, coord_cases, piece)
            
            elif nom_touche == "Up" :
                score += hard_drop(plateau, coord_cases, piece)
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
                if not RANDOM_BAGS :
                    piece, next_piece = next_piece, random.choice(sac_en_cours)
                    sac_en_cours.remove(next_piece)
                    if len(sac_en_cours) == 0 :
                        sac_en_cours = list(SAC)
                else :
                    piece, next_piece = next_piece, random.choice(SAC)
                coord_cases = nouvelle_piece(plateau, piece)
                if len(coord_cases) != 4 :
                    break
                else :
                    affichage_plateau(plateau, coord_cases, piece)
                    update_affichage(score, line_clears, next_piece)

            
            elif nom_touche in ["a", "e"] :
                if nom_touche == "a" :
                    coord_cases = rotation_piece(coord_cases, piece, "AntiClockwise")
                else :
                    coord_cases = rotation_piece(coord_cases, piece, "Clockwise")
                affichage_plateau(plateau, coord_cases, piece)


        if tev == "Quitte" :
            break
        mise_a_jour()

    ferme_fenetre()
