import numpy as np
from nicegui import ui
import random

class Word:
    def __init__(self, number, direction, row, col, len):
        self.number = number
        self.direction = direction
        self.row = row
        self.col = col
        self.len = len
        self.word = None

class Grid:
    def __init__(self, difficulty=1, theme="default", size=15): 
        if not (10 <= size <= 20):
            raise ValueError("Size must be between 10 and 20")
        if not (1<=difficulty<=10):
            raise ValueError("Difficulty must be between 1 and 10")
        self.difficulty = difficulty
        self.theme = theme
        self.size = size
        self.theme_words = []
        self.cells = []
        self.seed1 = np.random.randint(low=-1, high=1) #TODO - Make seed more meaningful and impactful, currently using for basic puzzle variation
        self.seed2 = np.random.randint(low=-1, high=1)
        self.theme_rows = []
        self.words = {}

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
        self.theme_words = ["orcsandwargs","thetwotowers","frodobaggins"]    #Test Hardcoded
        #TODO - Add API call to generate theme words based on theme and difficulty

    def place_theme_words(self):
        valid_rows = range(self.size//4,3*self.size//4) #Prevents theme words from being at the top or bottom of the puzzle
        while len(self.theme_rows) < 3: #TODO Magic number! 3 theme words, can make this a variable later
            row = random.choice(valid_rows)
            if row not in self.theme_rows and (row+1) not in self.theme_rows and (row-1) not in self.theme_rows:
                self.theme_rows.append(row)
        print(f"theme_rows for this puzzle are {self.theme_rows}") #Remove when finished debugging
        for idx, word in enumerate(self.theme_words):
            print(f"placing {word}")
            for i in range(len(word)):
                print(f"i={i},row={self.theme_rows[idx]},letter={word[i]}") #Debug - remove
                self.cells[self.theme_rows[idx]][i]=word[i]

    def set_black(self, row, col):
        if self.cells[row][col] == '' and self.cells[self.size-1-row][self.size-1-col] == '':
            self.cells[row][col] = '#'
            self.cells[self.size-1-row][self.size-1-col] = '#' #every time we set one black, we set the symmetric cell black as well 
        if not (self.cells[row][col] == '' and self.cells[self.size-1-row][self.size-1-col] == ''):
            pass #TODO - See about having this re-run in a different place if not enough black tiles generate

    def gen_black_cells(self): #TODO - Implement black cells function
        print(f"seed1 is {self.seed1}, seed2 is {self.seed2}")
        first_col_offset = max(4,self.size//3 + self.seed1) #How far first column is offset from either y-axis, min: 3 (seed can be -1) to prevent 1 or 2-letter words. Roughly want 1 at 1/3 and 2/3 across grid.
        len_first_col = 4 + self.seed2
        first_black_row = max(4,self.size//3 + self.seed2) #How far down first black row appears
        len_first_black_row = 4 + self.seed1
        len_first_opp_black_row = 4 + self.seed2
        len_second_col = 4 + self.seed1
        second_col_offset = min(first_col_offset+4,self.size-3)
        center_block_1 = (self.size//2) + self.seed1 #TODO - Remove and add real center decoration logic
        len_center_block_1 = 4 + self.seed2
        while first_black_row in self.theme_rows:
            first_black_row+=1
        for i in range(len_first_col):
            self.set_black(i,first_col_offset)
        for i in range(len_second_col):
            self.set_black(i,second_col_offset)
        for i in range(len_first_black_row):
            self.set_black(first_black_row,i)
        for i in range(len_first_opp_black_row):
            self.set_black(first_black_row,self.size - len_first_opp_black_row + i)
        for i in range(len_center_block_1):
            self.set_black((self.size//2)-len_center_block_1//2,center_block_1)

    ###TODO - Overhaul the way words are generated and viewed. This needs to be refactored as a graph with words being head->tail paths, edges for intersections.
    ###If you have time, this is the first thing to come back and fix. 



    def word_reqs(self): #TODO - Generate word requirements (size, letters in common) (Intersections?) (Move to diff function?)
        words = {}
        num = 1
        size = self.size
        numbered = [[None for i in range(size)] for j in range(size)]

        for row in range(size):
            col = 0
            while col < size:
                while col < size and self.cells[row][col]=="#": #for rows that start w black squares
                    col+=1
                start_col = col
                while col < size and self.cells[row][col] != "#": #move forward until a new square -> end of word
                    col+=1
                len = col - start_col
                if len >=3:
                    if numbered[row][start_col] is None:
                        numbered[row][start_col] = num
                        words[f"{num}_acc"] = Word(num,"across",row, start_col, len)
                        num+=1
                col+=1

        for col in range(size):
            row = 0
            while row < size:
                while row < size and self.cells[row][col]=="#": #for rows that start w black squares
                    row+=1
                start_row = row
                while row < size and self.cells[row][col] != "#": #move forward until a new square -> end of word
                    row+=1
                len = row - start_row
                if len >=3:
                    if numbered[start_row][col] is None:
                        numbered[start_row][col] = num
                        words[f"{num}_dwn"] = Word(num,"down",start_row, col, len)
                        num+=1
                row+=1

        self.words=words
        for key, slot in self.words.items():
            print(f"{key}: ({slot.row},{slot.col}), len={slot.len}")

    def word_list(self): #TODO - Query ditionary (NLTK library?) to generate words based on word_reqs
        pass

    def key_gen(self): #TODO - Take word list and assign each word to the correct spot in grid as the answer key
        pass

grid = Grid(1,"default",12)

grid.generate_grid()
grid.gen_theme_words()
grid.place_theme_words()
grid.gen_black_cells()
grid.print_grid()
grid.word_reqs()
print(grid.words)
