from dataclasses import dataclass


@dataclass
class PIDController:
    Kp: float = 0.1
    Ki: float = 0.01
    Kd: float = 0.1
    error_accumulator: float = 0
    prev_error: float = 0

    def calc_input(self, sp: float, pv: float, umin: float = -100, umax: float = 100) -> float:
        """Calculate the control signal.
        sp: Set point
        pv: Process variable
        """
        e = sp - pv
        P = self.Kp * e

        self.error_accumulator += e
        I = self.Ki * self.error_accumulator

        D = self.Kd * (e - self.prev_error)
        self.prev_error = e

        pid = P + I + D

        if pid < umin:
            u = umin
        elif pid > umax:
            u = umax
        else:
            u = pid

        # print(f"P: {P:0.2f}, I: {I:0.2f}, D: {D:0.2f}, e: {e:0.2f}, u: {u:0.2f}")
        return u