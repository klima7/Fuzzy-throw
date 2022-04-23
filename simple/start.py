import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from fuzzy import get_velocity_fuzzy, alpha_range, dist_range, vel_range


# function to plot
def get_velocity_exact(alpha, distance):
    num = 9.81 * distance
    denom = np.sin(2 * np.radians(alpha))
    return np.sqrt(num / denom)


def show_diff_map():
    resolution = 50
    alpha_values = np.linspace(alpha_range[0], alpha_range[1], resolution)
    dist_values = np.linspace(dist_range[0], dist_range[1], resolution)

    space = np.meshgrid(alpha_values, dist_values)
    space_flat = np.dstack([*space]).reshape(-1, 2)

    exact = get_velocity_exact(space[0], space[1])
    estimated = get_velocity_fuzzy(space_flat[:, 0], space_flat[:, 1]).reshape(resolution, resolution)

    diff = estimated - exact
    fig, ax = plt.subplots()

    norm = colors.CenteredNorm(vcenter=0, clip=True, halfrange=15)
    cp = ax.contourf(space[1], space[0], diff, 200, cmap='seismic', norm=norm)

    ax.set_xlabel('Distance [m]')
    ax.set_ylabel('Angle [\N{degree sign}]')
    ax.set_title('Difference map')
    ax.grid()
    fig.colorbar(cp, label='Difference')
    fig.show()


show_diff_map()


# parameters
init_alpha = sum(alpha_range) / 2
distances = np.linspace(dist_range[0], dist_range[1], 100)

# figure
fig, ax = plt.subplots()

# exact velocity plot
velocities_exact = get_velocity_exact(init_alpha, distances)
line_exact, = plt.plot(distances, velocities_exact, lw=2, label='Exact velocity')

# fuzzy velocity plot
velocities_fuzzy = get_velocity_fuzzy(init_alpha, distances)
line_fuzzy, = plt.plot(distances, velocities_fuzzy, lw=2, label='Fuzzy velocity')

# decorations
ax.set_xlabel('Distance [m]')
ax.set_ylabel('Velocity [m/s]')
ax.set_xlim(dist_range)
ax.set_ylim(vel_range)
ax.set_title('Velocities comparison')
ax.grid()
ax.legend(loc='upper left')

# move main plot
plt.subplots_adjust(left=0.20, bottom=0.15)


# angle slider
ax_alpha = plt.axes([0.06, 0.15, 0.0225, 0.73])
alpha_slider = Slider(
    ax=ax_alpha,
    label='Angle [\N{degree sign}]',
    valmin=alpha_range[0],
    valmax=alpha_range[1],
    valinit=init_alpha,
    orientation='vertical',
)


# reset button
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(ax_reset, 'Reset', hovercolor='0.975')


def update(val):
    alpha = alpha_slider.val

    # exact update
    velocities = get_velocity_exact(alpha, distances)
    line_exact.set_ydata(velocities)

    # fuzzy update
    velocities = get_velocity_fuzzy(alpha, distances)
    line_fuzzy.set_ydata(velocities)

    fig.canvas.draw_idle()


def reset(event):
    alpha_slider.reset()


alpha_slider.on_changed(update)
reset_button.on_clicked(reset)

plt.show()
