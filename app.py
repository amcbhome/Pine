import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Feasible Region with Isoprofit Line")

# User selects a profit level with slider
profit = st.slider("Select Profit Level (P = 40x + 30y):", min_value=0, max_value=6000, step=100, value=2000)

# Constraints boundaries (no laminate constraint)
x_vals = np.linspace(0, 150, 400)

y1 = (400 - 4*x_vals)/4    # Pine: 4x + 4y ≤ 400
y3 = 200 - 4*x_vals        # Varnish: 4x + y ≤ 200

# Upper boundary for y is min of Pine and Varnish constraints
y_upper = np.minimum(y1, y3)
y_upper = np.maximum(y_upper, 0)

fig, ax = plt.subplots(figsize=(8,6))

# Fill feasible region (where y_upper >= 0)
ax.fill_between(x_vals, 0, y_upper, color='lightgreen', alpha=0.5, label='Feasible region')

# Plot constraint lines
ax.plot(x_vals, y1, label='4x + 4y ≤ 400 (Pine)')
ax.plot(x_vals, y3, label='4x + y ≤ 200 (Varnish)')

# Plot isoprofit line: 40x + 30y = profit
# Rearranged: y = (profit - 40x)/30
y_profit = (profit - 40*x_vals)/30

# Only plot where y_profit >= 0 and within plot limits
valid = (y_profit >= 0) & (y_profit <= 150)
ax.plot(x_vals[valid], y_profit[valid], 'r--', label=f'Isoprofit line: P = {profit}')

ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
ax.set_xlabel('Units of Product X (x)')
ax.set_ylabel('Units of Product Y (y)')
ax.set_title('Feasible Region and Isoprofit Line')
ax.legend()
ax.grid(True)

st.pyplot(fig)
