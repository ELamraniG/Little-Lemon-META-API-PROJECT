import tkinter as tk
from raycasting import update_rays
from cube import (MAP, MAP_WIDTH, MAP_HEIGHT, CELL_SIZE, PLAYER_DOT_SIZE)
import controls

# Global variables for canvas elements
canvas = None
dot = None
ray_lines = []

def display_map(root):
    """Create and display the game map with player and rays"""
    global canvas, dot
    canvas = tk.Canvas(root, width=MAP_WIDTH * CELL_SIZE, height=MAP_HEIGHT * CELL_SIZE)
    canvas.pack()

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            color = "white" if MAP[y][x] == 1 else "black"
            canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=color,
            )

    dot = canvas.create_oval(0, 0, 0, 0, fill="yellow")
    update_dot_position()
    update_rays(canvas, ray_lines)

    return canvas, dot

def update_dot_position():
    from cube import player_x, player_y
    cx = player_x * CELL_SIZE
    cy = player_y * CELL_SIZE
    canvas.coords(dot, cx - PLAYER_DOT_SIZE, cy - PLAYER_DOT_SIZE, cx + PLAYER_DOT_SIZE, cy + PLAYER_DOT_SIZE)

def setup_controls(root):
    """Bind keyboard controls to the root window"""
    def move_up(event): controls.move_up(event, canvas, ray_lines); update_dot_position()
    def move_down(event): controls.move_down(event, canvas, ray_lines); update_dot_position()
    def move_left(event): controls.move_left(event, canvas, ray_lines); update_dot_position()
    def move_right(event): controls.move_right(event, canvas, ray_lines); update_dot_position()
    def rotate_left(event): controls.rotate_left(event, canvas, ray_lines)
    def rotate_right(event): controls.rotate_right(event, canvas, ray_lines)
    
    root.bind("<KeyPress-w>", move_up)
    root.bind("<KeyPress-s>", move_down)
    root.bind("<KeyPress-a>", move_left)
    root.bind("<KeyPress-d>", move_right)
    root.bind("<Left>", rotate_left)
    root.bind("<Right>", rotate_right)
    root.bind("<Escape>", lambda event: root.quit())

def main():
    root = tk.Tk()
    root.title("Cube3D")
    display_map(root)
    setup_controls(root)
    root.focus_set()
    root.mainloop()

if __name__ == "__main__":
    main()
