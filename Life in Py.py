#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:49:48 2021

@author: AKolcun
"""

#------Imports-----#
import numpy as np
import tkinter as tk
import functools as func
#-----Imports------#

class game_of_life:
    
    def __init__(self, n):
        #Initialize class variables, internal & external boards, and layout
        self.running = 0
        self.sim_speed = 2000
        self.n = n
        
        self.nodes = self.create_node_list(n)
        self.internal_board = np.zeros((n,n), dtype=int)
        
        #Root and frame creation, to allow for external_board creation
        self.root = tk.Tk()
        self.root.title('Life in Py')
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.pixel = tk.PhotoImage(width=1, height=1)
        self.root.geometry(f'{self.width}x{self.height}')
        
        
        board_frame = tk.LabelFrame(self.root, bg='white', labelanchor='n', text='Game Board')
        controls_frame = tk.LabelFrame(self.root, bg='lavender', padx=10, pady=10, labelanchor='n', text='Controls' )
        
        self.external_board = self.create_external_board(n, board_frame)
        
        #Button & slider creation
        self.play = tk.Button(controls_frame, text='Play', command=self.start_game)
        self.pause = tk.Button(controls_frame, text='Pause', state ='disabled', command=self.pause_game)
        self.clear = tk.Button(controls_frame, text='Clear Board', command=self.clear_board)
        self.speed = tk.Scale(controls_frame, from_=2000, to=1, orient='horizontal', label='Simulation Speed', 
                              showvalue=0, length=200, command=self.set_sim_speed)
        self.speed.set(2000)
        
        #Frame, button, and board layout
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_columnconfigure(1,weight=1)
        
        board_frame.grid(row=0, column=0)
        controls_frame.grid(row=0, column=1, padx=40, pady=40)
        
        for cell in self.external_board.keys():
            self.external_board[cell].grid(row=cell[0], 
                                           column=cell[1])
        
        self.play.grid(row=0)
        self.pause.grid(row=1)
        self.clear.grid(row=2)
        self.speed.grid(row=3, pady=15)
        
        self.root.mainloop()
    
            
    def live_or_die (self, cell_value, neighbor_sum):
        #As defined by rules of Game of Life. Runs on internal board
        if cell_value == 1 and 2 <= neighbor_sum <=3:
            new_value = 1
        elif cell_value == 0 and neighbor_sum == 3:
            new_value = 1
        else:
            new_value = 0
            
        return new_value    
        
           
    def find_next_gen (self):
        #Determines whether each cell lives or dies. Runs on internal board
        #Returns a list of changed nodes that will be updated on the external board
        #Rather than looping through entire external board
        
        next_gen = np.zeros((self.n, self.n), dtype=int) #To hold results for simultaneous update
        change_list = []

        for x in range(self.n):
            for y in range(self.n):
                #Adjacent and diagonal neighbors are considered
                neighbors = [(x, y+1), (x,y-1), (x+1, y), (x-1,y), (x+1, y-1),
                             (x+1, y+1), (x-1, y-1), (x-1, y+1)]
            
                neighbor_sum = sum([self.internal_board[cell] for cell in neighbors if cell in self.nodes])
                next_gen[(x,y)] = self.live_or_die(self.internal_board[(x,y)], neighbor_sum)
                
                if next_gen[(x,y)] != self.internal_board[(x,y)]:
                    change_list.append((x,y))
        
        self.internal_board = next_gen
        return change_list
    
    
    def cell_click(self, cell):
        #To be passed to external board cells, toggling alive/dead state
        if cell['bg'] == 'white':
            cell.configure(bg='blue')
        else:
            cell.configure(bg='white')
        
        
    def update_external(self, list_of_changes):
        #Translates list of changed internal cells to external board
        #Remember that grid coords are stored in text field of button as a tuple
        for cell in list_of_changes:
            if self.internal_board[cell] == 0:
                self.external_board[cell]['disabledforeground'] = 'white'
                self.external_board[cell]['bg'] = 'white'
            else:
                self.external_board[cell]['disabledforeground'] = 'blue'
                self.external_board[cell]['bg'] = 'blue'
                
        
    def start_game(self):
        #Deactivates game board and buttons as needed, initiates game loop
        self.disable_game_board()
        self.play['state'] = 'disabled'
        self.clear['state'] = 'disabled'
        
        self.read_external_board()
        
        self.running = 1
        self.game_loop()
        
    
    def read_external_board(self):
        #Reads external_board state
    
        board_read = np.zeros((self.n, self.n), dtype=int)
        for cell in self.external_board.keys():
            if self.external_board[cell]['bg'] == 'white':
                board_read[cell] = 0
            else:
                board_read[cell] = 1
        
        self.internal_board = board_read


    def disable_game_board(self):
        #Sets game board bottons to disabled and enables Pause button
        
        self.pause['state'] = 'normal'
        
        for cell in self.external_board.keys():
            self.external_board[cell]['disabledforeground'] = self.external_board[cell]['bg']
            self.external_board[cell]['state'] = 'disabled'
    
    
    def enable_game_board(self):
        #Opposite of disable game board.
        
        self.pause['state'] = 'disabled'
        self.play['state'] = 'normal'
        self.clear['state'] = 'normal'
        for cell in self.external_board.keys():
            self.external_board[cell]['state'] = 'normal'
        
        
    def pause_game(self):
        #Interrupts game loop, changes button states.
        #Bound to pause button
        
        self.running = 0
        self.enable_game_board()
        
                 
    def game_loop(self):
        #Executes loop of change internal board -> update external board
        
        if self.running == 1:
            self.update_external(self.find_next_gen())
            self.root.after(self.sim_speed,self.game_loop)
     
        
    def set_sim_speed(self, value):
        #Values are in ms
        #Bound to slider
        
        self.sim_speed = value
    
        
    def clear_board(self):
        #Resets external board, then updates internal board
        
        for cell in self.external_board.keys():
            self.external_board[cell]['bg'] = 'white'
        self.read_external_board()
        
        
    def create_node_list(self, n):
        #Generates and returns set of valid nodes to check against during neighbor_search
        
        nodes = []
         
        for x in range(n):
            for y in range(n):
                nodes.append((x,y))
                
        return set(nodes)
    

    def create_external_board(self, n, frame):
        #Generates and returns dict of buttons that will represent visible game board
        h = self.height * 0.65
        
        external_board = {}
        for x in range(n):
            for y in range(n):
                key = x,y
                cell = tk.Button(frame, bg='white', image = self.pixel, compound='c',
                        width=(h//n), height=(h//n), activebackground='gray')
                #command must be changed after object creation, to be able to pass in object 'loc'
                #rather than a string
                cell['command'] = func.partial(self.cell_click, cell)
                external_board[key] = cell
        
        return external_board
