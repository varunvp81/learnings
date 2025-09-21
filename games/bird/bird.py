import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Clock
clock = pygame.time.Clock()

# Bird settings
bird_size = 30
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -8

# Pipe settings
pipe_width = 60
pipe_gap = 150
pipe_speed = 4
pipes = []

# Score
score = 0
font = pygame.font.Font(None, 50)

def draw_bird(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, bird_size, bird_size))

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe["top"])
        pygame.draw.rect(screen, GREEN, pipe["bottom"])

def check_collision(bird_rect, pipes):
    # Check ground and ceiling
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    # Check pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            return True
    return False

def reset_game():
    global bird_y, bird_velocity, pipes, score
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Bird jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    # Bird movement
    bird_velocity += gravity
    bird_y += bird_velocity
    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)

    # Pipe movement and generation
    if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - 200:
        pipe_height = random.randint(100, 400)
        top_rect = pygame.Rect(WIDTH, 0, pipe_width, pipe_height)
        bottom_rect = pygame.Rect(WIDTH, pipe_height + pipe_gap, pipe_width, HEIGHT)
        pipes.append({"x": WIDTH, "top": top_rect, "bottom": bottom_rect})

    for pipe in pipes:
        pipe["x"] -= pipe_speed
        pipe["top"].x = pipe["x"]
        pipe["bottom"].x = pipe["x"]

    # Remove off-screen pipes
    if pipes and pipes[0]["x"] < -pipe_width:
        pipes.pop(0)
        score += 1

    # Collision check
    if check_collision(bird_rect, pipes):
        reset_game()

    # Drawing
    screen.fill(BLUE)
    draw_bird(bird_x, bird_y)
    draw_pipes(pipes)

    # Draw score
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 10, 20))

    pygame.display.flip()
    clock.tick(60)
