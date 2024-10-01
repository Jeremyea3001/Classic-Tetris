class Coordinates :

    def __init__(self, x: int, y: int) -> None :
        self.x = x
        self.y = y

    def translateX(self, positive: bool) -> None :
        self.x += 1 if positive else -1
    
    def translateY(self, positive: bool) -> None :
        self.y += 1 if positive else -1