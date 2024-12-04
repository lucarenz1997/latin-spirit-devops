# runcmd: cd ../.. & venv\Scripts\python server/py/dog_template.py
import random
from enum import Enum
from typing import List, Optional, ClassVar

from pydantic import BaseModel

from server.py.game import Game, Player, GameAction


class Card(BaseModel):
    suit: str  # card suit (color)
    rank: str  # card rank


class Marble(BaseModel):
    pos: int  # position on board (0 to 95)
    is_save: bool  # true if marble was moved out of kennel and was not yet moved


class PlayerState(BaseModel):
    name: str  # name of player
    list_card: List[Card]  # list of cards
    list_marble: List[Marble]  # list of marbles


class Action(BaseModel):
    card: Card  # card to play
    pos_from: Optional[int]  # position to move the marble from
    pos_to: Optional[int]  # position to move the marble to
    card_swap: Optional[Card] = None  # optional card to swap ()


class GamePhase(str, Enum):
    SETUP = 'setup'  # before the game has started
    RUNNING = 'running'  # while the game is running
    FINISHED = 'finished'  # when the game is finished


class GameState(BaseModel):
    LIST_SUIT: ClassVar[List[str]] = ['♠', '♥', '♦', '♣']  # 4 suits (colors)
    LIST_RANK: ClassVar[List[str]] = [
        '2', '3', '4', '5', '6', '7', '8', '9', '10',  # 13 ranks + Joker
        'J', 'Q', 'K', 'A', 'JKR'
    ]
    LIST_CARD: ClassVar[List[Card]] = [
                                          # 2: Move 2 spots forward
                                          Card(suit='♠', rank='2'), Card(suit='♥', rank='2'), Card(
            suit='♦', rank='2'), Card(suit='♣', rank='2'),
                                          # 3: Move 3 spots forward
                                          Card(suit='♠', rank='3'), Card(suit='♥', rank='3'), Card(
            suit='♦', rank='3'), Card(suit='♣', rank='3'),
                                          # 4: Move 4 spots forward or back
                                          Card(suit='♠', rank='4'), Card(suit='♥', rank='4'), Card(
            suit='♦', rank='4'), Card(suit='♣', rank='4'),
                                          # 5: Move 5 spots forward
                                          Card(suit='♠', rank='5'), Card(suit='♥', rank='5'), Card(
            suit='♦', rank='5'), Card(suit='♣', rank='5'),
                                          # 6: Move 6 spots forward
                                          Card(suit='♠', rank='6'), Card(suit='♥', rank='6'), Card(
            suit='♦', rank='6'), Card(suit='♣', rank='6'),
                                          # 7: Move 7 single steps forward
                                          Card(suit='♠', rank='7'), Card(suit='♥', rank='7'), Card(
            suit='♦', rank='7'), Card(suit='♣', rank='7'),
                                          # 8: Move 8 spots forward
                                          Card(suit='♠', rank='8'), Card(suit='♥', rank='8'), Card(
            suit='♦', rank='8'), Card(suit='♣', rank='8'),
                                          # 9: Move 9 spots forward
                                          Card(suit='♠', rank='9'), Card(suit='♥', rank='9'), Card(
            suit='♦', rank='9'), Card(suit='♣', rank='9'),
                                          # 10: Move 10 spots forward
                                          Card(suit='♠', rank='10'), Card(suit='♥', rank='10'), Card(
            suit='♦', rank='10'), Card(suit='♣', rank='10'),
                                          # Jake: A marble must be exchanged
                                          Card(suit='♠', rank='J'), Card(suit='♥', rank='J'), Card(
            suit='♦', rank='J'), Card(suit='♣', rank='J'),
                                          # Queen: Move 12 spots forward
                                          Card(suit='♠', rank='Q'), Card(suit='♥', rank='Q'), Card(
            suit='♦', rank='Q'), Card(suit='♣', rank='Q'),
                                          # King: Start or move 13 spots forward
                                          Card(suit='♠', rank='K'), Card(suit='♥', rank='K'), Card(
            suit='♦', rank='K'), Card(suit='♣', rank='K'),
                                          # Ass: Start or move 1 or 11 spots forward
                                          Card(suit='♠', rank='A'), Card(suit='♥', rank='A'), Card(
            suit='♦', rank='A'), Card(suit='♣', rank='A'),
                                          # Joker: Use as any other card you want
                                          Card(suit='', rank='JKR'), Card(
            suit='', rank='JKR'), Card(suit='', rank='JKR')
                                      ] * 2

    cnt_player: int = 4  # number of players (must be 4)
    phase: GamePhase  # current phase of the game
    cnt_round: int  # current round
    bool_card_exchanged: bool  # true if cards was exchanged in round
    idx_player_started: int  # index of player that started the round
    idx_player_active: int  # index of active player in round
    list_player: List[PlayerState]  # list of players
    list_card_draw: List[Card]  # list of cards to draw
    list_card_discard: List[Card]  # list of cards discarded
    # active card (for 7 and JKR with sequence of actions)
    card_active: Optional[Card]

    def __str__(self) -> str:
        player_states = "\n".join(
            f"Player {i + 1} ({player.name}): Cards: {len(player.list_card)}, Marbles: {len(player.list_marble)}"
            for i, player in enumerate(self.list_player)
        )
        return (
            f"Game Phase: {self.phase}\n"
            f"Round: {self.cnt_round}\n"
            f"Active Player: {self.idx_player_active + 1}\n"
            f"Players:\n{player_states}\n"
            f"Cards to Draw: {len(self.list_card_draw)}\n"
            f"Cards Discarded: {len(self.list_card_discard)}\n"
            f"Active Card: {self.card_active}\n"
        )


class Dog(Game):
    # Constants for player positions
    PLAYER_POSITIONS = {
        0: {'start': 0, 'queue_start': 64, 'final_start': 68},
        1: {'start': 16, 'queue_start': 72, 'final_start': 76},
        2: {'start': 32, 'queue_start': 80, 'final_start': 84},
        3: {'start': 48, 'queue_start': 88, 'final_start': 92}
    }

    # Total steps in the main path ignoring the "special fields"
    TOTAL_STEPS = 64

    def __init__(self) -> None:
        """ Game initialization (set_state call not necessary, we expect 4 players) """
        super().__init__()
        self._state = GameState(
            phase=GamePhase.RUNNING,
            cnt_round=1,
            bool_game_finished=False,
            bool_card_exchanged=False,
            idx_player_started=0,
            idx_player_active=0,
            list_player=[PlayerState(
                name=f"Player {i + 1}", list_card=[], list_marble=[]) for i in range(4)],
            list_card_draw=GameState.LIST_CARD.copy(),
            list_card_discard=[],
            card_active=None
        )
        random.shuffle(self._state.list_card_draw)
        self.deal_cards()
        self._set_marbles()

    def set_state(self, state: GameState) -> None:
        """ Set the game to a given state """
        self._state = state

    def get_state(self) -> GameState:
        """ Get the complete, unmasked game state """
        return self._state

    def print_state(self) -> None:
        """ Print the current game state """
        print(self._state)

    def get_list_action(self) -> List[Action]:
        """ Get a list of possible actions for the active player """
        actions = []
        to_positions = []
        active_player = self._state.list_player[self._state.idx_player_active]
        marbles_in_kennel = self._count_marbles_in_kennel()
        for card in active_player.list_card:
            for marble in active_player.list_marble:
                # TODO Go through all cards and marbles and return the possible positions.

                # if marble is in kennel
                queue_start = self.PLAYER_POSITIONS[self._state.idx_player_active]['queue_start']
                if marble.pos in range(queue_start,
                                       queue_start + 4):

                    # only allow actions for ACE, KING or JOKER
                    if card.rank in ['A', 'JKR', 'K']:
                        start_position = self.PLAYER_POSITIONS[self._state.idx_player_active]['start']

                        # allow only if the current player does not have a marble on start
                        if all(m.pos != start_position for m in active_player.list_marble):
                            # if 4 in kennel, start_position + 3 - #in kennel-1
                            if marble.pos == queue_start + 4 - marbles_in_kennel:
                                actions.append(Action(card=card, pos_from=marble.pos, pos_to=start_position,
                                                      card_swap=None))
                else:
                    if card.rank.isdigit() and card.rank not in ['7', '4']:
                        to_positions = self._calculate_position_to(
                            marble.pos, card, self._state.idx_player_active)

                    # TODO Add more logic for all the other cards LATIN-35
                    if card.rank == '7':
                        # can be split into multiple marbles. if takes over, reset other marble
                        # to_positions = ...
                        pass

                    # checks for each possible position if the way is blocked. if it is not blocked, we add it to action.
                    for pos_to in to_positions:
                        if not self._is_way_blocked(
                                pos_to, marble.pos, self._get_all_safe_marbles()):
                            # TODO add logic for card_swap (once we know what this is used for) LATIN-37
                            actions.append(Action(card=card, pos_from=marble.pos, pos_to=pos_to,
                                                  card_swap=None))
            unique_actions = []
            for action in actions:
                if action not in unique_actions:
                    unique_actions.append(action)

        return unique_actions

    def _count_marbles_in_kennel(self) -> int:
        active_player = self._state.list_player[self._state.idx_player_active]
        queue_start = self.PLAYER_POSITIONS[self._state.idx_player_active]['queue_start']
        queue_end = queue_start + 4
        marbles_in_kennel = [marble for marble in active_player.list_marble if
                             queue_start <= int(marble.pos) < queue_end]
        return len(marbles_in_kennel)

    def _check_finish_game(self):
        """
        Check if the game is finished, i.e., any player has all their marbles in the final area.
        If the game is finished, set the game phase to FINISHED.
        """
        for idx_player, player in enumerate(self._state.list_player):
            final_start = self.PLAYER_POSITIONS[idx_player]['final_start']
            # Final area positions
            final_positions = range(final_start, final_start + 4)
            if all(marble.pos in final_positions for marble in player.list_marble):
                # All marbles of this player are in their final positions
                self._state.phase = GamePhase.FINISHED
                print(
                    f"Player {idx_player + 1} ({player.name}) has won the game!")
                return True
        return False

    # TODO LATIN-47 Check for TEAM WIN, if 2 players of the same team have all their marbles in the final area
    def _check_team_win(self):
        """
        Check if a team has won, that means, both players on a team have all their marbles in the final area.
        """
        # Define teams
        teams = {
            0: [0, 2],  # Team 1: Player 1 and Player 3
            1: [1, 3],  # Team 2: Player 2 and Player 4
        }

        # Check each team
        for team_id, players in teams.items():  # Iterates through each team and its associated players
            team_wins = True
            for player_idx in players:
                final_start = self.PLAYER_POSITIONS[player_idx]['final_start']
                final_positions = range(final_start, final_start + 4)
                player = self._state.list_player[player_idx]
                if not all(marble.pos in final_positions for marble in player.list_marble):
                    team_wins = False
                    break

            if team_wins:
                # Update game phase and print winner
                self._state.phase = GamePhase.FINISHED
                print(f"Team {team_id + 1} has won the game!")
                return True

        return False

    # TODO LATIN-27
    def apply_action(self, action: Action) -> None:
        if action == None:
            return
        """ Apply the given action to the game """
        active_player = self._state.list_player[self._state.idx_player_active]

        if action.card in active_player.list_card:
            # removing card from players hand and putting it to discarded stack
            active_player.list_card.remove(action.card)
            self._state.list_card_discard.append(action.card)
            marble_to_move = next(
                (marble for marble in active_player.list_marble if int(
                    marble.pos) == int(action.pos_from)),
                None
            )
            self._move_marble_logic(marble_to_move, action.pos_to, action.card)
            # Check if the game is finished
            if self._check_finish_game():
                return  # Exit if the game is finished
            # TODO LATIN -46 check for collision
            # if self._is_collision :
            # self.handle_collision(....)
            # TODO Add more logic for other actions like sending marble home
            # TODO LATIN -42 logic for check if game is over (define winners)

        # calculate the next player (after 4, comes 1 again). not sure if needed here or somewhere else
        # example: (4+1)%4=1 -> after player 4, it's player 1's turn again
        self._state.idx_player_active = (
                                                self._state.idx_player_active + 1) % self._state.cnt_player

    def _move_marble_logic(self, marble: Marble, pos_to: int, card: Card) -> None:
        """
        Core logic for moving a marble to a new position.
        """
        pos_from = int(marble.pos)
        pos_to = int(pos_to)  # Ensure the target position is an integer

        # Handle overtaking logic
        self._handle_overtaking(marble, pos_from, pos_to, card)

        # Update marble position
        marble.pos = pos_to

    # Def is_collision()
    # self._handle_collision(marble, pos_to) #TODO LATIN -45 create handle collision
    def _is_collision(self, marble: Marble, pos_to: int, card: Card) -> bool:
        """
        Check if the movement of the marble using the card results in a collision.

        Args:
            marble (Marble): The marble being moved.
            pos_to (int): The target position.
            card (Card): The card being played.

        Returns:
            bool: True if the marble jumps over another marble, False otherwise.
        """
        pos_from = int(marble.pos)
        total_steps = self.TOTAL_STEPS
        marble_positions = {int(m.pos) for player in self._state.list_player for m in player.list_marble}

        # Exclude the active player's marbles from the collision check for the start marble
        active_player = self._state.list_player[self._state.idx_player_active]
        active_player_marbles = {int(m.pos) for m in active_player.list_marble}

        # If the marble is moving to a position occupied by its own start, do not count as a collision
        if pos_to in active_player_marbles and pos_to != marble.pos:
            return True

        if card.rank == '7':
            # Simulate all positions between pos_from and pos_to
            steps = abs(pos_to - pos_from)
            for step in range(1, steps + 1):
                intermediate_pos = (pos_from + step) % total_steps
                if intermediate_pos in marble_positions and intermediate_pos not in active_player_marbles:
                    return True

        elif card.rank == '4':
            # Similar logic, but account for reverse movement
            if pos_to < pos_from:  # Handling wrap-around
                pos_range = list(range(pos_from, total_steps)) + list(range(0, pos_to + 1))
            else:
                pos_range = list(range(pos_from, pos_to + 1))

            for pos in pos_range:
                if pos in marble_positions and pos not in active_player_marbles:
                    return True

        # Add additional checks for other cards with collision logic
        return False

    def _handle_overtaking(self, marble: Marble, pos_from: int, pos_to: int, card: Card) -> None:
        # Handle the logic for overtaking marbles during a move.

        total_steps = self.TOTAL_STEPS  # Total positions on the board
        marble_positions = {
            int(m.pos): m
            for player in self._state.list_player
            for m in player.list_marble
        }
        active_player = self._state.list_player[self._state.idx_player_active]
        active_player_positions = {int(m.pos) for m in active_player.list_marble}

        overtaken_marbles = set()

        # Check the range of positions between pos_from and pos_to
        if pos_to > pos_from:
            path = range(pos_from + 1, pos_to + 1)  # Regular forward movement
        else:
            path = list(range(pos_from + 1, total_steps)) + list(range(0, pos_to + 1))  # Wrap-around movement

        for step in path:
            position = step % total_steps
            if position in marble_positions and position not in active_player_positions:
                overtaken_marbles.add(marble_positions[position])

        # Handle overtaken marbles based on card rules
        if card.rank == '7':  # Special SEVEN card handling
            for overtaken_marble in overtaken_marbles:
                self._reset_marble_to_kennel(overtaken_marble)
        else:
            # For other cards, overtaking may not require special handling
            pass

    def _reset_marble_to_kennel(self, marble: Marble) -> None:
        marble.pos = marble.start_pos  # Reset to its starting position
        marble.in_kennel = True

    # TODO LATIN-28 check if logic is actually what we need it to be

    def get_player_view(self, idx_player: int) -> GameState:
        """ Get the masked state for the active player (e.g. the opponent's cards are face down) """
        masked_state: GameState = self._state.copy()
        for i, player in enumerate(masked_state.list_player):
            if i != idx_player:
                player.list_card = [
                                       Card(suit='?', rank='?')] * len(player.list_card)
        return masked_state

    ##################################################### PRIVATE METHODS #############################################

    # TODO in case the way is blocked (marble on 0/16/32/48 of the player with correct index?). LATIN-36
    def _is_way_blocked(self, pos_to: int, pos_from: int, safe_marbles: List[Marble]) -> bool:
        """ Check if the way is blocked between from  & to by any safe marble
        - If a marble is in the way: return True
        - If no marble is in the way: return False"""

        # Identify the "safe" positions (0, 16, 32, 48)
        safe_positions = [0, 16, 32, 48]  # Marbles are protected and can't be passed by others

        # Adjust pos_to for circular board wrapping
        total_steps = self.TOTAL_STEPS  # Board has 64 total steps (0–63)
        if pos_to < pos_from:
            pos_to += total_steps  # Adjust pos_to if it wraps around the board

        # Loop through each safe marble
        for marble in safe_marbles:  # Loops through all the marbles that are currently on the safe spots
            marble_pos = marble.pos
            if marble_pos in safe_positions:
                # Normalize marble_pos to match the current path calculation
                if marble_pos < pos_from:
                    marble_pos += total_steps

                # Check if the marble is blocking the path
                if pos_from < marble_pos <= pos_to:
                    return True  # Path is blocked by a safe marble

        return False  # No safe marble is blocking the path

    # TODO complete method LATIN-34
    def _calculate_position_to(self, pos_from: int, card: Card, active_player_indx: int) -> List[int]:
        """ Calculate the final possible_positions based on the card """

        active_player_fields = self.PLAYER_POSITIONS[active_player_indx]
        start = active_player_fields['start']
        queue_start = active_player_fields['queue_start']
        final_start = active_player_fields['final_start']
        possible_positions = []

        if card.rank.isdigit() and card.rank not in ['7', '4']:
            # Calculate next position
            next_position = (pos_from + int(card.rank)) % self.TOTAL_STEPS

            # Checking if the player is crossing his "start"
            if pos_from < queue_start and next_position >= queue_start:
                next_position = final_start + (next_position - queue_start) - 1

            possible_positions.append(next_position)

        elif card.rank == '4':
            # TODO refactor this logic. deals just as an example (it works probably, but still, refactor it maybe)

            # Calculate next position
            next_position = (pos_from + 4) % self.TOTAL_STEPS

            # Checking if the player is crossing his "start"
            if pos_from < queue_start and next_position >= queue_start:
                next_position = final_start + (next_position - queue_start) - 1

            possible_positions.append(next_position)

            # separator of logic for +4 & -4

            # Calculate next position
            if pos_from == 0:
                next_position = self.TOTAL_STEPS - 4
            else:
                next_position = (pos_from - 4) % self.TOTAL_STEPS

            # Checking if the player is crossing his "start"
            if pos_from < queue_start and next_position >= queue_start:
                next_position = final_start + (next_position - queue_start) - 1

            possible_positions.append(next_position)

        elif card.rank == '7':
            # TODO add logic
            # remember that if you overtake with this card, the marble which was overtaken will be sent back to kennel.
            # even your own marbles?
            # cannot overtake blocked fields
            pass

        elif card.rank == 'J':
            # TODO add logic
            pass

        # TODO Add more logic for other special cards (K, A, Joker)

        return possible_positions

    # TODO LATIN-41
    def _get_all_safe_marbles(self) -> List[Marble]:
        # use marble.is_save

        pass

    def deal_cards(self):
        for player in self._state.list_player:
            round_mod = self._state.cnt_round % 10
            if round_mod == 0:
                cards_to_deal = 2
            elif round_mod <= 5:
                cards_to_deal = 7 - round_mod
            else:
                cards_to_deal = 12 - round_mod
            for _ in range(cards_to_deal):
                card = self._state.list_card_draw.pop()
                player.list_card.append(card)

    def _set_marbles(self):
        for player_index in range(len(self._state.list_player)):
            for marble_index in range(4):
                self._state.list_player[player_index].list_marble.append(
                    Marble(
                        pos=str(
                            int(self.PLAYER_POSITIONS[player_index]['queue_start'] + marble_index)),
                        is_save=True)
                )


class RealPlayer(Player):

    def select_action(self, state: GameState, actions: List[GameAction]) -> GameAction:
        # TODO LATIN-33
        """ Given masked game state and possible actions, select the next action """
        pass


class RandomPlayer(Player):

    def select_action(self, state: GameState, actions: List[Action]) -> Optional[Action]:
        """ Given masked game state and possible actions, select the next action """
        if len(actions) > 0:
            return random.choice(actions)
        return None


if __name__ == '__main__':
    game = Dog()
    player = RealPlayer()

    while game.get_state() != GamePhase.FINISHED:
        active_players = 4
        game.deal_cards()
        while not active_players == 0:
            list_actions = game.get_list_action()

            if len(list_actions) == 0:
                active_players = active_players - 1
                print("Player has no actions left. Please wait until the round is over")
            else:
                action = player.select_action(game.get_state(), list_actions)
                game.apply_action(action)
                game.print_state()

        print(
            f"\n --------------- ROUND {game.get_state().cnt_round} finished -----------------")
