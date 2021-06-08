# Author: Justin Canzonetta
# Date: 5/20/2021
# Description:  Implementation of the game "Kuba". Kuba is won by either capturing 7 of the neutral red
#               marbles or by blocking your oppoenent from any remaining moves. The board can be
#               displayed in the console for debug purposes.

from copy import deepcopy


class KubaGame:
    '''
    Represents the game "Kuba".

    Responsible for:
        - Initializing the game board per the game rules and storing two Player objects.
        - Keeping track of whose turn it is and returning the player name if requested.
        - Determing the validity of a game move and updating the game state/game board as the rules
        dictate.
        - Determing and returning the winner of the game.
        - Returning the number of marbles captured by the specified player.
        - Returning the color of a marble at specified coordinates.
        - Returning the total number of all colored marbles on the game board.
        - Displaying the board in the console.

    Class Dependencies: 
        - Player: used to track the number of red marbles per player
    '''

    def __init__(self, player1, player2):
        '''
        Initializes the KubaGame with two specified players. Both players are passed as tuples
        of length two with the first value the player name and the second the color
        represented as either "W" or "B".

        The board is initialized per the game rules with R (red), B (black), and W (white) representing
        the different colored marbles and X for empty spots on the board.
        '''

        self._players = {player1[0]: Player(
            player1), player2[0]: Player(player2)}
        self._game_winner = None
        self._current_turn = None

        # Initialize board with all X.
        self._game_board = [["X"] * 7 for i in range(7)]

        # Add white squares.
        for i in range(2):
            for j in range(2):
                self._game_board[i][j] = "W"
                self._game_board[6-i][6-j] = "W"

        # Add black squares.
        for i in range(2):
            for j in range(2):
                self._game_board[i+5][j] = "B"
                self._game_board[i][j+5] = "B"

        # Add red squares.
        red_coordinates = [(1, 3), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2),
                           (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 4), (5, 3)]

        for marble in red_coordinates:
            self._game_board[marble[0]][marble[1]] = "R"

    def display_board(self):
        '''
        Displays the game board in a console friendly format for debugging purposes.

        Also includes basic information of the game state.
        '''

        print()
        print("Captured Red Marbles")

        for player in self._players:
            print(player + ": " +
                  str(self._players[player].get_captured_red_marbles()))

        print()
        print("Number of Marbles on Board")

        color_tuple = ("White: ", "Black: ", "Red:   ")
        counter = 0
        for color in self.get_marble_count():
            print(color_tuple[counter] + str(color))
            counter += 1
        print()
        try:
            print("Current Turn: " + self._current_turn)
        except TypeError:
            print("Anyone's turn.")
        print()
        print("-----------------")
        for row in self._game_board:

            print("|", end=" ")

            for marble in row:
                print(marble, end=" ")
            print("|")
        print("-----------------")
        print()

    def get_current_turn(self):
        '''
        Returns the player name whose turn it is to play the game. If the game hasn't started yet,
        None is returned.
        '''

        return self._current_turn

    def make_move(self, playername, coordinates, direction):
        '''
        Takes the specified player name as a string, the coordinates as a tuple of the marble
        that is being pushed, and the direction to push as a string ('L' is left, 'R' is
        right, 'F' is forward, and 'B' is back.)

        If the move is valid, the game board is updated to reflect the move. If a red marbles is
        captured, the player's captured_red_marbles is incremented by 1. If the move wins the game, the
        the internal self._game_winner variable is updated accordingly.

        If for any reason the move is not valid, False is returned, otherwise True.
        '''

        if self._validate_move(playername, coordinates, direction):

            self._move_marble(playername, coordinates, direction, None)

            # Update current turn.
            self._current_turn = self._get_other_playername(playername)

            if self._check_for_winner(playername):
                self._game_winner = playername

            return True
        else:
            return False

    def _get_other_playername(self, playername):
        '''
        Takes a player name as a parameter and returns the name of the other player.
        '''

        for key in self._players:
            if key != playername:
                return key

    def _check_for_winner(self, playername):
        '''
        Takes a player name and returns True if the specified player meets a win condition and False
        otherwise.

        Win conditions are:
            - The player has captured 7 red marbles.
            - The other player has no more of their own marbles on the board.
            - The other players marbles are boxed in.
        '''

        # Check if this player just won with 7 marbles.
        if self._players[playername].get_captured_red_marbles() > 6:
            return True

        # Check if the other player has 0 marbles.
        if self._players[playername].get_color() == "B":
            if self.get_marble_count()[0] < 1:
                return True
        else:
            if self.get_marble_count()[1] < 1:
                return True

        # If the next player has no valid moves, the recent player is declared the winner. (optional)
        if self._check_all_moves_blocked(playername):
            return True

        return False

    def _check_all_moves_blocked(self, playername):
        '''
        Takes a player name and checks if the opposing player has any valid moves left. If all moves are
        blocked, True is returned. False is returned otherwise.
        '''

        possible_directions = ('F', 'B', 'L', 'R')

        playername = self._get_other_playername(playername)
        marble_color = self._players[playername].get_color()

        for i, row in enumerate(self._game_board):
            for j, marble in enumerate(row):
                if self._game_board[i][j] == marble_color:
                    for direction in possible_directions:
                        if self._validate_move(playername, (i, j), direction):
                            return False

        return True

    def _validate_move(self, playername, coordinates, direction):
        '''
        Takes the specified player name as a string, the coordinates as a tuple of the marble
        that is being pushed, and the direction to push as a string ('L' is left, 'R' is
        right, 'F' is forward, and 'B' is back.)

        If the move is valid, True is returned.

        False is returned if any of the following conditions are met:
            - It is not the specified player's turn.
            - If there is already a winner.
            - If the color of the marble at the specified coordinate is not the color for the specified
            player.
            - If the marble is not 'open' to be pushed.
            - If the Ko rule is violated.
            - If the move would push the own player's marble off the board.
        '''

        # Check if it's the player's turn.
        if not (playername == self._current_turn or self._current_turn is None):
            #print("not the player's turn")
            return False

        # Check if there's a winner.
        if self._game_winner is not None:
            #print("there is already a winner")
            return False

        # Check that the color of the selected marble is the player's chosen color.
        if self._players[playername].get_color() != self.get_marble(coordinates):
            #print("the selected marble is not the player's marble")
            return False

        # Check that the marble to be moved is 'open'.
        if not self._check_open_marble(coordinates, direction):
            #print("the marble isn't open")
            return False

        # Check that the Ko rule isn't violated.
        if not self._check_ko_rule(coordinates, direction):
            #print("the ko rule is violated")
            return False

        # Check if the move will knock off the player's own marble.
        if not self._check_selfdefeating_rule(playername, coordinates, direction):
            #print("that move will knock the own player's marble off")
            return False

        return True

    def _check_open_marble(self, coordinates, direction):
        '''
        Takes the coordinates as a tuple of the marble that is being pushed, and the direction to push as a string ('L' is left, 'R' is
        right, 'F' is forward, and 'B' is back.)

        If the marble is 'open' and can be pushed, True is returned, otherwise False is returned.
        '''

        if direction == "F":
            blocking_spot = (coordinates[0] + 1, coordinates[1])
        elif direction == "B":
            blocking_spot = (coordinates[0] - 1, coordinates[1])
        elif direction == "L":
            blocking_spot = (coordinates[0], coordinates[1] + 1)
        elif direction == "R":
            blocking_spot = (coordinates[0], coordinates[1] - 1)

        for index in blocking_spot:
            if index < 0 or index > 6:
                return True

        if self.get_marble(blocking_spot) == "X":
            return True
        else:
            return False

    def _check_ko_rule(self, coordinates, direction):
        '''
        Takes the coordinates as a tuple of the marble that is being pushed, and the direction to push as a string ('L' is left, 'R' is
        right, 'F' is forward, and 'B' is back.)

        If the Ko rule is not violated, True is returned, otherwise False is returned.
        '''

        previous_board = deepcopy(self._game_board)

        previous_board = self._move_marble(
            None, coordinates, direction, previous_board)

        row_index = 0
        for row in previous_board:

            col_index = 0
            for marble in row:
                if marble != self.get_marble((row_index, col_index)):
                    return True
                col_index += 1
        row_index += 1

        return False

    def _move_marble(self, playername, coordinates, direction, board):
        '''
        Takes the specified player name as a string, the coordinates as a tuple of the marble
        that is being pushed, the direction to push as a string ('L' is left, 'R' is
        right, 'F' is forward, and 'B' is back.), and the board to make the move on.

        If board is passed as None, then the private _game_board is updated. If playername
        is not None, then any captured red marbles will appropriately increment for that player.

        Returns the board with the updated marble positions.
        '''

        if board is None:
            board = self._game_board

        row = coordinates[0]
        column = coordinates[1]
        current_marble = board[row][column]
        board[row][column] = "X"

        if direction == "F":

            while current_marble != "X":
                row -= 1

                previous_marble = current_marble
                current_marble = board[row][column]
                board[row][column] = previous_marble

                if row == 0 and current_marble != "X":
                    if current_marble == "R" and playername is not None:
                        self._players[playername].increment_captured_red_marbles()
                    current_marble = "X"

        elif direction == "B":
            while current_marble != "X":
                row += 1

                previous_marble = current_marble
                current_marble = board[row][column]
                board[row][column] = previous_marble

                if row == 6 and current_marble != "X":
                    if current_marble == "R" and playername is not None:
                        self._players[playername].increment_captured_red_marbles()
                    current_marble = "X"

        elif direction == "L":

            while current_marble != "X":
                column -= 1

                previous_marble = current_marble
                current_marble = board[row][column]
                board[row][column] = previous_marble

                if column == 0 and current_marble != "X":
                    if current_marble == "R" and playername is not None:
                        self._players[playername].increment_captured_red_marbles()
                    current_marble = "X"

        else:

            while current_marble != "X":
                column += 1

                previous_marble = current_marble
                current_marble = board[row][column]
                board[row][column] = previous_marble

                if column == 6 and current_marble != "X":
                    if current_marble == "R" and playername is not None:
                        self._players[playername].increment_captured_red_marbles()
                    current_marble = "X"

        return board

    def _check_selfdefeating_rule(self, playername, coordinates, direction):
        '''
        Takes the specified player name as a string, the coordinates as a tuple of the marble
        that is being pushed, and the direction to push as a string ('L' is left, 'R' is
        right, 'F' is forward, and 'B' is back.)

        Determines whether the move removes one of the player's own marbles from the board.

        Returns True if the rule is not violated and False otherwise.
        '''

        player_marble_color = self._players[playername].get_color()

        row = coordinates[0]
        column = coordinates[1]
        current_marble = self._game_board[row][column]

        if direction == "F":

            while current_marble != "X":
                row -= 1
                current_marble = self._game_board[row][column]

                if row == 0:
                    if current_marble == player_marble_color:
                        return False
                    else:
                        current_marble = "X"

        elif direction == "B":

            while current_marble != "X":
                row += 1
                current_marble = self._game_board[row][column]

                if row == 6:
                    if current_marble == player_marble_color:
                        return False
                    else:
                        current_marble = "X"

        elif direction == "L":

            while current_marble != "X":
                column -= 1
                current_marble = self._game_board[row][column]

                if column == 0:
                    if current_marble == player_marble_color:
                        return False
                    else:
                        current_marble = "X"

        else:

            while current_marble != "X":
                column += 1
                current_marble = self._game_board[row][column]

                if column == 6:
                    if current_marble == player_marble_color:
                        return False
                    else:
                        current_marble = "X"

        return True

    def get_winner(self):
        '''
        Returns the name of the winning player. If there is no winner yet, None is returned.
        '''

        return self._game_winner

    def get_captured(self, playername):
        '''
        Takes a player name and returns the number of Red marbles captured by the specified
        player.
        '''

        return self._players[playername].get_captured_red_marbles()

    def get_marble(self, coordinates):
        '''
        Takes coordinates as a tuple and returns the marble that is present at the specified location
        as R (red), B (black), and W (white). If there is no marble at the specified location, 'X" is
        returned.
        '''

        return self._game_board[coordinates[0]][coordinates[1]]

    def get_marble_count(self):
        '''
        Returns the number of White, Black, and Red marbles on the board as a tuple in the order (W,B,R).
        '''

        white = 0
        black = 0
        red = 0

        for row in self._game_board:
            for marble in row:
                if marble == "R":
                    red += 1
                elif marble == "B":
                    black += 1
                elif marble == "W":
                    white += 1

        return (white, black, red)


class Player:
    '''
    Represents a player in the game "Kuba".

    Responsible for:
        - Storing and returning the player's name, color, and the number of captured Red marbles.
        - Incrementing the number of captured Red marbles when a Red marble is captured by the player.

    While the class itself can operate with no dependencies, its functionality is centered around the
    KubaGame class.
    '''

    def __init__(self, player_tuple):
        '''
        Initializes a player by taking a tuple of length two with the first value the player name and the
        second the color represented as either "W" or "B".

        The number of captured red marbles is initially set to 0.
        '''

        self._name = player_tuple[0]
        self._color = player_tuple[1]
        self._captured_red_marbles = 0

    def get_name(self):
        '''
        Returns the name of the player.
        '''

        return self._name

    def get_color(self):
        '''
        Returns the color of the player's chosen marble.
        '''

        return self._color

    def increment_captured_red_marbles(self):
        '''
        Increments the number of Red marbles captured by the player by 1.
        '''

        self._captured_red_marbles += 1

    def get_captured_red_marbles(self):
        '''
        Returns the number of Red marbles captured by the player.
        '''

        return self._captured_red_marbles


def main():
    '''Main function which is called if the file is run as a script.'''

    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    game.display_board()


if __name__ == '__main__':
    main()
