import pygame
import time
import random
import os

# Initialize pygame
pygame.init()

# Screen size
width = 600
height = 400

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 0)
purple = (160, 32, 240)

# Create screen
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption("🐍 Snake Game Plus")

# Clock
clock = pygame.time.Clock()

# Snake block size
snake_block = 10

# Initial speed
snake_speed = 15

# Font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)

# High score file
HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip() or 0)
    return 0


def save_high_score(score):
    high_score = load_high_score()
    if score > high_score:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def your_score(score, high_score):
    value = score_font.render(f"Score: {score}  High: {high_score}", True, red)
    dis.blit(value, [10, 10])


def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 3 + y_offset])


def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Obstacles
    obstacles = [[random.randrange(0, width, 10), random.randrange(0, height, 10)] for _ in range(10)]

    # Special foods
    special_food = None
    poison_food = None

    # Power-up
    power_up = None
    power_up_timer = 0
    power_active = None

    global snake_speed
    high_score = load_high_score()

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(length_of_snake - 1, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        save_high_score(length_of_snake - 1)
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        save_high_score(length_of_snake - 1)
                        snake_speed = 15
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(length_of_snake - 1)
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Check wall collision
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        # Draw regular food
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # Draw obstacles
        for obs in obstacles:
            pygame.draw.rect(dis, purple, [obs[0], obs[1], snake_block, snake_block])

        # Randomly spawn special food
        if special_food is None and random.randint(0, 100) < 2:
            special_food = [random.randrange(0, width, 10), random.randrange(0, height, 10)]
        if special_food:
            pygame.draw.rect(dis, yellow, [special_food[0], special_food[1], snake_block, snake_block])

        # Randomly spawn poison food
        if poison_food is None and random.randint(0, 100) < 2:
            poison_food = [random.randrange(0, width, 10), random.randrange(0, height, 10)]
        if poison_food:
            pygame.draw.rect(dis, red, [poison_food[0], poison_food[1], snake_block, snake_block])

        # Randomly spawn power-up
        if power_up is None and random.randint(0, 200) < 1:
            power_up = [random.randrange(0, width, 10), random.randrange(0, height, 10)]
        if power_up:
            pygame.draw.rect(dis, white, [power_up[0], power_up[1], snake_block, snake_block])

        # Snake mechanics
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check collisions
        for x in snake_list[:-1]:
            if x == snake_head and power_active != "invincible":
                game_close = True

        for obs in obstacles:
            if snake_head == obs and power_active != "invincible":
                game_close = True

        # Check food eaten
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            snake_speed += 1

        if special_food and x1 == special_food[0] and y1 == special_food[1]:
            length_of_snake += 3  # bonus
            snake_speed += 2
            special_food = None

        if poison_food and x1 == poison_food[0] and y1 == poison_food[1]:
            length_of_snake = max(1, length_of_snake - 2)
            poison_food = None

        if power_up and x1 == power_up[0] and y1 == power_up[1]:
            power_active = random.choice(["slow", "double", "invincible"])
            power_up = None
            power_up_timer = 100  # lasts for some ticks

        # Power-up effects
        if power_active == "slow":
            snake_speed = max(10, snake_speed - 5)
        elif power_active == "double":
            pass  # applied on score display
        elif power_active == "invincible":
            pass

        if power_active:
            power_up_timer -= 1
            if power_up_timer <= 0:
                power_active = None

        our_snake(snake_block, snake_list)
        score_value = length_of_snake - 1
        if power_active == "double":
            score_value *= 2
        your_score(score_value, high_score)

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_loop()
