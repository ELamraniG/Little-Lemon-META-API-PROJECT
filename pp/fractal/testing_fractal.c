#include "raycast.h"

#define WIN_WIDTH 800
#define WIN_HEIGHT 600
#define SCALL 100

typedef struct s_data {
    void *mlx_ptr;
    void *win_ptr;
} t_data;

typedef struct s_img {
    void *img_ptr;
    char *addr;
    int bits_per_pixel;
    int line_length;
    int endian;
} t_img;

void ft_pixel_put(t_img *img, int x, int y, int color)
{
    char *dst;
    
    dst = img->addr + (y * img->line_length + x * (img->bits_per_pixel / 8));
    *(unsigned int*)dst = color;
}



int key_hook(int keycode, t_data *data)
{
    if (keycode == 65307)
    {
        mlx_destroy_window(data->mlx_ptr, data->win_ptr);
        exit(0);
    }
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
    char map[5][6] = {
        "11111"
        "10001"
        "10001"
        "10000"
        "11111"
    };
    init_img(&img, data.mlx_ptr, 500, 500);
    for(int i = 0; i < 500;i += 100)
    {
        for(int j = 0;j < 500;j += 100)
        {
            if (map[i / SCALL][j / SCALL] == '1')
            {
                for(int k = 0; k < 100; k++)
                {
                     for(int m = 0; m < 100; m++)
                    {
                         ft_pixel_put(&img,i + k,j + m,0xFFFFFF);
                        }
                    }
                }
            else
                ft_pixel_put(&img,i,j,0xFF);
            j += 99;
        }
    }
    mlx_put_image_to_window(data.mlx_ptr, data.win_ptr, img.img_ptr, 0, 0);
    mlx_key_hook(data.win_ptr, key_hook, &data);
    mlx_mouse_hook(data.win_ptr, mouse_hook, &data);
    mlx_hook(data.win_ptr, 17, 0, close_hook, &data);  
    mlx_loop(data.mlx_ptr);
    
    return (0);
}
