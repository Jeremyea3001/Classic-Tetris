from rotation import rotation

class Piece :
    """Une instance d'une pièce dans un plateau de jeu
    """

    def __init__(self, nom_piece: str, cases_longueur: int, cases_hauteur: int, plateau: list[list[None | str]]):
        """Initialisation de la pièce

        :param str nom_piece: Le nom de la pièce ("I", "T", "L", "J", "S", "Z", "O")
        :param int cases_longueur: Le nombre de cases en longueur du plateau
        :param int cases_hauteur: Le nombre de cases en hauteur du plateau
        :param list[list[None | str]] plateau: Le plateau de jeu
        :raises Exception: Si couleur_bg est différent de "white" ou "black"
        """

        if nom_piece not in ["I", "T", "L", "J", "S", "Z", "O"] :
            raise Exception("The piece name is invalid")
        
        self.nom_piece = nom_piece
        self.cases_longueur = cases_longueur
        self.cases_hauteur = cases_hauteur
        self.plateau = plateau

        self.coord_cases = self.__nouvelle_piece(self.nom_piece)
        # Coordonnées des cases de la pièce

        self.etat = 0
        # Etat de la pièce (orientation)


    def __nouvelle_piece(self, piece: str) -> list | bool :
        """Crée une liste de couples, si possible avec l'état du plateau actuel

        :param str piece: le nom de la pièce ("I", "T", "L", "J", "S", "Z", "O")
        :return list | bool: Renvoie une liste de 4 couples de coordonnées s'il n'y a pas d'obstacles et False si cette opération a échoué
        """

        lst = []

        if piece == "I" :
            for i in range(-2, 2) :
                if self.plateau[0][i + self.cases_longueur // 2] != None :
                    return False
                lst.append([0, i + self.cases_longueur // 2])
        

        elif piece == "O" :
            for i in range(2) :
                for j in range(-1, 1) :
                    if self.plateau[i][self.cases_longueur // 2 + j] != None :
                        return False
                    lst.append([i, j + self.cases_longueur // 2])


        elif piece in ["T", "L", "J"] :
            for i in range(-1, 2) :
                if ((piece == "L" and i == 1)
                or  (piece == "T" and i == 0)
                or  (piece == "J" and i == -1)) :
                    for j in range(2) :
                        if self.plateau[j][self.cases_longueur // 2 + i] != None :
                            return False
                        lst.append([j, i + self.cases_longueur // 2])

                else :
                    if self.plateau[1][self.cases_longueur // 2 + i] != None :
                        return False
                    lst.append([1, i + self.cases_longueur // 2])
                

        else :
            for i in range(-1, 2) :
                if ((i == -1 and piece == "S")
                or  (i == 1 and piece == "Z")) :
                    if self.plateau[1][self.cases_longueur // 2 + i] != None :
                        return False
                    lst.append([1, i + self.cases_longueur // 2])

                elif i == 0 :
                    for j in range(2) :
                        if self.plateau[j][i] != None :
                            return False
                        lst.append([j, i + self.cases_longueur // 2])
                
                else :
                    if self.plateau[0][i + self.cases_longueur // 2] != None :
                        return False
                    lst.append([0, i + self.cases_longueur // 2])
        
        return lst

    
    def rotation(self, dir: str) :
        """Modifie les coordonnées de piece avec la rotation normale dir s'il n'y a aucun obstacles.

        :param str dir: La direction de la rotation ("Clockwise", ou "AntiClockwise")
        """

        if self.nom_piece == "O" :      # Si la pièce est le O, ne pas faire de rotation
            return None

        lst = rotation(self.coord_cases, self.nom_piece, dir)
        # Algorithme pour appliquer une rotation dans un sens

        if all(0 <= e[1] <= self.cases_longueur - 1 and 0 <= e[0] <= self.cases_hauteur - 1 for e in lst) :
        # Si une coordonnée n'est pas dans la matrice, ne pas exécuter la prochaine condition
            
            if all(self.plateau[i][j] is None for i, j in lst) :
            # Si un couple coordonnées a un obstacle dans le plateau, ne pas changer les coordonnées de la pièce
                self.coord_cases = lst


    def rotation_SRS(self, dir: str) :
        """Modifie les coordonnées de piece avec la rotation SRS dans la direction dir.

        :param str dir: La direction de la rotation ("Clockwise", ou "AntiClockwise")
        """

        if self.nom_piece == "O" :      # Même condition que pour rotation
            return None

        tests = [(0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)]
        # Liste de tests, pour savoir si une de ces positions sont possibles
        # Pour plus d'informations sur ces tests, voir Github

        # En fonction de l'état de la pièce et de la direction de la rotation, le signe des tests diffèrent
        if self.etat == 0 :
            if dir == "Clockwise" :
                y = 1
            else :
                y = -1
            x = 1
        elif self.etat == 1 :
            y = -1
            x = -1
        elif self.etat == 2 :
            if dir == "Clockwise" :
                y = -1
            else :
                y = 1
            x = 1
        elif self.etat == 3 :
            y = 1
            x = -1


        lst = rotation(self.coord_cases, self.nom_piece, dir)
        # Même algorithme utilisé que dans la précédente méthode

        for test in tests :
            if all(0 <= e[1] + test[1] * y <= self.cases_longueur - 1 and 0 <= e[0] + test[0] * x <= self.cases_hauteur - 1 for e in lst) :
                if all(self.plateau[e[0] + test[0] * x][e[1] + test[1] * y] is None for e in lst) :
                # Mêmes tests que la précédente méthode
                    
                    for e in lst :
                        e[0] += test[0] * x
                        e[1] += test[1] * y
                    # Modification des coordonnées dans lst
                        
                    self.coord_cases = lst

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

                    break


    def deplacement(self, dir: str) :
        """Effectue le déplacement dans la direction indiquée.

        :param str dir: La direction du déplacement ("Left", "Right", ou "Down")
        """
        if all(e[1] > 0 for e in self.coord_cases) and dir == "Left" :
        # Si une coordonnée est déjà à l'extrémité et que le déplacement est vers la gauche,
        # Ne pas effectuer le déplacement
            
            if all(self.plateau[e[0]][e[1] - 1] is None for e in self.coord_cases) :
            # S'il y a un obstacle aux coordonnées après le déplacement,
            # Ne pas effectuer le déplacement

                for e in self.coord_cases :
                    e[1] -= 1

        elif all(e[1] < self.cases_longueur - 1 for e in self.coord_cases) and dir == "Right" :
        # Idem que pour le premier bloc
            
            if all(self.plateau[e[0]][e[1] + 1] is None for e in self.coord_cases) :

                for e in self.coord_cases :
                    e[1] += 1

        elif all(e[0] < self.cases_hauteur - 1 for e in self.coord_cases) and dir == "Down" :
        # Idem que pour les 2 premiers blocs
            
            if all(self.plateau[e[0] + 1][e[1]] is None or [e[0] + 1, e[1]] in self.coord_cases for e in self.coord_cases) :
            
                for e in self.coord_cases :
                    e[0] += 1