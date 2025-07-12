import math

# Integer map
MAP = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

# Map and game constants
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)

CELL_SIZE = 100
PLAYER_DOT_SIZE = 5

MOVE_STEP = 0.05
ROTATION_STEP = 0.1
FOV = math.pi / 3
NUM_RAYS = 1000

THREE_D_WALL_HEIGHT = 100

player_y = 2.5
player_x = 2.5
player_angle = math.pi / -2
hits = []

if __name__ == "__main__":
    from map2d import main
    main()