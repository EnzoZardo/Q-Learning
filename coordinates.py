from result import *
from vector2 import Vector2

class Coordinates:
    def __init__(self, limit: int) -> None:
        self.limit: int = limit;
        pass;

    def input(self) -> Result:
        c: list[str] = list(input('> ').replace(' ', '').split(','));

        if len(c) != 2:
            return Error('Número incorreto de coordenadas passadas.');

        r: list[str] = [str(x) for x in range(self.limit)];
        if c[0] not in r or c[1] not in r:
            return Result(False, message = 'Coordenadas inválidas.');
        
        coords: list[int] = list(map(lambda x: int(x), c));
        return Success(Vector2(coords[0], coords[1]));