import pygame
import numpy as np
from scipy import signal

pygame.init()
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Scroll Simulation")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

a, b, c = 1, 0.5, 0
A = np.array([[0, 1], [-c / a, -b / a]])
B = np.array([[0], [1 / a]])
C = np.array([[1, 1]])
D = np.array([[0]])
SS = signal.StateSpace(A, B, C, D)
t = np.linspace(0, 100, 1000)
u = np.zeros_like(t)
u[10:20] = 3
u[50:60] = -2
u[80:90] = 5
t, y, x = signal.lsim(SS, u, t)

position_scale = 50
speed_scale = 100
time_scale = 100

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Current time
    current_time = pygame.time.get_ticks() // time_scale
    if current_time < len(t):
        position = x[current_time, 0] * position_scale

        display_height = 100
        padding = 10
        # Plot a rectangle with stroke and no fill
        pygame.draw.rect(screen, WHITE, (padding, padding + position, width - 2 * padding, display_height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
