import pygame
import time
import random

pygame.init()

# Display window size
dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Load images
snake_img = pygame.image.load('snake_body.png')
food_img = pygame.image.load('food.png')
background_img = pygame.image.load('background.png')

# Set the title of the window
pygame.display.set_caption('Customizable Snake Game')

clock = pygame.time.Clock()

# Customization Options
snake_speed_options = {'slow': 10, 'medium': 15, 'fast': 20}
game_modes = ['classic', 'time_trial', 'survival']

# Set default values
snake_speed = snake_speed_options['medium']  # Can be 'slow', 'medium', or 'fast'
game_mode = 'classic'  # Can be 'classic', 'time_trial', or 'survival'

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        dis.blit(snake_img, (x[0], x[1]))

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def gameLoop(game_mode, snake_speed):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Additional variables for new modes
    start_time = pygame.time.get_ticks()
    time_limit = 60000  # 1 minute for Time Trial Mode
    boundary_shrink_timer = pygame.time.get_ticks()
    boundary_margin = 0

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("You lost! Press Q-Quit or C-Play Again", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(game_mode, snake_speed)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Game mode logic
        if game_mode == 'time_trial' and (pygame.time.get_ticks() - start_time) > time_limit:
            game_close = True
        if game_mode == 'survival':
            current_time = pygame.time.get_ticks()
            if current_time - boundary_shrink_timer > 10000:  # Boundary shrinks every 10 seconds
                boundary_margin += 10
                boundary_shrink_timer = current_time

        # Movement and collision logic
        if x1 >= dis_width - boundary_margin or x1 < boundary_margin or y1 >= dis_height - boundary_margin or y1 < boundary_margin:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.blit(background_img, (0, 0))
        if game_mode == 'survival':
            pygame.draw.rect(dis, red, [boundary_margin, boundary_margin, dis_width - 2 * boundary_margin, dis_height - 2 * boundary_margin], 1)
        dis.blit(food_img, (foodx, foody))
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(boundary_margin, dis_width - snake_block
