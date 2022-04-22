import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import Antecedent, Consequent, Rule
import matplotlib.pyplot as plt


alpha = Antecedent(np.arange(10, 80, 1), 'alpha')
dist = Antecedent(np.arange(0, 160, 1), 'distance')
vel = Consequent(np.arange(0, 70, 1), 'velocity')

# alpha.automf(3, names=['l', 'm', 'h'])
# dist.automf(3, names=['l', 'm', 'h'])
vel.automf(5, names=['xl', 'l', 'm', 'h', 'xh'])

alpha['l'] = fuzz.trimf(alpha.universe, [10, 10, 45])
alpha['m'] = fuzz.trimf(alpha.universe, [10, 45, 80])
alpha['h'] = fuzz.trimf(alpha.universe, [45, 80, 80])

dist['z'] = fuzz.gaussmf(dist.universe, 0, 10)
dist['l'] = fuzz.trimf(dist.universe, [0, 0, 80])
dist['m'] = fuzz.trimf(dist.universe, [0, 80, 160])
dist['h'] = fuzz.trimf(dist.universe, [80, 160, 160])


vel['xl'] = fuzz.trimf(vel.universe, [0, 0, 17])
vel['l'] = fuzz.trimf(vel.universe, [0, 17, 35])
vel['m'] = fuzz.trimf(vel.universe, [17, 35, 52])
vel['h'] = fuzz.trimf(vel.universe, [35, 52, 70])
vel['xh'] = fuzz.trimf(vel.universe, [51, 70, 70])

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

vel.view()
plt.show()

rules = [
    Rule((alpha['l'] | alpha['h']) & dist['z'], vel['xl']),
    Rule((alpha['l'] | alpha['h']) & dist['l'], vel['xl']),
    Rule((alpha['l'] | alpha['h']) & dist['m'], vel['h']),
    Rule((alpha['l'] | alpha['h']) & dist['h'], vel['xh']),

    Rule(alpha['m'] & dist['z'], vel['xl']),
    Rule(alpha['m'] & dist['l'], vel['xl']),
    Rule(alpha['m'] & dist['m'], vel['m']),
    Rule(alpha['m'] & dist['h'], vel['h']),
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
