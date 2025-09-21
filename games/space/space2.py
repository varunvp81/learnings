import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Plus")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Player
player_width, player_height = 60, 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 50
player_speed = 6
player_lives = 3
shield_active = False
shield_timer = 0

# Player bullets
bullet_width, bullet_height = 5, 10
bullets = []
bullet_speed = -8
multi_shot = False
multi_timer = 0

# Enemy
enemy_width, enemy_height = 40, 20
enemy_rows = 4
enemy_cols = 8
enemies = []
enemy_speed_x = 2
enemy_direction = 1

# Enemy bullets
enemy_bullets = []
enemy_bullet_speed = 5
enemy_fire_rate = 0.01  # Probability each frame

# Score & wave
score = 0
wave = 1

# Create enemies
def create_enemies():
    enemies.clear()
    for row in range(enemy_rows):
        for col in range(enemy_cols):
            x = 100 + col * (enemy_width + 20)
            y = 50 + row * (enemy_height + 20)
            enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

create_enemies()

def draw_text(text, font, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

def game_over():
    screen.fill(BLACK)
    draw_text("GAME OVER", big_font, RED, WIDTH//2 - 150, HEIGHT//2 - 50)
    draw_text(f"Score: {score}", font, WHITE, WIDTH//2 - 50, HEIGHT//2 + 50)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if multi_shot:
                    # Shoot 3 bullets
                    bullets.append(pygame.Rect(player_x + player_width//2 - 15, player_y, bullet_width, bullet_height))
                    bullets.append(pygame.Rect(player_x + player_width//2, player_y, bullet_width, bullet_height))
                    bullets.append(pygame.Rect(player_x + player_width//2 + 15, player_y, bullet_width, bullet_height))
                else:
                    bullets.append(pygame.Rect(player_x + player_width//2 - bullet_width//2, player_y, bullet_width, bullet_height))

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

    # Move enemy bullets
    for e_bullet in enemy_bullets[:]:
        e_bullet.y += enemy_bullet_speed
        if e_bullet.y > HEIGHT:
            enemy_bullets.remove(e_bullet)
        # Check collision with player
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(e_bullet):
            if shield_active:
                enemy_bullets.remove(e_bullet)
            else:
                enemy_bullets.remove(e_bullet)
                player_lives -= 1
                if player_lives <= 0:
                    game_over()

    # Move enemies
    move_down = False
    for enemy in enemies:
        enemy.x += enemy_speed_x * enemy_direction
        if enemy.right >= WIDTH - 10 or enemy.left <= 10:
            move_down = True
        # Randomly fire bullets
        if random.random() < enemy_fire_rate:
            enemy_bullets.append(pygame.Rect(enemy.x + enemy_width//2, enemy.y + enemy_height, 5, 10))

    if move_down:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += 20

    # Collision: player bullets & enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                # Random powerup
                if random.random() < 0.1:
                    # 50% chance shield or multi-shot
                    if random.random() < 0.5:
                        shield_active = True
                        shield_timer = 300  # lasts 5 seconds (assuming 60 FPS)
                    else:
                        multi_shot = True
                        multi_timer = 300
                break

    # Check if wave cleared
    if not enemies:
        wave += 1
        enemy_rows = min(6, enemy_rows + 1)  # increase difficulty
        create_enemies()

    # Power-up timers
    if shield_active:
        shield_timer -= 1
        if shield_timer <= 0:
            shield_active = False
    if multi_shot:
        multi_timer -= 1
        if multi_timer <= 0:
            multi_shot = False

    # Drawing
    screen.fill(BLACK)
    # Draw player
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))
    if shield_active:
        pygame.draw.circle(screen, YELLOW, (player_x + player_width//2, player_y + player_height//2), 40, 2)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    for e_bullet in enemy_bullets:
        pygame.draw.rect(screen, RED, e_bullet)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, WHITE, enemy)

    # Draw score & lives & wave
    draw_text(f"Score: {score}", font, WHITE, 10, 10)
    draw_text(f"Lives: {player_lives}", font, WHITE, WIDTH - 120, 10)
    draw_text(f"Wave: {wave}", font, WHITE, WIDTH//2 - 50, 10)

    pygame.display.flip()
    clock.tick(60)
