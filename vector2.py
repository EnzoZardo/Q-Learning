class Vector2:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x;
        self.y = y;
    
    def from_str(self, str_tuple: str):
        t: str = str_tuple.replace('(', '').replace(')', '').replace(' ', '');
        coords: list[int] = list(map(lambda x: int(x), t.split(',')));
        return Vector2(coords[0], coords[1]);

    def stringfy(self) -> str: return str((self.x, self.y));

    def tuplefy(self) -> tuple[int, int]: return (self.x, self.y);