# streamlit_app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="LP Feasible Region Visualizer", layout="centered")

st.title("Linear Programming Feasible Region with Moving Iso-Profit Line")

# Constraints:
A = np.array([[4, 4],    # Pine
              [3, 5],    # Laminate
              [4, 1],    # Varnish
              [3, 2]])   # Labour
b = np.array([400, 600, 200, 300])
labels = ["Pine: 4x + 4y ≤ 400",
          "Laminate: 3x + 5y ≤ 600",
          "Varnish: 4x + y ≤ 200",
          "Labour: 3x + 2y ≤ 300"]

# Create a meshgrid for shading feasible region
x_vals = np.linspace(0, 120, 500)
y_vals = np.linspace(0, 120, 500)
X, Y = np.meshgrid(x_vals, y_vals)

# Feasibility mask
feasible_mask = (
    (4*X + 4*Y <= 400) &
    (3*X + 5*Y <= 600) &
    (4*X + 1*Y <= 200) &
    (3*X + 2*Y <= 300)
)

# Slider for iso-profit line
P_val = st.slider("Move the iso-profit line: P = 40x + 30y = constant", 
                  min_value=0, max_value=4000, value=1000, step=50)

# Plotting
fig, ax = plt.subplots(figsize=(8, 6))

# Shade feasible region
ax.contourf(X, Y, feasible_mask, levels=[0.5, 1], colors=["#cce5ff"], alpha=0.5)

# Plot each constraint line & label
for i, (a1, a2) in enumerate(A):
    y_line = (b[i] - a1 * x_vals) / a2
    ax.plot(x_vals, y_line, label=labels[i])
    
# Iso-profit line: 40x + 30y = P_val
y_profit = (P_val - 40 * x_vals) / 30
ax.plot(x_vals, y_profit, 'r--', label=f"Iso-profit: {P_val}")

# Axes settings
ax.set_xlim(0, 120)
ax.set_ylim(0, 120)
ax.set_xlabel("x (units of Product X)")
ax.set_ylabel("y (units of Product Y)")
ax.set_title("Feasible Region & Iso-Profit Line")
ax.legend(loc="upper right", fontsize=8)
ax.grid(True)

st.pyplot(fig)
