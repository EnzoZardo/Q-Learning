import constants
from result import *
from vector2 import Vector2;

class Board:
    def __init__(self) -> None:
        self.size: int = 3;
        self.board: list[list[int]] = self.init_board();

    def reset(self) -> None: self.board = self.init_board();

    def init_board(self) -> list[list[int]]: return [[constants.empty for _ in range(self.size)] for _ in range(self.size)];

    def is_filled(self, vec: Vector2) -> bool: return self.board[vec.y][vec.x] != constants.empty;

    def snapshot(self) -> str: return str(tuple(tuple(row) for row in self.board));

    def get(self, x: int, y: int) -> int | None: return self.board[y][x];

    def print(self) -> None:
        print('+---+---+---+');
        for row in self.board:
            for cell in row:
                print('|', constants.map[cell], end=' ');
            print('|');
            print('+---+---+---+');

    def place(self, vec: Vector2, element: int) -> Result:
        if self.is_filled(vec): 
            return Error('Ocupada.');
    
        if list(constants.map.keys()).count(element) == 0:
            return Error('Opção inválida.')

        self.board[vec.y][vec.x] = element;
        return Success();

    def get_empty(self) -> list[Vector2]:
        empty: list[Vector2] = [];
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == constants.empty: 
                    empty.append(Vector2(x, y));
        return empty;

    def has_victory(self) -> bool:
        def column(i: int) -> bool:
            return (self.is_filled(Vector2(i, 0)) 
                    and self.board[0][i] == self.board[1][i] 
                    and self.board[1][i] == self.board[2][i]);

        def row(i: int) -> bool: 
            return (self.is_filled(Vector2(0, i)) 
                    and self.board[i][0] == self.board[i][1] 
                    and self.board[i][1] == self.board[i][2]);

        def diagonal_top_bottom() -> bool:
            return (self.is_filled(Vector2(0, 0)) 
                    and self.board[0][0] == self.board[1][1] 
                    and self.board[1][1] == self.board[2][2]);

        def diagonal_bottom_top() -> bool:
            return (self.is_filled(Vector2(2, 0)) 
                    and self.board[2][0] == self.board[1][1] 
                    and self.board[1][1] == self.board[0][2]);

        return (column(0) or column(1) or column(2) or
                row(0) or row(1) or row(2) or 
                diagonal_bottom_top() or diagonal_top_bottom());
        
    def has_stalemate(self) -> bool:
        if self.has_victory(): return False;
        for row in self.board: 
            if row.count(constants.empty) > 0: 
                return False;
        return True;