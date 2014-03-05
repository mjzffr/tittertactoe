#!/usr/bin/env python2

import Tkinter as tk
# themed tk
import ttk
import tkFont
import ttt

WIDTH = 750
HEIGHT = 800
PLAYER_LABELS = {1:'X', -1:'O', 0:''}

''' This GUI uses game logic in ttt directly; no networking involved'''        

# TODO: need to schedule events in the Tkinter main loop, call after()

class TkTictactoe(ttk.Frame):

    def __init__(self, master = None):
        ttk.Frame.__init__(self, master, width=WIDTH, height=HEIGHT)
        
        self.game = ttt.TicTacToeGame()
        self.gameswon = 0
        self.gameslost = 0

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
        

    def place_widgets(self):
        # game buttons
        self.board = [[tk.Button(self, font=tkFont.Font(size=60))  
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
        
    def quit(self):
        # TODO: disconnect
        self.master.quit()

    def record_move(self, event):
        #if self.game.mode != ttt.GSTATES.mode('In_Progress'):
        if not self.game.is_over():
            if event.widget['text'] == '':
                player = self.game.current_player
                player_repr = PLAYER_LABELS[player]
                self.game.make_move(player, self.find_button_coords(event.widget))
                event.widget['text'] = player_repr
                # computer responds to the above human move
                self.record_computer_move()
        else:
            self.cleanup()
            

    def record_computer_move(self):
        if not self.game.is_over():
            player = self.game.current_player
            player_repr = PLAYER_LABELS[player]
            (row, col) = self.game.make_random_move(player)
            self.board[row][col]['text'] = player_repr
        else:
            self.cleanup()

    
    def cleanup(self):   
        print 'Done' 

    def start_new_game(self):
        if self.game.mode == ttt.GSTATES['In_Progress']:
            self.gameslost += 1 
            losttext = self.glostlbl['text']
            self.glostlbl['text'] = (losttext[:losttext.rindex(':') + 1] +
                str(self.gameslost))
        self.game = ttt.TicTacToeGame()
        for row in self.board:
            for b in row:  
                b['text'] = ''

    
    def find_button_coords(self, button):
        # This sucks. I don't know how to associate a button with an id in tk
        # but it seems impossible
        for r,row in enumerate(self.board):
            for c,b in enumerate(row):
                if b is button:
                    return (r,c)

        raise Exception("Button not found!")
    

# puts the Tktictactoe frame in main root window
if __name__ == "__main__":
    root = tk.Tk()
    # the window content should expand if the main window is resized
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    gameframe = TkTictactoe(master = root)

    root.title("Tic Tac Toe!")
    root.mainloop()
    


    
