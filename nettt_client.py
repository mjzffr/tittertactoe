#!/usr/bin/env python2

import Tkinter as tk
# themed tk
import ttk

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
        '''# place game board and other controls in two different frames
        self.tttboard = ttk.Frame(master=self, width=WIDTH, height=HEIGHT)
        self.tttboard.grid_propagate(False)
        self.tttboard.grid(sticky=tk.NSEW)
        self.controls = ttk.Frame(master=self)
        self.controls = grid()'''
        self.place_widgets()
        

    def place_widgets(self):
        # game buttons
        self.board = [[ttk.Button(self) for i in range(3)] for i in range(3)]
        for rownum, row in enumerate(self.board):
            for colnum, button in enumerate(row):
                button['text'] = str(rownum) + ',' + str(colnum)
                button.grid(column=colnum, row=rownum, sticky=tk.NSEW)
        # menu
        self.quit_btn = ttk.Button(self, text='Exit', command=self.quit)
        self.quit_btn.grid(column=2, row=5, sticky=tk.SE, pady=10, padx=10)
        self.newgame_btn = ttk.Button(self, text='New Game', 
                                      command=self.start_new_game)
        self.newgame_btn.grid(column=0, row=5, sticky=tk.SW, pady=10, padx=10)

        # status
        self.games_won = tk.IntVar()
        self.games_lost = tk.IntVar()
        ttk.Label(self, text="Games Won").grid(column=0, row=3, sticky=tk.SW)
        ttk.Label(self, text="Games Lost").grid(column=0, row=4, sticky=tk.SW)
        ttk.Label(self, textvariable=self.games_won).grid(column=1, row=3, \
                                                         sticky=(tk.W, tk.E))
        ttk.Label(self, textvariable=self.games_lost).grid(column=1, row=4, \
                                                         sticky=(tk.W, tk.E))
        #padding
        #for child in self.winfo_children():
        #    child.grid_configure(padx=10, pady=10)



    def quit(self):
        print "My quit"
        self.master.quit()

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