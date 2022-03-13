import numpy as np
import pymc3 as pm
from dataclasses import dataclass
from collections import Counter


@dataclass(eq=True, frozen=True)
class Arm:
    color: str
    theme: str


@dataclass
class Response:
    arm: Arm
    reward: int


class Env(object):
    arms = [
        Arm('red', 'art'),
        Arm('red', 'food'),
        Arm('blue', 'art'),
        Arm('blue', 'food')
    ]

    phis = np.array([
        [0, 0, 1],
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]).T


class User(object):
    def __init__(self):
        # color * 0.2 + theme * 0.8 - 4
        self.preferences = {}

        for arm in Env.arms:
            color = 0 if arm.color == 'red' else 1
            theme = 0 if arm.theme == 'art' else 1
            score = color * 0.2 + theme * 0.8 - 4
            self.preferences[arm] = 1 / (1 + np.exp(-score))

    def response(self, arm: Arm):
        pref = self.preferences[arm]
        return Response(arm, 1) if np.random.random() < pref else Response(arm, 0)


class StateRepository:
    def __init__(self, responses=[]):
        self.responses = responses

    @property
    def cum_rewards(self):
        rewards = []
        for arm in Env.arms:
            rewards.append(sum([res.reward for res in self.responses if res.arm == arm]))
        return rewards

    @property
    def counts(self):
        c = Counter()
        c.update({arm: 0 for arm in Env.arms})
        arms = map(lambda res: res.arm, self.responses)
        c.update(arms)
        return [c[arm] for arm in Env.arms]

    def append(self, response: Response):
        self.responses.append(response)


class BerTSAgent:
    def get_arm(self, counts, wins):
        if 0 in counts:
            return Env.arms[counts.index(0)]

        model = pm.Model()
        with model:
            beta = pm.Normal('beta', mu=0, sigma=10, shape=3)
            linpred = pm.math.dot(beta, Env.phis)
            theta = pm.Deterministic('theta', 1 / (1 + pm.math.exp(-linpred)))
            obs = pm.Binomial('obs', n=counts, p=theta, observed=wins)
            trace = pm.sample(1000, chains=1)

        sample = pm.sample_posterior_predictive(trace, samples=1, model=model, var_names=['theta'])
        idx = np.argmax(sample['theta'])
        return Env.arms[idx]