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

# alpha.automf(3, names=['l', 'm', 'h'])
# dist.automf(3, names=['l', 'm', 'h'])
vel.automf(5, names=['xl', 'l', 'm', 'h', 'xh'])

# alpha['l'] = fuzz.trimf(alpha.universe, [10, 10, 45])
# alpha['m'] = fuzz.trimf(alpha.universe, [10, 45, 80])
# alpha['h'] = fuzz.trimf(alpha.universe, [45, 80, 80])
alpha.automf(5, names=['xl', 'l', 'm', 'h', 'xh'])

# dist['z'] = fuzz.trimf(dist.universe, [0, 0, 10])
# dist['l'] = fuzz.trimf(dist.universe, [0, 10, 80])
dist['z'] = fuzz.gaussmf(dist.universe, 0, 7)
dist['l'] = fuzz.trimf(dist.universe, [0, 7, 80])
dist['m'] = fuzz.trimf(dist.universe, [0, 80, 160])
dist['h'] = fuzz.trimf(dist.universe, [80, 160, 160])


# vel['xl'] = fuzz.trimf(vel.universe, [0, 0, 17])
# vel['l'] = fuzz.trimf(vel.universe, [0, 17, 35])
# vel['m'] = fuzz.trimf(vel.universe, [17, 35, 52])
# vel['h'] = fuzz.trimf(vel.universe, [35, 52, 70])
# vel['xh'] = fuzz.trimf(vel.universe, [51, 70, 70])

vel.automf(9, names=['xxxl', 'xxl', 'xl', 'l', 'm', 'h', 'xh', 'xxh', 'xxxh'])
vel['zero'] = fuzz.trapmf(vel.universe, [0, 0, 5, 5])

# alpha_sigma = 15
# alpha['l'] = fuzz.gaussmf(alpha.universe, 10, alpha_sigma)
# alpha['m'] = fuzz.gaussmf(alpha.universe, 45, alpha_sigma)
# alpha['h'] = fuzz.gaussmf(alpha.universe, 80, alpha_sigma)
#
# dist_sigma = 30
# dist['l'] = fuzz.gaussmf(dist.universe, 0, dist_sigma)
# dist['m'] = fuzz.gaussmf(dist.universe, 80, dist_sigma)
# dist['h'] = fuzz.gaussmf(dist.universe, 160, dist_sigma)
#
# vel_sigma = 7
# vel['xl'] = fuzz.gaussmf(vel.universe, 0, vel_sigma)
# vel['l'] = fuzz.gaussmf(vel.universe, 17, vel_sigma)
# vel['m'] = fuzz.gaussmf(vel.universe, 35, vel_sigma)
# vel['h'] = fuzz.gaussmf(vel.universe, 52, vel_sigma)
# vel['xh'] = fuzz.gaussmf(vel.universe, 70, vel_sigma)

# alpha.view()
vel.view()
# vel.view()
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
