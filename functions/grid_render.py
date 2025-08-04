from nicegui import ui
from grid import *



#Test Grid
g = Grid(1,"default", 3)
dictionary = load_dic("./en_US.dic")

g.solve_with_backtracking(dictionary)
grid = g.cells
print(grid)

# Used ChatGPT to help generate below this line as I have essentially no knowledge of UI generation

def generate_clue_numbers(grid): 
    clue_numbers = {}
    number = 1
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '#':
                continue

            is_across_start = (
                c == 0 or grid[r][c-1] == '#'
            ) and (c + 1 < cols and grid[r][c+1] != '#')

            is_down_start = (
                r == 0 or grid[r-1][c] == '#'
            ) and (r + 1 < rows and grid[r+1][c] != '#')

            if is_across_start or is_down_start:
                clue_numbers[(r, c)] = number
                number += 1

    return clue_numbers

clue_numbers = generate_clue_numbers(grid)

rows = len(grid)
cols = len(grid[0])
cell_inputs = {}

CELL_SIZE = 40  # in px

def input_style():
    return f'''
        width: {CELL_SIZE}px;
        height: {CELL_SIZE}px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        padding: 0;
        margin: 0;
        box-sizing: border-box;
        line-height: 1;
        position: relative;
    '''

def clue_number_style():
    return '''
        position: absolute;
        top: 1px;
        left: 3px;
        font-size: 10px;
        z-index: 2;
        color: black;
    '''

with ui.column().style('gap: 2px;'):
    for r in range(rows):
        with ui.row().style(f'gap: 2px; height: {CELL_SIZE}px; align-items: center;'):
            for c in range(cols):
                val = grid[r][c]
                if val == '#':
                    ui.element('div').style(f'''
                        width: {CELL_SIZE}px;
                        height: {CELL_SIZE}px;
                        background-color: black;
                        border: 1px solid #888;
                        box-sizing: border-box;
                    ''')
                else:
                    cell_id = f'cell_{r}_{c}'
                    default = val.upper() if val else ''

                    with ui.element('div').style(f'''
                        position: relative;
                        width: {CELL_SIZE}px;
                        height: {CELL_SIZE}px;
                    '''):
                        # Optional clue number overlay
                        if (r, c) in clue_numbers:
                            ui.html(f'''
                                <div style="{clue_number_style()}">{clue_numbers[(r, c)]}</div>
                            ''')

                        input_box = ui.input(value=default).props(
                            f'maxlength=1 dense outlined input-class="text-center" id={cell_id}'
                        ).style(input_style())

                        cell_inputs[(r, c)] = input_box

# JavaScript for basic tab-to-next-cell navigation - Used ChatGPT to supply this
ui.add_head_html('''
<script>
document.addEventListener('DOMContentLoaded', () => {
    const inputs = [...document.querySelectorAll("input[id^='cell_']")];
    inputs.forEach((input, idx) => {
        input.addEventListener("input", () => {
            if (input.value.length === 1 && idx + 1 < inputs.length) {
                inputs[idx + 1].focus();
            }
        });
    });
});
</script>
''')

def submit():
    output = [[None for _ in range(cols)] for _ in range(rows)]
    for (r, c), input_element in cell_inputs.items():
        output[r][c] = input_element.value.upper() if input_element.value else ''
    print("User-filled Grid:")
    for row in output:
        print(row)
    ui.notify("Grid printed to console")

ui.button('Submit', on_click=submit)
ui.run()
