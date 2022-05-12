import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import Antecedent, Consequent, Rule
import matplotlib.pyplot as plt

alpha_range = (10, 80)
dist_range = (0, 160)
vel_range = (0, 70)

alpha = Antecedent(np.arange(10, 80, 1), 'alpha')
dist = Antecedent(np.arange(0, 160, 1), 'distance')
vel = Consequent(np.arange(0, 70, 1), 'velocity')

vel.automf(5, names=['xl', 'l', 'm', 'h', 'xh'])
alpha.automf(5, names=['xl', 'l', 'm', 'h', 'xh'])

dist['z'] = fuzz.gaussmf(dist.universe, 0, 7)
dist['l'] = fuzz.trimf(dist.universe, [0, 7, 80])
dist['m'] = fuzz.trimf(dist.universe, [0, 80, 160])
dist['h'] = fuzz.trimf(dist.universe, [80, 160, 160])


vel.automf(9, names=['xxxl', 'xxl', 'xl', 'l', 'm', 'h', 'xh', 'xxh', 'xxxh'])
vel['zero'] = fuzz.trapmf(vel.universe, [0, 0, 5, 5])


# alpha.view()
plt.show()

rules = [
    Rule((alpha['xl'] | alpha['xh']) & dist['z'], vel['zero']),
    Rule((alpha['xl'] | alpha['xh']) & dist['l'], vel['xl']),
    Rule((alpha['xl'] | alpha['xh']) & dist['m'], vel['xh']),
    Rule((alpha['xl'] | alpha['xh']) & dist['h'], vel['xxh']),

    Rule((alpha['l'] | alpha['h']) & dist['z'], vel['zero']),
    Rule((alpha['l'] | alpha['h']) & dist['l'], vel['xxl']),
    Rule((alpha['l'] | alpha['h']) & dist['m'], vel['m']),
    Rule((alpha['l'] | alpha['h']) & dist['h'], vel['h']),

    Rule(alpha['m'] & dist['z'], vel['zero']),
    Rule(alpha['m'] & dist['l'], vel['xxl']),
    Rule(alpha['m'] & dist['m'], vel['l']),
    Rule(alpha['m'] & dist['h'], vel['m']),
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
