from game.deck import GameDeck
from game.enemies import EasyEnemy, Difficulties
from game.errors import assertion, ArgumentCodes, ArgumentError


def create_enemy(difficulty: Difficulties, player_count: int, game_deck: GameDeck, cards: int = 4, pid: int = 0):
    assertion.assert_type(difficulty, Difficulties, ArgumentError, code=ArgumentCodes.NOT_ENUM)
    if difficulty == Difficulties.EASY:
        return EasyEnemy(player_count, game_deck, cards, pid)

