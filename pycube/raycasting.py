import math
import cube

def cast_ray(player_x, player_y, angle):

	map_x = int(player_x)
	map_y = int(player_y)


	steps_in_x_to_reach_next_x_at_angle = math.cos(angle)
	steps_in_y_to_reach_next_y_at_angle = math.sin(angle)

	if steps_in_x_to_reach_next_x_at_angle != 0:
		steps_in_angle_to_reach_next_x = abs(1 / steps_in_x_to_reach_next_x_at_angle)
	else:
		steps_in_angle_to_reach_next_x = float('inf')

	if steps_in_y_to_reach_next_y_at_angle != 0:
		steps_in_angle_to_reach_next_y = abs(1 / steps_in_y_to_reach_next_y_at_angle)
	else:
		steps_in_angle_to_reach_next_y = float('inf')
	
	# What direction to step in x or y (either +1 or -1)
	if steps_in_x_to_reach_next_x_at_angle < 0: # moving left
		x_intercept_distance = (player_x - map_x) * steps_in_angle_to_reach_next_x
	else:
		x_intercept_distance = (map_x + 1 - player_x) * steps_in_angle_to_reach_next_x
   
	if steps_in_y_to_reach_next_y_at_angle < 0: # moving up
		y_intercept_distance = (player_y - map_y) * steps_in_angle_to_reach_next_y
	else:
		y_intercept_distance = (map_y + 1 - player_y) * steps_in_angle_to_reach_next_y

	while True:
		if x_intercept_distance < y_intercept_distance:
			x_intercept_distance += steps_in_angle_to_reach_next_x
			if steps_in_x_to_reach_next_x_at_angle < 0:
				map_x += -1
			else:
				map_x += 1
			if is_wall(map_y, map_x):
				# Hit x-side
				if steps_in_x_to_reach_next_x_at_angle > 0:
					hit_x = map_x
				else:
					hit_x = map_x + 1
				hit_y = player_y + ((hit_x - player_x) / steps_in_x_to_reach_next_x_at_angle) * steps_in_y_to_reach_next_y_at_angle
				break
		else:
			y_intercept_distance += steps_in_angle_to_reach_next_y
			if steps_in_y_to_reach_next_y_at_angle < 0:
				map_y += -1
			else:
				map_y += 1
			if is_wall(map_y, map_x):
				# Hit y-side
				if steps_in_y_to_reach_next_y_at_angle > 0:
					hit_y = map_y
				else:
					hit_y = map_y + 1
				hit_x = player_x + ((hit_y - player_y) / steps_in_y_to_reach_next_y_at_angle) * steps_in_x_to_reach_next_x_at_angle
				break
   
	return hit_x, hit_y

def calculate_rays():
	cube.hits = []
	
	HALF_FOV = cube.FOV / 2
	for i in range(cube.NUM_RAYS):
		ray_angle = cube.player_angle - HALF_FOV + (i + 0.5) * (cube.FOV / cube.NUM_RAYS)
		end_x, end_y = cast_ray(cube.player_x, cube.player_y, ray_angle)

		cube.hits.append((ray_angle, end_x, end_y))

def is_wall(row, col):
	r, c = int(row), int(col)
	if 0 <= r < cube.MAP_HEIGHT and 0 <= c < cube.MAP_WIDTH:
		return cube.MAP[r][c] == 1
	return True  # Out of bounds is considered a wall