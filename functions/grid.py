import numpy as np
from nicegui import ui

class Grid:
    def __init__(self, difficulty=1, theme="default", size=15):
        self.difficulty = difficulty
        self.theme = theme
        self.size = size
        self.theme_words = []
        self.cells = []

    def generate_grid(self): #TODO - Add sys.argv or some other user input

        for r in range(self.size):
            row = []
            for c in range(self.size):    
                row.append('')
            self.cells.append(row)
        print(self.cells)


    def print_grid(self):
        for row in self.cells:
            print(' '.join(
                f'{cell}' if isinstance(cell, str) and cell not in ['', '#'] else
                '⬛' if cell == '#' else '⬜'
                for cell in row
            ))

    def gen_theme_words(difficulty=1, theme=None):
        if theme == None:   #Handle no theme, generic, easy crossword
            return
        theme_words = ["balrog","returnoftheking","fellowship"]    #Test Hardcoded
        #TODO - Add API call to generate theme words based on theme and difficulty

    def place_theme_words(self):
        pass

    def black_cells(self): #TODO - Implement black cells function
        pass

    def word_reqs(self): #TODO - Generate word requirements (size, letters in common) (Intersections?) (Move to diff function?)
        pass

    def word_list(self): #TODO - Query ditionary (NLTK library?) to generate words based on word_reqs
        pass

    def key_gen(self): #TODO - Take word list and assign each word to the correct spot in grid as the answer key
        pass

grid = Grid(1,"default",15)
grid.generate_grid()
print(grid.cells)
