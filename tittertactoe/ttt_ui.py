#!/usr/bin/env python2

import Tkinter as tk
# themed tk
import ttk
import tkFont
import ttt

WIDTH = 750
HEIGHT = 800

PLAYER_LABELS = {ttt.BSTATES['P1']:'X',
                 ttt.BSTATES['P2']:'O',
                 ttt.BSTATES['EMPTY']:''}

class TkTictactoe(ttk.Frame):

    def __init__(self, master = None):
        ttk.Frame.__init__(self, master, width=WIDTH, height=HEIGHT)

        self.game = ttt.TicTacToeGame()
        # the user of this UI. ASSUMPTIONS: user is always P2 and P1 is
        # always the first player
        # Human moves second
        self.THISPLAYER = self.game.current_player * -1

        # don't shrink the frame to its content
        self.grid_propagate(False)

        # draw the frame (and its content); make all the edges of the frame
        # stick to the edges of the root window
        self.grid(sticky=tk.NSEW)
        # All the board buttons should expand if the main window is resized
        # We achieve this by giving w/h of the cells on the diagonal the same
        # "expansion" weight
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)
        self.place_widgets()

        self.record_computer_move()


    def place_widgets(self):
        # game buttons
        self.board = [[tk.Button(self, font=tkFont.Font(size=60), fg='black')
                       for i in range(3)] for i in range(3)]
        for rownum, row in enumerate(self.board):
            for colnum, button in enumerate(row):
                name = str(rownum) + ',' + str(colnum)
                button.grid(column=colnum, row=rownum, sticky=tk.NSEW)
                button.bind("<Button-1>", self.record_move)

        # menu
        self.quit_btn = ttk.Button(self, text='Exit', command=self.quit)
        self.quit_btn.grid(column=2, row=4, pady=10)
        self.newgame_btn = ttk.Button(self, text='New Game',
                                      command=self.start_new_game)
        self.newgame_btn.grid(column=2, row=3, pady=10)

        # status
        self.glostlbl = ttk.Label(self, text="Games Lost: 0")
        self.glostlbl.grid(column=1, row=3)
        self.gwonlbl = ttk.Label(self, text="Games Won: 0")
        self.gwonlbl.grid(column=0, row=3)

    def record_move(self, event):
        ''' process human move '''
        if not self.game.is_over():
            if event.widget['text'] == '':
                P = self.THISPLAYER
                player_repr = PLAYER_LABELS[P]
                self.game.make_move(P, self.find_button_coords(event.widget))
                event.widget['text'] = player_repr
                # check for game over each time make_move is called
                if self.game.is_over():
                    self.cleanup()
                self.record_computer_move()

    def record_computer_move(self):
        ''' process move generated by super fancy game ai'''
        if not self.game.is_over():
            PLAYER = self.THISPLAYER * -1
            player_repr = PLAYER_LABELS[PLAYER]
            (row, col) = self.game.make_minimax_move(PLAYER)
            self.board[row][col]['text'] = player_repr
            # check for game over each time make_move is called
            if self.game.is_over():
                self.cleanup()


    def cleanup(self):
        ''' update/reset after finished game '''
        mode = self.game.mode
        if mode == ttt.GSTATES['P2WON']:
            self.update_status_lbl(self.gwonlbl,
                                   self.game.wins[self.THISPLAYER])
        elif mode == ttt.GSTATES['P1WON']:
            self.update_status_lbl(self.glostlbl,
                                   self.game.losses[self.THISPLAYER])
        if mode < 2: # X won or O won
            for (row,col) in self.game.lastwincoords:
                self.board[row][col].configure(fg="red")

    def start_new_game(self):
        PLAYER = self.THISPLAYER
        self.game.reset(PLAYER)
        self.update_status_lbl(self.glostlbl, self.game.losses[PLAYER])
        # reset the buttons
        for row in self.board:
            for b in row:
                b['text'] = ''
                b['fg'] = 'black'
        self.record_computer_move()


    def update_status_lbl(self, label, newcount):
        ltext = label['text']
        label['text'] = (ltext[:ltext.rindex(':') + 1] + " " +
                        str(newcount))

    def find_button_coords(self, button):
        # This sucks. I don't know how to associate a button with an id in tk
        # but it seems impossible
        for r,row in enumerate(self.board):
            for c,b in enumerate(row):
                if b is button:
                    return (r,c)

        raise Exception("Button not found!")


def main():
    root = tk.Tk()
    # the window content should expand if the main window is resized
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    gameframe = TkTictactoe(master = root)

    root.title("Tic Tac Toe!")
    root.mainloop()

if __name__ == "__main__":
    main()


