#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 12:00:49 2021

@author: AKolcun
"""

import numpy as np
import tkinter as tk
import functools as func
from tkmacosx import Button as Button #tk toolset won't change bg on MacOSX
tk.Button = Button

grid_size = 10
nodes = {}
for x in range(grid_size):
    for y in range(grid_size):
        nodes[x,y] = None
        
board = np.zeros((grid_size,grid_size))

        
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
    next_gen = np.zeros((grid_size, grid_size), dtype=int) #To hold results for simultaneous update

    for x in range(grid_size):
        for y in range(grid_size):
            neighbors = [(x, y+1), (x,y-1), (x+1, y), (x-1,y), (x+1, y-1),
                         (x+1, y+1), (x-1, y-1), (x-1, y+1)]
            
            neighbor_sum = sum([array[cell] for cell in neighbors if cell in nodes])
            
            next_gen[(x,y)] = live_or_die(array[(x,y)], neighbor_sum)
            
    return(next_gen)


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
        
for cell in button_list:
    cell.grid(row=cell['text'][0], column=cell['text'][1])
    if board[cell['text']] == 0:
        cell['bg'] = 'grey'
    else:
        cell['bg'] = 'blue'

play = tk.Button(root, text='Play', command=func.partial(read_player_input, button_list))
play.grid(row=grid_size+1, column=grid_size+1)

root.mainloop()

