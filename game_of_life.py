#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 12:00:49 2021

@author: AKolcun
"""

#------Imports-----#
import numpy as np
import tkinter as tk
import functools as func
import time
from tkmacosx import Button as Button #tk toolset won't change bg on MacOSX
tk.Button = Button
#-----Imports------#

#------Initialization------#
grid_size = 30
nodes = {}
for x in range(grid_size):
    for y in range(grid_size):
        nodes[x,y] = None        
board = np.zeros((grid_size,grid_size), dtype=int)
#------Initialization------#

#NOTE- internal_board value of 0 = grey
#internal_board value of 1 = blue

#------Function Setup------#        
def live_or_die (cell_value, neighbor_sum):
    #As defined by rules of Game of Life
    if cell_value == 1 and 2 <= neighbor_sum <=3:
        new_value = 1
    elif cell_value == 0 and neighbor_sum == 3:
        new_value = 1
    else:
        new_value = 0
        
    return new_value 

       
def find_next_gen (array):
    global board
    next_gen = np.zeros((grid_size, grid_size), dtype=int) #To hold results for simultaneous update

    for x in range(grid_size):
        for y in range(grid_size):
            neighbors = [(x, y+1), (x,y-1), (x+1, y), (x-1,y), (x+1, y-1),
                         (x+1, y+1), (x-1, y-1), (x-1, y+1)]
            
            neighbor_sum = sum([array[cell] for cell in neighbors if cell in nodes])
            next_gen[(x,y)] = live_or_die(array[(x,y)], neighbor_sum)
        
    board = next_gen


def cell_click(cell):
    #To be passed to grid cells, toggling on/off state
    if cell['bg'] == 'grey':
        cell.configure(bg='blue')
    else:
        cell.configure(bg='grey')


def read_player_input(list_of_buttons):
    #Reads beginning state of board
    global board
    
    board_state = np.zeros((grid_size,grid_size), dtype=int)
    for button in list_of_buttons:
        index = button['text']
        if button['bg'] == 'grey':
            board_state[index] = 0
        else:
            board_state[index] = 1
    
    board = board_state
   
    
def update_game_board(array):
    #Reads internal board state, translates to external board
    global button_list
    
    for button in button_list:
        index = button['text']
        if array[index] == 0: #board
            button['bg'] = 'grey'
        else:
            button['bg'] = 'blue'

def execute_game_loop(array):
#Runs one cycle of read, find next gen, and update
    read_player_input(button_list)
        
    find_next_gen(board)
    update_game_board(board)
        
def step():
    
    find_next_gen(board)
    update_game_board(board)            
#------Function Setup------#
    
root = tk.Tk()

#Next block builds a list of Button objects, which serve as the main game board
button_list = []
for x in range(grid_size):
    for y in range(grid_size):
        loc = '{},{}'.format(x,y)
        loc = tk.Button(root, bg='blue', borderless=1,
                 width=25, height=25, text=(x,y), fg='', activeforeground='')
        #command must be changed after object creation, to be able to pass in object 'loc'
        #rather than a string
        loc['command'] = func.partial(cell_click, loc)
        button_list.append(loc)

#Sets up game board, and updates cells with starting color by reading state from the board       
for cell in button_list:
    cell.grid(row=cell['text'][0], column=cell['text'][1])
    if board[cell['text']] == 0:
        cell['bg'] = 'grey'
    else:
        cell['bg'] = 'blue'

#Play button setup. This starts the simulation
play = tk.Button(root, text='Play', command=lambda: execute_game_loop(board))
play.grid(row=grid_size+1, column=grid_size+1)

next_step = tk.Button(root, text='Step', command=lambda: step)
next_step.grid(row=grid_size+1,column=grid_size+2)

print_board  = tk.Button(root, text='Board State', command=lambda: print(board))
print_board.grid(row=grid_size+1, column=grid_size+3)
root.mainloop()

