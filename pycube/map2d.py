import tkinter as tk
import cube
from raycasting import calculate_rays
from cube import (MAP, MAP_WIDTH, MAP_HEIGHT, CELL_SIZE, PLAYER_DOT_SIZE, FOV, NUM_RAYS)
import controls
import map3d

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
    

def draw_rays(canvas, ray_lines):
    for ray_line in ray_lines:
        if ray_line:
            canvas.delete(ray_line)
    ray_lines.clear()
    
    for i, (_, end_x, end_y) in enumerate(cube.hits):
        start_x = cube.player_x * CELL_SIZE
        start_y = cube.player_y * CELL_SIZE
        end_x = end_x * CELL_SIZE
        end_y = end_y * CELL_SIZE
        ray_line = canvas.create_line(start_x, start_y, end_x, end_y, fill="red", width=2)
        ray_lines.append(ray_line)
    return ray_lines

def update_rays(canvas, ray_lines):
    calculate_rays()
    return draw_rays(canvas, ray_lines)

def setup_controls(root):
    """Bind keyboard controls to the root window"""
    controls.setup_2d_controls(root, canvas, ray_lines)

def main():
    root = tk.Tk()
    root.title("2D View")
    display_map(root)
    setup_controls(root)
    root.focus_set()
    map3d.create_3d_window()
    root.mainloop()

if __name__ == "__main__":
    main()
