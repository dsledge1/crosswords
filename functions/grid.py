import numpy as np
from nicegui import ui
import random

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

    def gen_theme_words(self):
        if self.theme == None:   #Handle no theme, generic, easy crossword
            return
        self.theme_words = ["balrog","returnoftheking","fellowship"]    #Test Hardcoded
        #TODO - Add API call to generate theme words based on theme and difficulty

    def place_theme_words(self):
        valid_rows = range(self.size//4,3*self.size//4) #Prevents theme words from being at the top or bottom of the puzzle
        theme_rows = []
        while len(theme_rows) < 3: #TODO Magic number! 3 theme words, can make this a variable later
            row = random.choice(valid_rows)
            if row not in theme_rows:
                theme_rows.append(row)
        print(f"theme_rows for this puzzle are {theme_rows}") #Remove when finished debugging
        for idx, word in enumerate(self.theme_words):
            print(f"placing {word}")
            for i in range(len(word)):
                print(f"i={i},row={theme_rows[idx]},letter={word[i]}")
                self.cells[theme_rows[idx]][i]=word[i]
        print(self.cells)

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
grid.gen_theme_words()
grid.place_theme_words()

