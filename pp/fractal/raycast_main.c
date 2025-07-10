#include "raycast.h"

int main(void)
{
	t_game game;
	
	printf("=== Raycasting Demo ===\n");
	printf("Controls:\n");
	printf("  WASD: Move player\n");
	printf("  Left/Right arrows: Turn player\n");
	printf("  ESC: Exit\n\n");
	
	// Initialize game
	if (!init_game(&game))
	{
		printf("Error: Failed to initialize game\n");
		return (1);
	}
	
	// Load map
	if (!load_map(&game, "cub.txt"))
	{
		printf("Error: Failed to load map from cub.txt\n");
		return (1);
	}
	
	printf("Map loaded successfully!\n");
	printf("Left side: 2D map view with player (red dot) and rays (yellow)\n");
	printf("Right side: 3D raycasted view\n\n");
	
	// Set up event handlers
	mlx_hook(game.window, 2, 1L<<0, key_press, &game);   // KeyPress
	mlx_hook(game.window, 3, 1L<<1, key_release, &game); // KeyRelease
	mlx_hook(game.window, 17, 0, close_game, &game);     // Close button
	mlx_loop_hook(game.mlx, game_loop, &game);
	
	// Start the game loop
	mlx_loop(game.mlx);
	
	return (0);
}
