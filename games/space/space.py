import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()

# Player settings
player_width, player_height = 60, 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 40
player_speed = 6

# Bullet settings
bullet_width, bullet_height = 5, 10
bullets = []
bullet_speed = -8

# Enemy settings
enemy_width, enemy_height = 40, 20
enemies = []
enemy_rows = 4
enemy_cols = 8
enemy_speed_x = 2
enemy_direction = 1  # 1 = right, -1 = left

# Score
score = 0
font = pygame.font.Font(None, 36)

# Create enemies
def create_enemies():
    enemies.clear()
    for row in range(enemy_rows):
        for col in range(enemy_cols):
            x = 100 + col * (enemy_width + 20)
            y = 50 + row * (enemy_height + 20)
            enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

create_enemies()

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player_x + player_width // 2 - bullet_width // 2,
                                     player_y, bullet_width, bullet_height)
                bullets.append(bullet)

    # Keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Move bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Move enemies
    move_down = False
    for enemy in enemies:
        enemy.x += enemy_speed_x * enemy_direction
        if enemy.right >= WIDTH - 10 or enemy.left <= 10:
            move_down = True

    if move_down:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += 20

    # Collision detection
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Check if enemies reach bottom
    for enemy in enemies:
        if enemy.bottom >= HEIGHT:
            pygame.quit()
            sys.exit()

    # Drawing
    screen.fill(BLACK)

    # Draw player
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
