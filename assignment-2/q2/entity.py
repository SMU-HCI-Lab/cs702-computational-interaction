import copy
import random
from dataclasses import dataclass


@dataclass
class Bird:
    x: float
    y: float
    vx: float
    vy: float
    w: float = 20
    h: float = 20


def bird_motion(bird: Bird, u: float, dt: float, gravity: float = -50) -> Bird:
    """Updates the bird's y position and velocity."""
    new_bird = copy.deepcopy(bird)
    new_bird.y = bird.y + bird.vy * dt
    new_bird.vy = bird.vy + (u + gravity) * dt
    return new_bird


@dataclass
class Pipe:
    x: float
    h: float
    w: float = 70
    gap: float = 200


def pipe_motion(pipe: Pipe, vx: float, dt: float, screen_width: int = 400) -> (Pipe, int):
    """Updates the pipe"""
    new_pipe = copy.deepcopy(pipe)
    new_pipe.x -= vx * dt

    d_score = 0
    if new_pipe.x < -pipe.w:
        new_pipe.x = screen_width
        new_pipe.h = random.randint(200, 300)
        d_score = 1
    return new_pipe, d_score
