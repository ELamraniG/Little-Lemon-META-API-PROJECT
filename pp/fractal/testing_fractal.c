#include "raycast.h"
typedef struct s_data {
    void *mlx_ptr;
    void *win_ptr;
    float player_y_pos;
float player_x_pos;
} t_data;

typedef struct s_img {
    void *img_ptr;
    char *addr;
    int bits_per_pixel;
    int line_length;
    int endian;
} t_img;
 typedef   struct all_dataaa{
        t_data *data;
        t_img *img;
        char **map;
    }all_dataa;
#define WIN_WIDTH 800
#define WIN_HEIGHT 600
#define SCALL 100
void ft_pixel_put(t_img *img, int x, int y, int color)
{
    char *dst;
    
    dst = img->addr + (y * img->line_length + x * (img->bits_per_pixel / 8));
    *(unsigned int*)dst = color;
}

void render_image(t_img *img,t_data *data,char **map)
{
     for(int i = 0; i < 5; i += 1) {
    for(int j = 0; j < 5; j += 1) {
        if (map[i][j] == '1') {
            for(int k = 0; k < 100; k++) {
                for(int m = 0; m < 100; m++) {
                    ft_pixel_put(img, i * SCALL + k, j * SCALL + m, 0xFF0000);
                }
            }
        } else {
            for(int k = 0; k < 100; k++) {
                for(int m = 0; m < 100; m++) {
                    ft_pixel_put(img, i * SCALL + k, j * SCALL + m, 0xFFFFFF);
                }
            }
        }
    }
}
for(int i = 0; i < 25; i++)
{
    for(int j = 0; j < 25; j++)
    {
        ft_pixel_put(img, data->player_x_pos + i, data->player_y_pos + j, 0xFEFEF);
    }
}


    mlx_put_image_to_window(data->mlx_ptr, data->win_ptr, img->img_ptr, 0, 0);
}




int key_hook(int keycode, void *d)
{
    all_dataa *data = (all_dataa*)d;
    if (keycode == 65307)
    {
        mlx_destroy_window(data->data->mlx_ptr, data->data->win_ptr);
        exit(0);
    }
    if(keycode == 119)
    {
        data->data->player_y_pos -= 25;
        render_image(data->img,data->data,data->map);
    }
    if(keycode == 115)
    {
        data->data->player_y_pos += 25;
        render_image(data->img,data->data,data->map);
    }
     if(keycode == 97)
    {
        data->data->player_x_pos -= 25;
        render_image(data->img,data->data,data->map);
    }
     if(keycode == 100)
    {
        data->data->player_x_pos += 25;
        render_image(data->img,data->data,data->map);
    }
    printf("%d\n",keycode);
    return (0);
}
int mouse_hook(int button, int x, int y, void *param)
{
    printf("Mouse button %d pressed at (%d, %d)\n", button, x, y);
    return (0);
}

int close_hook(t_data *data)
{
    mlx_destroy_window(data->mlx_ptr, data->win_ptr);
    exit(0);
    return (0);
}
void init_img(t_img *img, void *mlx_ptr, int width, int height)
{
    img->img_ptr = mlx_new_image(mlx_ptr, width, height);
    img->addr = mlx_get_data_addr(img->img_ptr, &img->bits_per_pixel, 
                                  &img->line_length, &img->endian);
}

int main()
{
    t_data data;
    t_img img;
    data.mlx_ptr = mlx_init();
    data.win_ptr = mlx_new_window(data.mlx_ptr, 500, 500, "MLX Square Drawing");
    data.player_y_pos = 200.5;
    data.player_x_pos = 200.5;
    char *map[5] = {
        "11111",
        "10001",
        "10001",
        "10001",
        "11111"
    };

    all_dataa all_data;
    all_data.img = &img;
    all_data.data = &data;
    all_data.map = map;
    init_img(&img, data.mlx_ptr, 500, 500);
    render_image(&img,&data,map);
    mlx_key_hook(data.win_ptr, key_hook, &all_data);
    mlx_mouse_hook(data.win_ptr, mouse_hook, &all_data);
    mlx_hook(data.win_ptr, 6, 1L<<6, mouse_hook, &all_data);
    mlx_hook(data.win_ptr, 17, 0, close_hook, &all_data);  
    mlx_loop(data.mlx_ptr);
    
    return (0);
}
