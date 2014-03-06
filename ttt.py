#!/usr/bin/env python2
import random

BSTATES = {'EMPTY':0, 'P1':1, 'P2':-1}
GSTATES = {'INPROGRESS':4, 'NOTSTARTED':3, 'P2WON':BSTATES['P1'],
                        'P1WON':BSTATES['P2'], 'DRAW':2}

class TicTacToeGame:

    # TODO: keep track of a whole session instead of a single game?
    #   how many times each player has won, etc.

    def __init__(self, size = 3, initial_state = None):
        # initial_state is used for testing
        self.SIZE = size
        self.board = [[BSTATES['EMPTY'] for i in range(self.SIZE)] \
                       for i in range(self.SIZE)]
        self.current_player = BSTATES['P1']
        self.mode = GSTATES['NOTSTARTED']
        self.lastwincoords = []
        if initial_state:
            self.board = initial_state

    def make_random_move(self, player):
        ''' player is 1 or -1 (for X or O)
            returns the location that was changed
        '''
        location = random.choice(self.get_locations(BSTATES['EMPTY']))
        return self.make_move(player, location)
        
    def get_locations(self, bstate):
        ''' returns list of (row, col) tuples '''
        board = self.board
        return [(ri,ci) for ri,row in 
                enumerate(board) for ci,spot in 
                enumerate(row) if spot == bstate]
 
    def is_over(self):
        #print "Check %s" % self.mode
        return self.mode <= 2
        #return self.mode in (GSTATES['XWon'], GSTATES['OWon'], GSTATES['Draw'])

    def make_move(self, player, location):
        ''' player is 1 or -1 (for X or O)
            location is tuple of row,col coords
            returns location that was changed
        '''
        (row, col) = location
        # validate
        size = self.SIZE
        if player != self.current_player:
            msg = ("Invalid player " + str(player) + ". Should be " + 
                    str(self.current_player))
            raise ValueError(msg)
        if row not in range(size) or col not in range(size):
            raise ValueError("Invalid location value " + str(location))

        # update state
        if self.board[row][col] == BSTATES['EMPTY']:
            self.board[row][col] = player
            self.current_player *= -1
        else:
            raise ValueError("Location already full " + str(location))
        
        self.update_mode()
        print(self)
        print
        #
        return location

    def update_mode(self):
        ''' determines whether game is over '''
        s = self.SIZE
        # TODO: could be way more efficient. Don't need to check until 5 moves
        # have been made
        for ri,row in enumerate(self.board):
            if TicTacToeGame.is_winning_line(row):
                self.mode = TicTacToeGame.winner_to_mode(row[0])
                self.lastwincoords = [(ri,i) for i in range(s)]
                return
        for ci,col in enumerate(zip(*self.board)):
            if TicTacToeGame.is_winning_line(col):
                self.mode = TicTacToeGame.winner_to_mode(col[0])
                self.lastwincoords = [(i,ci) for i in range(s)]
                return
        
        diagonal_coords = [[(i,i) for i in range(s)], 
            [(s-1-i, i) for i in range(s)]]
        diagonals = [[self.board[i][i] for i in range(s)], 
            [self.board[s-1-i][i] for i in range(s)]]
            
                     
        for i,l in enumerate(diagonals):
            if TicTacToeGame.is_winning_line(l):
                self.mode = TicTacToeGame.winner_to_mode(l[0])
                self.lastwincoords = diagonal_coords[i]
                return
        #it's a draw
        if BSTATES['EMPTY'] not in [i for row in self.board for i in row]:
            self.mode = GSTATES['DRAW']
            self.lastwincoords = []
            return

        #otherwise
        self.mode = GSTATES['INPROGRESS']        

    @staticmethod
    def is_winning_line(line):
        ''' return true if line consists of all 'X' or 'O';
        line is a list of board spaces, like a row or a diagonal'''
        return BSTATES['EMPTY'] not in line and all(line[0] == i for i in \
                                                      line)

    @staticmethod
    def winner_to_mode(player):
        if player == BSTATES['P1']:
            return GSTATES['P1WON']
        else:
            return GSTATES['P2WON']

    # assuming game loop is implemented by UI
    def play(self):
        while self.mode == GSTATES['INPROGRESS']:
            break
            #TODO

    def __str__(self):
        boardstr = ''
        for row in self.board:
            for i in row:
                if i == BSTATES['P1']:
                    boardstr += 'X'
                elif i == BSTATES['P2']:
                    boardstr += 'O'
                else:
                    boardstr += '_'
            boardstr += '\n'
        return boardstr


''' Terrible testing '''
def test_mode():
    game = TicTacToeGame(initial_state=[[0,0,0],[0,0,0],[0,0,0]]) 
    print game
    game.update_mode()
    print game.mode
    print game.lastwincoords
    print
    game = TicTacToeGame(initial_state=[[1,1,-1],[-1,1,1],[1,-1,-1]]) 
    print game
    game.update_mode()
    print game.mode
    print game.lastwincoords
    print
    game = TicTacToeGame(initial_state=[[1,0,0],[0,1,0],[0,1,0]]) 
    print game
    game.update_mode()
    print game.mode
    print game.lastwincoords
    print
    game = TicTacToeGame(initial_state=[[1,0,0],[0,1,0],[0,0,1]]) 
    print game
    game.update_mode()
    print game.mode
    print game.lastwincoords
    print
    game = TicTacToeGame(initial_state=[[-1,0,0],[-1,1,0],[-1,0,1]]) 
    print game
    game.update_mode()
    print game.mode
    print game.lastwincoords
    print
    game = TicTacToeGame(initial_state=[[-1,-1,-1],[1,1,0],[1,0,1]]) 
    print game
    game.update_mode()
    print game.mode
    print game.lastwincoords
    print
    game = TicTacToeGame(initial_state=[[1,0,1],[-1,1,0],[1,0,-1]]) 
    print game
    game.update_mode()
    print game.mode
    print game.lastwincoords
    print

def test_moves(game):
    game.update_mode()
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
    #game = TicTacToeGame()
    #game.make_random_move(BSTATES['P1'])
    test_mode()
