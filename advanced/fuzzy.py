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
drag = Antecedent(np.linspace(0, 1, 50), 'drag')
mass = Antecedent(np.linspace(1, 6, 50), 'mass')
vel = Consequent(np.arange(0, 70, 1), 'velocity')

vel.automf(5, names=['xl', 'l', 'm', 'h', 'xh'])
alpha.automf(5, names=['xl', 'l', 'm', 'h', 'xh'])
drag.automf(2, names=['l', 'h'])
mass.automf(2, names=['l', 'h'])

dist['z'] = fuzz.gaussmf(dist.universe, 0, 7)
dist['l'] = fuzz.trimf(dist.universe, [0, 7, 80])
dist['m'] = fuzz.trimf(dist.universe, [0, 80, 160])
dist['h'] = fuzz.trimf(dist.universe, [80, 160, 160])


vel.automf(9, names=['xxxl', 'xxl', 'xl', 'l', 'm', 'h', 'xh', 'xxh', 'xxxh'])
vel['zero'] = fuzz.trapmf(vel.universe, [0, 0, 5, 5])


plt.show()

rules = [
    Rule(dist['z'], vel['zero']),

    # Low drag
    Rule(drag['l'] & (alpha['xl'] | alpha['xh']) & dist['l'], vel['xl']),
    Rule(drag['l'] & (alpha['xl'] | alpha['xh']) & dist['m'], vel['xh']),
    Rule(drag['l'] & (alpha['xl'] | alpha['xh']) & dist['h'], vel['xxh']),

    Rule(drag['l'] & (alpha['l'] | alpha['h']) & dist['l'], vel['xxl']),
    Rule(drag['l'] & (alpha['l'] | alpha['h']) & dist['m'], vel['m']),
    Rule(drag['l'] & (alpha['l'] | alpha['h']) & dist['h'], vel['h']),

    Rule(drag['l'] & alpha['m'] & dist['l'], vel['xxl']),
    Rule(drag['l'] & alpha['m'] & dist['m'], vel['l']),
    Rule(drag['l'] & alpha['m'] & dist['h'], vel['m']),

    # high drag, low mass
    Rule(drag['h'] & mass['l'] & (alpha['xl'] | alpha['xh']) & dist['l'], vel['l']),
    Rule(drag['h'] & mass['l'] & (alpha['xl'] | alpha['xh']) & dist['m'], vel['xxh']),
    Rule(drag['h'] & mass['l'] & (alpha['xl'] | alpha['xh']) & dist['h'], vel['xxxh']),

    Rule(drag['h'] & mass['l'] & (alpha['l'] | alpha['h']) & dist['l'], vel['xl']),
    Rule(drag['h'] & mass['l'] & (alpha['l'] | alpha['h']) & dist['m'], vel['h']),
    Rule(drag['h'] & mass['l'] & (alpha['l'] | alpha['h']) & dist['h'], vel['xh']),

    Rule(drag['h'] & mass['l'] & alpha['m'] & dist['l'], vel['xl']),
    Rule(drag['h'] & mass['l'] & alpha['m'] & dist['m'], vel['m']),
    Rule(drag['h'] & mass['l'] & alpha['m'] & dist['h'], vel['h']),

    # high drag, high mass
    Rule(drag['h'] & mass['h'] & (alpha['xl'] | alpha['xh']) & dist['l'], vel['xl']),
    Rule(drag['h'] & mass['h'] & (alpha['xl'] | alpha['xh']) & dist['m'], vel['xh']),
    Rule(drag['h'] & mass['h'] & (alpha['xl'] | alpha['xh']) & dist['h'], vel['xxh']),

    Rule(drag['h'] & mass['h'] & (alpha['l'] | alpha['h']) & dist['l'], vel['xxl']),
    Rule(drag['h'] & mass['h'] & (alpha['l'] | alpha['h']) & dist['m'], vel['m']),
    Rule(drag['h'] & mass['h'] & (alpha['l'] | alpha['h']) & dist['h'], vel['h']),

    Rule(drag['h'] & mass['h'] & alpha['m'] & dist['l'], vel['xxl']),
    Rule(drag['h'] & mass['h'] & alpha['m'] & dist['m'], vel['l']),
    Rule(drag['h'] & mass['h'] & alpha['m'] & dist['h'], vel['m']),

]

throw_ctrl = ctrl.ControlSystem(rules)
throw = ctrl.ControlSystemSimulation(throw_ctrl)


def get_velocity_fuzzy_single(alpha, distance, drag, mass):
    print(alpha, distance, drag, mass)
    throw.input['alpha'] = alpha
    throw.input['distance'] = distance
    throw.input['drag'] = drag
    throw.input['mass'] = mass
    throw.compute()
    velocity = throw.output['velocity']
    return velocity


def get_velocity_fuzzy(alphas, distances, drag, mass):
    alphas, distances, drag, mass = np.broadcast_arrays(alphas, distances, drag, mass)
    velocities = []
    for alpha, distance, drag, mass in zip(alphas, distances, drag, mass):
        velocity = get_velocity_fuzzy_single(alpha, distance, drag, mass)
        velocities.append(velocity)
    return np.array(velocities)


# quick test
if __name__ == '__main__':
    print(get_velocity_fuzzy_single(45, 50, 0.5, 4))
