import pygame
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game mode (True = AI opponent, False = 2-player mode)
ai_enabled = True  

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
player = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(10, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball settings
BALL_SIZE = 20
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 5
ball_speed_y = 5

# Speeds
player_speed = 0
opponent_speed = 0
opponent_ai_speed = 5

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Keydown
        if event.type == pygame.KEYDOWN:
            # Player 1 (Right paddle)
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
            
            # Player 2 (Left paddle) - only in 2-player mode
            if not ai_enabled:
                if event.key == pygame.K_w:
                    opponent_speed = -6
                if event.key == pygame.K_s:
                    opponent_speed = 6

        # Keyup
        if event.type == pygame.KEYUP:
            # Player 1
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                player_speed = 0
            # Player 2
            if not ai_enabled and event.key in (pygame.K_w, pygame.K_s):
                opponent_speed = 0

    # Move paddles
    player.y += player_speed
    
    if ai_enabled:
        # AI opponent: follow the ball
        if opponent.centery < ball.centery:
            opponent.y += opponent_ai_speed
        elif opponent.centery > ball.centery:
            opponent.y -= opponent_ai_speed
    else:
        # Human-controlled opponent
        opponent.y += opponent_speed

    # Keep paddles inside screen
    player.y = max(0, min(HEIGHT - PADDLE_HEIGHT, player.y))
    opponent.y = max(0, min(HEIGHT - PADDLE_HEIGHT, opponent.y))

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    # Score system
    if ball.left <= 0:
        player_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x *= -1

    if ball.right >= WIDTH:
        opponent_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x *= -1

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Render scores
    player_text = font.render(f"{player_score}", True, WHITE)
    opponent_text = font.render(f"{opponent_score}", True, WHITE)
    screen.blit(player_text, (WIDTH - 50, 20))
    screen.blit(opponent_text, (30, 20))

    # Update
    pygame.display.flip()
    clock.tick(60)
