import copy
import pygame
import random

from dataclasses import dataclass
from pid_controller import PIDController


@dataclass
class Bird:
    x: float
    y: float
    vx: float
    vy: float
    w: float = 20
    h: float = 20


@dataclass
class Pipe:
    x: float
    h: float
    w: float = 70
    gap: float = 200


# Pygame initialization and settings
pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
WHITE = (240, 240, 240)
GREEN = (0, 200, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
transform = lambda x, y: (x, SCREEN_HEIGHT - y)

# Controller
pid = PIDController(0.8, 0.01, 0.1)

# Bird variables and motion function
bird = Bird(50, 300, 30, 0)
x, y = transform(bird.x, bird.y)
bird_rect = pygame.Rect(x, y, bird.w, bird.h)


def bird_motion(bird: Bird, u: float, dt: float, gravity: float = -50) -> Bird:
    """Updates the bird's y position and velocity."""
    new_bird = copy.deepcopy(bird)
    new_bird.y = bird.y + bird.vy * dt
    new_bird.vy = bird.vy + (u + gravity) * dt
    return new_bird


# Pipe variables and motion function
pipe_height = random.randint(200, 300)
pipe = Pipe(SCREEN_WIDTH - 50, pipe_height)


def pipe_motion(pipe: Pipe, vx: float, dt: float) -> (Pipe, int):
    """Updates the pipe"""
    new_pipe = copy.deepcopy(pipe)
    new_pipe.x -= vx * dt

    d_score = 0
    if new_pipe.x < -pipe.w:
        new_pipe.x = SCREEN_WIDTH
        new_pipe.h = random.randint(200, 300)
        d_score = 1
    return new_pipe, d_score


def calculate_the_control_signal(bird: Bird, pipe: Pipe):
    """Calculate the control signal for the bird.
    You must implement your control logic here!
    """
    sp = pipe.h + pipe.gap / 2
    pv = bird.y + bird.h / 2
    u_jump = pid.calc_input(sp, pv)
    return u_jump


x, h = transform(pipe.x, pipe.h)
bottom_pipe_rect = pygame.Rect(x, 0, pipe.w, h)

x, y = transform(pipe.x, pipe.h + pipe.gap)
top_pipe_rect = pygame.Rect(x, y, pipe.w, SCREEN_HEIGHT - y)

# Clock
clock = pygame.time.Clock()
running = True
fps = 30
dt = 1 / fps

score = 0
while running:
    screen.fill(WHITE)

    # Handle events.
    u_jump = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                u_jump = 500

    # Calculate the control signal
    u_jump = calculate_the_control_signal(bird, pipe)

    # Bird dynamics
    bird = bird_motion(bird, u_jump, dt)
    x, y = transform(bird.x, bird.y)
    bird_rect.y = y

    # Pipe dynamics
    pipe, d_score = pipe_motion(pipe, bird.vx, dt)
    x, y = transform(pipe.x, pipe.h)
    bottom_pipe_rect = pygame.Rect(x, y, pipe.w, pipe.h)
    top_pipe_rect = pygame.Rect(x, 0, pipe.w, SCREEN_HEIGHT - pipe.h - pipe.gap)

    # Update the score and bird velocity
    score += d_score
    bird.vx += d_score * 10

    # Draw bird and pipes
    pygame.draw.rect(screen, GREEN, bird_rect)
    pygame.draw.rect(screen, GREEN, bottom_pipe_rect)
    pygame.draw.rect(screen, GREEN, top_pipe_rect)

    # Draw the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # Collision detection
    if bird_rect.colliderect(bottom_pipe_rect) or \
            bird_rect.colliderect(top_pipe_rect) or \
            bird.y + bird.h > 1.5 * SCREEN_HEIGHT or \
            bird.y < -0.5 * SCREEN_HEIGHT:
        running = False

    # Update the display
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
