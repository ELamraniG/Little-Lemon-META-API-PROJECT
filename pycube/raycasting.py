import math
import cube

def cast_ray(player_x, player_y, angle):

    map_x = int(player_x)
    map_y = int(player_y)

    if math.cos(angle) != 0:
        steps_in_angle_to_reach_next_x = abs(1 / math.cos(angle))
    else:
        steps_in_angle_to_reach_next_x = math.infinity
    if math.sin(angle) != 0:
        steps_in_angle_to_reach_next_y = abs(1 / math.sin(angle))
    else:
        steps_in_angle_to_reach_next_y = math.infinity
    
    # What direction to step in x or y (either +1 or -1)
    if math.cos(angle) < 0:
        x_intercept_distance = (player_x - map_x) * steps_in_angle_to_reach_next_x
    else:
        x_intercept_distance = (map_x + 1 - player_x) * steps_in_angle_to_reach_next_x
   
    if math.sin(angle) < 0:
        y_intercept_distance = (player_y - map_y) * steps_in_angle_to_reach_next_y
    else:
        y_intercept_distance = (map_y + 1 - player_y) * steps_in_angle_to_reach_next_y

    while True:
        if x_intercept_distance < y_intercept_distance:
            x_intercept_distance += steps_in_angle_to_reach_next_x
            map_x += -1 if math.cos(angle) < 0 else 1
            if is_wall(map_y, map_x):
                # Hit x-side
                if math.cos(angle) > 0:
                    hit_x = map_x
                else:
                    hit_x = map_x + 1
                hit_y = player_y + ((hit_x - player_x) / math.cos(angle)) * math.sin(angle)
                break
        else:
            y_intercept_distance += steps_in_angle_to_reach_next_y
            map_y += -1 if math.sin(angle) < 0 else 1
            if is_wall(map_y, map_x):
                # Hit y-side
                if math.sin(angle) > 0:
                    hit_y = map_y
                else:
                    hit_y = map_y + 1
                hit_x = player_x + ((hit_y - player_y) / math.sin(angle)) * math.cos(angle)
                break
   
    return hit_x, hit_y

def update_rays(canvas, ray_lines):
    """Update ray visualization on the screen"""
    for ray_line in ray_lines:
        if ray_line:
            canvas.delete(ray_line)
    ray_lines.clear()

    HALF_FOV = cube.FOV / 2
    for i in range(cube.NUM_RAYS):
        ray_angle = cube.player_angle - HALF_FOV + (i + 0.5) * (cube.FOV / cube.NUM_RAYS)

        end_x, end_y = cast_ray(cube.player_x, cube.player_y, ray_angle)

        start_x = cube.player_x * cube.CELL_SIZE
        start_y = cube.player_y * cube.CELL_SIZE

        end_x = end_x * cube.CELL_SIZE
        end_y = end_y * cube.CELL_SIZE

        ray_line = canvas.create_line(start_x, start_y, end_x, end_y, fill="red", width=2)
        ray_lines.append(ray_line)
    
    return ray_lines

def is_wall(row, col):
    r, c = int(row), int(col)
    if 0 <= r < cube.MAP_HEIGHT and 0 <= c < cube.MAP_WIDTH:
        return cube.MAP[r][c] == 1
    return True  # Out of bounds is considered a wall