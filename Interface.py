from fltk import *
from Piece import Piece
import math

class Interface() :

    COULEURS = ["pink", "#00CCFF", "yellow", "lime", "red", "orange", "dark blue"]
            #     T   ,     I    ,    O    ,   S   ,   Z  ,     L   ,      J
            # Liste des couleurs des pièces avec leur pièce respective en dessous

    def __init__(self, longueurFenetre: float, hauteurFenetre: float, taille_case: int, cases_longueur: int, cases_hauteur: int, couleur_bg: str) -> None:
        """Initialisation de l'interface

        :param float longueurFenetre: La taille en pixel de la fenêtre en longueur (x)
        :param float hauteurFenetre: La taille en pixel de la fenêtre en hauteur (y)
        :param int taille_case: La taille d'une case en pixel
        :param int cases_longueur: La quantité de cases en longueur (x)
        :param int cases_hauteur: La quantité de cases en hauteur (y)
        :param str couleur_bg: La couleur du fond d'écran
        :raises Exception: Si couleur_bg est différent de "white" ou "black"
        """


        if not (couleur_bg == "white" or couleur_bg == "black") :
            raise Exception("The background color has to be either white or black")
        
        self.longueurFenetre = longueurFenetre
        self.hauteurFenetre = hauteurFenetre

        self.taille_case = taille_case
        self.cases_longueur = cases_longueur
        self.cases_hauteur = cases_hauteur

        self.COULEUR_BG = couleur_bg
        self.COULEUR_INVERSE_BG = "black" if self.COULEUR_BG == "white" else "white"


    def initialiser_interface(self) -> None :
        """Crée l'interface et initialise tous les graphismes statiques
        """

        cree_fenetre(self.longueurFenetre, self.hauteurFenetre)


        # Background
        rectangle(0, 0, self.longueurFenetre, self.hauteurFenetre, self.COULEUR_BG, self.COULEUR_BG, tag="bg")


        # Encadré SCORE et le texte
        rectangle(self.taille_case * self.cases_longueur * 1.1, 
                self.taille_case * 1, 
                self.taille_case * self.cases_longueur * 1.1 + self.taille_case * 5, 
                self.taille_case * 4, 
                self.COULEUR_INVERSE_BG, 
                epaisseur=2, 
                tag="encadre"
                )
        texte(13.5 * self.taille_case, 9/5 * self.taille_case, "SCORE", self.COULEUR_INVERSE_BG, "center", tag="SCORE")


        # Encadré NEXT et le texte
        rectangle(self.taille_case * self.cases_longueur * 1.1, 
                self.taille_case * 5, 
                self.taille_case * self.cases_longueur * 1.1 + self.taille_case * 5, 
                self.taille_case * 9, 
                self.COULEUR_INVERSE_BG, 
                epaisseur=2, 
                tag="encadre"
                )
        texte(13.5 * self.taille_case, 29/5 * self.taille_case, "NEXT", self.COULEUR_INVERSE_BG, "center", tag="NEXT")


        # Encadré HOLD et le texte
        rectangle(self.taille_case * self.cases_longueur * 1.1, 
                self.taille_case * 10, 
                self.taille_case * self.cases_longueur * 1.1 + self.taille_case * 5, 
                self.taille_case * 14, 
                self.COULEUR_INVERSE_BG, 
                epaisseur=2, 
                tag="encadre"
                )
        texte(13.5 * self.taille_case, 54/5 * self.taille_case, "HOLD", self.COULEUR_INVERSE_BG, "center", tag="NEXT")


        # Texte lignes remplis
        texte(13.5 * self.taille_case, self.hauteurFenetre - 13/5 * self.taille_case, "Lines cleared :", self.COULEUR_INVERSE_BG, "center", taille=18, tag="LIGNES")
            

        # Zone de jeu
        for i in range(self.cases_longueur + 1) :
            ligne(i * self.taille_case, 0, i * self.taille_case, self.hauteurFenetre, self.COULEUR_INVERSE_BG, tag="bordure")
        for i in range(self.cases_hauteur) :
            ligne(0, i *self. taille_case, self.longueurFenetre / 1.7, i * self.taille_case, self.COULEUR_INVERSE_BG, tag="bordure")


    def remplir_case(self, i: int, j: int, piece: str) -> None :
        """Colorie la case plateau[i][j] avec la couleur de la pièce correspondante

        :param int i: L'emplacement de la case en y
        :param int j: L'emplacement de la case en x
        :param str piece: Le nom de la pièce actuelle
        """
        if piece == "T" :
            couleur = self.COULEURS[0]
        elif piece == "I" :
            couleur = self.COULEURS[1]
        elif piece == "O" :
            couleur = self.COULEURS[2]
        elif piece == "S" :
            couleur = self.COULEURS[3]
        elif piece == "Z" :
            couleur = self.COULEURS[4]
        elif piece == "L" :
            couleur = self.COULEURS[5]
        elif piece == "J" :
            couleur = self.COULEURS[6]
        rectangle(j * self.taille_case, i * self.taille_case, (j + 1) * self.taille_case, (i + 1) * self.taille_case, self.COULEUR_INVERSE_BG, couleur, tag="piece")


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


    def update_affichage(self, score: int, lines: int, piece: str, held_piece: str, fps: int) -> None :
        """Rafraichis l'affichage du score, des lignes, de la pièce suivante et des fps

        :param int score: Le nouveau score
        :param int lines: La nouvelle quantité de lignes remplies
        :param str piece: Le nom de la pièce actuelle
        :param str held_piece: Le nom de la pièce suivante
        :param int fps: La quantité de fps à cette frame
        """
        efface("next")
        efface("score")
        efface("lines")
        efface("hold")
        efface("fps")

        # Rafraichissage de la prochaine pièce
        if piece == "I" :
            for j in range(11, 15) :
                rectangle((j + 0.5) * self.taille_case, 7 * self.taille_case, (j + 1.5) * self.taille_case, 8 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[1], tag="next")

        elif piece == "O":
            for j in range(12, 14) :
                for i in range(6, 8) :
                        rectangle((j + 0.5) * self.taille_case, (i + 0.5) * self.taille_case, (j + 1.5) * self.taille_case, (i + 1.5) * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[2], tag="next")

        else :
            for j in range(12, 15) :
                if piece == "T" :
                    rectangle(j * self.taille_case, 7.5 * self.taille_case, (j + 1) * self.taille_case, 8.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[0], tag="next")
                    if j == 13 :
                        rectangle(j * self.taille_case, 6.5 * self.taille_case, (j + 1) * self.taille_case, 7.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[0], tag="next")
                
                elif piece == "S" :
                    if j <= 13 :
                        rectangle(j * self.taille_case, 7.5 * self.taille_case, (j + 1) * self.taille_case, 8.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[3], tag="next")
                    if j >= 13 :
                        rectangle(j * self.taille_case, 6.5 * self.taille_case, (j + 1) * self.taille_case, 7.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[3], tag="next")
                
                elif piece == "Z" :
                    if j <= 13 :
                        rectangle(j * self.taille_case, 6.5 * self.taille_case, (j + 1) * self.taille_case, 7.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[4], tag="next")
                    if j >= 13 :
                        rectangle(j * self.taille_case, 7.5 * self.taille_case, (j + 1) * self.taille_case, 8.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[4], tag="next")
                
                elif piece == "L" :
                    rectangle(j * self.taille_case, 7.5 * self.taille_case, (j + 1) * self.taille_case, 8.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[5], tag="next")
                    if j == 14 :
                        rectangle(j * self.taille_case, 6.5 * self.taille_case, (j + 1) * self.taille_case, 7.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[5], tag="next")
                
                elif piece == "J" :
                    rectangle(j * self.taille_case, 7.5 * self.taille_case, (j + 1) * self.taille_case, 8.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[6], tag="next")
                    if j == 12 :
                        rectangle(j * self.taille_case, 6.5 * self.taille_case, (j + 1) * self.taille_case, 7.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[6], tag="next")

        # Rafraichissage du score
        if score > 0 :
            nb_zeros = 7 - round((math.log10(score))) if 7 - round((math.log10(score))) >= 0 else 0
            texte(13.5 * self.taille_case, 16/5 * self.taille_case, "0" * nb_zeros + str(round(score)), self.COULEUR_INVERSE_BG, "center", tag="score")
        else :
            texte(13.5 * self.taille_case, 16/5 * self.taille_case, "0000000", self.COULEUR_INVERSE_BG, "center", tag="score")

        # Rafraichissage des lignes remplies
        texte(13.5 * self.taille_case, self.hauteurFenetre - 7/5 * self.taille_case, str(lines), self.COULEUR_INVERSE_BG, "center", taille=18, tag="lines")

        # Rafraichissage du hold
        if held_piece == "I" :
            for j in range(11, 15) :
                rectangle((j + 0.5) * self.taille_case, 12 * self.taille_case, (j + 1.5) * self.taille_case, 13 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[1], tag="hold")

        elif held_piece == "O":
            for j in range(12, 14) :
                for i in range(11, 13) :
                        rectangle((j + 0.5) * self.taille_case, (i + 0.5) * self.taille_case, (j + 1.5) * self.taille_case, (i + 1.5) * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[2], tag="hold")

        else :
            for j in range(12, 15) :
                if held_piece == "T" :
                    rectangle(j * self.taille_case, 12.5 * self.taille_case, (j + 1) * self.taille_case, 13.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[0], tag="hold")
                    if j == 13 :
                        rectangle(j * self.taille_case, 11.5 * self.taille_case, (j + 1) * self.taille_case, 12.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[0], tag="hold")
                
                elif held_piece == "S" :
                    if j <= 13 :
                        rectangle(j * self.taille_case, 12.5 * self.taille_case, (j + 1) * self.taille_case, 13.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[3], tag="hold")
                    if j >= 13 :
                        rectangle(j * self.taille_case, 11.5 * self.taille_case, (j + 1) * self.taille_case, 12.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[3], tag="hold")
                
                elif held_piece == "Z" :
                    if j <= 13 :
                        rectangle(j * self.taille_case, 11.5 * self.taille_case, (j + 1) * self.taille_case, 12.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[4], tag="hold")
                    if j >= 13 :
                        rectangle(j * self.taille_case, 12.5 * self.taille_case, (j + 1) * self.taille_case, 13.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[4], tag="hold")
                
                elif held_piece == "L" :
                    rectangle(j * self.taille_case, 12.5 * self.taille_case, (j + 1) * self.taille_case, 13.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[5], tag="hold")
                    if j == 14 :
                        rectangle(j * self.taille_case, 11.5 * self.taille_case, (j + 1) * self.taille_case, 12.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[5], tag="hold")
                
                elif held_piece == "J" :
                    rectangle(j * self.taille_case, 12.5 * self.taille_case, (j + 1) * self.taille_case, 13.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[6], tag="hold")
                    if j == 12 :
                        rectangle(j * self.taille_case, 11.5 * self.taille_case, (j + 1) * self.taille_case, 12.5 * self.taille_case, self.COULEUR_INVERSE_BG, self.COULEURS[6], tag="hold")
        
        # Rafraichissage des FPS
        texte(self.longueurFenetre, self.hauteurFenetre, str(fps), self.COULEUR_INVERSE_BG, "se", taille=10, tag="fps")