#!/usr/bin/env python2
BSTATES = {'Empty':0, 'X':1, 'O':-1}
GSTATES = {'In_Progress':0, 'Not_Started':3, 'XWon':BSTATES['X'],
                        'OWon':BSTATES['O'], 'Draw':2}

class TicTacToeGame:

    # TODO: keep track of a whole session instead of a single game?
    #   how many times each player has won, etc.

    def __init__(self, size = 3, initial_state = None):
        # initial_state is used for testing
        self.SIZE = size
        self.board = [[BSTATES['Empty'] for i in range(self.SIZE)] \
                       for i in range(self.SIZE)]
        self.current_player = BSTATES['X']
        self.mode = GSTATES['Not_Started']
        if initial_state:
            self.board = initial_state


    def make_move(self, player, location):
        ''' player is 1 or -1 (for X or O)
            location is tuple of row,col coords
            returns the int mode that results after the move (see GSTATES)
        '''
        (row,col) = location
        # validate
        size = self.SIZE
        if player != self.current_player:
            msg = ("Invalid player " + str(player) + ". Should be " + 
                    str(self.current_player))
            raise ValueError(msg)
        if row not in range(size) or col not in range(size):
            raise ValueError("Invalid location value " + str(location))

        # update state
        if self.board[row][col] == BSTATES['Empty']:
            self.board[row][col] = player
            self.current_player *= -1
        else:
            raise ValueError("Location already full " + str(location))
        return self.update_mode();


    def update_mode(self):
        ''' determines whether game is over '''
        s = self.SIZE
        # TODO: could be way more efficient. Don't need to check until 5 moves
        # have been made
        for row in self.board:
            if TicTacToeGame.is_winning_line(row):
                return TicTacToeGame.winner_to_mode(row[0])
        for col in zip(*self.board):
            if TicTacToeGame.is_winning_line(col):
                return TicTacToeGame.winner_to_mode(col[0])
        diagonals = [[self.board[i][i] for i in range(s)], \
                     [self.board[s - 1 -i][i] for i in range(s)]]
        for l in diagonals:
            if TicTacToeGame.is_winning_line(l):
                return TicTacToeGame.winner_to_mode(l[0])
        #it's a draw
        if BSTATES['Empty'] not in [i for row in self.board for i in row]:
            return GSTATES['Draw']

        #otherwise
        return GSTATES['In_Progress']        

    @staticmethod
    def is_winning_line(line):
        ''' return true if line consists of all 'X' or 'O';
        line is a list of board spaces, like a row or a diagonal'''
        return BSTATES['Empty'] not in line and all(line[0] == i for i in \
                                                      line)

    @staticmethod
    def winner_to_mode(player):
        if player == BSTATES['X']:
            return GSTATES['XWon']
        else:
            return GSTATES['OWon']

    # assuming game loop is implemented by UI
    def play(self):
        while self.mode == GSTATES['In_Progress']:
            break
            #TODO

    def __str__(self):
        boardstr = ''
        for row in self.board:
            for i in row:
                if i == BSTATES['X']:
                    boardstr += 'X'
                elif i == BSTATES['O']:
                    boardstr += 'O'
                else:
                    boardstr += '_'
            boardstr += '\n'
        return boardstr


''' Terrible testing '''
def test_mode():
    game = TicTacToeGame(initial_state=[[0,0,0],[0,0,0],[0,0,0]]) 
    print game
    print game.update_mode()
    print
    game = TicTacToeGame(initial_state=[[1,1,-1],[-1,1,1],[1,-1,-1]]) 
    print game
    print game.update_mode()
    print
    game = TicTacToeGame(initial_state=[[1,0,0],[0,1,0],[0,1,0]]) 
    print game
    print game.update_mode()
    print
    game = TicTacToeGame(initial_state=[[1,0,0],[0,1,0],[0,0,1]]) 
    print game
    print game.update_mode()
    print
    game = TicTacToeGame(initial_state=[[-1,0,0],[-1,1,0],[-1,0,1]]) 
    print game
    print game.update_mode()
    print


def test_moves(game):
    print game.update_mode()
    print(game.make_move(1, (1,0)))
    print game
    print(game.make_move(-1, (0,2)))
    print game
    print(game.make_move(1, (0,1)))
    print game
    print(game.make_move(-1, (1,2)))
    print game
    print(game.make_move(1, (0,0)))
    print game
    print(game.make_move(-1, (2,2)))
    print game

if __name__ == "__main__":
    print 'BSTATES: ' + str(BSTATES)
    print 'GSTATES: ' + str(GSTATES)

    #Server().start_server()
    game = TicTacToeGame()
    game.make_random_move(BSTATES['X'])
    #test_mode()
