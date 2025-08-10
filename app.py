import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Feasible Region with Isoprofit Line and Variable Pine Availability")

# Slider for Pine availability
pine_avail = st.slider("Pine Availability (max 4x + 4y):", min_value=100, max_value=600, step=10, value=400)

# Slider for profit level
profit = st.slider("Select Profit Level (P = 40x + 30y):", min_value=0, max_value=6000, step=100, value=2000)

# Define x range
x_vals = np.linspace(0, 150, 400)

# Updated Pine constraint boundary
y1 = (pine_avail - 4*x_vals)/4

# Varnish constraint boundary remains fixed
y3 = 200 - 4*x_vals

# Calculate upper boundary of feasible region
y_upper = np.minimum(y1, y3)
y_upper = np.maximum(y_upper, 0)  # Ensure no negative y

fig, ax = plt.subplots(figsize=(8,6))

# Fill feasible region
ax.fill_between(x_vals, 0, y_upper, color='lightgreen', alpha=0.5, label='Feasible region')

# Plot constraint lines
ax.plot(x_vals, y1, label=f'4x + 4y ≤ {pine_avail} (Pine)')
ax.plot(x_vals, y3, label='4x + y ≤ 200 (Varnish)')

# Plot isoprofit line: y = (profit - 40x) / 30
y_profit = (profit - 40*x_vals)/30
valid = (y_profit >= 0) & (y_profit <= 150)
ax.plot(x_vals[valid], y_profit[valid], 'r--', label=f'Isoprofit line: P = {profit}')

ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
ax.set_xlabel('Units of Product X (x)')
ax.set_ylabel('Units of Product Y (y)')
ax.set_title('Feasible Region & Isoprofit Line with Variable Pine Availability')
ax.legend()
ax.grid(True)

st.pyplot(fig)
