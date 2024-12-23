from abc import ABCMeta, abstractmethod
from typing import List, Any


GameState = Any
GameAction = Any

class Game(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._state: GameState = None
        self._actions: List[GameAction] = []

    @abstractmethod
    def set_state(self, state: GameState) -> None:
        """ Set the game to a given state """
        self._state = state

    @abstractmethod
    def get_state(self) -> GameState:
        """ Get the complete, unmasked game state """
        return self._state

    @abstractmethod
    def print_state(self) -> None:
        """ Print the current game state """
        print(self._state)

    @abstractmethod
    def get_list_action(self) -> List[GameAction]:
        """ Get a list of possible actions for the active player """
        return self._actions

    @abstractmethod
    def apply_action(self, action: GameAction) -> None:
        """ Apply the given action to the game """
        pass

    @abstractmethod
    def get_player_view(self, idx_player: int) -> GameState:
        """ Get the masked state for the active player (e.g. the opponent's cards are face down)"""
        pass


class Player(metaclass=ABCMeta):

    @abstractmethod
    def select_action(self, state: GameState, actions: List[GameAction]) -> GameAction:
        """ Given masked game state and possible actions, select the next action """
        pass
