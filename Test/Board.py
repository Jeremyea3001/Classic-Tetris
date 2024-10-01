from Main import Piece

class Board :

    def __init__(self, width: int = 10, height: int = 20) -> None:
        self.width = width
        self.height = height
        self.board = [[None for _ in range(width)] for __ in range(height)]

    def add_piece(self, piece: Piece) -> bool :
        