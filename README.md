# Damped Pendulum Simulator

An interactive physics simulator for a damped pendulum, built with Python, NumPy, SciPy and Matplotlib.


## What it does
- Models a damped pendulum by solving ODEs derived from Newton's second law
- Three interactive sliders: pendulum length, damping coefficient, initial angle
- Three live panels: angle vs time, phase portrait (θ vs ω), and animated pendulum

## The maths
The equation of motion:
```
d²θ/dt² = -(b/mL²)(dθ/dt) - (g/L)sin(θ)
```

Converted to a system of first-order ODEs and integrated using `scipy.integrate.solve_ivp` (RK45 method).

## Run it
```bash
pip install numpy matplotlib scipy
python pendulum.py
```

## What I learned
- Translating a physical system into ODEs from Newton's second law
- Numerical ODE integration using scipy
- Phase portraits as a visualisation of dynamic system behaviour
- Directly applies Engineering Mechanics coursework computationally

## Built with
Python · NumPy · SciPy · Matplotlib
