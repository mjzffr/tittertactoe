#!/usr/bin/env python2

import Tkinter as tk
# themed tk
import ttk
import tkFont

WIDTH = 750
HEIGHT = 800

# Abort second window
# players assigned X or O autormatically upon connecting
# Widgets: "Join game" [For now, always two humans: "Human or Computer?"]
# class TkWelcome(ttk.Frame):
#     def __init__(self, master = None):
#         ttk.Frame.__init__(self, master, width=WIDTH, height=HEIGHT)
#         # don't shrink the frame to its content
#         self.grid_propagate(False)
#         # draw the frame (and its content); make all the edges of the frame
#         # stick to the edges of the root window
#         self.grid(sticky=tk.NSEW)
#         self.text = tk.Text(self)
#         self.text.grid(column=0,row=0)
#         self.text.insert('5.0', 'text ttexta;lkad;')
        


class TkTictactoe(ttk.Frame):

    def __init__(self, master = None):
        ttk.Frame.__init__(self, master, width=WIDTH, height=HEIGHT)
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
        self.board = [[tk.Button(self, font=tkFont.Font(size=60)) \
                       for i in range(3)] for i in range(3)]
        for rownum, row in enumerate(self.board):
            for colnum, button in enumerate(row):
                button.grid(column=colnum, row=rownum, sticky=tk.NSEW)
                button.bind("<Button-1>", self.record_move)
        # menu
        self.quit_btn = ttk.Button(self, text='Exit', command=self.quit)
        self.quit_btn.grid(column=2, row=4, pady=10)
        self.newgame_btn = ttk.Button(self, text='New Game', 
                                      command=self.start_new_game)
        self.newgame_btn.grid(column=2, row=3, pady=10)

        # status
        ttk.Label(self, text="Games Won: 0").grid(column=0, row=3)
        ttk.Label(self, text="Games Lost: 0").grid(column=1, row=3)
        #ttk.Label(self, text="TODO").grid(column=1, row=3, \
                                                         #sticky=tk.W)
        #ttk.Label(self, text="TODO").grid(column=1, row=4, \
                                                         #sticky=tk.W)

    def quit(self):
        # TODO: disconnect
        self.master.quit()

    def record_move(self, event):
        event.widget['text'] = 'X'
        # figure out which button was pressed
        # change the text of that button to X or O
        pass

    def start_new_game(self):
        # forfeit current game
        # assign new random partner? or keep same partner?
        pass

# puts the Tktictactoe frame in main root window
root = tk.Tk()
# the window content should expand if the main window is resized
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.title("Tic Tac Toe!")
TkTictactoe(master=root)

root.mainloop()