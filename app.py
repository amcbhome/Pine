import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def is_feasible(x, y):
    if x < 20:          # New constraint x >= 20
        return False
    if y < 0:
        return False
    if 4*x + 4*y > 400:
        return False
    if 3*x + 5*y > 600:
        return False
    if 4*x + y > 200:
        return False
    return True

st.title("LP Feasibility Checker with Feasible Region (x ≥ 20)")

# User inputs
x = st.number_input("Enter units of Product X (x):", min_value=0.0, step=1.0)
y = st.number_input("Enter units of Product Y (y):", min_value=0.0, step=1.0)

if st.button("Check Feasibility"):
    if is_feasible(x, y):
        st.success(f"The point (x={x}, y={y}) is feasible.")
    else:
        st.error(f"The point (x={x}, y={y}) is NOT feasible.")

# Plotting feasible region with x >= 20 constraint
x_vals = np.linspace(0, 150, 400)

# Constraints lines y = f(x)
y1 = (400 - 4*x_vals)/4    # Pine
y2 = (600 - 3*x_vals)/5    # Laminate
y3 = 200 - 4*x_vals        # Varnish

# Calculate y_upper as min of constraints
y_upper = np.minimum(np.minimum(y1, y2), y3)
y_upper = np.maximum(y_upper, 0)  # avoid negative y

fig, ax = plt.subplots(figsize=(8,6))

# Mask for x >= 20
mask = x_vals >= 20

# Fill feasible region only where x >= 20
ax.fill_between(x_vals[mask], 0, y_upper[mask], color='lightgreen', alpha=0.5, label='Feasible region (x ≥ 20)')

# Plot constraint lines
ax.plot(x_vals, y1, label='4x + 4y ≤ 400 (Pine)')
ax.plot(x_vals, y2, label='3x + 5y ≤ 600 (Laminate)')
ax.plot(x_vals, y3, label='4x + y ≤ 200 (Varnish)')

# Plot vertical line for x=20 constraint
ax.axvline(x=20, color='purple', linestyle='--', label='x ≥ 20 constraint')

# Plot user point
ax.plot(x, y, 'ro', label='Your point (x,y)')

ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
ax.set_xlabel('Units of Product X (x)')
ax.set_ylabel('Units of Product Y (y)')
ax.set_title('Feasible Region and Your Point (x ≥ 20)')
ax.legend()
ax.grid(True)

st.pyplot(fig)
