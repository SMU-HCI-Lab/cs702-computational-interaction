from collections import deque
from dataclasses import dataclass, field


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
        else:
            D = 0

        return self.bias + P + I + D
