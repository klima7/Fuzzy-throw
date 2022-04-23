import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize


def get_distance(m, k, v0, alpha):

    alpha = np.radians(alpha)

    def deriv(t, u):
        x, xdot, z, zdot = u
        speed = np.hypot(xdot, zdot)
        xdotdot = -k/m * speed * xdot
        zdotdot = -k/m * speed * zdot - 9.81
        return xdot, xdotdot, zdot, zdotdot

    u0 = 0, v0 * np.cos(alpha), 0., v0 * np.sin(alpha)
    t0, tf = 0, 50

    def hit_target(t, u):
        return u[2]

    hit_target.terminal = True
    hit_target.direction = -1

    soln = solve_ivp(deriv, (t0, tf), u0, dense_output=True, events=(hit_target,))
    distance = soln.t_events[0][0]
    return distance


def get_velocity_with_drag(alpha, distance, m, k):

    def fun(v):
        diff = distance - get_distance(m, k, v[0], alpha)
        return diff**2

    res = minimize(fun, np.array([5]), bounds=[(0, np.inf)])
    return res.x


if __name__ == '__main__':
    # print(get_distance(m=0.2, k=0.5, v0=50, alpha=65))
    print(get_velocity_with_drag(m=0.2, k=0.5, alpha=65, distance=1.00806))