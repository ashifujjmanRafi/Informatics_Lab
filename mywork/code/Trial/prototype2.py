import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Car Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
YELLOW = (255, 223, 0)
BLUE = (0, 0, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Car settings
car_width, car_height = 30, 50
car_x = WIDTH // 2 - car_width // 2  # Center of the lane
car_y = HEIGHT - car_height - 20
car_speed = 5

# Road settings
lane_width = 400
road_x = WIDTH // 2 - lane_width // 2
line_speed = 5  # Speed of road lines moving down
line_height = 20
line_spacing = 40
lines = [(HEIGHT + i * (line_height + line_spacing)) for i in range(-5, 5)]  # Initial lane line positions

# Run simulation
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update positions
    car_y -= car_speed  # Move car dynamically upward
    lines = [(line + line_speed) % (HEIGHT + line_spacing) for line in lines]  # Loop lines for scrolling effect

    # Drawing everything
    screen.fill(WHITE)

    # Draw road
    pygame.draw.rect(screen, GRAY, (road_x, 0, lane_width, HEIGHT))

    # Draw lane lines
    for line_y in lines:
        pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 5, line_y, 10, line_height))

    # Draw car
    pygame.draw.rect(screen, BLUE, (car_x, car_y, car_width, car_height))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)
