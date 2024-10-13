# Les valeurs qui peuvent être changé


TAILLE_CASE = 30         # Valeur minimale : 1
# Taille des cases en pixels

CASES_LONGUEUR = 10      # Valeur minimale : 4
# Nombre de cases en longueur (sur l'axe des abscisses)

CASES_HAUTEUR = 23       # Valeur minimale : 4
# Nombre de cases en hauteur (sur l'axe des ordonnée)

level = 1                # Valeur minimale : 1
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

PIECE_QUEUE_LENGTH = 5   # Valeur minimale : 1
# Nombre de pièces visibles qui arriveront après la pièce courante


# -------------------------------------------------------------------------------------------------------------------


from fltk import cree_fenetre, type_ev, donne_ev, touche, ferme_fenetre, mise_a_jour, rectangle
import time
from piece import Piece
from interface import Interface
from piece_queue import Piece_Queue


# -------------------------------------------------------------------------------------------------------------------


# Valeurs à ne pas changer

gravite : float
# Temps avant qu'une pièce tombe d'une ligne

score = 0
line_clears = 0

longueurFenetre, hauteurFenetre = 1000, 1200


# -------------------------------------------------------------------------------------------------------------------


def pose_piece(plateau: list, piece: Piece) -> bool :
    """Détermine si une pièce doit être placée

    :param list plateau: Le plateau de jeu
    :param list lst: La liste de coordonnées de la pièce
    :return bool: Renvoie True si la pièce doit être placé et False dans le cas contraire.
    """
    coord_cases = piece.coord_cases
    if (any(l >= len(plateau) - 1 for l, c in coord_cases)
     or any(plateau[l + 1][c] != None and (l + 1, c) not in coord_cases for l, c in coord_cases)) :
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
    while not pose_piece(plateau, piece) :
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


def get_score(level: int, line_clears: int) -> float :
    """Donne le score correspondant au niveau et au nombre de lignes remplies d'un coup

    :param int level: Le niveau actuel
    :param int line_clears: Le nombre de lignes remplies d'un coup
    :return float: Le score correspondant
    """
    match line_clears :
        case 1 :
            score = 40
        case 2 :
            score = 100
        case 3 :
            score = 300
        case 4 :
            score = 400
        case _ :
            score = 0
    return score * level



if __name__ == "__main__" :


    try :

        assert (COULEUR_BG in ["white", "black"]
            and level > 0
            and HD_SCORE >= SD_SCORE
            and LOCKDELAY >= 0
            and type(RANDOM_BAGS) == bool
            and TAILLE_CASE >= 1
            and CASES_HAUTEUR >= 4
            and CASES_LONGUEUR >= 4)

    except AssertionError:
        print("""
Des valeurs changeables ont un format incorrecte.\n
Elles ne respectent pas :
\t - Les valeurs minimales, ou
\t - Les valeurs imposées
""")
        exit()
        
    plateau = [[None for _ in range(CASES_LONGUEUR)] for __ in range(CASES_HAUTEUR)]
    queue = Piece_Queue(PIECE_QUEUE_LENGTH, RANDOM_BAGS)

    interface = Interface(TAILLE_CASE, CASES_LONGUEUR, CASES_HAUTEUR, COULEUR_BG, queue, TAILLE_CASE * 3, TAILLE_CASE * 3)

    # Initialise l'interface
    cree_fenetre(longueurFenetre, hauteurFenetre)
    rectangle(0, 0, longueurFenetre, hauteurFenetre, COULEUR_BG, COULEUR_BG, tag="bg")
    interface.initialiser_interface()

    piece = Piece(queue.get_next_piece(), CASES_LONGUEUR, CASES_HAUTEUR, plateau)

    gravite = update_gravity(level)
    held_piece = None
    interface.affichage_plateau(plateau, piece)
    interface.update_affichage(score, line_clears, held_piece, 0)
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

        if pose_piece(plateau, piece) :
            if active :
                if t2 - tlockdelay1 >= LOCKDELAY :                   
                    # Actualise le plateau pour qu'il ait la pièce posée dedans
                    for l, c in piece.coord_cases :
                        plateau[l][c] = piece.nom_piece

                    # Rafraichis le score et le nombre de lignes remplies
                    line_clears_at_once = rafraichir_plateau(plateau)
                    score += get_score(level, line_clears_at_once)
                    line_clears += line_clears_at_once

                    # Rafraichis le niveau du jeu
                    if line_clears // (level * 10) > 0 :
                        level += 1
                        gravite = update_gravity(level)

                    # Change la pièce actuel et la prochaine pièce
                    piece = Piece(queue.get_next_piece(), CASES_LONGUEUR, CASES_HAUTEUR, plateau)

                    # Termine le jeu dans le cas où la pièce n'a pas pu se générer
                    if not piece.coord_cases :
                        break

                    active = False

            else :
                # Timer pour le lockdelay (voir Github)
                tlockdelay1 = time.perf_counter()
                active = True


        if tev == "Touche" :
            nom_touche = touche(ev)

            # Déplacement de la pièce dans une direction
            if nom_touche in ["Left", "Right", "Down"] :
                piece.deplacement(nom_touche)
                if nom_touche == "Down" :
                    score += SD_SCORE
            
            # Hard drop
            elif nom_touche == "Up" :

                # Donne le score correspondant au hard drop
                score += hard_drop(plateau, piece)

                # Rafraichis le score et le nombre de lignes remplies
                line_clears_at_once = rafraichir_plateau(plateau)
                score += get_score(level, line_clears_at_once)
                line_clears += line_clears_at_once

                # Rafraichis le niveau du jeu
                if line_clears // (level * 10) > 0 :
                    level += 1
                    gravite = update_gravity(level)

                # Change la pièce actuel et la prochaine pièce
                piece = Piece(queue.get_next_piece(), CASES_LONGUEUR, CASES_HAUTEUR, plateau)

                # Termine le jeu dans le cas où la pièce n'a pas pu se générer
                if not piece.coord_cases :
                    break

                active = False

            # Rotation de la pièce actuelle
            elif nom_touche in ["a", "e"] :
                if nom_touche == "a" :
                    piece.rotation_SRS("AntiClockwise")
                else :
                    piece.rotation_SRS("Clockwise")

            # Hold
            elif nom_touche == "space" :
                active = False

                # Échange des noms des pièces
                held_piece, piece = piece.nom_piece, held_piece

                if piece == None :
                    piece = queue.get_next_piece()

                piece = Piece(piece, CASES_LONGUEUR, CASES_HAUTEUR, plateau)



        elif tev == "Quitte" :
            break

        # Rafraichis l'interface avec les nouvelles données
        interface.affichage_plateau(plateau, piece)
        interface.update_affichage(score, line_clears, held_piece, fps)
        mise_a_jour()


    ferme_fenetre()