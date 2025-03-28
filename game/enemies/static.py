from torch import optim

from game.deck import GameDeck, PlayerDeck
from game.enemies import EasyEnemy, Difficulties, PolicyNN
from game.errors import assertion, ArgumentCodes, ArgumentError


def create_enemy(difficulty: Difficulties, player_count: int, game_deck: GameDeck, cards: int = 4, pid: int = 0):
    assertion.assert_type(difficulty, Difficulties, ArgumentError, code=ArgumentCodes.NOT_ENUM)
    if difficulty == Difficulties.EASY:
        return EasyEnemy(player_count, game_deck, cards, pid)


def train(episodes: int = 100, cards: int = 4, players: int = 4):
    temp_en = create_enemy(Difficulties.EASY, players, GameDeck(), cards)
    PolNN: PolicyNN = PolicyNN(temp_en.get_input_dim(), temp_en.get_actions_per_phase())
    del temp_en
    optimizer = optim.Adam(PolNN.parameters(), lr=0.001)
    gamma = 0.99