import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from fuzzy import get_velocity_fuzzy


# parameters
init_amplitude = 5
init_alpha = 45
init_weight = 3.5
init_drag = 0.5

distances = np.linspace(0, 160, 80)

# figure
fig, ax = plt.subplots()

# fuzzy velocity plot
velocities_fuzzy = get_velocity_fuzzy(init_alpha, distances, init_drag, init_weight)
line_fuzzy, = plt.plot(distances, velocities_fuzzy, lw=2)

# decorations
ax.set_xlabel('Distance [m]')
ax.set_ylabel('Velocity [m/s]')
ax.set_xlim([0, 160])
ax.set_ylim([0, 70])
ax.grid()

# move main plot
plt.subplots_adjust(left=0.20, bottom=0.3)


# distance slider
ax_alpha = plt.axes([0.06, 0.25, 0.0225, 0.63])
alpha_slider = Slider(
    ax=ax_alpha,
    label='Angle [\N{degree sign}]',
    valmin=10,
    valmax=80,
    valinit=init_alpha,
    orientation='vertical'
)

ax_weight = plt.axes([0.20, 0.15, 0.70, 0.03])
weight_slider = Slider(
    ax=ax_weight,
    label='Weight [kg]',
    valmin=1,
    valmax=6,
    valinit=init_weight,
)


ax_drag = plt.axes([0.20, 0.10, 0.70, 0.03])
drag_slider = Slider(
    ax=ax_drag,
    label='Drag [1]',
    valmin=0,
    valmax=1,
    valinit=init_drag,
)


# reset button
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(ax_reset, 'Reset', hovercolor='0.975')


def update(val):
    alpha = alpha_slider.val
    weight = weight_slider.val
    drag = drag_slider.val

    # fuzzy update
    velocities = get_velocity_fuzzy(alpha, distances, drag, weight)
    line_fuzzy.set_ydata(velocities)

    fig.canvas.draw_idle()


def reset(event):
    alpha_slider.reset()
    weight_slider.reset()
    drag_slider.reset()


alpha_slider.on_changed(update)
weight_slider.on_changed(update)
drag_slider.on_changed(update)
reset_button.on_clicked(reset)

plt.show()
