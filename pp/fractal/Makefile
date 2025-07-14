NAME = raycast_demo

FLAGS = #-Wall -Wextra -Werror

CC = cc $(FLAGS)

FOLDER = mlx_linux

SRC = testing_fractal.c

OBJ = $(SRC:%.c=%.o)

MLX = $(FOLDER)/libmlx.a

FRAMEWORKS = -lX11 -lXext -lm

all : $(NAME)

$(NAME) : $(OBJ)
	$(MAKE) -C $(FOLDER)
	$(CC) $(OBJ) $(MLX) $(FRAMEWORKS) -o $(NAME)

%.o: %.c
	$(CC) -I/usr/include -Imlx_linux -O3 -c $< -o $@

clean :
	rm -f $(OBJ)
	$(MAKE) clean -C $(FOLDER)

fclean : clean
	rm -f $(NAME)

re : fclean all

.PHONY: all clean fclean re
