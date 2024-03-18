# This file was created by: Miguel Castrillon

import pygame
import random
import sys
import os
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
NEON_GREEN = (57, 255, 20)

# Player settings
player_size = 90
player_speed = 5

# Enemy settings
enemy_size = 40
enemy_speed = 2
enemy_spawn_delay = 60

# Point and lives counters
points = 0
lives = 3
font = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Get the current script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Full path to the images
player_img_path = os.path.join(script_directory, "rocket.png")
alien_img_path = os.path.join(script_directory, "alien.png")
alien2_img_path = os.path.join(script_directory, "alien2.png")  # Second type of alien
background_img_path = os.path.join(script_directory, "background.png")

# Load images
player_img = pygame.image.load(player_img_path)
alien_img = pygame.image.load(alien_img_path)
alien2_img = pygame.image.load(alien2_img_path)  # Second type of alien
background_img = pygame.image.load(background_img_path)

# Scale the images
player_img = pygame.transform.scale(player_img, (player_size, player_size))
alien_img = pygame.transform.scale(alien_img, (enemy_size, enemy_size))
alien2_img = pygame.transform.scale(alien2_img, (enemy_size, enemy_size))  # Second type of alien

# Player
player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - player_size - 10, player_size, player_size)

# Player movement flags
move_left = False
move_right = False
move_up = False
move_down = False

# Enemies
enemies = []

# Bullets
bullets = []

# Functions
def draw_background():
    screen.blit(background_img, (0, 0))

def draw_player():
    screen.blit(player_img, player)

def draw_enemies():
    for enemy in enemies:
        if enemy["type"] == 1:
            screen.blit(alien_img, enemy["rect"])
        elif enemy["type"] == 2:
            screen.blit(alien2_img, enemy["rect"])

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, BRIGHT_GREEN, bullet)

def draw_points():
    points_text = font.render(f"Points: {points}", True, WHITE)
    screen.blit(points_text, (10, 10))

def draw_lives():
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 50))

def move_player():
    global move_left, move_right, move_up, move_down

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += player_speed

def move_enemies():
    for enemy in enemies:
        enemy["rect"].y += enemy_speed

def move_bullets():
    for bullet in bullets:
        bullet.y -= 5

def spawn_enemy():
    # Generate a random number between 1 and 6. If it's 6, spawn alien1, else spawn alien2
    enemy_type = random.randint(1, 6)
    if enemy_type == 6:
        enemy = {"rect": pygame.Rect(random.randint(0, WIDTH - enemy_size), 0, enemy_size, enemy_size), "type": 1}
    else:
        enemy = {"rect": pygame.Rect(random.randint(0, WIDTH - enemy_size), 0, enemy_size, enemy_size), "type": 2}
    enemies.append(enemy)

def check_collision():
    global points, lives

    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy["rect"]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                if enemy["type"] == 1:
                    points += 5
                elif enemy["type"] == 2:
                    points += 1  # Adjust points for the second type of alien

    for enemy in enemies:
        if player.colliderect(enemy["rect"]):
            lives -= 1
            enemies.remove(enemy)

# Main game loop
def main():
    global points, lives
    enemy_spawn_counter = 0

    start_time = time.time()  # Get the starting time of the game

    while lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.centerx - 2, player.top, 4, 10)
                    bullets.append(bullet)

        move_player()

        screen.fill(BLACK)
        draw_background()
        draw_player()
        draw_enemies()
        draw_bullets()
        draw_points()
        draw_lives()

        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
        screen.blit(time_text, (10, 90))  # Adjust the position as needed

        move_enemies()
        move_bullets()
        check_collision()

        enemy_spawn_counter += 1
        if enemy_spawn_counter == enemy_spawn_delay:
            spawn_enemy()
            enemy_spawn_counter = 0

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
