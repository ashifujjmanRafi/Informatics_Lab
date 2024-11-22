import pygame
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Single Car in Straight Road")

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
road_y = 0
road_height = HEIGHT * 2

# Run simulation
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update car position (basic straight-line motion)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car_y -= car_speed
    if keys[pygame.K_DOWN]:
        car_y += car_speed
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
    if keys[pygame.K_RIGHT]:
        car_x += car_speed

    # Ensure car stays within the road
    if car_y < 0:
        car_y = 0
    if car_y > HEIGHT - car_height:
        car_y = HEIGHT - car_height

    # Drawing Road
    screen.fill(WHITE)


    pygame.draw.rect(screen, BLACK, (road_x, road_y, lane_width, HEIGHT))

    # Draw lane lines
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 5, i, 10, 20))

    # Draw car
    pygame.draw.rect(screen, BLUE, (car_x, car_y, car_width, car_height))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(20)
