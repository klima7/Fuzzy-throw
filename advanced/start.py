import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from fuzzy import get_velocity_fuzzy


# function to plot
def get_velocity_exact(alpha, distance):
    num = 9.81 * distance
    denom = np.sin(2 * np.radians(alpha))
    return np.sqrt(num / denom)


# parameters
init_amplitude = 5
init_alpha = 45
init_weight = 3.5
init_drag = 1

distances = np.linspace(0, 160, 100)

# figure
fig, ax = plt.subplots()

# exact velocity plot
velocities_exact = get_velocity_exact(init_alpha, distances)
line_exact, = plt.plot(distances, velocities_exact, lw=2)

# fuzzy velocity plot
velocities_fuzzy = get_velocity_fuzzy(init_alpha, distances)
line_fuzzy, = plt.plot(distances, velocities_fuzzy, lw=2)

# decorations
ax.set_xlabel('Distance [m]')
ax.set_ylabel('Velocity [m/s]')
ax.set_xlim([0, 160])
ax.set_ylim([0, 70])
ax.grid()

# move main plot
plt.subplots_adjust(left=0.30, bottom=0.25)


# distance slider
ax_alpha = plt.axes([0.25, 0.1, 0.65, 0.03])
alpha_slider = Slider(
    ax=ax_alpha,
    label='Angle [\N{degree sign}]',
    valmin=10,
    valmax=80,
    valinit=init_alpha,
)

ax_weight = plt.axes([0.15, 0.25, 0.0225, 0.63])
weight_slider = Slider(
    ax=ax_weight,
    label='Weight\n[kg]',
    valmin=1,
    valmax=6,
    valinit=init_weight,
    orientation='vertical'
)


ax_drag = plt.axes([0.06, 0.25, 0.0225, 0.63])
drag_slider = Slider(
    ax=ax_drag,
    label='Drag\n[1]',
    valmin=0.01,
    valmax=2,
    valinit=init_drag,
    orientation='vertical'
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
    weight_slider.reset()
    drag_slider.reset()


alpha_slider.on_changed(update)
reset_button.on_clicked(reset)

plt.show()
