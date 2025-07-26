import numpy as np
from nicegui import ui

grid = []

def generate_grid(difficulty=1, theme="default", size=15): #TODO - Add sys.argv or some other user input

    for r in range(size):
        row = []
        for c in range(size):    
            row.append('')
        grid.append(row)
    print(grid)


def print_grid(grid):  #For visualizing while debugging
    for row in grid:
        print(' '.join(
            '⬛' if cell == '#' else (cell if cell else '⬜')
            for cell in row
        ))

def black_cells(grid): #TODO - Implement black cells function
    pass

def word_reqs(grid): #TODO - Generate word requirements (size, letters in common) (Intersections?) (Move to diff function?)
    pass



generate_grid(1,"default",15)
print_grid(grid)