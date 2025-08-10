import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def is_feasible(x, y, min_x, min_y):
    if x < min_x:
        return False
    if y < min_y:
        return False
    if 4*x + 4*y > 400:  # Pine
        return False
    # Laminate constraint removed
    if 4*x + y > 200:    # Varnish
        return False
    return True

st.title("LP Feasibility and Profit Calculator (No Laminate Constraint)")

# Sliders for min x and y
min_x = st.slider("Minimum units of Product X (x) allowed:", 0, 100, 20)
min_y = st.slider("Minimum units of Product Y (y) allowed:", 0, 100, 0)

# Number inputs for x and y production units
x = st.number_input(f"Enter units of Product X (x) (≥ {min_x}):", min_value=float(min_x), step=1.0)
y = st.number_input(f"Enter units of Product Y (y) (≥ {min_y}):", min_value=float(min_y), step=1.0)

if st.button("Check Feasibility and Calculate Profit"):
    feasible = is_feasible(x, y, min_x, min_y)
    profit = 40*x + 30*y
    if feasible:
        st.success(f"The point (x={x}, y={y}) is feasible.")
        st.info(f"Total profit P = 40x + 30y = {profit:.2f}")
    else:
        st.error(f"The point (x={x}, y={y}) is NOT feasible.")
        st.info(f"Profit if feasible: {profit:.2f}")

# Plotting feasible region considering min_x and min_y (no laminate constraint)
x_vals = np.linspace(0, 150, 400)

y1 = (400 - 4*x_vals)/4    # Pine
# Laminate constraint removed
y3 = 200 - 4*x_vals        # Varnish

# Upper boundary for y is min of Pine and Varnish
y_upper = np.minimum(y1, y3)
y_upper = np.maximum(y_upper, 0)

fig, ax = plt.subplots(figsize=(8,6))

# Mask for x >= min_x
mask_x = x_vals >= min_x
# y_lower = min_y
y_lower = min_y

# Fill feasible region where x >= min_x and y between y_lower and y_upper
ax.fill_between(x_vals[mask_x], y_lower, y_upper[mask_x], 
                where=(y_upper[mask_x] >= y_lower), color='lightgreen', alpha=0.5, label='Feasible region')

# Plot constraints lines
ax.plot(x_vals, y1, label='4x + 4y ≤ 400 (Pine)')
ax.plot(x_vals, y3, label='4x + y ≤ 200 (Varnish)')

# Plot vertical and horizontal lines for min_x and min_y
ax.axvline(x=min_x, color='purple', linestyle='--', label=f'x ≥ {min_x} (min x)')
ax.axhline(y=min_y, color='orange', linestyle='--', label=f'y ≥ {min_y} (min y)')

# Plot user point
ax.plot(x, y, 'ro', label='Your point (x,y)')

ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
ax.set_xlabel('Units of Product X (x)')
ax.set_ylabel('Units of Product Y (y)')
ax.set_title('Feasible Region and Your Point (No Laminate Constraint)')
ax.legend()
ax.grid(True)

st.pyplot(fig)
