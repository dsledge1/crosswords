import numpy as np
from nicegui import ui
import random


def load_dic(file, min_len=3, max_len=3):
    with open(file, "r", encoding='utf-8') as f:
        lines = f.readlines()

    words = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        word = line.split('/')[0]
        if word.isalpha():
            word = word.lower()
            if min_len <= len(word) <= max_len:
                words.add(word)
    return words

class Word:
    def __init__(self, number, direction, row, col, len):
        self.number = number
        self.direction = direction
        self.row = row
        self.col = col
        self.len = len
        self.word = None
        self.intersections = []
        #self.cells = []
    
    def get_cells(self):
        cells = []
        for i in range(self.len):
            if self.direction == "across":
                cells.append((self.row,self.col+i))
            else:
                cells.append((self.row+i, self.col))
        return cells

    def key(self):
        return f"{self.number}_{self.direction[:3]}"
    
    @property
    def cells(self):
        return [(self.row + i if self.direction == 'down' else self.row, self.col + i if self.direction == 'across' else self.col)
                for i in range(self.len)]

class Grid:
    def __init__(self, difficulty=1, theme="default", size=15): 
        if not (3 <= size <= 20):
            raise ValueError("Size must be between 3 and 20")
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

        self.generate_grid()
        self.gen_theme_words()
        #self.place_theme_words() #Out until refactor
        #self.gen_black_cells() #Out until refactor
        self.word_reqs()
        self.word_intersections()

    def generate_grid(self): #TODO - Add sys.argv or some other user input
        for r in range(self.size):
            row = []
            for c in range(self.size):    
                row.append('')
            self.cells.append(row)
        


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



    def word_reqs(self): #TODO - (Move to diff function?)
        words = {}
        num = 1
        size = self.size
        numbered = [[None for i in range(size)] for j in range(size)]

        for col in range(size):
                row = 0
                while row < size:
                    while row < size and self.cells[row][col] == "#":
                        row += 1
                    start_row = row
                    while row < size and self.cells[row][col] != "#":
                        row += 1
                    length = row - start_row
                    if length >= 3:
                        if numbered[start_row][col] is None:
                            numbered[start_row][col] = num
                            num += 1
                        word_num = numbered[start_row][col]
                        words[f"{word_num}_down"] = Word(word_num, "down", start_row, col, length)
                    row += 1
            
        for row in range(size):
            col = 0
            while col < size:
                while col < size and self.cells[row][col] == "#":
                    col += 1
                start_col = col
                while col < size and self.cells[row][col] != "#":
                    col += 1
                length = col - start_col
                if length >= 3:
                    if numbered[row][start_col] is None:
                        numbered[row][start_col] = num
                        num += 1
                    word_num = numbered[row][start_col]
                    words[f"{word_num}_across"] = Word(word_num, "across", row, start_col, length)
                col += 1

        self.words=words
        for key, slot in self.words.items():
            print(f"{key}: ({slot.row},{slot.col}), len={slot.len}")

    
    
    def word_intersections(self):
        for key1, word1 in self.words.items():
            for key2, word2 in self.words.items():
                if key1 == key2 or word1.direction == word2.direction:
                    continue 

                for idx1, (r1, c1) in enumerate(word1.cells):
                    for idx2, (r2, c2) in enumerate(word2.cells):
                        if (r1, c1) == (r2, c2):
                            if not any(
                                        existing[0] == idx1 and existing[1] == key2 and existing[2] == idx2
                                        for existing in word1.intersections
                                    ):
                                word1.intersections.append((idx1, key2, idx2))
                            if not any(
                                existing[0] == idx2 and existing[1] == key1 and existing[2] == idx1
                                for existing in word2.intersections
                            ):
                                word2.intersections.append((idx2, key1, idx1))

    def fill_words_from_dict(self, dictionary):
        available_words = [w for w in dictionary if 3 <= len(w) <= 15]
        used_words = set()

        def get_pattern(word_obj):
            pattern = ''
            for r, c in word_obj.cells:
                val = self.cells[r][c]
                pattern += val if val not in ('', '#') else '_'
            return pattern

        def matches_pattern(word, pattern):
            return all(p == '_' or p == w for p, w in zip(pattern, word))

        def can_place(word_obj, candidate):
            for i, (r, c) in enumerate(word_obj.cells):
                cell_val = self.cells[r][c]
                if cell_val != '' and cell_val != candidate[i]:
                    return False
            return True

        def place_word(word_obj, chosen):
            for i, (r, c) in enumerate(word_obj.cells):
                self.cells[r][c] = chosen[i]
            word_obj.word = chosen

        for key, word_obj in self.words.items():
            pattern = get_pattern(word_obj)
            candidates = [w for w in available_words
                        if len(w) == word_obj.len
                        and matches_pattern(w, pattern)
                        and w not in used_words
                        and can_place(word_obj, w)]

            if candidates:
                chosen = random.choice(candidates)
                place_word(word_obj, chosen)
                used_words.add(chosen)
            else:
                print(f"Could not find match for {key} with pattern '{pattern}'")
    
    def get_pattern(self, word_obj):
        return ''.join(
            self.cells[r][c] if self.cells[r][c] not in ('', '#') else '_'
            for r, c in word_obj.cells
        )

    def can_place(self, word_obj, candidate):
        for (r, c), ch in zip(word_obj.cells, candidate):
            val = self.cells[r][c]
            if val not in ('', ch):
                return False
        return True

    def place_word(self, word_obj, word):       #TODO - Add smarter initial word selection, maybe start with hardest words to fit
        for (r, c), ch in zip(word_obj.cells, word):
            self.cells[r][c] = ch
        word_obj.word = word

    def unplace_word(self, word_obj):
        for i, (r, c) in enumerate(word_obj.cells):
            still_used = False
            for other_key, other_word in self.words.items():
                if other_word.word is None or other_word == word_obj:
                    continue
                if (r, c) in other_word.cells:
                    idx = other_word.cells.index((r, c))
                    self.cells[r][c] = other_word.word[idx]
                    still_used = True
                    break
            if not still_used:
                self.cells[r][c] = ''
        word_obj.word = None

    def solve_with_backtracking(self, dictionary):
        slots = list(self.words.items())
        used_words = set()

        def helper(index):
            if index == len(slots):
                return True  # Done!

            key, word_obj = slots[index]
            pattern = self.get_pattern(word_obj)

            candidates = [
                w for w in dictionary
                if len(w) == word_obj.len
                and w not in used_words
                and self.can_place(word_obj, w)
            ]

            for candidate in candidates:
                self.place_word(word_obj, candidate)
                used_words.add(candidate)

                if helper(index + 1):
                    return True  # Success!

                self.unplace_word(word_obj)
                used_words.remove(candidate)

            return False  # Trigger backtrack

        success = helper(0)
        if not success:
            print("Could not solve puzzle with given dictionary.")
        return success

    def word_list(self): #TODO - Query ditionary (NLTK library?) to generate words based on word_reqs
        pass

    def key_gen(self): #TODO - Take word list and assign each word to the correct spot in grid as the answer key
        pass





if __name__ == '__main__':
    grid = Grid(1, "default", 3)

    dictionary = load_dic("./en_US.dic")
    #with open("./themewords.txt") as t:
    #    custom = [line.strip().lower() for line in t if line.strip()]
    #dictionary.update(custom)
    grid.solve_with_backtracking(dictionary)
    grid.print_grid()