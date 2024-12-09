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
        pass

    def test_Action_class(self):
        """Test 005: Validate Action class [1 points]"""
        pass

    def test_GamePhase_class(self):
        """Test 006: Validate GamePhase class [1 points]"""
        pass

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
        self.game_server.print_state()
        assert True

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

    


        
# --- end of tests ---


