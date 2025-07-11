import tkinter as tk
import math

# Integer map
int_map = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

# Convert map to float-friendly reference (still integers in logic)
MAP_WIDTH = len(int_map[0])
MAP_HEIGHT = len(int_map)
CELL_SIZE = 100
dot_radius = 5

# Player starts at center of (2,2)
player_row = 2.5
player_col = 2.5
player_angle = math.pi / 2  # Pointing upward

# Global variables for canvas elements
canvas = None
dot = None
ray_lines = []

def is_wall(row, col):
    """Check if a position is a wall (1) or out of bounds"""
    r, c = int(row), int(col)
    if 0 <= r < MAP_HEIGHT and 0 <= c < MAP_WIDTH:
        return int_map[r][c] == 1
    return True  # Out of bounds is considered a wall

def cast_ray(start_col, start_row, angle):
    # Ray direction
    dx = math.cos(angle)
    dy = math.sin(angle)
    
    # Current position
    x = start_col
    y = start_row
    
    # Which grid cell we're in
    map_x = int(x)
    map_y = int(y)
    
    # Calculate delta distances (distance ray travels for 1 unit in x or y)
    if dx == 0:
        delta_dist_x = float('inf')
    else:
        delta_dist_x = abs(1 / dx)
    
    if dy == 0:
        delta_dist_y = float('inf')
    else:
        delta_dist_y = abs(1 / dy)
    
    # What direction to step in x or y (either +1 or -1)
    if dx < 0:
        step_x = -1
        side_dist_x = (x - map_x) * delta_dist_x
    else:
        step_x = 1
        side_dist_x = (map_x + 1.0 - x) * delta_dist_x
    
    if dy < 0:
        step_y = -1
        side_dist_y = (y - map_y) * delta_dist_y
    else:
        step_y = 1
        side_dist_y = (map_y + 1.0 - y) * delta_dist_y
    
    # Perform DDA
    hit = False
    while not hit:
        # Jump to next map square, either in x-direction, or in y-direction
        if side_dist_x < side_dist_y:
            side_dist_x += delta_dist_x
            map_x += step_x
            side = 0  # Hit x-side
        else:
            side_dist_y += delta_dist_y
            map_y += step_y
            side = 1  # Hit y-side
        
        # Check if ray has hit a wall
        if is_wall(map_y, map_x):
            hit = True
    
    # Calculate exact hit point
    if side == 0:  # Hit x-side
        perp_wall_dist = (map_x - x + (1 - step_x) / 2) / dx
    else:  # Hit y-side
        perp_wall_dist = (map_y - y + (1 - step_y) / 2) / dy
    
    # Calculate exact hit coordinates
    hit_x = x + perp_wall_dist * dx
    hit_y = y + perp_wall_dist * dy
    
    return hit_x, hit_y

def update_ray():
    global ray_lines
    for ray_line in ray_lines:
        if ray_line:
            canvas.delete(ray_line)
    ray_lines = []

    FOV = math.pi / 3  # 60 degrees
    NUM_RAYS = 6
    HALF_FOV = FOV / 2

    for i in range(NUM_RAYS):
        # Center the rays: offset goes from -HALF_FOV to +HALF_FOV
        ray_angle = player_angle - HALF_FOV + (i + 0.5) * (FOV / NUM_RAYS)

        end_col, end_row = cast_ray(player_col, player_row, ray_angle)

        start_x = player_col * CELL_SIZE
        start_y = player_row * CELL_SIZE

        end_x = end_col * CELL_SIZE
        end_y = end_row * CELL_SIZE

        ray_line = canvas.create_line(start_x, start_y, end_x, end_y, fill="red", width=2)
        ray_lines.append(ray_line)


def display_map(root):
    global canvas, dot
    canvas = tk.Canvas(root, width=MAP_WIDTH * CELL_SIZE, height=MAP_HEIGHT * CELL_SIZE)
    canvas.pack()
    
    # Draw map cells
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            color = "white" if int_map[y][x] == 1 else "black"
            canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=color,
                outline="gray"
            )
    
    # Create player dot
    dot = canvas.create_oval(0, 0, 0, 0, fill="yellow")
    update_dot_position()
    
    # Draw initial ray
    update_ray()
    
    return canvas, dot

def update_dot_position():
    cx = player_col * CELL_SIZE
    cy = player_row * CELL_SIZE
    canvas.coords(dot, cx - dot_radius, cy - dot_radius, cx + dot_radius, cy + dot_radius)

def is_walkable(row, col):
    r, c = int(row), int(col)
    if 0 <= r < MAP_HEIGHT and 0 <= c < MAP_WIDTH:
        return int_map[r][c] == 0
    return False

def move(dx, dy):
    global player_row, player_col
    
    new_row = player_row + dy
    new_col = player_col + dx
    
    if is_walkable(new_row, new_col):
        player_row = new_row
        player_col = new_col
        update_dot_position()
        update_ray()

# Create window
root = tk.Tk()
root.title("Raycasting Map - Single Ray")
canvas, dot = display_map(root)

# Movement step size
STEP = 0.05

# Movement functions
def move_up(event): move(math.cos(player_angle) * STEP, math.sin(player_angle) * STEP)
def move_down(event): move(math.cos(player_angle) * -STEP, math.sin(player_angle) * -STEP)
def move_left(event): move(math.cos(player_angle - math.pi/2) * STEP, math.sin(player_angle - math.pi/2) * STEP)
def move_right(event): move(math.cos(player_angle - math.pi/2) * -STEP, math.sin(player_angle - math.pi/2) * -STEP)

# Rotation functions
def rotate_left(event):
    global player_angle
    player_angle -= math.pi / 16  # Rotate by 11.25 degrees
    update_ray()

def rotate_right(event):
    global player_angle
    player_angle += math.pi / 16  # Rotate by 11.25 degrees
    update_ray()

# Bind keys
root.bind("<KeyPress-w>", move_up)
root.bind("<KeyPress-s>", move_down)
root.bind("<KeyPress-a>", move_left)
root.bind("<KeyPress-d>", move_right)
root.bind("<Left>", rotate_left)
root.bind("<Right>", rotate_right)

# Make sure window can receive key events
root.focus_set()

print("Use WASD keys to move relative to player direction:")
print("  W - Move forward (in facing direction)")
print("  S - Move backward (opposite to facing direction)")
print("  A - Strafe left (perpendicular left)")
print("  D - Strafe right (perpendicular right)")
print("Use LEFT/RIGHT arrow keys to rotate the player")
print("The red ray shows the direction the player is facing")

root.mainloop()