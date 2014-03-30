#!/usr/bin/env python2
import random
import copy

# suggestion: BSTATES and GSTATES moved into TicTacToeGame class or to
# their own class? or something?
BSTATES = {'EMPTY':0, 'P1':1, 'P2':-1}
# suggestion: use tuple of strings instead of dict
GSTATES = {'INPROGRESS':4, 'NOTSTARTED':3, 'P2WON':BSTATES['P2'],
                        'P1WON':BSTATES['P1'], 'DRAW':2}

class TicTacToeGame:

    def __init__(self, size=3, initial_state=None):
        self.SIZE = size
        self.board = [[BSTATES['EMPTY']] * self.SIZE for _ in range(self.SIZE)]

        self.current_player = BSTATES['P1']
        self.mode = GSTATES['NOTSTARTED']

        # TODO: feature addition: full game stats: draws, num games
        self.wins = {BSTATES['P1']:0, BSTATES['P2']:0}
        self.losses = {BSTATES['P1']:0, BSTATES['P2']:0}

        self.lastwincoords = set()

        # for testing
        if initial_state:
            self.board = initial_state

    def make_random_move(self, player):
        ''' player is 1 or -1 (for X or O)
            returns the location that was changed
        '''
        if self.is_over():
            raise Exception("No game in progress. Game over.")

        location = random.choice(TicTacToeGame.get_locations(self.board, BSTATES['EMPTY']))
        return self.make_move(player, location)

    def collect_values(self, player):
        def calc_value(player, lines):
            empty_weight = 0.5
            winning_weight = 999
            opponent_win_weight = 99
            value = 0
            for line in lines:
                linestates = self.get_board_states(line)
                num_empty = linestates.count(BSTATES['EMPTY'])
                num_opponent = linestates.count(player * -1)
                num_player = linestates.count(player)

                s = sum(linestates) * player
                if s == self.SIZE - 1:
                    # our winning spot
                    value += winning_weight
                elif s == -(self.SIZE - 1):
                    # opponent's winning spot
                    value += opponent_win_weight
                elif num_player > 0 and num_opponent > 0:
                    # mixed line
                    value = 0
                else:
                    value += num_empty * empty_weight + s
                    if num_player == 0 and num_opponent >= 1:
                        # blocking opponent
                        value += (empty_weight / 2 - s)
            return value

        values = [[0] * self.SIZE for _ in range(self.SIZE)]
        for ri, row in enumerate(values):
            for ci, item in enumerate(row):
                if self.board[ri][ci] != BSTATES['EMPTY']:
                    values[ri][ci] = 0
                else:
                    lines = []
                    if ri == ci:
                        lines.append(self.get_diagonal_left_coords())
                    if ri + ci == self.SIZE - 1:
                        lines.append(self.get_diagonal_right_coords())
                    lines.append(self.get_vertical_coords(ci))
                    lines.append(self.get_horizontal_coords(ri))

                    values[ri][ci] = calc_value(player, lines)

        print values
        return values

    def get_board_states(self, line):
        return [self.board[row][col] for (row, col) in line]

    def get_diagonal_left_coords(self):
        return [(i,i) for i in range(self.SIZE)]

    def get_diagonal_right_coords(self):
        return [(self.SIZE-1-i, i) for i in range(self.SIZE)]

    def get_vertical_coords(self, col_i):
        return [(i, col_i) for i in range(self.SIZE)]

    def get_horizontal_coords(self, row_i):
        return [(row_i, i) for i in range(self.SIZE)]


    def minimax_eval(self, player, possible_board):
          '''
          if game is over
             return 1, -1, 0
          '''
          # for ri,row in enumerate(self.board):
          #    for ci,bstate in enumerate(row):
          #        if bstate == BSTATES['EMPTY']:
          #            self.minimax_eval(player, possible_board)
          return 1

    def make_minimax_move(self, player):
        move_values = {}
        for ri,row in enumerate(self.board):
            for ci,bstate in enumerate(row):
                if bstate == BSTATES['EMPTY']:
                    possible_board = copy.deepcopy(self.board)
                    possible_board[ri][ci] = player
                    move_values[(ri, ci)] = self.minimax_eval(player, possible_board)

        #choose random key in dictionary that has max value
        maxval = max(move_values.values())
        maxlist = [i[0] for i in move_values.iteritems() if i[1] == maxval]

        return self.make_move(player, random.choice(maxlist))


    # TODO: during draw, this always tries to use (0,0) as last move
    #       File "tittertactoe/ttt.py", line 167, in make_move
    #     raise ValueError("Location already full " + str((row, col)))
    # ValueError: Location already full (0, 0)

    def make_smart_move(self, player):
        values = self.collect_values(player)
        max_val = -1
        (r, c) = (0, 0)
        for ri, row in enumerate(values):
            localmax = max(row)
            if localmax > max_val:
                max_val = localmax
                r = ri
                c = row.index(localmax) #random.choice([i for i,_ in enumerate(row) if value == max_val])

        return self.make_move(player, (r, c))

    @staticmethod
    def get_locations(board, bstate):
        ''' returns list of (row, col) tuples at which the board state is
         bstate '''
        return [(ri,ci) for ri,row in
                enumerate(board) for ci,spot in
                enumerate(row) if spot == bstate]

    def is_over(self):
        return self.mode <= 2


    def reset(self, player):
        if self.mode == GSTATES['INPROGRESS']:
            self.losses[player] += 1
            self.wins[player * -1] += 1
        self.board = [[BSTATES['EMPTY'] for i in range(self.SIZE)] \
                   for i in range(self.SIZE)]
        self.current_player = BSTATES['P1']
        self.mode = GSTATES['NOTSTARTED']

    def make_move(self, player, (row,col)):
        ''' player is 1 or -1 (for X or O)
            returns location that was changed
        '''
        if self.is_over():
            raise Exception("No game in progress. Game over.")

        # validate
        size = self.SIZE
        if player != self.current_player:
            msg = ("Invalid player " + str(player) + ". Should be " +
                    str(self.current_player))
            raise ValueError(msg)
        if row not in range(size) or col not in range(size):
            raise ValueError("Invalid location value " + str((row, col)))

        # update state
        if self.board[row][col] == BSTATES['EMPTY']:
            self.board[row][col] = player
            self.update_mode()
            if self.mode == GSTATES['INPROGRESS']:
                # only switch turns if most recent move did not end the game
                self.current_player *= -1
        else:
            raise ValueError("Location already full " + str((row, col)))

        print self

        return (row, col)

    def update_points(self):
        if self.mode == GSTATES['P1WON']:
            self.wins[BSTATES['P1']] += 1
            self.losses[BSTATES['P2']] += 1
        elif self.mode == GSTATES['P2WON']:
            self.wins[BSTATES['P2']] += 1
            self.losses[BSTATES['P1']] += 1

    @property
    def board_1d(self):
        return [i for row in self.board for i in row]

        #rewrite to fix the repeated return statements
    def update_mode(self):
        ''' determines whether game is over '''
        s = self.SIZE

        # don't check until one player has made > size moves
        if self.board_1d.count(BSTATES['EMPTY']) > s ** 2 - (s * 2 - 1):
            self.mode = GSTATES['INPROGRESS']
            return

        self.mode, resultcoords = \
            TicTacToeGame.calc_game_status(self.board)
        self.update_points()

        # <= 2 means draw, xwon or owon
        if self.mode <= 2:
            self.lastwincoords = resultcoords

    @staticmethod
    def is_winning_line(line):
        ''' return true if line consists of all 'X' or 'O';
        line is a list of board space states, like a row or a diagonal'''
        return BSTATES['EMPTY'] not in line and all(line[0] == i for i in \
                                                      line)
    @staticmethod
    def calc_game_status(board):
        ''' return pair of gstate and set of winning line coords if there is one
        Assuming board is square!'''
        s = len(board)

        for ri,rowvals in enumerate(board):
            if TicTacToeGame.is_winning_line(rowvals):
                return (rowvals[0], set([(ri,i) for i in range(s)]))
        for ci,colvals in enumerate(zip(*board)):
            if TicTacToeGame.is_winning_line(colvals):
                return (colvals[0], set([(i,ci) for i in range(s)]))

        diagonal_coords = [[(i,i) for i in range(s)],
            [(s - 1 - i, i) for i in range(s)]]
        diagonals = [[board[i][i] for i in range(s)],
            [board[s - 1 - i][i] for i in range(s)]]

        for i,diagvals in enumerate(diagonals):
            if TicTacToeGame.is_winning_line(diagvals):
                return (diagvals[0], set(diagonal_coords[i]))

        #it's a draw
        board_1d = [i for row in board for i in row]
        if BSTATES['EMPTY'] not in board_1d:
            return (GSTATES['DRAW'], set())

        #otherwise
        return (GSTATES['INPROGRESS'], set())


    # assuming game loop is implemented by UI
    def play(self):
        while self.mode == GSTATES['INPROGRESS']:
            break
            #TODO

    # for testing
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

if __name__ == '__main__':
    g = TicTacToeGame(initial_state=[[0,0,0],[0,0,0],[1,0,0]])
    print g.collect_values(-1)


'''
Player = 1
[[0,0,0],[0,0,0],[0,0,0]] -->
[[4.5, 3.0, 4.5], [3.0, 6.0, 3.0], [4.5, 3.0, 4.5]]

[[1,0,-1],[0,0,0],[1,0,-1]] -->
[[-1, 2.0, -1], [1000.5, 4.0, 100.5], [-1, 2.0, -1]]

[[1,0,0],[0,0,0],[0,0,-1]]

'''
