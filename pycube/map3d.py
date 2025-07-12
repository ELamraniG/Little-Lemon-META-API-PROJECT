import tkinter as tk
import cube
import math
from cube import THREE_D_WALL_HEIGHT

def render_3d():
    if canvas_3d is None:
        return
    canvas_3d.delete("all")
    screen_width = 800
    screen_height = 600
    
    if not cube.hits:
        return
    
    num_rays = len(cube.hits)
    for i, (ray_angle, end_x, end_y) in enumerate(cube.hits):
        
        distance = math.sqrt((end_x - cube.player_x) ** 2 + (end_y - cube.player_y) ** 2)
        corrected_distance = distance * math.cos(ray_angle - cube.player_angle)
        
        wall_height = int(THREE_D_WALL_HEIGHT / max(corrected_distance, 0.1))
        wall_height = min(wall_height, screen_height)

        canvas_3d.create_rectangle(
            i * (screen_width / num_rays), 
            (screen_height - wall_height) // 2, 
            (i + 1) * (screen_width / num_rays), 
            (screen_height - wall_height) // 2 + wall_height,
            fill='white', outline=''
        )

def create_3d_window():
    global window_3d, canvas_3d
    
    window_3d = tk.Tk()
    window_3d.title("3D View")
    
    window_3d.geometry("800x600+{}+{}".format(window_3d.winfo_screenwidth()-800, 0))
    
    canvas_3d = tk.Canvas(window_3d, width=800, height=600, bg="black")
    canvas_3d.pack()
    
    import controls
    controls.setup_3d_controls(window_3d)
    
    window_3d.focus_set()
    
    render_3d()

    window_3d.mainloop()