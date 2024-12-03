import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Collision Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
YELLOW = (255, 223, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Car settings
car1 = {"x": 300, "y": HEIGHT - 120, "width": 50, "height": 80, "speed": 4, "color": BLUE}
car2 = {"x": 500, "y": HEIGHT - 300, "width": 50, "height": 80, "speed": 3, "color": RED}

# Obstacle settings
construction_x = WIDTH // 2 - 50
construction_y = HEIGHT // 3
construction_width = 100
construction_height = 20

# Simulation loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update car positions
    car1["y"] -= car1["speed"]
    car2["y"] += car2["speed"]

    # Check collision
    if (
        car1["x"] < car2["x"] + car2["width"]
        and car1["x"] + car1["width"] > car2["x"]
        and car1["y"] < car2["y"] + car2["height"]
        and car1["y"] + car1["height"] > car2["y"]
    ):
        car1["speed"], car2["speed"] = 0, 0  # Stop cars on collision

    # Drawing everything
    screen.fill(WHITE)

    # Draw road
    pygame.draw.rect(screen, GRAY, (200, 0, 400, HEIGHT))

    # Draw lane lines
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 5, i, 10, 20))

    # Draw construction
    pygame.draw.rect(screen, ORANGE, (construction_x, construction_y, construction_width, construction_height))
    pygame.draw.polygon(screen, ORANGE, [(construction_x, construction_y), 
                                         (construction_x - 20, construction_y - 20), 
                                         (construction_x + construction_width + 20, construction_y - 20), 
                                         (construction_x + construction_width, construction_y)])

    # Draw stop sign
    pygame.draw.rect(screen, BLACK, (construction_x + construction_width // 2 - 15, construction_y - 60, 30, 60))
    pygame.draw.circle(screen, RED, (construction_x + construction_width // 2, construction_y - 80), 20)
    pygame.font.init()
    font = pygame.font.Font(None, 20)
    text = font.render("STOP", True, WHITE)
    screen.blit(text, (construction_x + construction_width // 2 - 12, construction_y - 88))

    # Draw cars
    pygame.draw.rect(screen, car1["color"], (car1["x"], car1["y"], car1["width"], car1["height"]))
    pygame.draw.rect(screen, car2["color"], (car2["x"], car2["y"], car2["width"], car2["height"]))

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(30)
