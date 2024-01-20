import pygame
from collections import deque
from dataclasses import dataclass, field

screen_x = 640
screen_y = 480
SCREEN_SIZE = (screen_x, screen_y)
DARK_GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 191, 0)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Simple 1D control")
clock = pygame.time.Clock()


def main():
    running = True

    t_sum = 0  # Accumulate time (ms)

    goal_x = 0
    obj_x = 0

    p_control = PController()
    pi_control = PIController()
    pid_control = PIDController()

    while running:
        screen.fill(DARK_GRAY)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                goal_x = event.pos[0]

        # Calculate the control signal
        # u = p_control.calc_input(goal_x, obj_x)
        # u = pi_control.calc_input(goal_x, obj_x)
        u = pid_control.calc_input(goal_x, obj_x)
        obj_x += u

        # Render the goal
        pygame.draw.line(
            screen,
            WHITE,
            (goal_x, screen_y / 2 - 10),
            (goal_x, screen_y / 2 + 10),
            1
        )

        # Render the object
        pygame.draw.circle(
            screen,
            YELLOW,
            (obj_x, screen_y / 2),
            5
        )

        t_sum += clock.get_time()
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()


@dataclass
class PController:
    Kp: float = 0.1
    bias: float = 0

    def calc_input(self, sp: float, pv: float) -> float:
        """Calculate the control signal.
        sp: Set point
        pv: Process variable
        """
        e = sp - pv
        return self.Kp * e + self.bias


@dataclass
class PIController:
    Kp: float = 0.1
    Ki: float = 0.01
    bias: float = 0
    errors: deque = field(default_factory=lambda: deque(maxlen=10))

    def calc_input(self, sp: float, pv: float) -> float:
        """Calculate the control signal.
        sp: Set point
        pv: Process variable
        """
        e = sp - pv
        P = self.Kp * e

        self.errors.append(e)
        esum = sum(self.errors)
        I = self.Ki * esum

        return self.bias + P + I


@dataclass
class PIDController:
    Kp: float = 0.1
    Ki: float = 0.01
    Kd: float = 0.1
    bias: float = 0
    errors: deque = field(default_factory=lambda: deque(maxlen=10))

    def calc_input(self, sp: float, pv: float) -> float:
        """Calculate the control signal.
        sp: Set point
        pv: Process variable
        """
        e = sp - pv
        P = self.Kp * e

        self.errors.append(e)
        esum = sum(self.errors)
        I = self.Ki * esum

        if len(self.errors) > 1:
            D = self.Kd * (e - self.errors[-2])

        return self.bias + P + I


if __name__ == "__main__":
    main()
