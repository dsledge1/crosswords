from nicegui import ui
from grid import Grid, load_dic

def generate_and_display():
    grid = Grid(difficulty=1, theme="default", size=3)
    dictionary = load_dic("./en_US.dic", min_len=3, max_len=3)
    success = grid.solve_with_backtracking(dictionary)
    if success:
        render_grid(grid)
    else:
        ui.notify("Failed to solve grid")

def render_grid(grid_obj):
    with ui.column().classes('p-4'):
        for row in grid_obj.grid:
            with ui.row():
                for cell in row:
                    ui.label(cell if cell else " ").style(
                        "border: 1px solid black; width: 30px; height: 30px; "
                        "display: inline-flex; align-items: center; justify-content: center;"
                    )

with ui.column():
    ui.button("Generate 3x3 Crossword", on_click=generate_and_display)

ui.run()