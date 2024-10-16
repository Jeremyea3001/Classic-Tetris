from fltk import rectangle, texte, efface, ligne
from piece import Piece
from piece_queue import Piece_Queue
import math

class Interface() :
    """La classe comportant tous les éléments liés à l'interface du jeu
    """

    COULEURS = ["pink", "#00CCFF", "yellow", "lime", "red", "orange", "dark blue"]
            #     T   ,     I    ,    O    ,   S   ,   Z  ,     L   ,      J
            # Liste des couleurs des pièces avec leur pièce respective en dessous

    def __init__(self, taille_case: int, cases_longueur: int, cases_hauteur: int, couleur_bg: str, piece_queue: Piece_Queue, anchrage: str = "nw", offsetX: int = 0, offsetY: int = 0) -> None:
        """Initialisation de l'interface

        :param int taille_case: La taille d'une case en pixel
        :param int cases_longueur: La quantité de cases en longueur (x)
        :param int cases_hauteur: La quantité de cases en hauteur (y)
        :param str couleur_bg: La couleur du fond d'écran
        :param str anchrage: 
        :param int offsetX: La position de la zone de jeu d'un joueur par rapport au coin supérieur gauche de la fenêtre (en x)
        :param int offsetY: la position de la zone de jeu d'un joueur par rapport au coin supérieur droite de la fenêtre (en y)
        :raises Exception: Si offsetX ou offsetY est négatif
        :raises Exception: Si couleur_bg est différent de "white" ou "black"
        """

        if anchrage not in ["ne", "nw", "se", "sw", "center"] :
            raise Exception("L'orientation doit avoir la valeur ne, nw, se ou sw")

        if offsetX < 0 or offsetY < 0 :
            raise Exception("L'offset ne peut pas être négatif")

        if not (couleur_bg == "white" or couleur_bg == "black") :
            raise Exception("The background color has to be either white or black")
        
        self.longueurFenetreJoueur = taille_case * cases_longueur + taille_case * 10
        self.hauteurFenetreJoueur = taille_case * cases_hauteur

        self.taille_case = taille_case
        self.cases_longueur = cases_longueur
        self.cases_hauteur = cases_hauteur

        self.COULEUR_BG = couleur_bg
        self.COULEUR_INVERSE_BG = "black" if self.COULEUR_BG == "white" else "white"

        self.piece_queue = piece_queue

        self.offsetX = offsetX
        self.offsetY = offsetY

        match anchrage :
            case "nw" :
                self.offsetX -= -self.longueurFenetreJoueur
            case "se" :
                self.offsetY -= -self.hauteurFenetreJoueur
            case "sw" :
                self.offsetX -= self.longueurFenetreJoueur
                self.offsetY -= self.hauteurFenetreJoueur
            case "center" :
                self.offsetX -= self.longueurFenetreJoueur / 2
                self.offsetY -= self.hauteurFenetreJoueur / 2


    def initialiser_interface(self) -> None :
        """Initialise tous les graphismes statiques
        """

        # Encadré SCORE et le texte
        rectangle(self.offsetX, 
                self.hauteurFenetreJoueur - self.taille_case * 4 + self.offsetY, 
                self.taille_case * 5 + self.offsetX, 
                self.hauteurFenetreJoueur + self.offsetY, 
                self.COULEUR_INVERSE_BG, 
                epaisseur=2, 
                tag="encadre"
                )
        texte(2.5 * self.taille_case + self.offsetX, self.hauteurFenetreJoueur - 14/5 * self.taille_case + self.offsetY, "SCORE", self.COULEUR_INVERSE_BG, "center", taille=int(6*self.taille_case/10), tag="SCORE")

        # Encadré NEXT et le texte
        taille_queue = len(self.piece_queue.get_piece_queue())
        rectangle(self.longueurFenetreJoueur - self.taille_case * 5 + self.offsetX, 
                self.offsetY, 
                self.longueurFenetreJoueur + self.offsetX, 
                self.taille_case * (3 * taille_queue + 1) + self.offsetY, 
                self.COULEUR_INVERSE_BG, 
                epaisseur=2, 
                tag="encadre"
                )
        texte(self.longueurFenetreJoueur - 2.5 * self.taille_case + self.offsetX, 4/5 * self.taille_case + self.offsetY, "NEXT", self.COULEUR_INVERSE_BG, "center", taille=int(6*self.taille_case/10), tag="NEXT")

        # Encadré HOLD et le texte
        rectangle(self.offsetX, 
                self.offsetY, 
                self.taille_case * 5 + self.offsetX, 
                self.taille_case * 4 + self.offsetY, 
                self.COULEUR_INVERSE_BG, 
                epaisseur=2, 
                tag="encadre"
                )
        texte(2.5 * self.taille_case + self.offsetX, 4/5 * self.taille_case + self.offsetY, "HOLD", self.COULEUR_INVERSE_BG, "center", taille=int(6*self.taille_case/10), tag="HOLD")

        # Texte lignes remplis
        texte(2.5 * self.taille_case + self.offsetX, self.hauteurFenetreJoueur - 33/5 * self.taille_case + self.offsetY, "Lines cleared :", self.COULEUR_INVERSE_BG, "center", taille=int(6*self.taille_case/10) - 6 if int(6*self.taille_case/10) - 6 > 0 else 1, tag="LIGNES")
            
        # Bordures de la zone de jeu
        for i in range(5, self.cases_longueur + 6) :
            ligne(i * self.taille_case + self.offsetX, self.offsetY, i * self.taille_case + self.offsetX, self.hauteurFenetreJoueur + self.offsetY, self.COULEUR_INVERSE_BG, tag="bordure")
        for i in range(self.cases_hauteur + 1) :
            ligne(self.offsetX + self.taille_case * 5, i * self.taille_case + self.offsetY, self.taille_case * (5 + self.cases_longueur) + self.offsetX, i * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, tag="bordure")


    def remplir_case(self, i: int, j: int, piece: str) -> None :
        """Colorie la case plateau[i][j] avec la couleur de la pièce correspondante

        :param int i: L'emplacement de la case en y
        :param int j: L'emplacement de la case en x
        :param str piece: Le nom de la pièce actuelle
        """
        match piece :
            case "T" :
                couleur = self.COULEURS[0]
            case "I" :
                couleur = self.COULEURS[1]
            case "O" :
                couleur = self.COULEURS[2]
            case "S" :
                couleur = self.COULEURS[3]
            case "Z" :
                couleur = self.COULEURS[4]
            case "L" :
                couleur = self.COULEURS[5]
            case "J" :
                couleur = self.COULEURS[6]

        xOrig, yOrig = (j + 5) * self.taille_case + self.offsetX, i * self.taille_case + self.offsetY
        xFin, yFin = (j + 6) * self.taille_case + self.offsetX, (i + 1) * self.taille_case + self.offsetY
        rectangle(xOrig, yOrig, xFin, yFin, self.COULEUR_INVERSE_BG, couleur, tag="piece")


    def affichage_plateau(self, plateau: list, piece: Piece) -> None :
        """Rafraichis l'affichage du plateau

        :param list plateau: Le plateau de jeu
        :param Piece piece: La pièce en jeu
        """
        efface("piece")
        for l, c in piece.coord_cases :
            self.remplir_case(l, c, piece.nom_piece)
        for i in range(len(plateau)) :
            for j in range(len(plateau[0])) :
                if plateau[i][j] != None :
                    self.remplir_case(i, j, plateau[i][j])


    def update_affichage(self, score: int, lines: int, held_piece: str, fps: int) -> None :
        """Rafraichis l'affichage du score, des lignes, de la pièce suivante et des fps

        :param int score: Le nouveau score
        :param int lines: La nouvelle quantité de lignes remplies
        :param str piece: Le nom de la pièce actuelle
        :param list[str] held_piece: La liste des pièces suivantes
        :param int fps: La quantité de fps à cette frame
        """
        efface("next")
        efface("score")
        efface("lines")
        efface("hold")
        efface("fps")

        piece_queue = list(reversed(self.piece_queue.get_piece_queue()))
        # Rafraichissage de la prochaine pièce
        for k in range(len(piece_queue)) :
            piece = piece_queue[k]
            k *= 2.8
            if piece == "I" :
                for j in range(15, 19) :
                    rectangle((j + 0.5) * self.taille_case + self.offsetX, (2.5 + k) * self.taille_case + self.offsetY, (j + 1.5) * self.taille_case + self.offsetX, (3.5 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[1], tag="next")

            elif piece == "O":
                for j in range(16, 18) :
                    for i in range(1, 3) :
                            rectangle((j + 0.5) * self.taille_case + self.offsetX, (i + 1 + k) * self.taille_case + self.offsetY, (j + 1.5) * self.taille_case + self.offsetX, (i + 2 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[2], tag="next")

            else :
                for j in range(16, 19) :
                    if piece == "T" :
                        rectangle(j * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (4 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[0], tag="next")
                        if j == 17 :
                            rectangle(j * self.taille_case + self.offsetX, (2 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[0], tag="next")
                    
                    elif piece == "S" :
                        if j <= 17 :
                            rectangle(j * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (4 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[3], tag="next")
                        if j >= 17 :
                            rectangle(j * self.taille_case + self.offsetX, (2 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[3], tag="next")
                    
                    elif piece == "Z" :
                        if j <= 17 :
                            rectangle(j * self.taille_case + self.offsetX, (2 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[4], tag="next")
                        if j >= 17 :
                            rectangle(j * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (4 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[4], tag="next")
                    
                    elif piece == "L" :
                        rectangle(j * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (4 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[5], tag="next")
                        if j == 18 :
                            rectangle(j * self.taille_case + self.offsetX, (2 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[5], tag="next")
                    
                    elif piece == "J" :
                        rectangle(j * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (4 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[6], tag="next")
                        if j == 16 :
                            rectangle(j * self.taille_case + self.offsetX, (2 + k) * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, (3 + k) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[6], tag="next")

        # Rafraichissage du score
        xScore, yScore = 2.5 * self.taille_case + self.offsetX, self.hauteurFenetreJoueur - 7/5 * self.taille_case + self.offsetY
        if score > 0 :
            nb_zeros = 7 - round((math.log10(score))) if 7 - round((math.log10(score))) >= 0 else 0
            texte(xScore, yScore, "0" * nb_zeros + str(round(score)), self.COULEUR_INVERSE_BG, "center", taille=int(6 * self.taille_case / 10) + 6, tag="score")
        else :
            texte(xScore, yScore, "00000000", self.COULEUR_INVERSE_BG, "center", taille=int(6 * self.taille_case / 10) + 6, tag="score")

        # Rafraichissage des lignes remplies
        xLignes, yLignes = 2.5 * self.taille_case + self.offsetX, self.hauteurFenetreJoueur - 26/5 * self.taille_case + self.offsetY
        texte(xLignes, yLignes, str(lines), self.COULEUR_INVERSE_BG, "center", taille=int(6 * self.taille_case / 10) + 6, tag="lines")

        # Rafraichissage du hold
        if held_piece == "I" :
            for j in range(4) :
                rectangle((j + 0.5) * self.taille_case + self.offsetX, 2 * self.taille_case + self.offsetY, (j + 1.5) * self.taille_case + self.offsetX, 3 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[1], tag="hold")

        elif held_piece == "O":
            for j in range(1, 3) :
                for i in range(1, 3) :
                        rectangle((j + 0.5) * self.taille_case + self.offsetX, (i + 0.5) * self.taille_case + self.offsetY, (j + 1.5) * self.taille_case + self.offsetX, (i + 1.5) * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[2], tag="hold")

        else :
            for j in range(1, 4) :
                if held_piece == "T" :
                    rectangle(j * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 3.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[0], tag="hold")
                    if j == 2 :
                        rectangle(j * self.taille_case + self.offsetX, 1.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[0], tag="hold")
                
                elif held_piece == "S" :
                    if j <= 2 :
                        rectangle(j * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 3.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[3], tag="hold")
                    if j >= 2 :
                        rectangle(j * self.taille_case + self.offsetX, 1.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[3], tag="hold")
                
                elif held_piece == "Z" :
                    if j <= 2 :
                        rectangle(j * self.taille_case + self.offsetX, 1.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[4], tag="hold")
                    if j >= 2 :
                        rectangle(j * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 3.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[4], tag="hold")
                
                elif held_piece == "L" :
                    rectangle(j * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 3.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[5], tag="hold")
                    if j == 3 :
                        rectangle(j * self.taille_case + self.offsetX, 1.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[5], tag="hold")
                
                elif held_piece == "J" :
                    rectangle(j * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 3.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[6], tag="hold")
                    if j == 1 :
                        rectangle(j * self.taille_case + self.offsetX, 1.5 * self.taille_case + self.offsetY, (j + 1) * self.taille_case + self.offsetX, 2.5 * self.taille_case + self.offsetY, self.COULEUR_INVERSE_BG, self.COULEURS[6], tag="hold")
        
        # Rafraichissage des FPS
        texte(self.longueurFenetreJoueur + self.offsetX, self.hauteurFenetreJoueur + self.offsetY, str(fps), self.COULEUR_INVERSE_BG, "se", taille=int(self.taille_case / 3), tag="fps")