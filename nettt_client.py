#!/usr/bin/env python2

import Tkinter as tk
# themed tk
import ttk

WIDTH = 750
HEIGHT = 800

class TkTictactoe(ttk.Frame):

    def __init__(self, master = None):
        ttk.Frame.__init__(self, master, width=WIDTH, height=HEIGHT)
        # don't shrink the frame to its content
        self.grid_propagate(False)
        # draw the frame (and its content); make all the edges of the frame
        # stick to the edges of the root window
        self.grid(sticky=tk.NSEW)
        #self.height = HEIGHT
        #self.width = WIDTH
        # All the board buttons should expand if the main window is resized
        # We achieve this by giving w/h of the cells on the diagonal the same
        # "expansion" weight 
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)

        self.create_board()
        

    def create_board(self):
        # game buttons
        self.board = [[ttk.Button(self) for i in range(3)] for i in range(3)]
        for rownum, row in enumerate(self.board):
            for colnum, button in enumerate(row):
                button['text'] = str(rownum) + ',' + str(colnum)
                button.grid(column=colnum, row=rownum, sticky=tk.NSEW)
        # status/menu
        self.quit_btn = ttk.Button(self, text = 'Quit', command = self.quit)
        self.quit_btn.grid(column=2, row=3, sticky=tk.SE, pady=10, padx = 10)

    def run(self):
        self.master.mainloop()

    def onObjectClick(self, event):
        print 'Got object click', event.x, event.y,  
        print event.widget.find_closest(event.x, event.y)  

class TkWelcome(ttk.Frame):
    def __init__(self, master = None):
        ttk.Frame.__init__(self,master)
        


# puts the Tktictactoe frame in main root window
root = tk.Tk()
# the window content should expand if the main window is resized
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.title("Tic Tac Toe!")
TkTictactoe(master = root).run()
