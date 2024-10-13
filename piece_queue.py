from collections import deque
import random

class Piece_Queue :
    """La file d'attente pour les pièces suivantes
    """

    def __init__(self, queue_size: int, random_bag: bool) -> None:
        """Initialise une file d'attente pour les prochaines pièces

        :param int queue_size: La taille de la file d'attente
        :param bool random_bag: True n'utilise pas le système 7-bag (NES Tetris) tandis que False si (modern tetris)
        :raises Exception: Si queue_size est strictement inférieur à 1
        """

        if queue_size < 1 :
            raise Exception("The queue size cannot be lower than 1")

        self.SAC = ["I", "T", "L", "J", "S", "Z", "O"]
        # Les pièces dans un sac

        self.random_bag = random_bag
        self.piece_queue = deque()

        if not self.random_bag :
            self.sac_courant = list(self.SAC)

        for _ in range(queue_size) :
            self.piece_queue.appendleft(self.__choose_piece())

    
    def __choose_piece(self) -> str :
        """Chooses a piece according to the bag choice

        :return str: The name of the chosen piece
        """
        if self.random_bag :
            return random.choice(self.SAC)
        
        if len(self.sac_courant) == 1 :
            chosen_piece = self.sac_courant.pop()
            self.sac_courant = list(self.SAC)
            return chosen_piece

        chosen_piece = random.choice(self.sac_courant)
        self.sac_courant.remove(chosen_piece)
        return chosen_piece


    def get_piece_queue(self) -> list[str] :
        """Gives a list version of the piece queue read from end to start

        :return list[str]: The converted piece queue
        """
        return list(self.piece_queue)
    

    def get_next_piece(self) -> str :
        """Gives the next piece in queue

        :return str: The name of the piece
        """
        next_piece = self.piece_queue.pop()
        self.piece_queue.appendleft(self.__choose_piece())
        return next_piece