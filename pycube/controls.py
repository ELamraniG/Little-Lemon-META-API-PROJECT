from cube import MOVE_STEP, ROTATION_STEP
import math
import cube
from raycasting import calculate_rays

def is_walkable(row, col):
    from cube import MAP, MAP_WIDTH, MAP_HEIGHT
    r, c = int(row), int(col)
    if 0 <= r < MAP_HEIGHT and 0 <= c < MAP_WIDTH:
        return MAP[r][c] == 0
    return False

def move(dx, dy):
    new_row = cube.player_y + dy
    new_col = cube.player_x + dx
    
    if is_walkable(new_row, new_col):
        cube.player_y = new_row
        cube.player_x = new_col
        calculate_rays()

# Movement _ handlers
def move_up(_): 
    dx = math.cos(cube.player_angle) * MOVE_STEP
    dy = math.sin(cube.player_angle) * MOVE_STEP
    move(dx, dy)

def move_down(_):
    dx = math.cos(cube.player_angle) * -MOVE_STEP
    dy = math.sin(cube.player_angle) * -MOVE_STEP
    move(dx, dy)

def move_left(_):
    angle = cube.player_angle - math.pi/2
    dx = math.cos(angle) * MOVE_STEP
    dy = math.sin(angle) * MOVE_STEP
    move(dx, dy)

def move_right(_):
    angle = cube.player_angle - math.pi/2
    dx = math.cos(angle) * -MOVE_STEP
    dy = math.sin(angle) * -MOVE_STEP
    move(dx, dy)

def rotate_left(_):
    cube.player_angle -= ROTATION_STEP
    if cube.player_angle < 0:
        cube.player_angle += 2 * math.pi
    calculate_rays()

def rotate_right(_):
    cube.player_angle += ROTATION_STEP
    if cube.player_angle >= 2 * math.pi:
        cube.player_angle -= 2 * math.pi
    calculate_rays()

# 2D controls setup
def setup_2d_controls(root, canvas, ray_lines):
    """Set up controls for 2D view"""
    import map2d
    import map3d
    
    def move_up_2d(_): 
        move_up(_)
        map2d.update_dot_position()
        map2d.draw_rays(canvas, ray_lines)
        map3d.render_3d()
    def move_down_2d(_): 
        move_down(_)
        map2d.update_dot_position()
        map2d.draw_rays(canvas, ray_lines)
        map3d.render_3d()
    def move_left_2d(_): 
        move_left(_)
        map2d.update_dot_position()
        map2d.draw_rays(canvas, ray_lines)
        map3d.render_3d()
    def move_right_2d(_): 
        move_right(_)
        map2d.update_dot_position()
        map2d.draw_rays(canvas, ray_lines)
        map3d.render_3d()
    def rotate_left_2d(_): 
        rotate_left(_)
        map2d.draw_rays(canvas, ray_lines)
        map3d.render_3d()
    def rotate_right_2d(_): 
        rotate_right(_)
    
    root.bind("<KeyPress-w>", move_up_2d)
    root.bind("<KeyPress-s>", move_down_2d)
    root.bind("<KeyPress-a>", move_left_2d)
    root.bind("<KeyPress-d>", move_right_2d)
    root.bind("<Left>", rotate_left_2d)
    root.bind("<Right>", rotate_right_2d)
    root.bind("<Escape>", lambda _: root.quit())

# 3D controls setup
def setup_3d_controls(window):
    """Set up controls for 3D view"""
    import map2d
    import map3d
    
    def move_up_3d(_): 
        move_up(_)
        map3d.render_3d()
        map2d.update_dot_position()
        map2d.draw_rays(map2d.canvas, map2d.ray_lines)
    def move_down_3d(_): 
        move_down(_)
        map3d.render_3d()
        map2d.update_dot_position()
        map2d.draw_rays(map2d.canvas, map2d.ray_lines)
    def move_left_3d(_): 
        move_left(_)
        map3d.render_3d()
        map2d.update_dot_position()
        map2d.draw_rays(map2d.canvas, map2d.ray_lines)
    def move_right_3d(_): 
        move_right(_)
        map3d.render_3d()
        map2d.update_dot_position()
        map2d.draw_rays(map2d.canvas, map2d.ray_lines)
    def rotate_left_3d(_): 
        rotate_left(_)
        map3d.render_3d()
        map2d.draw_rays(map2d.canvas, map2d.ray_lines)
    def rotate_right_3d(_): 
        rotate_right(_)
        map3d.render_3d()
        map2d.draw_rays(map2d.canvas, map2d.ray_lines)
    
    window.bind("<KeyPress-w>", move_up_3d)
    window.bind("<KeyPress-s>", move_down_3d)
    window.bind("<KeyPress-a>", move_left_3d)
    window.bind("<KeyPress-d>", move_right_3d)
    window.bind("<Left>", rotate_left_3d)
    window.bind("<Right>", rotate_right_3d)
    window.bind("<Escape>", lambda _: window.quit())
