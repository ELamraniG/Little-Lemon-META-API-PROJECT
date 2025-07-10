#include "raycast.h"

int init_game(t_game *game)
{
	game->mlx = mlx_init();
	if (!game->mlx)
		return (0);
	
	game->window = mlx_new_window(game->mlx, WINDOW_WIDTH, WINDOW_HEIGHT, "Raycasting Demo");
	if (!game->window)
		return (0);
	
	game->img = mlx_new_image(game->mlx, WINDOW_WIDTH, WINDOW_HEIGHT);
	if (!game->img)
		return (0);
	
	game->addr = mlx_get_data_addr(game->img, &game->bits_per_pixel, 
									&game->line_length, &game->endian);
	
	// Initialize player
	game->player.pos.x = 2.5;
	game->player.pos.y = 2.5;
	game->player.angle = PI * -0.5;
	game->player.speed = MOVE_SPEED;
	game->player.turn_speed = TURN_SPEED;
	
	// Initialize key states
	game->key_w = 0;
	game->key_s = 0;
	game->key_a = 0;
	game->key_d = 0;
	game->key_left = 0;
	game->key_right = 0;
	
	return (1);
}

int load_map(t_game *game, char *filename)
{
	int fd;
	char buffer[1024];
	int bytes_read;
	int i, j, pos;
	
	fd = open(filename, O_RDONLY);
	if (fd < 0)
		return (0);
	
	bytes_read = read(fd, buffer, sizeof(buffer) - 1);
	close(fd);
	
	if (bytes_read <= 0)
		return (0);
	
	buffer[bytes_read] = '\0';
	
	// Parse the map
	pos = 0;
	for (i = 0; i < MAP_HEIGHT && pos < bytes_read; i++)
	{
		for (j = 0; j < MAP_WIDTH && pos < bytes_read; j++)
		{
			if (buffer[pos] == '\n')
			{
				pos++;
				j--;
				continue;
			}
			game->map[i][j] = buffer[pos];
			pos++;
		}
		// Skip to next line
		while (pos < bytes_read && buffer[pos] != '\n')
			pos++;
		if (pos < bytes_read)
			pos++;
	}
	
	return (1);
}

void put_pixel(t_game *game, int x, int y, int color)
{
	char *dst;
	
	if (x < 0 || x >= WINDOW_WIDTH || y < 0 || y >= WINDOW_HEIGHT)
		return;
	
	dst = game->addr + (y * game->line_length + x * (game->bits_per_pixel / 8));
	*(unsigned int*)dst = color;
}

void draw_line(t_game *game, t_point start, t_point end, int color)
{
	float dx = end.x - start.x;
	float dy = end.y - start.y;
	float steps = fmax(fabs(dx), fabs(dy));
	
	float x_inc = dx / steps;
	float y_inc = dy / steps;
	
	float x = start.x;
	float y = start.y;
	
	for (int i = 0; i <= steps; i++)
	{
		put_pixel(game, (int)x, (int)y, color);
		x += x_inc;
		y += y_inc;
	}
}

void draw_map(t_game *game)
{
	int i, j;
	int screen_x, screen_y;
	
	// Draw map tiles
	for (i = 0; i < MAP_HEIGHT; i++)
	{
		for (j = 0; j < MAP_WIDTH; j++)
		{
			screen_x = j * MAP_SCALE;
			screen_y = i * MAP_SCALE;
			
			int color = (game->map[i][j] == '1') ? COLOR_WHITE : COLOR_BLACK;
			
			// Draw tile
			for (int y = 0; y < MAP_SCALE; y++)
			{
				for (int x = 0; x < MAP_SCALE; x++)
				{
					put_pixel(game, screen_x + x, screen_y + y, color);
				}
			}
		}
	}
	
	// Draw grid lines
	for (i = 0; i <= MAP_WIDTH; i++)
	{
		t_point start = {i * MAP_SCALE, 0};
		t_point end = {i * MAP_SCALE, MAP_HEIGHT * MAP_SCALE};
		draw_line(game, start, end, COLOR_GRAY);
	}
	
	for (i = 0; i <= MAP_HEIGHT; i++)
	{
		t_point start = {0, i * MAP_SCALE};
		t_point end = {MAP_WIDTH * MAP_SCALE, i * MAP_SCALE};
		draw_line(game, start, end, COLOR_GRAY);
	}
}

void draw_player(t_game *game)
{
	int player_x = (int)(game->player.pos.x * MAP_SCALE);
	int player_y = (int)(game->player.pos.y * MAP_SCALE);
	
	// Draw player as a red circle
	for (int y = -3; y <= 3; y++)
	{
		for (int x = -3; x <= 3; x++)
		{
			if (x * x + y * y <= 9)
				put_pixel(game, player_x + x, player_y + y, COLOR_RED);
		}
	}
	
	// Draw direction line
	t_point start = {player_x, player_y};
	t_point end = {
		player_x + cos(game->player.angle) * 15,
		player_y + sin(game->player.angle) * 15
	};
	draw_line(game, start, end, COLOR_RED);
}

int is_wall(t_game *game, float x, float y)
{
	int map_x = (int)x;
	int map_y = (int)y;
	
	if (map_x < 0 || map_x >= MAP_WIDTH || map_y < 0 || map_y >= MAP_HEIGHT)
		return (1);
	
	return (game->map[map_y][map_x] == '1');
}

void cast_rays(t_game *game)
{
	float ray_angle;
	float angle_step = (FOV * PI / 180.0) / NUM_RAYS;
	float start_angle = game->player.angle - (FOV * PI / 180.0) / 2;
	
	for (int i = 0; i < NUM_RAYS; i++)
	{
		ray_angle = start_angle + i * angle_step;
		ray_angle = normalize_angle(ray_angle);
		
		game->rays[i].start.x = game->player.pos.x;
		game->rays[i].start.y = game->player.pos.y;
		game->rays[i].angle = ray_angle;
		game->rays[i].hit_wall = 0;
		
		// DDA algorithm variables
		float ray_dir_x = cos(ray_angle);
		float ray_dir_y = sin(ray_angle);
		
		// Current position
		int map_x = (int)game->player.pos.x;
		int map_y = (int)game->player.pos.y;
		
		// Length of ray from current position to x or y side
		float side_dist_x, side_dist_y;
		
		// Calculate delta distances
		float delta_dist_x = (ray_dir_x == 0) ? 1e30 : fabs(1 / ray_dir_x);
		float delta_dist_y = (ray_dir_y == 0) ? 1e30 : fabs(1 / ray_dir_y);
		
		// What direction to step in x or y-direction (either +1 or -1)
		int step_x, step_y;
		
		int hit = 0; // was there a wall hit?
		int side; // was a NS or a EW wall hit?
		
		// Calculate step and initial sideDist
		if (ray_dir_x < 0)
		{
			step_x = -1;
			side_dist_x = (game->player.pos.x - map_x) * delta_dist_x;
		}
		else
		{
			step_x = 1;
			side_dist_x = (map_x + 1.0 - game->player.pos.x) * delta_dist_x;
		}
		if (ray_dir_y < 0)
		{
			step_y = -1;
			side_dist_y = (game->player.pos.y - map_y) * delta_dist_y;
		}
		else
		{
			step_y = 1;
			side_dist_y = (map_y + 1.0 - game->player.pos.y) * delta_dist_y;
		}
		
		// Perform DDA
		while (hit == 0)
		{
			// Jump to next map square, either in x-direction, or in y-direction
			if (side_dist_x < side_dist_y)
			{
				side_dist_x += delta_dist_x;
				map_x += step_x;
				side = 0;
			}
			else
			{
				side_dist_y += delta_dist_y;
				map_y += step_y;
				side = 1;
			}
			// Check if ray has hit a wall
			if (is_wall(game, map_x, map_y))
				hit = 1;
		}
		
		// Calculate distance
		float perp_wall_dist;
		if (side == 0)
			perp_wall_dist = (map_x - game->player.pos.x + (1 - step_x) / 2) / ray_dir_x;
		else
			perp_wall_dist = (map_y - game->player.pos.y + (1 - step_y) / 2) / ray_dir_y;
		
		game->rays[i].distance = perp_wall_dist;
		game->rays[i].hit_wall = hit;
		
		// Calculate exact hit point
		game->rays[i].end.x = game->player.pos.x + ray_dir_x * perp_wall_dist;
		game->rays[i].end.y = game->player.pos.y + ray_dir_y * perp_wall_dist;
		
		// Draw ray on 2D map
		t_point start = {game->rays[i].start.x * MAP_SCALE, game->rays[i].start.y * MAP_SCALE};
		t_point end = {game->rays[i].end.x * MAP_SCALE, game->rays[i].end.y * MAP_SCALE};
		draw_line(game, start, end, COLOR_YELLOW);
	}
}

void draw_3d_view(t_game *game)
{
	int view_start_x = MAP_WIDTH * MAP_SCALE + 20;
	int view_width = WINDOW_WIDTH - view_start_x - 20;
	int view_height = WINDOW_HEIGHT - 40;
	int ray_width = view_width / NUM_RAYS;
	
	// Clear 3D view area
	for (int y = 20; y < WINDOW_HEIGHT - 20; y++)
	{
		for (int x = view_start_x; x < WINDOW_WIDTH - 20; x++)
		{
			put_pixel(game, x, y, COLOR_BLACK);
		}
	}
	
	for (int i = 0; i < NUM_RAYS; i++)
	{
		if (game->rays[i].hit_wall)
		{
			// Correct for fish-eye effect
			float corrected_distance = game->rays[i].distance * cos(game->rays[i].angle - game->player.angle);
			
			// Calculate wall height on screen
			int wall_height = (int)(view_height / (corrected_distance + 0.1));
			
			// Calculate wall color based on distance (darker = farther)
			int brightness = (int)(255 / (1 + corrected_distance * 0.2));
			if (brightness > 255) brightness = 255;
			if (brightness < 50) brightness = 50;
			
			int wall_color = (brightness << 16) | (brightness << 8) | brightness;
			
			int wall_start = (view_height - wall_height) / 2 + 20;
			int wall_end = wall_start + wall_height;
			
			// Draw wall slice
			for (int x = 0; x < ray_width; x++)
			{
				for (int y = wall_start; y < wall_end && y < WINDOW_HEIGHT - 20; y++)
				{
					int screen_x = view_start_x + i * ray_width + x;
					put_pixel(game, screen_x, y, wall_color);
				}
			}
		}
	}
	
	// Draw border around 3D view
	for (int i = 0; i < view_width; i++)
	{
		put_pixel(game, view_start_x + i, 20, COLOR_WHITE);
		put_pixel(game, view_start_x + i, WINDOW_HEIGHT - 21, COLOR_WHITE);
	}
	for (int i = 20; i < WINDOW_HEIGHT - 20; i++)
	{
		put_pixel(game, view_start_x, i, COLOR_WHITE);
		put_pixel(game, WINDOW_WIDTH - 21, i, COLOR_WHITE);
	}
}

float normalize_angle(float angle)
{
	while (angle < 0)
		angle += 2 * PI;
	while (angle >= 2 * PI)
		angle -= 2 * PI;
	return (angle);
}

void update_player(t_game *game)
{
	float new_x = game->player.pos.x;
	float new_y = game->player.pos.y;
	
	// Movement
	if (game->key_w)
	{
		new_x += cos(game->player.angle) * game->player.speed;
		new_y += sin(game->player.angle) * game->player.speed;
	}
	if (game->key_s)
	{
		new_x -= cos(game->player.angle) * game->player.speed;
		new_y -= sin(game->player.angle) * game->player.speed;
	}
	if (game->key_a)
	{
		new_x -= cos(game->player.angle + PI/2) * game->player.speed;
		new_y -= sin(game->player.angle + PI/2) * game->player.speed;
	}
	if (game->key_d)
	{
		new_x += cos(game->player.angle + PI/2) * game->player.speed;
		new_y += sin(game->player.angle + PI/2) * game->player.speed;
	}
	
	// Check collision
	if (!is_wall(game, new_x, game->player.pos.y))
		game->player.pos.x = new_x;
	if (!is_wall(game, game->player.pos.x, new_y))
		game->player.pos.y = new_y;
	
	// Rotation
	if (game->key_left)
		game->player.angle -= game->player.turn_speed;
	if (game->key_right)
		game->player.angle += game->player.turn_speed;
	
	game->player.angle = normalize_angle(game->player.angle);
}

int key_press(int keycode, t_game *game)
{
	if (keycode == KEY_ESC)
		close_game(game);
	else if (keycode == KEY_W)
		game->key_w = 1;
	else if (keycode == KEY_S)
		game->key_s = 1;
	else if (keycode == KEY_A)
		game->key_a = 1;
	else if (keycode == KEY_D)
		game->key_d = 1;
	else if (keycode == KEY_LEFT)
		game->key_left = 1;
	else if (keycode == KEY_RIGHT)
		game->key_right = 1;
	
	return (0);
}

int key_release(int keycode, t_game *game)
{
	if (keycode == KEY_W)
		game->key_w = 0;
	else if (keycode == KEY_S)
		game->key_s = 0;
	else if (keycode == KEY_A)
		game->key_a = 0;
	else if (keycode == KEY_D)
		game->key_d = 0;
	else if (keycode == KEY_LEFT)
		game->key_left = 0;
	else if (keycode == KEY_RIGHT)
		game->key_right = 0;
	
	return (0);
}

int game_loop(t_game *game)
{
	// Clear the image
	for (int i = 0; i < WINDOW_WIDTH * WINDOW_HEIGHT; i++)
		((int*)game->addr)[i] = COLOR_BLACK;
	
	// Update game state
	update_player(game);
	
	// Draw everything
	draw_map(game);
	draw_player(game);
	cast_rays(game);
	draw_3d_view(game);
	
	// Display the image
	mlx_put_image_to_window(game->mlx, game->window, game->img, 0, 0);
	
	return (0);
}

int close_game(t_game *game)
{
	if (game->img)
		mlx_destroy_image(game->mlx, game->img);
	if (game->window)
		mlx_destroy_window(game->mlx, game->window);
	if (game->mlx)
		mlx_destroy_display(game->mlx);
	exit(0);
	return (0);
}
