

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import solve_ivp


def pendulum_ode(t, y, L, b, g=9.81):
    """
    y[0] = theta (angle from vertical, radians)
    y[1] = omega (angular velocity)
    Returns [d_theta/dt, d_omega/dt]
    """
    theta, omega = y
    d_theta = omega
    d_omega = -(b / (m * L**2)) * omega - (g / L) * np.sin(theta)
    return [d_theta, d_omega]

def solve_pendulum(L, b, theta0_deg):
    theta0 = np.radians(theta0_deg)
    t_span = (0, 20)
    t_eval = np.linspace(0, 20, 2000)
    sol = solve_ivp(
        pendulum_ode,
        t_span,
        [theta0, 0.0],
        t_eval=t_eval,
        args=(L, b),
        method='RK45'
    )
    return sol.t, sol.y[0], sol.y[1]


m = 1.0  # mass (kg)
g = 9.81


L_init      = 1.0
b_init      = 0.3
theta_init  = 45.0


fig = plt.figure(figsize=(12, 6))
fig.suptitle("Damped Pendulum Simulator", fontsize=13, fontweight='bold')
plt.subplots_adjust(left=0.07, right=0.97, top=0.88, bottom=0.28, wspace=0.35)

ax_time   = fig.add_subplot(1, 3, 1)
ax_phase  = fig.add_subplot(1, 3, 2)
ax_anim   = fig.add_subplot(1, 3, 3)


t, theta, omega = solve_pendulum(L_init, b_init, theta_init)


ax_time.set_title("Angle vs Time", fontsize=10)
ax_time.set_xlabel("Time (s)")
ax_time.set_ylabel("θ (radians)")
ax_time.grid(True, alpha=0.3)
line_time, = ax_time.plot(t, theta, color='steelblue', linewidth=1.5)


ax_phase.set_title("Phase Portrait", fontsize=10)
ax_phase.set_xlabel("θ (rad)")
ax_phase.set_ylabel("ω (rad/s)")
ax_phase.grid(True, alpha=0.3)
line_phase, = ax_phase.plot(theta, omega, color='coral', linewidth=1.2)
phase_dot, = ax_phase.plot([], [], 'ko', markersize=6)


ax_anim.set_xlim(-2, 2)
ax_anim.set_ylim(-2.2, 0.5)
ax_anim.set_aspect('equal')
ax_anim.set_title("Pendulum", fontsize=10)
ax_anim.grid(True, alpha=0.2)
ax_anim.axhline(0, color='gray', linewidth=0.5)

pivot, = ax_anim.plot([0], [0], 'ks', markersize=8)
rod,   = ax_anim.plot([], [], 'k-', linewidth=2.5)
bob,   = ax_anim.plot([], [], 'o', color='steelblue', markersize=18)
time_text = ax_anim.text(-1.8, 0.35, '', fontsize=9, color='gray')

def update_plots(L, b, theta0_deg):
    t, theta, omega = solve_pendulum(L, b, theta0_deg)

    line_time.set_data(t, theta)
    ax_time.relim(); ax_time.autoscale_view()

    line_phase.set_data(theta, omega)
    ax_phase.relim(); ax_phase.autoscale_view()

    # show pendulum at t=0
    x_bob =  L * np.sin(theta[0])
    y_bob = -L * np.cos(theta[0])
    rod.set_data([0, x_bob], [0, y_bob])
    bob.set_data([x_bob], [y_bob])
    phase_dot.set_data([theta[0]], [omega[0]])
    time_text.set_text(f'L={L:.1f}m  b={b:.2f}  θ₀={theta0_deg:.0f}°')

    fig.canvas.draw_idle()


ax_L     = plt.axes([0.10, 0.14, 0.75, 0.03])
ax_b     = plt.axes([0.10, 0.09, 0.75, 0.03])
ax_theta = plt.axes([0.10, 0.04, 0.75, 0.03])

sl_L     = Slider(ax_L,     'Length (m)',     0.3,  3.0,  valinit=L_init,     valstep=0.1)
sl_b     = Slider(ax_b,     'Damping b',      0.0,  2.0,  valinit=b_init,     valstep=0.05)
sl_theta = Slider(ax_theta, 'Initial θ (°)',  5.0,  170.0, valinit=theta_init, valstep=5.0)

def on_change(val):
    update_plots(sl_L.val, sl_b.val, sl_theta.val)

sl_L.on_changed(on_change)
sl_b.on_changed(on_change)
sl_theta.on_changed(on_change)

update_plots(L_init, b_init, theta_init)
plt.show()
