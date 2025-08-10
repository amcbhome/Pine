import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.title("Optimal Production and Profit with Variable Pine Availability (x ≥ 20)")

# Slider for Pine availability
pine_avail = st.slider("Pine Availability (max 6x + 4y):", min_value=100, max_value=800, step=10, value=400)

# Objective function coefficients (negative for maximization)
c = [-40, -30]  # Maximize 40x + 30y → minimize -40x - 30y

# Inequality constraints
A = [
    [6, 4],   # Pine: 6x + 4y ≤ pine_avail
    [4, 1],   # Varnish: 4x + y ≤ 200
]
b = [pine_avail, 200]

# Bounds: x ≥ 20, y ≥ 0
x_bounds = (20, None)
y_bounds = (0, None)

# Solve LP
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if res.success:
    x_opt, y_opt = res.x
    max_profit = 40 * x_opt + 30 * y_opt
    st.success(f"Optimal production: x = {x_opt:.2f}, y = {y_opt:.2f}")
    st.success(f"Maximum profit: P = {max_profit:.2f}")
else:
    st.error("Optimization failed. No feasible solution found.")
    x_opt = y_opt = max_profit = None

# Plot feasible region
x_vals = np.linspace(20, 150, 400)  # Start from x = 20
y1 = (pine_avail - 6 * x_vals) / 4
y2 = 200 - 4 * x_vals
y_upper = np.minimum(y1, y2)
y_upper = np.maximum(y_upper, 0)

fig, ax = plt.subplots(figsize=(8, 6))

# Feasible region shading
ax.fill_between(x_vals, 0, y_upper, color='lightgreen', alpha=0.5, label='Feasible region')

# Constraint lines
ax.plot(x_vals, y1, label=f'6x + 4y ≤ {pine_avail} (Pine)')
ax.plot(x_vals, y2, label='4x + y ≤ 200 (Varnish)')
ax.axvline(20, color='purple', linestyle='--', label='x ≥ 20')

# Isoprofit line & optimal point
if res.success:
    y_profit = (max_profit - 40 * x_vals) / 30
    valid = (y_profit >= 0) & (y_profit <= max(y_upper))
    ax.plot(x_vals[valid], y_profit[valid], 'r--', label=f'Isoprofit: P = {max_profit:.2f}')
    ax.plot(x_opt, y_opt, 'bo', label=f'Optimal ({x_opt:.2f}, {y_opt:.2f})')

ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
ax.set_xlabel('Units of Product X (x)')
ax.set_ylabel('Units of Product Y (y)')
ax.set_title('Feasible Region and Optimal Production Point (x ≥ 20)')
ax.legend()
ax.grid(True)

st.pyplot(fig)
