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

        self._players = (player1: Player(player1), player2: Player(player2))
        self._game_winner = None
        self._current_turn = None

        # Initialize board with all X.
        self._board = [["X"] * 7 for i in range(7)]

        # Add white squares.
        for i in range(2):
            for j in range(2):
                self._board[i][j] = "W"
                self._board[6-i][6-j] = "W"

        # Add black squares.
        for i in range(2):
            for j in range(2):
                self._board[i+5][j] = "B"
                self._board[i][j+5] = "B"

        # Add red squares.
        red_coordinates = [(1, 3), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2),
                           (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 4), (5, 3)]

        for marble in red_coordinates:
            self._board[marble[0]][marble[1]] = "R"

    def display_board(self):
        '''
        Displays the game board in a console friendly format for debugging purposes.

        Also includes basic information of the game state.
        '''
        for row in self._board:
            print(row)

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

        pass

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
        if playername != self._current_turn:
            return False
        
        # Check if there's a winner.
        if self._game_winner is not None:
            return False
        
        # Check that the color of the selected marble is the player's chosen color.
        if self._players[playername].get_color() != self.get_marble(coordinates):
            return False
        
        # Check that the marble to be moved is 'open'.
        if not self._check_open_marble(coordinates, direction):
            return False
        
        # Check that the Ko rule isn't violated.
        if not self._check_ko_rule(coordinates, direction):
            return False

        # Check if the move will knock off the player's own marble.
        if not self._check_selfdefeating_rule(playername, coordinates, direction):
            return False
        
        return True

    def _check_open_marble(self, coordinates, direction):
        '''
        Takes the coordinates as a tuple of the marble that is being pushed, and the direction to push as a string ('L' is left, 'R' is
        right, 'F' is forward, and 'B' is back.)

        If the marble is 'open' and can be pushed, True is returned, otherwise False is returned.
        '''

        if direction == "F":
            try:
                blocking_spot = (coordinates[0] + 1, coordinates[1])
            except IndexError:
                return True
        elif direction == "B":
            try:
                blocking_spot = (coordinates[0] - 1, coordinates[1])
            except IndexError:
                return True
        elif direction == "L":
            try:
                blocking_spot = (coordinates[0], coordinates[1] + 1)
            except IndexError:
                return True
        else:
            try:
                blocking_spot = (coordinates[0], coordinates[1] - 1)
            except IndexError:
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

        previous_board = deepcopy(self._board)

        # Under Construction

    def _check_selfdefeating_rule(self, playername, coordinates, direction):
        '''
        Takes the specified player name as a string, the coordinates as a tuple of the marble
        that is being pushed, and the direction to push as a string ('L' is left, 'R' is
        right, 'F' is forward, and 'B' is back.)

        Determines whether the move removes one of the player's own marbles from the board.

        Returns True if the rule is not violated and False otherwise.
        '''

        last_marble_index = None

        if direction == "F":
            
            row = coordinates[0]
            current_marble = self.get_marble(coordinates)
            
            while current_marble != "X" and row > 0:
                row -= 1
                current_marble = self.get_marble((row, coordinates[1]))

            if row

        elif direction == "B":
            
        elif direction == "L":
            
        else:
            


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
        
        return self._board[coordinates[0], coordinates[1]]

    def get_marble_count(self):
        '''
        Returns the number of White, Black, and Red marbles on the board as a tuple in the order (W,B,R).
        '''
        
        white = 0
        black = 0
        red = 0

        for row in self._board:
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
