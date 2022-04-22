import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import Antecedent, Consequent, Rule
import matplotlib.pyplot as plt


alpha = Antecedent(np.arange(10, 80, 1), 'alpha')
dist = Antecedent(np.arange(0, 160, 1), 'distance')
vel = Consequent(np.arange(0, 70, 1), 'velocity')

alpha.automf(3, names=['l', 'm', 'h'])
dist.automf(3, names=['l', 'm', 'h'])
vel.automf(3, names=['l', 'm', 'h'])

rules = [
    Rule(alpha['l'] & dist['l'], vel['l']),
    Rule(alpha['l'] & dist['m'], vel['h']),
    Rule(alpha['l'] & dist['h'], vel['h']),
    Rule(alpha['m'] & dist['l'], vel['l']),
    Rule(alpha['m'] & dist['m'], vel['m']),
    Rule(alpha['m'] & dist['h'], vel['h']),
    Rule(alpha['h'] & dist['l'], vel['l']),
    Rule(alpha['h'] & dist['m'], vel['h']),
    Rule(alpha['h'] & dist['h'], vel['h']),
]

throw_ctrl = ctrl.ControlSystem(rules)
throw = ctrl.ControlSystemSimulation(throw_ctrl)


def get_velocity_fuzzy_single(alpha, distance):
    throw.input['alpha'] = alpha
    throw.input['distance'] = distance
    throw.compute()
    velocity = throw.output['velocity']
    return velocity


def get_velocity_fuzzy(alphas, distances):
    alphas, distances = np.broadcast_arrays(alphas, distances)
    velocities = []
    for alpha, distance in zip(alphas, distances):
        velocity = get_velocity_fuzzy_single(alpha, distance)
        velocities.append(velocity)
    return np.array(velocities)


# quick test
if __name__ == '__main__':
    print(get_velocity_fuzzy_single(45, 50))
