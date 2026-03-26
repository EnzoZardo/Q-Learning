import random

from board import Board
import constants
from coordinates import Coordinates
from result import Error, Result
from trainer import QLearning
from vector2 import Vector2

# TODO: tem muitos jeitos melhores e mais performáticos de fazer isso, pensar depois

class Game: 
    def __init__(self):
        self.board: Board = Board();
        self.q_learn: QLearning = QLearning(
            self.board,
            player = constants.o,
            max_episodes = 50_000,
            learning_rate = 0.1,
            discount_factor = 0.95,
            epsilon_greedy = 1.0,
        );
        self.player: int = constants.empty;

    def play_after_training(self) -> None:
        print('>> Aguarde o treinamento da IA...\n>> Ela vai jogar', self.q_learn.max_episodes, 'partidas em pouco tempinho...');
        self.train();
        print('-' * 20);
        print('>> Você estará jogando com um agente que\n>> venceu', self.q_learn.win_count, 'partidas em', self.q_learn.count);
        print('-' * 20);
        player: int = constants.empty;
        coordinates: Coordinates = Coordinates(self.board.size);
        while not self.board.has_victory() and not self.board.has_stalemate():
            self.board.print()
            player = constants.x;
            played_result: Result = Error('');
            while played_result.failure:
                if played_result.message: print(played_result.message);
                coord_result: Result = Error('');
                while coord_result.failure:
                    if coord_result.message: print(coord_result.message);
                    coord_result = coordinates.input();
                    if coord_result.failure: continue;
                    coord: Vector2 = coord_result.value; # type: ignore
                    played_result = self.board.place(coord, player);
            
            if self.board.has_victory() or self.board.has_stalemate():
                break;
            
            player = constants.o;
            self.q_learn.before();
            coord: Vector2 = self.q_learn.choose();
            self.board.place(coord, player);

            if self.board.has_victory() or self.board.has_stalemate():
                break;
            
            self.q_learn.after();
        
        if self.board.has_stalemate(): print('Você conseguiu um empate!');
        elif self.board.has_victory(): print('O jogador', constants.map[player], 'ganhou!');
    
    def train(self):
        player: int = constants.empty;
        while self.q_learn.proceed():
            while not self.board.has_victory() and not self.board.has_stalemate():
                # X realiza sua jogada
                player = constants.x;
                self.board.place(random.choice(self.board.get_empty()), player);

                if self.board.has_victory() or self.board.has_stalemate():
                    break;

                # O realiza sua jogada
                player = constants.o;
                self.q_learn.before();
                coord: Vector2 = self.q_learn.choose();
                self.board.place(coord, player);

                if self.board.has_victory() or self.board.has_stalemate():
                    break;
                
                self.q_learn.after();
            
            if self.board.has_stalemate(): self.q_learn.contabilize(constants.empty);
            elif self.board.has_victory(): self.q_learn.contabilize(player);
            
            self.board.reset();