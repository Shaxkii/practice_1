import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen size
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Dodge Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (50, 150, 255)
RED = (255, 70, 70)
YELLOW = (255, 220, 50)

# FPS settings
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)


# Reset the game state
def reset_game():
    # Create the player at the center of the screen
    player = pygame.Rect(
        WIDTH // 2 - 20,
        HEIGHT // 2 - 20,
        40,
        40
    )

    # List to store bullets
    bullets = []

    # Store the game start time
    start_time = pygame.time.get_ticks()

    # Store the time when the last bullet was created
    last_bullet_time = 0

    return player, bullets, start_time, last_bullet_time


# Create a bullet that moves toward the player
def create_bullet(player):
    bullet_radius = 8
    bullet_speed = 4

    # Randomly choose the side where the bullet will appear
    side = random.randint(0, 3)

    if side == 0:  # Top
        x = random.randint(0, WIDTH)
        y = -20

    elif side == 1:  # Bottom
        x = random.randint(0, WIDTH)
        y = HEIGHT + 20

    elif side == 2:  # Left
        x = -20
        y = random.randint(0, HEIGHT)

    else:  # Right
        x = WIDTH + 20
        y = random.randint(0, HEIGHT)

    # Get the center position of the player
    player_x = player.centerx
    player_y = player.centery

    # Calculate the direction from the bullet to the player
    dx = player_x - x
    dy = player_y - y

    # Calculate the distance between the bullet and the player
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # Normalize the direction vector
    dx /= distance
    dy /= distance

    # Store bullet information
    bullet = {
        "x": float(x),
        "y": float(y),
        "dx": dx,
        "dy": dy,
        "speed": bullet_speed,
        "radius": bullet_radius
    }

    return bullet


# Initialize the game
player, bullets, start_time, last_bullet_time = reset_game()

# Player movement speed
player_speed = 6

# Game over state
game_over = False

# Store the final survival time when the player dies
final_survival_time = 0

# Main program state
running = True


# Main game loop
while running:

    current_time = pygame.time.get_ticks()

    # Handle events
    for event in pygame.event.get():

        # Close the game window
        if event.type == pygame.QUIT:
            running = False

        # Detect keyboard input
        if event.type == pygame.KEYDOWN:

            # Restart the game by pressing R after game over
            if game_over and event.key == pygame.K_r:

                player, bullets, start_time, last_bullet_time = reset_game()

                final_survival_time = 0
                game_over = False

    # --------------------------------------------------
    # Game logic
    # --------------------------------------------------

    if not game_over:

        # Get the current keyboard state
        keys = pygame.key.get_pressed()

        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed

        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed

        # Move up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= player_speed

        # Move down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += player_speed

        # Keep the player inside the screen
        if player.left < 0:
            player.left = 0

        if player.right > WIDTH:
            player.right = WIDTH

        if player.top < 0:
            player.top = 0

        if player.bottom > HEIGHT:
            player.bottom = HEIGHT

        # Calculate current survival time
        survival_time = (current_time - start_time) / 1000

        # Decrease the bullet spawn interval over time
        # The minimum interval is 200 milliseconds
        bullet_interval = max(
            200,
            800 - int(survival_time * 20)
        )

        # Create a new bullet
        if current_time - last_bullet_time > bullet_interval:

            bullets.append(create_bullet(player))

            last_bullet_time = current_time

        # Move all bullets
        for bullet in bullets:

            bullet["x"] += bullet["dx"] * bullet["speed"]
            bullet["y"] += bullet["dy"] * bullet["speed"]

        # Remove bullets that move far outside the screen
        bullets = [
            bullet for bullet in bullets
            if -50 < bullet["x"] < WIDTH + 50
            and -50 < bullet["y"] < HEIGHT + 50
        ]

        # Check collision between the player and bullets
        for bullet in bullets:

            # Create a rectangular collision area for the bullet
            bullet_rect = pygame.Rect(
                bullet["x"] - bullet["radius"],
                bullet["y"] - bullet["radius"],
                bullet["radius"] * 2,
                bullet["radius"] * 2
            )

            # Check if the player collides with the bullet
            if player.colliderect(bullet_rect):

                # Save the survival time at the moment of collision
                final_survival_time = (
                    current_time - start_time
                ) / 1000

                game_over = True
                break

    # --------------------------------------------------
    # Timer
    # --------------------------------------------------

    # Stop the timer when the game is over
    if game_over:
        survival_time = final_survival_time
    else:
        survival_time = (
            current_time - start_time
        ) / 1000

    # --------------------------------------------------
    # Drawing
    # --------------------------------------------------

    # Fill the background
    screen.fill(BLACK)

    # Draw the player
    pygame.draw.rect(
        screen,
        BLUE,
        player,
        border_radius=8
    )

    # Draw all bullets
    for bullet in bullets:

        pygame.draw.circle(
            screen,
            RED,
            (
                int(bullet["x"]),
                int(bullet["y"])
            ),
            bullet["radius"]
        )

    # Display survival time
    time_text = font.render(
        f"Survival Time : {survival_time:.1f}",
        True,
        WHITE
    )

    screen.blit(
        time_text,
        (20, 20)
    )

    # Display the number of bullets
    bullet_text = font.render(
        f"Bullets : {len(bullets)}",
        True,
        YELLOW
    )

    screen.blit(
        bullet_text,
        (20, 60)
    )

    # Display controls
    control_text = font.render(
        "Move : Arrow Keys / WASD",
        True,
        WHITE
    )

    screen.blit(
        control_text,
        (WIDTH - 330, 20)
    )

    # Display the game over screen
    if game_over:

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        score_text = font.render(
            f"You survived {survival_time:.1f} seconds!",
            True,
            WHITE
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            YELLOW
        )

        screen.blit(
            game_over_text,
            game_over_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 70
                )
            )
        )

        screen.blit(
            score_text,
            score_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2
                )
            )
        )

        screen.blit(
            restart_text,
            restart_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 + 50
                )
            )
        )

    # Update the display
    pygame.display.update()

    # Limit the game to 60 FPS
    clock.tick(FPS)


# Quit Pygame and close the program
pygame.quit()
sys.exit()