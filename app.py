import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.title("Optimal Production and Profit with Variable Pine Availability")

# Slider for Pine availability
pine_avail = st.slider("Pine Availability (max 4x + 4y):", min_value=100, max_value=600, step=10, value=400)

# Coefficients for objective function (negative for linprog minimization)
c = [-40, -30]  # maximize 40x + 30y -> minimize -40x -30y

# Inequality constraint matrix and RHS vector
A = [
    [4, 4],    # 4x + 4y ≤ pine_avail
    [4, 1],    # 4x + y ≤ 200
]

b = [pine_avail, 200]

# Bounds for x and y (non-negative)
x_bounds = (0, None)
y_bounds = (0, None)

# Solve LP
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if res.success:
    x_opt, y_opt = res.x
    max_profit = 40*x_opt + 30*y_opt
    st.success(f"Optimal production: x = {x_opt:.2f}, y = {y_opt:.2f}")
    st.success(f"Maximum profit: P = {max_profit:.2f}")
else:
    st.error("Optimization failed. No feasible solution found.")
    x_opt = y_opt = max_profit = None

# Plot feasible region and optimal solution
x_vals = np.linspace(0, 150, 400)
y1 = (pine_avail - 4*x_vals)/4
y3 = 200 - 4*x_vals
y_upper = np.minimum(y1, y3)
y_upper = np.maximum(y_upper, 0)

fig, ax = plt.subplots(figsize=(8,6))

# Feasible region
ax.fill_between(x_vals, 0, y_upper, color='lightgreen', alpha=0.5, label='Feasible region')

# Constraint lines
ax.plot(x_vals, y1, label=f'4x + 4y ≤ {pine_avail} (Pine)')
ax.plot(x_vals, y3, label='4x + y ≤ 200 (Varnish)')

if res.success:
    # Plot isoprofit line at maximum profit: y = (max_profit - 40x)/30
    y_profit = (max_profit - 40*x_vals)/30
    valid = (y_profit >= 0) & (y_profit <= 150)
    ax.plot(x_vals[valid], y_profit[valid], 'r--', label=f'Isoprofit line: P = {max_profit:.2f}')
    # Plot optimal point
    ax.plot(x_opt, y_opt, 'bo', label=f'Optimal point ({x_opt:.2f}, {y_opt:.2f})')

ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
ax.set_xlabel('Units of Product X (x)')
ax.set_ylabel('Units of Product Y (y)')
ax.set_title('Feasible Region and Optimal Production Point')
ax.legend()
ax.grid(True)

st.pyplot(fig)
