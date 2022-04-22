import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# function to plot
def calc_velocity(alpha, distance):
    num = 9.81 * distance
    denom = np.sin(2 * np.radians(alpha))
    return np.sqrt(num / denom)


# parameters
init_amplitude = 5
init_alpha = 20
distances = np.linspace(0, 160, 1000)

# plot
fig, ax = plt.subplots()
velocities = calc_velocity(init_alpha, distances)
line, = plt.plot(distances, velocities, lw=2)
ax.set_xlabel('Distance [m]')
ax.set_ylabel('Velocity [m/s]')
ax.set_xlim([0, 160])
ax.set_ylim([0, 70])
ax.grid()

# move main plot
plt.subplots_adjust(bottom=0.25)


# distance slider
ax_alpha = plt.axes([0.25, 0.1, 0.65, 0.03])
alpha_slider = Slider(
    ax=ax_alpha,
    label='Angle [\N{degree sign}]',
    valmin=10,
    valmax=80,
    valinit=init_alpha,
)


# reset button
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(ax_reset, 'Reset', hovercolor='0.975')


def update(val):
    alpha = alpha_slider.val
    velocities = calc_velocity(alpha, distances)
    line.set_ydata(velocities)
    fig.canvas.draw_idle()


def reset(event):
    alpha_slider.reset()


alpha_slider.on_changed(update)
reset_button.on_clicked(reset)

plt.show()
