

import random
import constants
from board import Board
from vector2 import Vector2

class QLearning:
    def __init__(self,
            board: Board,
            player: int = constants.o,
            max_episodes: int = 20_000,
            learning_rate: float = 0.3,
            discount_factor: float = 0.9,
            epsilon_greedy: float = 1.0,
            epsilon_min: float = 0.05,
            epsilon_decay: float = 0.9995) -> None:
        self.board = board;
        self.player: int = player;
        self.max_episodes: int = max_episodes;
        self.epsilon_min: float = epsilon_min;
        self.learning_rate: float = learning_rate;
        self.epsilon_decay: float = epsilon_decay;
        self.epsilon_greedy: float = epsilon_greedy;
        self.discount_factor: float = discount_factor;
        self.init_states();    
        self.init_counts();
        self.init_actions();
        self.init_q_values();
    
    '''
    Testa se não chegamos no final ainda.
    '''
    def proceed(self) -> bool: return self.count < self.max_episodes;

    '''
    q_values é um dicionário cuja chave é um estado do campo do nosso jogo da velha,
    algo como ((0,0,0),(0,0,0),(0,0,0)) em seu estado inicial.
    O valor de q_values é outro dicionário contendo uma tupla de coordenadas como
    cada chave, algo como (x, y) e a sua 'taxa de ganho' como valor, ou seja, quanto
    maior, melhor.
    '''
    def init_q_values(self) -> None: self.q_values: dict[str, dict[str, float]] = dict();

    '''
    Só inicializa as coisas zeradas.
    '''
    def init_actions(self) -> None:
        self.max_action: tuple[str, float] = ('', 0.0);
        self.max_value: float = 0.0;
        self.action: Vector2 = Vector2(0, 0);

    '''
    Só inicializa os estados de um campo vazio.
    '''
    def init_states(self) -> None:
        self.last_state: str = self.board.snapshot();
        self.new_state: str = self.board.snapshot();
    
    '''
    Inicializa as contagens zeradas.
    '''
    def init_counts(self) -> None:
        self.count: int = 0;
        self.win_count: int = 0;
        self.loss_count: int = 0;
        self.stalemate_count: int = 0;
    
    '''
    Faz uma escolha dentre nossas opções possíveis para o nosso board.
    '''
    def choose(self) -> Vector2:
        '''
        Caso random seja menor do que a nossa 'taxa de aleatoriedade',
        fazemos uma esolha aleatória sem levar em conta o aprendizado 
        anterior.
        '''
        if random.random() < self.epsilon_greedy:
            self.action = random.choice(self.board.get_empty());
            return self.action;

        '''
        Busca no nosso aprendizado (q_values) a coordenada que possamos jogar onde
        tenhamos a maior taxa de acertividade, buscando pelo maior valor das nossas
        coordenadas.
        '''
        last_state_entries: list[tuple[str, float]] = list(self.q_values.get(self.last_state, {}).items());
        self.max_action = max(last_state_entries, key = lambda x: x[1]);
        '''
        Precisei transformar a chave do tipo string para Vector2, perdão
        '''
        self.action = Vector2().from_str(self.max_action[0]);
        self.max_value = self.max_action[1];
        return self.action;
    
    '''
    Vai preencher o estado informado com 0's caso não haja ainda
    nenhuma probabilidade para aquele campo.
    '''
    def ensure_state(self, state: str) -> None:
        if state not in self.q_values:
            self.q_values[state] = {};
        for y in range(self.board.size):
            for x in range(self.board.size):
                state_coords: str = Vector2(x, y).stringfy();
                if self.board.get(x, y) == constants.empty and state_coords not in self.q_values[state]:
                    self.q_values[state][state_coords] = 0.0;

    '''
    Preenche o estado atual pré-jogada.
    '''
    def fill_last_state(self) -> None:
        self.last_state = self.board.snapshot();
        self.ensure_state(self.last_state);
    
    '''
    Preenche o novo estado pós-jogada.
    '''
    def fill_new_state(self) -> None:
        self.new_state = self.board.snapshot();
        self.ensure_state(self.new_state);
    
    '''
    Vai preencher o estado atual pré-jogada
    (esse método só existe pra uma melhor divisão de responsabilidades)
    '''
    def before(self) -> None: self.fill_last_state();

    '''
    Executa a ccontabilização de uma jogada intermediaria, ou seja:
    - Ela não foi a jogada vitoriosa nem a perdedora e nem final;
    - Foi apenas mais uma jogada no meio do jogo;
    '''
    def after(self) -> None:
        self.fill_new_state();

        '''
        Como ele ainda não chegou no final, sua recompensa é negativa.
        '''
        reward: float = -0.005;
        actions_dict: dict[str, float] = self.q_values.get(self.new_state, {});

        if len(actions_dict) == 0:
            '''
            Se ainda não tem nada nessa posição, seu valor máximo é 0.
            '''
            self.max_value = 0.0;
        else:
            '''
            Se ele já possui esse valor conhecido no dicionário,
            atribuimos para ele o seu maior valor conhecido.
            '''            
            new_state_entries = list(actions_dict.items());
            best = max(new_state_entries, key=lambda x: x[1]);
            self.max_value = best[1];

        '''
        Adicionamos ao nosso dicionário de jogadas conhecidas
        a pontuação desta jogada com base na sua recompensa e seu valor.
        '''
        action_key: str = self.action.stringfy();
        val: float = self.q_values[self.last_state][action_key];
        self.q_values[self.last_state][action_key] = (
            val + self.learning_rate * (reward + self.discount_factor * self.max_value - val)
        );

    '''
    Contabiliza uma vitória/derrota/empate após finalização
    do jogo.
    '''
    def contabilize(self, winner: int) -> None:
        reward: float = 0.5;
        match winner:
            case constants.empty: 
                self.stalemate_count += 1;
            case self.player: 
                reward = 1;
                self.win_count += 1;
            case _: 
                reward = -1;
                self.loss_count += 1;
        
        val: float = self.q_values[self.last_state][self.action.stringfy()];
        self.q_values[self.last_state][self.action.stringfy()] = val + self.learning_rate * (reward - val);
        self.count += 1;

        '''
        A cada nova partida, nossa possibilidade de fazer uma 
        nova tentativa aleatória diminui.
        '''
        if self.epsilon_greedy > self.epsilon_min:
            self.epsilon_greedy *= self.epsilon_decay;