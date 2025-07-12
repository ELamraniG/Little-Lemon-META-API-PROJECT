import math
import cube
from raycasting import update_rays
from cube import MOVE_STEP, ROTATION_STEP

def is_walkable(row, col):
	from cube import MAP, MAP_WIDTH, MAP_HEIGHT
	r, c = int(row), int(col)
	if 0 <= r < MAP_HEIGHT and 0 <= c < MAP_WIDTH:
		return MAP[r][c] == 0
	return False

def move(dx, dy, canvas, ray_lines):
	new_row = cube.player_y + dy
	new_col = cube.player_x + dx
	
	if is_walkable(new_row, new_col):
		cube.player_y = new_row
		cube.player_x = new_col
		update_rays(canvas, ray_lines)

# Movement event handlers
def move_up(event, canvas, ray_lines): 
	move(math.cos(cube.player_angle) * MOVE_STEP, math.sin(cube.player_angle) * MOVE_STEP, canvas, ray_lines)

def move_down(event, canvas, ray_lines):
	move(math.cos(cube.player_angle) * -MOVE_STEP, math.sin(cube.player_angle) * -MOVE_STEP, canvas, ray_lines)

def move_left(event, canvas, ray_lines):
	move(math.cos(cube.player_angle - math.pi/2) * MOVE_STEP, math.sin(cube.player_angle - math.pi/2) * MOVE_STEP, canvas, ray_lines)

def move_right(event, canvas, ray_lines):
	move(math.cos(cube.player_angle - math.pi/2) * -MOVE_STEP, math.sin(cube.player_angle - math.pi/2) * -MOVE_STEP, canvas, ray_lines)

def rotate_left(event, canvas, ray_lines):
	cube.player_angle -= ROTATION_STEP
	if cube.player_angle < 0:
		cube.player_angle += 2 * math.pi
	update_rays(canvas, ray_lines)

def rotate_right(event, canvas, ray_lines):
	cube.player_angle += ROTATION_STEP
	if cube.player_angle >= 2 * math.pi:
		cube.player_angle -= 2 * math.pi
	update_rays(canvas, ray_lines)
