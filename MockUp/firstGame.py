import pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Intersection Mockup")

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(WHITE)

    # Draw roads
    pygame.draw.rect(screen, GRAY, (100, 0, 200, HEIGHT))  # Horizontal road
    pygame.draw.rect(screen, GRAY, (0, 100, WIDTH, 200))  # Vertical road

    # Draw traffic lights
    pygame.draw.circle(screen, RED, (250, 200), 20)  # Red light
    pygame.draw.circle(screen, GREEN, (350, 200), 20)  # Green light

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

