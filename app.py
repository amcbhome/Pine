import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def is_feasible(x, y):
    if x < 0 or y < 0:
        return False
    if 4*x + 4*y > 400:
        return False
    if 3*x + 5*y > 600:
        return False
    if 4*x + y > 200:
        return False
    if 3*x + 2*y > 300:
        return False
    return True

st.title("LP Feasibility Checker with Feasible Region")

# User inputs
x = st.number_input("Enter units of Product X (x):", min_value=0.0, step=1.0)
y = st.number_input("Enter units of Product Y (y):", min_value=0.0, step=1.0)

if st.button("Check Feasibility"):
    if is_feasible(x, y):
        st.success(f"The point (x={x}, y={y}) is feasible.")
    else:
        st.error(f"The point (x={x}, y={y}) is NOT feasible.")

# Plotting feasible region
x_vals = np.linspace(0, 150, 400)

# Constraints lines expressed as y = f(x)
y1 = (400 - 4*x_vals)/4    # Pine
y2 = (600 - 3*x_vals)/5    # Laminate
y3 = 200 - 4*x_vals        # Varnish
y4 = (300 - 3*x_vals)/2    # Labour

# To plot feasible region, take minimum y values of all constraints and y>=0
y_upper = np.minimum(np.minimum(y1, y2), np.minimum(y3, y4))
y_upper = np.maximum(y_upper, 0)  # ensure no negative y in plot

fig, ax = plt.subplots(figsize=(8,6))

# Fill feasible region
ax.fill_between(x_vals, 0, y_upper, color='lightgreen', alpha=0.5, label='Feasible region')

# Plot constraint boundaries
ax.plot(x_vals, y1, label='4x + 4y ≤ 400 (Pine)')
ax.plot(x_vals, y2, label='3x + 5y ≤ 600 (Laminate)')
ax.plot(x_vals, y3, label='4x + y ≤ 200 (Varnish)')
ax.plot(x_vals, y4, label='3x + 2y ≤ 300 (Labour)')

# Plot user point
ax.plot(x, y, 'ro', label='Your point (x,y)')

ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
ax.set_xlabel('Units of Product X (x)')
ax.set_ylabel('Units of Product Y (y)')
ax.set_title('Feasible Region and Your Point')
ax.legend()
ax.grid(True)

st.pyplot(fig)
