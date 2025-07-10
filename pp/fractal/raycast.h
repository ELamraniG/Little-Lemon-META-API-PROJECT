#ifndef RAYCAST_H
# define RAYCAST_H

# include "mlx_linux/mlx.h"
# include <stdio.h>
# include <stdlib.h>
# include <math.h>
# include <unistd.h>
# include <fcntl.h>

# define MAP_WIDTH 314
# define MAP_HEIGHT 224
# define WINDOW_WIDTH 1920
# define WINDOW_HEIGHT 1080
# define MAP_SCALE 1
# define FOV 60
# define NUM_RAYS (2000)

# define MOVE_SPEED 0.08
# define TURN_SPEED 0.05
# define PI 3.14159265359

// Key codes
# define KEY_ESC 65307
# define KEY_W 119
# define KEY_S 115
# define KEY_A 97
# define KEY_D 100
# define KEY_LEFT 65361
# define KEY_RIGHT 65363

// Colors
# define COLOR_WHITE 0xFFFFFF
# define COLOR_BLACK 0x000000
# define COLOR_RED 0xFF0000
# define COLOR_GREEN 0x00FF00
# define COLOR_BLUE 0x0000FF
# define COLOR_YELLOW 0xFFFF00
# define COLOR_GRAY 0x808080

typedef struct s_point
{
	float x;
	float y;
} t_point;

typedef struct s_player
{
	t_point pos;
	float angle;
	float speed;
	float turn_speed;
} t_player;

typedef struct s_ray
{
	t_point start;
	t_point end;
	float angle;
	float distance;
	int hit_wall;
} t_ray;

typedef struct s_game
{
	void *mlx;
	void *window;
	void *img;
	char *addr;
	int bits_per_pixel;
	int line_length;
	int endian;
	
	char map[MAP_HEIGHT][MAP_WIDTH];
	t_player player;
	t_ray rays[NUM_RAYS];
	
	int key_w;
	int key_s;
	int key_a;
	int key_d;
	int key_left;
	int key_right;
} t_game;

// Function prototypes
int init_game(t_game *game);
int load_map(t_game *game, char *filename);
void put_pixel(t_game *game, int x, int y, int color);
void draw_line(t_game *game, t_point start, t_point end, int color);
void draw_map(t_game *game);
void draw_player(t_game *game);
void cast_rays(t_game *game);
void draw_3d_view(t_game *game);
void update_player(t_game *game);
int key_press(int keycode, t_game *game);
int key_release(int keycode, t_game *game);
int game_loop(t_game *game);
int close_game(t_game *game);
float normalize_angle(float angle);
int is_wall(t_game *game, float x, float y);

#endif
