# This is the test file for the whole dog.py file
# The test file should be in the test folder and called test_dog.py for benchmark_dog.py to find it

# Write your test functions in this file, that is clear and easy to understand what you are testing

# # OLD - NOT WORKING # Run with: python test/test_dog.py python dog.Dog
##################################################
# Run with: pytest -v test/test_dog.py
#Or simply run: pytest
##################################################

# For coverage, run with: coverage report -m # This will show the coverage of the test file over the whole dog.py file. The -m flag will show the missing lines in the report
'''missing lines:
1-102, 118-134, 154, 158-727, 731, 735, 738, 744, 762-836'''

from pydantic import BaseModel
from typing import List, Optional, Dict

from server.py.dog import Card, Marble, PlayerState, Action, GameState, GamePhase, Dog, RandomPlayer

import coverage
import pytest



class TestDogBenchmark:
    CNT_PLAYERS = 4
    CNT_STEPS = 64
    CNT_BALLS = 4

    def setup_method(self):
        self.game_server = Dog()

    # --- tests ---

    def test_Card_class(self):
        """Test 002: Validate Card class [1 points]"""
        card1 = Card(suit='hearts', rank='A')
        card2 = Card(suit='hearts', rank='K')        
        assert isinstance(card1, Card), f'{card1}Error: Card class must be defined'
       
        # test def __lt__(self, card: "Card") -> bool:
        assert card1 < card2, f'Expected True, got False'
        assert card1.__lt__(card2) == True, f'Expected True, got False'

    def test_Marble_class(self):
        """Test 003: Validate Marble class [1 points]"""
        marble = Marble(pos=0, is_save=True)
        assert isinstance(marble, Marble), f'{marble}Error: Marble class must be defined'

    def test_PlayerState_class(self):
        """Test 004: Validate PlayerState class [1 points]"""
        # Create an instance of PlayerState
        player_state = PlayerState(name="Test Player", list_card=[], list_marble=[])

        # Assert instance is correctly initialized
        assert isinstance(player_state, PlayerState), f"Expected instance of PlayerState, got {type(player_state)}"

        # Assert default attributes
        assert player_state.name == "Test Player", f"Expected name to be 'Test Player', got {player_state.name}"
        assert player_state.list_card == [], f"Expected list_card to be an empty list, got {player_state.list_card}"
        assert player_state.list_marble == [], f"Expected list_marble to be an empty list, got {player_state.list_marble}"

    def test_Action_class(self):
        """Test 005: Validate Action class [1 points]"""
        # Create a mock card
        card = Card(suit="Hearts", rank="5")
        # Create an Action instance
        action = Action(card=card, pos_from=1, pos_to=10, card_swap=None)
        # Check attributes
        assert action.card == card
        assert action.pos_from == 1
        assert action.pos_to == 10
        assert action.card_swap is None

    def test_GamePhase_class(self):
        """Test 006: Validate GamePhase class [1 point]"""
        # Import the GamePhase class (adjust if necessary)
        # Check if GamePhase has expected attributes (example phases)
        assert hasattr(GamePhase, 'RUNNING'), "GamePhase should have an attribute 'RUNNING'."
        assert hasattr(GamePhase, 'FINISHED'), "GamePhase should have an attribute 'FINISHED'."

        # Validate that accessing a phase works
        assert GamePhase.RUNNING.name == 'RUNNING', f"Expected 'RUNNING', got {GamePhase.RUNNING.name}."
        assert GamePhase.FINISHED.name == 'FINISHED', f"Expected 'FINISHED', got {GamePhase.FINISHED.name}."


    def test_game_state(self):
        """Test 007: Validate GameState class [5 points]"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )

        assert game_state.cnt_player == 4, f'Expected cnt_player to be 4, got {game_state.cnt_player}'
        assert game_state.phase == GamePhase.RUNNING, f'Expected phase to be RUNNING, got {game_state.phase}'
        assert game_state.cnt_round == 1, f'Expected cnt_round to be 1, got {game_state.cnt_round}'
        assert game_state.bool_card_exchanged is False, f'Expected bool_card_exchanged to be False, got {game_state.bool_card_exchanged}'
        assert game_state.idx_player_started == 0, f'Expected idx_player_started to be 0, got {game_state.idx_player_started}'
        assert game_state.idx_player_active == 0, f'Expected idx_player_active to be 0, got {game_state.idx_player_active}'
        assert len(game_state.list_player) == 4, f'Expected list_player length to be 4, got {len(game_state.list_player)}'
        assert len(game_state.list_card_draw) == len(GameState.LIST_CARD), f'Expected list_card_draw length to be {len(GameState.LIST_CARD)}, got {len(game_state.list_card_draw)}'
        assert len(game_state.list_card_discard) == 0, f'Expected list_card_discard length to be 0, got {len(game_state.list_card_discard)}'
        assert game_state.card_active is None, f'Expected card_active to be None, got {game_state.card_active}'

    def test_game_state_str(self):
        """Test 008: Validate GameState.__str__ method [5 points]"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )

        expected = (
            "Game Phase: GamePhase.RUNNING\n"
            "Round: 1\n"
            "Active Player: 1\n"
            "Players:\n"
            "Player 1 (Player 1): Cards: 0, Marbles: 0\n"
            "Player 2 (Player 2): Cards: 0, Marbles: 0\n"
            "Player 3 (Player 3): Cards: 0, Marbles: 0\n"
            "Player 4 (Player 4): Cards: 0, Marbles: 0\n"
            "Cards to Draw: 110\n"
            "Cards Discarded: 0\n"
            "Active Card: None\n"
        )

        assert str(game_state) == expected, f'Expected {expected}, got {str(game_state)}'

    '''def set_state(self, state: GameState) -> None:
        """ Set the game to a given state """
        self._state = state'''
    def test_set_state(self):
        """Test 009: Validate Dog.set_state method [5 points]"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )

        self.game_server.set_state(game_state)
        assert self.game_server._state == game_state, f'Expected {game_state}, got {self.game_server._state}'

    def test_list_action(self):
        """Test 009: Validate Dog.set_state method [5 points]"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x'),Card(rank='3', suit='x'),Card(rank='4', suit='x'),Card(rank='5', suit='x'),Card(rank='6', suit='x'),Card(rank='7', suit='x'),Card(rank='8', suit='x'), Card(rank='K', suit='x')], list_marble=[Marble(pos=1, is_save=False),Marble(pos=0, is_save=True),Marble(pos=68, is_save=True),Marble(pos=65, is_save=True)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=2, is_save=False)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=3, is_save=False)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=4, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)
        result = self.game_server.get_list_action()

        assert len(result) >0

    def test_apply_action(self):
        """Test 009: Validate Dog.set_state method [5 points]"""
        # Initialize the game state
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(
                    name='Player 1',
                    list_card=[
                        Card(rank='2', suit='x'), 
                        Card(rank='3', suit='x'), 
                        Card(rank='4', suit='x'), 
                        Card(rank='5', suit='x'), 
                        Card(rank='6', suit='x'), 
                        Card(rank='7', suit='x'), 
                        Card(rank='8', suit='x'), 
                        Card(rank='9', suit='x')
                    ],
                    list_marble=[
                        Marble(pos=1, is_save=False),
                        Marble(pos=0, is_save=True),
                        Marble(pos=68, is_save=True),
                        Marble(pos=65, is_save=True)
                    ]
                ),
                PlayerState(name='Player 2', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=2, is_save=False)]),
                PlayerState(name='Player 3', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=3, is_save=False)]),
                PlayerState(name='Player 4', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=4, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        # Iterate through the player's cards and test marble movement
        for card in self.game_server._state.list_player[0].list_card:
            rank = int(card.rank)
            initial_pos = self.game_server._state.list_player[0].list_marble[0].pos

            # Apply action
            self.game_server.apply_action(Action(card=card, pos_from=initial_pos, pos_to=initial_pos + rank))

            # Check the updated position of the marble
            updated_pos = self.game_server._state.list_player[0].list_marble[0].pos
            assert updated_pos == initial_pos + rank, f'Expected {initial_pos + rank}, got {updated_pos}'

            


    def test_deal_cards_x(self):
        for i in range(2, 10):
            """Test 009: Validate Dog.set_state method [5 points]"""
            game_state = GameState(
                cnt_player=4,
                phase=GamePhase.RUNNING,
                cnt_round=i,
                bool_card_exchanged=False,
                idx_player_started=0,
                idx_player_active=0,
                list_player=[
                    PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x'),Card(rank='3', suit='x'),Card(rank='4', suit='x'),Card(rank='5', suit='x'),Card(rank='6', suit='x'),Card(rank='7', suit='x'),Card(rank='8', suit='x'), Card(rank='K', suit='x')], list_marble=[Marble(pos=1, is_save=False),Marble(pos=0, is_save=True),Marble(pos=68, is_save=True),Marble(pos=65, is_save=True)]),
                    PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=2, is_save=False)]),
                    PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=3, is_save=False)]),
                    PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=4, is_save=False)])
                ],
                list_card_draw=GameState.LIST_CARD.copy(),
                list_card_discard=[],
                card_active=None
            )
            self.game_server.set_state(game_state)



            self.game_server.deal_cards()

        assert True


    def test_deal_cards(self):

        """Test 009: Validate Dog.set_state method [5 points]"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x'),Card(rank='3', suit='x'),Card(rank='4', suit='x'),Card(rank='5', suit='x'),Card(rank='6', suit='x'),Card(rank='7', suit='x'),Card(rank='8', suit='x'), Card(rank='K', suit='x')], list_marble=[Marble(pos=1, is_save=False),Marble(pos=0, is_save=True),Marble(pos=68, is_save=True),Marble(pos=65, is_save=True)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=2, is_save=False)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=3, is_save=False)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=4, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.get_player_view(0)



        self.game_server.deal_cards()

        assert True

    def test_none_actions(self):

        """Test 009: Validate Dog.set_state method [5 points]"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1',
                            list_card=[Card(rank='2', suit='x'), Card(rank='3', suit='x'), Card(rank='4', suit='x'),
                                       Card(rank='5', suit='x'), Card(rank='6', suit='x'), Card(rank='7', suit='x'),
                                       Card(rank='8', suit='x'), Card(rank='K', suit='x')],
                            list_marble=[Marble(pos=1, is_save=False), Marble(pos=0, is_save=True),
                                         Marble(pos=68, is_save=True), Marble(pos=65, is_save=True)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=2, is_save=False)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=3, is_save=False)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=4, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        actions = self.game_server.get_list_action()

        assert len(actions) > 0
        

    def test_game_over(self):
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1',
                            list_card=[],
                            list_marble=[Marble(pos=68, is_save=False), Marble(pos=69, is_save=True),
                                        Marble(pos=70, is_save=True), Marble(pos=71, is_save=True)]),
                PlayerState(name='Player 2', list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=2, is_save=False)]),
                PlayerState(name='Player 3', list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=84, is_save=False), Marble(pos=85, is_save=True),
                                        Marble(pos=86, is_save=True), Marble(pos=87, is_save=True)]),
                PlayerState(name='Player 4', list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=4, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server._state = game_state  # Ensure game_server uses the correct game state
        self.game_server._check_team_win()
        assert self.game_server._state.phase == GamePhase.FINISHED, f'Expected phase to be FINISHED, got {self.game_server._state.phase}'
        

    def test_state(self):
        """Test the initialization and state consistency of the game"""
        # Create a custom game state
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1',
                            list_card=[],
                            list_marble=[
                                Marble(pos=68, is_save=False), Marble(pos=69, is_save=True),
                                Marble(pos=70, is_save=True), Marble(pos=71, is_save=True)
                            ]),
                PlayerState(name='Player 2',
                            list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=2, is_save=False)]),
                PlayerState(name='Player 3',
                            list_card=[Card(rank='2', suit='x')],
                            list_marble=[
                                Marble(pos=84, is_save=False), Marble(pos=85, is_save=True),
                                Marble(pos=86, is_save=True), Marble(pos=87, is_save=True)
                            ]),
                PlayerState(name='Player 4',
                            list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=4, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        # Set the game state
        self.game_server.set_state(game_state)

        # Check if the game server's state matches the initialized game state
        assert self.game_server.get_state() == game_state, \
        f'Expected state to match the initialized state, but got {self.game_server.get_state()}'

        # Validate the printed state (using print_state for visual inspection)
        self.game_server.print_state()

        # Perform specific assertions
        assert len(game_state.list_player) == 4, \
            f'Expected 4 players in the game, got {len(game_state.list_player)}'
        assert game_state.list_player[0].name == 'Player 1', \
            f'Expected Player 1 name, got {game_state.list_player[0].name}'
        assert len(game_state.list_card_draw) == len(GameState.LIST_CARD), \
            f'Expected {len(GameState.LIST_CARD)} cards in draw pile, got {len(game_state.list_card_draw)}'
        assert game_state.phase == GamePhase.RUNNING, \
            f'Expected phase to be RUNNING, got {game_state.phase}'
        assert game_state.cnt_round == 1, \
            f'Expected round to be 1, got {game_state.cnt_round}'
        # Example check for a marble's position and state
        assert game_state.list_player[0].list_marble[0].pos == 68, \
            f'Expected marble at position 68, got {game_state.list_player[0].list_marble[0].pos}'
        assert game_state.list_player[0].list_marble[0].is_save is False, \
            f'Expected marble save state to be False, got {game_state.list_player[0].list_marble[0].is_save}'

    def test_get_player_view(self):
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1',
                            list_card=[],
                            list_marble=[Marble(pos=68, is_save=False), Marble(pos=69, is_save=True),
                                         Marble(pos=70, is_save=True), Marble(pos=71, is_save=True)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=2, is_save=False)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=84, is_save=False), Marble(pos=85, is_save=True),
                                         Marble(pos=86, is_save=True), Marble(pos=87, is_save=True)]),
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')],
                            list_marble=[Marble(pos=4, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.get_player_view(0)
        assert True

        self.game_server.set_state(game_state)
        assert self.game_server.get_state() == game_state, f'Expected {game_state}, got {self.game_server.get_state()}'

    def test_print_state(self):
        """Test 011: Validate Dog.print_state method [5 points]"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )

        self.game_server.set_state(game_state)
        self.game_server.print_state()
        assert self.game_server.get_state() == game_state, f'Expected {game_state}, got {self.game_server.get_state()}'

    def test_get_list_action_no_card_exchanged(self):
        """Test get_list_action when no card has been exchanged"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[Card(rank='A', suit='x')], list_marble=[Marble(pos=1, is_save=False)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[Card(rank='2', suit='w')], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)
        actions = self.game_server.get_list_action()
        assert len(actions) == 1

    def test_get_list_action_card_exchanged(self):
        """Test get_list_action when a card has been exchanged"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[Card(rank='A', suit='x')], list_marble=[Marble(pos=1, is_save=False)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[Card(rank='2', suit='w')], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)
        actions = self.game_server.get_list_action()
        assert len(actions) > 0 # At least one action should be available

    def test_get_list_action_player_finished(self):
        """Test get_list_action when the active player has finished"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=True,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[Card(rank='A', suit='x')], list_marble=[Marble(pos=68, is_save=True), Marble(pos=69, is_save=True), Marble(pos=70, is_save=True), Marble(pos=71, is_save=True)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)
        actions = self.game_server.get_list_action()
        assert len(actions) == 0

    def test_all_cards_actions(self):
        card_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        """Test get_list_action when the active player has all cards"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=True,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[Marble(pos=1, is_save=False)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        # Add all cards to the player[0] from suit '♥'
        for card in card_list:
            game_state.list_player[0].list_card.append(Card(rank=card, suit='♥'))
        self.game_server.set_state(game_state)
        actions = self.game_server.get_list_action()
        assert len(actions) >= len(card_list)

        # test all cards have atleast 1 action individually
        self.game_server.set_state(game_state)
        for card in card_list:
            game_state.list_player[0].list_card.append(Card(rank=card, suit='♥'))
            actions = self.game_server.get_list_action()
            assert len(actions) >= 1, f'Expected at least 1 action with card {card}, got {len(actions)}'

    def test_get_marbles_between(self):
        """Test _get_marbles_between method"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[Marble(pos=1, is_save=False), Marble(pos=5, is_save=False)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[Marble(pos=8, is_save=False), Marble(pos=12, is_save=False)]),
                PlayerState(name='Player 3', list_card=[], list_marble=[Marble(pos=10, is_save=False)]),
                PlayerState(name='Player 4', list_card=[], list_marble=[Marble(pos=15, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        # Test case 1: No marbles between pos_from and pos_to
        marbles = self.game_server._get_marbles_between(1, 2)
        assert len(marbles) == 0, f'Expected 0 marbles, got {len(marbles)}'

        # Test case 2: One marble between pos_from and pos_to
        marbles = self.game_server._get_marbles_between(1, 6)
        assert len(marbles) == 1, f'Expected 1 marble, got {len(marbles)}'
        assert marbles[0].pos == 5, f'Expected marble at pos 5, got {marbles[0].pos}'

        # Test case 3: Multiple marbles between pos_from and pos_to
        marbles = self.game_server._get_marbles_between(1, 8)
        assert len(marbles) == 2, f'Expected 2 marbles, got {len(marbles)}'
        assert marbles[0].pos == 5, f'Expected marble at pos 5, got {marbles[0].pos}'
        assert marbles[1].pos == 8, f'Expected marble at pos 8, got {marbles[1].pos}'

    def test_apply_action_card_7(self):
        """Test apply_action with card rank 7"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(
                    name='Player 1',
                    list_card=[Card(rank='7', suit='x')],
                    list_marble=[Marble(pos=1, is_save=False)]
                ),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        action = Action(card=Card(rank='7', suit='x'), pos_from=1, pos_to=8)
        self.game_server.apply_action(action)

        assert self.game_server._state.list_player[0].list_marble[0].pos == 8, \
            f'Expected marble position to be 8, got {self.game_server._state.list_player[0].list_marble[0].pos}'
        
    def test_apply_action_card_exchange(self):
        """Test apply_action with card exchange"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(
                    name='Player 1',
                    list_card=[Card(rank='A', suit='x')],
                    list_marble=[]
                ),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        action = Action(card=Card(rank='A', suit='x'), pos_from=None, pos_to=None)
        self.game_server.apply_action(action)

        assert len(self.game_server._state.list_player[2].list_card) == 1, \
            f'Expected partner to have 1 card, got {len(self.game_server._state.list_player[2].list_card)}'
        assert len(self.game_server._state.list_player[0].list_card) == 0, \
            f'Expected active player to have 0 cards, got {len(self.game_server._state.list_player[0].list_card)}'

    
    def test_apply_action_card_exchange_with_partner(self):
        """Test apply_action with card exchange with partner"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(
                    name='Player 1',
                    list_card=[Card(rank='A', suit='x')],
                    list_marble=[]
                ),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        action = Action(card=Card(rank='A', suit='x'), pos_from=None, pos_to=None)
        self.game_server.apply_action(action)

        assert len(self.game_server._state.list_player[2].list_card) == 1, \
            f'Expected partner to have 1 card, got {len(self.game_server._state.list_player[2].list_card)}'
        assert len(self.game_server._state.list_player[0].list_card) == 0, \
            f'Expected active player to have 0 cards, got {len(self.game_server._state.list_player[0].list_card)}'
        assert self.game_server._state.idx_player_active == 1, \
            f'Expected next active player to be 1, got {self.game_server._state.idx_player_active}'

    def test_apply_action_card_exchange_with_partner_limit(self):
        """Test apply_action with card exchange with partner limit"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(
                    name='Player 1',
                    list_card=[Card(rank='A', suit='x')],
                    list_marble=[]
                ),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)
        self.game_server.card_exchanges_counter = 4

        action = Action(card=Card(rank='A', suit='x'), pos_from=None, pos_to=None)
        self.game_server.apply_action(action)

        assert self.game_server._state.bool_card_exchanged is True, \
            f'Expected bool_card_exchanged to be True, got {self.game_server._state.bool_card_exchanged}'
        assert self.game_server.card_exchanges_counter == 0, \
            f'Expected card_exchanges_counter to be 0, got {self.game_server.card_exchanges_counter}'
        assert self.game_server._state.idx_player_active == 1, \
            f'Expected next active player to be 1, got {self.game_server._state.idx_player_active}'

    
    def test_apply_action_none_action(self):
        """Test apply_action with None action"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(
                    name='Player 1',
                    list_card=[Card(rank='2', suit='x')],
                    list_marble=[Marble(pos=1, is_save=False)]
                ),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        self.game_server.apply_action(None)

        assert self.game_server.none_actions_counter == 1, \
            f'Expected none_actions_counter to be 1, got {self.game_server.none_actions_counter}'
        assert len(self.game_server._state.list_player[0].list_card) == 0, \
            f'Expected active player to have 0 cards, got {len(self.game_server._state.list_player[0].list_card)}'

    def test_swap_marbles(self):
        """Test _swap_marbles method"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[Marble(pos=1, is_save=False), Marble(pos=5, is_save=False)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[Marble(pos=8, is_save=False), Marble(pos=12, is_save=False)]),
                PlayerState(name='Player 3', list_card=[], list_marble=[Marble(pos=10, is_save=False)]),
                PlayerState(name='Player 4', list_card=[], list_marble=[Marble(pos=15, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        # Test case 1: Swap marbles within the same player
        action = Action(card=Card(rank='J', suit='x'), pos_from=1, pos_to=5)
        self.game_server._swap_marbles(action)
        assert self.game_server._state.list_player[0].list_marble[0].pos == 5, f'Expected marble at pos 5, got {self.game_server._state.list_player[0].list_marble[0].pos}'
        assert self.game_server._state.list_player[0].list_marble[1].pos == 1, f'Expected marble at pos 1, got {self.game_server._state.list_player[0].list_marble[1].pos}'

        # Test case 2: Swap marbles between different players
        action = Action(card=Card(rank='J', suit='x'), pos_from=8, pos_to=10)
        self.game_server._swap_marbles(action)
        assert self.game_server._state.list_player[1].list_marble[0].pos == 10, f'Expected marble at pos 10, got {self.game_server._state.list_player[1].list_marble[0].pos}'
        assert self.game_server._state.list_player[2].list_marble[0].pos == 8, f'Expected marble at pos 8, got {self.game_server._state.list_player[2].list_marble[0].pos}'

        # Test case 3: Swap marbles where one marble is not found
        action = Action(card=Card(rank='J', suit='x'), pos_from=1, pos_to=20)
        self.game_server._swap_marbles(action)
        assert self.game_server._state.list_player[0].list_marble[0].pos == 5, f'Expected marble at pos 5, got {self.game_server._state.list_player[0].list_marble[0].pos}'
        assert self.game_server._state.list_player[0].list_marble[1].pos == 1, f'Expected marble at pos 1, got {self.game_server._state.list_player[0].list_marble[1].pos}'

        # Test case 4: Swap marbles where both marbles are not found
        action = Action(card=Card(rank='J', suit='x'), pos_from=20, pos_to=30)
        self.game_server._swap_marbles(action)
        assert self.game_server._state.list_player[0].list_marble[0].pos == 5, f'Expected marble at pos 5, got {self.game_server._state.list_player[0].list_marble[0].pos}'
        assert self.game_server._state.list_player[0].list_marble[1].pos == 1, f'Expected marble at pos 1, got {self.game_server._state.list_player[0].list_marble[1].pos}'

    def test_random_player_select_action(self):
        """Test RandomPlayer's select_action method"""
        player = RandomPlayer()
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[Card(rank='2', suit='x')], list_marble=[Marble(pos=1, is_save=False)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        actions = [
            Action(card=Card(rank='2', suit='x'), pos_from=1, pos_to=3),
            Action(card=Card(rank='3', suit='x'), pos_from=1, pos_to=4)
        ]

        selected_action = player.select_action(game_state, actions)
        assert selected_action in actions, f'Expected selected action to be one of {actions}, got {selected_action}'

    def test_reset_to_kennel(self):
        """Test _reset_to_kennel method"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[Marble(pos=10, is_save=False), Marble(pos=15, is_save=False)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[Marble(pos=20, is_save=False), Marble(pos=25, is_save=False)]),
                PlayerState(name='Player 3', list_card=[], list_marble=[Marble(pos=30, is_save=False), Marble(pos=35, is_save=False)]),
                PlayerState(name='Player 4', list_card=[], list_marble=[Marble(pos=40, is_save=False), Marble(pos=45, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        # Test case 1: Reset marble for Player 1
        marble = self.game_server._state.list_player[0].list_marble[0]
        self.game_server._reset_to_kennel(marble)
        assert marble.pos == self.game_server.PLAYER_POSITIONS[0]['queue_start'], f'Expected marble position to be {self.game_server.PLAYER_POSITIONS[0]["queue_start"]}, got {marble.pos}'
        assert marble.is_save is True, f'Expected marble to be safe, got {marble.is_save}'

        # Test case 2: Reset marble for Player 2
        marble = self.game_server._state.list_player[1].list_marble[1]
        self.game_server._reset_to_kennel(marble)
        assert marble.pos == self.game_server.PLAYER_POSITIONS[1]['queue_start'] + 1, f'Expected marble position to be {self.game_server.PLAYER_POSITIONS[1]["queue_start"] + 1}, got {marble.pos}'
        assert marble.is_save is True, f'Expected marble to be safe, got {marble.is_save}'

        # Test case 3: Reset marble for Player 3
        marble = self.game_server._state.list_player[2].list_marble[0]
        self.game_server._reset_to_kennel(marble)
        assert marble.pos == self.game_server.PLAYER_POSITIONS[2]['queue_start'], f'Expected marble position to be {self.game_server.PLAYER_POSITIONS[2]["queue_start"]}, got {marble.pos}'
        assert marble.is_save is True, f'Expected marble to be safe, got {marble.is_save}'

        # Test case 4: Reset marble for Player 4
        marble = self.game_server._state.list_player[3].list_marble[1]
        self.game_server._reset_to_kennel(marble)
        assert marble.pos == self.game_server.PLAYER_POSITIONS[3]['queue_start'] + 1, f'Expected marble position to be {self.game_server.PLAYER_POSITIONS[3]["queue_start"] + 1}, got {marble.pos}'
        assert marble.is_save is True, f'Expected marble to be safe, got {marble.is_save}'

    def test_refresh_deck(self):
        """Test _refresh_deck method"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=[],
            list_card_discard=[Card(rank='A', suit='x'), Card(rank='2', suit='x')],
            card_active=None
        )
        self.game_server.set_state(game_state)

        # Call the _refresh_deck method
        self.game_server._refresh_deck()

        # Check if the draw pile has been refreshed and shuffled
        assert len(self.game_server._state.list_card_draw) == len(GameState.LIST_CARD), \
            f'Expected draw pile length to be {len(GameState.LIST_CARD)}, got {len(self.game_server._state.list_card_draw)}'
        assert len(self.game_server._state.list_card_discard) == 0, \
            f'Expected discard pile length to be 0, got {len(self.game_server._state.list_card_discard)}'

        # Check if the draw pile is shuffled (not in the same order as LIST_CARD)
        assert self.game_server._state.list_card_draw != GameState.LIST_CARD, \
            'Expected draw pile to be shuffled, but it is in the same order as LIST_CARD'

    def test_is_way_blocked(self):
        """Test _is_way_blocked method"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[Marble(pos=0, is_save=True), Marble(pos=5, is_save=False)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[Marble(pos=16, is_save=True), Marble(pos=20, is_save=False)]),
                PlayerState(name='Player 3', list_card=[], list_marble=[Marble(pos=32, is_save=True), Marble(pos=35, is_save=False)]),
                PlayerState(name='Player 4', list_card=[], list_marble=[Marble(pos=48, is_save=True), Marble(pos=50, is_save=False)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        # Test case 1: No marbles blocking the way
        result = self.game_server._is_way_blocked(pos_to=10, pos_from=5, safe_marbles=self.game_server._get_all_safe_marbles())
        assert result is False, f'Expected False, got {result}'

        # Test case 2: Marble blocking the way at position 16
        result = self.game_server._is_way_blocked(pos_to=20, pos_from=5, safe_marbles=self.game_server._get_all_safe_marbles())
        assert result is True, f'Expected True, got {result}'

        # Test case 3: Marble blocking the way at position 0 (circular board)
        result = self.game_server._is_way_blocked(pos_to=65, pos_from=60, safe_marbles=self.game_server._get_all_safe_marbles())
        assert result is True, f'Expected True, got {result}'

        # Test case 5: Marble blocking the way at position 32
        result = self.game_server._is_way_blocked(pos_to=40, pos_from=30, safe_marbles=self.game_server._get_all_safe_marbles())
        assert result is True, f'Expected True, got {result}'

    def test_is_valid_move_in_final_area(self):
        """Test _is_valid_move_in_final_area method"""
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[Marble(pos=68, is_save=True), Marble(pos=69, is_save=True)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[Marble(pos=72, is_save=True), Marble(pos=73, is_save=True)]),
                PlayerState(name='Player 3', list_card=[], list_marble=[Marble(pos=84, is_save=True), Marble(pos=85, is_save=True)]),
                PlayerState(name='Player 4', list_card=[], list_marble=[Marble(pos=88, is_save=True), Marble(pos=89, is_save=True)])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

    
        # Test case 1: Invalid move within the final area (jumping over a marble)
        result = self.game_server._is_valid_move_in_final_area(pos_from=68, pos_to=71, marbles=game_state.list_player[0].list_marble, final_area_start=68, final_area_end=71)
        assert result is False, f'1 Expected False, got {result}'

        # Test case 2: Valid move outside the final area
        result = self.game_server._is_valid_move_in_final_area(pos_from=60, pos_to=65, marbles=game_state.list_player[0].list_marble, final_area_start=68, final_area_end=71)
        assert result is True, f'2 Expected True, got {result}'

        # Test case 3: Invalid move within the final area (jumping over multiple marbles)
        result = self.game_server._is_valid_move_in_final_area(pos_from=68, pos_to=72, marbles=game_state.list_player[0].list_marble + game_state.list_player[1].list_marble, final_area_start=68, final_area_end=75)
        assert result is False, f'3 Expected False, got {result}'

        # Test case 4: Valid move within the final area with no marbles in the way
        result = self.game_server._is_valid_move_in_final_area(pos_from=68, pos_to=69, marbles=game_state.list_player[2].list_marble, final_area_start=68, final_area_end=71)
        assert result is True, f'4 Expected True, got {result}'

    def test_joker_transformation_actions(self):
        # Setup a state where a player has a Joker card
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=True,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(
                    name='Player 1',
                    list_card=[Card(rank='JKR', suit='')],
                    list_marble=[Marble(pos=1, is_save=False)]
                ),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)
        actions = self.game_server.get_list_action()
        # Joker should transform into multiple possible cards
        assert any(act.card_swap for act in actions), "Expected joker to produce actions with card_swap options"

    def test_refresh_deck_when_draw_empty(self):
        # Create a state with a very limited draw pile
        # Let's say only 2 cards left in draw pile
        limited_draw_pile = GameState.LIST_CARD[:2]
        discard_pile = [Card(suit='♥', rank='2'), Card(suit='♣', rank='K')]  # Some discard cards

        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=True,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(name='Player 1', list_card=[], list_marble=[Marble(pos=1, is_save=False)]),
                PlayerState(name='Player 2', list_card=[], list_marble=[]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=limited_draw_pile,
            list_card_discard=discard_pile,
            card_active=None
        )
        self.game_server.set_state(game_state)

        # Apply None action 4 times to simulate end of a round - should trigger new dealing
        for _ in range(4):
            self.game_server.apply_action(None)

        # At this point, the game tries to deal new cards. Since the draw pile is almost empty,
        # it should trigger a deck refresh using the discarded cards.
        # After refresh, the draw pile should not be empty.
        assert len(self.game_server.get_state().list_card_draw) > 2, \
            "Expected the draw pile to be replenished and shuffled after it became empty."

        # Also verify that bool_card_exchanged is reset after new round
        assert not self.game_server.get_state().bool_card_exchanged, \
            "Expected bool_card_exchanged to be reset after the deck refresh and new dealing."

    def test_card_7_multiple_partial_moves(self):
        # Setup a game state where the active player has a 7 card and a marble on the board.
        # We'll simulate partial moves: first move 3 steps, then 4 steps, totaling 7.
        game_state = GameState(
            cnt_player=4,
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_card_exchanged=True,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[
                PlayerState(
                    name='Player 1',
                    list_card=[Card(suit='x', rank='7')],
                    list_marble=[Marble(pos=10, is_save=False)]
                ),
                PlayerState(name='Player 2', list_card=[], list_marble=[Marble(pos=15, is_save=False)]),
                PlayerState(name='Player 3', list_card=[], list_marble=[]),
                PlayerState(name='Player 4', list_card=[], list_marble=[])
            ],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        self.game_server.set_state(game_state)

        # First partial move: Move the marble 3 steps forward with 7 card
        action_3_steps = Action(card=Card(suit='x', rank='7'), pos_from=10, pos_to=13)
        self.game_server.apply_action(action_3_steps)

        # At this point, card_active should still be '7', since total 7 steps not yet completed
        assert self.game_server.get_state().card_active is not None, "Expected card_active to remain set after partial 7 steps."
        assert self.game_server.get_state().card_active.rank == '7', "Expected card_active to be the 7 card after partial move."
        assert self.game_server._state.idx_player_active == 0, "Expected to remain the same player's turn after partial move."

        # Second partial move: Move the same marble 4 more steps forward
        action_4_steps = Action(card=Card(suit='x', rank='7'), pos_from=13, pos_to=17)
        self.game_server.apply_action(action_4_steps)

        # Now total 7 steps have been completed. The card_active should reset and turn should pass to next player.
        assert self.game_server.get_state().card_active is None, "Expected card_active to reset after completing all 7 steps."
        assert self.game_server._state.idx_player_active == 1, "Expected turn to move to next player after completing all 7 steps."
        assert self.game_server._state.list_player[0].list_marble[
                   0].pos == 17, "Expected the marble to be moved to position 17."

# --- end of tests ---